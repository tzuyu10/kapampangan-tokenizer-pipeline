"""Write a readable interpretation from the already verified paired results."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()
    root = args.results
    report = json.loads((root / 'reports/comparison.json').read_text(encoding='utf-8'))
    scores = report['scores']
    lines = ['# What changed and whether it helped', '',
        'All 12 configurations were retrained. The result is mixed: weighted32 improves on DEV, while infix-first48 at 6,080 and 8,192 declines slightly on DEV. Every Morph condition improves slightly on the reused historical TEST.', '',
        'The previous infix-first48 / 6,080 remains the highest observed DEV candidate across both rounds. The revised infix-first48 / 6,080 leads only the new round. Keep the previous webapp default while further morphology evidence is gathered.', '',
        '## Controlled preparation change', '',
        '- Retained exactly 26,268 Kapampangan records plus 7,880 Tagalog records.',
        '- Retained 3,311 original roots plus 993 unique Tagalog additions.',
        '- Reused 779 original roots with source-matched Tagalog dictionary entries, making 1,772 entries accessible to the Tagalog analyzer without increasing the 4,304 unique-root total.',
        '- Added lossless annotation for known prefix-hyphen-stem forms; did not generate or rewrite training text.',
        '- Tagalog boundary-annotated occurrences rose from 10,204 to 14,940. Boundaries changed on 1,246 pretoken types / 5,066 occurrences. These are automatic coverage counts, not accuracy scores.',
        '- Kept the original Kapampangan prepared stream, affix inventory, infix priority, trainers, vocabulary sizes and runtime unchanged.', '',
        '## All twelve configurations', '',
        '| Family | Vocab | DEV F1 before % | DEV F1 revised % | Change, pp | TEST F1 before % | TEST F1 revised % |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for family in ['weighted32', 'infix_first48', 'plain', 'unigram']:
        for size in [6080, 8192, 16384]:
            a, b = [scores[f'{phase}_{family}_{size}'] for phase in ['before', 'after']]
            x, y = a['dev']['metrics']['boundary_f1'], b['dev']['metrics']['boundary_f1']
            lines.append(f'| {family} | {size:,} | {100*x:.3f} | {100*y:.3f} | {100*(y-x):+.3f} | {100*a["test"]["metrics"]["boundary_f1"]:.3f} | {100*b["test"]["metrics"]["boundary_f1"]:.3f} |')
    lines += ['', '## Other measures at 6,080', '',
        '| Condition | Exact DEV words | Consistency F1 % | PAM pieces/word | TL pieces/word |',
        '|---|---:|---:|---:|---:|']
    for family in ['infix_first48', 'weighted32']:
        for phase in ['before', 'after']:
            s = scores[f'{phase}_{family}_6080']
            lines.append(f'| {phase} {family} | {s["dev"]["counts"]["exact"]}/272 | {100*s["dev"]["metrics"]["mcf1"]:.3f} | {s["corpus"]["kapampangan_validation"]["word_fertility"]:.6f} | {s["corpus"]["tagalog_unseen_articles"]["word_fertility"]:.6f} |')
    lines += ['', 'Longer sequences can accompany better boundary protection. Fertility alone does not decide morphological quality.', '',
        '## Prefixes and suffixes at 6,080', '',
        'These are subgroup scores on the existing Kapampangan DEV reference, not Tagalog affix gold.', '',
        '| Family | DEV process | Before F1 % | Revised F1 % | Reference words |',
        '|---|---|---:|---:|---:|']
    for family in ['infix_first48', 'weighted32']:
        a, b = [scores[f'{phase}_{family}_6080'] for phase in ['before', 'after']]
        for process in ['prefixation', 'suffixation', 'infixation']:
            x, y = a['dev_by_process'][process], b['dev_by_process'][process]
            lines.append(f'| {family} | {process} | {100*x["boundary_f1"]:.3f} | {100*y["boundary_f1"]:.3f} | {x["words"]} |')
    lines += ['', '## The reported example', '',
        'The revised analyzer now recognizes `nag | aral`. Both new infix-first48 / 6,080 and / 8,192 still encode unhyphenated `nagaral` as `na | garal`. The spelling `nag-aral` improves from `nag | -a | ral` to `nag | - | aral`.', '',
        'A corrected training analysis does not impose a dictionary lookup at inference. Global BPE merge order can still join across the intended boundary on an unseen word. Fixing this particular unhyphenated result would require a separately tested change to merge-priority training or inference, rather than claiming that the current correction solved it.', '',
        '## Uncertainty', '']
    for key, block in report['exploratory_dev_bootstrap'].items():
        low, high = block['percentile95']
        lines.append(f'- {key}: DEV difference {100*block["observed_difference"]:+.3f} percentage points; exploratory 95% interval [{100*low:+.3f}, {100*high:+.3f}].')
    lines += ['',
        'Both intervals include zero. The word-type bootstrap ignores root dependence, label uncertainty and selection. It does not establish reliable superiority.', '',
        f'DEV has {report["dev_rows"]} words and historical TEST {report["test_rows"]}; {report["dev_words_in_training"]}/272 DEV and {report["test_words_in_training"]}/262 TEST word forms occur in tokenizer training. Labels are mixed silver and user-derived. TEST has been used previously.', '',
        'Tagalog morphology has no independent reviewed gold in this experiment. Its 1,000 article-disjoint evaluation records measure coverage and length. The 12 targeted fixtures are debugging checks, partly from upstream tests; they are not a blind language benchmark.', '',
        'All six Morph conditions score zero unknown tokens on those Tagalog records. All retain 39 Kapampangan validation records containing unknown characters. Plain and Unigram have unchanged evaluation scores; neither uses morphology annotations.', '',
        '## Verification and installed state', '',
        'Four annotation regression tests passed. Independent verification reencoded 12,816 DEV/TEST cases across 24 before/after configurations, recomputed boundary and pairwise consistency arithmetic, validated inventories and dataset identities, checked nested BPE snapshots and identical Plain vocabularies/merges, and confirmed all 615 protected files unchanged.', '',
        'The webapp continues to use its previous installed artifacts. Translator files, neural checkpoints and source embeddings are unchanged. No BLEU/chrF++, neural training, human linguistic validation or webapp replacement was performed.']
    (root / 'reports/findings.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(root / 'reports/findings.md')


if __name__ == '__main__':
    main()
