# expanded_morphology_v4 penalty-64 extension tokenizer (8,192)

Artifact fingerprint: `b49913254279a1df0e0c577ca04c41bd8b7cf30887a1513b22179d32abfb18b2`

Genuinely new crossing_penalty=64 configuration, trained on the exact
prepared stream (verified byte-identical provenance -- see README.md) that
produced the real expanded_morphology_v4 penalty-1/2/4/8 artifacts already
deployed in the webapp. Ranks merge pair p by
`allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is ordinary
lexicon-free BPE. Not selected, not a frozen thesis artifact.
