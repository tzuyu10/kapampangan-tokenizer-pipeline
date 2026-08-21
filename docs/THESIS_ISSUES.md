# Problems in the proposal, and why each one is a problem

Read this before your defence. Each entry says **what the proposal says**,
**why it breaks**, **what it costs you**, and **the fix** (all fixes are already
implemented or scaffolded in this repo).

Severity: 🔴 blocks a valid result · 🟠 will be challenged at defence · 🟡 tidy-up

Quick index:

| # | Issue | Severity |
|---|---|---|
| M-1 | Tokenizer condition and embedding initialisation are confounded | 🔴 |
| M-2 | Morpheme Boundary F1 has no gold standard — and risks circularity | 🔴 |
| M-3 | Fertility Rate vs NLLB is a foregone conclusion, not a test of morphology | 🔴 |
| N-1 | "Resize the source embedding layer" is not possible as described | 🔴 |
| N-2 | Kapampangan has no NLLB language code; the baseline is unspecified | 🟠 |
| S-1 | MCF1 cannot be fed into a per-sentence paired t-test | 🟠 |
| S-2 | Five tests at α=.05 with no multiple-comparison correction | 🟠 |
| S-3 | Paired t-test on sentence BLEU does not test the corpus BLEU you report | 🟠 |
| D-1 | A "unigram corpus" cannot yield 13,000 sentence pairs | 🔴 |
| D-2 | Domain mismatch between training (religious) and test (news/conversational) | 🟠 |
| T-1 | Figure 7 has no affix ordering — short affixes shadow long ones | 🟠 |
| T-2 | `TRY_CLITIC` "contains or ends with" over-segments | 🟠 |
| T-3 | No allomorph handling, though Chapter 1 names it as the core problem | 🔴 |
| T-4 | Reduplication excluded from scope but present in the data | 🟠 |
| T-5 | Boundary protection does not survive to inference | 🟠 |
| T-6 | MCF1 is undefined without two conventions the proposal never states | 🟠 |
| C-1 | NLLB-200 distilled 600M has no Mixture-of-Experts layers | 🟡 |
| C-2 | NLLB has no "Language Identifier" | 🟡 |
| C-3 | Character fallback does not guarantee processability; bytes do | 🟡 |
| C-4 | The Rust component is unjustified | 🟡 |

---

## 🔴 M-1 — Tokenizer condition and embedding initialisation are confounded

**Proposal (p. 44):** the adapted condition gets a resized, *newly initialised*
source embedding, trained while everything else is frozen. The baseline uses the
native tokenizer with its *pretrained* embeddings. Both are "fine-tuned with
identical settings".

**Why it breaks.** The two arms differ in two variables simultaneously:

| | tokenizer | source embedding at step 0 |
|---|---|---|
| baseline | native | pretrained on 200 languages |
| adapted | proposed | random noise |

The conceptual framework (p. 9) claims "any observed differences in translation
quality can be attributed primarily to the tokenizer condition". They cannot.
The initialisation difference is large and works entirely against the proposed
condition.

**What it costs you.** If the adapted arm loses — which is the likely outcome —
you cannot tell whether morphology failed or whether a randomly initialised
8M-parameter embedding table simply had too little signal to converge. Hypothesis
2 becomes untestable, and a sharp panel member will say so.

**Fix.** Add a third arm: native tokenizer **with a re-initialised embedding**,
trained identically. Implemented as `--arm control` in `scripts/05_train_nmt.py`.
Then:

- `adapted − control` = the effect of the tokenizer (what RQ4 actually asks)
- `baseline − control` = the cost of re-initialisation (a nuisance you now measure)

Also switch the default initialisation to `subword_average` (seed each new token
from the average of the NLLB pieces that spell it) so the adapted arm has a
realistic chance of converging. Keep `random` available and report both.

---

## 🔴 M-2 — Morpheme Boundary F1 has no gold standard, and risks circularity

**Proposal:** MBF1 compares predicted boundaries against "the validated morpheme
boundaries" (p. 55). Sources of Data and Research Instrument describe a lexicon
and expert consultations — but never a gold-annotated segmentation test set: no
size, no annotation protocol, no agreement measure.

