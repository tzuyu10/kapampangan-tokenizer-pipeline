# Weighted MorphBPE v3 tokenizer (8,192; penalty 8)

Artifact fingerprint: `8e83bc43cc7f4365d540a75eb845c91b823a88d2cbd2bee6f3f6d6db9e75c5e9`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 8 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
