# Every piece of data the pipeline needs

Five inputs. Three are required to get any result; two are required to get a
*defensible* result.

| # | What | Required for | Format | Size target | Status |
|---|---|---|---|---|---|
| 1 | Kapampangan–Filipino parallel corpus | everything | TSV | ≥ 13,000 pairs | **you must collect** |
| 2 | Lexicon Dictionary (roots + affixes) | tokenizer training | 8 TSVs | ≥ 3,000 roots | seed provided (165 roots) |
| 3 | Orthography rules | normalisation | TSV | ~5–20 rules | empty, needs validator sign-off |
| 4 | Gold morpheme segmentations | Morpheme Boundary F1 | TSV | ≥ 1,000 word types, 2 annotators | **you must annotate** |
| 5 | NLLB-200 distilled 600M weights | translation arms | HF model | 2.5 GB download | auto-downloads |

---

## 1. Parallel corpus — `data/raw/parallel.tsv`

```tsv
pam	fil	domain	source
Kinan ne ing pamangan.	Kinain niya ang pagkain.	religious	PLOC:Mateo 4:2
Nanu ing lagyu mu?	Ano ang pangalan mo?	conversational	validator:JS-2026-02-11
Meging masalese ing bayung dalan.	Naging maayos ang bagong daan.	news	https://…  (accessed 2026-02-14)
```

**Columns**

- `pam` — Kapampangan source sentence
- `fil` — Filipino reference translation
- `domain` — `religious` | `conversational` | `news` (drives stratified splitting)
- `source` — provenance. **Fill this in.** Web-scraped rows need the URL and the
  access date; validator-produced rows need the validator's identifier. The
  Ethical Considerations section commits you to this.

**Where it comes from, per the proposal**

| source | expected volume | what to check first |
|---|---|---|
| PLOC Kapampangan religious corpus + Filipino parallel | ~13,000 | **Verify it is sentence-aligned, not a word list.** See Issue D-1 — the proposal calls it a "unigram" corpus, which cannot contain sentences. Download and count lines before you rely on this number. |
| Conversational samples from native speakers | 300–800 | informed consent on file; no personal information |
| Kapampangan news, web-scraped | 500–2,000 | robots.txt and terms of use checked; publicly accessible only; no paywalled content |
| Kapampangan Dictionary Embeddings | (lexical, not sentences) | feeds the lexicon, not the parallel corpus |

**Minimum to run the code:** ~500 pairs. **Minimum to say anything:** ~5,000.
**As designed:** 13,000 → 10,400 train / 1,300 val / 1,300 test, which is where
the `n = 1300` in the Statistical Treatment section comes from.

**Cleaning is automatic and audited.** `scripts/00_prepare_data.py` removes
duplicates, empty rows, length outliers, implausible source/target length
ratios, non-text rows, and redacts emails / phone numbers / URLs. Every drop is
counted by reason in `data/processed/split_report.json` — that table answers
"how did 13,000 raw pairs become N usable pairs", which you will be asked.

---

## 2. Lexicon Dictionary — `data/lexicon/*.tsv`

Eight files. A 165-root seed ships in the repo so the pipeline runs today; it is
**not** a research resource and every row is tagged `source=SEED`.

| file | columns | seed rows | target |
|---|---|---|---|
| `roots.tsv` | root, gloss_fil, pos, source | 165 | **3,000+** |
| `prefixes.tsv` | prefix, gloss, allomorphs, source | 26 | 40–60 |
| `infixes.tsv` | infix, gloss, source | 3 | 3–5 |
| `suffixes.tsv` | suffix, gloss, allomorphs, source | 2 | 3–6 |
| `circumfixes.tsv` | prefix, suffix, gloss, source | 8 | 10–20 |
| `clitics.tsv` | clitic, type, gloss, source | 17 | 20–30 |
| `compounds.tsv` | compound, parts, gloss, source | 1 | as found |
| `variants.tsv` | variant, canonical, note, source | 5 | 200+ |

**Root count is the single biggest lever on your results.** The segmenter only
accepts an analysis when the remainder is a known root, so lexicon coverage is a
hard ceiling on Morpheme Boundary F1 and Morphological Consistency F1 for the
*proposed* tokenizer. `scripts/01_validate_lexicon.py` prints the coverage
figure and lists unanalysed word types — work that list until coverage is above
about 70% on your training data.

