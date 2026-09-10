# Phase 5 Colab run, 2026-09-04 — partial, transcript-recovered

**Not an official `phase5-results.json` save.** The Colab session hit the
free-tier "Cannot connect to GPU backend (usage limits)" wall mid-run; the
`phase5-results.json` the user downloaded (`phase5-results-2026-09-04.json`,
same folder) was saved *before* `morphbpe/seed0` finished, so it contains
only `nllb_zeroshot`. The numbers below are transcribed by hand from the
Colab console output the user pasted in chat — real data, but not machine-
verified against a saved JSON. Re-running will regenerate `morphbpe/seed0`
properly (the notebook re-trains anything not already a key in
`phase5-results.json`).

## Reference (saved, confirmed)

`nllb_zeroshot` (no training): dev chrF++ 33.04 / BLEU 11.45,
**test_bible chrF++ 33.78 / BLEU 11.69**, **test_ood chrF++ 33.49 / BLEU 9.06**.

## morphbpe/seed0 — completed, printed, NOT in the saved JSON

10 epochs, batch 8, lr 3e-4, warm-started `nn.Embedding(6080,1024)`:

| epoch | train loss | dev loss |
|---|---|---|
| 1 | 4.774 | 5.034 |
| 2 | 4.620 | 4.940 |
| 3 | 4.539 | 4.926 |
| 4 | 4.521 | 4.915 |
| 5 | 4.520 | 4.892 |
| 6 | 4.509 | 4.846 |
| 7 | 4.491 | 4.811 |
| 8 | 4.477 | 4.799 |
| 9 | 4.471 | 4.781 |
| 10 | 4.464 | 4.781 |

Dev loss still trending down at ep10 (~0.03/epoch, no plateau — patience 3
never tripped, epoch cap 10 was the limiter). Never came close to a
"coherent generation" loss range.

**Final scores: DEV chrF++ 12.47 / BLEU 0.31, test_bible chrF++ 13.01 /
BLEU 0.24, test_ood chrF++ 10.10 / BLEU 0.12. Took 122.6 minutes.**

**This is far below `nllb_zeroshot` on every metric** — training the
warm-started embedding made translation quality *worse* than not training
at all, not just "not better."

## morphbpe/seed1 — trained, eval crashed, nothing saved

Same 10-epoch schedule ran to completion (dev loss 5.025 -> 4.704, same
non-plateaued trend), but the GPU backend became unavailable during the
post-training generation eval (before the `-> morphbpe/seed1 ...` summary
line printed) -> `results["morphbpe/seed1"]` was never assigned ->
**~2 hours of GPU time lost with no recoverable score.**

## Reading

Two independent embedding-only fine-tunes have now collapsed well below
zero-shot: random-init at 598 pairs (first run, 2026-09-02) and
**warm-started at ~3,590 pairs (this run)**. The warm-start hypothesis --
that starting inside NLLB's embedding space would let the frozen encoder
cope -- does not hold at either data scale tested. The dev-loss trend
(linear, ~0.03/epoch, unplateaued) extrapolates to ~80+ more epochs
(~16h/seed at this pace) to reach a loss range associated with usable
generation -- consistent with a **capacity bottleneck** (only a
6,080x1,024 embedding is trainable; every attention/FFN/decoder weight is
frozen), not a data-quantity or under-training problem.

Also notable: **122.6 min/run is ~4-6x the ~20-35 min I estimated when
building the bundle.** The notebook trains/evals in fp32 -- a T4's fp16
tensor cores are much faster than its fp32 throughput, so switching to fp16
autocast is the likely fix and should be done before spending more Colab
time on any recipe (embedding-only or LoRA).

---

# Local LR-diagnostic, 2026-09-08 (RTX 4050, bf16)

`experiments/nllb_finetune_v1/local_diagnostic.py`, warm-start, **lr 3e-3**
(10x the Colab recipe), batch 8, bf16 autocast. Results in
`reports/phase5-results-local.json`.

- **`nllb_zeroshot` (local, bf16)**: test_bible chrF++ 33.58 / BLEU 11.51,
  test_ood chrF++ 33.69 / BLEU 9.57 -- **matches Colab's 33.78/33.49 within
  ~0.5**, so the local pipeline is faithful.
- **`morphbpe/seed0`, lr 3e-3**: dev-loss 4.323 (ep1) -> **4.196 (ep3, best)**
  then bounced 4.40 / 4.41 / 4.41 / 4.32 / 4.24 / 4.36 -> **early stop ep9**.
  **DEV chrF++ 11.54, test_bible chrF++ 11.33 / BLEU 0.58, test_ood chrF++
  13.25 / BLEU 0.19. 95.5 min** (bf16, early-stopped -- faster than Colab's
  122.6 min fp32).

**Verdict: capacity bottleneck confirmed.** The 10x LR *did* help
optimisation -- dev-loss floor dropped from ~4.78 (Colab, lr 3e-4, 10
epochs) to ~4.20, reached in 3 epochs not 10 -- but then it **floored** and
oscillated, and **generation quality did not move** (chrF++ ~11-13, same
collapse). Three embedding-only runs now fail to beat zero-shot's ~33.6:
random-init @ 598 pairs, warm-start @ 3,590 pairs, warm-start + 10x LR @
3,590 pairs. Init, data scale, and LR are all exhausted as cheap levers.
Training only a 6,080x1,024 input embedding, everything else frozen, cannot
make NLLB-200 translate from a novel Kapampangan tokenisation. Next per the
notebook's own escalation note: LoRA-on-encoder, or accept the null result.

