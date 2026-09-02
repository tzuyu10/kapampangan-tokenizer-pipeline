# Session Handoff — Phase 5 (NLLB fine-tuning), with a data refresh expected

Updated 2026-09-03. Paste this whole file as the opening prompt for a new
session. Supersedes `HANDOFF_PHASE3.md` (kept for history).

---

Continue the Kapampangan MorphBPE tokenizer project at
`D:\Coding\thesis\kapampangan-morphbpe-paper-v1` (branch
`feat/kapampangan-morphbpe`). Run `git log` / `git status` first.

**Read `AGENT_CONTEXT.md` in full before doing anything** — the living
session-by-session log, most-recent entries prepended per section. It is
**untracked on disk by deliberate user decision** (2026-08-22): it shows as
`??` in `git status`; do not commit it, do not delete it. Focus on the
2026-08-28 → 2026-09-03 Decisions entries.

## Git state

```
60da05d  Phase 5: warm-start the encoder embedding + speed fixes      <- HEAD
4e64042  Phase 5: drop trained nllb_native (OOM on T4)
a27e59b  Phase 5: add unigram6080 condition (fair comparison)
907db79  Add HANDOFF_PHASE5.md
086603b  Checkpoint: Phases 3-4 complete + Phase 5 scaffold           <- restore point
```

- **Start new work from HEAD (`60da05d`)** — it has the improved Phase 5
  notebook (warm-start, unigram6080). Everything through Phase 4 is done.
- `git reset --hard 086603b` is *only* for "Phase 5 went badly, undo the
  whole scaffold" — then restore `AGENT_CONTEXT.md` from disk (it is
  outside git).

## Status by phase

| phase | state |
|---|---|
| 1 — data triage | done (`translation_gold_v1`, `morphology_gold_v1`) |
| 2 — parallel extraction | done + a 2nd pass (`parallel_extraction_v1` + `_v2`) |
| 3 — tokenizer selection | **done**. Winner **`penalty-8` @ vocab 6,080** (held-out morphology DEV boundary F1 0.4639 / TEST 0.4093). Hard-constrained `morphbpe` family added to v4. `experiments/tokenizer_selection_v1/`. |
| 4 — NLLB architecture | **done, verified on real weights**. Encoder embedding can be untied + trained alone; target side unchanged. **Caveat: `tie_weights()` re-ties the encoder — apply the swap after model load and never call it.** `nllb/phase4-architecture-verification.md`. |
| 5 — NLLB fine-tune | **first Colab run done; recipe failed; revised; re-run pending.** See next section. |
| 6 — evaluation | not started. Fuller BLEU/chrF++/COMET on the held-out test set, from `phase5-results.json`. |

## Phase 5 — what happened and where it stands

`experiments/nllb_finetune_v1/` + `notebooks/phase5-nllb-morphbpe-finetune.ipynb`.
Conditions: `morphbpe` / `penalty8` **vs `unigram6080`** (fair headline —
same 6,080 vocab, same Kapampangan corpus, same embedding recipe, only the
subword algorithm differs) + `nllb_zeroshot` (the pretrained off-the-shelf
reference the proposal names).

