# expanded_morphology_v4 penalty-32 extension tokenizer (8,192)

Artifact fingerprint: `266e3c436ec79c3def27c764875837cfcd0ceb1832319d34088cf59299b908fe`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=32, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
