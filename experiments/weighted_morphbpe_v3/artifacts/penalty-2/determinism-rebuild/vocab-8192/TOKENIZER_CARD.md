# Weighted MorphBPE v3 tokenizer (8,192; penalty 2)

Artifact fingerprint: `7aa491995cf4092f8b916cfb79362a06babcf7cb6bf3f008e226b86ca114128e`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 2 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
