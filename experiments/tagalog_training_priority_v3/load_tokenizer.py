"""Inspect an exported tokenizer using only its unchanged standard-library runtime."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, default=Path(__file__).resolve().parent / 'runtime/kapampangan_morphbpe_runtime/tokenizer.py')
    parser.add_argument('--text', required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('_portable_ordinary_bpe', args.runtime)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    tokenizer = module.Tokenizer(args.artifact)
    encoding = tokenizer.encode(args.text)
    print(json.dumps(dict(normalized_text=encoding.normalized_text,
        pieces=[token.token for token in encoding.tokens], ids=list(encoding.ids),
        offsets=[[token.start, token.end] for token in encoding.tokens],
        runtime_morphology=False), ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