---

# LoRA-on-encoder, 2026-09-08 (RTX 4050, bf16)

`experiments/nllb_finetune_v1/local_lora.py`. Warm-started embedding (6.23M,
emb-lr 1e-3) **+ LoRA r=16 on the encoder self-attn q_proj/v_proj, all 12
layers** (786K, lora-lr 2e-4). Decoder + lm_head + shared frozen; no
`tie_weights()` after the swap. 25 epochs (ran to the cap -- kept finding
tiny improvements), bf16, batch 8. 185 min (thermal-throttled late).

- dev-loss 3.612 (ep1) -> **3.300 (ep25, best)** -- broke well below the
  embedding-only floors (~4.2 local / ~4.8 Colab); front-loaded (0.15 in the
  first 5 epochs, ~0.16 over the next 20).
- **DEV chrF++ 20.13 / BLEU 2.16;  test_bible chrF++ 20.41 / BLEU 1.90;
  test_ood chrF++ 14.02 / BLEU 0.21.**

**Verdict: LoRA helps but does not close the gap.** vs embedding-only it
~doubled test_bible chrF++ (11.3 -> 20.4) and BLEU (0.6 -> 1.9), and cut the
dev-loss floor by ~0.9 nats. But it is still **~13 chrF++ / ~10 BLEU below
`nllb_zeroshot` (33.6 / 11.5)**, and `test_ood` (register transfer) barely
moved (13.2 -> 14.0) -- BLEU ~0.2 there means the output is still largely
incoherent; the chrF++ ~20 is mostly character overlap from shared
Kapampangan/Filipino/Spanish vocabulary, not fluent translation.

## Run 5 -- Option 4: encoder-LoRA for `penalty8` + `unigram6080` (local, 2026-09-08)

`local_lora.py --condition penalty8` then `--condition unigram6080`,
identical recipe to `morphbpe-lora` (warm-start embedding 6.23M @ emb-lr
1e-3 + LoRA r16 alpha32 encoder self-attn q_proj/v_proj all 12 layers 786K
@ lora-lr 2e-4; decoder frozen; no `tie_weights()`; bf16, batch 8, 25
epochs, ran to the cap). 212 min + 207 min back-to-back on the RTX 4050.

- `penalty8-lora/seed0`: dev-loss 3.608 -> **3.332 (ep25)**. DEV chrF++
  19.24 / BLEU 1.36; **test_bible chrF++ 18.45 / BLEU 1.04; test_ood
  chrF++ 13.59 / BLEU 0.27.**
- `unigram6080-lora/seed0`: dev-loss 3.617 -> **3.260 (ep23, best)**. DEV
  chrF++ 21.16 / BLEU 2.25; **test_bible chrF++ 20.59 / BLEU 1.82; test_ood
  chrF++ 16.16 / BLEU 0.49.**

## The Phase 5 picture (2026-09-08, COMPLETE -- all 3 tokenizers)

| condition | best dev-loss | test_bible chrF++ / BLEU | test_ood chrF++ / BLEU |
|---|---|---|---|
| `nllb_zeroshot` (no training) | -- | **33.6 / 11.5** | **33.7 / 9.6** |
| `morphbpe` embedding-only (lr 3e-4, Colab) | 4.781 | 13.0 / 0.24 | 10.1 / 0.12 |
| `morphbpe` embedding-only (lr 3e-3, local) | 4.196 | 11.3 / 0.58 | 13.2 / 0.19 |
| `unigram6080` + LoRA-on-encoder (local) | **3.260** | 20.6 / 1.82 | 16.2 / 0.49 |
| `morphbpe` + LoRA-on-encoder (local) | 3.300 | 20.4 / 1.90 | 14.0 / 0.21 |
| `penalty8` + LoRA-on-encoder (local) | 3.332 | 18.5 / 1.04 | 13.6 / 0.27 |

The proposal's stated setup -- swap NLLB's tokenizer for Kapampangan
MorphBPE and adapt lightly while keeping the decoder frozen -- **does not
beat zero-shot NLLB** at ~3,600 silver pairs, for any of the three
tokenizers. Robust across random-vs-warm init, 598-vs-3,590 pairs, lr
3e-4-vs-3e-3, embedding-only-vs-+encoder-LoRA, and all 3 tokenizers.

**Cross-cut finding:** the LoRA ranking is `unigram6080 >= morphbpe >
penalty8` on every split, and dev-loss agrees (3.26 < 3.30 < 3.33). NLLB's
own subword algorithm (Unigram-LM, matched vocab/corpus) adapts *best*
downstream; MorphBPE penalty-8, the Phase-3 *intrinsic* winner (boundary F1
0.46), adapts *worst*. **The intrinsic morpheme-boundary metric does not
predict downstream MT quality in this frozen-decoder regime** -- if
anything mildly inverse at the margin. Single seed each, so hold loosely,
but the dev-loss ordering corroborates. A thorough, reproducible negative
result; accept it and reframe the thesis around the Phases 1-4 intrinsic
tokenizer contribution + zero-shot NLLB as the honest MT baseline.
