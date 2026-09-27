# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 256)

Artifact fingerprint: `8ac4487a7ed1ea78fe7350624292fc844892635c581bf43197ca033728b24b7f`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
