# expanded_morphology_v4 penalty-64 extension tokenizer (6,080)

Artifact fingerprint: `0542852ece480bff55988452ebf1b85de1fe4590468a7210fd10cdfb7d4293bd`

Genuinely new crossing_penalty=64 configuration, trained on the exact
prepared stream (verified byte-identical provenance -- see README.md) that
produced the real expanded_morphology_v4 penalty-1/2/4/8 artifacts already
deployed in the webapp. Ranks merge pair p by
`allowed_frequency(p) - 64 * crossing_frequency(p)`. Inference is ordinary
lexicon-free BPE. Not selected, not a frozen thesis artifact.
