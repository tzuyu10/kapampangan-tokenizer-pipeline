# Weighted MorphBPE v3 tokenizer (6,080; penalty 2)

Artifact fingerprint: `0d9e0bdc937b98dbabe0791245f372f6fb047b17c016d504a4d549621fcc2cea`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 2 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
