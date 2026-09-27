# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 8)

Artifact fingerprint: `d7288ec6dba62b5d38aab491e2970990b5820dbcf7d80040c5decf797d9ac139`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 8 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
