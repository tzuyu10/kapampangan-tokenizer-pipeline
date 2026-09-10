# Session Handoff — Phase 5 (NLLB fine-tuning), winding toward a negative result

Updated 2026-09-08 (Option 4 complete). Paste this whole file as the opening
prompt for a new session. Supersedes `HANDOFF_PHASE3.md`.

Continue the Kapampangan MorphBPE tokenizer project at
`D:\Coding\thesis\kapampangan-morphbpe-paper-v1` (branch
`feat/kapampangan-morphbpe`). Run `git log` / `git status` first.

**Read `AGENT_CONTEXT.md` in full before doing anything** — the living
session-by-session log, most-recent entries prepended per section. It is
**untracked on disk by deliberate user decision** (2026-08-22): shows as
`??` in `git status`; do not commit it, do not delete it. Focus on the
2026-09-03 → 2026-09-08 Decisions entries.

---

## TL;DR — where Phase 5 actually stands

The proposal's setup — swap NLLB's tokenizer for Kapampangan MorphBPE and
adapt lightly while the decoder stays frozen — **does not beat the zero-shot
NLLB baseline** at ~3,600 silver pairs. Demonstrated across all 3 tokenizers:

| condition | test_bible chrF++ / BLEU | test_ood chrF++ / BLEU |
|---|---|---|
| **`nllb_zeroshot`** (no training) | **33.6 / 11.5** | **33.7 / 9.6** |
| `morphbpe` embedding-only, lr 3e-4 (Colab) | 13.0 / 0.24 | 10.1 / 0.12 |
| `morphbpe` embedding-only, lr 3e-3 (local) | 11.3 / 0.58 | 13.2 / 0.19 |
| `unigram6080` + LoRA-on-encoder r16 (local) | 20.6 / 1.82 | 16.2 / 0.49 |
| `morphbpe` + LoRA-on-encoder r16 (local) | 20.4 / 1.90 | 14.0 / 0.21 |
| `penalty8` + LoRA-on-encoder r16 (local) | 18.5 / 1.04 | 13.6 / 0.27 |

LoRA roughly doubled the embedding-only score but is still ~13-17 chrF++ /
~10 BLEU short, for all three tokenizers. Ordering `unigram6080 >= morphbpe
> penalty8` (dev-loss agrees) — NLLB's own subword algorithm adapts best
downstream, the Phase-3 intrinsic winner adapts worst: the intrinsic
boundary metric does not predict downstream MT here. The bottleneck is a
**frozen-decoder capacity** limit: the
frozen decoder + lm_head expect encoder representations built from NLLB's
own 256K SentencePiece vocab; a 6,080-token MorphBPE vocab is a different
input distribution and ~3,600 silver pairs can't re-align the encoder
output (even with adapters) to what the frozen decoder wants. Zero-shot
works because Kapampangan shares heavy surface vocabulary with Filipino.

Full detail + the dev-loss curves: `experiments/nllb_finetune_v1/reports/phase5-run-2026-09-04-transcript.md`.

## What's in flight right now

1. **Option 4 — DONE (2026-09-08).** LoRA-r16-on-encoder now run for all
   three tokenizers locally on the RTX 4050 (`penalty8-lora/seed0` chrF++
   18.5/13.6 ~212 min; `unigram6080-lora/seed0` chrF++ 20.6/16.2 ~207 min;
   both in `phase5-results-local.json`). The fair three-way is complete:
   `unigram6080 >= morphbpe > penalty8`, all ~13-17 chrF++ below zero-shot.
   **-> the null result is accepted** (see the Decision framework below).
2. **Two Colab escalation notebooks are with the user's groupmates:**
   - `notebooks/phase5-lora-encoder.ipynb` — option 2, bigger encoder LoRA
     (r32, all attn proj + FFN), decoder frozen, no methodology caveat.
     Default `penalty8` x 3 seeds. Realistic outcome ~24-27 chrF++ (still
     short); makes the null result robust to adapter size.
   - `notebooks/phase5-lora-encoder-decoder.ipynb` — option 3, LoRA on
     encoder + decoder. **Departs from the proposal's frozen-NLLB framing**
     (needs a caveat). Runs `penalty8` vs `nllb_native` under an identical
     LoRA budget — that pairing is the real tokenizer test once the decoder
     adapts. Best shot at actually beating zero-shot; also risks
     catastrophic forgetting of NLLB's Filipino fluency.
   Both read the same 6 bundle files, tag their keys distinctly, merge into
   one `phase5-results.json`, resumable. Groupmates send the JSON back →
   `experiments/nllb_finetune_v1/reports/`.
