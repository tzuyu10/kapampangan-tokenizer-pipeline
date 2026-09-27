# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 32)

Artifact fingerprint: `a5816946ff7e99cad4a15216f826ac412c1799a00cd77a1a1efe5d188f394455`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
