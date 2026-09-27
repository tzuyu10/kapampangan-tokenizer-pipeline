# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 8)

Artifact fingerprint: `49830afc3cd55905386932ecef748df3eef5fc1c17f9d2ea3108347852b2b677`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 8 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
