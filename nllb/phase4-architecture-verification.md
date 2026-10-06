# Phase 4 — NLLB-200 embedding-swap architecture verification

Ran 2026-08-31 on Google Colab (Tesla T4, 14.56 GiB), against the real
`facebook/nllb-200-distilled-600M` weights
(`M2M100ForConditionalGeneration`, 615M params, `torch` 2.11 / `transformers`
4.57). Notebook: `notebooks/phase4-nllb-architecture-verification.ipynb`.
Raw result: `phase4-architecture-verification.json`
(SHA-256 `35e04b62c93135b533d28824a3a2ee821886e2fa9fa014f2102e82fdf1b572af`).

## Verdict: the embedding-swap approach is sound, with one operational caveat

The core assumption in `nllb_contract.py` —

> "expose a genuinely independent source embedding without changing tied
> target embeddings or output projection"

**holds.** 7 of 8 mechanical checks pass; the 8th is an expected,
well-understood HuggingFace behaviour, not an architectural obstacle.

### What passed (7/8)

| check | result |
|---|---|
| `shared` (256,206 × 1,024) starts tied across encoder-input, decoder-input, and `lm_head` | ✅ confirmed |
| encoder `embed_tokens` can be replaced with an independent `nn.Embedding(6080, 1024)` | ✅ |
| decoder `embed_tokens` and `lm_head` stay tied to `shared`, shape unchanged (256,206 × 1,024) | ✅ |
| after the swap the **only** trainable tensor is the new embedding — exactly 6,225,920 params (6080 × 1024) | ✅ |
| forward + backward: gradient flows **only** to the new embedding (`grad_sum` 108.85); `shared` / decoder / `lm_head` grads are `None` | ✅ |
| target logits stay full-width (`[2, 6, 256206]`) | ✅ |
| `model.generate()` runs end to end, encoder(new 6,080 vocab) → decoder(NLLB vocab), all output ids in target range | ✅ |
| loss ≈ 11.32 (≈ `ln(256206)` = 12.45, i.e. near-uniform for a random encoder embedding) | sane |

### The caveat (the 1 "fail")

`model.tie_weights()` **re-points the encoder `embed_tokens` back to `shared`**
(the check `explicit_retie_keeps_encoder_independent` came back `false`, and
`after_tie_weights_encoder_shape` reverted to `[256206, 1024]`). `lm_head`
stayed correctly tied to `shared` through the re-tie — only the encoder is
affected.

`from_pretrained` calls `tie_weights()` at load, and it can also be triggered
by `resize_token_embeddings`, `save_pretrained` → `from_pretrained`
round-trips, and some `.to()` / gradient-checkpointing paths.

### What Phase 5 must do

1. Load the model, **then** apply the encoder-only swap (direct attribute
   assignment on `model.model.encoder.embed_tokens` — **not**
   `set_input_embeddings`, which also repoints the decoder).
2. Do **not** call `tie_weights()` afterwards.
3. For checkpointing, save the custom encoder embedding as a separate
   `state_dict` and re-apply the swap after every model reload — do not rely
   on `save_pretrained`/`from_pretrained` to preserve the untied encoder.
4. Optionally set `model.config.tie_word_embeddings` handling so any
   framework-internal `tie_weights()` is a no-op — but verify this does not
   also break the wanted `lm_head` ↔ `shared` tie (in this run the re-tie
   kept `lm_head` tied, so leaving the config alone and just not calling
   `tie_weights()` is the simplest safe path).

### Notes for Phase 5 wiring (unchanged from before, confirmed here)

- `decoder_start_token_id` = 2, `pad_token_id` = 1 (NLLB model side).
- Source tokenizer `<pad>` = 0 (project artifacts) — the new encoder
  embedding uses `padding_idx=0`, independent of the model's pad id 1.
- Target language code is **`tgl_Latn`** (Tagalog); NLLB-200 has no separate
  `fil_Latn`.
- `scale_embedding=True` — the encoder multiplies embeddings by
  `sqrt(1024) ≈ 32`; initialise the new embedding at std `1024**-0.5` so the
  scaled magnitude starts near 1.
- The contract's `source_vocabulary_size` (6,080) matches both Phase-5
  conditions (`morphbpe`, `penalty-8`); its `artifact_fingerprint` still
  points at the old canonical 6,080 tokenizer and will need repointing to
  the chosen v4 artifact(s) at Phase 5.
