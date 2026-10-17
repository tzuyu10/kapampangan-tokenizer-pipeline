"""Evaluate two training-only priority variants with exact existing controls."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / 'experiments/tagalog_augmentation_30_v1'), str(REPO / 'experiments/tagalog_augmentation_30_v2')]
from evaluate_vocab_grid import Model, reference_score, prepare_corpus, corpus_score, boot
from evaluate_revision import category_counts, fixtures
from kapampangan_morphbpe.serialization import write_json, sha256_file, fingerprint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--v1', type=Path, required=True)
    parser.add_argument('--v2', type=Path, required=True)
    args = parser.parse_args()
    root = args.results.resolve()
    policy = json.loads((root / 'experiment.json').read_text(encoding='utf-8'))
    assert policy['runtime_morphology'] is False
    spec = importlib.util.spec_from_file_location('training_only_reference', REPO / 'experiments/tokenizer_selection_v1/run_selection.py')
    selection = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(selection)
    dev_path = REPO / 'experiments/tokenizer_selection_v1/data/dev.csv'
    assert sha256_file(dev_path) == 'c36f662b31d882503d7bde33a245cba6626e8b34c780a082628e1cd992b34275'
    dev = selection.load_split(dev_path)
    candidates = []
    for size in [6080, 8192]:
        candidates += [
            (f'new_infix_affix48_{size}', 'new', 'infix_affix_first48', size, root / f'vocab_grid/infix_affix_first48/vocab-{size}'),
            (f'installed_v1_infix48_{size}', 'v1', 'infix_first48', size, args.v1 / f'vocab_grid/infix_first48/vocab-{size}'),
            (f'revised_v2_infix48_{size}', 'v2', 'infix_first48', size, args.v2 / f'vocab_grid/infix_first48/vocab-{size}'),
            (f'revised_v2_weighted32_{size}', 'v2', 'weighted32', size, args.v2 / f'vocab_grid/weighted32/vocab-{size}'),
            (f'plain_{size}', 'v2', 'plain', size, args.v2 / f'vocab_grid/plain/vocab-{size}'),
            (f'unigram_{size}', 'v2', 'unigram', size, args.v2 / f'vocab_grid/unigram/vocab-{size}')]
    old_reports = {phase: json.loads((folder / 'reports/comparison.json').read_text(encoding='utf-8'))
                   for phase, folder in [('v1', args.v1), ('v2', args.v2)]}
    scores, models = {}, {}
    for key, phase, family, size, path in candidates:
        model = Model(path, family == 'unigram')
        assert model.size == size
        block = reference_score(model, dev, selection)
        if phase != 'new':
            expected = old_reports[phase]['scores'][(f'after_' if phase == 'v2' else '') + f'{family}_{size}']
            assert block == expected['dev']
        scores[key] = dict(phase=phase, family=family, vocabulary_size=size,
            artifact=str(path.resolve()), tokenizer_sha256=sha256_file(path / 'tokenizer.json'),
            dev=block, dev_by_process=category_counts(block, dev))
        models[key] = model
        print('DEV', key, block['metrics']['boundary_f1'], flush=True)
    rank = lambda key: (scores[key]['dev']['metrics']['boundary_f1'],
                        scores[key]['dev']['metrics']['exact_match'], -scores[key]['dev']['metrics']['fertility'])
    ranking = sorted(scores, key=rank, reverse=True)
    new_ranking = sorted((key for key in scores if scores[key]['phase'] == 'new'), key=rank, reverse=True)
    selected = dict(criterion='existing DEV boundary F1, exact match, lower fertility', ranking=ranking,
        new_ranking=new_ranking, overall_winner=ranking[0], new_winner=new_ranking[0],
        test_read_at_selection=False, runtime_morphology=False, budgets_frozen_before_dev=True)
    write_json(root / 'reports/selection-before-test.json', selected)
    test_path = REPO / 'experiments/tokenizer_selection_v1/data/test.csv'
    assert sha256_file(test_path) == '1eff199e25c8969aa9f2defebff2032702465019f927829f888217b40144ed8c'
    test = selection.load_split(test_path)
    csv.field_size_limit(2**31 - 1)
    with (root / 'evaluation_inputs/kapampangan_validation.csv').open(encoding='utf-8', newline='') as stream:
        kap = list(csv.DictReader(stream))
    tag = [json.loads(line) for line in (root / 'evaluation_inputs/tagalog_unseen_articles.jsonl').read_text(encoding='utf-8').splitlines()]
    corpora = dict(kapampangan_validation=prepare_corpus(kap), tagalog_unseen_articles=prepare_corpus(tag))
    for key, phase, family, size, _path in candidates:
        score, model = scores[key], models[key]
        score['test'] = reference_score(model, test, selection)
        score['test_by_process'] = category_counts(score['test'], test)
        score['corpus'] = {name: corpus_score(model, value) for name, value in corpora.items()}
        score['targeted_diagnostics'] = fixtures(model)
        if phase != 'new':
            expected = old_reports[phase]['scores'][(f'after_' if phase == 'v2' else '') + f'{family}_{size}']
            assert score['test'] == expected['test'] and score['corpus'] == expected['corpus']
        write_json(root / f'reports/{key}.json', score)
        model.cache.clear()
        print('Completed', key, flush=True)
    uncertainty, changes = {}, {}
    for size in [6080, 8192]:
        new = scores[f'new_infix_affix48_{size}']
        for phase, comparator in [('v1', f'installed_v1_infix48_{size}'), ('v2', f'revised_v2_infix48_{size}')]:
            key = f'new_{size}_minus_{phase}'
            uncertainty[key] = boot(new['dev']['predictions'], scores[comparator]['dev']['predictions'])
            changes[key] = dict(dev_boundary_f1_delta=new['dev']['metrics']['boundary_f1'] - scores[comparator]['dev']['metrics']['boundary_f1'],
                test_boundary_f1_delta=new['test']['metrics']['boundary_f1'] - scores[comparator]['test']['metrics']['boundary_f1'])
    body = dict(selection=selected, training_policy=policy, scores=scores, paired_changes=changes,
        exploratory_dev_bootstrap=uncertainty, dev_rows=len(dev), test_rows=len(test),
        runtime_morphology=False, runtime_word_overrides=False,
        evaluation_scope='mixed silver/user-derived reference, mostly training-seen words; historical TEST reuse',
        tagalog_morphology_gold=False, targeted_fixture_scope='engineering checks, not a blind morphology benchmark',
        neural_training_or_translation_evaluation=False, webapp_installation=False)
    write_json(root / 'reports/comparison.json', {**body, 'report_fingerprint': fingerprint(body)})
    fields = ['configuration', 'vocabulary', 'dev_f1', 'dev_exact', 'dev_consistency', 'test_f1',
              'dev_prefix_f1', 'dev_suffix_f1', 'dev_infix_f1', 'pam_fertility', 'tl_fertility', 'targeted_exact']
    with (root / 'reports/comparison.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        for key in ranking:
            s = scores[key]
            writer.writerow([key, s['vocabulary_size'], s['dev']['metrics']['boundary_f1'],
                s['dev']['counts']['exact'], s['dev']['metrics']['mcf1'], s['test']['metrics']['boundary_f1'],
                *[s['dev_by_process'][kind]['boundary_f1'] for kind in ['prefixation', 'suffixation', 'infixation']],
                s['corpus']['kapampangan_validation']['word_fertility'], s['corpus']['tagalog_unseen_articles']['word_fertility'],
                s['targeted_diagnostics']['exact']])
    lines = ['# Training-only affix-priority comparison', '',
        'Both new 6,080 and 8,192 configurations completed training. Runtime is unchanged ordinary BPE with no morphology lookup or per-word override.', '',
        f'Highest DEV score across all compared conditions: **{ranking[0]}**. Highest new candidate: **{new_ranking[0]}**.', '',
        '| Configuration | Vocab | DEV F1 % | Exact /272 | Consistency F1 % | Historical TEST F1 % |',
        '|---|---:|---:|---:|---:|---:|']
    for key in ranking:
        s = scores[key]
        lines.append(f'| {key} | {s["vocabulary_size"]:,} | {100*s["dev"]["metrics"]["boundary_f1"]:.3f} | {s["dev"]["counts"]["exact"]} | {100*s["dev"]["metrics"]["mcf1"]:.3f} | {100*s["test"]["metrics"]["boundary_f1"]:.3f} |')
    lines += ['', '## Targeted words', '', '| Word | Installed 6k | New 6k | New 8k |', '|---|---|---|---|']
    baseline = scores['installed_v1_infix48_6080']['targeted_diagnostics']['predictions']
    for index, word in enumerate(baseline):
        rows = [word, scores['new_infix_affix48_6080']['targeted_diagnostics']['predictions'][index],
                scores['new_infix_affix48_8192']['targeted_diagnostics']['predictions'][index]]
        lines.append('| ' + word['surface'] + ' | ' + ' | '.join(' + '.join(row['pieces']) for row in rows) + ' |')
    lines += ['', '## Scope', '',
        'Only the training role schedule changes relative to revised v2: infix budget32, other-affix budget256, no root-priority phase, then weighted penalty48. Budgets were fixed before DEV. The corpus, boundaries, 993 additions and all runtime code remain unchanged.',
        'The ordinary BPE encoder executes the learned vocabulary and merge ranks only. It does not consult any root/affix dictionary or morphology analyzer.',
        'DEV272 and historical TEST262 use mixed silver/user-derived labels; most forms occur in training and TEST has been evaluated before. Bootstrap intervals are exploratory.',
        'The 1,000 article-disjoint Tagalog records have no reviewed morphology gold; they measure coverage and sequence length. Targeted words are debugging checks, not a blind benchmark.',
        'No installed webapp artifacts, translators or neural weights were changed. No neural training or translation-quality evaluation occurred.']
    (root / 'reports/findings.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(dict(winner=ranking[0], new_winner=new_ranking[0], changes=changes), indent=2), flush=True)


if __name__ == '__main__':
    main()
