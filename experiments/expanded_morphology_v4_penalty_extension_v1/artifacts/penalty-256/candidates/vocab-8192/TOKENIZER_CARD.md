# expanded_morphology_v4 penalty-256 extension tokenizer (8,192)

Artifact fingerprint: `32d7f9971aa7e7ad5346599cc3a6d7308c252769228d395f460a74a3b5f95f40`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=256, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
