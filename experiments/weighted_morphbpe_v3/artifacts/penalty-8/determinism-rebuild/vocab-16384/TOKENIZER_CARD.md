# Weighted MorphBPE v3 tokenizer (16,384; penalty 8)

Artifact fingerprint: `b2d5fcb673722bb90cec07143183421a962255508bf91ae4b53505654cee8c00`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 8 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
