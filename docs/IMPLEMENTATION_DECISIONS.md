# Implementation Decisions

Status: frozen before candidate validation unless a recorded defect requires a
versioned correction.

## D-001: Deterministic serialization

- Classification: `implementation_defined`
- Decision: UTF-8, LF endings, sorted object keys, two-space JSON indentation,
  one terminal newline, no timestamps in core artifacts.
- Reason: the paper requires a learned vocabulary/rule artifact but supplies no
  schema. Canonical serialization enables byte-identical rebuilds.

## D-002: Normalization

- Classification: `implementation_defined`
- Decision: normalize raw input to Unicode NFC only. Do not lowercase, strip
  accents, modernize spelling, normalize dialect, stem, lemmatize, or apply a
  spelling-replacement table.
- Reason: the paper mentions spelling-variant normalization but defines no
  complete mapping. The permitted resources contain provisional evidence, not
  a validated directional mapping. Exact root matching may use a lowercase
  comparison key without changing emitted text.

## D-003: Pre-token boundaries and offsets

- Classification: `implementation_defined`
- Decision: scan normalized Unicode by code point. Word units are runs of
  letters, combining marks, and numbers; apostrophes and hyphens remain inside
  a word only when flanked by word characters. Whitespace runs, punctuation,
  and symbols remain explicit pretokens so encoding can preserve exact
  normalized-input offsets and decoding can reconstruct normalized text.
- Reason: the paper requires word isolation plus whitespace and punctuation
  handling but does not define a tokenizer regex or offset convention.

## D-004: Special tokens and unknown Unicode

- Classification: `implementation_defined`
- Decision: fixed ID order is `<pad>` = 0, `<unk>` = 1, `<s>` = 2, `</s>` = 3.
  BOS/EOS are opt-in runtime additions. Characters observed in training are
  ordinary vocabulary units. A truly unseen runtime character emits `<unk>`
  with its source offset; decoding an unknown emits U+FFFD.
- Reason: the paper specifies character fallback but cannot guarantee coverage
  of Unicode never observed in training. It does not specify special tokens.

## D-005: Operational lexicon extraction

- Classification: `implementation_defined` plus `dataset_constraint`
- Decision:
  - Affix, circumfix, clitic, and `pang-` inventories come only from Table 1 of
    the paper. Additional affixes present in reference CSVs are retained as
    evidence but never activated.
  - Operational roots are exact, single-word, letter/mark/apostrophe forms from
    reference types `root`, `lemma_or_root_candidate`,
    `lexical_root_validation_candidate`, and
    `root_or_dictionary_headword`.
  - Root candidates are annotated with neutral-training frequency; training
    text does not create new roots.
  - Entries explicitly described as `compound` are recorded. Only compounds
    that form one pretoken can be protected by the word-level segmenter;
    multiword compounds remain documented non-operational evidence.
  - Provisional orthographic/stress evidence is retained with sources but does
    not create a replacement mapping. Exact listed root surfaces remain valid
    hosts without canonicalizing their spelling.
- Reason: this is conservative, reproducible, and avoids inventing linguistic
  mappings or broadening morphology beyond the paper.

## D-006: Morphological matching and ambiguity

- Classification: `implementation_defined`
- Decision: follow the paper's stage priority exactly. Within a stage, evaluate
  affixes longest-first, then Unicode lexical order. Deduplicate identical
  results. Accept exactly one distinct valid segmentation; if two or more
  distinct results remain, preserve the token unchanged with an ambiguity
  trace. Empty hosts are invalid.
- Reason: the paper defines stage order and host validation but not ordering or
  ambiguity resolution. Preserving ambiguity is safer than greedy stripping.

## D-007: Infix and clitic context

- Classification: `paper_inferred` and `implementation_defined`
- Decision: `in` and `um` are tested only immediately after the first Unicode
  code point, matching the paper's prose and examples. Clitics are tested only
  as suffixes; the host must be an exact operational root, exact one-pretoken
  compound, or exact variant surface. The returned clitic analysis is
  `[host, clitic]`, as in the paper pseudocode.
- Reason: unrestricted `contains` behavior would create root-internal false
  splits. The paper says clitics may be contained or final but its pseudocode
  requires a valid host and returns host plus clitic.

## D-008: `pang-` variants

- Classification: `paper_inferred`
- Decision: `pam`, `pan`, and `panga` are surface alternatives only for the
  paper's `pang...an` circumfix in the primary segmenter; they are not added as
  unrelated general prefixes.
- Reason: Table 1 labels them variations of `pang-`, while `pang` is listed in
  the circumfix inventory rather than the general prefix inventory.

## D-009: Python-Rust integration

