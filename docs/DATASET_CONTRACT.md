# Dataset Contract

## Immutable source

- Package: `<DATASET_ROOT>/kapampangan-general-corpus-v1`
- Dataset name: `kapampangan-general-corpus-v1`
- Version: `1.0.0`
- Neutral corpus fingerprint:
  `aff5de7b8fc158f144eaec4af3e3c22faa3b184859925130a04604a2aa9c5d17`
- Portable ZIP expected SHA-256:
  `9f45ba35ac48147677d269870c52d9f2244ddc3fb60703011c11f640daa6186f`

The source package and ZIP are protected. This project will not edit, copy into
source control, regenerate, resplit, deduplicate, or normalize them.

## Authoritative inputs used in this goal

| Path | Records | Permitted use |
| --- | ---: | --- |
| `data/train.csv` | 26,268 | Lexicon attestation, independent morphology-aware stream, candidate and final training |
| `data/validation.csv` | 3,284 | Candidate/parameter selection and provisional development diagnostics only |
| `data/morphology-reference.csv` | 2,212 | Provisional roots, compounds, samples, and source evidence |
| `data/linguistic-evidence.csv` | 806 | Provisional evidence and unresolved variant/ambiguity documentation |
| `data/parallel-pam-tgl.csv` | 45 | Readiness audit only; never tokenizer or translation training |

`data/test.csv` has 3,284 records and is not parsed during this goal. Its bytes
may be hashed against the package checksum inventory. Optional code-switched,
PAM-ENG, translated, and derived representations are not training inputs.

## Integrity gates

- Package derived-view validator: passed for 32,836 neutral records and 11
  views. This is an integrity check only, not methodological use.
- Package dataset validator as shipped: failed during portability scan because
  `HANDOFF.md` is an extra unchecksummed file containing a prohibited label.
- Validator core against the canonical checksum inventory, excluding only that
  extra path from iteration: passed; 127 checksum files, 75 CSV files, neutral
  fingerprint and all requested counts reconciled.
- Required end gate: recompute protected ZIP/package hashes and confirm no input
  changed after training.

## Split isolation

- Training readers accept only an explicit train path and reject names/paths
  resolving to the test split.
- Evaluation readers accept only an explicit validation path during this goal.
- Manifests record each input file hash and the neutral corpus fingerprint.
- No test text is allowed in unit/regression fixtures.

## Rights and evidence status

The package is for local experimental research. Source rights were not
comprehensively verified and public redistribution clearance is not claimed.
The package is technically validated but not wholly human-validated. IDs and
sources must be retained in evidence records; no entry is called gold merely
because it is present in the package.
