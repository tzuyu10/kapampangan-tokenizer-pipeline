"""Inspect installed experimental controls and exact source sequences without NLLB."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'webapp/backend'))
import translation_service as service


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', default='Masanting ya ing abak. Komusta ka?')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'controls': service.comparison_audit(), 'conditions': {}}
    for condition in ('plain_bpe', 'morph_bpe'):
        path, manifest = service._bundle(condition)
        encoding = service.tokenize_adapted(args.text, condition)
        history_path = path/'history.json'
        history = json.loads(history_path.read_text(encoding='utf-8')) if history_path.exists() else []
        result['conditions'][condition] = {
            'cfg': manifest['cfg'],
            'adaptation': manifest['adaptation'],
            'completed_epochs': len(history) if history else None,
            'best_validation_epoch': min(history, key=lambda h: h['validation_loss'])['epoch'] if history else None,
            'tokenization': encoding,
            'unknown_count': encoding['ids'].count(1),
        }
    result['scope'] = 'Source sequences and saved controls only; no generation or translation-quality assessment.'
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered+'\n', encoding='utf-8')
    print(rendered)


if __name__ == '__main__':
    main()