- Classification: `implementation_defined`
- Decision: use a PyO3 extension built with maturin. Python performs shared NFC
  normalization/pre-tokenization and passes normalized lexical tokens plus the
  constructed lexicon into a persistent Rust segmenter object. Candidate
  training uses Rust output; the Python implementation is the readable
  reference. Full-corpus parity is a release gate.
- Reason: the paper requires Python plus Rust-assisted training preprocessing
  but does not prescribe an ABI.

## D-010: Structured protected boundaries

- Classification: `implementation_defined`
- Decision: store protected boundaries as code-point offsets inside each
  pretoken. The literal ` || ` representation is display-only.
- Reason: source text could contain marker characters, and BPE needs an
  unambiguous machine representation.

## D-011: BPE counting and tie-breaking

- Classification: `implementation_defined`
- Decision: aggregate identical `(surface, protected-boundary-set, kind)`
  sequences with integer frequency. Count only adjacent occurrences whose
  joining position is not protected. Select greatest frequency; ties use
  lexicographically smallest `(left UTF-8 bytes, right UTF-8 bytes)`. Apply a
  selected merge left-to-right and never across a protected boundary.
- Reason: the paper specifies frequency selection and boundary protection but
  not traversal, overlapping-pair behavior, or ties.

## D-012: Candidate grid

- Classification: `implementation_defined`
- Decision: after preparing the training stream, let `U` be the number of
  distinct lexical word types. Proposed targets are the nearest multiples of
  64 to `4*sqrt(U)`, `8*sqrt(U)`, and `16*sqrt(U)`, bounded above by feasible
  unique vocabulary growth and below by the initial character-plus-special
  vocabulary. Any collision after bounding is deterministically expanded to
  retain at least three materially different targets where feasible. The
  resulting concrete grid and its fingerprint are written before validation is
  evaluated.
- Reason: the paper requires validation-based selection but supplies no sizes.
  This formula depends only on this project's independently prepared training
  inventory and does not copy packaged provisional configurations.

## D-013: Morphological distance and proxy scope

- Classification: `implementation_defined` and `dataset_constraint`
- Decision: for each validation lexical word with a proxy analysis, compute the
  symmetric disagreement between predicted subword boundaries and proxy
  morpheme boundaries, divided by the number of possible internal code-point
  boundaries. Report the occurrence-weighted mean. MBF1 is micro boundary F1.
  MCF1 counts unordered distinct word-type pairs exactly using the paper's
  shared-token/shared-morpheme definitions. These are provisional development
  proxies only.
- Reason: the paper names morphological distance but provides no formula; the
  portable resources are not human-validated gold.

## D-014: Fertility and nonlexical tokens

- Classification: `implementation_defined`
- Decision: development FR is the number of produced subword tokens for lexical
  word pretokens divided by the number of lexical source-word occurrences.
  Explicit whitespace/punctuation tokens used for lossless runtime round-trip
  are excluded from both numerator and denominator and reported separately.
- Reason: this realizes the paper's tokens-per-source-word definition without
  inflating it because of the lossless offset/decoding representation.

## D-015: Candidate selection hierarchy

- Classification: `paper_inferred` and `implementation_defined`
- Decision, frozen before results: reject any artifact whose constrained
  training log reports a protected-boundary merge; then minimize validation
  morphological distance, maximize MBF1, maximize MCF1, minimize FR only when
  morphology metrics are maintained, and prefer the smaller target as final
  tie-breaker. Numeric comparisons use exact stored decimal values, not rounded
  display values.

## D-016: Finalization and runtime independence

- Classification: `paper_mandated` plus `implementation_defined`
- Decision: retrain the selected target from scratch on train only. Export a
  standalone runtime package and artifact. A clean temporary-directory test
  copies only those two items, denies configured dataset/lexicon paths, and
  requires representative encode/decode success.

## D-017: Dataset-validator packaging defect

- Classification: `dataset_constraint`
- Decision: preserve the package unchanged. Record that the unmodified
  `validate_dataset.py` fails because unchecksummed `HANDOFF.md` contains a
  prohibited label and is absent from `checksums.sha256`. Run the validator core
  unchanged except for excluding that one noncanonical extra path from file
  iteration. The canonical 127-file inventory then validates. The independent
  derived-view validator also passes, but no derived view/configuration is used
  by this project.

## D-018: Held-out isolation

- Classification: `dataset_constraint`
- Decision: project code never parses `data/test.csv`; it verifies only its file
  SHA-256 from the package inventory. The explicitly requested 45-row PAM-TGL
  readiness audit revealed that 30 PAM source strings map to test-assigned
  neutral IDs. Those pairs are barred from smoke tests, fixtures, tuning, and
  training and are documented as a readiness contamination risk.
