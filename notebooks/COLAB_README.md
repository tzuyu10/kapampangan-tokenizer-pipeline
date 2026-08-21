# Training the tokenizer on Google Colab

**Notebook:** `notebooks/Train_Kapampangan_MorphBPE.ipynb`

---

## Read this first: you do not need a GPU

**Training this tokenizer takes ~15 seconds on a CPU.** That is not a shortcut —
it is what BPE *is*. BPE counts how often character pairs sit next to each other
and merges the most frequent one, repeatedly. It is counting and sorting. There
is nothing for a GPU to do.

The part of your thesis that needs a GPU is the **NLLB-200 translation
experiment** (Chapter 3, p. 44), which is a separate stage and is currently
blocked for a different reason (no parallel data — see the end of this file).

Colab is still worth using: no Python install, no dependency conflicts, and your
teammates get an identical environment. **Leave the runtime on CPU.** Selecting
a GPU changes nothing and burns your quota.

---

## Exactly which dataset files are used

From the `DATASET` folder you provided:

### Corpus — the text the tokenizer learns merges from

| File | Used for | Notes |
|---|---|---|
| `CLEANED_JSON/Kapampangan_Religious_Text-1_cleaned.json` | corpus | 5,464 Bible verses (Genesis, Deuteronomy, Judges). ~97% survives cleaning. |
| `CLEANED_JSON/Kapampangan_Literary_Text-1_cleaned.json` | corpus | 13,310 lines of poetry/prose. **~12% discarded** — binary leaked in from a bad `.doc` extraction. |

→ **16,981 clean lines / 257,166 word tokens / 25,511 word types**, split
13,584 train / 1,698 validation / 1,699 test.

### Lexicon — what tells the segmenter where morpheme joints are

| File | Used for | Yields |
|---|---|---|
| `CLEANED_JSON/kapampangan_annotated.json` | Lexicon Dictionary | 3,138 headwords with roots + syllables |
| `UNANNOTATED/ilide.info-kapampangandictionaryamongsamson-1-*.pdf` | Lexicon Dictionary | **9,763 entries** (835 pp) — the main source |
| `UNANNOTATED/ilide.info-ka-pampanga-n-*.pdf` | Lexicon Dictionary | 3,056 Kapampangan–English–**Pilipino** entries |
| `UNANNOTATED/Speaking Kapampangan -- ... Mirikitani ... .pdf` | Lexicon Dictionary | 1,322 glossary entries |
| `UNANNOTATED/ilide.info-mga-salita-...dayalekto-*.pdf` | Lexicon Dictionary | 68 entries |

### Deliberately **not** used

| File | Why |
|---|---|
| `CLEANED_JSON/dictionary_entries.json` | Superseded by `kapampangan_annotated.json` — same dictionary, unenriched, plus PDF boilerplate (`download`, `national`, `pines.`). 8% have empty `pos_blocks`. |
| `UNANNOTATED/SL-030-forman-kapampangan-grammar-notes.pdf` | A grammar, not a dictionary — no lexical entries. **You still need it**: it is the authoritative source for the affix gap described at the bottom of this file. |
| `UNANNOTATED/ilide.info-an-introduction-to-the-kapampangan-langu-*.pdf` | Lecture notes. Prose with scattered examples; mining words out of explanations would break the rule that definition words must not become headwords. |
| `UNANNOTATED/ilide.info-paghahambing-ng-wikang-kapampangan-*.pdf` | Comparative paper in Filipino. Cite it for orthography/phonology rules; it has no entries. |

---

## Setup, step by step

### 1. Put the two folders in Google Drive

```
MyDrive/
  kapampangan-morphbpe/     <- this whole project folder
  DATASET/
    CLEANED_JSON/
    UNANNOTATED/
```

Drive is recommended over uploading a ZIP: Colab disconnects after ~90 minutes
idle, and with Drive you just re-mount instead of re-uploading 80 MB of PDFs.

### 2. Open the notebook

Upload `notebooks/Train_Kapampangan_MorphBPE.ipynb` to Colab
(**File → Upload notebook**), or open it from Drive.

### 3. Runtime → Change runtime type → **CPU**

### 4. Edit two paths

In the "Option A: Google Drive" cell:

```python
PROJECT_DIR = '/content/drive/MyDrive/kapampangan-morphbpe'
DATASET_DIR = '/content/drive/MyDrive/DATASET'
```

