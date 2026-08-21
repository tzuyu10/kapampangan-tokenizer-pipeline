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
compare-tokenizers
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

To inspect morphology for one raw word or a sentence, the training lexicon is
required:

```powershell
& $K segment `
  --lexicon .\resources\training-lexicon.json `
  --text "Kasulatan ya."
```

A single pretoken retains the word-level segmentation response. Multi-pretoken
text returns normalized text, a `||`-delimited display, and lossless pretokens
with offsets; word pretokens contain an `analysis`, while whitespace,
punctuation, and symbols have `analysis: null`.

`segment` and `tokenize` are separate views of the pipeline. Morphology is
used during training before BPE learning. The artifact-only `tokenize` command
is the paper-aligned standard runtime and does not load the lexicon. Use `prop`
for the primary matched comparison at any trained size:

```powershell
prop 6k original "text or sentence"
prop 8k original "text or sentence"
prop 16k original "text or sentence"

prop 6k experimental "text or sentence"
prop 8k experimental "text or sentence"
prop 16k experimental "text or sentence"
```

`prop` runs both the Plain-BPE artifact and MorphBPE-trained artifact through
the same ordinary, lexicon-free BPE runtime. Morphology affects MorphBPE merge
learning only. The optional text defaults to `kabukasan`.

The `prop`, `comp`, and `prop2` shortcuts print a compact human-readable view:

```text
kabukasan
  MorphBPE  3 | ka + bukas + an
  Plain BPE 2 | kabu + kasan
              | fertility morph 3.00 plain 2.00
```

For sentences, `|` separates input words and `+` separates subword pieces
inside a word. Fertility is the number of word-subword tokens divided by the
number of input word pretokens. The underlying comparison data remains
unchanged; use the explicit `compare-tokenizers` command when full JSON with
IDs, offsets, artifact fingerprints, and morphology diagnostics is required.

An isolated training-only boundary-safe extension is available through `prop2`:

```powershell
prop2 6k "kabukasan"
prop2 8k "kabukasan"
prop2 16k "kabukasan"
```

`prop2` also uses ordinary artifact-only BPE inference and loads no lexicon at
runtime. Its trainer defers merges that would cross the five frozen word forms
whose boundaries changed under the source-adjudicated experiment. All three
artifacts emit `ka + bukas + an` for `kabukasan`. This is an explicitly labelled
extension with a closed-set guarantee, not the primary MorphBPE paper
replication and not a claim about unseen words. See
`experiments/boundary_safe_v1/README.md` for construction and diagnostics.

The full-corpus conservative source-reconciliation experiment is available as
`v2prop` (source-enriched MorphBPE with standard runtime) and `v2prop2`
(boundary-safe extension with standard runtime):

```powershell
v2prop 6k "sinulat"
v2prop 8k "sinulat"
v2prop 16k "sinulat"

v2prop2 6k "sinulat"
v2prop2 8k "sinulat"
v2prop2 16k "sinulat"
```

At all three sizes, `v2prop2` emits `s + in + ulat`, `S + in + ulat`, and
`ka + bukas + an`. Its hard exact guarantee covers only lowercase/title-case
variants of those two required regressions; all 1,197 externally
relationship-supported derivations are
reported as a measurement list, not a simultaneous guarantee. Keep `prop` as
the paper-replication baseline, treat `v2prop` as the source-enriched
experimental condition, and report `v2prop2` separately as an extension. See
`experiments/source_adjudicated_v2/README.md` for the frozen evidence policy,
artifacts, limitations, and reproduction commands.

The weighted v3 extension removes the v2 word-specific guarantee and applies a
general boundary-conflict penalty to every merge candidate:

```text
score(pair) = allowed_frequency - penalty * crossing_frequency
```

Use `v3prop` with a vocabulary size, one of the frozen penalties 1/2/4/8, and
optional quoted text:

```powershell
v3prop 6k 1 "sumulat"
v3prop 8k 2 "Sumulat ako ng tula"
v3prop 8k 4 "sinulat at kabukasan"
v3prop 16k 8 "sumulat"
```

V3 contains no surface-form override or hard runtime guarantee. It retains
ordinary lexicon-free BPE inference and must be reported as a weighted
MorphBPE extension/ablation, not as the unmodified paper algorithm. The penalty
grid is intentionally unselected until independent development/test morphology
and downstream translation evaluation are available. See
`experiments/weighted_morphbpe_v3/README.md` for reproduction and current silver
diagnostics.

The explicit `compare-tokenizers` command and its compact `comp` shorthand are
a separate runtime-constrained diagnostic extension:

```powershell
& $K compare-tokenizers `
  --plain-artifact .\experiments\source_adjudicated_v1\artifacts\plain-bpe-tokenizer `
  --morph-artifact .\experiments\source_adjudicated_v1\artifacts\selected-tokenizer `
  --morph-lexicon .\experiments\source_adjudicated_v1\resources\training-lexicon.json `
  --text "kabukasan"
```

That diagnostic requires equal vocabulary sizes and a runtime lexicon. It first
segments each word and applies BPE independently inside each segment, providing
a hard boundary guarantee not specified by the paper. BPE pieces remain
statistical subwords rather than gold morpheme labels.

For the runtime-constrained diagnostic, the installed `comp` shortcut resolves
all paths automatically:

```powershell
comp 8k original "kasulatan"
comp 8k experimental "kabukasan"
comp 16k experimental "Bukas na datang ing pangulo."
```

Accepted sizes are `6k`, `8k`, and `16k`; accepted conditions are `original`
and `experimental`. Run it inside the repository, or add `--root PATH` when
invoking it elsewhere. Activate this repository's virtual environment first so
its `comp.exe` is resolved ahead of Windows' unrelated system `comp.exe`.

For the original canonical 6,080-entry implementation, use:

```powershell
& $K compare-tokenizers `
  --plain-artifact .\experiments\source_adjudicated_v1\artifacts\plain-bpe-tokenizer `
  --morph-artifact .\artifacts\selected-tokenizer `
  --morph-lexicon .\resources\training-lexicon.json `
  --text "kasulatan"
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
