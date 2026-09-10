# Tokenizer selection v1 (Phase 3, Part 1)

Resolves the long-standing "vocab size and penalty/dropout are unselected"
blocker that every prior tokenizer experiment (v1 -> v4, the weighted grid,
the stochastic-dropout grid) left open because no genuine held-out
dev/test morphology split existed.

## What this does

1. **`build_reference.py`** carves a held-out morphology reference from
   `experiments/morphology_gold_v1/` (the Phase 1 triaged 650-row set + its
   full 97-row user adjudication):
   - Tier A/B non-function rows whose `tokenizer_target` reconstructs
     (`452` rows), plus
   - the 97 Tier F rows re-annotated with the **user's** 2026-08-25
     adjudicated analysis (the only human-verified subset): `50` auto-parsed,
     `20` monomorphemic zero-boundary "do-not-over-split" rows, `12`
     surface-mapped by hand (nasal assimilation / medial d->r / vowel
     hiatus / `-ng` ligature / reduplication fusion -- see
     `reports/tierF-mapping-decisions.csv`), `15` excluded as genuinely
     ambiguous.
   - `534` rows total, `656` gold boundaries.
   - **Label: silver + partial user adjudication -- NOT independent
     native-speaker gold.**
2. **`freeze_split.py`** freezes a 50/50 DEV/TEST split, stratified by
   (process family x has-boundary), **root-family disjoint** (0 lexical
   leakage), seed `20260828`. DEV `272` / TEST `262`.
3. **`run_selection.py`** scores all 27 trained candidates (9 conditions x
   {6080, 8192, 16384}) on DEV and TEST: type-weighted boundary P/R/F1,
   exact-segmentation match, pairwise MCF1, fertility, and a "kept-whole
   rate" for the zero-boundary rows. Selects on DEV (max boundary F1;
   tie-break exact-match, then lower fertility); confirms on TEST.

## Result

**Global winner (DEV): `penalty-8` @ vocab 6,080** -- DEV boundary F1
`0.4639`, TEST `0.4093`. Boundary F1 is monotone in the crossing penalty and
decreasing in vocab size at every condition (bigger vocab merges more
aggressively -> precision up, recall collapses). Full grid in
`reports/selection-report.md`.

**The paper-aligned hard-constrained `morphbpe` family** (the condition Phase
5 integrates with NLLB) scores `0.268` DEV / `0.15-0.17` TEST -- barely above
plain BPE and well below every weighted condition. The purely-local hard
constraint rarely changes the greedy merge outcome at inference: a
boundary-crossing merge learned from unprotected occurrences elsewhere is
still reapplied. This is expected (see the v4 `run_experiment.py` code
comment) and is the key input for the Phase 5 tokenizer-choice discussion.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\tokenizer_selection_v1\build_reference.py
.\.venv\Scripts\python.exe .\experiments\tokenizer_selection_v1\freeze_split.py
.\.venv\Scripts\python.exe .\experiments\tokenizer_selection_v1\run_selection.py
```

Deterministic: identical CSV SHA-256 and identical report numbers on every
re-run. Reads only frozen inputs (the `morphology_gold_v1` CSVs and the
already-trained `expanded_morphology_v4/artifacts/`); writes only inside
this folder; touches no existing artifact.

## `compare_segmentations.py` — qualitative retest (added 2026-09-08)

Companion to `run_selection.py` for eyeballing / native review. Runs a word
list through **all 25 candidates** (8 MorphBPE-family conditions x 3 vocab
sizes + `unigram-ablation@6080`) and lays the segmentations side by side.
Reads only frozen artifacts + the frozen reference; writes only into
`reports/segmentation-comparison/`.

```
.venv\Scripts\python.exe experiments\tokenizer_selection_v1\compare_segmentations.py
  ... --words "sumulat,misamban,kabukasan"     # ad-hoc list -> *.custom.*
  ... --all                                     # whole 534-row reference -> *.all.*
```

Outputs per run: `by-word[.tag].md` (one table per word, every candidate's
slicing + `==` exact-match vs silver gold), `wide[.tag].csv`,
`native-review[.tag].csv` (blank `correct_segmentation` / `best_version` /
`notes` columns for a native speaker), and — for the reference-backed runs —
`summary[.tag].md` (the grid re-scored on that word set, ranked by every
metric).

**What it shows (2026-09-08):** on the full 534-word silver reference,
`penalty-8@6080` still tops **F1** (0.437) and is #1–2 on exact-match, so the
Phase 3 selection holds on aggregate. But it is a **close family** —
`penalty-4@6080`, `penalty-8@8192`, `stochastic-p4-d0.1/0.2@6080` are all
within ~0.02–0.06 F1 and the sub-#1 ranking reshuffles by sample and metric.
Per word there is genuine disagreement and no candidate dominates
(`sumulat` -> `penalty-4` gets `s+um+ulat`, `penalty-8` gets `su+mu+lat`;
`misamban` -> `penalty-8` gets `mi+sam+ban`, `penalty-4` gets `mis+amban`).
The retest that settles it is a native pass on `native-review.csv`.

## Caveats

- The reference is **silver**. Tier A/B is corroborated by this project's own
  lexicon + page-cited reconciliation, not native-speaker verified; the
  folded-in Tier F rows carry the user's adjudication. Treat absolute F1 as
  this-repo-specific; the **ranking** (plain << hard-constrained <<
  weighted; penalty monotone; smaller vocab better for boundary retention)
  is the portable finding.
- The 12 hand surface-maps and 15 exclusions are documented per-row in
  `reports/tierF-mapping-decisions.csv` and were shown to the user before
  the split was frozen.
- Reduplication follows the source dataset's own convention (reduplicant
  fused with its host; only prefix/suffix boundaries scored) -- a documented
  divergence from v4's internal segment convention.
- `unigram-ablation` is **not** NLLB's tokenizer; it is a matched-vocab
  Unigram-LM control trained on this project's own corpus.
