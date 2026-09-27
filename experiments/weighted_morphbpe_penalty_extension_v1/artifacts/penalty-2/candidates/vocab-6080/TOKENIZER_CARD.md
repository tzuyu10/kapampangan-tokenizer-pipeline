# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 2)

Artifact fingerprint: `7e41fb4802650eb8c39ab8d164efa3caf6816dc1c4ccc93ce85891fc8b85d464`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 2 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
