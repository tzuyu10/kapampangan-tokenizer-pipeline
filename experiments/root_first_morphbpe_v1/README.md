# Morphology-priority Morph-BPE experiments

This experiment implements the owner's requested training order:

1. Prefer merges inside confirmed continuous root or root-fragment spans.
2. Prefer merges inside confirmed affix spans.
3. Fill remaining vocabulary capacity with the original weighted selection.

The candidate uses the original expanded-v4 prepared stream, penalty 32 and
6,080 vocabulary entries. It exports to a separate research directory. It does
not install a tokenizer or train a translation model.

The trainer also supports the reversed order, affixes then roots then weighted
completion, for a matched comparison. The original root-first order remains
the default. Two further orders separate infixes from other affixes:
`infix-only` (infix then weighted) and `infix-root-affix` (infix then root,
then other affix, then weighted).

## Trainer

`src/kapampangan_morphbpe/root_priority_bpe.py` subclasses the existing weighted
trainer. It keeps the original protected-boundary merge application and standard
global BPE runtime. Root and affix labels are used only during training.

Within the active priority phase, pairs are ranked by:

1. Current frequency of eligible occurrences inside that role's surface spans.
2. Original weighted score: allowed frequency minus 32 times crossing frequency.
3. Allowed frequency.
4. UTF-8 ordering of the left and right pieces.

The default root budget is 2,244 newly added vocabulary tokens, half of the
4,488 available slots. The default affix budget is 256 new tokens. These caps
were chosen before evaluating DEV. A phase ends early when no supported pair
remains. Remaining capacity returns to normal weighted selection. Intermediate
tokens count toward the vocabulary budget; merge-rule count can differ from the
number of new tokens.

Role support describes occurrences rather than pair strings. Selecting a pair
still merges every allowed occurrence, including occurrences outside its
priority role. Protected occurrences remain separate during training. Global
inference can still cross morphology boundaries or absorb an affix into a larger
token. Priority changes do not guarantee correct segmentation.

## Training annotations

The runner reuses the expanded-v4 analyzer and original training lexicon. It
requires accepted/protected-root analyses, unchanged normalized surfaces and
exact agreement with the frozen stream boundaries. Span offsets come from
`analysis.segments`, not underlying spellings or potentially stale unit surfaces.

- Root roles: `root`, `root_fragment`, and `root_or_compound` only when the
  surface segment is a valid lexicon host and is absent from compounds.
- Affix roles: prefix, suffix, infix, circumfix prefix and circumfix suffix.
- In the two infix orders, infixes have their own role and are excluded from
  the other-affix role. The current analyzer supports `in` and `um`, with
  accepted casing preserved from actual surface segments.
- Compounds, reduplicants, clitics, ambiguous/unchanged analyses and unconfirmed
  hosts have no priority role. Their normal allowed merges remain available.

For the intended analysis `k | um | ain`, root priority can form `ain`, followed
by affix priority forming `um`. Adjacent BPE cannot combine `k` and `ain` while
skipping `um`; reconstructed `kain` remains analysis metadata.

## Run on the recovered original inputs

From the repository directory in PowerShell:

```powershell
$experimentBase = "C:\Users\Gabo\.codex\visualizations\2026\10\10\01a123b1-9446-7a33-b574-09074e63c7e7"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/run_experiment.py `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --output-dir "$experimentBase\root_first_comparison" `
  --um-first "$experimentBase\infix_prioritization\um-first-penalty32"
```

`--mode annotate` writes only the role audit. `--root-budget` and
`--affix-budget` change the declared caps. `--um-first` optionally includes the
previous seeded-um candidate as an additional comparator. The runner checks the
original stream, lexicon, DEV and validation hashes, plus the installed baseline
manifest and inventory. It freshly evaluates each comparator.

`--priority-order affix-first` reverses the two role phases. It exports
`affix-first-penalty32/` and labels the candidate `affix_first32` in results;
`--priority-order root-first` preserves the default naming. Actual phase
consumption can differ under the same caps because earlier global merges change
which supported pairs remain.

