# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 16)

Artifact fingerprint: `8b6b380e693dd386290be2d941ddc0e6b5a0369ae9b502a3a86ebe14f0931235`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
