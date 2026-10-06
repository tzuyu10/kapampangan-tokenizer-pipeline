# MorphBPE vocabulary-size ablation

This isolated experiment trains 8,192- and 16,384-token MorphBPE candidate
artifacts for two conditions:

- `original`: the canonical training stream and lexicon;
- `source-adjudicated`: the locally adjudicated experimental stream and
  lexicon from `experiments/source_adjudicated_v1/`.

The two vocabulary sizes are comparison candidates only. They are not selected
final tokenizers because the raw validation split needed for honest reselection
is unavailable. Existing 6,080-token artifacts are hash-snapshotted before and
after training and are never used as output directories.

Run both conditions from the repository root:

```powershell
& .\.venv\Scripts\python.exe `
  .\experiments\vocab_ablation_v1\run_ablation.py
```

Run one condition when resuming:

```powershell
& .\.venv\Scripts\python.exe `
  .\experiments\vocab_ablation_v1\run_ablation.py `
  --condition original
```

Generated outputs are ignored and remain below this directory:

- `configs/<condition>/candidate-grid.json`
- `artifacts/<condition>/candidates/vocab-8192/`
- `artifacts/<condition>/candidates/vocab-16384/`
- `reports/training-summary.json`

## Completed builds

| Condition | Vocabulary | Merges | Artifact fingerprint |
|---|---:|---:|---|
| Original | 8,192 | 6,600 | `06662a9067835cddcb4c7a9a13eebd9702def7a4a39b02bb48dc080efff89aff` |
| Original | 16,384 | 14,792 | `529d1b81c6c4806e1ad8b2744e228e7a91b0e34becd0fee75d4ef9e980ec3606` |
| Source-adjudicated | 8,192 | 6,600 | `5eec98b74730717e76b0603552269b83545af8741c9b1aed1604389da317d1ef` |
| Source-adjudicated | 16,384 | 14,792 | `ed616c40a883fd395c2793804c2a81de054764e91813380dac8070efe9293ee7` |

Every build reached its exact target, reported zero training-time protected
boundary violations, passed artifact checksum validation, and round-tripped the
diagnostic sentence through the standalone runtime.

The shared matched Plain-BPE controls are:

| Vocabulary | Merges | Artifact fingerprint |
|---:|---:|---|
| 8,192 | 6,600 | `115de1e49ae6530370c57a53bd89e6c054d6353eb8adc400ea028c7f499a5e0e` |
| 16,384 | 14,792 | `b690d8ae4faffb9f11c5c0ef0e5e7a8946dfa109e57d3d2a9bfdc2b0ae81d914` |

Both controls use the exact shared original/source-adjudicated
surface/kind/frequency stream after clearing every morphology boundary. They
have artifact type `kapampangan_plain_bpe`, reached their exact targets, passed
checksum/runtime validation, and left all existing MorphBPE artifacts unchanged.

## Paper-aligned standard-runtime comparisons

Use `prop` for the primary thesis comparison. It runs both artifacts through
ordinary BPE inference and does not load the morphology lexicon:

```powershell
prop 6k original "text or sentence"
prop 8k original "text or sentence"
prop 16k original "text or sentence"

prop 6k experimental "text or sentence"
prop 8k experimental "text or sentence"
prop 16k experimental "text or sentence"
```

The text defaults to `kabukasan` when omitted.

## Optional runtime-constrained diagnostics

The installed shorthand accepts a dedicated quoted text or sentence argument:

```powershell
comp 6k original "text or sentence"
comp 8k original "text or sentence"
comp 16k original "text or sentence"

comp 6k experimental "text or sentence"
comp 8k experimental "text or sentence"
comp 16k experimental "text or sentence"
```

When the text argument is omitted, it defaults to `kabukasan`, so this is also
valid:

```powershell
comp 8k original
comp 8k experimental
```

Activate this repository's virtual environment first so its `comp.exe` is
resolved ahead of Windows' unrelated system `comp.exe`.

The equivalent fully explicit commands are retained below for reproducibility.

```powershell
$Root = 'D:\Coding\thesis\kapampangan-morphbpe-paper-v1'
$K = "$Root\.venv\Scripts\kapampangan-morphbpe.exe"
$Text = 'kabukasan'

# Original 8,192
& $K compare-tokenizers `
  --plain-artifact "$Root\experiments\vocab_ablation_v1\artifacts\plain\candidates\vocab-8192" `
  --morph-artifact "$Root\experiments\vocab_ablation_v1\artifacts\original\candidates\vocab-8192" `
  --morph-lexicon "$Root\resources\training-lexicon.json" `
  --text $Text

# Original 16,384
& $K compare-tokenizers `
  --plain-artifact "$Root\experiments\vocab_ablation_v1\artifacts\plain\candidates\vocab-16384" `
  --morph-artifact "$Root\experiments\vocab_ablation_v1\artifacts\original\candidates\vocab-16384" `
  --morph-lexicon "$Root\resources\training-lexicon.json" `
  --text $Text

# Source-adjudicated 8,192
& $K compare-tokenizers `
  --plain-artifact "$Root\experiments\vocab_ablation_v1\artifacts\plain\candidates\vocab-8192" `
  --morph-artifact "$Root\experiments\vocab_ablation_v1\artifacts\source-adjudicated\candidates\vocab-8192" `
  --morph-lexicon "$Root\experiments\source_adjudicated_v1\resources\training-lexicon.json" `
  --text $Text

# Source-adjudicated 16,384
& $K compare-tokenizers `
  --plain-artifact "$Root\experiments\vocab_ablation_v1\artifacts\plain\candidates\vocab-16384" `
  --morph-artifact "$Root\experiments\vocab_ablation_v1\artifacts\source-adjudicated\candidates\vocab-16384" `
  --morph-lexicon "$Root\experiments\source_adjudicated_v1\resources\training-lexicon.json" `
  --text $Text
```

For `kabukasan`, the source-adjudicated MorphBPE outputs `ka + bukas + an` at
both sizes. Plain BPE outputs `kabu + kasan` at 8,192 and the whole word
`kabukasan` at 16,384. The original lexicon leaves this word morphologically
unchanged, so its visible pieces match Plain BPE for this example.
