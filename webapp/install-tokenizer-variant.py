"""Install a named tokenizer-only pack without replacing any existing variant."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'webapp' / 'backend'))
import model_bundles
import tokenizer_variants


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _runtime_file(path):
    path = Path(path).resolve()
    if path.is_file() and path.name == 'tokenizer.py':
        return path
    for candidate in (path / 'tokenizer.py', path / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'):
        if candidate.is_file():
            return candidate
    raise ValueError('Runtime must be tokenizer.py, its package directory, or the runtime directory.')


def install(artifact, name, label, variant, runtime=None, root=ROOT):
    root = Path(root).resolve()
    name = model_bundles.safe_bundle_name(name)
    if not isinstance(label, str) or not label.strip() or not isinstance(variant, str) or not variant.strip():
        raise ValueError('Label and tokenizer variant must be nonempty strings.')
    artifact = Path(artifact).resolve()
    if not artifact.is_dir():
        raise ValueError('Source artifact directory does not exist.')
    for filename in ('tokenizer.json', 'tokenizer-manifest.json', 'checksums.sha256'):
        if not (artifact / filename).is_file():
            raise ValueError('Source artifact is missing ' + filename)
    runtime = _runtime_file(runtime or root / 'webapp' / 'backend' / 'tokenizer' / 'kapampangan_morphbpe_runtime')
    destination_root = root / 'webapp' / 'backend' / 'tokenizer' / 'variants'
    if destination_root.resolve().is_relative_to(artifact):
        raise ValueError('The installation directory must be outside the source artifact.')
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / name
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(str(destination) + ' already exists. Choose a new name to preserve this variant.')
    with tempfile.TemporaryDirectory(prefix='.install-', dir=destination_root) as temporary:
        pack = Path(temporary)
        shutil.copytree(artifact, pack / 'source_artifact', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        runtime_dir = pack / 'runtime' / 'kapampangan_morphbpe_runtime'
        runtime_dir.mkdir(parents=True)
        shutil.copy2(runtime, runtime_dir / 'tokenizer.py')
        initializer = runtime.parent / '__init__.py'
        if initializer.is_file():
            shutil.copy2(initializer, runtime_dir / '__init__.py')
        document = json.loads((pack / 'source_artifact' / 'tokenizer.json').read_text(encoding='utf-8'))
        info = dict(label=label, tokenizer_variant=variant, source_vocab_size=len(document['vocabulary']),
                    tokenizer_sha256=_digest(pack / 'source_artifact' / 'tokenizer.json'),
                    artifact_manifest_sha256=_digest(pack / 'source_artifact' / 'tokenizer-manifest.json'),
                    runtime_sha256=_digest(runtime_dir / 'tokenizer.py'))
        (pack / 'package_info.json').write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        tokenizer_variants.validate_package(pack)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(str(destination) + ' was created during installation. Choose a new name.')
        pack.rename(destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact', type=Path, help='Complete exported source artifact directory.')
    parser.add_argument('--name', required=True, help='Unique folder name using letters, digits, underscores or hyphens.')
    parser.add_argument('--label', required=True, help='Description shown in the Tokenization selector.')
    parser.add_argument('--variant', required=True, help='Scientific tokenizer variant, for example infix_first_penalty12.')
    parser.add_argument('--runtime', type=Path, help='Matching portable runtime file or directory. Defaults to the app runtime.')
    args = parser.parse_args()
    print('Installed tokenizer:', install(args.artifact, args.name, args.label, args.variant, args.runtime))
