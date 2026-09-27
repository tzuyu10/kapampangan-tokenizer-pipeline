# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 1)

Artifact fingerprint: `c22309634aec2135f73ce23771992bd6d6f691c43dacffb5a0176d1a00dee09c`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 1 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
