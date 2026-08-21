# Expanded morphology v4 tokenizer (penalty-4; 16,384)

Artifact fingerprint: `c0b06753631238d86ba006981021d398e9ae873f272ec294fbeaacf006f39ffe`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
Weighted MorphBPE thesis extension (not the unmodified MorphBPE paper
algorithm). Each candidate merge pair p is ranked by

`allowed_frequency(p) - 4 * crossing_frequency(p)`

where both quantities are summed globally across the v4-resegmented training
corpus (see EVIDENCE.md for the new affix/circumfix/suffix/reduplication rules
that produced its protected boundaries), not only within one word. A merge is
still never applied across a protected boundary during training; the penalty
only demotes a pair's global rank when it frequently conflicts with a
boundary elsewhere in the corpus.
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
