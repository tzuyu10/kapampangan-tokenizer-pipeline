# Weighted MorphBPE penalty extension v1

Follow-up to `weighted_morphbpe_v3` after that experiment's 12 artifacts were
scored against the real `data/validation.csv` for the first time (see
`experiments/weighted_morphbpe_v3/reports/official-validation-scores.json`).
Every penalty in the frozen v3 grid (1, 2, 4, 8) beat the shipped
`ConstrainedBPETrainer` candidate on boundary F1, with no sign of plateauing
by penalty 8. This experiment asks: does it keep helping past 8, and where
does it stop?

## Important: this is not a byte-identical extension of v3

`weighted_morphbpe_v3` trained on a prepared stream whose protected
boundaries came from `experiments/source_adjudicated_v2`'s adjudicated
lexicon (~3,311 roots). That lexicon is derived through a multi-stage
pipeline (`internet_root_reconciliation_v1` -> `source_adjudicated_v1` ->
`source_adjudicated_v2`) that depends on external reference dictionaries
(Forman 1971, Bergano/Samson, the ACD dataset) which are not present on this
machine and are not committed to the repo (by design -- see each
experiment's `.gitignore`). Reconstructing that exact chain was out of scope
here.

Instead, this experiment prepares its own training stream from the
canonical, already-committed `resources/training-lexicon.json` (the same
lexicon the shipped `ConstrainedBPETrainer` candidate and the official
`evaluate-validation` step both use). This is fully self-contained -- no
external files beyond the sealed dataset zip. The tradeoff: results here are
**not directly stitchable** onto the v3 penalty=1..8 points as one trend
line, because the underlying protected-boundary set differs. To keep the
sweep internally consistent, this experiment retrains penalty 1, 2, 4, and 8
itself (on the canonical lexicon) alongside the new 16, 32, 64 points, so
the within-experiment trend is a fair comparison.

## Grid

Penalties: 1, 2, 4, 8, 16, 32, 64. Vocabulary targets: 6,080 / 8,192 /
16,384 (same as v3). Single training pass per configuration (no
determinism-doubling rebuild check -- this is exploratory, not a frozen
thesis artifact).

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\weighted_morphbpe_penalty_extension_v1\run_extension.py --dataset-root "C:\DevTools\KapampanganTokenizer\kapampangan-general-corpus-v1"
```
