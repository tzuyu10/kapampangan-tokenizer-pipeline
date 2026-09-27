# expanded_morphology_v4 penalty-256 extension tokenizer (6,080)

Artifact fingerprint: `310297b30ff757e9bae971b66f6bc1defde5a94c96d668ef9e6fc4c55d05e4fc`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=256, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
