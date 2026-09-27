# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 4)

Artifact fingerprint: `60969389a6cccc07ebd292111a28785fb5b307ff33611464953342739b87ee5a`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 4 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
