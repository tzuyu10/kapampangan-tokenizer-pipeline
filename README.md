# Morphologically-Aware BPE Tokenizer for Kapampangan → Filipino NMT

Reference implementation of the thesis proposal *"Morphologically-Aware
Byte-Pair Encoding Tokenizer for the Kapampangan Language"* (Cansino,
Faeldonia, Lucero, Magtanong, Mital — PUP CCIS, 2026).

> **This is the second, independent implementation.** The other one lives on
> `feat/kapampangan-morphbpe`. The two branches share no history on purpose —
> they are meant to be compared, not merged. Different package name
> (`kapampangan_mt` vs `kapampangan_morphbpe`), different scripts, different
> layout. **Close VS Code before switching branches** or you will get confusing
> import errors from a stale interpreter path.

---

# START HERE

## Just cloned this branch? Test the tokenizer in 10 seconds

**No installs. No virtualenv. No GPU.** The trained tokenizer is committed, and
loading it needs only the Python standard library.

```powershell
python try_tokenizer.py
```

Expect `ALL CHECKS PASSED`. Then:

```powershell
python try_tokenizer.py --interactive    # type your own sentences
python try_tokenizer.py --compare        # Morph-BPE vs the plain-BPE control
python segment_word.py kuman             # k | um | an
python segment_word.py                   # interactive morpheme splitter
```

If `python` is not recognised, use `py` instead.

## Want to retrain it?

You need the dataset, which is **not in this repo** — it contains copyrighted
dictionary text. Ask the team for the `DATASET` folder, then:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/10_ingest_dataset.py --dataset "PATH\TO\DATASET"
python scripts/11_split_mono.py
python scripts/20_extract_dictionaries.py --pdf-dir "PATH\TO\DATASET\UNANNOTATED"
python scripts/22_build_candidate_lexicon.py
python scripts/24_merge_candidate_lexicon.py
python scripts/03_train_tokenizer.py
python scripts/03_train_tokenizer.py --plain-bpe
python scripts/04_eval_tokenizer.py --no-nllb --allow-auto-gold
python scripts/07_report.py
```

About 5 minutes total; the 835-page PDF pass is 3 of those.

**Or run it on Google Colab** — no local Python needed at all:
`notebooks/Train_Kapampangan_MorphBPE.ipynb`. See
[notebooks/COLAB_README.md](notebooks/COLAB_README.md).

## Current state

| | |
|---|---|
| tokenizer | 12,464 tokens, 12,091 merges, boundary-constrained |
| corpus | 16,981 lines / 257,166 tokens, split 13,584 / 1,698 / 1,699 |
| lexicon | 11,496 roots — **unvalidated**, machine-derived |
| segmenter coverage | 84.4% of tokens, 40.3% of types |
| translation half | **blocked** — no Filipino parallel data exists yet |

Evaluation numbers currently use `--allow-auto-gold`, so **they are directional
only**. Human-annotated gold is outstanding. See
[docs/DATASET_AUDIT.md](docs/DATASET_AUDIT.md).

---

## Read these, in this order

| Document | What it covers |
|---|---|
| **[notebooks/COLAB_README.md](notebooks/COLAB_README.md)** | **Train the tokenizer on Google Colab** — no GPU needed, exact dataset files used, 5 minutes |
| **[docs/EXTRACTION_README.md](docs/EXTRACTION_README.md)** | Dictionary extraction: 15,116 entries from the source PDFs, and how to verify them |
| **[docs/CANDIDATE_LEXICON_README.md](docs/CANDIDATE_LEXICON_README.md)** | The AI-assisted candidate morphological lexicon: 14,209 entries, how each analysis is licensed, what a validator does first |
| **[docs/DATASET_AUDIT.md](docs/DATASET_AUDIT.md)** | Audit of the real `DATASET/` folder: what is usable, what is broken, what is blocking |
| **[docs/TOKENIZER_README.md](docs/TOKENIZER_README.md)** | How the tokenizer works, stage by stage, in plain language |
| **[docs/MT_PIPELINE_README.md](docs/MT_PIPELINE_README.md)** | How the tokenizer is grafted into NLLB-200 and how translation is scored |
| **[docs/DATA_REQUIREMENTS.md](docs/DATA_REQUIREMENTS.md)** | Every input the pipeline needs, with formats and target sizes |
| **[docs/VSCODE_SETUP.md](docs/VSCODE_SETUP.md)** | Step-by-step setup and run guide, complete dependency list |
| **[docs/GIT_SETUP.md](docs/GIT_SETUP.md)** | Branch layout, what is committed and why, the two traps that will bite you |
| **[docs/THESIS_ISSUES.md](docs/THESIS_ISSUES.md)** | 20 problems in the proposal, why each is a problem, and the fix |

---

## The pipeline

```
                        ┌───────────────────────── TOKENIZER (training-time) ─────────────────────────┐
