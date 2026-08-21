# Weighted MorphBPE v3 tokenizer (16,384; penalty 4)

Artifact fingerprint: `26b0b64a0e7699b961b97af73302dca0f2e3e4176a846af90263795509138db5`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 4 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
