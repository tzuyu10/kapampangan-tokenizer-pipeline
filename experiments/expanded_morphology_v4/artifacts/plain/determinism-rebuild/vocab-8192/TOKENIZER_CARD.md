# Expanded morphology v4 tokenizer (plain; 8,192)

Artifact fingerprint: `bcbde127e86e647a4c9f0dec58f814ad62449b1c2881cc9e23e316c8b6e31234`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
Ordinary Plain-BPE control: no morphology boundaries of any kind.
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
