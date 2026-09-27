# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 2)

Artifact fingerprint: `c16abead0b964e8192f5899a44e1d2e6ee266665aa6ff2a8a451ad20404be4ec`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 2 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
