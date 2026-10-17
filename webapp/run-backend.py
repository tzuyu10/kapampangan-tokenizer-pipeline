"""Launch the backend with named Plain BPE and Morph-BPE model variants."""
import argparse
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'webapp' / 'backend'))
import model_bundles


def choose_bundle(condition, available):
    candidates = [item for item in available if item['condition'] == condition]
    label = 'Plain BPE' if condition == 'plain_bpe' else 'Morph-BPE'
    if not candidates:
        print(f'No installed {label} bundles. This translation slot will be unavailable.')
        return None
    current = os.environ.get(model_bundles.SELECTION_ENV[condition], condition)
    default = next((i for i, item in enumerate(candidates, 1) if item['bundle_id'] == current), 1)
    print(f'\nChoose the {label} model:')
    for index, item in enumerate(candidates, 1):
        print(f"  {index}. {item['display_name']}" + (' (default)' if index == default else ''))
    while True:
        try:
            answer = input(f'Number or bundle name [Enter = {default}; q = cancel]: ').strip()
        except EOFError as exc:
            raise ValueError('Interactive selection needs a terminal. Use --plain-bundle and --morph-bundle instead.') from exc
        if answer.lower() == 'q':
            raise KeyboardInterrupt
        if not answer:
            return candidates[default - 1]['bundle_id']
        if answer.isdigit() and 1 <= int(answer) <= len(candidates):
            return candidates[int(answer) - 1]['bundle_id']
        if any(item['bundle_id'] == answer for item in candidates):
            return answer
        print('Choose one of the listed bundles.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list-models', action='store_true', help='List usable installed variants and exit.')
    parser.add_argument('--select-models', action='store_true', help='Choose each translation bundle from a menu.')
    parser.add_argument('--plain-bundle', metavar='NAME', help='Named installed bundle for the Plain BPE slot.')
    parser.add_argument('--morph-bundle', metavar='NAME', help='Named installed bundle for the Morph-BPE slot.')
    parser.add_argument('--defaults', action='store_true', help='Use the original plain_bpe and morph_bpe folders.')
    args = parser.parse_args(argv)
    if args.select_models and (args.plain_bundle or args.morph_bundle or args.defaults):
        parser.error('Use the menu or explicit bundle names, not both.')
    if args.defaults and (args.plain_bundle or args.morph_bundle):
        parser.error('--defaults cannot be combined with bundle names.')
    os.environ.setdefault('HF_HOME', str(ROOT / '.cache' / 'huggingface'))
    os.environ.setdefault('KAPAMPANGAN_MODEL_DIR', str(ROOT / 'nllb' / 'checkpoints'))
    try:
        if args.list_models or args.select_models:
            available, rejected = model_bundles.discover_bundles()
            print('Installed translation bundles:')
            for item in available:
                print(f"  {item['display_name']} | {item['source_vocab_size']:,} source tokens")
            if not available:
                print('  None. Install a trained bundle with webapp/install-model-bundle.py.')
            for item in rejected:
                print(f"  Unavailable: {item['bundle_id']}: {item['reason']}")
            if args.list_models:
                return 0
            for condition in model_bundles.CONDITIONS:
                chosen = choose_bundle(condition, available)
                if chosen is not None:
                    os.environ[model_bundles.SELECTION_ENV[condition]] = chosen
        if args.defaults:
            for condition in model_bundles.CONDITIONS:
                os.environ.pop(model_bundles.SELECTION_ENV[condition], None)
        for condition, chosen in (('plain_bpe', args.plain_bundle), ('morph_bpe', args.morph_bundle)):
            if chosen is not None:
                os.environ[model_bundles.SELECTION_ENV[condition]] = model_bundles.safe_bundle_name(chosen)
            selected = model_bundles.resolve_bundle_path(condition)
            explicit = model_bundles.SELECTION_ENV[condition] in os.environ
            if explicit or selected.exists():
                manifest = model_bundles.validate_bundle(selected, condition)
                print('[models] ' + model_bundles.bundle_metadata(selected, manifest)['display_name'])
        runpy.run_path(str(ROOT / 'webapp' / 'backend' / 'server.py'), run_name='__main__')
        return 0
    except KeyboardInterrupt:
        print('\nStartup cancelled.')
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(f'Cannot start with these model selections: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
