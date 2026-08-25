# Translation gold v1 (Phase 1 triage)

This isolated experiment triages the existing 250-row PAM-FIL MT candidate
set (`D:\Coding\thesis\curated_research_dataset\kapampangan_mt_pld_pam_fil_curated.csv`,
copied byte-for-byte into `resources/`) against a documented, stated 0-3
rubric applied by direct reading of every row, not a single opaque
pass/fail judgment. It does not touch the external source file, and it does
not attempt real alignment/reconstruction of the misaligned pairs it finds
evidence of -- that is scoped separately as Phase 2 (a real
extraction/alignment pipeline against the raw PLD archive).

See `reports/mt-pair-triage-summary.md` for the full methodology, results
(11/250 rows confirmed correct translations, 11/250 plausible partial
matches, 9 dictionary-gloss entries that are not translation pairs, the
rest confirming the known cross-matching failure mode), and a documented
finding that several later blocks show evidence of shifted/shuffled
alignment (a real, recoverable correct pair exists at a *different* row
than where either half of it is currently attached) -- concrete, actionable
context for Phase 2's alignment methodology.

Everything produced here is silver / AI-triaged, never independent gold.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\translation_gold_v1\triage_mt_pairs.py
```

Reads `resources/kapampangan_mt_pld_pam_fil_curated.csv` and
`reports/mt-pair-rubric-scores.tsv` (the hand-scored rubric, one row per
candidate); writes `reports/mt-pair-triage.csv` and
`reports/mt-pair-triage-stats.json`.
