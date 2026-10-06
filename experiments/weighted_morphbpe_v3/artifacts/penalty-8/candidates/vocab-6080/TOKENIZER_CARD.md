# Weighted MorphBPE v3 tokenizer (6,080; penalty 8)

Artifact fingerprint: `692863f152085920d69ffcfc2eabd487cddee0ddbc67041df43b83f5675bbf75`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 8 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
