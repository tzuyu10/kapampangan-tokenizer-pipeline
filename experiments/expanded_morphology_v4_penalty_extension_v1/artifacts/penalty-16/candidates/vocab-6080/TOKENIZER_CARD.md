# expanded_morphology_v4 penalty-16 extension tokenizer (6,080)

Artifact fingerprint: `21755c18386488038d6633ceb80c9c2375eea04ee0c020083da0ba46ca4fba52`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=16, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 16 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
