# expanded_morphology_v4 penalty-256 extension tokenizer (16,384)

Artifact fingerprint: `5d6da57669ec9c5951398a7744d7bd22c02dfb8b330d90691b138ed5dc24771c`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty=256, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - 256 * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
