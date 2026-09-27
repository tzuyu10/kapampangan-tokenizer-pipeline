# expanded_morphology_v4 penalty-16 extension tokenizer (16,384)

Artifact fingerprint: `27d02d78c45e97b3e8d865572b043a5c8cb9a45d80d46577a0cc4297a2b035ec`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=16, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