The input directory contains `training-inputs/training-stream.jsonl`,
`training-inputs/training-lexicon.json`, the supplied
`provenance/penalty32-tokenizer-manifest.json`, and recovered `validation.csv`.
These data stay outside the repository.

## Outputs and evaluation

The output directory contains the role audit/summary, exported
`root-first-penalty32/`, `comparison-result.json`, and `comparison-report.md`.

Compare full frozen DEV boundary F1, exact segmentation, tokens per word and
the original span-specific infix isolation counts (five `um`, 41 `in` examples).
The runner also reports process groups, analyzer/reference-aligned role
diagnostics with single-character and longer-span denominators, provisional
root controls containing `um`, training fertility, and original validation
fertility/coverage. All encodings without unknown characters must round-trip.

DEV is mixed silver/user-derived and 270/272 words were seen in training.
Role diagnostics use a smaller analyzer/reference-aligned subset and are not
independent human gold. The 3,284 validation records have no morphology gold;
fertility is a length/coverage diagnostic. No final test text is read.

Changed tokenizer IDs require compatible new source-embedding adaptation
before translation deployment. Tokenizer-only results do not establish
translation-quality improvements.

## Completed original-input comparison (2026-10-10)

Two complete candidates were trained and evaluated. Both use the same frozen
stream, penalty 32, vocabulary 6,080 and unchanged runtime. The smaller root
budget was a diagnostic follow-up after the default performed poorly; neither
run is an unbiased final selection or held-out test result.

| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 |
| --- | ---: | ---: | ---: | ---: |
| Installed32 | 54.22% | 81 | 0 | 33 |
| Root-first, root cap 2,244 | 32.60% | 56 | 0 | 7 |
| Root-first, root cap 512 | 33.87% | 57 | 0 | 9 |
| Previous um-first candidate | 56.45% | 83 | 3 | 32 |

The root phases added 2,244 and 512 tokens, respectively. The affix phases
exhausted supported pairs after 75 and 103 new tokens, below their shared cap
of 256. Normal weighted selection added the remaining 2,169 and 3,873 tokens.

Both candidates learn `ku` at rank 19 and `bu` at rank 37 before `um` at rank
221. At inference these earlier global rules still produce `ku | main` and
`bu | ma | sa`. The default candidate additionally learns `s + in -> sin`
at rank 550, producing `sin | ulat`. Training boundary safety does not imply
runtime boundary safety.

The default candidate keeps 23/74 provisional standalone root controls whole,
compared with 10/74 for installed32, but its root isolation inside the aligned
DEV subset falls from 73/97 to 49/97. The smaller candidate scores 47/97.
These role diagnostics cover only 72 analyzer/reference-aligned words and
are not independent human gold. Lower fertility and more whole root controls
do not offset the observed morphology regression. Retain installed32.

Detailed results and candidate artifacts are in the external
`$experimentBase\root_first_comparison` directory. To reproduce the smaller
candidate, use the same runner with `--root-budget 512` and a separate output
directory such as `$experimentBase\root_first_comparison\root-budget-512`.
The `summarize_comparison.py` helper combines these two declared outputs:

```powershell
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/summarize_comparison.py `
  --output-dir "$experimentBase\root_first_comparison"
```

Twenty focused tests passed. An independent audit reproduced 1,360 DEV
encodings across the saved comparator evaluations, all role/infix counts,
round-trips, inventories and source hashes. A randomized scheduler audit
also passed 100 fixtures and 1,943 independently ranked merges. The runner
scored all 3,284 validation records per comparator, retaining 118 unknown
tokens across 39 records; that full validation corpus was not independently
reencoded during the audit. Installed artifacts remain unchanged.

## Fresh comparison of phase orders

The earlier `um`-first result does not establish that all-affix-first is better.
To test phase order, train both orders with the same root cap 2,244 and affix
cap 256, and compare their complete exported runtimes. Only the order changes.
Keep separate output directories to preserve earlier results:

```powershell
$retestOutput = "$experimentBase\priority_order_retest"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/run_experiment.py `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --output-dir "$retestOutput\root-first" `
  --priority-order root-first --root-budget 2244 --affix-budget 256 `
  --um-first "$experimentBase\infix_prioritization\um-first-penalty32"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/run_experiment.py `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --output-dir "$retestOutput\affix-first" `
  --priority-order affix-first --root-budget 2244 --affix-budget 256
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/compare_priority_orders.py `
  --root-dir "$retestOutput\root-first" `
  --affix-dir "$retestOutput\affix-first" `
  --output-dir "$retestOutput" `
  --old-root-artifact "$experimentBase\root_first_comparison\root-first-penalty32"
```

