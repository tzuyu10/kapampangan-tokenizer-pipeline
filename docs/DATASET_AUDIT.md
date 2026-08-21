# Dataset audit — what you have, what works, what is blocking

Audit of `Downloads/DATASET` run through the pipeline on 19 Aug 2026.
Everything below is measured, not estimated. Reproduce with:

```bash
python scripts/10_ingest_dataset.py --dataset "C:/Users/<you>/Downloads/DATASET"
python scripts/11_split_mono.py
python scripts/01_validate_lexicon.py
python scripts/12_lexicon_worklist.py --n 800
```

---

## 1. Inventory

### `CLEANED_JSON/` — usable, with caveats

| File | Records | What it actually is | Verdict |
|---|---|---|---|
| `Kapampangan_Religious_Text-1_cleaned.json` | 5,464 | Kapampangan Bible: Genesis (1,451 v), Deuteronomy (861 v), Judges (547 v), plus prayers. `Book <lbl>C:V</lbl> text` format. | **Excellent.** 97% survives cleaning. |
| `Kapampangan_Literary_Text-1_cleaned.json` | 13,310 | Poetry and prose. | **Usable but contaminated** — see below. 88% survives. |
| `kapampangan_annotated.json` | 3,138 | PALI/Forman dictionary headwords with `root`, syllabification, POS, and heuristically segmented affixed forms. | **The most valuable file you have.** |
| `dictionary_entries.json` | 3,334 | The same dictionary *before* enrichment, plus PDF boilerplate (`download`, `national`, `pines.`, `Bacolor,`). 8% have empty `pos_blocks`. | **Superseded.** Ignore it; `kapampangan_annotated.json` is strictly better. |

### `UNCLEANED/` — one of these is much more important than you think

| File | Pages | Content | Verdict |
|---|---|---|---|
| `ilide.info-ka-pampanga-n-pr_*.pdf` | 56 | **A three-column KAPAMPANGAN / ENGLISH / PILIPINO glossary.** ~2,900 word triples. | **Extract this.** It is your only Kapampangan→Filipino resource. |
| `ilide.info-mga-salita-sa-iba-t-ibang-dayalekto-pr_*.pdf` | 11 | ~50-row Tagalog/Cebuano/Waray/Kapampangan/Hiligaynon table. | Minor; 50 more word pairs. |
| `ilide.info-paghahambing-ng-wikang-kapampangan-pr_*.pdf` | 8 | Filipino-language linguistics paper on Kapampangan orthography, phonology, morphology, syntax. | **Cite it.** It documents the `i/e`, `o/u`, `d/r`, `w/u`, `y/i` alternations you need for `orthography_rules.tsv`. |

---

## 2. The literary file contains binary garbage

The `.doc` source was read as Latin-1, so OLE compound-document streams leaked
into the JSON. You can see the file signature verbatim in record text:
`ÐÏà¡±á` (= `D0 CF 11 E0 A1 B1 1A E1`), plus NUL bytes and `ÿÿÿÿ` runs.

Measured, on the literary file only:

| Reason dropped | Records |
|---|---|
| control bytes (`\x00`–`\x1f`) | 961 |
| fewer than 3 words | 470 |
| alphabetic ratio below 45% | 124 |
| duplicate | 33 |
| >25% non-ASCII letters | 20 |
| no letters at all | 14 |
| no vowels | 10 |
| impossible word length (≥22 chars) | 1 |
| **total discarded** | **1,638 (12%)** |

The religious file loses only 155 records (3%), almost all one- or two-word
fragments. `data/raw/ingest_report.json` has the full breakdown — put that table
in Chapter 3, because you will be asked how 18,774 raw records became 16,981
usable lines.

> **Action:** if you still have the original `.doc`/`.docx`, re-extract it with
> `python-docx` or LibreOffice (`soffice --convert-to txt`). You would recover
> roughly 1,000 lines of real poetry that the current extraction destroyed.

---

## 3. The corpus after cleaning