**Why it breaks.** Two failures, either fatal:

1. **No data.** Without a gold file, RQ1.2 and RQ3.2 simply cannot be answered.
2. **Circularity.** The obvious shortcut is to generate the gold boundaries with
   the rule-based segmenter. But that segmenter *is* the training signal that
   constrained Morph-BPE. You would be grading a student against their own
   answer key: the proposed tokenizer wins by construction, at a level that says
   nothing about linguistic validity, while the NLLB baseline is measured
   against a standard it was never given.

**Fix.**
- `scripts/02_build_gold_template.py` produces an annotation template, sampled
  in frequency bands (high / mid / low / hapax) so the gold set isn't all
  function words, and flags word types that appear **only in test** so you can
  report MBF1 on unseen forms separately.
- **Two annotators** review independently. Report Cohen's kappa on boundary
  agreement. Target ≥ 1,000 word types; the SIGMORPHON-2022 systems the
  proposal cites (p. 55) were evaluated on sets of this order.
- `metrics/boundary_f1.load_gold()` **raises an error** on any row tagged
  `provenance=auto` unless you explicitly pass `allow_auto=True`. That guard
  exists so the circular version can never be run by accident.

---

## 🔴 M-3 — Fertility Rate vs NLLB is a foregone conclusion

**Proposal:** RQ3.1 tests whether the proposed tokenizer has lower fertility
than NLLB's native tokenizer.

**Why it breaks.** Fertility falls monotonically with vocabulary size and with
how much of that vocabulary is spent on the language in question. NLLB spreads
256,000 tokens across 200 languages, none of them Kapampangan. Any tokenizer
trained on Kapampangan wins this comparison — a plain BPE with no morphological
awareness whatsoever wins it too. So RQ3.1 as posed tests "did we train on
Kapampangan", not "does morphological awareness help".

**What it costs you.** A guaranteed p < .001 that supports no claim about
morphology. Worse, it invites the objection that the whole tokenizer-level
result is an artefact of vocabulary specialisation.

**Fix.** Add the **matched control tokenizer**: plain unconstrained BPE, same
corpus, same vocabulary size, same everything (`03_train_tokenizer.py
--plain-bpe`). Report all three columns in Table 2. NLLB stays as the *practical*
baseline (it is what a practitioner would actually use); plain BPE is the
*scientific* baseline for the morphology claim.

