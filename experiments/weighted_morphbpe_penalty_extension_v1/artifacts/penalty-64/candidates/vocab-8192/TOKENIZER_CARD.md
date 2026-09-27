# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 64)

Artifact fingerprint: `5b964cdbcd37ec5c3fb1eab8c0d66604b59c5030f86e0e810838896f32f3ba80`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
