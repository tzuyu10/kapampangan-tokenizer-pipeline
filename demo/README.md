# Kapampangan MorphBPE — standalone demo

A self-contained 3-way comparison of Kapampangan subword tokenizers, for
presentations. Detached from the research repo — nothing here imports it.

```
python demo.py                       # words + consistency demo + scored sentences
python demo.py "Minta ya keni."      # your own Kapampangan text
python demo.py "d|in|atang ya keni"  # '|' marks gold morpheme boundaries
```

**Requirements:** Python 3.11+. Nothing else — pure standard library, no
`pip install`, no internet.

## The three tokenizers

All trained on the **same** Kapampangan corpus, **same** vocab (6,080),
**same** special tokens. Only the subword algorithm / bias differs.

| tokenizer | what it is |
|---|---|
| **MorphBPE `penalty-8`** | ordinary BPE, merge learning biased against crossing morpheme boundaries (`allowed_freq(p) − 8·crossing_freq(p)`). The Phase-3-selected tokenizer. |
| **Plain BPE** | the identical BPE with the morphology penalty switched off. |
| **Unigram-LM** | SentencePiece's Unigram-LM — **NLLB's own subword algorithm** — trained from scratch on this corpus (`unigram-ablation`). Isolates "MorphBPE vs BPE" from "BPE vs Unigram". Decoded here by a ~40-line stdlib Viterbi that matches the `tokenizers` library piece-for-piece. |

At **runtime all three are plain, lexicon-free** — no analyzer, no
dictionary. MorphBPE's learned vocabulary just tends to cut on morpheme
boundaries instead of through them.

## Phase 3 result (boundary F1, held-out morphology, vocab 6,080)

| tokenizer | boundary F1 (dev) | note |
|---|---|---|
| Plain BPE | 0.198 | no morphology |
| MorphBPE, hard-constrained | 0.268 | the literal paper algorithm; barely above plain |
| Unigram-LM (NLLB's algorithm) | 0.293 | same corpus / vocab / specials |
| **MorphBPE, penalty-8** | **0.4639** (0.4093 test) | **selected** |

Two robust findings: F1 is monotone in the crossing penalty (8 tops the
tested grid), and smaller vocab retains more boundaries (6,080 > 8,192 >
16,384). MorphBPE beats NLLB's own algorithm under matched conditions, so
the gain is the morphology bias, not "BPE ≠ Unigram".

## The three intrinsic metrics (per sentence, from `demo.py`)

| metric | question |
|---|---|
| **1.1 Fertility Rate** | pieces per word (lower = tighter) |
| **1.2 Morpheme Boundary F1** | do the tokenizer's cuts land on real morpheme boundaries? |
| **1.3 Morphological Consistency F1** | when two words share a morpheme (e.g. root `ligtas` in `kaligtasan` / `magligtas` / `pangaligtas`), is it cut the same way in both? |

`demo.py` scores 1.2 and 1.3 with functions lifted verbatim from
`experiments/tokenizer_selection_v1/run_selection.py`; gold morpheme splits
come from that experiment's frozen `reference-morphology.csv`
(silver, not native gold).

## Contents

| path | what |
|---|---|
| `demo.py` | the runnable 3-way comparison + stdlib Unigram decoder |
| `morphbpe-penalty8/` | the selected tokenizer — 9 files, fingerprint `f2ea195a…` |
| `plain-bpe/` | matched Plain-BPE baseline — fingerprint `005f6da9…` |
| `unigram-lm-6080/` | matched Unigram-LM (`unigram-ablation`) — fingerprint `454549cf…` |
| `kapampangan_morphbpe_runtime/` | the BPE loader, pure stdlib |
| `PROVENANCE.md` | exact source paths + SHA-256s (byte-identical to the research repo) |

## Loading it yourself

```python
from pathlib import Path
from kapampangan_morphbpe_runtime import Tokenizer

tok = Tokenizer(Path("morphbpe-penalty8"))
enc = tok.encode("Sinulat ne ing lagyu na.")
print([t.token for t in enc.tokens])   # subword strings
print(list(enc.ids))                    # integer ids, 0..6079
print(tok.decode(enc.ids))              # round-trips
```
