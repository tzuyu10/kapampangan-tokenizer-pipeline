# Constrained Morph-BPE Training

## Paper-mandated behavior

Chapter 2 (printed pp. 20-21; PDF pp. 23-24) and Chapter 3 (printed
pp. 42-43; PDF pp. 45-46) require character initialization, repeated
most-frequent adjacent-pair merging, and protection of morphological
boundaries. This implementation does not use byte initialization, an external
pretrained tokenizer, or an unconstrained BPE library.

## Prepared stream

The Rust segmenter processed only the 26,268 neutral training records. Exact
`(surface, protected-boundary tuple, pretoken kind)` sequences are aggregated
with integer frequency and serialized deterministically in
`runs/prepared/training-stream.jsonl`.

| Training inventory | Value |
| --- | ---: |
| Normalized code points | 9,270,406 |
| Pretoken occurrences | 3,182,053 |
| Word occurrences | 1,476,145 |
| Word types | 143,529 |
| Unique prepared sequences | 143,665 |
| Character types | 1,588 |
| Fixed special tokens | 4 |
| Initial vocabulary | 1,592 |
| Initial permitted pair types | 7,728 |
| Character-adjacency merge upper bound | 967,122 |

The broad 1,588-character inventory reflects the immutable corpus's
multiscript/OCR material; it was neither filtered nor normalized away.

## Deterministic trainer

1. IDs 0-3 are the fixed special tokens.
2. Observed characters are sorted by UTF-8 bytes and assigned subsequent IDs.
3. A pair is counted only if its joining position is not protected.
4. Pair frequency is occurrence count times aggregated sequence frequency.
5. Highest frequency wins; ties use `(left UTF-8 bytes, right UTF-8 bytes)`.
6. The selected pair is applied left-to-right to every affected sequence.
7. Every proposed span is checked again against protected offsets.
8. A new surface receives the next ID; merge precedence is append order.
9. Training stops at the target or when no permitted pair remains.

An incremental pair-to-sequence index updates only affected sequences. The
stored report records requested/trained targets, merge counts, termination
reason, model fingerprints, and protected-boundary violations.

## Candidate family and final rebuild

Frozen targets were 1,656, 3,008, and 6,080. They learned 64, 1,416, and 4,488
merge rules respectively; all reached their target with zero training
protected-boundary merge violations. Validation selected 6,080. Finalization
retrained that target twice from the same train-only stream. Both artifacts had
fingerprint
`d3974f566756314f961a678a6bbf665a4ed3ecd2e64a82826c01950aa3e0e14e`
and all nine artifact files were byte-identical.

## Important boundary interpretation

The zero invariant applies to boundaries explicitly protected in the training
stream. At runtime no lexicon is available; proxy boundaries on unseen
validation forms can therefore be missed. Those misses are reported as
validation proxy crossings and morphological distance rather than falsely
claimed as violations of the constrained training algorithm.