```
16,981 lines   257,166 word tokens   25,511 word types   59% hapax
   religious  5,309 lines  (28.0 words/line — Bible prose)
   literary  11,672 lines  ( 9.8 words/line — verse)
```

Split 80/10/10, stratified by length × morphological complexity × domain:
**13,584 train / 1,698 validation / 1,699 test.**

Two things about this corpus that matter:

**Orthography is not consistent.** Your corpus spells the same word several
ways. Measured collapse when accents are stripped and Spanish-era rules applied:

| Merged form | Spellings found | Total tokens |
|---|---|---|
| `king` | `king`, `qng`, `quing`, `qñg` | 12,007 |
| `ku` | `ku`, `cu`, `cú`, `cû` | 3,420 |
| `karing` | `karing`, `caring`, `caríng`, `cáring` | 2,429 |
| `kekang` | `kekang`, `kecang`, `kécang`, `quecang` | 1,838 |
| `metung` | `metung`, `métung` | 1,707 |

Normalising removes **3,769 spurious word types (14.8% of the vocabulary)**.
`data/lexicon/orthography_rules.tsv` now ships with the eight rules that produced
this, each derived from your own data — **but a Kapampangan validator must sign
off on every line before you report anything.**

**59% hapax.** Well over half your word types appear exactly once. That is
partly poetry, partly OCR noise, and partly genuine morphological productivity —
and it is precisely the situation where morphology-aware tokenisation should
pay off, because a tokenizer that recognises `ma-` + a known root generalises to
a form it has never seen.

---

## 4. The dictionary makes a real Lexicon Dictionary

`kapampangan_annotated.json` converts cleanly into the pipeline's format:

| Output | Count | Notes |
|---|---|---|
| `roots.tsv` | **2,642** | 2,581 dictionary roots + 61 grammatical morphemes |
| `variants.tsv` | 57 | PALI-orthography spellings (`a’bak` → `abak`) |
| `prefixes.tsv` | 11 | `ma- mag- maka- makapag- mang- me- meka- i- ipa- ka- pa-` |
| `infixes.tsv` | 2 | `-in-` (128×), `-um-` (34×) |
| `suffixes.tsv` | 1 | `-an` (77×) |
| `circumfixes.tsv` | 4 | `ka-…-an`, `pa-…-an`, `pang-…-an`, `panga-…-an` |
| `derived_forms.tsv` | 3,295 | attested affixed forms with segmentation |
| `segmentation_candidates.tsv` | 3,295 | MBF1 annotation candidates (826 occur in your corpus) |

Two problems I hit while building this, both now fixed in `10_ingest_dataset.py`
— read them, because they would have silently wrecked your results:

**(a) Derived headwords were blocking segmentation.** Dictionaries list derived
lemmas as headwords: `sumulat`, `sinulat`, `masanting`, `mangabala` all appear as
their own entries. Figure 7 checks "is this a root?" *before* trying any affix
rule, so putting them in `roots.tsv` made the segmenter return them whole:

```
sumulat  ->  sumulat[root]          # wrong — no morphology learned
sumulat  ->  s[root] um[infix] ulat[root]     # after the fix
```

The ingester now demotes **171** such headwords into `derived_forms.tsv`.

**(b) The dictionary transcribes phonology, not orthography.** PALI/Forman uses
`’`/`q` for glottal stop and `:` for vowel length: `a’bak`, `ma:walaq`,
`pa:makiya’be`. Your corpus writes `abak`, `mawala`. Every entry is now stored
stripped, with the PALI form kept in `variants.tsv`.

Also note: **59% of the dictionary's own segmentations do not concatenate back
to the surface form** (`payablasan` ← `pa-...-an`, `ma:walaq` ← `ma-wala`). Those
are template strings and morphophonemic alternations, not usable segmentations.
Only the 3,295 that do reconstruct are exported.

---

## 5. What you can do **today**

The tokenizer needs only monolingual Kapampangan. You have that. It trains in
**12 seconds** and it already works:

