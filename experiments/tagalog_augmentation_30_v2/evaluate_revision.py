"""Compare all twelve revised exports against their exact frozen predecessors."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'experiments/tagalog_augmentation_30_v1'))
from evaluate_vocab_grid import Model, reference_score, prepare_corpus, corpus_score, boot
from train_tokenizer import verify_inputs
from kapampangan_morphbpe.serialization import fingerprint, write_json, sha256_file

FAMILIES = ('weighted32', 'infix_first48', 'plain', 'unigram')
SIZES = (6080, 8192, 16384)

# Targeted debugging fixtures, never used as training rows or model selection.
# The first eight come from the supplied Filipino repository's unit tests,
# converted mechanically from underlying infix order to surface order.
FIXTURES = [
    ('kumain', ['k', 'um', 'ain'], 'upstream_test'),
    ('kinain', ['k', 'in', 'ain'], 'upstream_test'),
    ('pagkain', ['pag', 'kain'], 'upstream_test'),
    ('maganda', ['ma', 'ganda'], 'upstream_test'),
    ('pagkainan', ['pag', 'kain', 'an'], 'upstream_test'),
    ('kasiyahan', ['ka', 'siya', 'han'], 'upstream_test'),
    ('pinakamahusay', ['pinaka', 'ma', 'husay'], 'upstream_test'),
    ('pangalan', ['pangalan'], 'upstream_test'),
    ('nagaral', ['nag', 'aral'], 'user_bug_diagnostic'),
    ('nag-aral', ['nag', '-', 'aral'], 'hyphen_regression'),
    ('basahin', ['basa', 'hin'], 'suffix_regression'),
    ('sulatan', ['sulat', 'an'], 'suffix_regression'),
]


def category_counts(block, rows):
    groups = {}
    for row, predicted in zip(rows, block['predictions'], strict=True):
        group = groups.setdefault(row['process'], dict(words=0, tp=0, fp=0, fn=0, exact=0))
        group['words'] += 1
        for key in ('tp', 'fp', 'fn', 'exact'):
            group[key] += predicted[key]
    for group in groups.values():
        denominator = 2 * group['tp'] + group['fp'] + group['fn']
        group['boundary_f1'] = 2 * group['tp'] / denominator if denominator else None
    return groups


def fixtures(model):
    output = []
    for word, reference, source in FIXTURES:
        pieces, unknown = model.encode(word)
        output.append(dict(surface=word, expected=reference, pieces=pieces, exact=pieces == reference,
                           unknown=unknown, source=source))
    return dict(exact=sum(row['exact'] for row in output), words=len(output), predictions=output,
                scope='Targeted debugging checks, partly from upstream tests; not blind independent Tagalog gold.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--before', type=Path, required=True)
    args = parser.parse_args()
    root, previous = args.results.resolve(), args.before.resolve()
    reports = root / 'reports'
    manifest = verify_inputs(root / 'inputs')
    spec = importlib.util.spec_from_file_location('revision_reference_metrics', REPO / 'experiments/tokenizer_selection_v1/run_selection.py')
    selection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(selection)
    dev_path = REPO / 'experiments/tokenizer_selection_v1/data/dev.csv'
    assert sha256_file(dev_path) == 'c36f662b31d882503d7bde33a245cba6626e8b34c780a082628e1cd992b34275'
    dev = selection.load_split(dev_path)
    previous_report = json.loads((previous / 'reports/comparison.json').read_text(encoding='utf-8'))
    scores, models = {}, {}
    for phase, base in [('before', previous), ('after', root)]:
        for family in FAMILIES:
            for size in SIZES:
                key = f'{phase}_{family}_{size}'
                artifact = base / f'vocab_grid/{family}/vocab-{size}'
                model = Model(artifact, family == 'unigram')
                assert model.size == size
                block = reference_score(model, dev, selection)
                if phase == 'before':
                    assert block == previous_report['scores'][f'{family}_{size}']['dev']
                scores[key] = dict(phase=phase, family=family, vocabulary_size=size,
                    artifact=str(artifact), tokenizer_sha256=sha256_file(artifact / 'tokenizer.json'),
                    dev=block, dev_by_process=category_counts(block, dev))
                models[key] = model
                print(f'DEV {key}: F1={block["metrics"]["boundary_f1"]:.6f}', flush=True)
    rank = lambda name: (scores[name]['dev']['metrics']['boundary_f1'],
                         scores[name]['dev']['metrics']['exact_match'],
                         -scores[name]['dev']['metrics']['fertility'])
    order = sorted((key for key in scores if key.startswith('after_')), key=rank, reverse=True)
    old_order = sorted((key for key in scores if key.startswith('before_')), key=rank, reverse=True)
    selected = dict(criterion='Existing DEV boundary F1, then exact match, then lower fertility',
        ranking=order, overall_winner=order[0], previous_winner=old_order[0],
        morphology_test_read_at_selection=False, targeted_fixtures_used_for_selection=False,
        dev_csv_sha256=sha256_file(dev_path))
    write_json(reports / 'selection-before-test.json', selected)
    test_path = REPO / 'experiments/tokenizer_selection_v1/data/test.csv'
    assert sha256_file(test_path) == '1eff199e25c8969aa9f2defebff2032702465019f927829f888217b40144ed8c'
    test = selection.load_split(test_path)
    csv.field_size_limit(2**31 - 1)
    with (root / 'evaluation_inputs/kapampangan_validation.csv').open(encoding='utf-8', newline='') as stream:
        kap = list(csv.DictReader(stream))
    tag = [json.loads(line) for line in (root / 'evaluation_inputs/tagalog_unseen_articles.jsonl').read_text(encoding='utf-8').splitlines()]
    corpora = dict(kapampangan_validation=prepare_corpus(kap), tagalog_unseen_articles=prepare_corpus(tag))
    for key, score in scores.items():
        model = models[key]
        score['test'] = reference_score(model, test, selection)
        score['test_by_process'] = category_counts(score['test'], test)
        score['corpus'] = {name: corpus_score(model, corpus) for name, corpus in corpora.items()}
        score['targeted_diagnostics'] = fixtures(model)
        if score['phase'] == 'before':
            original = previous_report['scores'][f'{score["family"]}_{score["vocabulary_size"]}']
            assert score['test'] == original['test']
            assert score['corpus'] == original['corpus']
        write_json(reports / f'{key}.json', score)
        model.cache.clear()
        print('TEST/corpus complete:', key, flush=True)
    pairs = {}
    for family in FAMILIES:
        for size in SIZES:
            before, after = scores[f'before_{family}_{size}'], scores[f'after_{family}_{size}']
            pairs[f'{family}_{size}'] = dict(
                dev_boundary_f1_delta=after['dev']['metrics']['boundary_f1'] - before['dev']['metrics']['boundary_f1'],
                test_boundary_f1_delta=after['test']['metrics']['boundary_f1'] - before['test']['metrics']['boundary_f1'],
                dev_exact_count_delta=after['dev']['counts']['exact'] - before['dev']['counts']['exact'],
                dev_consistency_delta=after['dev']['metrics']['mcf1'] - before['dev']['metrics']['mcf1'])
    uncertainty = {}
    for key in dict.fromkeys([order[0], 'after_infix_first48_6080', 'after_weighted32_6080']):
        uncertainty[key] = boot(scores[key]['dev']['predictions'], scores[key.replace('after_', 'before_')]['dev']['predictions'])
    train_words = {json.loads(line)['surface'].casefold() for line in (root / 'inputs/prepared/training-stream.jsonl').read_text(encoding='utf-8').splitlines()}
    body = dict(selection=selected, scores=scores, paired_changes=pairs, exploratory_dev_bootstrap=uncertainty,
        augmented_dataset_fingerprint=manifest['augmented_dataset_fingerprint'],
        training_manifest_sha256=sha256_file(root / 'inputs/manifest.json'),
        annotation_revision=manifest['annotation_revision'], dev_rows=len(dev), test_rows=len(test),
        dev_words_in_training=sum(row['surface'].casefold() in train_words for row in dev),
        test_words_in_training=sum(row['surface'].casefold() in train_words for row in test),
        labels='Mixed silver and partial user-derived Kapampangan references, not independent native-speaker gold.',
        test_scope='Historical TEST reused; selection frozen on DEV before reading TEST in this run.',
        tagalog_gold=False, raw_corpus_and_unique_root_additions_unchanged=True,
        control_scope='Plain/Unigram do not use morphology annotations; independent Unigram EM runs may differ.',
        neural_training_or_translation_evaluation=False)
    write_json(reports / 'comparison.json', {**body, 'report_fingerprint': fingerprint(body)})
    fields = ['family', 'vocabulary', 'before_dev_f1', 'after_dev_f1', 'delta_dev_percentage_points',
              'before_test_f1', 'after_test_f1', 'before_dev_consistency', 'after_dev_consistency',
              'before_tl_fertility', 'after_tl_fertility', 'before_targeted_exact', 'after_targeted_exact']
    with (reports / 'comparison.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        for family in FAMILIES:
            for size in SIZES:
                old, new = [scores[f'{phase}_{family}_{size}'] for phase in ('before', 'after')]
                a, b = old['dev']['metrics'], new['dev']['metrics']
                writer.writerow([family, size, a['boundary_f1'], b['boundary_f1'], 100 * (b['boundary_f1'] - a['boundary_f1']),
                    old['test']['metrics']['boundary_f1'], new['test']['metrics']['boundary_f1'], a['mcf1'], b['mcf1'],
                    old['corpus']['tagalog_unseen_articles']['word_fertility'], new['corpus']['tagalog_unseen_articles']['word_fertility'],
                    old['targeted_diagnostics']['exact'], new['targeted_diagnostics']['exact']])
    lines = ['# Tagalog affix preparation revision: matched comparison', '',
        f'Highest revised DEV boundary F1: **{order[0]}**. Previous winner: **{old_order[0]}**.', '',
        'All 12 configurations were retrained. Same 34,148 records and 4,304 unique roots; 779 existing roots are now accessible to Tagalog analysis.', '',
        '| Family | Vocab | Before DEV F1 % | Revised DEV F1 % | Change, pp | Before TEST F1 % | Revised TEST F1 % |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for family in FAMILIES:
        for size in SIZES:
            a, b = [scores[f'{phase}_{family}_{size}'] for phase in ('before', 'after')]
            x, y = a['dev']['metrics']['boundary_f1'], b['dev']['metrics']['boundary_f1']
            lines.append(f'| {family} | {size:,} | {100*x:.3f} | {100*y:.3f} | {100*(y-x):+.3f} | {100*a["test"]["metrics"]["boundary_f1"]:.3f} | {100*b["test"]["metrics"]["boundary_f1"]:.3f} |')
    lines += ['', '## Interpretation limits', '',
        'DEV/TEST labels are mixed silver and user-derived. Historical TEST was previously seen, and most reference word forms occur in tokenizer training. These are exploratory comparisons.',
        'The 1,000 article-disjoint Tagalog records measure coverage and length, without independent morphology gold. Targeted fixtures are engineering checks from upstream tests and this bug, not a new blind benchmark.',
        'Plain BPE and Unigram use the unchanged plain stream. Any Unigram difference can arise from a fresh EM run and cannot be attributed to affix annotations.',
        'The 30-percent additions, original Kapampangan preparation, infix priority, vocabulary sizes and runtime algorithm stay fixed. No neural training, translation evaluation or installed webapp replacement occurred.']
    (reports / 'comparison.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(winner=order[0], paired_changes=pairs), indent=2), flush=True)


if __name__ == '__main__':
    main()
