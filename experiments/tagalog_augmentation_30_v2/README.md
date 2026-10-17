# Shared-root and affix annotation revision

This experiment changes only Tagalog training preparation. The 26,268 original
Kapampangan records, 7,880 Tagalog records, 3,311 original roots and 993 unique
Tagalog additions remain byte-identical to v1. The original Kapampangan prepared
stream, affix inventories, infix priority, trainer and runtime remain unchanged.

Tagalog analysis reuses 779 existing Kapampangan root strings whose Tagalog source
dictionary entries pass the same word, URL-headword and definition checks. These
are shared recognition entries, not additional unique roots. Recognition now has
1,772 Tagalog dictionary entries, while the combined unique-root count stays 4,304.
Known prefix-hyphen-stem forms are analyzed without removing any characters;
unknown stems remain intact. Imported dictionary analyses remain provisional.

## Reproduce from the repository

Use a new output directory. The original v1 input package and comparison directory
are required. Run these commands from the repository root with actual paths:

```powershell
python experiments/tagalog_augmentation_30_v2/build_revision.py --original ORIGINAL_INPUTS --dictionary TAGALOG_DICTIONARY_JSON --output NEW_RESULTS/inputs
```

The input builder refuses an existing destination and checks all original input
hashes before changing annotations. For each family `weighted32`, `infix_first48`,
`plain` and `unigram`, run the unchanged grid trainer:

```powershell
.venv-translation/Scripts/python.exe experiments/tagalog_augmentation_30_v1/train_vocab_grid.py --inputs NEW_RESULTS/inputs --output NEW_RESULTS/vocab_grid/FAMILY --condition FAMILY
```

Each BPE family follows one deterministic training trajectory with snapshots at
6,080, 8,192 and 16,384. Unigram trains independently at each size, with the same
frequency-expanded plain stream and tokenizers 0.21.0. Plain and Unigram do not
use morphology annotations. The completed local rerun has unchanged control
evaluation scores; Plain vocabularies/merges are identical to v1.

Copy the original comparison's `evaluation_inputs` directory into `NEW_RESULTS`.
The local run also saved a pre-edit `reports/protected_before.json` hash snapshot
of installed application/model files and previous experiment files. Then run:

```powershell
.venv-translation/Scripts/python.exe experiments/tagalog_augmentation_30_v2/evaluate_revision.py --results NEW_RESULTS --before ORIGINAL_COMPARISON
.venv-translation/Scripts/python.exe experiments/tagalog_augmentation_30_v2/verify_revision.py --results NEW_RESULTS --before ORIGINAL_COMPARISON
$env:TAGALOG_V2_INPUTS = 'NEW_RESULTS/inputs'
python -m unittest discover -s experiments/tagalog_augmentation_30_v2 -p 'test_*.py' -v
```

Evaluation reproduces all old scores before comparing the new exports. It ranks
on the existing 272-word DEV, writes selection, then reads the historical 262-word
TEST. It also evaluates the unchanged 3,284-record Kapampangan validation corpus
and 1,000 Tagalog records from article titles absent from the selected training
subset. These corpora measure coverage and length, not Tagalog morphology accuracy.

## Completed result

Weighted32 DEV boundary F1 improves by 0.715, 0.957 and 0.671 percentage points at
6,080, 8,192 and 16,384. Infix-first48 changes by -0.375, -0.496 and +0.460 points.
All six Morph conditions improve slightly on the historical TEST. The revised
6,080 infix-first48 remains highest among the new runs, but its DEV score
58.960% is below the previous 59.334%. Do not replace the previous recommendation
with a claim that the revised preparation is better overall.

The two checked 6,080 DEV bootstrap intervals include zero. Labels are mixed
silver/user-derived, most reference words occur in training and TEST has been
evaluated previously. The changes are exploratory, not statistically established
superiority or independent final-test evidence.

The targeted `nag-aral` split improves to `nag | - | aral`; `nagaral` still becomes
`na | garal`. Access to the root fixes preparation, but global BPE merge ordering
can still produce a different split at inference. Targeted fixtures are debugging
checks, partly from the upstream Filipino repository tests, not a blind benchmark.

No webapp tokenizer was replaced. No translator, neural training, source embedding
or translation-quality evaluation is included.
