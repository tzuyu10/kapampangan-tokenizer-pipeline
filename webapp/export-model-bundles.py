"""Export verified installed bundles for inference without modifying their files.

ZIP members start at manifest.json, as required by install-model-bundle.py.
The frozen NLLB base is downloaded separately. last.pt and caches are omitted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'webapp' / 'backend'))
import model_bundles


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def export_bundles(output, names, root=ROOT):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('Choose a new output folder; existing exports are preserved.')
    if not names or len(set(names)) != len(names):
        raise ValueError('Select at least one distinct installed bundle.')
    sources = []
    checkpoint_root = (Path(root) / 'nllb' / 'checkpoints').resolve()
    if output.is_relative_to(checkpoint_root):
        raise ValueError('Export outside nllb/checkpoints so archives cannot become model files.')
    for name in names:
        path = checkpoint_root / model_bundles.safe_bundle_name(name)
        if path.resolve().parent != checkpoint_root:
            raise ValueError('Bundle must be directly inside nllb/checkpoints.')
        manifest = model_bundles.validate_bundle(path)
        files = sorted(p for p in path.rglob('*') if p.is_file()
                       and '__pycache__' not in p.parts and p.suffix != '.pyc'
                       and p.name not in {'last.pt', '.DS_Store'})
        if any(p.is_symlink() or not p.resolve().is_relative_to(path.resolve()) for p in files):
            raise ValueError('Bundle contains a linked file outside its directory.')
        sources.append((path, manifest, files))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.export-', dir=output.parent) as temporary:
        temporary = Path(temporary)
        records = []
        for path, manifest, files in sources:
            archive = temporary / (path.name + '_inference.zip')
            hashes = {p.relative_to(path).as_posix(): digest(p) for p in files}
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
                for file in files:
                    zipped.write(file, file.relative_to(path).as_posix())
            with zipfile.ZipFile(archive) as zipped:
                if zipped.testzip() is not None or set(zipped.namelist()) != set(hashes):
                    raise ValueError('Export ZIP failed its inventory check.')
                for name, expected in hashes.items():
                    if hashlib.sha256(zipped.read(name)).hexdigest() != expected:
                        raise ValueError('Export ZIP changed ' + name)
            metadata = model_bundles.bundle_metadata(path, manifest)
            metadata.pop('path', None)
            records.append(dict(metadata, archive=archive.name, bytes=archive.stat().st_size,
                                sha256=digest(archive), files=hashes))
        (temporary / 'share-manifest.json').write_text(
            json.dumps(dict(purpose='inference only; frozen NLLB base downloaded separately',
                            bundles=records), indent=2) + '\n', encoding='utf-8')
        (temporary / 'SHA256SUMS.txt').write_text(''.join(
            f"{record['sha256']}  {record['archive']}\n" for record in records), encoding='utf-8')
        temporary.rename(output)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New private output directory.')
    parser.add_argument('--bundles', nargs='+', default=[
        'plain_bpe', 'morph_bpe', 'morph_bpe_infix_first_penalty48'])
    args = parser.parse_args()
    print('Exported:', export_bundles(args.output, args.bundles))