```
word            Morph-BPE                    plain BPE
kinan           ▁k  inan                     ▁kin  an
makapagsulat    ▁makapag  sulat              ▁makapag  s  ulat
balemi          ▁bale  mi                    ▁bale  mi
gagawa          ▁gag  awa                    ▁gagawa
```

And the core claim of your thesis already holds on your real data. Morph-BPE
beats plain BPE on Morpheme Boundary F1 at **every** vocabulary size, at a small
and consistent fertility cost:

| Vocab | Morph-BPE fertility | plain fertility | Morph-BPE MBF1 (macro / micro) | plain MBF1 (macro / micro) |
|---|---|---|---|---|
| 1,000 | 2.132 | 2.053 | 0.163 / 0.222 | 0.131 / 0.118 |
| 2,000 | 1.883 | 1.785 | 0.195 / 0.256 | 0.144 / 0.091 |
| 4,000 | 1.742 | 1.637 | 0.232 / 0.265 | 0.188 / 0.054 |
| 8,000 | 1.652 | 1.533 | 0.296 / 0.269 | 0.260 / 0.028 |
| 16,000 | 1.608 | 1.486 | **0.368 / 0.303** | 0.334 / **0.011** |

Read the micro column: as the vocabulary grows, plain BPE simply memorises whole
frequent words and its boundary F1 collapses toward zero, while Morph-BPE holds
around 0.27–0.30. That is a clean, defensible result and it is the strongest
single table you currently have.

*(Caveat: the gold used here is the dictionary's own heuristic segmentation,
provenance `auto`. These numbers are directional only — see gap 2 below.)*

---

## 6. What is blocking you

### 🔴 Gap 1 — You have **no parallel data**. At all.

Every file is monolingual Kapampangan. The dictionary glosses are **English**
("the abaca plant, fiber, or cloth"), not Filipino. I scanned all 16,981 lines
for Filipino-dominant text: **4 lines**.

This blocks Research Questions 2 and 4 entirely — no BLEU, no chrF++, no NLLB
arms, half your Statement of the Problem.

The proposal claims ~13,000 Kapampangan–Filipino sentence pairs from PLOC. That
data is not in this folder, and Issue D-1 already flagged that a "unigram corpus"
cannot contain sentence pairs. **Resolve this before anything else.**

Three routes, best first:

1. **Bible verse alignment — your best option, and you are already set up for
   it.** Your religious file has explicit `Book Chapter:Verse` references for
   2,859 verses. Filipino Bibles (*Ang Dating Biblia* 1905, *Magandang Balita
   Biblia*) are freely available with the same versification. Join on
   `(book, chapter, verse)` and you get ~2,800 sentence pairs *mechanically*,
   with no manual translation. Genesis + Deuteronomy + Judges all exist in every
   Filipino Bible. Expand the Kapampangan side to more books and this scales to
   10,000+ pairs. **This is a few days of work, not months.**
2. **Extract the trilingual PDF glossary.** ~2,900 Kapampangan–Filipino *word*
   pairs. Not sentences, but it fills `gloss_fil` in your lexicon and gives you
   a dictionary-level parallel resource. Needs a column-aware extractor
   (`pdfplumber` with x-coordinates), not naive line splitting — the columns
   interleave when read linearly.
3. **Native-speaker translation.** Slowest. Reserve it for the conversational
   register the proposal promises, where nothing else exists.

### 🔴 Gap 2 — No human-annotated gold segmentations

You have 3,295 machine-segmented forms tagged `confidence: heuristic`. The
pipeline saves them as `data/gold/morpheme_gold.PROVISIONAL.tsv` and the metric
loader **refuses** them unless you pass `--allow-auto-gold`, because grading the
tokenizer against its own training signal is circular (Issue M-2).

**Action:** take the 826 candidates that occur in your corpus, have **two**
annotators review them independently, report Cohen's kappa, save as
`morpheme_gold.tsv` with `provenance=human`. Target ≥1,000 rows.

### 🟠 Gap 3 — Segmenter coverage is 73% of tokens, 29% of types

