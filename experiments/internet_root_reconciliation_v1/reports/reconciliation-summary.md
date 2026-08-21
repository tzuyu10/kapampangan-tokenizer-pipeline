# Internet Root Reconciliation V1

Status: evidence pass complete; no lexicon mutation or retraining performed.

## Coverage

- Distinct dataset word pretokens: **143,529**.
- Word-token occurrences represented: **1,476,145**.
- Mechanical candidate rows: **219,995**.
- Dataset fingerprint: `aff5de7b8fc158f144eaec4af3e3c22faa3b184859925130a04604a2aa9c5d17`.
- Preserved stream SHA-256: `fa1a59212353f288fe90ca205ef16a657237d89ddccd79c891987d4d91719336`.

## Word decisions

| Status | Types |
|---|---:|
| `already_analyzed` | 4,914 |
| `conflicting_exact_root_matched_hypotheses` | 117 |
| `current_rule_conflict` | 20 |
| `lexically_attested_unresolved` | 10,406 |
| `new_exact_root_matched_hypothesis` | 5,838 |
| `probable_noise_unresolved` | 7,471 |
| `unresolved_no_source_match` | 114,763 |

## Current segmenter statuses

| Status | Types |
|---|---:|
| `accepted` | 2,634 |
| `ambiguous` | 20 |
| `protected_compound` | 24 |
| `protected_root` | 2,256 |
| `unchanged` | 138,595 |

## Source indexes

| Source | Extracted forms | Unique normalized forms |
|---|---:|---:|
| `acd_v1_2` | 826 | 803 |
| `bergano1732_samson_translation` | 5,202 | 4,492 |
| `forman1971` | 3,349 | 3,199 |
| `kaikki_enwiktionary` | 1,650 | 1,366 |
| `samson2011` | 6,874 | 6,436 |
| `ucla_phonetics_archive` | 291 | 269 |

## Source links

