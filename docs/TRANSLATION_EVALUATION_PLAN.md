# Future Translation Evaluation Plan

Status: plan only; no translation evaluation was executed.

## Tokenizer conditions

1. Proposed selected Kapampangan MorphBPE tokenizer.
2. Native NLLB-200 tokenizer baseline.

On adjudicated tokenizer test references, report Fertility Rate, Morpheme
Boundary F1, and Morphological Consistency F1 with per-sentence or per-word
paired observations retained for statistics. Development proxy scores in this
repository must not be reused as final results.

## Translation conditions

1. Baseline NLLB-200 Distilled 600M with native source and target tokenization.
2. Adapted NLLB-200 Distilled 600M with this tokenizer on the Kapampangan
   source side only, a newly initialized source embedding, and native Filipino
   target tokenization/generation.

Use the same reviewed parallel records, splits, schedule, optimizer, batch
size, seeds, stopping/checkpoint rule, and decoding configuration. Verify the
target vocabulary, target tokenizer, decoder, and output projection are
unchanged.

## Data protocol

- Obtain approximately 13,000 rights-reviewed, human-validated aligned
  Kapampangan-Filipino pairs.
- Create leakage-safe 80/10/10 aligned splits under a frozen seed/grouping
  policy, yielding approximately 1,300 sealed test pairs.
- Freeze all development choices before unsealing test.
- Preserve source IDs, target IDs, provenance, review state, and exclusion
  reasons.
- Never substitute PAM-ENG, fabricate Filipino, or use model-generated
  references.

## Translation metrics

Compute corpus BLEU and chrF++ with a frozen, versioned evaluator and exact
tokenization/case settings recorded. Retain sentence-level paired values for
sensitivity and diagnostic analysis, while treating corpus scores as the main
translation summary specified by the paper.

## Release gates

Before execution require: parallel-data readiness; language/rights review;
source-embedding feasibility; parameter-freeze tests; identical-run configs;
sealed test access procedure; evaluator lock; and a pre-registered statistical
table. Any target-side change or premature test access invalidates the intended
comparison.

