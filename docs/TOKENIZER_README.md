# The Kapampangan Tokenizer — plain-language guide

This explains the **first half** of the system: everything that turns raw
Kapampangan text into numbers. If you only read one document before touching
the code, read this one.

---

## 1. The problem in one paragraph

A translation model never sees letters. It sees **token IDs** — integers that
index a lookup table. The thing that decides "which pieces does this word break
into" is the **tokenizer**, and it is chosen *before* the model ever trains.
Kapampangan builds words by gluing pieces (morphemes) onto a root:

```
kan          "eat"              root
k-in-an      "ate"              root + infix -in-
k-um-an      "eats / will eat"  root + infix -um-
sulat-an     "write on"         root + suffix -an
ka-pampang-an  "Kapampangan"    prefix ka- + root pampang + suffix -an
```

A normal tokenizer does not know this. It only knows which letter sequences are
frequent. So it might cut `kinan` as `kin | an` — which mixes half the root with
half the infix and means nothing. The model then has to *reconstruct* the idea
"this is the past tense of eat" from garbage pieces, using only ~13,000 example
sentences. That is the failure this project attacks.

**Our fix:** teach the tokenizer where the morpheme joints are *while it is
learning its vocabulary*, so it never learns a piece that straddles a joint.

---

## 2. The five stages

```
raw text
   |
   v
[1] Normalizer          spelling + Unicode clean-up          normalize.py
   |
   v
[2] Pre-Tokenizer       split into words, mark word starts   pretokenize.py
   |
   v
[3] Morphological       cut each word into morphemes,        segmenter.py
    Segmenter           guided by the Lexicon Dictionary     lexicon.py
   |
   v
[4] Morph-BPE           learn frequent pieces, but NEVER     morph_bpe.py
                        merge across a morpheme joint
   |
   v
[5] Runtime tokenizer   vocabulary + merge rules only,       tokenizer.py
                        no lexicon, byte fallback
```

Stages 1–4 run **once**, during training. Stage 5 is what the translation model
actually uses. This split matters: the lexicon is a crutch used to build a
better vocabulary, then thrown away.

---

### Stage 1 — Normalizer (`normalize.py`)

Makes text consistent so `Ing`, `ing`, and `ING` are one thing.

- Unicode NFC (so `ñ` is one character, not `n` + a combining tilde)
- straight quotes, normal hyphens, no invisible characters
- lowercase (recommended — casing would triple your word types on a small corpus)
- **optional orthography rules** from `data/lexicon/orthography_rules.tsv`

That last one is important. Kapampangan is written two ways: the Spanish-based
system (`quing`, `cacu`, `ualu`) and the modern one (`king`, `kaku`, `walu`).
If half your corpus uses one and half the other, the tokenizer sees two
unrelated words. **The rules file ships empty on purpose** — a Kapampangan
validator must approve each rule before you switch it on, because some of these
mappings change meaning in edge cases.

### Stage 2 — Pre-Tokenizer (`pretokenize.py`)

Splits on whitespace and punctuation, and glues a marker `▁` onto the front of
every word that starts after a space:

```
"kinan ne ing pamangan."  ->  ▁kinan  ▁ne  ▁ing  ▁pamangan  .
```

The marker means detokenising is exact: join the pieces, turn `▁` back into a
space. It also means a merge can never accidentally join two words.

Note: `words_only()` defines **W** for the Fertility Rate formula as the count
of *alphabetic* words — punctuation and numbers are excluded. Write that
definition into Chapter 3; without it "tokens per word" is ambiguous.

### Stage 3 — Morphological Segmenter (`segmenter.py`)

This is the linguistic brain. For each word it tries rules **in the exact order
of Figure 7** in the proposal:

