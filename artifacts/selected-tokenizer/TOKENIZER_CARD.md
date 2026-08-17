# Kapampangan MorphBPE Tokenizer Card

Artifact fingerprint: `d3974f566756314f961a678a6bbf665a4ed3ecd2e64a82826c01950aa3e0e14e`

## Intended use

This is the independently trained, paper-defined Kapampangan source tokenizer
selected at target vocabulary size 6080. It is a technical research artifact
for local tokenizer experiments and a future controlled NLLB-200 source adapter.

## Training data

The tokenizer was trained only on the 26,268-record neutral training split from
`kapampangan-general-corpus-v1`, fingerprint
`aff5de7b8fc158f144eaec4af3e3c22faa3b184859925130a04604a2aa9c5d17`. Validation selected the vocabulary size using provisional
proxy morphology diagnostics. Held-out test text was not used.

## Runtime

Runtime uses NFC normalization, deterministic Unicode pre-tokenization, this
artifact's vocabulary and merge precedence, and character/`<unk>` fallback. It
does not load a lexicon, corpus, morphology reference, or training segmentation.

## Limitations

Morphology resources were not human-validated under the thesis methodology.
Development morphology scores are proxies, not final thesis results. Formal
held-out evaluation and NLLB translation evaluation remain pending.
