# expanded_morphology_v4 penalty-16 extension tokenizer (8,192)

Artifact fingerprint: `e0d6d798c7a02892d7a1c0e3a2610a7996e3ecac10870b74f93ba8c4ac12d3ea`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=16, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
