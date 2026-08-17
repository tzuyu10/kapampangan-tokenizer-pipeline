# Morphological Segmentation Specification

## Pipeline position and runtime boundary

Morphological segmentation runs only while preparing tokenizer training data.
The paper-mandated order is implemented independently in Python and Rust. The
final runtime contains neither implementation nor any morphological inventory.

## Inventory

- Prefixes: `ma me pa maka ka mag meg mang meng i ipa makapag mig meka mekapag`
- Infixes: `in um`
- Suffix: `an`
- Circumfixes: `ka...an pa...an pang...an`
- Clitics: `na pa mu ku ya la ra ne no`
- `pang-` variants: `pam pan panga`, used only as surface variants of
  `pang...an`

This inventory is `paper_mandated` from Chapter 2, Table 1, printed p. 19
(PDF p. 22). No unrelated morphological process is added.

## Exact stage order

1. NFC-normalize the token.
2. Return `empty` for empty input.
3. If it is a known one-pretoken compound, preserve it as
   `protected_compound`.
4. If it is a known root/variant, preserve it as `protected_root`.
5. Call `TRY_CIRCUMFIX`.
6. Call `TRY_PREFIX`.
7. Call `TRY_INFIX`.
8. Call `TRY_SUFFIX`.
9. Call `TRY_CLITIC`.
10. Otherwise return the original normalized token as `unchanged`.

This follows Figure 7 (Chapter 3, printed pp. 39-41; PDF pp. 42-44).

## Analysis functions

`TRY_CIRCUMFIX` requires one matched prefix and its paired `an` suffix, a
nonempty core, and an exact root/variant core. The `pam`, `pan`, and `panga`
surfaces map only to the `pang...an` family.

`TRY_PREFIX` requires an exact root/variant remainder. `TRY_SUFFIX` requires an
exact root/variant host. `TRY_INFIX` tests `in` or `um` immediately after the
first Unicode code point, removes it to reconstruct the candidate root, and
returns left/infix/right segments. `TRY_CLITIC` is suffix-contextual and
requires an exact root, variant, or protected compound host.

`MARK_BOUNDARIES` converts segments into sorted internal code-point offsets.
For example, `("k", "um", "an")` is displayed as `k || um || an` and stores
boundaries `(1,3)`. No literal marker is inserted into corpus text.

## Ambiguity and safety completions

The following are `implementation_defined` because the paper is silent:

- affixes are enumerated longest-first, then by Unicode lexical order;
- all valid candidates in the current stage are deduplicated;
- one distinct candidate is accepted;
- two or more distinct candidates make the form `ambiguous`, unchanged, with
  rule IDs in the trace; and
- stages after an ambiguous stage are not attempted.

No empty host, greedy recursive stripping, root-internal split, or analysis
without exact host validation is permitted. Every accepted result reconstructs
the normalized token, has a stable rule ID, kind, status, trace, and structured
protected boundaries. Failure always leaves the token processable.

## Implementations and parity

- Reference: `src/kapampangan_morphbpe/morphology.py`
- Rust/PyO3: `rust/src/lib.rs`
- Bridge: `src/kapampangan_morphbpe/rust_bridge.py`

The actual training stream uses Rust. A full development-corpus gate compared
154,446 distinct train/validation word types across 29,552 records: 154,446
exact matches, zero discrepancies. The held-out test was not used.

## Training coverage

For 1,476,145 training word occurrences, accepted multi-segment analyses total
41,923 (2.8400327%). An additional 488,967 known-root and 5,781 known-compound
occurrences are protected as indivisible units. Ninety-one ambiguous
occurrences (20 types) remain unchanged. These counts are provisional because
the underlying references are not human-adjudicated.

