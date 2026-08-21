# The Machine Translation Pipeline — plain-language guide

This explains the **second half** of the system: how the tokenizer gets plugged
into NLLB-200 and how translation quality is measured.

---

## 1. What NLLB-200 distilled 600M actually is

An encoder–decoder Transformer from Meta covering 200 languages, 600 million
parameters. You give it a source sentence and a target-language tag; it
produces a translation.

```
Kapampangan text
   |
   v
[source tokenizer]  ->  token IDs
   |
   v
[embedding table]   ->  one vector per token
   |
   v
[encoder]           ->  contextual meaning of the whole sentence
   |
   v
[decoder]           ->  generates Filipino, one token at a time
   |
   v
[output projection + softmax]  ->  picks the most likely next token
   |
   v
Filipino text
```

**Two corrections to the proposal's description (Chapter 1, p. 6–7):**

1. NLLB does **not** have a "Language Identifier" that detects the source
   language. You *tell* it the language with a tag token, and you force the
   first decoder token to be the target-language tag
   (`forced_bos_token_id = tgl_Latn`). Chapter 1 should say "language tags",
   not "language identifier".
2. The **distilled 600M has no Mixture-of-Experts layers**. MoE is in the 54B
   `NLLB-200 MoE` model. The distilled 600M is a plain dense Transformer.
   Chapter 1 currently attributes MoE to the 600M backbone; a panel member who
   knows the paper will catch it.

**And one thing the proposal never states:** Kapampangan is not one of NLLB's
200 languages. There is no `pam_Latn` code. So the baseline condition has to
pick *something* as the source tag. This pipeline uses `tgl_Latn` (Tagalog/
Filipino — the closest supported relative) and records the choice in
`config/pipeline.yaml` as `nllb.baseline_src_lang`. Write this choice and its
justification into Chapter 3; leaving it unspecified makes the baseline
unreproducible.

---

## 2. The graft: how our tokenizer gets in

The proposal says (p. 44): *"the source embedding layer will be resized and
newly initialized … only the source embedding parameters will be updated …
minimizing broader architectural modification."*

Here is what that requires in practice.

NLLB has **one** embedding matrix, `model.model.shared`, used in three places:

```
                 ┌──────────────► encoder input embeddings
model.shared ────┼──────────────► decoder input embeddings
                 └──────────────► lm_head (output projection)
```

There is no separate "source embedding layer" to resize. Resizing `shared`
would also resize the Filipino output vocabulary, which we must not touch. So
the only way to do what the proposal describes is to **untie the encoder
embedding**:

```
new_encoder_embeddings (our vocab) ──► encoder input
                 ┌──────────────► decoder input embeddings
model.shared ────┴──────────────► lm_head
```

That is a real architectural change, not a resize. `nllb/graft.py` performs it,
and it performs it **identically for every arm** so the arms are structurally
the same and differ only in tokenizer and initialisation.

### The three arms

| arm | source tokenizer | encoder embedding starts as | why it exists |
|---|---|---|---|
| `baseline` | native NLLB | a copy of the pretrained matrix | the thesis' baseline |
| `adapted` | proposed Morph-BPE | fresh, seeded from NLLB subwords | the thesis' proposed condition |
| `control` | native NLLB | fresh, same seeding procedure | **the missing control** |

Why `control` matters: in the two-arm design, `adapted` differs from `baseline`
in *two* ways at once — different tokenizer **and** a from-scratch embedding
table instead of a pretrained one. If `adapted` loses, you cannot tell whether
morphology failed or whether re-learning 8 million embedding parameters from
13,000 sentences failed. `control` holds the tokenizer fixed and re-initialises
the embedding, so the difference `adapted − control` isolates the tokenizer and
`baseline − control` measures the cost of re-initialisation. Run all three.

### Initialisation

`random` — what the proposal literally specifies: `N(0, d_model^-0.5)`.

`subword_average` (**default, recommended**) — for each new token, run its
surface string through the native NLLB tokenizer and average the pretrained
embeddings of the pieces. So `▁pamangan` starts life near NLLB's own idea of
`▁pama` + `ngan`, instead of at random noise. This is standard vocabulary
transfer and it matters a lot here: with the backbone frozen you are training
~8M parameters on ~260k token occurrences. Random init in that regime usually
does not converge, and reporting "morphology did not help" when the real cause
was an untrainable initialisation would be a wrong conclusion.

Set `nllb.init: random` if you want the literal thesis specification — but then
run both and report both.

### What trains

```python
for p in model.parameters():
    p.requires_grad = False
model.model.encoder.embed_tokens.weight.requires_grad = True
```

