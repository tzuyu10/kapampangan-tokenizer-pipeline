# Weighted MorphBPE v3 tokenizer (8,192; penalty 4)

Artifact fingerprint: `034db661ef27e732bc1220cad5bcea0b39ece75ae169ab25494dd138963be0cc`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - 4 * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