raw Kapampangan  ──►  normalise ──► pre-tokenise ──► morphological ──► Morph-BPE ──► tokenizer model
      corpus                                          segmentation      (boundary-        (vocab +
                                                            ▲           constrained)       merges)
                                                            │                                 │
                                                   Lexicon Dictionary                         │
                                                   (roots, affixes,                           │
                                                    clitics, variants)                        │
                                                   discarded after training                   │
                                                                                              ▼
                        ┌───────────────────────── TRANSLATION (NLLB-200 600M) ──────────────────────┐
                        │  source ids ──► grafted encoder embedding ──► encoder ──► decoder ──►      │
                        │                 (only trainable component)              output + softmax   │
                        └────────────────────────────────────────────────────────────────────────────┘
                                                                                              │
                                                                                              ▼
                                                                                    Filipino translation
                                                                                              │
                    Fertility · Morpheme Boundary F1 · Morphological Consistency F1  ◄────────┤
                                                        BLEU · chrF++  ◄─────────────────────┘
                              paired t-test / Wilcoxon / paired bootstrap / Holm–Bonferroni
```

Three tokenizers are compared, not two:

| | trained on Kapampangan | morphology-aware | role |
|---|---|---|---|
| **proposed** Morph-BPE | yes | yes | the contribution |
| **plain** BPE, matched vocab | yes | no | the scientific control (missing from the proposal — Issue M-3) |
| **native** NLLB SentencePiece | no | no | the practical baseline |

Three NMT arms, not two: `baseline`, `adapted`, and `control` — the third
separates "the tokenizer changed" from "the embedding table was re-initialised"
(Issue M-1).

---

## Train on Google Colab (no GPU needed)

Open `notebooks/Train_Kapampangan_MorphBPE.ipynb` in Colab, point it at your
Drive folders, Run All. ~5 minutes. See `notebooks/COLAB_README.md`.

## Working with the real DATASET folder (local)

```bash
python scripts/10_ingest_dataset.py --dataset "C:/Users/<you>/Downloads/DATASET"
python scripts/11_split_mono.py          # 13,584 / 1,698 / 1,699
python scripts/01_validate_lexicon.py    # segmenter coverage
python scripts/20_extract_dictionaries.py --pdf-dir "C:/.../DATASET/UNANNOTATED"
python scripts/22_build_candidate_lexicon.py
python scripts/24_merge_candidate_lexicon.py    # coverage 73% -> 84%
python scripts/12_lexicon_worklist.py --n 800   # prioritised annotation worklist
python scripts/03_train_tokenizer.py     # ~12 seconds
python scripts/03_train_tokenizer.py --plain-bpe
python scripts/04_eval_tokenizer.py --no-nllb   # add --allow-auto-gold until gold is human-annotated
```

Stages 05/06 (translation) stay blocked until Filipino references exist — see
the audit.

## Quick start (60 seconds, synthetic data)

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .\.venv\Scripts\Activate.ps1
pip install torch --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements-dev.txt
export PYTHONPATH=src                                  # Windows: $env:PYTHONPATH="src"

python -m pytest tests -q                              # 27 passed

python scripts/make_toy_data.py --n 600
python scripts/00_prepare_data.py
python scripts/01_validate_lexicon.py
python scripts/02_build_gold_template.py --n 200
cp data/gold/morpheme_gold.TEMPLATE.tsv data/gold/morpheme_gold.tsv
python scripts/03_train_tokenizer.py
python scripts/03_train_tokenizer.py --plain-bpe
python scripts/04_eval_tokenizer.py --allow-auto-gold --no-nllb
python scripts/07_report.py
```