### 5. Run all cells, top to bottom

**Runtime → Run all.** About **5 minutes** total; the 835-page PDF extraction is
~3 of those and is skipped on later runs.

---

## What each stage does

| Stage | Thesis section | What it does | Time |
|---|---|---|---|
| **A** Corpus | Sources of Data, p. 33 | clean the JSON files, 80/10/10 stratified split | 20 s |
| **B** Lexicon | Lexicon Dictionary, p. 41 | extract PDFs → propose morphology → merge | 3 min |
| **C** Pre-Tokenizing | Figure 6, p. 37 | normalise, split into words, mark `▁` | instant |
| **D** Segmentation | **Figure 7**, p. 38-41 | apply the affix rules in the thesis' exact order | 10 s |
| **E** Morph-BPE | p. 42 | **train** — merges may not cross a morpheme boundary | **15 s** |
| **F** Vocab size | p. 43 | pick `V` by morphological distance on validation | 60 s |
| **G** Runtime | p. 43 | show the finished tokenizer working, no lexicon | instant |
| **H** Evaluation | eq. 1-7 | Fertility, MBF1, MCF1 + paired tests | 90 s |

---

## What you should see

At Stage D, the thesis' own example working:

```
kinan   -> k[root] + in[infix] + an[root]
kuman   -> k[root] + um[infix] + an[root]
```

At Stage H, the trade-off curve — **this is the strongest table you currently
have for Chapter 4**:

| Vocab | Morph-BPE fertility / MBF1 micro | plain BPE fertility / MBF1 micro |
|---|---|---|
| 1,000 | 2.137 / **0.335** | 2.044 / 0.116 |
| 2,000 | 1.874 / **0.294** | 1.776 / 0.102 |
| 4,000 | 1.731 / **0.321** | 1.621 / 0.060 |
| 8,000 | 1.640 / **0.336** | 1.515 / 0.024 |
| 16,000 | 1.601 / **0.352** | 1.463 / **0.010** |

Read the last column. As the vocabulary grows, plain BPE simply memorises whole
frequent words and its boundary score collapses to 0.010. Morph-BPE holds at
~0.35 throughout, for a fertility cost of about 0.14 tokens per word.

That contrast is your contribution, and it is visible at every vocabulary size —
which makes it much harder to dismiss than a single-point comparison.

---

## Outputs

| File | What it is |
|---|---|
| `artifacts/tokenizer/morphbpe.json` | **the trained tokenizer** (vocabulary + merges, self-contained) |
| `artifacts/tokenizer/plainbpe.json` | the matched control tokenizer |
| `artifacts/tokenizer/vocab_search.json` | the vocabulary-size selection table |
| `artifacts/tokenizer/segmentation_train.jsonl` | every training-time analysis (audit trail) |
| `artifacts/results/tokenizer_level.json` | Tables 2 and 4 |
| `artifacts/results/vocab_sweep.json` | the trade-off curve above |
| `artifacts/results/REPORT.md` | Tables 2-5 as Markdown |
| `data/raw/ingest_report.json` | what cleaning dropped, by reason |
| `data/lexicon/MERGE_PROVENANCE.json` | which claims were admitted into the lexicon |

The last cell zips `artifacts/` and downloads it, and optionally copies it back
into Drive so it survives a runtime restart.

---

## Using the tokenizer afterwards

```python
import sys; sys.path.insert(0, 'src')
from kapampangan_mt.tokenizer import KapampanganTokenizer

tok = KapampanganTokenizer.load('artifacts/tokenizer/morphbpe.json')

tok.tokenize("Kinan ne ing pamangan.")   # ['▁k', 'inan', '▁ne', '▁ing', '▁pamangan', '.']
ids = tok.encode("Kinan ne ing pamangan.")
tok.decode(ids)
tok.vocab_size
```

The JSON is self-contained — no lexicon needed at runtime, which is exactly what
the thesis specifies on p. 42.

---

## Problems in the thesis this notebook surfaces

Full list with explanations: `docs/THESIS_ISSUES.md` (20 issues). The four that
matter most for the tokenizer half:

### 1. Fertility Rate vs NLLB is a rigged comparison (Issue M-3)

