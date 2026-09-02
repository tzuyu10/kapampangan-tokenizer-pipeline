# Parallel extraction v2 — PLD full-pool alignment

A **second pass** over the parsed PLD `.log` data. `parallel_extraction_v1`
aligned from the 1,924-row *canonical inventory*, which collapsed each
`(file, ordinal)` elicitation slot to one representative. But `prompt_ordinal`
was randomised per speaker, so that collapse discarded most of the content —
the raw parse (`resources/pld_prompt_entries_pam_fil.csv`, copied byte-for-byte
with a SHA-256 provenance manifest) actually holds **~4,700 distinct PAM /
~4,200 distinct FIL sentences**.

This experiment rebuilds the full distinct-sentence pools and runs a
candidate-alignment sweep over them, for human review — exactly the
`parallel_extraction_v1` discipline: **nothing here is a verified pair, and
nothing enters a dataset until the user reviews it.**

`parallel_extraction_v1` is left byte-unchanged; this is additive.

## Pipeline

```powershell
# 1. distinct sentence/phrase pools per shared-name file (pure stdlib)
.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v2\build_pools.py

# 2. LaBSE + lexical candidate sweep  (needs the global-Python install:
#    sentence-transformers / torch-cpu — see AGENT_CONTEXT.md 2026-08-31)
python .\experiments\parallel_extraction_v2\align_candidates.py

# 3. adjudicate the reviewed candidates into a tiered pair set (pure stdlib)
.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v2\adjudicate.py
```

- `adjudicate.py` reads `resources/user-evaluated-candidates-2026-09-01.csv`
  (the sweep + the user's automated dictionary-alignment verdicts —
  **not** a native-speaker review) and merges with the v1 gold →
  `data/verified-pairs.csv`: **545 pairs = 220 `gold_v1` + 232 `silver_a` +
  93 `silver_b`**. `silver_*` is adjudicated by three non-native passes
  (LaBSE+MNN, the dictionary script, a Claude read-through) — usable for
  Phase 5 fine-tuning **as silver**, needs native-speaker validation before
  any gold claim.

- `build_pools.py` → `data/sentence-pools.json`, `reports/pool-summary.csv`,
  `reports/pools-manifest.json`. 15 alignment units, 1,606 PAM / 1,725 FIL.
- `align_candidates.py` → `data/candidate-pairs.csv` (reviewer-ready, blank
  `reviewer_verdict` / `reviewer_notes`), `reports/alignment-summary.md`,
  `reports/alignment-stats.json`. Signals per candidate: `emb_cosine`
  (LaBSE), `token_jaccard`, `char3_cosine`, `length_ratio`, `mutual_best`
  (reciprocal nearest neighbour — the high-precision subset), `blended_score`.

## Caveats

- `prompt_text` is the elicitation prompt each speaker was asked to produce,
  **not a spoken transcription**. The WAV audio is not used (Whisper has no
  Kapampangan model).
- LaBSE was not trained on Kapampangan; it works here only because of heavy
  Kapampangan↔Tagalog surface-vocab overlap. Every candidate needs a human
  to confirm it is a real translation, not a same-topic near-neighbour.
- PLD redistribution rights are unresolved → local research use only. The
  copied source CSV and the `data/` outputs are `-text` in `.gitattributes`.
- Many shared-name files are independently authored per language
  (`parallel_extraction_v1` established this from samples); the sweep exists
  to find the translated *subset* a sample would miss, so a low accept rate
  per unit is expected and fine.
