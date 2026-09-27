# expanded_morphology_v4 penalty-32 extension tokenizer (16,384)

Artifact fingerprint: `9788e1f5779b4219d224a92af6fe2a42791203c602ba4d441579856d6176184b`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=32, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 32 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
