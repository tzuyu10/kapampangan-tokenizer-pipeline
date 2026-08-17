# Kapampangan MorphBPE

Independent implementation and completed train/validation run of the
three-stage tokenizer in `G4-THESIS-PROPOSAL-REVISED.pdf`:

1. deterministic NFC pre-tokenization;
2. training-only lexicon-guided Kapampangan morphological segmentation; and
3. character-initialized BPE that cannot merge across protected training
   morpheme boundaries.

The selected tokenizer has **6,080 vocabulary entries**, **4,488 merges**, and
artifact fingerprint
`d3974f566756314f961a678a6bbf665a4ed3ecd2e64a82826c01950aa3e0e14e`.
Its standalone runtime uses only normalization, pre-tokenization, vocabulary,
merge rules, and special tokens. It never loads the training lexicon or corpus.

## Evidence status

Training and validation-only selection are complete. Morphology references are
not human-validated, so validation FR/MBF1/MCF1/distance values are provisional
development proxies, not formal thesis results. Held-out evaluation, the native
NLLB tokenizer comparison, NLLB-200 download/fine-tuning, BLEU, chrF++, and
statistical tests were deliberately not performed.

## Environment

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-lock.txt
uv pip install --python .venv\Scripts\python.exe -e .
```

This builds the PyO3 Rust segmenter with pinned maturin. The project supports
Windows/Python/Rust and is CPU-only. See `requirements-lock.txt` and
`docs/REPRODUCIBILITY.md`.

## CLI

```text
verify-dataset          build-lexicon
segment                 verify-segmentation-parity
prepare-training        freeze-candidates
train-candidates        evaluate-validation
select-candidate        finalize-tokenizer
tokenize                decode
inspect-artifact        validate-artifact
verify-runtime-independence
export-nllb-contract
```

Every command accepts explicit paths. A complete copy/paste Windows sequence is
in `docs/REPRODUCIBILITY.md`; the Colab workflow is
`notebooks/tokenizer-training-colab.ipynb`.

Example runtime use:

```powershell
.\.venv\Scripts\kapampangan-morphbpe.exe tokenize `
  --artifact .\artifacts\selected-tokenizer `
  --text "Masánting! ñ"
```

## Key outputs

- Selected artifact: `artifacts/selected-tokenizer/`
- Candidate artifacts: `artifacts/candidates/`
- Training lexicon: `resources/training-lexicon.json`
- Candidate/selection configs: `configs/`
- Machine-readable validation reports: `reports/validation/`
- Standalone runtime: `runtime/kapampangan_morphbpe_runtime/`
- Future NLLB contract: `nllb/`

Start with `docs/PAPER_TRACEABILITY.md`, `docs/ARCHITECTURE.md`,
`reports/TRAINING_REPORT.md`, and `reports/VALIDATION_SELECTION_REPORT.md`.
