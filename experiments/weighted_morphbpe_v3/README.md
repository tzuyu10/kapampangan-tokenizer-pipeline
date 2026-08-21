# Weighted MorphBPE v3

This isolated thesis extension removes every word-specific training override and
runtime guarantee. It ranks each candidate pair using:

```text
allowed_frequency - crossing_penalty * crossing_frequency
```

The prepared corpus and 1,197-form external-relation audit are reused byte-for-byte
from `source_adjudicated_v2`. The Plain BPE and paper-aligned MorphBPE controls are
also reused, so the weighted merge score is the only new training intervention.

The frozen penalty grid is 1, 2, 4, and 8. Every penalty is trained at vocabulary
sizes 6,080, 8,192, and 16,384. No configuration is selected because an independent
development/test morphology split is not available.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\weighted_morphbpe_v3\run_experiment.py all
```

## Compare

Activate the project virtual environment, then supply vocabulary size, penalty,
and optional quoted text:

```powershell
v3prop 6k 1 "sumulat"
v3prop 8k 2 "Sumulat ako ng tula"
v3prop 8k 4 "sinulat"
v3prop 16k 8 "kabukasan"
```

Both sides use ordinary lexicon-free BPE inference. This condition must be
reported as a weighted MorphBPE extension/ablation, not as the unmodified
paper algorithm. Current aggregate measurements are training-derived silver
diagnostics and cannot substitute for an untouched gold test set.
