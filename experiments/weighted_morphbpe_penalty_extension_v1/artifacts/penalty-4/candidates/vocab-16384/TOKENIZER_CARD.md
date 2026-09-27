# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 4)

Artifact fingerprint: `ea955796e15e7873a4c7313aa59180fbe1508e10557470b00e2e3e0293ef7446`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 4 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
