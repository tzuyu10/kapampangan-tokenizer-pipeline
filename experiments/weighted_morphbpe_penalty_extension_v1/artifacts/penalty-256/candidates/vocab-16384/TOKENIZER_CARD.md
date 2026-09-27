# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 256)

Artifact fingerprint: `ed36d297e7f03cd1487887146e9e0d50173d8ade7166bf55e4d0b8b68fb7cdfe`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
