# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 32)

Artifact fingerprint: `8f4fabb275e125a306fae13e265d27102ff5b06e76fd65cd1d5dfaa5811ddf92`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
