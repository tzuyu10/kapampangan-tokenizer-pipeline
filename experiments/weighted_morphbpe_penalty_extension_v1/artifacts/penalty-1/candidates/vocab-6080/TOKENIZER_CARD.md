# Weighted MorphBPE penalty-extension tokenizer (6,080; penalty 1)

Artifact fingerprint: `bdf61d0af9649d28c87d823bfcdec0567bad9c053576df66e26f759d82793ffb`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - 1 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