The comparison helper verifies equal input/role/source hashes and caps, fresh
baseline evaluation equality, and optional ordered vocabulary/merge equality
with the original root-first run. It reports full DEV and role/infix metrics,
validation coverage/fertility, actual phase usage and an exploratory paired
DEV bootstrap. It does not install or select a tokenizer.

The 2026-10-10 fresh runs produced:

| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 |
| --- | ---: | ---: | ---: | ---: |
| Current32 | 54.22% | 81 | 0 | 33 |
| Root then affix | 32.60% | 56 | 0 | 7 |
| Affix then root | 36.68% | 54 | 0 | 5 |
| Previous targeted um seed | 56.45% | 83 | 3 | 32 |

Affix-first raises observed boundary F1 by 4.08 percentage points over this
root-first schedule, but loses exact segmentations and `in` isolation. Both
remain worse than installed32. The exploratory paired bootstrap interval for
affix-minus-root F1 is [-0.012146, 0.094701], including zero; this does not
establish a reliable general advantage across morphology, root families or
annotation uncertainty. Keep installed32.

Affix-first learns `ma` at rank2 before `um` at rank15, and later learns `sin`
at642 and `sum` at923. Those global rules can cross an infix/root boundary or
absorb a formed infix. Actual affix-first phase usage is130 affix tokens,
2,244 root tokens and2,114 weighted tokens. Broad affix priority is different
from the tested rank0 `um` seed.

Thirty-four focused tests pass. The root-first rerun exactly reproduces the
previous ordered vocabulary and merge rules. Independent audit confirms1,360
fresh DEV comparator encodings, counts, infix/role diagnostics, round-trips,
inventories and matching source/input/role hashes. Full validation records
were scored by the runner; independent audit did not repeat that full corpus.

## Separate infix priority orders

Both new schedules use a separate occurrence role for confirmed `in` and `um`
spans. Other affixes exclude those spans during training. The infix phase ranks
only pairs inside accepted infix spans, applies selected pairs to all allowed
training occurrences, and then ends when no supported pair remains. A cap of
32 new tokens permits all four attested forms (`in`, `um`, `IN`, `UM`) to form.
The runner rejects a completed run if supported internal infix pairs remain.

`infix-only` continues directly with weighted selection. Its inactive root and
affix budgets are zeroed. `infix-root-affix` continues with the previously
declared root cap 2,244 and other-affix cap 256, then weighted completion. Both
use penalty 32 and exactly 6,080 vocabulary entries. These are separately
exported candidates; the installed tokenizer and translation models are
preserved.

```powershell
$infixOutput = "$experimentBase\infix_order_comparison"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/run_experiment.py `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --output-dir "$infixOutput\infix-only" `
  --priority-order infix-only --infix-budget 32 `
  --um-first "$experimentBase\infix_prioritization\um-first-penalty32"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/run_experiment.py `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --output-dir "$infixOutput\infix-root-affix" `
  --priority-order infix-root-affix --infix-budget 32 `
  --root-budget 2244 --affix-budget 256 `
  --um-first "$experimentBase\infix_prioritization\um-first-penalty32"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/compare_infix_orders.py `
  --infix-dir "$infixOutput\infix-only" `
  --full-dir "$infixOutput\infix-root-affix" `
  --output-dir "$infixOutput"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/audit_infix_comparison.py `
  --comparison-dir "$infixOutput" `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --prior-um "$experimentBase\infix_prioritization\um-first-penalty32"
```

