# Expanded morphology v4 tokenizer (morphbpe; 8,192)

Artifact fingerprint: `68a68b26f2d16f2cf83a868e40ade5e312a6eaf03e05fa978cdd776f969c7d4a`

Paper-aligned hard-constrained MorphBPE (Asgari et al., 2025, as
operationalized throughout this repository). Ordinary greedy BPE merge
learning over v4's expanded-morphology resegmented training stream
(`runs/prepared/training-stream.jsonl`; see `EVIDENCE.md` for the affix /
circumfix / suffix / reduplication rules that produced its protected
boundaries), with exactly one constraint: a merge is never applied across a
protected morpheme boundary. No penalty, no dropout, no scoring change --
this is the literal paper constraint, not the weighted `penalty-*` thesis
extension. A boundary-crossing pair can still be learned from its
unprotected occurrences elsewhere in the corpus. Standard runtime is
ordinary, deterministic, lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data by
this script (see `experiments/tokenizer_selection_v1/`).
