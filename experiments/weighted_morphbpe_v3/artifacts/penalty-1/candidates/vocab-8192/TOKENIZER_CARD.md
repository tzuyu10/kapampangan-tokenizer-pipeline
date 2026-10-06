# Weighted MorphBPE v3 tokenizer (8,192; penalty 1)

Artifact fingerprint: `c02e4ff7686f90c2ca7a73de6454083a9285ffefd71855687cc84b783c468b08`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 1 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