| order | rule | example |
|---|---|---|
| 1 | is it a known compound? | `matuang-lalaki` |
| 2 | is it a bare root? | `kan` |
| 3 | circumfix (both ends) | `ka-pampang-an` |
| 4 | prefix | `ma-santing` |
| 5 | infix (inside the root) | `k-um-an` |
| 6 | suffix | `sulat-an` |
| 7 | reduplication *(added)* | `ga~gawa` |
| 8 | clitic | `bale-mi` |
| 9 | give up — return the whole word | `eskwela` |

A rule only fires if what remains is a **real root in the lexicon**. That is the
safety catch: without it, `ma` + anything would look like a valid analysis.

Two modes:

- `strict_thesis_mode: true` — a literal transcription of Figure 7.
- `strict_thesis_mode: false` (**default**) — same order, plus five repairs
  (R1–R5) documented in [THESIS_ISSUES.md](THESIS_ISSUES.md). In short:
  longest affix wins, allomorphs resolve (`pam-`/`pan-`/`panga-` → `pang-`),
  stacked affixes peel recursively, reduplication is handled, and a stem-final
  vowel that got eaten by `-an` is restored (`basa` + `-an` → `basan`).

Run `python scripts/01_validate_lexicon.py` to see **coverage** — the share of
word types the segmenter can actually analyse. This number is the hard ceiling
on your Morpheme Boundary F1, and it is set by lexicon size, not by cleverness.
With 165 seed roots the coverage on toy data is 95%; on real text with 165 roots
expect 20–30%. **You need ~3,000+ validated roots.**

### Stage 4 — Morph-BPE (`morph_bpe.py`)

Ordinary BPE: count every pair of adjacent symbols in the corpus, merge the most
frequent pair, repeat until the vocabulary is full.

Morph-BPE: the same, except each word is stored as a list of **cells**, one per
morpheme, and pairs are only counted *inside* a cell.

```
kapampangan  ->  [▁k a] [p a m p a n g] [a n]
                  ka       pampang        an
```

The pair `(a, p)` spanning `ka|pampang` is invisible to the counter, so the
merge `ap` can never be created from this word. Words the segmenter could not
analyse become a single cell and behave exactly like plain BPE — that is the
intended graceful degradation, and it is why lexicon coverage matters so much.

**Vocabulary size** is chosen by `vocab_search.py`, not guessed. For each
candidate size it trains a tokenizer, then scores it on the **validation** split
with

```
MorphDist(V) = mean over words of  1 - |predicted ∩ gold| / |predicted ∪ gold|
J(V)         = MorphDist(V) + λ · max(0, Fertility(V) − target)
```

and picks the smallest `V` with the lowest `J`. The first term is "do my cuts
land on real joints"; the second is "am I chopping too finely". The proposal
says "morphological distance scores" without giving a formula — this is the
formula you must write into Chapter 3.

### Stage 5 — Runtime tokenizer (`tokenizer.py`)

After training, the lexicon is gone. Encoding a word is:

1. split into characters (with `▁` fused onto the first one, exactly as in
   training — getting this wrong silently doubles your fertility);
2. any character never seen in training → its UTF-8 **bytes** as `<0x41>` tokens;
3. apply the learned merges greedily, lowest rank first, until none apply.

Byte fallback is why *no input is ever unprocessable*. The proposal claims
character fallback gives this guarantee — it does not, because a character that
never appeared in training has no vocabulary entry. Bytes always do.

Special-token IDs deliberately copy NLLB's layout so `pad_token_id` is `1` on
both sides of the grafted model:

| id | token | purpose |
|---|---|---|
| 0 | `<s>` | begin |
| 1 | `<pad>` | padding — **must match NLLB** |
| 2 | `</s>` | end |
| 3 | `<unk>` | unknown |
| 4 | `__pam_Latn__` | source-language tag (Kapampangan is **not** an official NLLB code) |
| 5 | `▁` | word-start marker |
| 6–261 | `<0x00>`…`<0xFF>` | byte fallback |
| 262+ | learned alphabet and merges | |

---

## 3. What gets measured, and what each number means

