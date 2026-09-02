# Session Handoff — Phase 3 (vocab/penalty/dropout selection)

Written 2026-08-28, end of the Phase 2 session, for whoever starts the next
session. Paste the "Immediate next step" section (or this whole file) as
the opening prompt.

---

Continue the Kapampangan MorphBPE tokenizer project at
`D:\Coding\thesis\kapampangan-morphbpe-paper-v1` (branch
`feat/kapampangan-morphbpe`). Check `git log`/`git status` for the current
HEAD and any uncommitted work before doing anything else.

Read `AGENT_CONTEXT.md` first, in full — it is a living log, most recent
entries are prepended to each section. Pay special attention to the
2026-08-26 through 2026-08-28 entries: Phase 2 (parallel-extraction) is now
substantially complete — PLD sentence pairs, an external vocabulary
verification pass, a 500-sentence AI-generated batch (mechanically checked
only, not linguist-reviewed — this review runs concurrently with Phase 3
and Phase 4, see below), a full OCR re-verification pass (three steps:
targeted page checks, full Mirikitani/Forman re-OCR, all 40 previously
untouched PDFs), and a dictionary-verification pass that both confirmed and
**corrected** several earlier claims (read the 2026-08-28 entries carefully
— they document a real self-caught error, not just new findings). Do not
re-discover any of this from scratch. The original full mandate (reproduced
below) still governs this project; only the "Immediate next step" section
at the bottom is new.

## Full development authority (unchanged from the original mandate)

You have full development authority to take this project from its current
state to a working translation-integration prototype: build a usable
evaluation gold standard, select a vocab-size/penalty/dropout configuration
on a genuine held-out split, integrate the real NLLB-200-Distilled-600M
model via Colab, and produce real BLEU/chrF++ numbers. This is a
multi-session undertaking — pace it accordingly.

## Colab notebook protocol — read before Phase 4

You write `.ipynb` notebooks; you do not run them. Claude Code has no access
to Colab's remote GPU runtime — it can only write files and drive the local
shell/filesystem. Do not attempt to automate Colab execution via the browser
tool. The user runs every notebook themselves, in their own Colab session.

Every time a notebook is ready to hand off, **stop and post a clear summary
in chat before telling the user to run it** — what each phase does, exactly
what data/weights it uploads or downloads and from where, GPU tier and why,
a time estimate, and where the output lands. Only after that summary should
you say the notebook is ready to run.

**Pre-authorized:** downloading the real NLLB-200-Distilled-600M weights
(~2.4GB), primarily inside Colab; if a local copy is ever needed, it must
land on the D: drive, not C:. GPU work happens in Colab, detect the actual
runtime's GPU/VRAM at the start of each notebook rather than assuming a
tier.

**Explicitly NOT authorized:** automating queries against
polytranslator.com's live translator widget (rate-limited, generic
multilingual backend, never treat its output as gold/reliable silver).

## Phased plan

**Phase 1 — DONE.** AI-assisted triage of the 250-row MT candidate pool and
650-row morphology candidate pool, plus a full user adjudication of every
flagged conflict. See `experiments/translation_gold_v1/` and
`experiments/morphology_gold_v1/`.

**Phase 2 — DONE, substantially beyond original scope.** Real
extraction/alignment against the raw PLD archive (`experiments/parallel_extraction_v1/`):
38 close-reading-verified PLD sentence pairs (user-reviewed, one pair
corrected/removed after review) + 182 externally-sourced vocabulary pairs
(individually verified against Forman/Bergaño/Samson, with real corrections
made along the way — read the 2026-08-28 Decisions entries) + a 500-sentence
AI-generated batch (mechanically word-checked only, **not yet
linguist-reviewed** — a reviewer-ready CSV was sent to the user and is
pending their reviewer's return; this runs on its own timeline,
**concurrent with Phase 3 and Phase 4** — neither touches translation-pair
data, so neither is blocked by nor blocks the review. The dependency only
becomes real at **Phase 5**, which needs actual reviewed/trustworthy
training data as input — check whether the review has come back before
starting Phase 5, not before Phase 3 or 4). A full OCR re-verification pass also ran this session
(`scripts/rerun_ocr.py`, `scripts/extract_new_pdfs.py`) confirming the
original OCR work's completeness and surfacing two genuine new finds: a
real citable academic source (Martizano 2024, modern Kapampangan slang with
example sentences — registered in `source-registry.json` but **not yet
formally extracted into a tracked dataset**) and real usage evidence for
`mekipag-` (previously a "deferred, genuinely open" morphology item in
`EVIDENCE.md`). Honest scope note: even combined, this is nowhere near the
original mandate's ~13,000-pair training-scale target — better suited as a
small gold evaluation set. **The training-scale PAM-FIL data strategy
conversation was explicitly deferred by the user and has not yet
happened** — raise it if it hasn't come up by the time Phase 3 wraps.