The combined report includes current Morph-BPE and the previous `um` seed,
freshly evaluated on the same references/corpus. The helper verifies identical
new candidate inputs, annotations and source hashes, baseline comparator
equality, phase usage and paired exploratory DEV bootstrap differences. The
independent audit reencodes DEV and controls without calling runner evaluation.
Evaluation retains the original aggregate affix denominator for comparison,
while the audit additionally separates infix and other-affix diagnostics.

The completed 2026-10-10 runs produced:

| Tokenizer | Boundary F1 | Exact /272 | um isolated /5 | in isolated /41 |
| --- | ---: | ---: | ---: | ---: |
| Current Morph-BPE | 54.22% | 81 | 0 | 33 |
| Previous um seed | 56.45% | 83 | 3 | 32 |
| Infix then weighted | 56.45% | 83 | 3 | 32 |
| Infix then root then other affix | 33.12% | 49 | 0 | 9 |

Both new orders first learn `in`, `um`, `IN`, `UM` at ranks 0-3 and exhaust
supported infix pairs. The infix-only candidate then adds 4,484 weighted tokens.
The full order adds 2,244 root, 72 other-affix and 2,168 weighted tokens.

Infix-only and the previous um seed have identical predictions on all 272 DEV
words, but different vocabularies and merge rules. Validation tokens per word
are 1.624227 versus 1.624191, a difference of seven word tokens among 198,790
word occurrences. This is a DEV tie, not tokenizer identity.

The full order later learns `s + in -> sin` at rank 549, `um + an -> uman`
at 792 and `s + um -> sum` at 1597, all during its root phase. These global
rules absorb infixes at runtime. Infix-only produces `k | um | ain` for
`kumain`; the full order produces `k | uma | in`. Root isolation inside the
aligned DEV subset falls from 79/97 to 54/97, while whole standalone root
controls increase from 11/74 to 23/74. Adding the two phases gains 12 exact DEV
words but loses 46 relative to infix-only.

Infix-only is the more promising new candidate on this exploratory set.
Its F1 gain over installed32 is 2.23 percentage points; the paired exploratory
bootstrap interval [-0.001527,0.049296] includes zero. Do not claim a reliable
general improvement from this small, mostly training-seen DEV set. Retain the
installed tokenizer pending larger human-validated, root-disjoint evaluation.

Forty-two focused tests pass. The independent audit reproduces 1,088 fresh DEV
encodings across four artifacts and 296 root-control encodings, checks six
stored comparator evaluations, annotations, inventories, source/input/role
hashes and phase accounting. Full validation records were scored by the
runner; the audit does not independently recompute validation, training
fertility or MCF1. Installed artifacts and translation weights are preserved.

## Infix-first penalty sweep

The runner accepts `--crossing-penalty`, defaulting to 32. Export names, result
keys, configuration and artifact metadata use the actual selected penalty.
`--matched-weighted` optionally includes an existing ordinary weighted export
from the same original stream, vocabulary size and penalty. It is freshly
evaluated alongside installed32 and the new infix candidate. Existing ordinary
weighted comparators are not retrained by this sweep.

This sweep trains infix -> weighted at penalties 8,16,32,48 with the same
infix cap 32, inactive root/affix budgets 0, vocabulary 6,080 and protected
training boundaries. It preserves earlier outputs in a separate directory:

```powershell
$penaltyOutput = "$experimentBase\infix_penalty_comparison"
foreach ($penaltyValue in 8,16,32,48) {
  & .\.venv-translation\Scripts\python.exe `
    experiments/root_first_morphbpe_v1/run_experiment.py `
    --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
    --output-dir "$penaltyOutput\penalty-$penaltyValue" `
    --priority-order infix-only --infix-budget 32 `
    --crossing-penalty $penaltyValue `
    --matched-weighted "$experimentBase\exact_penalty_comparison\penalty-$penaltyValue"
}
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/compare_infix_penalties.py `
  --comparison-dir "$penaltyOutput" --output-dir "$penaltyOutput" `
  --prior-infix32 "$experimentBase\infix_order_comparison\infix-only\infix-only-penalty32"