Expect the honest picture to be a **trade-off**: on the toy data in this repo the
morphology-aware tokenizer has *higher* fertility than plain BPE (1.56 vs 1.30)
but far better boundary F1 (0.82 vs 0.17). The proposal's own text anticipates
this (p. 54: fertility should be interpreted "provided that MBF1 and MCF1 are
maintained or improved") — the design just needs the control arm to show it.

---

## 🔴 N-1 — "Resize the source embedding layer" is not possible as described

**Proposal (p. 44):** "the source embedding layer will be resized and newly
initialized to match the proposed tokenizer vocabulary … minimizing broader
architectural modification."

**Why it breaks.** NLLB (`M2M100ForConditionalGeneration`) has exactly one
embedding matrix, `model.model.shared`, tied to encoder input, decoder input and
`lm_head`. There is no separate source embedding to resize. Calling
`resize_token_embeddings()` resizes **all three**, which would corrupt the
Filipino output vocabulary — the one thing the design says must stay constant.

Doing what the proposal wants therefore requires **untying** the encoder
embedding from the shared matrix. That is an architectural modification, and
describing it as "minimizing broader architectural modification" is a
contradiction the panel can point at.

**Fix.** `nllb/graft.py` performs the untie explicitly and applies it to **every
arm**, so all arms are structurally identical. Two implementation traps it also
handles:

- `model.set_input_embeddings()` must never be called afterwards — it re-links
  encoder, decoder and `lm_head` and silently undoes the graft.
- The new matrix is saved to its own `.pt` file, because `save_pretrained()` can
  drop weights it believes are tied.

Rewrite the Chapter 3 paragraph to say: *"the encoder input embedding is untied
from the shared embedding matrix and replaced with a new matrix sized to the
proposed vocabulary; decoder input embeddings and the output projection remain
tied to the original pretrained matrix and frozen."*

---

## 🟠 N-2 — Kapampangan has no NLLB language code

**Proposal:** the baseline is "NLLB-200 Distilled 600M using its native
tokenizer" for Kapampangan → Filipino.

**Why it breaks.** NLLB-200's 200 languages do not include Kapampangan. There is
no `pam_Latn` tag. Every NLLB call needs a source-language tag, so the baseline
is underspecified: results depend on whether you pick `tgl_Latn`, `ceb_Latn`,
`ilo_Latn`, or reuse an unused slot. Someone else cannot reproduce your baseline.

**Fix.** Fix the choice in config (`nllb.baseline_src_lang: tgl_Latn`, the
closest supported relative), justify it in Chapter 3, and ideally report a
one-paragraph sensitivity check with `ceb_Latn` and `ilo_Latn`. The proposed
condition sidesteps this by defining its own `__pam_Latn__` tag inside our
vocabulary.

---

## 🟠 S-1 — MCF1 cannot be fed into a per-sentence paired t-test

**Proposal (p. 61–62):** "both tokenizer conditions are evaluated on the same
1300 test sentences … n = 1300 paired observations per metric", applied to
Fertility Rate, MBF1 *and* MCF1.

**Why it breaks.** Fertility Rate has a per-sentence value — fine. MBF1 has a
per-*word* value, so its n is the number of annotated word types, not 1,300.
MCF1 is defined over **pairs of word types across the whole evaluation set**: it
has no per-sentence value at all. Most single sentences contain zero
shared-morpheme word pairs, so a per-sentence MCF1 is either undefined (0/0) or
degenerate.

**Fix.**
- Fertility Rate → paired t-test over sentences, n = 1,300. ✔ as proposed.
- MBF1 → paired t-test over annotated words, n = size of gold set. State the n.
- MCF1 → **paired bootstrap resampling over word types**
  (`metrics/consistency_f1.bootstrap_mcf1`), reporting mean difference, 95% CI
  and a two-sided p. Note this in the Statistical Treatment section.

---

## 🟠 S-2 — Five tests at α = .05, no correction

Five hypothesis tests (FR, MBF1, MCF1, BLEU, chrF++) each at α = .05 gives a
family-wise false-positive rate of about 23%. **Fix:** Holm–Bonferroni
(`stats.holm_bonferroni`) — uniformly more powerful than Bonferroni, no
independence assumption. The pipeline reports both corrected and uncorrected
decisions; put the corrected one in Tables 4 and 5 and mention the correction in
the Statistical Treatment section.

---

## 🟠 S-3 — Paired t-test on sentence BLEU does not test the corpus BLEU you report

Table 3 reports **corpus** BLEU. Corpus BLEU is not the mean of sentence BLEUs
(it pools n-gram counts and applies one brevity penalty), so a t-test on
sentence scores tests a different quantity than the number in your table. Also,
unsmoothed sentence BLEU is 0 whenever there is no 4-gram match, which makes the
paired differences a spike-at-zero distribution and violates the normality the
CLT argument is meant to license.

**Fix.** Report **paired bootstrap resampling** on corpus BLEU and chrF++
(Koehn, 2004 — the field standard) as the primary test for RQ4, and keep the
paired t-test on smoothed sentence-level scores as a secondary check. Both are
implemented (`stats/bootstrap.py`). Add Shapiro–Wilk on the paired differences
so normality is checked rather than assumed — the pipeline switches to Wilcoxon
automatically if it fails.

---

## 🔴 D-1 — A "unigram corpus" cannot yield 13,000 sentence pairs

**Proposal (p. 33):** the primary dataset is "approximately 13,000 parallel
sentence pairs drawn from the PLOC Kapampangan **unigram** religious corpus and
its corresponding Filipino parallel corpus".

**Why it breaks.** A unigram corpus is a word-frequency list — one word per line
with counts. It contains no sentences and therefore no sentence pairs. Either
the corpus is misnamed in the proposal, or the 13,000 figure comes from a
different resource that isn't named.

**What it costs you.** Everything downstream. 13,000 is the number that makes
the 80/10/10 split give exactly the n = 1,300 test set the Statistical Treatment
section assumes. If the sentence-aligned data does not exist, both the sample
size and the statistical power argument collapse.

**Fix — do this before the defence, not after.** Verify concretely:
1. Does PLOC actually distribute *sentence-aligned* Kapampangan–Filipino text,
   or only a word list? Download it and count lines.
2. If it is verse-aligned scripture, is the Filipino side the *same* translation
   tradition? Verse-to-verse alignment across different Bible translations is
   noisy and needs a filtering pass (`data/clean.py` has a length-ratio filter
   for exactly this).
3. Record the real number in Chapter 3 and re-derive the split sizes. If it is
   6,000 rather than 13,000, say so and adjust the power discussion.

---

## 🟠 D-2 — Domain mismatch

The bulk of the data is religious; the study then adds conversational and
news samples "to improve register diversity". If those extra samples are a small
fraction and land mostly in the test split, both arms will be evaluated on a
domain neither was trained on, and the comparison becomes noisy.

**Fix.** The stratified splitter (`data/split.py`) stratifies by
(length band × morphological complexity × **domain**), so each domain appears in
train, validation and test in the same proportion. Report the per-domain counts
from `split_report.json` in Chapter 3, and consider reporting BLEU/chrF++ broken
down by domain in Chapter 4 — that table is usually more informative than the
single pooled score.

---

## 🟠 T-1 — Figure 7 does not order the affixes

`TRY_PREFIX` iterates "for each prefix in LEXICON.PREFIXES" with no stated
order. If `ma-` is reached before `maka-` and `mag-`, it fires first: `magsulat`
is analysed as `ma + gsulat`, fails the root test, and the whole word falls
through to the fallback. The result depends on TSV row order, which is not a
property a segmentation algorithm should have.

**Fix.** `Lexicon.finalize()` sorts every affix list **longest-first**. Fix the
pseudocode in Figure 7 to say so (`for each prefix in LEXICON.PREFIXES ordered
by descending length`).

---

## 🟠 T-2 — `TRY_CLITIC` says "contains or ends with"

Matching a clitic anywhere in the word is destructive: the clitic `na` occurs
inside `nanu` ("what"), `danum` ("water"), `banal`. "Contains" would split all of
them.

**Fix.** Default to `endswith` (`clitic_match: suffix`). The literal "contains"
reading is still selectable for reproducing Figure 7 exactly, and it is
instructive to run it once and show the damage in your discussion.

---

## 🔴 T-3 — No allomorph handling, though Chapter 1 names it as the core problem

Chapter 1 (p. 3) identifies morphophonemic alternation as a central failure:
`pang-` surfaces as `pam-`, `pan-`, `panga-` depending on the following sound.
Figure 7 then tests `token starts with prefix` against a flat prefix list. If
only `pang` is listed, `pamangan` and `panyulat` never match.

Worse, Kapampangan assimilation changes the **root** too: `pang- + sulat →
panyulat`, where `s` becomes `y`. So even a correct `pan-` match leaves `yulat`,
which is not in the root list either.

**What it costs you.** The proposal promises to solve exactly this and the
algorithm as written cannot. Every `pang-` family word falls to the fallback,
directly lowering MBF1 and MCF1 — on the *proposed* tokenizer.

**Fix.** Two lookup tables, both already wired in:
- `prefixes.tsv` has an `allomorphs` column (`pang- → pam-|pan-|panga-|pany-`).
  Surface forms are matched; the canonical label `pang` is what MCF1 counts, so
  the variants collapse to one morpheme.
- `variants.tsv` maps assimilated root forms to their canonical root
  (`yulat → sulat`), so the remainder test succeeds.
- Circumfixes are auto-expanded over prefix allomorphs at load time, so
  `(pang, an)` also fires as `pam-…-an`, `pan-…-an`, `panga-…-an`.

Populating these tables is linguistic work, not code — budget time with your
validator for it.

---

## 🟠 T-4 — Reduplication is excluded from scope but present in the data

Scope (p. 12) limits the study to prefixation, infixation, suffixation,
circumfixation and clitics. Kapampangan also uses productive CV/CVC
reduplication for aspect and plurality (`gagawa`, `mamamangan`). Reduplicated
forms are common in running text, so excluding them means the segmenter marks
them unanalysable and MBF1/MCF1 drop **on the proposed tokenizer**.

**Fix.** Handled optionally (`enable_reduplication: true`, rule 7). If you keep
it out of scope, keep it out of the *code* too (`strict_thesis_mode: true`) and
report the share of test tokens that are reduplicated so the limitation is
quantified rather than asserted.

---

## 🟠 T-5 — Boundary protection does not survive to inference

The proposal presents constrained training and dictionary-free runtime as if the
runtime output inherits the morphological guarantee. It does not, fully.
Training forbids merges *learned* across a boundary. At runtime there is no
segmentation, so a merge learned inside one word's morpheme can still apply
across a boundary in a different word that happens to contain the same letters.

**What it costs you.** Nothing fatal — but the MBF1 you measure at runtime will
be lower than the training-time segmentation quality, and if you have described
the guarantee as absolute, that gap looks like a bug rather than an expected
property.

**Fix.** Describe it as *statistical* boundary preservation. Measure and report
both numbers: MBF1 of the rule-based segmenter (the upper bound) and MBF1 of the
runtime tokenizer (what you actually deploy). The gap between them is a genuinely
interesting result about how much morphological knowledge a merge table can hold.

---

## 🟠 T-6 — MCF1 is undefined without two conventions

Equations (5)–(7) count word pairs that "share tokens" and pairs that "share
morphemes" without saying what counts.

- If any shared token counts, then two words sharing the letter `a` are an ST
  pair. ST becomes nearly all pairs and precision collapses for *both*
  tokenizers, making the metric uninformative.
- If any shared morpheme counts, the suffix `-an` alone links thousands of
  unrelated pairs and swamps the root signal the metric is supposed to capture.

**Fix.** Two explicit settings, printed with every result and required in
Chapter 3: ignore tokens shorter than `min_token_len` (default 2), and count
only **root** morphemes for SM (`content_morphemes_only: true`). Results are not
comparable across different settings, so state them.

---

## 🟡 C-1 — NLLB-200 distilled 600M has no Mixture-of-Experts layers

Chapter 1 (p. 7) says the 600M "combines transformer-based encoding and decoding
with language identification and mixture-of-experts layers". MoE belongs to the
54B `NLLB-200 MoE` model. The distilled 600M is dense. Remove the MoE sentence
or attribute it to the correct variant.

## 🟡 C-2 — NLLB has no "Language Identifier"

Figure 2's description says a Language Identifier "detects the source language
and directs the output to the correct target language". NLLB uses explicit
**language tag tokens** supplied by the caller — you tell it, it does not detect.
Reword to "source and target language tags".

## 🟡 C-3 — Character fallback does not guarantee processability

p. 43–44 claims characters are "always present in the vocabulary by
construction". They are present only if they appeared in training. A character
that did not (an emoji, a Spanish-era diacritic, a stray Cyrillic letter in
scraped news) has no entry. **Byte-level fallback** makes the claim literally
true: 256 byte tokens cover every possible input. Implemented; update the
sentence in Chapter 3.

## 🟡 C-4 — The Rust component is unjustified

p. 48–49 introduces a Rust segmentation component "to improve efficiency in
training-stage morphological preprocessing". At 13,000 sentences the Python
segmenter takes seconds and runs once. Unless you measure and report a speed-up,
this is a second source of truth and an extra toolchain (PyO3/maturin, cargo,
MSVC on Windows) for no benefit. Either drop it, or keep it **and** add a parity
test asserting identical output on the full word-type list, plus a timing table.

---

## One more thing: pre-register your interpretation

Decide *now*, in writing, what you will conclude in each outcome — before you see
the numbers. Suggested wording to put in Chapter 3:

> The proposed tokenizer condition will be interpreted as superior at the
> tokenizer level when MBF1 and MCF1 are significantly higher than **both** the
> native NLLB tokenizer and the matched plain-BPE control, with Fertility Rate
> no more than X% higher than the matched control. At the translation level,
> superiority requires a significant improvement over the **re-initialised
> control arm**, since the pretrained-baseline comparison is confounded by
> embedding initialisation.

That paragraph turns three of the issues above from weaknesses into evidence
that you understood your own design.