3. **A data refresh is coming** — the user is gathering more data for BOTH
   the tokenizer and the translation set. See "Folding in the data refresh".

## Decision framework — how Phase 5 closes out

- **Option 4 done, all 3 tokenizers below zero-shot's 33.6 -> the null
  result IS accepted (2026-09-08).** Reframe the thesis around the
  tokenizer contribution (Phases 1-4 — MorphBPE beats plain BPE on held-out
  morphology, boundary F1 0.46 vs 0.20). Zero-shot NLLB is the honest MT
  baseline. The Phase 5 section documents what was tried (4 conditions, 2
  scales, 2 LRs, +encoder-LoRA, +decoder-LoRA) and why lightweight retrofit
  fails at this data scale. This is a legitimate, thorough low-resource
  finding. Then do Phase 6 (fuller BLEU/chrF++/COMET on zero-shot) + the
  native-speaker review.
- **If option 3 shows `penalty8` clearly beating `nllb_native`** under equal
  adaptation → MorphBPE has a real downstream effect; report it *with* the
  frozen-decoder caveat.
- **If the data refresh lands ~8-13k translation pairs** → re-run everything
  (local_lora.py + both notebooks) on the bigger set before concluding; LoRA
  scales with data and the picture could change.

## Folding in the data refresh (when it arrives)

**More translation pairs (PAM↔FIL):**
1. Ingest each source into `experiments/parallel_extraction_v2/resources/`
   with a SHA-256 provenance manifest (`resources/**` is already `-text` in
   `.gitattributes`).
2. Add it as a new explicit tier in
   `experiments/parallel_extraction_v2/adjudicate.py` (label silver unless
   native-verified), re-run it → `verified-pairs.csv`.
3. `experiments/parallel_extraction_v2/build_review_artifacts.py` →
   regenerate `DATASET_INVENTORY.csv` + the review sheet (add a batch).
4. Re-freeze split + bundle:
   ```
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_split.py
   .venv\Scripts\python.exe experiments\nllb_finetune_v1\build_colab_bundle.py
   ```
   `build_split.py`: chapter-level Bible holdout + OOD modern test, seed
   20260903; `BIBLE_TEST_VERSES`/`BIBLE_DEV_VERSES` near the top tune sizes.
   If the added data is conversational, weight it toward train — `test_ood`
   is currently near-total collapse (BLEU 0.2) and needs the register.
5. Hand the user the 6-file bundle; groupmates re-run the notebooks;
   locally re-run `local_lora.py` (delete the old keys in
   `phase5-results-local.json` first).

**More tokenizer data / native-validated morphology segmentations:**
- This helps Phases 1-4, **not** Phase 5's downstream gap (the tokenizer
  isn't the bottleneck there).
- If it's native-validated word→boundary data: build
  `experiments/tokenizer_selection_v2/` — re-score the existing 27 v4
  candidates on the gold set (no retraining), report whether `penalty-8` @
  6,080 still wins and the gold F1. Only build a **v5** tokenizer (retrain)
  if the gold data exposes systematic rule errors in `EVIDENCE.md`.
- Do NOT add a Tagalog/Filipino corpus to tokenizer training — it dilutes
  the Kapampangan-specific claim, competes for the 6,080 vocab budget
  (smaller vocab is better for boundary F1 per Phase 3), and unconstrained
  Tagalog text trains boundary-crossing merges that bleed into Kapampangan.

## Local GPU infrastructure (new 2026-09-08)

The user has an **NVIDIA RTX 4050 Laptop (6 GB, bf16-capable)**. Phase 5
experiments now run locally, no Colab session limits.

- **`runs/nllb-local/.venv`** — isolated venv (gitignored under `runs/`),
  **separate from the project `.venv`** and from the global Python's CPU
  `torch`. Has `torch==2.6.0+cu124`, `transformers==4.57.6`, `peft==0.20.0`,
  `sentencepiece`, `sacremoses`, `sacrebleu`. Recreate with `uv venv` + the
  installs in the 2026-09-08 AGENT_CONTEXT tooling entry if it's gone.