| metric | question it answers | direction | file |
|---|---|---|---|
| **Fertility Rate** | How many pieces per word? | lower is more compact | `metrics/fertility.py` |
| **Morpheme Boundary F1** | Do my cuts land on real joints? | higher is better, 1.00 ideal | `metrics/boundary_f1.py` |
| **Morphological Consistency F1** | Do words sharing a root share a token? | higher is better, 1.00 ideal | `metrics/consistency_f1.py` |

Three traps, all of them things a panel will ask about:

**Fertility is not a quality score by itself.** A tokenizer with a bigger
vocabulary always has lower fertility. The proposed tokenizer will beat NLLB's
fertility almost automatically, because NLLB spreads 256k tokens over 200
languages and we spend our whole vocabulary on one. That comparison proves
"we trained on Kapampangan", not "morphology helps". This is why the pipeline
also trains a **plain-BPE control** on the same corpus at the same vocabulary
size (`03_train_tokenizer.py --plain-bpe`). On the toy data, the morphology-aware
tokenizer actually has *higher* fertility than plain BPE (1.56 vs 1.30) and much
better boundary F1 (0.82 vs 0.17) — that trade-off is the real finding, and you
would never see it against NLLB alone.

**Morpheme Boundary F1 needs human gold data.** If the "correct" boundaries come
from the same segmenter that constrained training, you are grading a student
with their own answer key. `load_gold()` therefore refuses any file with
`provenance=auto` unless you pass `--allow-auto-gold` (smoke tests only). The
workflow is: `02_build_gold_template.py` produces a template with suggestions,
**two annotators** review it independently, you report Cohen's kappa on their
boundary agreement, and only then does it become `morpheme_gold.tsv`.

**Morphological Consistency F1 is undefined until you fix two conventions.**
The formula counts word pairs that "share tokens" and pairs that "share
morphemes". If a shared single letter counts, every pair shares tokens and both
tokenizers score near zero. We therefore ignore tokens shorter than
`mcf1_min_token_len` (default 2), and restrict "share morphemes" to **root**
morphemes (`mcf1_content_morphemes_only: true`), because otherwise the suffix
`-an` alone links thousands of unrelated pairs. Both settings are printed with
the result and must appear in Chapter 3 — results are not comparable across
different settings.

---

## 4. Files at a glance

```
src/kapampangan_mt/
  normalize.py      Unicode + orthography normalisation
  pretokenize.py    word splitting, ▁ marker, W for fertility
  lexicon.py        Lexicon Dictionary loader + validation
  segmenter.py      Figure 7 pseudocode + repairs R1-R5
  morph_bpe.py      boundary-constrained BPE trainer
  tokenizer.py      runtime encoder/decoder, byte fallback
  vocab_search.py   vocabulary-size selection
  baselines.py      NLLB tokenizer adapter, matched-BPE control
  metrics/          fertility, boundary F1, consistency F1, BLEU/chrF++
  stats/            paired t-test, Wilcoxon, bootstrap, Holm correction
```

## 5. Quick check that it works

```bash
python scripts/make_toy_data.py --n 600
python scripts/00_prepare_data.py
python scripts/01_validate_lexicon.py
python scripts/03_train_tokenizer.py
python scripts/03_train_tokenizer.py --plain-bpe
python scripts/04_eval_tokenizer.py --allow-auto-gold --no-nllb
python scripts/07_report.py
```

Expected on toy data: `kinan` tokenises as `▁k | in | an`, and plain BPE
tokenises it as one blob `▁kinan`. That contrast is the whole thesis in one line.

## 6. About the Rust component

The proposal says a Rust segmenter will be integrated "to improve efficiency".
For 13,000 sentences (~300k word tokens) the Python segmenter finishes in a few
seconds, and it runs **once** per experiment. The honest position is: keep the
Python implementation as the reference, and only add Rust (via PyO3/maturin) if
you also add a parity test asserting both produce identical segmentations on the
full word-type list. Otherwise you are adding a second source of truth and a
toolchain dependency for no measurable gain — and a panel member may reasonably
ask what the speed-up actually was.
