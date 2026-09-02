# Session Handoff — Phase 5 (NLLB fine-tuning) and beyond

Written 2026-09-02. Paste this whole file as the opening prompt for a new
session. It supersedes `HANDOFF_PHASE3.md` (kept for history).

---

Continue the Kapampangan MorphBPE tokenizer project at
`D:\Coding\thesis\kapampangan-morphbpe-paper-v1` (branch
`feat/kapampangan-morphbpe`). Run `git log`/`git status` first.

**Read `AGENT_CONTEXT.md` in full before doing anything** — it is the
living session-by-session log, most-recent entries prepended in each
section. It is **untracked on disk by deliberate user decision** (2026-08-22),
so it will show as `??` in `git status` — do not commit it, do not delete
it. Pay attention to the 2026-08-28 → 2026-09-02 Decisions entries.

## Checkpoint you are starting from

Commit **`086603b`** "Checkpoint: Phases 3-4 complete + Phase 5 scaffold
(pre-data-iteration)". This was made specifically so the user can gather /
modify more translation data and **restart Phase 5** from a clean state.
If Phase 5 data work goes sideways, `git reset --hard 086603b` returns
here (then restore `AGENT_CONTEXT.md` from disk if needed — it is outside
git).

## Status by phase

| phase | state |
|---|---|
| 1 — data triage | done (`translation_gold_v1`, `morphology_gold_v1`) |
| 2 — parallel extraction | done + a 2nd pass (`parallel_extraction_v1` + `_v2`) |
| 3 — tokenizer selection | **done**. Winner: **`penalty-8` @ vocab 6,080** (held-out morphology DEV boundary F1 0.4639 / TEST 0.4093). Hard-constrained `morphbpe` family added to v4. See `experiments/tokenizer_selection_v1/`. |
| 4 — NLLB architecture | **done, verified on real weights**. Encoder embedding can be untied + trained alone; target side unchanged. **Caveat: `tie_weights()` re-ties the encoder — apply the swap after model load and never call `tie_weights()`.** See `nllb/phase4-architecture-verification.md`. |
| 5 — NLLB fine-tune | **scaffolded, NOT run**. `experiments/nllb_finetune_v1/` + `notebooks/phase5-nllb-morphbpe-finetune.ipynb`. Waiting on: (a) user's data changes, (b) rights review before Colab upload, (c) the user actually running the notebook. |
| 6 — evaluation | not started. Fuller BLEU/chrF++/COMET on the held-out test set, building on `phase5-results.json`. |

## The translation dataset (all SILVER)

`experiments/parallel_extraction_v2/data/verified-pairs.csv` — **716 pairs**,
built by `adjudicate.py` from: the v1 gold (220), the v2 PLD alignment
sweep (silver_a 230 + silver_b 92), and a **native-authored story corpus**
(174 — modern/everyday/cultural register, the one thing the project
otherwise lacked). Tiers:

| tier | n | what |
|---|---:|---|
| `gold_stories` | 174 | native-authored, user-vouched (`story-pairs.csv` ← a PDF the user supplied) |
| `gold_v1` | 220 | user spot-checked (**user is not a native speaker**) |
| `silver_a` | 230 | PLD sweep, high confidence — three non-native passes |
| `silver_b` | 92 | PLD sweep, weaker band |

The label everywhere: **the entire set is silver for Phase 5. A
native-speaker pass on `experiments/parallel_extraction_v2/reports/native-speaker-review-sheet.csv`
(716 rows, batches 1-5, simple 6-column format) is still the gate for any
thesis-gold claim.** Claude read through all of it 2026-09-02
(`resources/claude-review-2026-09-02.csv`: 3 dropped, 27 flagged `partial`)
but that is non-native.

## If the user changes / adds translation data — the Phase 5 re-run recipe

1. New pairs go through the same discipline: copy source into a
   `resources/` dir with a SHA-256 provenance manifest; fold into
   `verified-pairs.csv` via `adjudicate.py` (extend it — it already merges
   4 sources) with an explicit tier.
2. Re-run the split + bundle:
   ```
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_split.py
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_colab_bundle.py
   ```
   `build_split.py` does a **story-level holdout** (5 whole native-authored
   stories are removed from train/dev entirely) + a clean `gold_v1`
   sample; seed 20260902; leakage asserted. Adjust `TEST_STORY_UNITS` /
   sizes there if the story set changes.
3. `build_colab_bundle.py` writes `data/bundle/{train,dev,test}.jsonl`
   with the Kapampangan side pre-tokenised by **both** vocab-6080 MorphBPE
   artifacts (`morphbpe`, `penalty-8`) so the notebook needs no project
   code. It also stamps `meta.json` with the split SHA-256s and a
   `rights_note`.
