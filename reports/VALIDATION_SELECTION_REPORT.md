# Validation Selection Report

Status: completed development-only selection; evidence is provisional proxy.

The grid `[1656, 3008, 6080]` and lexicographic rule were fingerprinted before
validation results existed. Evaluation read exactly 3,284 validation records,
198,790 word occurrences, and 34,046 word types. Of those, 6,058 occurrences
had accepted proxy multi-morpheme analyses. Test content was not read.

| Target | Morph distance | MBF1 (P/R) | MCF1 (P/R) | FR | Character fallback | Unknown fallback | Avg length | Tokens/sentence, nonspace | Tokens/sentence, all | Proxy crossings | Root/compound extra boundaries |
| ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,656 | 0.447541163 | 0.451628468 (0.329790358 / 0.716235174) | 0.112633790 (0.060851451 / 0.755744221) | 3.218019015 | 0.558431164 | 0.000171953 | 1.576409623 | 205.804202192 | 265.234470158 | 2,225 | 60,436 |
| 3,008 | 0.299174466 | 0.450506820 (0.442206117 / 0.459125112) | 0.158185193 (0.151995758 / 0.164900108) | 1.921535288 | 0.236864564 | 0.000287972 | 2.640032776 | 127.324299635 | 186.754567600 | 4,241 | 8,948 |
| 6,080 | **0.264722944** | 0.445369260 (0.498263889 / 0.402627216) | 0.152629388 (0.276066621 / 0.105470521) | **1.580627798** | **0.154672149** | 0.000350081 | **3.209431182** | **106.688185140** | **166.118453106** | 4,684 | **2,951** |

Every candidate had zero constrained-training protected-boundary violations.
Target 6,080 was selected because the first differentiating criterion was the
minimum morphology-distance proxy, 0.2647229439611416. It also had the lowest
fertility/over-segmentation diagnostics. MBF1 and MCF1 are reported rather than
hidden, even though they do not lead the frozen lexicographic comparison after
distance differs.

Selection fingerprint:
`3ca3a1781c5544014a50615032124ddc02875204a0d7501b39e481c2dbfb657f`.
Complete machine-readable reports and exact decimals are under
`reports/validation/` and `configs/selected-candidate.json`.

These values are not final thesis metrics: references were not human-reviewed,
the native NLLB tokenizer was not compared, and the held-out test stayed sealed.

