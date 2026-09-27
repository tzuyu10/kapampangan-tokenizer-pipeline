# expanded_morphology_v4 penalty-128 extension tokenizer (6,080)

Artifact fingerprint: `ba3a1e70b76813d910a8ab92844c1321d2c8a45297887a6c2c593c992711a1d7`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=128, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
