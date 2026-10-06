# Weighted MorphBPE v3 tokenizer (6,080; penalty 4)

Artifact fingerprint: `acb94f46ad30279ff5e44eb3c34fb897a96fb52a64508bdb308895c3c20b9fb3`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 4 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
