# Expanded morphology v4 tokenizer (morphbpe; 6,080)

Artifact fingerprint: `5c34233ebd33939aad1c6af9ccfb041855ccfa84a98b9894a24a4ed54c24803d`

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