**First Colab run (random-init `nn.Embedding(6080,1024)`, everything else
frozen — the thesis's stated condition): FAILED.** `nllb_zeroshot` TEST
chrF++ 33.59 / BLEU 10.67; every trained `morphbpe` seed converged to
chrF++ ~10-11 / BLEU ~0.3. A random 6,080 embedding can't learn NLLB's
semantic space from 598 pairs with the encoder frozen. Runs were 80-130
min each (per-epoch beam-5 dev generation) — the runtime disconnected
mid-way.

**Revision (commit `60da05d`), pending re-run:**
- Notebook **warm-starts** each embedding row from the mean of NLLB's own
  sub-token embeddings for that token string (`data/bundle/vocab.json`);
  special ids 0-3 mapped onto NLLB's pad/unk/bos/eos rows.
- Checkpoint selection on **dev loss** (one forward pass); generation eval
  only once at the end. batch 16 / 15 epochs / patience 4 / LR 3e-4 / beam
  4 → ~20 min/run. **1 seed** (`meta.seeds=[0]`); add [1,2] only if a
  condition beats zero-shot and the gap is worth error bars.
- Trained `nllb_native` was dropped (256K trainable embedding OOMs a T4).

**Escalation if warm-start still can't beat zero-shot (~33):** add a
LoRA-on-encoder condition (clearly labelled as departing from the frozen-
model condition), or accept the honest low-resource null result and
redirect effort to the native-speaker review + more data.

## Expected next step: a data refresh, then re-run Phase 5

The user said they will likely bring **new / modified translation data**.
Recipe:

1. **Ingest** each new source with the standing discipline: copy it into an
   `experiments/parallel_extraction_v2/resources/` file (or a new
   experiment dir) with a SHA-256 provenance manifest; `.gitattributes`
   `-text` the dir if a checksum references it.
2. **Fold into `verified-pairs.csv`** by extending
   `experiments/parallel_extraction_v2/adjudicate.py` — it already merges 5
   sources (v1 matched-pairs, v1 external-vocab, `story-pairs.csv`, the v2
   sweep via `user-evaluated-candidates-2026-09-01.csv`) and applies the
   Claude read-through (`resources/claude-review-2026-09-02.csv`). Add the
   new source as a **new explicit tier** (e.g. `gold_stories2`,
   `silver_c`), label it silver unless a native speaker verified it, re-run
   `adjudicate.py`. Then regenerate the inventory + review sheet:
   `experiments/parallel_extraction_v2/build_review_artifacts.py`.
3. **Re-freeze the split + bundle:**
   ```
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_split.py
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_colab_bundle.py
   ```
   - `build_split.py`: story-level TEST holdout (5 whole native-authored
     stories removed from train/dev) + a clean `gold_v1` sample; seed
     20260902; leakage asserted. **If the story set changed, edit
     `TEST_STORY_UNITS` / the sample sizes** near the top.
   - `build_colab_bundle.py` → `data/bundle/{train,dev,test}.jsonl` +
     `meta.json` + **`vocab.json`** (id-ordered token strings per
     condition, for the warm-start). Pre-tokenises the Kapampangan side
     three ways at vocab 6,080. Needs `tokenizers` (`.venv`
     `nllb-baseline` extra).
4. **Hand the user the notebook + bundle** (the notebook is data-agnostic).
   Tell them to **delete any old `phase5-results.json`** in Colab and
   re-upload the **5** bundle files. Re-post the Colab run summary first
   (protocol below).
5. If the data grew a lot (say >1,500 pairs), reconsider: more epochs, 3
   seeds from the start, and whether the frozen-encoder recipe now works
   without warm-start tricks.

## Colab protocol (still applies)

You write `.ipynb`, you do **not** run them. Every time a notebook is ready
to hand off: **stop and post a plain-language summary in chat first** —
what each cell does, what it uploads/downloads and from where, GPU tier +
why, time estimate, where output lands.

- Pre-authorised: downloading `facebook/nllb-200-distilled-600M` (~2.4 GB)
  inside Colab. Detect the runtime's actual GPU. A local weights copy, if
  ever needed, goes on **D:**, not C:.
- The Phase 5 bundle contains **PLD-derived pairs (redistribution rights
  unresolved)** + native-authored stories + gold_v1. **Confirm the rights
  point with the user before they upload to Colab** — explicit
  non-negotiable.
- NOT authorised: automating polytranslator.com's live translator widget.

## Open items

- **Native-speaker review** of
  `experiments/parallel_extraction_v2/reports/native-speaker-review-sheet.csv`
  (716 rows, batches 1-5, 6-col format) — the standing gate for any *gold*
  claim. Concurrent; doesn't block the Phase 5 run. Claude's 2026-09-02
  non-native read-through is `resources/claude-review-2026-09-02.csv`
  (3 dropped, 27 `partial`), already applied.
- **Gemini 500-sentence batch** — still out with the user's external
  reviewer (`experiments/parallel_extraction_v1/reports/gemini-batch-review-sheet.csv`).
  Fold in additively if usable.
- **google/smol (GATITOS)** — 3,993 EN→PAM lexicon entries, CC-BY-4.0, in
  scratch, **not in the repo**. Out of Phase 5 v1; revisit as an auxiliary
  if results stay weak. If used: copy in with a provenance manifest, cite
  arXiv 2502.12301 / 2303.15265.
- **Thesis 13,000-pair target** — not reachable (real number ~716 silver).
  User to decide: rewrite the proposal's data section to the low-resource
  regime (Claude offered to draft) or keep the number with a limitations
  paragraph. Not blocking.

## The translation dataset as of HEAD (all SILVER)

`experiments/parallel_extraction_v2/data/verified-pairs.csv` — **716 pairs**
(`adjudicate.py`): `gold_stories` 174 (native-authored, user-vouched;
`story-pairs.csv` ← a user-supplied PDF) + `gold_v1` 220 (user spot-checked,
user is **not** a native speaker) + `silver_a` 230 (PLD sweep, 3 non-native
passes) + `silver_b` 92. `claude_review` column: 689 ok / 27 partial; 3
rows dropped. **The whole set is silver for Phase 5**; the current split is
TRAIN 598 / DEV 45 / TEST 70.

## Non-negotiables (unchanged)

- Every existing artifact stays byte-unchanged; new work in new isolated
  locations; verify with before/after directory hashing.
- Silver vs. gold labelling on every dataset/metric.
- Full test suite + `ruff` + `mypy --strict` before any package-level
  change is "done" (135 tests pass at HEAD).
- Confirm before: force-pushes, deleting/overwriting data, uploading
  rights-unresolved data to third-party infra, anything needing a restore
  point.
- Update `AGENT_CONTEXT.md` as you go.
- Copy-with-provenance-manifest (SHA-256) for anything from outside the
  repo; `-text` in `.gitattributes` for checksum-referenced dirs.
- **New tool/package installs → document in `AGENT_CONTEXT.md` as they
  happen** (name, version, env, project-dep vs ambient, why). This
  session's data tooling (`sentence-transformers` 6.0.1 / `torch` 2.13.0+cpu
  / `transformers` 5.16.1 / `scikit-learn` 1.9.0 / `numpy` 2.5.2 / `scipy`
  1.18.1) went into the machine's **global Python** (`D:\Coding\Python`),
  NOT this project's `.venv` — a fresh env won't have them. The `.venv` is
  clean, matches `pyproject.toml` (`dev` + `nllb-baseline` extras only).
