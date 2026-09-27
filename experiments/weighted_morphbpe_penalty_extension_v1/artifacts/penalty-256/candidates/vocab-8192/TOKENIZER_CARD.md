# Weighted MorphBPE penalty-extension tokenizer (8,192; penalty 256)

Artifact fingerprint: `394e9921de5f8ff042540b0167301464d7eba45421925d225c8995538ed0314e`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