- **`experiments/nllb_finetune_v1/local_diagnostic.py`** — the embedding-only
  recipe (warm-start, bf16), CLI `--lr/--epochs/--condition/--seed`. Already
  run (`morphbpe/seed0`, lr 3e-3 → the collapse above).
- **`experiments/nllb_finetune_v1/local_lora.py`** — LoRA-on-encoder,
  validated. CLI `--condition/--seed/--r/--alpha/--targets/--emb-lr/--lora-lr`.
  `morphbpe-lora/seed0` done (chrF++ 20.4). **This is the option-4 tool.**
- Both write `reports/phase5-results-local.json` (same schema as the Colab
  `phase5-results.json`, distinct keys — mergeable).
- **Monitor discipline:** when running these in the background, stop the
  Monitor task as soon as the run completes — `tail -f` monitors set
  `persistent` do not self-terminate and pile up.

## Git state — everything below HEAD is UNCOMMITTED

```
ff18c10  Update HANDOFF_PHASE5.md (warm-start rev)          <- HEAD (committed)
086603b  Checkpoint: Phases 3-4 complete + Phase 5 scaffold  <- restore point
```

Uncommitted on disk (one large session's worth): the Bible-primary refresh
(`adjudicate.py`, `build_split.py`, `build_colab_bundle.py`,
`build_review_artifacts.py`, regenerated `verified-pairs.csv` / splits /
bundle / review sheet / `DATASET_INVENTORY.csv`, 2 new `resources/` files +
manifests), the Phase 5 notebook update, `local_diagnostic.py`,
`local_lora.py`, the 2 escalation notebooks, `reports/phase5-results-*.json`
+ `phase5-run-2026-09-04-transcript.md`, `experiments/nllb_finetune_v1/README.md`.
**Commit when the user asks** — they have not yet. `AGENT_CONTEXT.md` stays
untracked.

## Status by phase

| phase | state |
|---|---|
| 1 — data triage | done |
| 2 — parallel extraction | done (`parallel_extraction_v1` + `_v2`); `verified-pairs.csv` = 4,230 silver pairs |
| 3 — tokenizer selection | **done**. Winner **`penalty-8` @ vocab 6,080** (silver held-out morphology; DEV boundary F1 0.4639 / TEST 0.4093). A gold re-selection (`tokenizer_selection_v2`) is warranted if native-validated data arrives. |
| 4 — NLLB architecture | **done, verified on real weights**. **Caveat: never call `tie_weights()` after the encoder-embedding swap.** `nllb/phase4-architecture-verification.md`. |
| 5 — NLLB fine-tune | **negative result COMPLETE & ACCEPTED (2026-09-08).** Embedding-only + encoder-LoRA both below zero-shot for all 3 tokenizers (`unigram6080` 20.6 >= `morphbpe` 20.4 > `penalty8` 18.5 chrF++ test_bible, vs zero-shot 33.6). 2 Colab escalations (groupmates) still outstanding but not expected to change the conclusion. Reframe around Phases 1-4 + zero-shot MT baseline. |
| 6 — evaluation | not started. Fuller BLEU/chrF++/COMET on `test_bible` + `test_ood`, most likely of `nllb_zeroshot` as the baseline. |

## The Phase 5 dataset (all SILVER)

`experiments/parallel_extraction_v2/data/verified-pairs.csv` — **4,230
pairs**: `bible` 3,084 + `gold_v1` 220 + `gold_stories` 174 +
`silver_gemini` 430 + `silver_a` 230 + `silver_b` 92.
Split (`build_split.py`, seed 20260903): **train 3,590 / dev 238 /
test_bible 329 / test_ood 70**. Train is ~71% Bible.

Bundle: `experiments/nllb_finetune_v1/data/bundle/` — 6 files
(`{train,dev,test_bible,test_ood}.jsonl` + `meta.json` + `vocab.json`), each
Kapampangan side pre-tokenised 3 ways (`morphbpe_ids` / `penalty8_ids` /
`unigram_ids`) + `vocab.json` id-ordered strings for the warm-start.

## Open items

- **Bible corpus rights UNRESOLVED** — from a groupmate; the user believes
  PLOC / DLSU LTL (LGPL) but it's unconfirmed. Confirm exact Kapampangan +
  Tagalog editions + license before any Colab upload. Also: source Deut
  28:30 == 28:29 (mis-extracted, 1 row deduped).
- **Native-speaker review** — `experiments/parallel_extraction_v2/reports/native-speaker-review-sheet.csv`
  (1,346 rows, 7 batches). Standing gate for any *gold* claim; concurrent,
  doesn't block Phase 5.
- **Thesis 13,000-pair target** — 4,230 so far; more Bible books or the
  incoming data close it. Otherwise the low-resource reframe stands.
- **GATITOS** (`resources/smol-gatitos-en_pam.jsonl`) — EN→PAM, in the repo
  with a manifest, NOT in training. Auxiliary only. Cite arXiv 2502.12301 /
  2303.15265.
- Pre-existing, not fixed: a lone-surrogate mojibake (`\udc9d`) in a
  `parallel_extraction_v1/matched-pairs.csv` `gold_v1` row.

## Adjacent, not Phase 5

- **`D:\Coding\thesis\kapampangan-morphbpe-demo\`** — standalone portable
  demo of the selected tokenizer (`penalty-8` @ 6,080) + a Plain-BPE
  baseline + `demo.py` + `README.md` + `PROVENANCE.md`. Pure stdlib, runs
  anywhere. Built 2026-09-08. Nothing in the repo depends on it.
- **`D:\Coding\thesis\` was tidied 2026-09-08** (moves only) — 66 loose
  files → `_archive-bilstm-era/`, `thesis-manuscripts/` (incl.
  `G4-THESIS-PROPOSAL-REVISED (1).pdf`), `presentation/`, `reference-material/`.
  `D:\Coding\thesis\README.md` maps it. `curated_research_dataset/`,
  `datasets/`, `pdf-dls/`, the sibling projects, and the 49 GB PLD tar are
  untouched.

## Non-negotiables (unchanged)

- Every existing artifact stays byte-unchanged; new work in new isolated
  locations; verify with before/after directory hashing.
- Silver vs. gold labelling on every dataset/metric.
- Full test suite + `ruff` + `mypy --strict` before any `src/`-level change
  is "done" (135 tests). Experiment scripts (`build_*.py`, `local_*.py`) get
  `ruff` + a direct `mypy --strict <file>` where deps allow.
- Confirm before: force-pushes, deleting/overwriting data, uploading
  rights-unresolved data to third-party infra, anything needing a restore
  point.
- Update `AGENT_CONTEXT.md` as you go.
- Copy-with-provenance-manifest (SHA-256) for anything from outside the
  repo; `-text` in `.gitattributes` for checksum-referenced dirs.
- New tool/package installs → document in `AGENT_CONTEXT.md` as they happen
  (name, version, exact env, project-dep vs ambient, why).
- `runs/` is globally gitignored (holds `runs/nllb-local/.venv` now). The
  22 MB bulk `pld_prompt_entries_pam_fil.csv` is gitignored (manifest only).

## Key file map

- `AGENT_CONTEXT.md` — full log (untracked, on disk).
- `DATASET_INVENTORY.csv` — every thesis dataset, labelled (22 rows).
- `experiments/tokenizer_selection_v1/` — Phase 3 selection (silver).
- `experiments/expanded_morphology_v4/artifacts/{morphbpe,penalty-8,unigram-ablation}/…/vocab-6080`
  — the 3 tokenizers Phase 5 uses. `penalty-8` = the winner = `v4prop 6k 8`.
- `nllb/phase4-architecture-verification.{json,md}` — Phase 4 verdict + the
  exact Phase 5 requirements.
- `experiments/parallel_extraction_v2/` — `adjudicate.py`, `verified-pairs.csv`,
  review sheet, `build_review_artifacts.py`.
- `experiments/nllb_finetune_v1/` — `build_split.py`, `build_colab_bundle.py`,
  `local_diagnostic.py`, `local_lora.py`, `data/bundle/`, `reports/`, `README.md`.
- `notebooks/` — `phase5-nllb-morphbpe-finetune.ipynb` (base, embedding-only),
  `phase5-lora-encoder.ipynb` (option 2), `phase5-lora-encoder-decoder.ipynb`
  (option 3).
