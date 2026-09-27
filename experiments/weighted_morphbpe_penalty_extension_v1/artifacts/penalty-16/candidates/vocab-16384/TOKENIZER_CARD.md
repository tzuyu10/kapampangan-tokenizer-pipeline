# Weighted MorphBPE penalty-extension tokenizer (16,384; penalty 16)

Artifact fingerprint: `4cddee39a6ef3485c3ab749077a847b8e977b3ec2b3871bd52b08252cfc86eb9`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