Expected: `kinan` tokenises as `▁k | in | an` (root + infix + root) under
Morph-BPE, and as a single blob `▁kinan` under plain BPE.

The toy corpus is **synthetic**. Delete it before doing real work.

---

## Full run

```bash
# stages 00-04 as above, with real data and human-annotated gold
python scripts/05_train_nmt.py --arm baseline
python scripts/05_train_nmt.py --arm adapted
python scripts/05_train_nmt.py --arm control
python scripts/06_translate_eval.py --arms baseline adapted control
python scripts/07_report.py            # -> artifacts/results/REPORT.md (Tables 2-5)
```

---

## Layout

```
config/pipeline.yaml        every knob; override with --set key=value
data/
  raw/                      cleaned monolingual corpus (gitignored)
  lexicon/                  Lexicon Dictionary — 11,496 roots, UNVALIDATED
  gold/                     human-annotated morpheme segmentations
  processed/                80/10/10 split + audit report
src/kapampangan_mt/
  normalize.py pretokenize.py lexicon.py segmenter.py
  morph_bpe.py tokenizer.py vocab_search.py baselines.py
  metrics/  fertility, boundary F1, consistency F1, BLEU/chrF++
  stats/    paired tests, bootstrap, Holm correction
  data/     cleaning, stratified splitting
  nllb/     graft, dataset, train, translate
try_tokenizer.py            test the trained tokenizer, zero installs
segment_word.py             morpheme splitter: kuman -> k | um | an
scripts/                    00-07 pipeline, 10-24 data prep
tests/                      27 tests, no GPU needed
artifacts/                  tokenizers, checkpoints, results, REPORT.md
```

---

## Mapping to the proposal

| Proposal | Implementation |
|---|---|
| Figure 6 — Pre-Tokenizing | `pretokenize.py`, `normalize.py` |
| Figure 7 — Morphological Segmentor pseudocode | `segmenter.py` (`strict_thesis_mode` reproduces it literally) |
| Lexicon Dictionary (p. 41) | `lexicon.py`, `data/lexicon/*.tsv` |
| Morph-BPE (p. 42) | `morph_bpe.py` |
| Vocabulary-size selection by morphological distance (p. 43) | `vocab_search.py` |
| Runtime tokenization behaviour (p. 43) | `tokenizer.py` |
| NLLB graft (p. 44) | `nllb/graft.py` |
| Eq. 1 Fertility Rate | `metrics/fertility.py` |
| Eq. 2–4 Morpheme Boundary F1 | `metrics/boundary_f1.py` |
| Eq. 5–7 Morphological Consistency F1 | `metrics/consistency_f1.py` |
| Eq. 8–9 BLEU, chrF++ | `metrics/translation.py` |
| Eq. 10–13 mean, SD, paired differences, paired t-test | `stats/paired_tests.py` |
| Tables 2–5 | `scripts/07_report.py` → `artifacts/results/REPORT.md` |

---

## Licence and attribution

- PLOC corpus: LGPL, research and non-commercial use — cite it.
- NLLB-200 distilled 600M: CC-BY-NC 4.0 — **non-commercial only**, which fits an
  academic thesis. State this in Chapter 3.
- Web-collected news: record source URL and access date per sentence; use only
  publicly accessible material, per the proposal's Ethical Considerations.
