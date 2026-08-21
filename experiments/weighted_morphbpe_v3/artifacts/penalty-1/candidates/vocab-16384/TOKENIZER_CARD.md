# Weighted MorphBPE v3 tokenizer (16,384; penalty 1)

Artifact fingerprint: `7406ddd46a02e36b50ae2c2adcb1f15389e99a918cd93e01df9262d18bf62144`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 1 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
