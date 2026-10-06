# Training Lexicon Construction

## Role

The lexicon implements the paper's training-time dictionary (Chapter 3,
printed p. 42; PDF p. 45). It guides segmentation but is not part of the final
tokenizer runtime. Canonical files are:

- `resources/training-lexicon.json`
- `resources/training-lexicon-manifest.json`

Lexicon fingerprint:
`02a9886ccfeff83b710374c71a0c3dd8bd5a8a99d440621cafe1709cfb03daba`.

## Inputs

Only the following were used:

- the paper's Table 1 affix/clitic inventory;
- 2,212 rows from `data/morphology-reference.csv`;
- 806 rows from `data/linguistic-evidence.csv`; and
- neutral `train.csv` only for exact word-frequency attestation.

Training text never creates a new root. Validation and held-out test text never
participate in lexicon construction.

## Deterministic extraction

Operational root candidates must have one of four permitted reference types,
be NFC, contain at least two code points, and consist only of letters, marks,
or apostrophes. Comparison keys use NFC plus lowercase; stored/emitted surfaces
are unchanged. Explicit `compound;...` records are retained, but only forms
that are one word pretoken can be operationally protected. Paper affixes are
stored as their own typed inventory. All entries retain reference IDs, source
locators, descriptions, types, and a provisional flag.

Variation, dialect, and stress evidence is retained verbatim as evidence but
does not become a rewrite map. The supplied rows repeatedly state that
interpretation is pending linguistic review, so manufacturing a directional
mapping would be unsafe. The lexicon therefore has zero operational spelling
mappings and 187 traceable spelling-variation evidence rows.

## Counts

| Resource type | Records/elements |
| --- | ---: |
| Operational root comparison keys | 1,478 |
| Operational root surfaces | 1,494 |
| Root source records | 1,601 |
| `lemma_or_root_candidate` sources | 1,292 |
| `lexical_root_validation_candidate` sources | 222 |
| `root_or_dictionary_headword` sources | 79 |
| `root` sources | 8 |
| Root keys attested in train | 1,200 |
| Root keys not attested in train | 278 |
| Compound reference records | 26 |
| Operational one-pretoken compounds | 20 |
| Compounds attested in train | 12 |
| Spelling/variation/stress evidence | 187 (88 orthographic, 27 dialectal, 72 stress) |
| Sample inflected-form records | 118 |
| Excluded root candidates | 79 |

The paper inventory contributes 15 prefixes, 2 infixes, 1 suffix, 3
circumfixes, 9 clitics, and 3 declared `pang-` surface variants. Non-paper
affixes in reference rows are evidence only and never operational.

## Evidence status

This is a reproducible experimental lexicon, not a gold or linguist-adjudicated
lexicon. Before formal thesis reporting, native-speaker/linguist review must
validate roots, variants, compound interpretations, and boundary references.

