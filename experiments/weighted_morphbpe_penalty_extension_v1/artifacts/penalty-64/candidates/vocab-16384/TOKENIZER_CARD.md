# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 64)

Artifact fingerprint: `a8f6c8465b0aa13a36fe27d76b54b24ad599768160936e278985cd190fb84164`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
