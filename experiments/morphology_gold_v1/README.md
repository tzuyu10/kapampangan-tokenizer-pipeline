# Morphology gold v1 (Phase 1 triage)

This isolated experiment triages the existing 650-row morphology candidate
set (`D:\Coding\thesis\datasets\kapampangan_morph_annotated_dataset.csv`,
copied byte-for-byte into `resources/`) against three mechanical, defensible
checks: lossless surface reconstruction, independent root attestation
(against `experiments/source_adjudicated_v2/resources/training-lexicon.json`
and two external lexicons, also copied into `resources/`), and whether the
claimed affix marker is inside this project's own already-modeled affix
inventory (Table 1's `src/kapampangan_morphbpe/constants.py` union v4's
documented additions). It does not touch any external source file, and it
does not modify v4 or any other existing experiment.

See `reports/morphology-triage-summary.md` for the full methodology,
results (220 strong-silver, 306 moderate-silver, 26 needs-review, 1 genuine
structural defect, 97 flagged as conflicting with this project's own
existing v2/v4 analysis or with prior page-cited reconciliation evidence),
and a documented finding that most of the remaining needs-review rows share
a real coverage gap in v4's current rule set (`pe-`, `pama-`, `pami-`
prefixes attested in this candidate data but not yet modeled by v4) -- a
candidate list for a possible future v4 rule-expansion pass, out of scope
for this triage.

A 2026-08-25 user spot-check found and corrected a real blind spot in the
original three-signal method (a claimed root can be independently attested
*and still be the wrong root for that word*, e.g. `mamangan` reusing the
attested root `mang` when this project's own v2/v4 system already accepts
`mangan`) by adding a fourth signal that cross-checks each row's exact
surface against `experiments/internet_root_reconciliation_v1/reports/word-evidence.csv`
-- this project's own prior page-cited reconciliation of the full corpus
against Forman/Bergaño/Samson/ACD/Kaikki. See the triage summary's "User
spot-check corrections" section for the full writeup.

Everything produced here is silver / AI-triaged, never independent gold.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\morphology_gold_v1\triage_morphology.py
```

Reads `resources/kapampangan_morph_annotated_dataset.csv` and the two
corroboration lexicons; writes `reports/morphology-triage.csv` and
`reports/morphology-triage-stats.json`.
