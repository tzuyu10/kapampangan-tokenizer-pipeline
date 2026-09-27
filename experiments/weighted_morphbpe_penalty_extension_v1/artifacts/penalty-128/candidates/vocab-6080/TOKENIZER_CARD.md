# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 128)

Artifact fingerprint: `c9d24e9bc352cfc616760fd6d3bfaf7adce963aa3761ae2dd76536eab2965b85`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
