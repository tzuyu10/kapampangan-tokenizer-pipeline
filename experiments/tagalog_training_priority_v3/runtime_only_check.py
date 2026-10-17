"""Check ordinary BPE in isolation, without morphology imports or resources."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unicodedata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()
    root = args.results.resolve()
    source = root / 'inputs/runtime/kapampangan_morphbpe_runtime/tokenizer.py'
    spec = importlib.util.spec_from_file_location('_isolated_ordinary_bpe', source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    words = []
    for split in ['dev', 'test']:
        with (root / f'evaluation_inputs/{split}.csv').open(encoding='utf-8') as stream:
            words.extend(row['surface'] for row in csv.DictReader(stream))
    extra = ['nagaral', 'nag-aral', 'sinulat', 'kumain', 'basahin', 'sulatan',
             '  Nag-aral\tku.\n', 'Masa\u0301nting', '\U00020000', '', '<unk>']
    cases, outputs = 0, {}
    for size in [6080, 8192]:
        tokenizer = module.Tokenizer(root / f'vocab_grid/infix_affix_first48/vocab-{size}')
        assert tokenizer.vocabulary_size == size
        for word in words + extra:
            result = tokenizer.encode(word)
            assert result.normalized_text == unicodedata.normalize('NFC', word)
            for token in result.tokens:
                assert 0 <= token.start <= token.end <= len(result.normalized_text)
                assert tokenizer.token_to_id[token.token] == token.identifier
                if token.identifier != tokenizer.special_by_role['unk'][1]:
                    assert result.normalized_text[token.start:token.end] == token.token
            if 1 not in result.ids:
                assert tokenizer.decode(result.ids) == result.normalized_text
            cases += 1
        outputs[str(size)] = {word: [token.token for token in tokenizer.encode(word).tokens] for word in extra[:6]}
    forbidden = [name for name in sys.modules if name.startswith(('filipino_tokenizer', 'expanded_morphology', 'kapampangan_morphbpe.lexicon'))]
    assert not forbidden, forbidden
    report = dict(status='passed', runtime_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  reference_and_edge_cases=cases, morphology_modules_loaded=forbidden,
                  ordinary_runtime_only=True, diagnostic_outputs=outputs)
    (root / 'reports/runtime-only-verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
