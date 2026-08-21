# Weighted MorphBPE v3 tokenizer (6,080; penalty 1)

Artifact fingerprint: `c3e140b93a3b47a937005b483329b75fb7663c82be1ec461deb363d503c6f823`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 1 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
