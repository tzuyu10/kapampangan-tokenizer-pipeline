# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 128)

Artifact fingerprint: `9d5d69f270bde55c65cacd32311bf4c13f43181113260793b6a2617d303ac62a`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