4. The notebook (`notebooks/phase5-nllb-morphbpe-finetune.ipynb`) is
   data-agnostic — the user just re-uploads the 4 bundle files and
   `Run all`.

## Phase 5 notebook — the Colab protocol still applies

You write `.ipynb`, you do **not** run them. Before telling the user to run
any notebook, post a plain-language summary in chat: what each cell does,
what it uploads/downloads and from where, GPU tier + why, time estimate,
where output lands. The Phase 5 summary was already posted 2026-09-02; if
you regenerate the notebook, re-post it.

- Pre-authorised: downloading `facebook/nllb-200-distilled-600M` weights
  (~2.4 GB) inside Colab. GPU work happens in Colab (detect the runtime's
  actual GPU). A local weights copy, if ever needed, goes on **D:**, not C:.
- The Phase 5 bundle contains PLD-derived pairs (**redistribution rights
  unresolved**) + native-authored stories + gold_v1. **Confirm the rights
  point with the user before they upload to Colab** — this is an explicit
  non-negotiable.
- NOT authorised: automating polytranslator.com's live translator widget.

## Open items / decisions still pending

- **Native-speaker review** of `native-speaker-review-sheet.csv` — the
  standing gate for gold claims. Runs concurrently; only actually blocks a
  *gold* label, not the Phase 5 run.
- **Gemini 500-sentence batch** — still out with the user's external
  reviewer (`experiments/parallel_extraction_v1/reports/gemini-batch-review-sheet.csv`).
  Fold in additively if it returns usable.
- **google/smol (GATITOS)** — 3,993 EN→PAM lexicon entries, CC-BY-4.0,
  downloaded to scratch but **not copied into the repo**. Decided out of
  Phase 5 v1; revisit as an auxiliary if results are weak. If used, copy in
  with a provenance manifest + cite arXiv 2502.12301 / 2303.15265.
- **Thesis 13,000-pair target** — not reachable; real number is 716
  (silver). User to decide whether to rewrite the proposal's data section
  to the low-resource regime (Claude offered to draft it) or keep the
  number with a limitations paragraph. Not blocking.
- **Phase 5 result expectation** — 598 silver training pairs adapting a
  600M model is deep low-resource; a MorphBPE-vs-native gap smaller than
  the across-seed std is not a real effect. Say so plainly when reporting.

## Non-negotiables (unchanged)

- Every existing artifact stays byte-unchanged; new work in new isolated
  locations. Verify with before/after directory hashing in runners.
- Silver vs. gold labelling on every dataset/metric.
- Full test suite + `ruff` + `mypy --strict` before any package-level change
  is "done". (135 tests currently pass.)
- Confirm before: force-pushes, deleting/overwriting data, uploading
  rights-unresolved data to third-party infra, anything needing a restore
  point.
- Update `AGENT_CONTEXT.md` as you go, not just at the end.
- Copy-with-provenance-manifest (SHA-256) for anything pulled in from
  outside the repo; protect checksum-referenced dirs with `-text` in
  `.gitattributes` before committing.
- **New tool/package installs → document in `AGENT_CONTEXT.md` as they
  happen** (name, version, exact environment, project-dep vs ambient-tool,
  why). This session's data tooling
  (`sentence-transformers`/`torch-cpu`/`transformers`/`scikit-learn`) went
  into the machine's **global Python** (`D:\Coding\Python`), NOT this
  project's `.venv` — a fresh environment won't have them. The `.venv` is
  clean and matches `pyproject.toml` (`dev` + `nllb-baseline` extras only).
- `runs/` is globally gitignored (rights-unresolved OCR/parse outputs).
  `runs/source-ocr-v2/text/` is a shared parent — a targeted `rm` must name
  specific subdirectories, never `text/*`.

## Key file map

- `AGENT_CONTEXT.md` — the full log (untracked, on disk).
- `DATASET_INVENTORY.csv` — every thesis-relevant dataset, labelled
  (21 rows; `native_speaker_reviewed` column).
- `experiments/tokenizer_selection_v1/` — Phase 3 selection.
- `experiments/expanded_morphology_v4/artifacts/{morphbpe,penalty-8}/candidates/vocab-6080`
  — the two tokenizers Phase 5 integrates.
- `nllb/phase4-architecture-verification.{json,md}` — Phase 4 verdict +
  the exact Phase 5 requirements. `src/kapampangan_morphbpe/nllb_contract.py`
  carries the `integration_property_verification` block.
- `experiments/parallel_extraction_v2/` — the alignment sweep, adjudication,
  `verified-pairs.csv`, the review sheet, `build_review_artifacts.py`.
- `experiments/nllb_finetune_v1/` — Phase 5 split + bundle + `README.md`.
- `notebooks/phase5-nllb-morphbpe-finetune.ipynb` — hand to the user.
