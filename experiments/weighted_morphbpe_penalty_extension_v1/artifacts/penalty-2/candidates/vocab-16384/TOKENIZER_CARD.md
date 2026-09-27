# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 2)

Artifact fingerprint: `0f65f2bca62e2da9a01dfc57275e0889667aac148b857090031536feee295e6e`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 2 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
