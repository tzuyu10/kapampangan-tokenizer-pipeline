# expanded_morphology_v4 penalty-128 extension tokenizer (8,192)

Artifact fingerprint: `cb48b9873b2aa6cd7f1d1070c773305f54c92e0278cf52745225a4422e803b94`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=128, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 128 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