RQ3.1 asks whether your tokenizer beats NLLB's on fertility. It will —
automatically. NLLB spreads 256,000 tokens over 200 languages, none of them
Kapampangan. **Plain BPE with zero morphological awareness wins that comparison
too.** So RQ3.1 as written tests "did we train on Kapampangan", not "does
morphology help".

The notebook therefore trains a **matched control**: plain BPE, same corpus,
same vocabulary size. That is the comparison that isolates your contribution.
Report all three columns in Table 2.

### 2. Morpheme Boundary F1 has no gold standard (Issue M-2)

Chapter 3 says MBF1 compares against "the validated morpheme boundaries" but
never says where those come from. The obvious shortcut — generate them with your
own segmenter — is **circular**: you would be grading a student with their own
answer key, and the NLLB baseline would be measured against a standard it was
never given.

The notebook runs with `--allow-auto-gold`, so **those numbers are directional
only**. For Chapter 4 you need ~1,000 word types annotated by **two** people
independently with Cohen's kappa reported. `scripts/02_build_gold_template.py`
produces the form pre-filled with suggestions.

### 3. Boundary protection does not fully survive to inference (Issue T-5)

You will see `kinan` tokenised as `▁k | inan` rather than `▁k | in | an`.

Training forbids merges *learned* across a boundary. At runtime there is no
segmentation, so a merge learned inside one word's morpheme can still apply
across a boundary in a different word with the same letters. Describe it as
**statistical** boundary preservation, and report both numbers: segmenter MBF1
(the upper bound) and runtime MBF1 (what you deploy). The gap is a genuinely
interesting result.

### 4. A specific gap in the affix inventory — fix this next

The affix inventory is derived from the paradigms Samson prints inside its own
entries, which are **verb-focused**. Measured:

| Affix | Explicit observations in Samson | Licensed? |
|---|---|---|
| `ma-` | 8 | no (floor is 20) |
| `pa-` | 3 | no |
| `ka-…-an` | 3 | no (floor is 5) |
| `pang-` | 0 | no |

So `masanting` and `kapampangan` come back **unsegmented**. The dictionary's own
evidence does not license `ma-` or `ka-…-an`, and inventing them would break the
rule that nothing is asserted without support.

**This is a task for your validator, not a bug to code around.** Take the affix
inventory from `SL-030-forman-kapampangan-grammar-notes.pdf` — Forman's grammar,
already in your `UNANNOTATED/` folder, left unextracted for exactly this reason.
Adding `ma-`, `ka-…-an`, `pang-` and its allomorphs (`pam-`, `pan-`, `panga-`)
will move every number in Table 2.

---

## What is blocked, and why it is not a compute problem

**Research Questions 2 and 4 cannot run.** BLEU, chrF++, the whole
Kapampangan→Filipino half.

**There is no parallel data in your dataset.** Every file is monolingual
Kapampangan. The dictionary glosses are **English**, not Filipino. A scan of all
16,981 corpus lines found 4 that look Filipino-dominant.

The way out is already in your data. Your religious file carries explicit
`Book Chapter:Verse` references for **2,859 verses**. Filipino Bibles (*Ang
Dating Biblia* 1905, *Magandang Balita Biblia*) use the same versification. Join
on `(book, chapter, verse)` and you get ~2,800 sentence pairs **mechanically** —
no manual translation. Days of work, not months.

Once that file exists, `scripts/05_train_nmt.py` and `06_translate_eval.py` run,
and *those* do need a GPU. Colab's T4 handles it: ~45-90 minutes per arm, three
arms.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: kapampangan_mt` | setup cell not run, or run out of order | re-run the "Point Python at the project" cell |
| `project found: False` | wrong Drive path | check the exact folder name in the Drive file browser on the left |
| `data/raw/mono_pam.tsv not found` | Stage A skipped or failed | re-run Stage A; check `DATASET_DIR` points at the folder *containing* `CLEANED_JSON` |
| PDF extraction very slow | 835 pages, expected | ~3 minutes; skipped automatically on later runs |
| Runtime disconnected mid-run | Colab idle timeout | re-mount Drive and re-run; completed stages are skipped |
| `ValueError: rows tagged provenance=auto` | using machine-generated gold | expected until you have human annotation — that is what `--allow-auto-gold` is for |
| Coverage much lower than 84% | lexicon merge not run | run the Stage B merge cell |
