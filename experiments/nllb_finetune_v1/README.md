# NLLB fine-tune v1 (Phase 5)

Adapts `facebook/nllb-200-distilled-600M` to **Kapampangan -> Filipino**
(`tgl_Latn`) and compares three source-tokenizer conditions in the
low-resource regime this project actually has.

**All training data is SILVER.** A native-speaker validation pass on
`experiments/parallel_extraction_v2/reports/native-speaker-review-sheet.csv`
is still the gate for any thesis-gold claim.

## Conditions (each trained condition x 3 seeds)

| condition | encoder source tokenizer | trainable params |
|---|---|---|
| `nllb_native` | NLLB SentencePiece, 256K vocab, pretrained on 200 languages (Kapampangan read as `tgl_Latn`) | encoder input embedding, untied from `shared` (256,206 x 1,024) |
| `morphbpe` | paper-aligned hard-constrained MorphBPE @ 6,080, trained on Kapampangan | fresh `nn.Embedding(6080, 1024)` |
| `penalty8` | weighted MorphBPE, crossing penalty 8 @ 6,080, trained on Kapampangan | fresh `nn.Embedding(6080, 1024)` |
| `unigram6080` | **Unigram-LM (NLLB's own subword algorithm) trained from scratch on this project's Kapampangan corpus** @ 6,080 | fresh `nn.Embedding(6080, 1024)` |

Everything else frozen; `tie_weights()` never called after the swap
(Phase 4, `nllb/phase4-architecture-verification.md`). Plus a
`nllb_zeroshot` reference (no training), once. = 12 training runs + 1
zero-shot, ~3 h on a T4.

### The comparison, two layers

- **Fair headline:** `morphbpe` / `penalty8` **vs `unigram6080`** -- same
  vocab (6,080), same Kapampangan corpus, same fresh-embedding recipe;
  only the subword algorithm differs (morphology-constrained BPE vs
  Unigram-LM). This isolates the MorphBPE effect from the vocab-size /
  corpus / multilingual-exposure confounds. (`unigram6080` is the
  `train_unigram_ablation.py` artifact from 2026-08-22, built for exactly
  this; disclosed limitation: the `tokenizers`-library Unigram trainer is
  not byte-reproducible, so it is one frozen instance.)
- **Reference:** `nllb_native` (embedding-adapted) + `nllb_zeroshot` -- the
  pretrained off-the-shelf NLLB-200 tokenizer the thesis proposal names
  (Scope & Limitation, p.15). Not a like-for-like tokenizer test.

## Pipeline

```powershell
# 1. freeze the split (pure stdlib)
.\.venv\Scripts\python.exe .\experiments\nllb_finetune_v1\build_split.py

# 2. build the Colab bundle (uses the MorphBPE runtime tokenizers)
.\.venv\Scripts\python.exe .\experiments\nllb_finetune_v1\build_colab_bundle.py
```

- `build_split.py` -> `data/{train,dev,test}.csv` + `reports/split-manifest.json`.
  **Story-level holdout**: five whole native-authored stories
  (`Ing Panabilin kang Roy`, `Ing kekaming Komunidad...`,
  `Kebaytan nang Imang Lily`, `Transportasyun king Pilipinas`,
  `Kaluguran da ka Ima`) are removed entirely -> TEST 70 (48 story + 22
  gold_v1, `claude_review == "ok"` only). DEV 45 (15 each
  gold_stories/gold_v1/silver_a). TRAIN 598 (keeps silver_b + the 24
  `partial`-flagged rows). seed 20260902. Leakage asserted.
- `build_colab_bundle.py` -> `data/bundle/{train,dev,test}.jsonl` + `meta.json`.
  Each row carries the Kapampangan side pre-tokenised three ways
  (`morphbpe_ids`, `penalty8_ids`, `unigram_ids` -- all vocab 6,080, ids in
  [0, 6080), `<s>`/`</s>` included; `unigram_ids` is pretokenised the
  project's way then Unigram-encoded per segment), so the notebook needs no
  project code. Needs the `tokenizers` lib (`.venv` `nllb-baseline` extra).

## Run

`notebooks/phase5-nllb-morphbpe-finetune.ipynb` -- upload the four bundle
files, `Run all`, T4 GPU, ~3 h (12 training runs + zero-shot, results
written incrementally so a disconnect is recoverable). Emits
`phase5-results.json` (per-run + mean/std across seeds). See the notebook's
own summary before running.
