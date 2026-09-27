# Handoff — Kapampangan MorphBPE Thesis Project

Last updated: 2026-09-13. Written for a fresh Claude session (or a human) that
has no memory of prior conversations. Read the "Read this first" section
before doing anything else — it explains an active infrastructure outage
that changes how work has to be done right now.

Repo: `C:\Users\Gabo\kapampangan-tokenizer-pipeline` (Windows machine,
connected to Claude via the device bridge in the desktop app). A Claude
Project called **"Thesis Ninja Time"** holds five longer write-ups that go
deeper than this file on specific topics — see "Project docs" at the bottom.

---

## Read this first: local shell execution is currently broken

`device_bash` (the tool that runs commands inside a sandboxed VM with access
to this repo) fails with:

```
sandbox-helper: no Plan9 drive shares mounted under /mnt/.virtiofs-root/shared
```

**This is a confirmed Microsoft bug, not a Claude or repo problem.** The
September 8, 2026 Windows cumulative update (KB5124008 on most Windows 11
x64/ARM64 builds; KB5124012 on 26H1 ARM64; KB5122878 on Windows 10) broke
the Plan9/virtiofs share mechanism the Cowork sandbox VM uses to reach local
folders. Anthropic's status page confirmed this as an open incident on
2026-09-10; Microsoft acknowledged the bug but had not shipped a fix as of
2026-09-12. Restarting Claude, reinstalling it, or rebooting the machine
does **not** help — this is documented and reproduced across many machines.

**What still works:** `device_list_dir`, `device_stage_files`, and
`device_commit_files` are unaffected — only the in-VM shell is broken.

**The practical workaround for anything that needs code execution:** stage
the specific files needed from the repo into the cloud session's own
workspace (unaffected by this bug), run Python there, then
`device_commit_files` the results back into the repo. This is how all of
this session's training-code investigation was done, and it's the way to
actually run new evaluations/experiments until Microsoft ships a fix.

An uninstall-the-KB workaround exists (`wusa /uninstall /kb:5124008
/norestart`, confirmed to restore the shell on several machines) but it
reverses ~628 security fixes including two actively-exploited
privilege-escalation CVEs, Windows Update will silently reinstall the KB
unless updates are paused, and there are reports of the uninstall itself
failing or (once) causing a boot failure. Don't suggest this casually —
only raise it if the user brings it up, and confirm their exact Windows
build/KB first.

---

## Repo layout cheat-sheet

```
kapampangan-tokenizer-pipeline/
├── src/kapampangan_morphbpe/     — the tokenizer training/eval library
│   ├── bpe.py                    — ConstrainedBPETrainer (hard-constrained; SHIPPED/SELECTED)
│   ├── weighted_bpe.py           — WeightedMorphBPETrainer (crossing-penalty scoring)
│   ├── stochastic_bpe.py         — StochasticWeightedMorphBPETrainer (+ BPE-dropout)
│   ├── boundary_safe_bpe.py      — BoundarySafeBPETrainer (runtime-order audit/defer)
│   ├── evaluation.py             — evaluate_candidate/evaluate_candidates/select_candidate
│   ├── pipeline.py               — export_candidate_models, finalize_selected_tokenizer
│   └── models.py, constants.py   — shared types/constants
├── configs/
│   ├── dataset-contract.json     — official split sizes (train 26268 / val 3284 / test 3284, sealed)
│   ├── candidate-grid.json       — frozen vocab-size grid {1656,3008,6080}, selection hierarchy
│   └── selected-candidate.json   — the official selected tokenizer's metrics (see below)
├── resources/                    — training-lexicon.json (+ manifest); raw corpus lives outside the repo
├── experiments/                  — 13 subfolders, see table below
├── webapp/                       — the React+Python demo app (separate from training; see below)
├── DATASET_INVENTORY.csv         — full inventory of every data source, quality tier, rights status
└── Claude outputs/                — misc prior Claude-session output (stray zip; excluded when pushing)
```

Training venv: `.venv\Scripts\python.exe` at repo root (PowerShell). No pip
installs happen in the cloud session — this repo's own venv is the only
place training code has ever actually been run.

---

## The four BPE trainer variants (what exists vs. what's tested)

