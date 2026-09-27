# expanded_morphology_v4 penalty-128 extension tokenizer (16,384)

Artifact fingerprint: `343e9414ee9c5986482c05bd0b18a9b118237c63795e7cf55706459fcd0ab060`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=128, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
