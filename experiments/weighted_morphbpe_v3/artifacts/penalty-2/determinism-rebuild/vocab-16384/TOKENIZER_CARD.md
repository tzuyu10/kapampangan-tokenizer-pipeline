# Weighted MorphBPE v3 tokenizer (16,384; penalty 2)

Artifact fingerprint: `cafdc22f4748bc1762ba157ef6ea87b9a1f7ed9bba95cee578784c01d87a9f59`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 2 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
