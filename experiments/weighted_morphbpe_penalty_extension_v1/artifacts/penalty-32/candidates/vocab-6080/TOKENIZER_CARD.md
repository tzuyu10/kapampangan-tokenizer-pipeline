# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 32)

Artifact fingerprint: `fa380786e53b17350188ae1fe97e67293572aabef51033baeeb3e4861053bcab`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
