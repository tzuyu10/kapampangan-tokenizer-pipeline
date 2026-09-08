# Expanded morphology v4 tokenizer (plain; 6,080)

Artifact fingerprint: `005f6da948e787876732424df6f25efd6086e0a6d693918892683c346b57f478`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
Ordinary Plain-BPE control: no morphology boundaries of any kind.
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
