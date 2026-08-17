# Future Statistical Analysis Plan

Status: `future_phase`; no hypothesis test was computed in this goal.

## Paired observations

For each metric, define the paired observational unit before test access
(sentence for translation metrics; the paper-aligned unit for each tokenizer
metric). Retain baseline and proposed values for the same ID and compute
`d_i = proposed_i - baseline_i`, with direction interpreted per metric.

## Descriptive statistics

Report sample size, arithmetic mean, sample standard deviation (`n-1`
denominator), mean paired difference, SD of paired differences, confidence
interval, and transparent missing/excluded-pair counts. Do not turn aggregated
corpus BLEU alone into fabricated sentence-level pairs.

## Primary inference

Use a two-tailed paired-samples t-test at `alpha = 0.05` on the frozen paired
differences. Report the test statistic, degrees of freedom, exact p-value,
confidence interval, and decision without equating non-significance with proof
of equivalence.

Effect size is Cohen's paired `dz`:

```text
dz = mean(d_i) / sample_sd(d_i)
```

Predefine behavior for zero SD (report undefined/infinite as mathematically
appropriate; do not divide silently).

## Assumptions and sensitivity

Inspect paired-difference distributions, missingness, extreme outliers, and
dependence introduced by duplicate/document groups. For severe non-normality or
extreme outliers, add a two-tailed Wilcoxon signed-rank sensitivity analysis
with zero/tie handling and software version documented. This supplements rather
than opportunistically replaces the primary test.

Multiplicity handling and the family of confirmatory metrics must be frozen
before test access. Development validation metrics remain descriptive proxies
and are excluded from formal hypothesis tests.

