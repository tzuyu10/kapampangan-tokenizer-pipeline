"""Install a trusted exported model ZIP into this checkout without changing its bytes."""
import argparse
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'webapp' / 'backend'))
import model_bundles

def install(archive, root=ROOT, name=None):
    if name is not None:
        model_bundles.safe_bundle_name(name)
    destination_root=root/'nllb'/'checkpoints'
    destination_root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.install-',dir=destination_root) as temporary:
        temp=Path(temporary)
        with zipfile.ZipFile(archive) as z:
            for item in z.infolist():
                if not (temp/item.filename).resolve().is_relative_to(temp.resolve()):
                    raise ValueError('Unsafe ZIP entry')
            z.extractall(temp)
        manifest = model_bundles.validate_bundle(temp)
        destination=destination_root/(name or manifest['identity']['condition'])
        if destination.exists():raise FileExistsError(f'{destination} already exists. Keep a backup and move it aside before replacing.')
        shutil.move(str(temp),str(destination))
    return destination

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('--name', help='Keep this variant in its own named folder; existing bundles are preserved.')
    args=parser.parse_args()
    print('Installed:',install(args.archive, name=args.name))
