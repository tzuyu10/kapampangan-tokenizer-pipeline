# Source-adjudicated v2 experiment

Status: trained and validated provisional local-test candidates; no model selected.

- Accepted root keys: **1,830**.
- Explicitly supported derived types: **1,197**.
- New training-boundary types versus v1: **889**.
- Plain, paper-runtime MorphBPE, and boundary-safe candidates: 6,080 / 8,192 / 16,384.
- Runtime is lexicon-free standard BPE for every reported tokenizer.
- These are silver training/audit data, not held-out morphology gold.

## Runtime boundary results

| Vocab | Paper MorphBPE missed accepted | Boundary-safe missed guaranteed regressions | `sinulat` | `kabukasan` |
|---:|---:|---:|---|---|
| 6,080 | 2,552 | 0 | `s + in + ulat` | `ka + bukas + an` |
| 8,192 | 2,570 | 0 | `s + in + ulat` | `ka + bukas + an` |
| 16,384 | 2,645 | 0 | `s + in + ulat` | `ka + bukas + an` |

Keep the original `prop` condition as the paper-replication baseline.
Use `v2prop` as the source-enriched condition with paper-aligned runtime.
Report `v2prop2` separately as a boundary-safe extension/ablation.
The hard exact guarantee covers only lowercase/title-case `sinulat` and `kabukasan`; all 1,197 source-supported derivations remain a measured evaluation list.
Vocabulary size remains a downstream validation choice, not a morphology truth claim.