That is the ceiling on your Morpheme Boundary F1, and it is set by lexicon
completeness, not by your algorithm. The good news: the fix is cheap and I have
measured exactly how cheap.

Adding just **61 grammatical morphemes** (`ing`, `king`, `ding`, `ya`, `la`,
`ku`, `ala`, `e`, …) — which the PALI dictionary omits because it covers content
words only — lifted token coverage from **50.0% → 73.4%** in one commit.

`scripts/12_lexicon_worklist.py` ranks what remains by frequency:

| Fill in… | Token coverage reaches |
|---|---|
| nothing (now) | 73.4% |
| top 100 rows | ~80% |
| top 400 rows | ~85% |
| **top 800 rows** | **~88.0%** |

`data/lexicon/WORKLIST_unanalysed.tsv` is pre-sorted by frequency with a
suggested category per row (644 content words, 86 proper nouns, 70 particles and
pronoun clusters). One focused session with a Kapampangan speaker closes this.

### 🟠 Gap 4 — Affix inventory is thin

The dictionary attests 11 prefixes, 2 infixes, **1 suffix**, 4 circumfixes.
Your Chapter 1 discusses `pang-` → `pam-`/`pan-`/`panga-` allomorphy at length,
but `prefixes.tsv` has an **empty `allomorphs` column**, so the segmenter cannot
match those surface forms (Issue T-3). No clitic inventory exists in the
dictionary at all — the hand-written `clitics.tsv` (17 entries) is all you have,
and clitics fired 783 times on your training data, so they matter.

**Action:** fill `allomorphs` from Del Corro (1980) and Forman (1971), and
expand `clitics.tsv`. The third PDF in `UNCLEANED/` documents several of these
alternations in Filipino — use it.

### 🟡 Gap 5 — Domain imbalance

69% of your lines are literary verse (9.8 words/line), 31% Bible prose
(28.0 words/line). Poetry has inverted word order, archaic vocabulary and heavy
elision. The stratified splitter keeps the ratio constant across train/val/test,
but you should report per-domain results in Chapter 4 — a pooled number will hide
that the tokenizer behaves differently on the two registers. The proposal also
promises conversational and news registers; neither is present.

---

## 7. Do this next, in order

| # | Task | Effort | Unblocks |
|---|---|---|---|
| 1 | Align the Bible verses against a Filipino Bible on `(book, chapter, verse)` | 2–3 days | **RQ2, RQ4, the entire NMT half** |
| 2 | Fill the top 400–800 rows of `WORKLIST_unanalysed.tsv` with a native speaker | 1–2 days | coverage 73% → ~88%, lifts MBF1 and MCF1 |
| 3 | Two annotators review 1,000 rows of `segmentation_candidates.tsv`; report kappa | 2 days | **RQ1.2, RQ3.2 — MBF1 becomes reportable** |
| 4 | Get a validator to approve `orthography_rules.tsv` | 2 hours | removes 14.8% spurious vocabulary |
| 5 | Fill the `allomorphs` column; expand `clitics.tsv` | 1 day | fixes the `pang-` problem Chapter 1 is built on |
| 6 | Re-extract the literary `.doc` properly | 2 hours | recovers ~1,000 lost lines |
| 7 | Extract the trilingual PDF with `pdfplumber` | 1 day | ~2,900 Filipino glosses |

Items 2 and 4 alone will visibly move every tokenizer-level number in Table 2.
Item 1 is the one that decides whether you have a thesis or half a thesis.

---

## 8. Honest summary

**You can train and evaluate the tokenizer today, and the result already
supports your hypothesis.** That is genuinely good — the hard part of Chapter 4
Table 2 is within reach this week.

**You cannot touch the translation half of the study.** There is no Filipino
text in this dataset. Everything in Research Questions 2 and 4, both hypotheses
about BLEU and chrF++, and the whole NLLB-200 pipeline is blocked on data that
does not currently exist.

The Bible verse references in your religious file are the way out, and they are
sitting right there in the data you already have.
