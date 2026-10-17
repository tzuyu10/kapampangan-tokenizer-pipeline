"""Discover immutable tokenizer packs and load each pack's own portable runtime."""
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

import model_bundles

TOKENIZER_ROOT = Path(__file__).resolve().parent / 'tokenizer'
DEFAULT_TOKENIZER = 'variant:pam_tl_infix_first48_6080'
LEGACY = {
    'plain-bpe': ('Plain BPE, 6,080 tokens (Kapampangan + Tagalog)', 'plain_bpe'),
    'morphbpe-penalty32': ('Weighted Morph-BPE, penalty 32 (visualization)', 'weighted_penalty32'),
}
UNIGRAM = {'unigram-lm-6080': 6080, 'unigram-lm-8192': 8192}


def default_tokenizer():
    if (TOKENIZER_ROOT / 'variants' / DEFAULT_TOKENIZER.removeprefix('variant:')).is_dir():
        return DEFAULT_TOKENIZER
    return 'morphbpe-penalty32'


def _read_object(path):
    value = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Tokenizer metadata must be an object.')
    return value


def _check_hash(path, expected):
    if not isinstance(expected, str) or re.fullmatch(r'[0-9a-f]{64}', expected) is None:
        raise ValueError('Tokenizer package must declare a SHA-256 checksum.')
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected:
        raise ValueError('Tokenizer package checksum mismatch: ' + Path(path).name)


def _safe_child(root, name):
    name = model_bundles.safe_bundle_name(name)
    root = Path(root).resolve()
    path = (root / name).resolve()
    if path.parent != root:
        raise ValueError('Tokenizer package must stay inside its catalog directory.')
    return path


@lru_cache(maxsize=64)
def _runtime(runtime_path, runtime_sha256):
    """A distinct module avoids global package-cache reuse between trained variants."""
    path = Path(runtime_path)
    _check_hash(path, runtime_sha256)
    module_name = '_tokenizer_variant_' + hashlib.sha256(
        (str(path.resolve()) + runtime_sha256).encode('utf-8')).hexdigest()
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError('Cannot load this tokenizer runtime.')
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolves annotations through the defining module.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(module_name, None)
        raise ValueError('Cannot initialize the selected tokenizer runtime: ' + str(exc)) from exc
    return module


def _metadata(tokenizer_id, label, tokenizer_variant, size, source, **extra):
    if not isinstance(label, str) or not label.strip() or not isinstance(tokenizer_variant, str) or not tokenizer_variant:
        raise ValueError('Tokenizer label and variant must be nonempty strings.')
    return dict(id=tokenizer_id, label=label, tokenizer_variant=tokenizer_variant,
                source_vocab_size=size, source=source, **extra)


def _package_description(path, tokenizer_id):
    path = Path(path).resolve()
    info = _read_object(path / 'package_info.json')
    artifact = path / 'source_artifact'
    runtime_path = path / 'runtime' / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
    _check_hash(runtime_path, info['runtime_sha256'])
    _check_hash(artifact / 'tokenizer.json', info['tokenizer_sha256'])
    _check_hash(artifact / 'tokenizer-manifest.json', info['artifact_manifest_sha256'])
    return artifact, runtime_path, info['runtime_sha256'], dict(
        id=tokenizer_id, label=info['label'], tokenizer_variant=info['tokenizer_variant'],
        source='tokenizer', declared_size=info['source_vocab_size'])


def _description(tokenizer_id):
    """Resolve an explicit ID only. Unknown selections never fall back to legacy32."""
    if not isinstance(tokenizer_id, str):
        raise ValueError('Tokenizer identifier must be a string.')
    if tokenizer_id == 'variant:pam_tl_plain_6080':
        artifact, runtime, checksum, info = _description('plain-bpe')
        return artifact, runtime, checksum, dict(info, id=tokenizer_id)
    if tokenizer_id in LEGACY:
        label, variant = LEGACY[tokenizer_id]
        artifact = TOKENIZER_ROOT / 'artifacts' / tokenizer_id
        runtime_path = TOKENIZER_ROOT / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
        runtime_hash = hashlib.sha256(runtime_path.read_bytes()).hexdigest()
        return artifact, runtime_path, runtime_hash, dict(
            id=tokenizer_id, label=label, tokenizer_variant=variant, source='tokenizer')
    if tokenizer_id.startswith('variant:'):
        path = _safe_child(TOKENIZER_ROOT / 'variants', tokenizer_id.removeprefix('variant:'))
        return _package_description(path, tokenizer_id)
    if tokenizer_id.startswith('trained:'):
        path = _safe_child(model_bundles.bundle_root(), tokenizer_id.removeprefix('trained:'))
        manifest = model_bundles.validate_bundle(path)
        info = model_bundles.bundle_metadata(path, manifest)
        runtime_path = path / 'runtime' / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
        return path / 'source_artifact', runtime_path, manifest['identity']['runtime_sha256'], dict(
            id=tokenizer_id, label=info['display_name'], tokenizer_variant=info['tokenizer_variant'],
            source='trained_bundle', bundle_id=path.name,
            declared_size=manifest['source_vocab_size'])
    raise ValueError('Unknown tokenizer identifier: ' + tokenizer_id)


