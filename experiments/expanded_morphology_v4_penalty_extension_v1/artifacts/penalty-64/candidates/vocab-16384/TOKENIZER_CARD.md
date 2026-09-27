# expanded_morphology_v4 penalty-64 extension tokenizer (16,384)

Artifact fingerprint: `0b063e3c1b65440ff776b78a1e45bd206499cc4f96f0329cc9cffe0e6f3e77a5`

Genuinely new crossing_penalty=64 configuration, trained on the exact
prepared stream (verified byte-identical provenance -- see README.md) that
produced the real expanded_morphology_v4 penalty-1/2/4/8 artifacts already
deployed in the webapp. Ranks merge pair p by
`allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is ordinary
lexicon-free BPE. Not selected, not a frozen thesis artifact.
