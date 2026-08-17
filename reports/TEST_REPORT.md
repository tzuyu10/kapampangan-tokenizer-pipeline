# Validation and Test Report

## Automated implementation checks

- Python: 26 unit/property/integration tests passed.
- Rust: 2 unit tests passed; doc-test suite passed with no failures.
- Full Python/Rust corpus parity: 154,446/154,446 exact word-type outputs.
- Ruff lint: all `src`, `runtime`, `tests`, and `scripts` checks passed.
- Ruff format: all 31 Python files are canonically formatted.
- Mypy strict: all 23 source/runtime modules passed.
- Artifact: 8 non-checksum files verified; reload succeeded; vocabulary 6,080.
- Determinism: two final builds, nine files each, byte-identical.
- Clean runtime: passed without dataset or lexicon; `<unk>` fallback ID 1.
- Notebook: JSON syntax and code-cell compilation passed.

Tests cover empty/whitespace/punctuation/NFC/accents/`ñ`, roots, compounds,
prefixes, infixes, suffix, circumfixes, clitics, `pang-` variants, overlaps,
ambiguity, root-internal false splitting, unseen forms/characters, deterministic
pair ties, protected merges, corruption/malformed artifacts, clean runtime,
future adapter padding/truncation, CLI encode/decode, and held-out path rejection.

## Dataset checks

Required dataset name/version/fingerprint/counts and required file hashes
matched. ZIP SHA-256 matched. The source `test.csv` was checksum-verified only;
the project reader refuses the test role/path. Final package verification is in
`reports/dataset-verification-final.json`.

The package's own derived-view validator passed. Its full validator's canonical
127-file core passed after excluding only extra, unchecksummed `HANDOFF.md` from
file iteration; the package was not modified. See `docs/DATASET_CONTRACT.md`.

## Formal held-out test status

**Not executed.** No held-out Fertility Rate, MBF1, MCF1, morphological
distance, native-NLLB baseline, BLEU, chrF++, confidence interval, p-value, or
effect size is reported here. The manifest count 3,284 and checksum are
integrity metadata, not test observations.

Formal evaluation remains blocked on linguist-adjudicated boundaries,
rights-reviewed PAM-Filipino parallel data, frozen baseline/adapted controls,
and an approved sealed-test procedure.