@lru_cache(maxsize=64)
def _tokenizer(artifact_path, runtime_path, runtime_hash, artifact_hash):
    module = _runtime(runtime_path, runtime_hash)
    tokenizer = module.Tokenizer(Path(artifact_path))
    return tokenizer, module._pretokenize


def _load_description(description):
    artifact, runtime_path, runtime_hash, info = description
    artifact_hash = hashlib.sha256((artifact / 'tokenizer.json').read_bytes()).hexdigest()
    # Validate the complete immutable inventory before using a cached instance.
    module = _runtime(str(runtime_path.resolve()), runtime_hash)
    inventory_validator = module.Tokenizer.__new__(module.Tokenizer)
    inventory_validator.artifact_dir = artifact.resolve()
    inventory_validator._validate_checksums()
    tokenizer, pretokenize = _tokenizer(str(artifact.resolve()), str(runtime_path.resolve()),
                                       runtime_hash, artifact_hash)
    declared = info.pop('declared_size', None)
    if declared is not None and (type(declared) is not int or declared != tokenizer.vocabulary_size):
        raise ValueError('Tokenizer package vocabulary size does not match its artifact.')
    metadata = _metadata(size=tokenizer.vocabulary_size, tokenizer_id=info.pop('id'),
                         **info, algorithm='bpe', tokenizer_sha256=artifact_hash, runtime_sha256=runtime_hash)
    return tokenizer, pretokenize, metadata


@lru_cache(maxsize=8)
def _unigram(artifact_path, artifact_hash, manifest_hash):
    from unigram_runtime import Tokenizer
    return Tokenizer(Path(artifact_path))


def _load_unigram(tokenizer_id):
    from unigram_runtime import Tokenizer, _pretokenize
    artifact = (TOKENIZER_ROOT / 'artifacts' / tokenizer_id).resolve()
    validator = Tokenizer.__new__(Tokenizer)
    validator.artifact_dir = artifact
    validator._validate_checksums()
    artifact_hash = hashlib.sha256((artifact / 'tokenizer.json').read_bytes()).hexdigest()
    manifest_hash = hashlib.sha256((artifact / 'unigram-manifest.json').read_bytes()).hexdigest()
    tok = _unigram(str(artifact), artifact_hash, manifest_hash)
    size = UNIGRAM[tokenizer_id]
    if tok.vocabulary_size != size:
        raise ValueError('Unigram vocabulary size does not match its catalog entry.')
    runtime_hash = hashlib.sha256((TOKENIZER_ROOT / 'unigram_runtime.py').read_bytes()).hexdigest()
    info = _metadata(tokenizer_id, f'Unigram-LM, {size:,} tokens (Kapampangan + Tagalog)',
                     'unigram_lm', size, 'tokenizer', algorithm='unigram_lm',
                     tokenizer_sha256=artifact_hash, runtime_sha256=runtime_hash)
    return tok, _pretokenize, info


def validate_package(path):
    """Validate a standalone pack before installation without depending on its folder ID."""
    try:
        _tokenizer_instance, _pretokenize, metadata = _load_description(
            _package_description(path, 'variant:' + Path(path).name))
        return metadata
    except (OSError, KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Invalid tokenizer package: ' + str(exc)) from exc


def load(tokenizer_id=None):
    tokenizer_id = default_tokenizer() if tokenizer_id is None else tokenizer_id
    try:
        if tokenizer_id in UNIGRAM:
            return _load_unigram(tokenizer_id)
        return _load_description(_description(tokenizer_id))
    except (OSError, KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Tokenizer unavailable: ' + str(tokenizer_id) + '. ' + str(exc)) from exc


def catalog():
    """Metadata is independent of the Translator's selected startup bundles."""
    ids = list(LEGACY)
    ids += [name for name in UNIGRAM if (TOKENIZER_ROOT / 'artifacts' / name).is_dir()]
    variants = TOKENIZER_ROOT / 'variants'
    if variants.is_dir():
        ids += ['variant:' + path.name for path in sorted(variants.iterdir(), key=lambda p: p.name.casefold())
                if path.is_dir() and not path.name.startswith('.')]
    root = model_bundles.bundle_root()
    if root.is_dir():
        ids += ['trained:' + path.name for path in sorted(root.iterdir(), key=lambda p: p.name.casefold())
                if path.is_dir() and not path.name.startswith('.') and (path / 'manifest.json').is_file()]
    available, unavailable = [], []
    for tokenizer_id in ids:
        try:
            _tok, _pretokenize, info = load(tokenizer_id)
            available.append(info)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            unavailable.append(dict(id=tokenizer_id, reason=str(exc)))
    return dict(default_tokenizer=default_tokenizer(), tokenizers=available, unavailable=unavailable)
