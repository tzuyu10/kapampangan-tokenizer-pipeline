# Weighted MorphBPE v3 experiment

This extension uses `allowed_frequency - penalty * crossing_frequency`.
It has no word-specific training override or runtime guarantee.
All results below use the 1,197-form training-derived silver audit, not independent gold.

| Vocab | Condition | Exact types | Missed-boundary types | Boundary F1 | Fertility |
|---:|---|---:|---:|---:|---:|
| 6,080 | `plain_bpe` | 51 | 1,008 | 0.146410 | 1.659431 |
| 6,080 | `paper_morphbpe` | 68 | 979 | 0.347909 | 2.252748 |
| 6,080 | `weighted_penalty_1` | 116 | 889 | 0.512592 | 2.493897 |
| 6,080 | `weighted_penalty_2` | 162 | 761 | 0.606285 | 2.542447 |
| 6,080 | `weighted_penalty_4` | 194 | 670 | 0.654157 | 2.542999 |
| 6,080 | `weighted_penalty_8` | 208 | 652 | 0.676571 | 2.542005 |
| 8,192 | `plain_bpe` | 56 | 1,025 | 0.121586 | 1.501961 |
| 8,192 | `paper_morphbpe` | 83 | 983 | 0.358481 | 2.173819 |
| 8,192 | `weighted_penalty_1` | 136 | 894 | 0.523262 | 2.417951 |
| 8,192 | `weighted_penalty_2` | 187 | 772 | 0.616329 | 2.482574 |
| 8,192 | `weighted_penalty_4` | 232 | 681 | 0.666641 | 2.485004 |
| 8,192 | `weighted_penalty_8` | 252 | 661 | 0.689246 | 2.478873 |
| 16,384 | `plain_bpe` | 76 | 1,063 | 0.061210 | 1.244794 |
| 16,384 | `paper_morphbpe` | 123 | 1,014 | 0.352043 | 2.044573 |
| 16,384 | `weighted_penalty_1` | 194 | 920 | 0.538619 | 2.313173 |
| 16,384 | `weighted_penalty_2` | 275 | 796 | 0.629989 | 2.385197 |
| 16,384 | `weighted_penalty_4` | 341 | 699 | 0.682042 | 2.396355 |
| 16,384 | `weighted_penalty_8` | 358 | 674 | 0.703925 | 2.391936 |

No penalty or vocabulary has been selected. Freeze independent development/test
morphology before choosing a configuration or making a thesis effectiveness claim.
