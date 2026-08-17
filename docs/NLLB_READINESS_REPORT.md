# NLLB and Parallel-data Readiness Report

Status: **not ready for NLLB fine-tuning**. This does not block tokenizer
training or technical artifact use.

## Reproducible 45-row audit

`reports/parallel-readiness-audit.json` was generated from
`data/parallel-pam-tgl.csv` plus metadata only. Neutral IDs were recomputed as
documented (`kgc-` plus the first 24 SHA-256 hex characters of NFC source text)
and joined to `metadata/split-manifest.csv`. `data/test.csv` was never parsed.

| Finding | Result |
| --- | ---: |
| Rows / unique pair IDs | 45 / 45 |
| Unique PAM sources | 37 |
| Repeated PAM-source rows beyond first | 8 |
| Unique targets | 41 |
| Repeated target rows beyond first | 4 |
| Nonempty, NFC pairs | 45 / 45 |
| Neutral source assignment: train | 14 |
| Neutral source assignment: validation | 0 |
| Neutral source assignment: test | 30 |
| Neutral source assignment: unassigned | 1 |
| Source document keys | 6 |
| Mapped rows marked OCR-derived | 29 |

All mapped provenance uses source key `pdf-parallel`. The portable parallel
table does not encode human-readable semantic domains; only six opaque PDF work
keys are available. Assigning topics from fragments would be fabrication.

## `tgl` is not silently relabeled Filipino

All 45 rows use target label `tgl`, i.e. the package's Tagalog label. The
paper requires Filipino. The dataset contract contains no adjudication proving
that these targets operationalize the paper's Filipino condition. They are
therefore documented as Tagalog-labeled data, not silently asserted to be
Filipino references.

## Technical usability and smoke-test decision

The CSV schema is technically readable and rows are nonempty. They are not
adequate for even the controlled translation smoke fixture in this project:

- 45 is far below approximately 13,000 aligned pairs;
- no validation-aligned source is available;
- 30 rows reveal overlap with neutral held-out assignments;
- eight PAM sources repeat;
- 29 mapped rows are OCR-derived; and
- translation and language quality are not human-validated.

Using them would risk test contamination and would imply unsupported target
quality. None were used for tokenizer training, fixtures, validation, model
download, translation metrics, or NLLB fine-tuning. PAM-ENG was not substituted
and no targets were fabricated or machine-translated.

## Paper requirement verdict

The paper expects approximately **13,000 Kapampangan-Filipino pairs** and
**1,300 aligned test sentences**. Available evidence is 45 Tagalog-labeled
pairs with no parallel split. The requirement is **not satisfied**.

Before NLLB work: acquire/clear and human-review the needed PAM-Filipino data,
create leakage-safe aligned splits with a sealed test, resolve the source
embedding integration gate, and freeze identical baseline/adapted controls.

