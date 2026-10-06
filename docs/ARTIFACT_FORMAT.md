# Tokenizer Artifact Format

## Version and canonical serialization

The artifact is an `implementation_defined` portable schema, version `1.0.0`.
JSON uses UTF-8, LF, sorted keys, two-space indentation, and one final newline.
Core outputs contain no timestamps or absolute local paths.

## Files

| File | Contract |
| --- | --- |
| `tokenizer.json` | Self-contained normalization, pretokenizer, specials, typed vocabulary, ordered merges, and provenance metadata |
| `vocab.json` | Contiguous ID-ordered entries `{id, token, kind}` and target/actual size |
| `merges.json` | Rank-ordered `{rank,left,right,result,result_id}` rules |
| `normalization.json` | NFC and empty spelling-map declaration |
| `pretokenizer.json` | Unicode categories, internal joiners, whitespace/punctuation preservation, offset unit |
| `special_tokens.json` | Token/ID/role mapping |
| `tokenizer-manifest.json` | Schema/type, dataset fingerprint, metadata, sizes, core hashes, artifact fingerprint |
| `TOKENIZER_CARD.md` | Intended use, training data, runtime boundary, and limitations |
| `checksums.sha256` | SHA-256 for every other file, sorted by relative POSIX path |

## Vocabulary kinds and IDs

Entries are `special`, `character`, or `merge`. IDs are fixed specials first,
training characters sorted by UTF-8 bytes, then new merge surfaces in learned
order. The selected artifact has 6,080 entries and 4,488 merge rules.

## Fingerprints

The artifact fingerprint hashes the canonical manifest body, including all
core-file SHA-256 values and provenance metadata. The selected fingerprint is
`d3974f566756314f961a678a6bbf665a4ed3ecd2e64a82826c01950aa3e0e14e`.
The checksum inventory additionally covers the manifest and tokenizer card.

Training resources are referenced only by immutable fingerprints in metadata;
they are not embedded. The artifact remains loadable when all training
resources are absent.

## Compatibility and failure behavior

Consumers must reject unsupported schema versions, unexpected type, checksum
set/hash mismatches, unsafe checksum paths, duplicate tokens, noncontiguous IDs,
missing special roles, malformed/duplicate merge pairs, nonreconstructing merge
results, or merge results absent from the vocabulary. Schema changes require a
new version; silent coercion is forbidden.