& .\.venv-translation\Scripts\python.exe `
  experiments/root_first_morphbpe_v1/audit_infix_penalties.py `
  --comparison-dir "$penaltyOutput" `
  --input-dir "$experimentBase\exact_penalty_comparison\inputs" `
  --prior-infix32 "$experimentBase\infix_order_comparison\infix-only\infix-only-penalty32" `
  --weighted-dir "$experimentBase\exact_penalty_comparison"
```

The primary comparison uses the installed penalty32 Morph-BPE. The secondary
comparison pairs infix-first and ordinary weighted training at each penalty
to distinguish changes from infix priority and changes from penalty alone.
All candidates form the supported infixes before weighted completion. Higher
penalties still change only pair ranking; protected positions remain blocked
during training at every penalty, and ordinary global inference has no such
boundary constraint.

The completed 2026-10-10 sweep produced:

| Tokenizer | Boundary F1 | Exact /272 | um isolated /5 | in isolated /41 |
| --- | ---: | ---: | ---: | ---: |
| Current penalty32 Morph-BPE | 54.22% | 81 | 0 | 33 |
| Infix-first penalty8 | 49.38% | 74 | 4 | 26 |
| Infix-first penalty16 | 52.86% | 82 | 3 | 29 |
| Infix-first penalty32 | 56.45% | 83 | 3 | 32 |
| Infix-first penalty48 | 59.26% | 87 | 4 | 33 |

At matching penalties, ordinary weighted versus infix-first F1 is
46.39%/49.38% at 8, 50.84%/52.86% at 16, 54.22%/56.45% at 32 and 54.04%/59.26%
at 48. Priority improves the observed score at all four matching penalties.
Only infix32/48 exceed the installed32 boundary F1. This algorithm's observed
best penalty is 48; the earlier ordinary weighted sweep still favors 32.

Infix48 gains 5.04 percentage points of F1 and six exact words over current32.
It preserves `kumain` as `k | um | ain`, `sumulat` as `s | um | ulat` and
`bumasa` as `b | um | asa`. The remaining um isolation error is `mumunang`,
predicted whole versus reference `m | um | unang`. Isolating an infix does not
guarantee exact root segmentation: `tumula` becomes `t | um | u | la`, and
`tumakut` becomes `t | um | a | kut`.

Infix48 isolates 80/97 root and 76/80 aggregate affix spans on the smaller
analyzer/reference-aligned subset, versus current 73/97 and 71/80. Provisional
standalone um-containing root controls cost 210 tokens versus current 190,
with both keeping 10/74 words whole. This candidate improves overall DEV
morphology while still fragmenting some standalone roots more.

Exploratory paired bootstrap intervals (5,000 resamples, seed 20261010) are
[0.015636,0.087871] for infix48 minus current32 and [0.002503,0.055628] for
infix48 minus infix32. These type intervals ignore root-family dependence,
annotation uncertainty and repeated DEV-driven choices. With 270/272 words
seen in training and only five genuine um references, they do not establish
unseen-root or translation superiority. Infix48 is the most promising tested
candidate for further evaluation; keep installed32 pending that work.

All four candidates were freshly trained. Existing ordinary weighted controls
and installed32 were freshly scored, not retrained. Forty-two focused tests
pass. An independent audit reproduces 2,448 DEV and 666 root-control encodings
across nine artifacts and compares 12 stored evaluations, including provenance,
penalty values, inventories, annotations and phase counts. Fresh infix32
exactly reproduces prior ordered and serialized vocab/merges. Each runner
scores all 3,284 validation records per comparator; independent audit does not
recompute full validation/training fertility or MCF1. Installed artifacts and
translation weights remain unchanged. Combined report, summary and audit are
under `$penaltyOutput`.

## Verification

```powershell
$env:PYTHONPATH = "src"
& .\.cache\python313-check\venv\Scripts\python.exe -m pytest `
  tests/test_root_priority_bpe.py `
  tests/test_root_priority_experiment.py `
  tests/test_weighted_bpe.py -q -p no:cacheprovider
```

The focused suite covers phase order and budgets, changing occurrence counts,
shared pair roles, protected boundaries, baseline parity with priorities
disabled, split roots, invalid annotations, and surface offsets despite root
restoration. Artifact checks, actual full training spans and fresh comparator
runtime checks are performed by the experiment runner.
