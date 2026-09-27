# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 8)

Artifact fingerprint: `034304354ae7150e2fe502396c66bedc02e8a10f046182f8f1e74894d9b8bb0e`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 8 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
