"""Independently verify metrics, unchanged inference and immutable controls."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / 'src'), str(REPO / 'experiments/tagalog_augmentation_30_v1'),
               str(REPO / 'experiments/tagalog_augmentation_30_v2')]
from verify_comparison import counts_from_rows
from verify_revision import independent_encoder
from train_tokenizer import verify_inputs
from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--v2', type=Path, required=True)
    args = parser.parse_args()
    root = args.results.resolve()
    manifest = verify_inputs(root / 'inputs')
    old_inventory = json.loads((args.v2 / 'inputs/checksums.json').read_text(encoding='utf-8'))
    for relative, digest in old_inventory.items():
        assert sha256_file(root / 'inputs' / relative) == digest
    policy = json.loads((root / 'experiment.json').read_text(encoding='utf-8'))
    assert fingerprint({key: value for key, value in policy.items() if key != 'experiment_fingerprint'}) == policy['experiment_fingerprint']
    assert policy['priority_order'] == ['infix', 'affix', 'weighted']
    assert policy['runtime_morphology'] is False and policy['root_token_budget'] == 0
    assert policy['affix_token_budget'] == 256 and policy['infix_token_budget'] == 32
    runtime = root / 'inputs/runtime/kapampangan_morphbpe_runtime/tokenizer.py'
    assert sha256_file(runtime) == policy['runtime_sha256']
    assert runtime.read_bytes() == (REPO / 'runtime/kapampangan_morphbpe_runtime/tokenizer.py').read_bytes()
    assert runtime.read_bytes() == (REPO / 'webapp/backend/tokenizer/kapampangan_morphbpe_runtime/tokenizer.py').read_bytes()
    read_lines = lambda path: [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    prepared = read_lines(root / 'inputs/prepared/training-stream.jsonl')
    old_roles = read_lines(root / 'inputs/prepared/role-spans.jsonl')
    new_roles = read_lines(root / 'training-role-spans.jsonl')
    types, occurrences = Counter(), Counter()
    for item, before, after in zip(prepared, old_roles, new_roles, strict=True):
        assert before == [span for span in after if span[2] == 'infix']
        edges = {0, len(item['surface']), *item['protected_boundaries']}
        for a, b, role in after:
            assert a < b and a in edges and b in edges and role in {'affix', 'infix'}
            assert not any(a < edge < b for edge in item['protected_boundaries'])
            types[role] += 1
            occurrences[role] += item['frequency']
        assert all(a[1] <= b[0] for a, b in zip(after, after[1:]))
    audit = json.loads((root / 'reports/role-audit.json').read_text(encoding='utf-8'))
    assert dict(types) == audit['role_span_types'] and dict(occurrences) == audit['role_span_occurrences']
    report = json.loads((root / 'reports/comparison.json').read_text(encoding='utf-8'))
    assert fingerprint({key: value for key, value in report.items() if key != 'report_fingerprint'}) == report['report_fingerprint']
    assert len(report['scores']) == 12
    cases = 0
    for name, score in report['scores'].items():
        artifact = Path(score['artifact'])
        assert sha256_file(artifact / 'tokenizer.json') == score['tokenizer_sha256']
        encode = independent_encoder(artifact, score['family'] == 'unigram')
        for line in (artifact / 'checksums.sha256').read_text(encoding='utf-8').splitlines():
            expected, relative = line.split('  ', 1)
            assert sha256_file(artifact / relative) == expected
        for split in ['dev', 'test']:
            block = score[split]
            counts = counts_from_rows(block['predictions'])
            for key in ['tp', 'fp', 'fn', 'exact']:
                assert counts[key] == block['counts'][key]
            assert abs(counts['boundary_f1'] - block['metrics']['boundary_f1']) < 1e-12
            assert abs(counts['mcf1'] - block['metrics']['mcf1']) < 1e-12
            for row in block['predictions']:
                assert encode(row['surface']) == row['pieces'], (name, row['surface'])
                cases += 1
        for corpus in score['corpus'].values():
            assert abs(corpus['word_tokens'] / corpus['word_occurrences'] - corpus['word_fertility']) < 1e-12
        if score['phase'] == 'new':
            artifact_manifest = json.loads((artifact / 'tokenizer-manifest.json').read_text(encoding='utf-8'))
            assert artifact_manifest['protected_boundary_merge_violations'] == 0
            metadata = json.loads((artifact / 'tokenizer.json').read_text(encoding='utf-8'))['metadata']
            assert metadata['lexicon_used_at_runtime'] is False
            assert metadata['training_roles_used_at_runtime'] is False
            assert metadata['crossing_penalty'] == 48
            assert metadata['augmented_dataset_fingerprint'] == manifest['augmented_dataset_fingerprint']
            assert metadata['full_grid_training_report']['training_roles_used_at_runtime'] is False
    documents = [json.loads((root / f'vocab_grid/infix_affix_first48/vocab-{size}/tokenizer.json').read_text(encoding='utf-8')) for size in [6080, 8192]]
    assert documents[0]['vocabulary'] == documents[1]['vocabulary'][:6080]
    assert documents[0]['merges'] == documents[1]['merges'][:len(documents[0]['merges'])]
    assert report['selection']['test_read_at_selection'] is False
    isolated = json.loads((root / 'reports/runtime-only-verification.json').read_text(encoding='utf-8'))
    assert isolated['status'] == 'passed' and isolated['morphology_modules_loaded'] == []
    protected = json.loads((root / 'reports/protected_before.json').read_text(encoding='utf-8'))
    assert all(sha256_file(Path(name)) == digest for name, digest in protected.items())
    result = dict(status='passed', new_configurations=2, compared_configurations=12,
        independently_reencoded_reference_cases=cases, runtime_identical_to_installed=True,
        no_runtime_morphology=True, isolated_runtime_cases=isolated['reference_and_edge_cases'],
        original_input_inventory_files_unchanged=len(old_inventory), infix_roles_unchanged=True,
        independent_role_and_metric_arithmetic=True, protected_files_unchanged=len(protected))
    write_json(root / 'reports/verification.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
