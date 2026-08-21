# Expanded morphology v4 tokenizer (penalty-1; 8,192)

Artifact fingerprint: `0b1bfbb9f68fd9f57ea9b06b3135d8ef5aa4efe06ab3b9b6ef721d720120bd3c`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
Weighted MorphBPE thesis extension (not the unmodified MorphBPE paper
algorithm). Each candidate merge pair p is ranked by

`allowed_frequency(p) - 1 * crossing_frequency(p)`

where both quantities are summed globally across the v4-resegmented training
corpus (see EVIDENCE.md for the new affix/circumfix/suffix/reduplication rules
that produced its protected boundaries), not only within one word. A merge is
still never applied across a protected boundary during training; the penalty
only demotes a pair's global rank when it frequently conflicts with a
boundary elsewhere in the corpus.
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