Roughly 0.5–4% of parameters, depending on vocabulary size. `graft_info.json`
records the exact count for every run — put it in Chapter 3.

---

## 3. Training

`nllb/train.py` — a plain loop, not `Seq2SeqTrainer`, so that the schedule is
provably identical across arms (which is what "held constant as much as
possible" has to mean to be defensible).

- AdamW, linear warmup then linear decay
- learning rate `5e-4` — high on purpose; only embeddings train
- label smoothing 0.1, gradient clipping 1.0
- mixed precision on GPU
- early stopping on validation loss, patience 3
- best checkpoint saved as `src_embeddings.best.pt`

The encoder embedding is saved **separately** rather than via
`save_pretrained()`, because Hugging Face's tied-weight bookkeeping can drop
weights it believes are shared. An explicit `.pt` is small and unambiguous.

**Runtime estimate on an RTX 4050 (6 GB), 13k pairs, batch 8 × accum 4:**
~4–8 minutes per epoch, so ~1 hour per arm for 10 epochs, ~3 hours for all
three. Decoding 1,300 test sentences with beam 5 takes another ~10–20 minutes
per arm. If you hit out-of-memory: drop `batch_size` to 4 and raise
`grad_accum` to 8 — the effective batch stays the same, which keeps the arms
comparable.

---

## 4. Decoding and evaluation

`nllb/translate.py` — beam search, 5 beams, `forced_bos_token_id = tgl_Latn`.
The target side is **unchanged in every arm**: Filipino is always produced with
NLLB's native vocabulary. Only the source side varies. That is what makes this
a controlled comparison.

### Metrics

| metric | what it counts | notes |
|---|---|---|
| **BLEU** | exact word n-gram overlap + brevity penalty | `sacrebleu`, `13a` tokeniser |
| **chrF++** | character n-grams (order 6) + word n-grams (order 2) | more sensitive to morphology, better for Philippine languages |

Always report the sacreBLEU **signature** (the pipeline saves it). BLEU computed
with a different tokeniser is a different number, and comparing across papers
without the signature is meaningless.

### Statistics

The proposal prescribes a paired-samples t-test on 1,300 sentences. That is
implemented, plus three additions:

1. **Shapiro–Wilk on the paired differences.** The proposal asserts normality
   via the Central Limit Theorem. Sentence-level BLEU differences are heavily
   spiked at zero; check rather than assume. If the check fails, the pipeline
   automatically reports Wilcoxon signed-rank as the primary test.
2. **Paired bootstrap on corpus-level BLEU/chrF++** (Koehn, 2004). Corpus BLEU
   is *not* the mean of sentence BLEUs, so a t-test on sentence scores does not
   test the number in Table 3. The bootstrap does. Report it as primary for
   RQ4 and keep the t-test as a secondary check.
3. **Holm–Bonferroni correction.** Five hypothesis tests at α = .05 gives a
   ~23% chance of at least one false positive. Holm is uniformly more powerful
   than Bonferroni and assumes nothing about independence. Both corrected and
   uncorrected decisions appear in the output.

Sentence-level BLEU is computed with `effective_order=True` (smoothing) —
without it, any sentence with no 4-gram match scores exactly 0 and the paired
differences become a degenerate distribution.

---

## 5. Running it

```bash
# after the tokenizer stages
python scripts/05_train_nmt.py --arm baseline
python scripts/05_train_nmt.py --arm adapted
python scripts/05_train_nmt.py --arm control      # recommended

python scripts/06_translate_eval.py --arms baseline adapted control
python scripts/07_report.py
```

Outputs land in `artifacts/`:

```
artifacts/
  tokenizer/  morphbpe.json, plainbpe.json, vocab_search.json
  nmt/<arm>/  src_embeddings.best.pt, train_log.json, graft_info.json
  results/    tokenizer_level.json, translation_level.json,
              hyp_<arm>.txt, REPORT.md      <- Tables 2-5 in Markdown
```

---

## 6. Reading the result honestly

Two outcomes are both publishable, and you should decide in advance how you
will write each one up:

**Adapted wins.** Then report the effect size (`cohens_dz`), the bootstrap CI,
and show `adapted − control` so the gain is attributed to the tokenizer rather
than to the re-initialisation.

**Adapted loses or ties.** This is the more likely outcome at 13k sentences with
a frozen backbone, and it is a legitimate finding: it would show that
morphological tokenisation improves *intrinsic* segmentation quality (Table 2)
without that improvement surviving into downstream translation under a
low-resource, frozen-backbone regime. That is exactly the kind of negative
result the low-resource NLP literature needs, provided you can show the
`control` arm and rule out "the embeddings simply never trained". Without the
control arm you cannot make that argument, which is the strongest practical
reason to run all three.
