"""Independently audit revised preparation and all paired result arithmetic."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import unicodedata

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(REPO / 'experiments/tagalog_augmentation_30_v1'))
from verify_comparison import counts_from_rows
from train_tokenizer import verify_inputs
from kapampangan_morphbpe.serialization import sha256_file, fingerprint, write_json
from kapampangan_morphbpe.pretokenizer import pretokenize_normalized
from kapampangan_morphbpe.lexicon import load_lexicon


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


def audit_inputs(root, before):
    package, original = root / 'inputs', before.parent / 'tagalog_30pct_tokenizer_inputs'
    manifest = verify_inputs(package)
    verify_inputs(original)
    unchanged = ['data/train.csv', 'data/kapampangan_train.csv', 'data/tagalog_train.jsonl',
                 'data/tagalog_train.csv', 'data/tagalog_train.txt', 'lexicons/tagalog_roots.json',
                 'lexicons/kapampangan-training-lexicon.json', 'original/kapampangan-training-stream.jsonl',
                 'prepared/plain-training-stream.jsonl']
    for name in unchanged:
        assert (package / name).read_bytes() == (original / name).read_bytes(), name
    assert manifest['counts'] == dict(kapampangan_root_entries=3311, tagalog_root_entries=993,
        combined_root_entries=4304, kapampangan_train_records=26268, tagalog_train_records=7880,
        combined_train_records=34148)
    lex = load_lexicon(package / 'lexicons/kapampangan-training-lexicon.json')
    selected = json.loads((package / 'lexicons/tagalog_roots.json').read_text(encoding='utf-8'))
    shared = json.loads((package / 'lexicons/shared_tagalog_roots.json').read_text(encoding='utf-8'))
    assert len(shared) == len({r['word'] for r in shared}) == 779
    assert {r['word'] for r in shared} <= lex.roots
    assert not {r['word'] for r in shared} & {r['word'] for r in selected}
    dictionary_path = Path(r'C:\Users\Gabo\filipino-tokenizer\filipino_tokenizer/data/tagalog_roots.json')
    assert sha256_file(dictionary_path) == manifest['sources']['tagalog_dictionary_sha256']
    dictionary = json.loads(dictionary_path.read_text(encoding='utf-8'))
    for row in shared:
        source = dictionary[row['source_dictionary_row_index']]
        assert row['word'] == unicodedata.normalize('NFC', source['word'].strip()).lower()
        for field in ['definition', 'language', 'part_of_speech', 'link']:
            assert row[field] == source[field]
    vendor = json.loads((package / 'vendor/filipino_tokenizer/data/tagalog_roots.json').read_text(encoding='utf-8'))
    assert {row['word'] for row in vendor} == {row['word'] for row in shared + selected}
    tag_rows = read_lines(package / 'data/tagalog_train.jsonl')
    token_counts = Counter((t.surface, t.kind) for row in tag_rows for t in pretokenize_normalized(row['text']))
    tag_prepared = read_lines(package / 'prepared/tagalog-training-stream.jsonl')
    assert token_counts == Counter({(r['surface'], r['kind']): r['frequency'] for r in tag_prepared})
    baseline = read_lines(package / 'original/kapampangan-training-stream.jsonl')
    expected = Counter()
    for row in baseline + tag_prepared:
        expected[(row['surface'], tuple(row['protected_boundaries']), row['kind'])] += row['frequency']
    prepared = read_lines(package / 'prepared/training-stream.jsonl')
    assert expected == Counter({(r['surface'], tuple(r['protected_boundaries']), r['kind']): r['frequency'] for r in prepared})
    roles = read_lines(package / 'prepared/role-spans.jsonl')
    assert len(roles) == len(prepared)
    for row, spans in zip(prepared, roles, strict=True):
        bounds = row['protected_boundaries']
        assert bounds == sorted(set(bounds))
        assert all(0 < value < len(row['surface']) for value in bounds)
        edges = {0, len(row['surface']), *bounds}
        for start, end, role in spans:
            assert start < end and start in edges and end in edges and role == 'infix'
    old_tag = {(r['surface'], r['kind']): r for r in read_lines(original / 'prepared/tagalog-training-stream.jsonl')}
    changed = [dict(surface=r['surface'], kind=r['kind'], frequency=r['frequency'],
                    before=old_tag[(r['surface'], r['kind'])]['protected_boundaries'],
                    after=r['protected_boundaries']) for r in tag_prepared
               if old_tag[(r['surface'], r['kind'])]['protected_boundaries'] != r['protected_boundaries']]
    write_json(root / 'reports/annotation_changes.json', changed)
    return dict(status='passed', unchanged_payload_files=len(unchanged), original_records=26268,
        added_records=7880, added_unique_roots=993, reused_shared_roots=779,
        changed_tagalog_pretoken_types=len(changed), changed_tagalog_pretoken_occurrences=sum(r['frequency'] for r in changed),
        tagalog_pretokens_independently_recounted=True, original_kapampangan_stream_unchanged=True,
        plain_stream_identical=True, role_spans_valid=True)


def independent_encoder(path, unigram):
    if unigram:
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_file(str(path / 'tokenizer.json'))
        return lambda word: tokenizer.encode(word).tokens
    document = json.loads((path / 'tokenizer.json').read_text(encoding='utf-8'))
    ranks = {(r['left'], r['right']): r['rank'] for r in document['merges']}
    vocabulary = {r['token'] for r in document['vocabulary']}
    def encode(word):
        if word in vocabulary:
            return [word]
        pieces = list(word)
        while True:
            pairs = [(ranks[(a, b)], a, b) for a, b in zip(pieces, pieces[1:]) if (a, b) in ranks]
            if not pairs:
                return pieces
            _rank, a, b = min(pairs)
            merged, index = [], 0
            while index < len(pieces):
                if index + 1 < len(pieces) and pieces[index:index + 2] == [a, b]:
                    merged.append(a + b)
                    index += 2
                else:
                    merged.append(pieces[index])
                    index += 1
            pieces = merged
    return encode


def audit_results(root, previous):
    report = json.loads((root / 'reports/comparison.json').read_text(encoding='utf-8'))
    assert fingerprint({key: value for key, value in report.items() if key != 'report_fingerprint'}) == report['report_fingerprint']
    assert len(report['scores']) == 24
    cases = 0
    for name, score in report['scores'].items():
        path = Path(score['artifact'])
        assert sha256_file(path / 'tokenizer.json') == score['tokenizer_sha256']
        for line in (path / 'checksums.sha256').read_text(encoding='utf-8').splitlines():
            digest, relative = line.split('  ', 1)
            assert sha256_file(path / relative) == digest
        encode = independent_encoder(path, score['family'] == 'unigram')
        for split in ('dev', 'test'):
            block = score[split]
            counts = counts_from_rows(block['predictions'])
            for key in ('tp', 'fp', 'fn', 'exact'):
                assert counts[key] == block['counts'][key]
            assert abs(counts['boundary_f1'] - block['metrics']['boundary_f1']) < 1e-12
            assert abs(counts['mcf1'] - block['metrics']['mcf1']) < 1e-12
            assert abs(counts['exact'] / block['rows'] - block['metrics']['exact_match']) < 1e-12
            for row in block['predictions']:
                assert encode(row['surface']) == row['pieces'], (name, row['surface'])
                cases += 1
        for corpus in score['corpus'].values():
            assert abs(corpus['word_tokens'] / corpus['word_occurrences'] - corpus['word_fertility']) < 1e-12
        if score['phase'] == 'after':
            manifest_name = 'unigram-manifest.json' if score['family'] == 'unigram' else 'tokenizer-manifest.json'
            manifest = json.loads((path / manifest_name).read_text(encoding='utf-8'))
            assert manifest['dataset_fingerprint'] == report['augmented_dataset_fingerprint']
            if score['family'] != 'unigram':
                assert manifest['protected_boundary_merge_violations'] == 0
    for family in ('weighted32', 'infix_first48', 'plain'):
        documents = [json.loads((root / f'vocab_grid/{family}/vocab-{size}/tokenizer.json').read_text(encoding='utf-8')) for size in (6080, 8192, 16384)]
        for small, large in zip(documents, documents[1:]):
            assert small['vocabulary'] == large['vocabulary'][:len(small['vocabulary'])]
            assert small['merges'] == large['merges'][:len(small['merges'])]
        if family == 'plain':
            for size, document in zip((6080, 8192, 16384), documents, strict=True):
                before = json.loads((previous / f'vocab_grid/plain/vocab-{size}/tokenizer.json').read_text(encoding='utf-8'))
                assert before['vocabulary'] == document['vocabulary'] and before['merges'] == document['merges']
    assert report['selection']['morphology_test_read_at_selection'] is False
    return dict(status='passed', independently_reencoded_reference_cases=cases, trained_configurations=12,
                paired_configurations=24, independent_metric_arithmetic=True, matching_plain_vocabularies=True,
                original_trainer_and_runtime_unchanged=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--before', type=Path, required=True)
    parser.add_argument('--inputs-only', action='store_true')
    args = parser.parse_args()
    verification = dict(inputs=audit_inputs(args.results, args.before))
    if not args.inputs_only:
        verification['results'] = audit_results(args.results, args.before)
    protected = json.loads((args.results / 'reports/protected_before.json').read_text(encoding='utf-8'))
    assert all(sha256_file(Path(name)) == digest for name, digest in protected.items())
    verification['protected_files_unchanged'] = len(protected)
    write_json(args.results / 'reports/verification.json', verification)
    print(json.dumps(verification, indent=2), flush=True)


if __name__ == '__main__':
    main()
