# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 64)

Artifact fingerprint: `73fb319c5a64598c850587480dcee4c4a87c21e3bcd1fe34ab65c6cd5b7bc2db`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
