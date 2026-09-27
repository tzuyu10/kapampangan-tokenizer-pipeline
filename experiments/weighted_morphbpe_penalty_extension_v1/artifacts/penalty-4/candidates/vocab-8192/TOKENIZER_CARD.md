# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 4)

Artifact fingerprint: `3b06ee3d3f269971ec1f8c379bff56e9ab941428e21c7f2fa23c860f26ff6d5a`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 4 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