**The `allomorphs` column is not optional.** Chapter 1 identifies `pang- →
pam-/pan-/panga-` alternation as a core failure of statistical tokenizers. If
you leave that column empty, your own segmenter fails on exactly those words.
See Issue T-3.

**The `variants.tsv` file carries assimilated roots too** — `yulat → sulat`,
because `pang- + sulat → panyulat` changes the root's first sound.

**Provenance.** Replace `SEED` with a real citation (`Del Corro 1980 p.44`) or a
validator identifier and date. The panel will spot-check.

---

## 3. Orthography rules — `data/lexicon/orthography_rules.tsv`

```tsv
# regex	replacement	note
qu(?=[ei])	k	Spanish qu- before e/i
c(?=[aou])	k	Spanish c before a/o/u
```

Ships **commented out on purpose**. Kapampangan has no single official
orthography; the Spanish-derived system (`quing`, `cacu`) and the modern
Filipino-derived one (`king`, `kaku`) both circulate. If your corpus mixes them,
the tokenizer sees unrelated words and both fertility and consistency suffer.
But some mappings are wrong in edge cases, so **a Kapampangan validator approves
each rule before you enable it**, and Chapter 3 lists the enabled rules.

---

## 4. Gold morpheme segmentations — `data/gold/morpheme_gold.tsv`

```tsv
word	segmentation	suggested	rule	count	in_test_only	annotator	provenance	notes
kapampangan	ka|pampang|an	ka|pampang|an	circumfix	42	0	JS	human
kinan	k|in|an	k|in|an	infix	18	0	JS	human
basan	bas|an	basan	fallback	7	1	MR	human	stem-final vowel elided
```

**Rules that the loader enforces:**

- the pieces must concatenate back to the word exactly — write **surface**
  pieces (`bas|an`), not underlying forms (`basa|an`);
- `provenance` must be `human`. Files containing `auto` rows are **rejected**
  unless you pass `--allow-auto-gold`, which exists only for smoke tests.

**Procedure**

1. `python scripts/02_build_gold_template.py --n 1500` → template, sampled in
   frequency bands (15% high / 30% mid / 30% low / 25% hapax) so it is not all
   function words, with `in_test_only` flagging types unseen in training.
2. **Two annotators** edit independently. Do not let them see each other's file.
3. Compute Cohen's kappa on boundary agreement and report it in Chapter 3.
   Below κ = 0.8, revise the annotation guideline and redo.
4. Resolve disagreements, set `provenance=human`, save as `morpheme_gold.tsv`.

Why this cannot be skipped or automated: see Issue M-2. Grading the tokenizer
against boundaries produced by its own training signal is circular and the
result would not survive a defence.

---

## 5. NLLB-200 distilled 600M

Downloads automatically on first use to `~/.cache/huggingface/`:

```bash
python -c "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer; \
  AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M'); \
  AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M')"
```

~2.5 GB. Do it once on good internet; after that everything runs offline
(`HF_HUB_OFFLINE=1`).

Note the target language code is **`tgl_Latn`** (Tagalog) — NLLB has no separate
"Filipino" code, and it has no Kapampangan code at all. See Issue N-2.

---

## Hardware

The proposal names an ASUS TUF Gaming A15 (Ryzen 7, RTX 4050 6 GB) plus Google
Colab. That works:

| stage | needs | time (13k pairs) |
|---|---|---|
| data prep, lexicon validation | CPU | seconds |
| tokenizer training + vocab search | CPU | 1–5 minutes |
| tokenizer evaluation | CPU (numpy) | 1–3 minutes |
| NMT fine-tuning, one arm | GPU 6 GB | ~45–90 minutes |
| decoding 1,300 sentences, beam 5 | GPU | 10–20 minutes |

All three NMT arms: roughly 4–6 hours total. If 6 GB is tight, set
`train.batch_size: 4` and `train.grad_accum: 8` — same effective batch, so the
arms stay comparable. Colab T4/L4 works with the same config.

---

## Folder layout when you are done

```
data/
  raw/parallel.tsv                    (1) you collect
  lexicon/*.tsv                       (2) you build + validate
  lexicon/orthography_rules.tsv       (3) validator approves
  gold/morpheme_gold.tsv              (4) two annotators
  processed/train.tsv  val.tsv  test.tsv    generated by stage 00
  processed/split_report.json               cleaning + stratum audit
```
