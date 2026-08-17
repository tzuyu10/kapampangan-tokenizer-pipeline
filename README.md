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

## Setup from scratch (Windows)

Prerequisites:

- Python 3.11 or newer
- `uv`
- Rust and Cargo (required to build the PyO3 segmenter)
- The external corpus only if you will reproduce training or validation

Clone the repository and select the project branch after it has been pushed:

```powershell
git clone https://github.com/tzuyu10/kapampangan-tokenizer-pipeline.git
cd kapampangan-tokenizer-pipeline
git switch feat/kapampangan-morphbpe
```

Create the environment and install the locked dependencies:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-lock.txt
uv pip install --python .venv\Scripts\python.exe -e .
```

The editable install builds the PyO3 Rust segmenter with pinned maturin. The
project is CPU-only. Define the CLI path for the commands below:

```powershell
$K = '.\.venv\Scripts\kapampangan-morphbpe.exe'
```

Validate the committed standalone artifact without the external corpus:

```powershell
& $K validate-artifact --artifact .\artifacts\selected-tokenizer
```

Run a first tokenization test:

```powershell
& $K tokenize --artifact .\artifacts\selected-tokenizer --text "Masánting! ñ"
```

The output includes normalized text, token strings, token IDs, token kinds,
and offsets. `tokenize` accepts raw text; do not run `segment` first.

For optional local validation:

```powershell
& .\.venv\Scripts\pytest.exe -q -p no:cacheprovider --basetemp=.test-tmp
& .\.venv\Scripts\ruff.exe check src runtime tests scripts
```

See `requirements-lock.txt` and `docs/REPRODUCIBILITY.md` for the pinned
environment and complete reproduction sequence.

## Handoff for other agents

This repository contains the tokenizer implementation and selected runtime
artifact, but not the immutable source corpus. The current Windows machine
stores the corpus at:

```powershell
$D = 'D:\DevTools\KapampanganTokenizer\kapampangan-general-corpus-v1'
$Z = 'D:\DevTools\KapampanganTokenizer\kapampangan-general-corpus-v1.zip'
```

These paths are machine-specific examples. On another machine, set `$D` to the
directory containing `metadata/dataset-manifest.json` and the `data/` folder.
Every dataset command accepts `--dataset-root`; no command should rely on a
hidden default path.

The corpus ZIP and directory are external dependencies for dataset
verification, lexicon construction, training preparation, and validation. They
are not needed by the standalone runtime, which only reads
`artifacts/selected-tokenizer/`.

### Reproduce the derived training state

The following creates the intentionally uncommitted, dataset-derived files:

```powershell
$K = '.\.venv\Scripts\kapampangan-morphbpe.exe'

& $K verify-dataset --dataset-root $D --output .\reports\dataset-verification-local.json
& $K build-lexicon --dataset-root $D --output-dir .\resources
& $K prepare-training --dataset-root $D `
  --lexicon .\resources\training-lexicon.json `
  --output-dir .\runs\prepared --engine rust
```

Use `docs/REPRODUCIBILITY.md` for the complete candidate-training and
validation sequence. Do not parse or train on `data/test.csv`.

### Files intentionally absent from the baseline commit

- `resources/training-lexicon.json` and its manifest: derived from the corpus;
  add only in a private repository or after redistribution rights are cleared.
- `artifacts/candidates/` and `artifacts/determinism-rebuild/`: reproducible
  intermediate outputs; the selected artifact is already included.
- `runs/`: generated training streams.
- `.venv/`, `target/`, and `*.pyd`: local environments and build products.
- `AGENT_CONTEXT.md`: machine-local agent handoff and intentionally untracked.

If the derived lexicon is approved for a private commit, add it explicitly:

```powershell
git add resources/training-lexicon.json resources/training-lexicon-manifest.json
git commit -m "Add derived training lexicon"
```

Agents should preserve the dataset fingerprint, keep the corpus outside the
repository, and avoid pushing unless the repository owner explicitly requests
it.

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

To inspect morphology for one raw word, the training lexicon is required:

```powershell
& $K segment `
  --lexicon .\resources\training-lexicon.json `
  --text "sinulat"
```

`segment` and `tokenize` are separate views of the pipeline. Morphology is
used during training before BPE learning; the standalone runtime uses only the
selected artifact and does not load the lexicon.

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
