# Results

## Table 2 — Tokenizer-Level Performance

| Metric | proposed | plain |
|---|---|---|
| Vocabulary size | 12464 | 14459 |
| Fertility Rate (corpus) | 1.6015 | 1.4626 |
| Fertility Rate (sentence mean) | 1.6198 | 1.4770 |
| Morpheme Boundary F1 | — | — |
| Morphological Consistency F1 | 0.0139 | 0.0042 |

## Table 4 — Statistical Test Results (Tokenizer-Level)

| Metric | Mean (Proposed) | Mean (Baseline) | Test | p | Cohen's dz | Decision (Holm) |
|---|---|---|---|---|---|---|
| Fertility Rate (vs plain) | 1.6198 | 1.4770 | paired t-test | 2.699e-235 | 0.939 | reject H0 |
| Morphological Consistency F1 (vs plain) | — | — | paired bootstrap | 0 | — | reject H0 |

