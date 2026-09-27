"""Install a trusted exported model ZIP into this checkout without changing its bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def install(archive, root=ROOT):
    destination_root=root/'nllb'/'checkpoints'
    destination_root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.install-',dir=destination_root) as temporary:
        temp=Path(temporary)
        with zipfile.ZipFile(archive) as z:
            for item in z.infolist():
                if not (temp/item.filename).resolve().is_relative_to(temp.resolve()):
                    raise ValueError('Unsafe ZIP entry')
            z.extractall(temp)
        manifest=json.loads((temp/'manifest.json').read_text(encoding='utf-8'))
        identity=manifest['identity'];condition=identity['condition']
        if condition not in ('plain_bpe','morph_bpe'):raise ValueError('Unknown model condition')
        for name,key in [('source_artifact/tokenizer.json','tokenizer_sha256'),('source_artifact/tokenizer-manifest.json','artifact_manifest_sha256'),('nllb_source_adapter.py','helper_sha256'),('runtime/kapampangan_morphbpe_runtime/tokenizer.py','runtime_sha256')]:
            if hashlib.sha256((temp/name).read_bytes()).hexdigest()!=identity[key]:raise ValueError('Checksum mismatch: '+name)
        for name in ['best_source.safetensors','target_tokenizer/tokenizer.json','target_tokenizer/tokenizer_config.json']:
            if not (temp/name).is_file():raise ValueError('Missing '+name)
        for line in (temp/'source_artifact/checksums.sha256').read_text().splitlines():
            if not line.strip():continue
            digest,name=line.split(maxsplit=1);file=(temp/'source_artifact'/name.lstrip('*')).resolve()
            if not file.is_relative_to((temp/'source_artifact').resolve()):raise ValueError('Unsafe checksum path')
            if hashlib.sha256(file.read_bytes()).hexdigest()!=digest:raise ValueError('Tokenizer checksum mismatch')
        destination=destination_root/condition
        if destination.exists():raise FileExistsError(f'{destination} already exists. Keep a backup and move it aside before replacing.')
        shutil.move(str(temp),str(destination))
    return destination

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path)
    print('Installed:',install(parser.parse_args().archive))