- [Kapampangan Dictionary](https://www.jstor.org/stable/j.ctv9hvskw) - tier `A`.
- [Vocabulary of the Kapampangan Language in Spanish and Dictionary of the Spanish Language in Kapampangan](https://quod.lib.umich.edu/p/philamer/AQN8189.0001.001?view=toc) - tier `B`.
- [Kapampangan Dictionary](https://tuklas.up.edu.ph/Record/UP-99796217609955159) - tier `B`.
- [Austronesian Comparative Dictionary CLDF dataset](https://doi.org/10.5281/zenodo.7741197) - tier `B`.
- [UCLA Phonetics Lab Archive Kapampangan Word Lists](https://archive.phonetics.ucla.edu/Language/PAM/pam.html) - tier `B`.
- [Kaikki.org machine-readable Kapampangan dictionary extracted from English Wiktionary](https://kaikki.org/dictionary/Kapampangan/index.html) - tier `C`.

Forman role partition: `cross_reference_headword` 429, `root_or_stem_headword` 2,710, `unaffixable_headword` 109, `unclassified_headword` 101.

Forman is the only broadly parsed source treated as root-oriented. Bergaño counts as root evidence only when an entry explicitly says `Root`. Samson, ACD, UCLA, and Kaikki matches establish lexical attestation, not productive-root status.

## Highest-frequency new exact-root-matched hypotheses

| Frequency | Word | Mechanical rule | Reconstructed root |
|---:|---|---|---|
| 2,877 | `Suglung` | `DIRECT_ROOT` | `Suglung` |
| 1,637 | `métung` | `DIRECT_ROOT` | `métung` |
| 1,633 | `pang` | `DIRECT_ROOT` | `pang` |
| 1,280 | `sensus` | `DIRECT_ROOT` | `sensus` |
| 1,071 | `Mat` | `DIRECT_ROOT` | `Mat` |
| 1,028 | `dake` | `DIRECT_ROOT` | `dake` |
| 1,002 | `balang` | `DIRECT_ROOT` | `balang` |
| 980 | `labuad` | `DIRECT_ROOT` | `labuad` |
| 909 | `bilang` | `DIRECT_ROOT` | `bilang` |
| 695 | `lugal` | `DIRECT_ROOT` | `lugal` |
| 693 | `mas` | `DIRECT_ROOT` | `mas` |
| 654 | `y` | `DIRECT_ROOT` | `y` |
| 635 | `lub` | `DIRECT_ROOT` | `lub` |
| 618 | `mabilug` | `PREFIX_MA` | `bilug` |
| 610 | `Y` | `DIRECT_ROOT` | `Y` |
| 572 | `keraklan` | `DIRECT_ROOT` | `keraklan` |
| 566 | `palual` | `PREFIX_PA` | `lual` |
| 552 | `Juan` | `SUFFIX_AN` | `Ju` |
| 509 | `obra` | `DIRECT_ROOT` | `obra` |
| 487 | `ca` | `DIRECT_ROOT` | `ca` |

## Highest-frequency conflicts

| Frequency | Word | Supported hypotheses |
|---:|---|---|
| 305 | `misan` | `DIRECT_ROOT:misan | SUFFIX_AN:mis` |
| 132 | `masaya` | `CLITIC_YA:masa | PREFIX_MA:saya` |
| 104 | `Misan` | `DIRECT_ROOT:Misan | SUFFIX_AN:Mis` |
| 81 | `kasangkapan` | `CIRCUMFIX_KA_AN:sangkap | DIRECT_ROOT:kasangkapan` |
| 64 | `sikan` | `DIRECT_ROOT:sikan | SUFFIX_AN:sik` |
| 50 | `katasan` | `CIRCUMFIX_KA_AN:tas | PREFIX_KA:tasan` |
| 48 | `pára` | `CLITIC_RA:pá | DIRECT_ROOT:pára` |
| 45 | `Masaya` | `CLITIC_YA:Masa | PREFIX_MA:saya` |
| 45 | `Kapitan` | `DIRECT_ROOT:Kapitan | SUFFIX_AN:Kapit` |
| 32 | `ula` | `CLITIC_LA:u | DIRECT_ROOT:ula` |
| 31 | `pau` | `DIRECT_ROOT:pau | PREFIX_PA:u` |
| 25 | `kapitan` | `DIRECT_ROOT:kapitan | SUFFIX_AN:kapit` |
| 24 | `Isik` | `DIRECT_ROOT:Isik | PREFIX_I:sik` |
| 23 | `palub` | `DIRECT_ROOT:palub | PREFIX_PA:lub` |
| 20 | `upa` | `CLITIC_PA:u | DIRECT_ROOT:upa` |

## Diagnostics

- `sinulat`: current `accepted` / `INFIX_IN` -> `s + in + ulat`; decision `already_analyzed`; candidates `INFIX_IN:sulat:source_supported_root_exact`.
- `kabukasan`: current `accepted` / `CIRCUMFIX_KA_AN` -> `ka + bukas + an`; decision `already_analyzed`; candidates `CIRCUMFIX_KA_AN:bukas:source_supported_root_exact`.

## Retraining gate

1. Review every `new_exact_root_matched_hypothesis` and every conflict; a reconstructed root match does not prove that the proposed affix relationship is correct.
2. Do not promote `lexically_attested_unresolved` rows as roots. That would protect derived words and hide valid affix boundaries.
3. Freeze an adjudicated boundary list independently of the training corpus, then measure conflicts before training. The complete automatic list is not guaranteed to be globally consistent for context-free BPE merges.
4. Retrain only in a new experiment folder and compare Plain BPE, paper-aligned MorphBPE, and the boundary-safe extension on held-out morphology plus downstream translation.

## Limitations

- Exact normalized matching does not solve productive allomorphy, nasal assimilation, reduplication, dialect variation, or global historical `c/k` conversion. No global `c -> k` rewrite was used.
- ACD Kapampangan records can cite Forman, and Kaikki/Wiktionary can overlap the current lexicon; these are not always independent confirmations.
- Obvious corruption is flagged, but unmatched text is not automatically labelled non-Kapampangan.
- Richards evidence IDs `ocr-010` through `ocr-012` remained held and were not indexed.
- The full source indexes and CSVs are local research outputs; publication/redistribution rights require a separate review.