| Trainer | File | Idea | Status |
|---|---|---|---|
| `ConstrainedBPETrainer` | `bpe.py` | Pure frequency; boundary-crossing pairs never considered at all | **Shipped.** This trained the official selected tokenizer. |
| `WeightedMorphBPETrainer` | `weighted_bpe.py` | `allowed_frequency − crossing_penalty × crossing_frequency`; crossing pairs demoted in rank but still never merged | Fully swept in `weighted_morphbpe_v3` (penalty ∈ {1,2,4,8} × vocab ∈ {6080,8192,16384}). Strong results, **not officially selected/validated** (see below). |
| `StochasticWeightedMorphBPETrainer` | `stochastic_bpe.py` | Same as above + BPE-dropout: each allowed merge occurrence randomly skipped w.p. `dropout_rate` during training (seeded, deterministic) | **Fully coded, never run.** No experiment folder exists for it. This is the most concrete unused lever in the repo. |
| `BoundarySafeBPETrainer` | `boundary_safe_bpe.py` | Simulates actual runtime (lexicon-free) merge order during training; defers any merge that would cross a boundary on a set of frozen "audit" word forms | Tested narrowly in `boundary_safe_v1` — only works when scoped to 5 known-regression words (`Bucasan`/`Kabukasan`/etc.); applying it to the full 2,634-word audit list degraded training toward character tokenization. |

**Untried combination worth building:** soften `BoundarySafeBPETrainer`'s
hard defer into a penalty (like `weighted_bpe.py` does) instead of blocking
outright — nobody has tried this, and it directly targets the failure mode
`boundary_safe_v1` already documented.

---

## `experiments/` status table (13 folders)

