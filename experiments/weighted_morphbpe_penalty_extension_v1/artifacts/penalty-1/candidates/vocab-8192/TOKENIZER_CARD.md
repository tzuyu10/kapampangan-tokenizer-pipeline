# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 1)

Artifact fingerprint: `d5f87f462ec6ca8dd5b2c14b05886919cb9d985b46384094a39c585f872128f0`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 1 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
