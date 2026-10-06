# Tokenizer Training Report

Status: complete for tokenizer training; formal held-out evaluation pending.

## Immutable inputs

- Dataset: `kapampangan-general-corpus-v1` version 1.0.0
- Corpus fingerprint:
  `aff5de7b8fc158f144eaec4af3e3c22faa3b184859925130a04604a2aa9c5d17`
- ZIP SHA-256:
  `9f45ba35ac48147677d269870c52d9f2244ddc3fb60703011c11f640daa6186f`
- Train: 26,268 records; SHA-256
  `2309d439133c73b183a45954adfc8c54d36b8824b0cd2899631415497f6d4d2d`
- Validation: 3,284 records; selection only
- Test: 3,284 records from manifest; content not parsed; checksum only

The input package remained external and read-only. No existing tokenizer
project source, schema, configuration, vocabulary, Rust code, tests, artifact,
or environment was imported.

## Lexicon and morphology

Lexicon fingerprint:
`02a9886ccfeff83b710374c71a0c3dd8bd5a8a99d440621cafe1709cfb03daba`.
It contains 1,478 operational root keys (1,494 surfaces), 20 operational
one-pretoken compounds, the paper's 15/2/1/3/9 affix/circumfix/clitic inventory,
187 retained nonoperational spelling-variation evidence rows, and 118 sample
inflected-form records. Full resource-type counts are in
`docs/LEXICON_CONSTRUCTION.md`.

Python/Rust full gate: 29,552 train/validation records scanned, 154,446 word
types compared, 154,446 exact matches, zero discrepancies. The Rust output was
used for the actual training stream.

Training morphology occurrences: 41,923 accepted multi-segment, 91 ambiguous
unchanged, 488,967 protected root, 5,781 protected compound, and 939,383
unchanged. Accepted segmentation coverage is 0.028400326526188145 of 1,476,145
word occurrences.

## Prepared inventory and frozen grid

- 143,529 training word types
- 143,665 unique prepared sequences
- 1,588 observed characters + 4 specials = 1,592 initial vocabulary
- 7,728 initial permitted pair types
- 967,122 character-adjacency feasible-merge upper bound
- Prepared stream SHA-256:
  `509d6d518737400f4658c268b4dcd3af4ca59b03a7b571551ffe704694b2c765`
- Frozen targets: 1,656, 3,008, 6,080
- Grid fingerprint:
  `5f098d5b92dc2428a7324783df0413536ff29c3896702b4971f90cf6c2194d0b`

## Candidate training

| Target/actual vocab | Merge rules | Protected-boundary violations | Artifact fingerprint |
| ---: | ---: | ---: | --- |
| 1,656 | 64 | 0 | `fb0e20e68584a00ae5fd94d7c0fa0eefb6ebafc8ac85d7d2c721e06133b8c8a3` |
| 3,008 | 1,416 | 0 | `81dbb64efe175750c4d6d0647666fbb89f710e9b6c091d21e29e8151bb8a3d2f` |
| 6,080 | 4,488 | 0 | `0b20503d668b762c5f9ad66921bb06da562e12c04c34bdf771f9a648a66c145b` |

All candidates reached their exact target. Candidate artifacts remain under
`artifacts/candidates/`.

## Finalization

Validation selected target 6,080. Final training used the unchanged train-only
prepared stream; validation was not absorbed. Two from-scratch builds produced
nine byte-identical files. Both final fingerprints are
`d3974f566756314f961a678a6bbf665a4ed3ecd2e64a82826c01950aa3e0e14e`.
The selected artifact has 6,080 tokens, 4,488 merges, specials `<pad>` 0,
`<unk>` 1, `<s>` 2, `</s>` 3, and zero protected-boundary training violations.

Runtime validation passed with only the standalone runtime and artifact;
dataset/lexicon sentinel paths were denied. Checksums and reload passed. No
NLLB model or held-out evaluation was run.