| Folder | What it is | Status |
|---|---|---|
| `weighted_morphbpe_v3` | Crossing-penalty sweep (see above) | **Done.** 12 trained artifacts + determinism proofs. Evaluated against a reused 1,197-word silver audit, **not** the official validation split — no selection performed, explicitly documented as such. |
| `boundary_safe_v1` | Runtime-audit trainer, 5 hard-coded regression words | **Done** (narrow scope). Results baked into its README; raw artifacts no longer present on disk. |
| `vocab_ablation_v1` | Same algorithm, "original" vs "source-adjudicated" lexicon at vocab 8192/16384 | **Done.** Shows data/lexicon quality is a second lever independent of algorithm. |
| `tokenizer_selection_v1` | Official dev/test morphology reference (534 rows: dev 272/test 262), the basis for the real selected-candidate scoring | **Done.** This is the "real" eval set — use it, not ad-hoc silver audits, for any thesis-citable claim. |
| `nllb_finetune_v1` | Downstream fine-tune of NLLB-200-distilled-600M, Kapampangan→Filipino, comparing tokenizer conditions (`morphbpe`, `penalty8`, `bpe6080`, `unigram6080`) | **IN PROGRESS.** A 4th condition (`bpe6080`) was added 2026-09-13 and was still running as of last check. **Important:** every trained condition so far scores far below the untrained zero-shot NLLB baseline (best trained BLEU ~2.3 vs. zero-shot ~10–12) — likely catastrophic forgetting from a fresh embedding + tiny ~3,590-pair silver corpus, not a verdict on any tokenizer. Don't trust these downstream numbers to judge tokenizer quality until the fine-tune recipe itself is revisited. |
| `morphology_gold_v1` | 650-row morphology-annotated dataset, tiers A(220)/B(306)/C(26)/D(1)/**F(97, only partially adjudicated)** | Done; the F tier is unresolved headroom. |
| `source_adjudicated_v1`, `source_adjudicated_v2` | Successive versions of the adjudicated training lexicon (v2 = current, 3,311 roots + 26 compounds) | Done; v2 is what current training uses. |
| `internet_root_reconciliation_v1` | 143,529-row page-cited evidence file cross-checking every training word type against Forman/Bergano/Samson/ACD/Kaikki | Reference data; feeds lexicon adjudication, not yet fully exploited. |
| `expanded_morphology_v4` | 13,615-entry rule-derived morphology index (recursive analyzer) | Done; feeds MorphBPE training boundaries. |
| `parallel_extraction_v1`, `parallel_extraction_v2` | PAM↔FIL sentence pair extraction/curation for the translation side (Phase 5), not the tokenizer itself | Done/ongoing; mostly tangential to tokenizer training. |
| `translation_gold_v1` | Triage of an auto-matched translation pair set — mostly rejected (10/250 usable) | Done; confirms that particular source isn't usable, tangential to tokenizer training. |

---

## The official selected tokenizer

`configs/selected-candidate.json`: vocab size **6,080**, trained by
`ConstrainedBPETrainer` (hard-constrained, via `pipeline.py`'s
`finalize_selected_tokenizer`, which retrains twice and asserts a
byte-identical rebuild). Key metric: `morpheme_boundary.f1 = 0.4454`,
scored against the **official** `data/validation.csv` (3,284 records) via
`evaluate_candidate()`. Selection followed the pre-frozen lexicographic
hierarchy in `candidate-grid.json` (reject boundary violations → minimize
morphological distance → maximize boundary F1 → maximize consistency F1 →
minimize fertility → prefer smaller vocab).

**Open, unreconciled discrepancy:** three different Boundary F1 numbers
exist for "hard-constrained MorphBPE" at similar settings:
- Webapp `PHASE3_HEADER` (older, prior session): 0.268
- `weighted_morphbpe_v3`'s own silver-audit eval of its `paper_morphbpe`
  control at vocab 6,080: 0.348
- Official `selected-candidate.json` (real validation.csv): 0.4454

These are likely three different evaluation harnesses/sets rather than a
real contradiction, but it hasn't been tracked down. **Don't cite these
numbers together in the thesis without reconciling which is which.**

---

## The webapp (`webapp/`)

A separate React + Python demo app (zero pip/npm dependencies — stdlib
`http.server` backend, no charting library on the frontend) with three
tabs: Translator, Tokenizer, Comparison. The Comparison tab was fully
reworked this project: it no longer ships a static demo showcase — it
always compares whatever text was just tokenized on the Tokenizer tab, adds
bar-chart visualizations per metric (Fertility, Boundary F1, Consistency
F1), and adds "How These Scores Are Computed" panels showing the literal
intermediate values, backed by a startup-time parity check
(`comparison_service.verify_scoring_fidelity()`) that guarantees those
diagnostics can never numerically diverge from the trusted scoring in
`reference_data.py`. Fully delivered and already committed into
`C:\Users\Gabo\kapampangan-tokenizer-pipeline\webapp\` on the local machine.

**Git note:** this folder has its own correct `.gitignore`, but the repo
root does not cleanly cover everything — there's a stray `Claude outputs/`
zip and a `demo/` folder with pycache at repo root. **Don't `git add -A` or
`git add .` from repo root** when pushing; scope adds to `webapp/`
specifically, or clean the stray root files first.

---

## The user's "reweight vocab via validation loss" idea — where it stands

The user proposed computing a cross-entropy/loss from validation
performance and using it to re-rank vocabulary/merges. Assessment: no
cross-entropy loss exists anywhere in this pipeline (all metrics are
discrete precision/recall/F1), so a literal reading doesn't map onto the
current deterministic rank-ordered BPE. But the *shape* of the idea already
exists as `weighted_bpe.py`'s crossing-penalty mechanism, and that's already
been swept across 12 configurations in `weighted_morphbpe_v3` — just scored
against a non-official silver set, with no selection step performed. The
concrete next step (no new training needed) is to run `evaluate_candidate()`
on those 12 already-trained artifacts against the real `validation.csv`,
then extend `select_candidate()`'s hierarchy to choose over `crossing_penalty`
the same way it already chooses over vocab size.

---

## Recommended next steps, roughly by effort vs. payoff

1. Score the 12 existing `weighted_morphbpe_v3` artifacts against the
   official `validation.csv` (evaluation only, no retraining needed).
2. Sweep `StochasticWeightedMorphBPETrainer` (dropout ∈ {0.0, 0.05, 0.1, 0.2}
   × a couple of known-good penalties) — new training runs, but the trainer
   is already written.
3. Reconcile more of the F-tier / low-confidence lexicon entries — data
   work, not code, and may raise the ceiling more than algorithm tweaks.
4. Build the soft-penalty + runtime-audit hybrid trainer described above —
   genuinely new code.
5. Revisit the Phase 5 NLLB fine-tuning recipe before trusting downstream
   BLEU/chrF to judge any tokenizer choice — right now every trained
   condition underperforms doing nothing.

---

## Project docs (Claude Project "Thesis Ninja Time")

If the new session has access to this Claude Project, these five docs have
the full detail behind the summaries above:

- `tokenizer-webapp-overview.md` — full webapp architecture, v1→v2 Comparison
  tab redesign.
- `tokenizer-runtime-encode-walkthrough.md` — how the shipped tokenizer
  encodes text at runtime (lexicon-free, rank-ordered merges).
- `kapampangan-pipeline-walkthrough.md` — general pipeline walkthrough.
- `tokenizer-vocab-reweighting-idea-assessment.md` — the full writeup on the
  user's reweighting idea, including the F1-discrepancy note.
- `tokenizer-training-improvement-recommendations.md` — the full writeup
  behind the "recommended next steps" section above, with more detail per
  item.
