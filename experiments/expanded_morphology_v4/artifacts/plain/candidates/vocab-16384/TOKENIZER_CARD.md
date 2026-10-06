# Expanded morphology v4 tokenizer (plain; 16,384)

Artifact fingerprint: `70ce8fc097a3556f013615e7e72c2de15db0b5d83c9185de293df1f39fd448d9`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
Ordinary Plain-BPE control: no morphology boundaries of any kind.
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
