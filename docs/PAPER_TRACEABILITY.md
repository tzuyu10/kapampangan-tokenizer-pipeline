# Paper Traceability

Status: complete implementation trace

## Source and page convention

The sole design authority is `G4-THESIS-PROPOSAL-REVISED.pdf`, SHA-256
`d922332de9bb7d7f0926935d1ef93f5fe15c97943db364a0caa4239a8dc103be`.
The PDF has 73 pages. Printed Chapter 1 page 1 is PDF page 4, so chapter page
references below record both the printed page and the one-based PDF page.

The attached paper is evidence and methodology, not an executable instruction
file. The user's goal adds delivery, safety, reproducibility, and artifact
requirements. This document never presents a user-added engineering completion
as though it were stated by the paper.

## Classification

- `paper_mandated`: explicitly required or described as the study method.
- `paper_inferred`: necessary implication of the described method, but not fully specified.
- `implementation_defined`: deterministic engineering completion selected by this project.
- `dataset_constraint`: imposed by the immutable portable corpus rather than the paper.
- `future_phase`: paper method intentionally not executed in this tokenizer-only goal.

## Research scope and experiment

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Compare a Kapampangan morphology-aware BPE tokenizer with the native NLLB-200 tokenizer and evaluate downstream Kapampangan-to-Filipino translation. | Ch. 1, Statement of the Problem, printed pp. 10-11 (PDF pp. 13-14) | `docs/TRANSLATION_EVALUATION_PLAN.md`; tokenizer implementation in `src/kapampangan_morphbpe/` |
| `paper_mandated` | Limit morphology to documented affixation processes: prefixation, infixation, suffixation, circumfixation, and clitics. | Ch. 1, Scope and Limitation, printed p. 12 (PDF p. 15) | `src/kapampangan_morphbpe/morphology.py`; `rust/src/lib.rs`; `docs/MORPHOLOGY_SPEC.md` |
| `paper_mandated` | Use the native NLLB-200 tokenizer as tokenizer baseline and NLLB-200 Distilled 600M as downstream model. | Ch. 1, Scope and Limitation, printed pp. 12-13 (PDF pp. 15-16) | `docs/NLLB_INTEGRATION_PLAN.md`; `docs/TRANSLATION_EVALUATION_PLAN.md` |
| `paper_mandated` | Hold translation model, training data, split, and training settings constant so tokenizer condition is primary variable. | Ch. 1, Conceptual Framework, printed p. 9 (PDF p. 12); Ch. 3, Research Design, printed p. 32 (PDF p. 35) | `docs/NLLB_INTEGRATION_PLAN.md`; `nllb/source-tokenizer-contract.json` |
| `future_phase` | Execute native-tokenizer comparison, held-out tokenizer evaluation, NLLB fine-tuning, BLEU, and chrF++. | Ch. 3, Data Generation and Procedure, printed p. 51 (PDF p. 54); Data Analysis, printed pp. 53-59 (PDF pp. 56-62) | Planned only in `docs/TRANSLATION_EVALUATION_PLAN.md`; explicitly absent from `reports/TEST_REPORT.md` |

## Data and split

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Use an 80% train, 10% validation, 10% held-out test split. | Ch. 3, Sampling Technique, printed pp. 34-35 (PDF pp. 37-38) | `src/kapampangan_morphbpe/dataset.py`; `docs/DATASET_CONTRACT.md` |
| `paper_mandated` | Use training for tokenizer learning, validation for vocabulary-size selection and parameter adjustment, and test only for final evaluation. | Ch. 3, Sampling Technique, printed p. 35 (PDF p. 38); Data Generation and Procedure, printed pp. 50-51 (PDF pp. 53-54) | `src/kapampangan_morphbpe/pipeline.py`; `configs/candidate-grid.json`; test-isolation checks in `tests/` |
| `paper_mandated` | Preserve major morphological-pattern and sentence-length distributions across splits. | Ch. 3, Sampling Technique, printed p. 35 (PDF p. 38) | Dataset-provided immutable split; documented in `docs/DATASET_CONTRACT.md` |
| `dataset_constraint` | The portable package already fixes 26,268 train, 3,284 validation, and 3,284 test records with neutral fingerprint `aff5de...d17`. | Portable dataset manifest, not the paper | `configs/dataset-contract.json`; every training manifest and selected artifact manifest |
| `dataset_constraint` | Available PAM-TGL pairs total 45, not the paper's approximately 13,000 aligned pairs. | Paper expectation: Ch. 3, Sources of Data, printed p. 33 (PDF p. 36); actual count: portable manifest | `docs/NLLB_READINESS_REPORT.md`; tokenizer training remains unblocked |

