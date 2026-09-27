# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 128)

Artifact fingerprint: `668b4a7f4df6054227d61eff3c2ae17d5aab82d6c5d34f7b119c1b46e44b2ecd`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
