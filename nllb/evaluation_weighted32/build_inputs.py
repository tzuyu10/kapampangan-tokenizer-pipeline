"""Package the installed Plain30/weighted32 Morph30 for saved-model evaluation."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / 'notebooks' / 'NLLB_600M_Kaggle_BLEU_CHRF_30Epochs_Weighted32.ipynb'
DESTINATION = ROOT / 'release-assets' / 'evaluation_weighted32'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def build(csv_path):
    files = {}
    conditions = {}
    dataset = csv_path.read_bytes()
    for condition in ('plain_bpe', 'morph_bpe'):
        source = ROOT / 'nllb' / 'checkpoints' / condition
        manifest = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
        history = json.loads((source / 'history.json').read_text(encoding='utf-8'))
        assert manifest['identity']['condition'] == condition
        assert manifest['identity']['data_sha256'] == sha256(dataset), 'CSV differs from training data'
        assert manifest['cfg']['epochs'] == 30
        assert [row['epoch'] for row in history] == list(range(1, 31))
        assert min(history, key=lambda row: row['validation_loss'])['epoch'] == 30
        if condition == 'morph_bpe':
            assert manifest['weighted_penalty_used'] is True
            assert manifest['tokenizer_variant'] == 'weighted_penalty32'
            assert manifest['crossing_penalty'] == 32
            ui = ROOT / 'webapp/backend/tokenizer/artifacts/morphbpe-penalty32'
            for artifact in (source / 'source_artifact').iterdir():
                assert artifact.is_file() and artifact.read_bytes() == (ui / artifact.name).read_bytes(), artifact.name
        for path in sorted(source.rglob('*')):
            if not path.is_file():
                continue
            rel = path.relative_to(source)
            if any(part in ('__pycache__', 'resume_backups', 'evaluation') for part in rel.parts):
                continue
            if path.name == 'last.pt' or path.suffix in ('.pyc', '.zip'):
                continue
            files[f'{condition}/{rel.as_posix()}'] = path.read_bytes()
        conditions[condition] = dict(
            completed_epochs=30, selected_epoch=30,
            weights_sha256=sha256(files[f'{condition}/best_source.safetensors']),
            tokenizer_sha256=sha256(files[f'{condition}/source_artifact/tokenizer.json']),
            tokenizer_variant=manifest.get('tokenizer_variant', 'plain_bpe'),
            weighted_penalty_used=manifest.get('weighted_penalty_used', False),
            crossing_penalty=manifest.get('crossing_penalty'))
    files['kpm_tgl_cleaned.csv'] = dataset
    info = dict(purpose='Current Plain30 versus weighted penalty32 Morph30 evaluation',
                notebook=NOTEBOOK.name, notebook_sha256=sha256(NOTEBOOK.read_bytes()),
                data_sha256=sha256(dataset), conditions=conditions,
                files={name: sha256(data) for name, data in files.items()})
    files['_package_info.json'] = (json.dumps(info, indent=2) + '\n').encode()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    archive = DESTINATION / 'kaggle_bleu_chrf_inputs_30epochs_weighted32.zip'
    if archive.exists():
        raise FileExistsError(f'Refusing to overwrite {archive}')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for name, data in files.items():
            zipped.writestr(name, data)
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None
        assert set(zipped.namelist()) == set(files)
        for name, data in files.items():
            assert zipped.read(name) == data, name
    checksum = sha256(archive.read_bytes())
    (DESTINATION / 'SHA256SUMS.txt').write_text(f'{checksum}  {archive.name}\n', encoding='utf-8')
    print(json.dumps(dict(path=str(archive), bytes=archive.stat().st_size, sha256=checksum,
                         files=len(files), conditions=conditions), indent=2))
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', type=Path)
    build(parser.parse_args().csv)
