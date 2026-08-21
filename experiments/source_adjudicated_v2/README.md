# Source-adjudicated v2

This isolated local experiment turns the complete internet/source reconciliation
into conservative provisional tokenizer-training data without changing any
canonical, source-adjudicated-v1, vocabulary-ablation, or boundary-safe-v1
artifact.

## Frozen adjudication policy

- Exact eligible Forman root/stem entries and explicitly labelled Bergano roots
  may add provisional roots.
- New affix boundaries require an explicit relationship: a Forman cross-reference
  to the reconstructed root, a derived form listed inside that Forman root entry,
  or the identical hyphenated segmentation in ACD.
- Root matches alone never authorize an affix split.
- Clitic hypotheses, competing analyses, roots shorter than three letters,
  corrupted/noisy rows, and Richards evidence remain held.
- Every decision is provisional silver data for local testing, not independent
  native-speaker or linguist gold.

The frozen result contains 1,830 provisional root keys and 1,197 explicitly
relationship-supported derived word types (18,105 corpus occurrences). Of these,
889 types/8,713 occurrences add boundaries beyond source-adjudicated v1; 308
confirm existing analyses.

## Trained candidates

Every family has matched 6,080, 8,192, and 16,384 vocabularies:

1. `plain`: identical surface/kind/frequency stream with every morphology
   boundary cleared.
2. `morphbpe`: source-adjudicated v2 morphology-constrained training followed by
   ordinary artifact-only BPE runtime.
3. `boundary-safe`: a separately labelled training extension whose hard exact
   runtime guarantee is limited to lowercase/title-case `sinulat` and
   `kabukasan`.

The complete 1,197-form relationship list is measured for both MorphBPE families,
but it is not a simultaneous hard guarantee. Attempting to enforce every form at
once produced severe character fragmentation because a context-free BPE merge can
be internal to one morpheme and cross a boundary in another word.

No candidate was selected: the raw validation split is unavailable, and these
source-derived rows are training/audit data rather than held-out gold.

## Simple comparisons

Activate the project virtual environment first. `v2prop` compares Plain BPE with
the source-enriched MorphBPE candidate using the paper-aligned standard runtime:

```powershell
v2prop 6k "sinulat"
v2prop 8k "sinulat"
v2prop 16k "sinulat"
```

`v2prop2` compares Plain BPE with the boundary-safe extension, also using standard
lexicon-free runtime:

```powershell
v2prop2 6k "sinulat"
v2prop2 8k "sinulat"
v2prop2 16k "sinulat"
```

Both commands accept any quoted word or sentence. Their default text is
`sinulat`. At all three sizes, `v2prop2` emits `s + in + ulat`,
`S + in + ulat`, and `ka + bukas + an`; `v2prop` still emits `sin + ulat`,
demonstrating that
MorphBPE-constrained learning biases but does not hard-enforce a word's boundary
under standard BPE inference.

## Reproduction

The adjudication stage needs the bundled Codex Python runtime because it includes
`pypdf`. The remaining stages use the project virtual environment.

```powershell
& 'C:\Users\Ken Audie\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  .\experiments\source_adjudicated_v2\run_experiment.py adjudicate `
  --forman-pdf 'D:\Downloads\Forman-KapampanganDictionary-1971.pdf'

& .\.venv\Scripts\python.exe `
  .\experiments\source_adjudicated_v2\run_experiment.py prepare

& .\.venv\Scripts\python.exe `
  .\experiments\source_adjudicated_v2\run_experiment.py train

& .\.venv\Scripts\python.exe `
  .\experiments\source_adjudicated_v2\run_experiment.py validate
```

Generated lexicons, streams, detailed decisions, reports, and tokenizer artifacts
stay below this experiment directory and are ignored by Git except for the two
human-readable summaries.

## Thesis interpretation

- Keep the original `prop` results as the paper-replication baseline.
- Treat `v2prop` as the source-enriched MorphBPE experimental condition with
  paper-aligned standard inference.
- Treat `v2prop2` only as a boundary-safe extension/ablation.
- Choose vocabulary size using held-out morphology and downstream translation
  metrics. Do not select 6K/8K/16K from these training-derived results alone.
