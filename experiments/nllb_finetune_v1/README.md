# NLLB fine-tune v1 (Phase 5)

Adapts `facebook/nllb-200-distilled-600M` to **Kapampangan -> Filipino**
(`tgl_Latn`) and compares three source-tokenizer conditions.

**Bible-primary refresh (2026-09-03).** The training set is now ~3,590 pairs,
built mostly from the **PLOC Kapampangan<->Tagalog Bible corpus** (the
proposal's primary downstream dataset) plus supplementary conversational /
story / news material. Two held-out test sets: `test_bible` (in-domain,
whole held-out chapters) and `test_ood` (register transfer: native-authored
stories + gold_v1).

**All training data is SILVER.** The Bible corpus provenance is via a
groupmate (believed PLOC / DLSU LTL, LGPL -- **UNCONFIRMED**; redistribution
rights unresolved). A native-speaker validation pass on
`experiments/parallel_extraction_v2/reports/native-speaker-review-sheet.csv`
is still the gate for any thesis-gold claim.

## Conditions (each trained condition x 3 seeds)

**Status: IN PROGRESS, not accepted.** A 4th condition (`bpe6080`) was added
2026-09-13 and is running; do not treat the 3-condition table in
`HANDOFF_PHASE5.md` as final until it lands.

| condition | encoder source tokenizer | trainable params |
|---|---|---|
| `morphbpe` | paper-aligned hard-constrained MorphBPE @ 6,080, trained on Kapampangan | fresh `nn.Embedding(6080, 1024)` |
| `penalty8` | weighted MorphBPE, crossing penalty 8 @ 6,080, trained on Kapampangan | fresh `nn.Embedding(6080, 1024)` |
| `bpe6080` | **plain (unconstrained) BPE — same algorithm + corpus as morphbpe/penalty8, no crossing penalty** @ 6,080 | fresh `nn.Embedding(6080, 1024)` |
| `unigram6080` | **Unigram-LM (NLLB's own subword algorithm) trained from scratch on this project's Kapampangan corpus** @ 6,080 | fresh `nn.Embedding(6080, 1024)` |

Each new embedding is **warm-started** from the mean of NLLB's own sub-token
embeddings for that token string (`data/bundle/vocab.json`). Everything else
frozen; `tie_weights()` never called after the swap (Phase 4,
`nllb/phase4-architecture-verification.md`). Checkpoints selected on **dev
loss**; generation eval on both test sets once at the end. Plus a
`nllb_zeroshot` reference (no training), once. Trained `nllb_native` was
dropped (256K trainable embedding OOMs a T4).

**History.** The first Colab run (random-init, 598 pairs) collapsed to
chrF++ ~10 vs zero-shot 33.6 -> warm-start rev. The 2026-09-03 refresh then
folded in the Bible corpus (598 -> ~3,590 pairs) and moved to 3 seeds + two
test sets; warm-start is kept (cheap, de-risks).

### The comparison, three layers

- **Fair headline:** `morphbpe` / `penalty8` **vs `unigram6080`** -- same
  vocab (6,080), same Kapampangan corpus, same fresh-embedding recipe;
  only the subword algorithm differs (morphology-constrained BPE vs
  Unigram-LM). This isolates the MorphBPE effect from the vocab-size /
  corpus / multilingual-exposure confounds. (`unigram6080` is the
  `train_unigram_ablation.py` artifact from 2026-08-22, built for exactly
  this; disclosed limitation: the `tokenizers`-library Unigram trainer is
  not byte-reproducible, so it is one frozen instance.)
- **Constraint ablation (added 2026-09-13):** `morphbpe` / `penalty8`
  **vs `bpe6080`** -- same vocab, same corpus, same BPE merge algorithm,
  same fresh-embedding recipe; only the morphology-boundary crossing
  penalty differs (constrained/weighted vs none). This isolates the
  morphology constraint itself, holding the algorithm family fixed --
  the cleanest downstream test of the thesis's actual claim. (`bpe6080`
  is the `plain` candidate from `expanded_morphology_v4`, already scored
  intrinsically in `tokenizer_selection_v1` as the floor of the boundary-F1
  ranking.)
- **Reference:** `nllb_zeroshot` -- the pretrained off-the-shelf NLLB-200
  tokenizer the thesis proposal names (Scope & Limitation, p.15). Not a
  like-for-like tokenizer test (confounded by vocab size and pretraining
  exposure, not just algorithm) -- see the two controlled layers above for
  the actual tokenizer claim.

## Pipeline

```powershell
# 1. freeze the split (pure stdlib)
.\.venv\Scripts\python.exe .\experiments\nllb_finetune_v1\build_split.py

# 2. build the Colab bundle (uses the MorphBPE runtime tokenizers)
.\.venv\Scripts\python.exe .\experiments\nllb_finetune_v1\build_colab_bundle.py
```

- `build_split.py` -> `data/{train,dev,test_bible,test_ood}.csv` +
  `reports/split-manifest.json`. seed 20260903, leakage asserted.
  - **`test_bible` (329)** -- whole held-out Bible **chapters**, per-book
    proportional (Gen/Deut/Jud), chapter-disjoint from train. The corpus is
    formulaic, so a verse-level random split would leak.
  - **`test_ood` (70)** -- five whole native-authored stories + 29 clean
    `gold_v1` sentences (`claude_review == "ok"` only). Register transfer.
  - **`dev` (238)** -- held-out Bible chapters + 15 each
    gold_stories/gold_v1/silver_a.
  - **`train` (3,590)** -- everything else: ~2,560 Bible verses + silver_a/b
    + silver_gemini (430) + stories + vocab + gold_v1 + the 24
    `partial`-flagged rows.
- `build_colab_bundle.py` -> `data/bundle/{train,dev,test_bible,test_ood}.jsonl`
  + `meta.json` + `vocab.json`. Each row carries the Kapampangan side
  pre-tokenised three ways (`morphbpe_ids`, `penalty8_ids`, `unigram_ids` --
  all vocab 6,080, ids in [0, 6080), `<s>`/`</s>` included), so the notebook
  needs no project code. `vocab.json` = id-ordered token strings per
  condition, for the warm-start. Needs the `tokenizers` lib (`.venv`
  `nllb-baseline` extra).

## Run

`notebooks/phase5-nllb-morphbpe-finetune.ipynb` -- upload the **six** bundle
files (`train`, `dev`, `test_bible`, `test_ood`, `meta.json`, `vocab.json`),
`Run all`, T4 GPU, **~4-6 h** (zero-shot + 3 conditions x 3 seeds; plan for
two Colab sessions -- results written incrementally, a re-run resumes). Set
`"seeds": [0, 1]` in `meta.json` for a faster first pass; `batch` is 8
(T4-safe for the longer Bible verses), raise to 16 if there is headroom.
Emits `phase5-results.json` (per-run + mean/std across seeds, both test
sets). See the notebook's own summary before running.
