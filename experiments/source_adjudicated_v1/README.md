# Source-adjudicated MorphBPE experiment v1

This is an isolated, local-test rebuild. It does not modify the canonical
`resources/`, `runs/`, `configs/`, `reports/`, or `artifacts/` directories.

## Adjudication boundary

- Add provisional roots `bukas`, `pangulo`, and `presidente`.
- Add only the exact historical `bucas` variant of `bukas`; there is no global
  `c`-to-`k` normalization.
- Keep existing `datang`, `pamuntuk`, and `pangulu` roots. `pangulo` and
  `pangulu` remain distinct, and `pangulo` is never split as `pang + ulo`.
- Hold all Richards-derived rows (`ocr-010` through `ocr-012`). They cannot
  alter clitic classification, morphophonemics, or the affix inventory here.

The complete machine-readable decision record is `adjudication-policy.json`.

## Reconstruction boundary

The original portable train and validation CSV files are no longer available
locally. The base `runs/prepared/training-stream.jsonl` is hash-verified against
the canonical manifest and retains every pretoken surface, kind, frequency, and
old protected boundary consumed by BPE. The experiment re-runs both Python and
Rust morphology over all 143,529 preserved word types and rebuilds the aggregate
stream. This is a faithful reconstruction of the training-stage BPE input, not
a reconstruction of sentence order.

Validation is not fabricated. All three already frozen candidates are
retrained, while vocabulary size 6,080 remains precommitted from the canonical
selection. The experiment's selection record explicitly says that current
validation was not re-evaluated.

## Run

From the repository root with the project virtual environment active:

```powershell
.\.venv\Scripts\python.exe .\experiments\source_adjudicated_v1\run_experiment.py all
```

Stages can be resumed independently with `prepare`, `train`, `finalize`, and
`plain-bpe`.
Generated outputs stay inside this folder and are git-ignored:

- `resources/`: experimental lexicon and manifest
- `runs/prepared/`: resegmented training stream and manifest
- `configs/`: frozen candidate grid and inherited selection record
- `artifacts/`: candidate, selected, and deterministic rebuild artifacts
- `reports/`: parity, sentence analysis, training, and final validation reports

The `plain-bpe` stage trains a matched 6,080-token control using the same
preserved surfaces, frequencies, pre-tokenizer, special tokens, character
inventory, trainer, and tie-breaking. It only clears morphology-protected
boundaries. The build also proves that the original and source-adjudicated
streams have identical surface/kind/frequency records after boundary removal,
so the same plain-BPE control is valid for both comparisons.

Use the paper-aligned standard-runtime comparison as the primary result:

```powershell
prop 6k experimental "Bukas na datang ing pangulo."
```

This runs both artifacts through ordinary BPE inference without loading a
lexicon. Morphology constrained merge learning, not runtime segmentation.

Inspect the optional runtime-constrained extension with:

```powershell
.\.venv\Scripts\kapampangan-morphbpe.exe compare-tokenizers `
  --plain-artifact .\experiments\source_adjudicated_v1\artifacts\plain-bpe-tokenizer `
  --morph-artifact .\experiments\source_adjudicated_v1\artifacts\selected-tokenizer `
  --morph-lexicon .\experiments\source_adjudicated_v1\resources\training-lexicon.json `
  --text "Bukas na datang ing pangulo."
```

The diagnostic reports pieces, IDs, offsets, token counts, their difference,
and whether the piece sequences differ. It requires the MorphBPE lexicon to
apply morphology first and run BPE independently inside each accepted segment.
This provides a hard runtime guarantee but is an implementation extension, not
the paper-aligned standard tokenizer runtime.

To compare against the original canonical implementation instead:

```powershell
.\.venv\Scripts\kapampangan-morphbpe.exe compare-tokenizers `
  --plain-artifact .\experiments\source_adjudicated_v1\artifacts\plain-bpe-tokenizer `
  --morph-artifact .\artifacts\selected-tokenizer `
  --morph-lexicon .\resources\training-lexicon.json `
  --text "kasulatan"
```

## Morphology versus tokenizer pieces

With the experimental lexicon, `segment` reports `Bukas`, `na`, `datang`,
`ing`, and `pangulo` as atomic protected roots. It correctly does **not** claim
`pang + ulo` as a morphological analysis.

The final tokenizer may still emit smaller BPE pieces inside an atomic root,
for example `Bu` + `kas` or `pang` + `ulo`. Protected boundaries constrain
merge learning, but the paper-aligned standard runtime carries no boundary
metadata and therefore offers statistical alignment rather than a per-word hard
guarantee. The optional runtime-constrained diagnostic does enforce a hard
boundary. In both modes, BPE pieces are statistical subwords rather than
additional adjudicated morphemes.