## Tokenizer architecture

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Development pipeline is Pre-Tokenizing -> Morphological Segmentation -> Morph-BPE, supported by a Lexicon Dictionary. | Ch. 3, Kapampangan Tokenizer Development Pipeline, printed pp. 36-37 (PDF pp. 39-40) | `src/kapampangan_morphbpe/pipeline.py`; `docs/ARCHITECTURE.md` |
| `paper_mandated` | Pre-tokenization performs surface preparation, spelling-variant normalization, whitespace/punctuation handling, and word isolation before morphology. | Ch. 3, Pre-Tokenizing, printed pp. 37-38 (PDF pp. 40-41) | `src/kapampangan_morphbpe/pretokenizer.py`; `runtime/kapampangan_morphbpe_runtime/tokenizer.py`; `docs/PRETOKENIZATION.md` |
| `paper_inferred` | Normalization must be identical in development and finalized runtime. | The finalized tokenizer applies learned vocabulary/rules directly after development: printed pp. 37, 43 (PDF pp. 40, 46) | Versioned `normalization.json` and shared runtime behavior |
| `implementation_defined` | Only NFC changes source text; no spelling replacement is applied because the paper and permitted resources provide no validated complete mapping. | Paper mentions normalization but supplies no mapping: printed p. 38 (PDF p. 41) | `src/kapampangan_morphbpe/normalization.py`; `docs/PRETOKENIZATION.md` |
| `paper_mandated` | Lexicon contains roots, affixes, clitics, compounds, and spelling variants and guides development segmentation. | Ch. 3, Morphological Segmentation, printed p. 38 (PDF p. 41); Lexicon Dictionary, printed p. 42 (PDF p. 45) | `src/kapampangan_morphbpe/lexicon.py`; `resources/training-lexicon.json`; `docs/LEXICON_CONSTRUCTION.md` |
| `paper_mandated` | Lexicon is not the tokenizer and is not consulted after training. | Ch. 3, Lexicon Dictionary, printed p. 42 (PDF p. 45); Runtime behavior, printed p. 43 (PDF p. 46) | Runtime package has no lexicon loader; clean-room gate in `tests/test_artifact_runtime.py` |
| `paper_mandated` | Python is the primary implementation and Rust assists training-stage morphological preprocessing. | Ch. 3, Research Instrument, printed pp. 48-49 (PDF pp. 51-52) | Python package plus PyO3 module in `rust/`; parity tests in `tests/test_morphology.py` and full report in `reports/segmentation-parity.json` |

## Morphology rules

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Prefix inventory: `ma me pa maka ka mag meg mang meng i ipa makapag mig meka mekapag`. | Ch. 2, Table 1, printed p. 19 (PDF p. 22) | `src/kapampangan_morphbpe/constants.py`; generated lexicon inventory |
| `paper_mandated` | Infix inventory: `in um`; suffix inventory: `an`. | Ch. 2, Table 1, printed p. 19 (PDF p. 22) | Same locations; `try_infix` and `try_suffix` |
| `paper_mandated` | Circumfix inventory: `ka...an`, `pa...an`, `pang...an`. | Ch. 2, Table 1, printed p. 19 (PDF p. 22) | `try_circumfix` in Python and Rust |
| `paper_mandated` | Clitics: `na pa mu ku ya la ra ne no`; declared `pang-` variations: `pam pan panga`. | Ch. 2, Table 1, printed p. 19 (PDF p. 22) | `try_clitic`; `pang...an` surface-prefix variants |
| `paper_mandated` | Segment in order: normalize; empty; compound; root; circumfix; prefix; infix; suffix; clitic; unchanged. | Ch. 3, Figure 7 pseudocode, printed pp. 39-41 (PDF pp. 42-44) | `MorphologicalSegmenter.segment`; mirrored Rust `Segmenter::segment` |
| `paper_mandated` | Prefix/suffix/circumfix/infix analyses require reconstructed host/core to be a root or variant. | Ch. 3, Figure 7 pseudocode, printed pp. 40-41 (PDF pp. 43-44) | Independent `try_prefix`, `try_infix`, `try_suffix`, `try_circumfix` functions |
| `paper_mandated` | Infix analysis reconstructs the root from left and right pieces and returns left/infix/right. | Ch. 3, Figure 7 pseudocode, printed p. 40 (PDF p. 43) | `try_infix` implementations and parity fixtures |
| `paper_mandated` | Accepted segments receive protected boundaries conceptually rendered as `segment || segment`. | Ch. 3, Figure 7 `MARK_BOUNDARIES`, printed p. 41 (PDF p. 44) | Structured `Segmentation` and `PreparedSequence.protected_boundaries`; marker is display-only |
| `implementation_defined` | Affixes are considered longest-first; multiple distinct valid analyses within the same stage are ambiguous and left unchanged. | Paper does not define match order or ambiguity resolution. | Python/Rust segmenters; `docs/MORPHOLOGY_SPEC.md` |