- `runs/` is globally gitignored. `.gitignore` also excludes the 22 MB bulk
  `pld_prompt_entries_pam_fil.csv` (only its provenance manifest tracked).
  `runs/source-ocr-v2/text/` is a shared parent — a targeted `rm` must name
  specific subdirectories, never `text/*`.

## Key file map

- `AGENT_CONTEXT.md` — full log (untracked, on disk).
- `DATASET_INVENTORY.csv` — every thesis-relevant dataset, labelled (21
  rows; `native_speaker_reviewed` column).
- `experiments/tokenizer_selection_v1/` — Phase 3 selection.
- `experiments/expanded_morphology_v4/artifacts/{morphbpe,penalty-8,unigram-ablation}/…/vocab-6080`
  — the three tokenizers Phase 5 uses.
- `nllb/phase4-architecture-verification.{json,md}` — Phase 4 verdict + the
  exact Phase 5 requirements. `src/kapampangan_morphbpe/nllb_contract.py`
  has the `integration_property_verification` block.
- `experiments/parallel_extraction_v2/` — alignment sweep, `adjudicate.py`,
  `verified-pairs.csv`, review sheet, `build_review_artifacts.py`.
- `experiments/nllb_finetune_v1/` — Phase 5 split + bundle + `build_split.py`
  + `build_colab_bundle.py` + `README.md`.
- `notebooks/phase5-nllb-morphbpe-finetune.ipynb` — hand to the user.
