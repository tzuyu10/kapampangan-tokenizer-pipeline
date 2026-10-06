# Validation-only Vocabulary Selection

## Frozen candidate grid

The paper requires validation-based vocabulary selection but supplies no sizes.
Before reading candidate validation results, the training inventory fixed this
`implementation_defined` formula:

```text
nearest multiple of 64 to m * sqrt(training word types), m in {4, 8, 16}
```

Targets are bounded below by initial vocabulary plus 64 and above by feasible
growth. With 143,529 training word types and an initial vocabulary of 1,592,
the immutable grid became **1,656, 3,008, 6,080**. Its fingerprint is
`5f098d5b92dc2428a7324783df0413536ff29c3896702b4971f90cf6c2194d0b`.
`configs/candidate-grid.json` records `validation_results_observed_when_frozen:
false` and the predeclared hierarchy.

## Proxy metrics

All morphology metrics are provisional development proxies, not gold-based or
formal thesis results. They use the supplied unadjudicated lexicon on the 3,284
validation records only.

- **FR**: produced lexical subword tokens / source word occurrences.
- **MBF1**: micro F1 of tokenizer boundaries against accepted proxy morpheme
  boundaries.
- **MCF1**: F1 over distinct word-type pairs that share tokenizer units and/or
  proxy morphemes, implemented with exact bit-set counting.
- **Morphological distance**: for each accepted proxy analysis, the symmetric
  difference between predicted and proxy boundary sets divided by the number
  of possible internal code-point boundaries; occurrence-weighted mean.
- **Proxy crossings**: proxy protected boundaries missed by runtime tokens.
  These are validation generalization diagnostics, not training constraint
  violations.

## Candidate results

| Target | Distance | MBF1 | MCF1 | FR/tokens per word | Character fallback | Unknown fallback | Avg token length | Nonspace tokens/sentence | Proxy crossings | Training violations |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,656 | 0.447541163 | 0.451628468 | 0.112633790 | 3.218019015 | 0.558431164 | 0.000171953 | 1.576409623 | 205.804202192 | 2,225 | 0 |
| 3,008 | 0.299174466 | 0.450506820 | 0.158185193 | 1.921535288 | 0.236864564 | 0.000287972 | 2.640032776 | 127.324299635 | 4,241 | 0 |
| 6,080 | **0.264722944** | 0.445369260 | 0.152629388 | **1.580627798** | **0.154672149** | 0.000350081 | **3.209431182** | **106.688185140** | 4,684 | 0 |

All candidates used 198,790 validation word occurrences, 34,046 word types,
and 6,058 proxy-scored occurrences. `reports/validation/` retains complete
precision, recall, counts, per-candidate fingerprints, tokens per sentence
including whitespace, and protected-root/compound over-segmentation counts.

## Frozen selection rule and result

The lexicographic hierarchy was: reject nonzero training boundary violations;
minimize distance; maximize MBF1; maximize MCF1; minimize FR when morphology is
maintained; then prefer smaller vocabulary. No candidate was rejected. Target
**6,080** won at the first differentiating criterion: the lowest morphological
distance (0.2647229439611416). Its lower FR is supporting compactness evidence;
its lower MBF1 than the smallest candidate does not override the previously
frozen primary criterion.

Validation was not absorbed into final training. No test record or test metric
participated in grid construction, evaluation, selection, or finalization.

