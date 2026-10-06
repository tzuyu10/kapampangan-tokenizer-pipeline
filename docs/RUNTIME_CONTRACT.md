# Standalone Runtime Contract

## Inputs and dependencies

`kapampangan_morphbpe_runtime.Tokenizer(artifact_dir)` accepts only the selected
artifact directory. It uses the Python standard library and reads only the
artifact checksum inventory plus `tokenizer.json`. It has no corpus, root,
affix, clitic, morphology-reference, linguistic-evidence, or prepared-stream
API.

## Load-time validation

The loader requires schema `1.0.0`, artifact type
`kapampangan_morphbpe`, the exact NFC-only normalization contract, a contiguous
unique vocabulary, ordered unique merge pairs, reconstructing merge results,
all four special roles, and a complete safe-path SHA-256 inventory. Missing,
extra, malformed, or changed files are rejected before encoding.

## Encoding algorithm

1. Require a Unicode string and normalize it to NFC.
2. Apply the frozen pretoken state machine.
3. For each pretoken, first emit it whole if its exact surface is a non-special
   vocabulary entry.
4. Otherwise initialize known characters and `<unk>` units.
5. Repeatedly choose the available pair with lowest learned merge rank and
   apply all nonoverlapping occurrences left-to-right.
6. Emit stable token strings, integer IDs, pretoken kind, vocabulary kind, and
   half-open normalized code-point offsets.
7. Optionally add zero-width BOS/EOS tokens.

This is standard learned-rule runtime behavior; morphological boundaries and
the training lexicon are deliberately unavailable.

## Special and fallback policy

| Role | Token | ID | Behavior |
| --- | --- | ---: | --- |
| Padding | `<pad>` | 0 | Adapter-only right padding; mask 0 |
| Unknown | `<unk>` | 1 | One token per unseen Unicode code point; decode U+FFFD |
| Beginning | `<s>` | 2 | Opt-in zero-width token |
| End | `</s>` | 3 | Opt-in zero-width token |

Observed training characters remain ordinary character vocabulary entries.
Unknown fallback was verified with unassigned U+10FFFF, producing ID 1.

## Decoding and offsets

Decoding concatenates non-special token surfaces in ID order. BOS, EOS, and
padding are skipped by default. `<unk>` decodes to U+FFFD because the unknown
source code point is not stored in an ID sequence. For known characters,
`decode(encode(text).ids)` equals NFC-normalized input, including whitespace and
punctuation. Offsets index normalized input; callers needing original-input
indices must retain their own normalization alignment.

## Clean-room proof

The release gate copied only `runtime/kapampangan_morphbpe_runtime/` and
`artifacts/selected-tokenizer/` to an isolated temporary directory. Dataset and
lexicon environment paths pointed to nonexistent sentinels. Empty, accented,
`ñ`, infix-like, punctuation, and repeated-whitespace examples round-tripped;
the unknown fallback used ID 1. The report fingerprint is
`e2461110afd54edf0bf36565548fa2b257a32911b3bf87f690c07c63e4543a82`.