**Phase 3 — THIS IS THE IMMEDIATE NEXT STEP — see below.**

**Phase 4 — Colab: NLLB model weights + architecture verification.**
Unchanged from the original mandate: verify the embedding-swap assumption
in `nllb_contract.py`/`nllb_adapter.py`.

**Phase 5 — Colab: fine-tuning implementation and training run.** Use the
**paper-aligned hard-constrained MorphBPE condition added in Phase 3** (not
the weighted-penalty or stochastic-dropout extensions) as the source
tokenizer. Package a Colab bundle, review with the user before upload
(parallel data's redistribution rights are unresolved).

**Phase 6 — Colab (or pulled back locally): real translation evaluation.**
BLEU/chrF++ (COMET if feasible) against both NLLB-native and
MorphBPE-integrated conditions, identical training controls.

## Non-negotiables (unchanged, don't relitigate)

- Every existing artifact stays byte-unchanged; new work goes in new,
  isolated locations.
- Silver vs. gold labeling discipline on every dataset/metric.
- Full test suite + ruff + mypy --strict before considering any
  package-level change done.
- Confirm before: force-pushes, deleting/overwriting data, uploading rights-
  unresolved data to third-party infrastructure, anything needing a restore
  point.
- Update `AGENT_CONTEXT.md` as you go, not just at the end of a session.
- Copy-with-provenance-manifest (SHA-256) discipline for anything pulled in
  from outside the repo; protect any resources/ directory holding
  checksum-referenced files in `.gitattributes` (`-text`) before committing.
- **New tool/package installations must be documented in `AGENT_CONTEXT.md`
  as they happen** (name, version, exact environment, project-dependency
  vs. ambient-tool, why) — this is now a standing policy, not a one-off.
  Note: this session's OCR tooling (`pypdf`, `pymupdf`, `pytesseract`) went
  into the machine's **global Python** (`D:\Coding\Python`), not this
  project's own `.venv` — a fresh environment won't have them.
- `runs/source-ocr-v2/text/` is a **shared parent directory** across
  multiple pieces of work — a targeted `rm` must name specific
  subdirectories, never `text/*` (this session lost and had to reason
  about recovering from exactly that mistake once already).

## Immediate next step: Phase 3 — vocab/penalty/dropout selection

This has been an explicitly flagged long-standing blocker since the
project's very first tokenizer experiments (v1 through v4, the weighted
grid, the stochastic-dropout grid) — every prior candidate left vocab size
and penalty/dropout **unselected** because no genuine held-out dev/test
split existed. That blocker was resolved on 2026-08-25 (the
`kapampangan-general-corpus-v1` monolingual split, 90,184/9,633/9,295
rows, documented 80/10/10 split, seed 20260816) but never acted on. Two
parts, both explicitly in scope:

1. **Actually select a configuration** using real validation numbers on
   morphology segmentation quality (boundary F1, MCF1, or similar —
   whatever this project's own existing metrics already compute) across
   the trained candidates (6,080/8,192/16,384 vocab × penalty/dropout
   grid). You'll need a genuine held-out morphology dev/test split to
   evaluate against — `experiments/morphology_gold_v1/` (Phase 1's
   triaged 650-row candidate set, including the full 97-row user
   adjudication) is the most credible available source for this; design
   how to carve a genuinely disjoint dev/test partition from it (or
   combine with the existing v2 lexicon's morphology annotations if
   needed) rather than assuming a pre-made split exists. Select on DEV
   only, confirm on TEST, cite exact numbers, and update `AGENT_CONTEXT.md`
   to mark this long-standing blocker resolved.
2. **Add a hard-constrained `ConstrainedBPETrainer` condition** trained on
   v4's own expanded-morphology resegmented stream
   (`experiments/expanded_morphology_v4/runs/prepared/training-stream.jsonl`)
   as a new artifact family under
   `experiments/expanded_morphology_v4/artifacts/` — v4 currently has none
   (replaced by the weighted penalty grid in the 2026-08-21 rebuild). Do
   not touch or replace `plain`/`penalty-*`/`stochastic-*`/
   `unigram-ablation`. This is the exact condition Phase 5 will integrate
   with NLLB, so get it right.

Start by reviewing what morphology evaluation infrastructure already
exists in this repo (boundary-F1/MCF1 computation appears throughout the
v2/v3/v4 experiment scripts already) before building anything new, and
report back on your proposed dev/test split methodology before running a
full selection pass across every candidate — this project's own
established pattern is small-sample validation before full-scale
commitment.
