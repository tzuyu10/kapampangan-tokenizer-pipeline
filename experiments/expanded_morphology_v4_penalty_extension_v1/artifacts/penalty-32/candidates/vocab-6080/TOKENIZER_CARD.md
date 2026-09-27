# expanded_morphology_v4 penalty-32 extension tokenizer (6,080)

Artifact fingerprint: `2dc38cb89b2b3545c134b43c932a1f343453372bdbaeea090900d5566d759ad1`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=32, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