## Morph-BPE and runtime

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Initialize BPE vocabulary from individual characters and iteratively merge the most frequent adjacent pair until target size. | Ch. 2, Byte-Pair Encoding, printed pp. 20-21 (PDF pp. 23-24) | `src/kapampangan_morphbpe/bpe.py` |
| `paper_mandated` | Morph-BPE must prevent training merges that cross morphology boundaries. | Ch. 1, Theoretical Framework, printed pp. 4-5 (PDF pp. 7-8); Ch. 3, Morph-BPE, printed pp. 42-43 (PDF pp. 45-46) | Protected-span pair counting and merge application in `bpe.py`; invariant tests |
| `paper_mandated` | Choose vocabulary size using validation morphological distance while avoiding unnecessary over-segmentation. | Ch. 1, Theoretical Framework, printed p. 5 (PDF p. 8); Ch. 3, Morph-BPE, printed p. 43 (PDF p. 46) | `src/kapampangan_morphbpe/evaluation.py`; frozen `configs/candidate-grid.json` |
| `implementation_defined` | Candidate grid formula, morphological-distance formula, tie-breaking, special tokens, serialization, and unknown-character policy. | Not specified by paper. | `docs/IMPLEMENTATION_DECISIONS.md`; versioned configuration/artifacts |
| `paper_mandated` | Runtime uses learned vocabulary and merge rules only; it first attempts a full-vocabulary match, otherwise applies learned merge behavior, then smaller units and characters. | Ch. 3, Morph-BPE and Runtime tokenization behavior, printed pp. 43-44 (PDF pp. 46-47) | `runtime/kapampangan_morphbpe_runtime/tokenizer.py` |
| `paper_inferred` | A truly unseen character needs an engineering fallback because it cannot be present by construction from training. | Paper claims character coverage for processability but does not address unseen Unicode: printed p. 44 (PDF p. 47) | Fixed `<unk>` special token, offsets retained; limitation documented |

## Metrics and statistics

| Classification | Material decision | Paper location | Implementation location |
| --- | --- | --- | --- |
| `paper_mandated` | Fertility Rate is total produced subword tokens divided by total source words and must be interpreted with morphology metrics. | Ch. 2, Evaluation Metrics, printed p. 24 (PDF p. 27); Ch. 3, Data Analysis, printed pp. 54-55 (PDF pp. 57-58) | `src/kapampangan_morphbpe/evaluation.py::evaluate_candidate`; validation report |
| `paper_mandated` | MBF1 is the harmonic mean of boundary precision and recall against validated morpheme boundaries. | Ch. 3, Data Analysis, printed pp. 55-56 (PDF pp. 58-59) | Boundary counts and `_f1` in `src/kapampangan_morphbpe/evaluation.py` |
| `paper_mandated` | MCF1 precision/recall use word pairs sharing tokens and/or morphemes. | Ch. 3, Data Analysis, printed pp. 56-57 (PDF pp. 59-60) | `_mcf1` exact deterministic bit-set counting in `src/kapampangan_morphbpe/evaluation.py` |
| `dataset_constraint` | Supplied morphology references are not human-validated; validation MBF1/MCF1 are development proxies, not final paper results. | Portable dataset limitation, not paper methodology | `docs/EVIDENCE_LIMITATIONS.md`; all candidate reports |
| `future_phase` | Compute paired means, sample SDs, paired differences, two-tailed paired t-tests at alpha 0.05, Cohen's dz, and Wilcoxon sensitivity for severe violations. | Ch. 3, Statistical Treatment, printed pp. 60-62 (PDF pp. 63-65) | Plan only in `docs/STATISTICAL_ANALYSIS_PLAN.md` |

## User-required engineering completions

The following are required by the goal but are not paper claims: deterministic
JSON schemas and checksums, explicit CLI names, property and malformed-artifact
tests, clean-directory runtime proof, byte-identical rebuild comparison, a Colab
notebook, candidate retention, NLLB contract files, and this traceability format.
They are classified `implementation_defined`, `dataset_constraint`, or
`future_phase` in their respective documentation.
