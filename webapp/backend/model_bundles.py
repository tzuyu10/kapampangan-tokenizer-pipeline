"""Discover and validate named source-embedding bundles without loading NLLB."""
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONDITIONS = ('plain_bpe', 'morph_bpe')
SELECTION_ENV = {'plain_bpe': 'KAPAMPANGAN_PLAIN_BUNDLE',
                 'morph_bpe': 'KAPAMPANGAN_MORPH_BUNDLE'}
CHECKSUM_FILES = (
    ('source_artifact/tokenizer.json', 'tokenizer_sha256'),
    ('source_artifact/tokenizer-manifest.json', 'artifact_manifest_sha256'),
    ('nllb_source_adapter.py', 'helper_sha256'),
    ('runtime/kapampangan_morphbpe_runtime/tokenizer.py', 'runtime_sha256'),
)


def safe_bundle_name(name):
    if (not isinstance(name, str) or len(name) > 100
            or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name) is None
            or name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}):
        raise ValueError('Use a bundle name containing letters, numbers, underscores or hyphens.')
    return name


def bundle_root():
    return Path(os.environ.get('KAPAMPANGAN_MODEL_DIR', str(ROOT / 'nllb' / 'checkpoints'))).resolve()


def resolve_bundle_path(condition):
    if condition not in CONDITIONS:
        raise ValueError('Unknown model condition')
    name = safe_bundle_name(os.environ.get(SELECTION_ENV[condition], condition))
    root = bundle_root()
    path = (root / name).resolve()
    if path.parent != root:
        raise ValueError('Selected bundle must be directly inside the model directory.')
    return path


def validate_bundle(path, expected_condition=None):
    """Validate exported identities, source inventory and tensor shape before selection."""
    path = Path(path)
    manifest = json.loads((path / 'manifest.json').read_text(encoding='utf-8'))
    identity = manifest['identity']
    condition = identity['condition']
    if condition not in CONDITIONS or (expected_condition and condition != expected_condition):
        raise ValueError('Bundle condition does not match the selected Plain/Morph slot.')
    if manifest.get('source_format') != 'kapampangan_project' or manifest.get('source_id_mapping') != 'swap_0_1':
        raise ValueError('This launcher requires a project source-tokenizer bundle with swap_0_1 mapping.')
    size = manifest['source_vocab_size']
    if type(size) is not int or size < 4:
        raise ValueError('Invalid source vocabulary size')
    for name, key in CHECKSUM_FILES:
        if hashlib.sha256((path / name).read_bytes()).hexdigest() != identity[key]:
            raise ValueError('Bundle checksum mismatch: ' + name)
    artifact = path / 'source_artifact'
    inventory = (artifact / 'checksums.sha256').read_text(encoding='utf-8').splitlines()
    if not inventory:
        raise ValueError('Source artifact inventory is empty')
    listed = {'checksums.sha256'}
    for line in inventory:
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        file = (artifact / name.lstrip('*')).resolve()
        if not file.is_relative_to(artifact.resolve()):
            raise ValueError('Unsafe source inventory path')
        if hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ValueError('Source artifact checksum mismatch: ' + name)
        listed.add(file.relative_to(artifact.resolve()).as_posix())
    actual = {file.relative_to(artifact).as_posix() for file in artifact.rglob('*')
              if file.is_file() and '__pycache__' not in file.parts}
    if listed != actual:
        raise ValueError('Source artifact inventory does not match its files.')
    entries = json.loads((artifact / 'vocab.json').read_text(encoding='utf-8'))['tokens']
    if (len(entries) != size or {entry['id'] for entry in entries} != set(range(size))
            or len({entry['token'] for entry in entries}) != size):
        raise ValueError('Source vocabulary does not match the trained embedding size.')
    specials = json.loads((artifact / 'special_tokens.json').read_text(encoding='utf-8'))['special_tokens']
    if {entry['token']: entry['id'] for entry in specials} != {'<pad>': 0, '<unk>': 1, '<s>': 2, '</s>': 3}:
        raise ValueError('Unexpected project special-token layout')
    document = json.loads((artifact / 'tokenizer.json').read_text(encoding='utf-8'))
    artifact_manifest = json.loads((artifact / 'tokenizer-manifest.json').read_text(encoding='utf-8'))
    merges = json.loads((artifact / 'merges.json').read_text(encoding='utf-8'))['merges']
    if (document['vocabulary'] != entries or document['special_tokens'] != specials
            or document['merges'] != merges or artifact_manifest['actual_vocabulary_size'] != size):
        raise ValueError('Source tokenizer documents are inconsistent.')
    for name, expected in artifact_manifest['core_file_sha256'].items():
        if Path(name).name != name or hashlib.sha256((artifact / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Source artifact core checksum mismatch: ' + name)
    weights = path / 'best_source.safetensors'
    with weights.open('rb') as stream:
        header_size = int.from_bytes(stream.read(8), 'little')
        if not 1 <= header_size <= 1_000_000:
            raise ValueError('Invalid source tensor header')
        tensor = json.loads(stream.read(header_size))['weight']
    if (tensor['dtype'] != 'F32' or tensor['shape'] != [size, 1024]
            or tensor['data_offsets'] != [0, size * 1024 * 4]
            or weights.stat().st_size != 8 + header_size + size * 1024 * 4):
        raise ValueError('Source weights must be a float32 source-vocabulary by 1024 tensor.')
    for name in ('target_tokenizer/tokenizer.json', 'target_tokenizer/tokenizer_config.json'):
        if not (path / name).is_file():
            raise ValueError('Missing ' + name)
    return manifest


def bundle_metadata(path, manifest):
    path = Path(path)
    identity = manifest['identity']
    condition = identity['condition']
    variant = manifest.get('tokenizer_variant') or identity.get('tokenizer_variant')
    if not variant:
        variant = 'plain_bpe' if condition == 'plain_bpe' else 'hard_constrained'
    epochs = manifest.get('completed_epochs')
    if epochs is None and (path / 'history.json').is_file():
        history = json.loads((path / 'history.json').read_text(encoding='utf-8'))
        epochs = max((row['epoch'] for row in history), default=0)
    label = 'Plain BPE' if condition == 'plain_bpe' else 'Morph-BPE'
    description = variant.replace('_', ' ')
    title = f'{label}: {description}' if variant != 'plain_bpe' else label
    title += f' | {epochs} epochs' if epochs is not None else ''
    return dict(bundle_id=path.name, path=str(path.resolve()), condition=condition,
                display_name=f'{title} [{path.name}]', tokenizer_variant=variant,
                completed_epochs=epochs, selected_epoch=manifest.get('selected_epoch'),
                crossing_penalty=manifest.get('crossing_penalty', identity.get('crossing_penalty')),
                source_vocab_size=manifest['source_vocab_size'],
                tokenizer_sha256=identity['tokenizer_sha256'],
                model_id=manifest['model_id'], revision=manifest['revision'],
                data_sha256=identity.get('data_sha256'),
                beams=identity['beams'], max_new_tokens=identity['max_new_tokens'])


def discover_bundles(root=None):
    root = bundle_root() if root is None else Path(root).resolve()
    available, rejected = [], []
    if not root.is_dir():
        return available, rejected
    for path in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        if not path.is_dir() or path.name.startswith('.') or not (path / 'manifest.json').is_file():
            continue
        try:
            safe_bundle_name(path.name)
            if path.resolve().parent != root:
                raise ValueError('Bundle directory points outside the model directory.')
            manifest = validate_bundle(path)
            available.append(bundle_metadata(path, manifest))
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            rejected.append(dict(bundle_id=path.name, reason=str(exc)))
    return available, rejected
