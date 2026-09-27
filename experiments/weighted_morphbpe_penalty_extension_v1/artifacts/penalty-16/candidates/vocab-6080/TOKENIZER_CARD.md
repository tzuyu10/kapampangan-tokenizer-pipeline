# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 16)

Artifact fingerprint: `b3ac9c5c43e85ae1d11433dccc80591717da0cad7e75cdd1ee6ee3dcf82621e8`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
