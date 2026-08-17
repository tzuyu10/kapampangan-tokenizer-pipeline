# Pre-tokenization

## Authority and scope

The paper mandates a pre-tokenizing stage before morphological segmentation,
including spelling-variant normalization, whitespace and punctuation handling,
and word isolation (Chapter 3, printed pp. 37-38; PDF pp. 40-41). It does not
define a complete normalization map, tokenization regular expression, or offset
unit. The choices below are therefore explicitly `implementation_defined`.

## Normalization

1. Accept a Python Unicode string.
2. Apply Unicode NFC exactly once.
3. Do not lowercase, strip accents, stem, lemmatize, modernize spelling, or
   normalize dialect.
4. Apply no spelling substitutions. The 187 provisional variation/stress rows
   in the supplied evidence do not define reviewed directional mappings.

NFC is the only surface-changing operation. All token offsets refer to the NFC
normalized string, not the original pre-normalization code-point sequence.

## Deterministic state machine

The scanner advances by normalized Unicode code point:

- A **word core** is a run of letters (`L*`), marks (`M*`), or numbers (`N*`).
- ASCII apostrophe, U+2019, and hyphen remain internal to a word only when
  flanked by word-core characters.
- Consecutive whitespace is one whitespace pretoken during pre-tokenization.
- Each punctuation or other symbol code point is an explicit pretoken.
- Empty input returns an empty sequence.

Every pretoken stores `surface`, `start`, `end`, and `kind`. The half-open
`[start,end)` indices count normalized Unicode code points. Concatenating all
pretoken surfaces must reconstruct normalized input exactly.

## Training/runtime identity

Training uses `src/kapampangan_morphbpe/pretokenizer.py`. The standalone runtime
implements the same state machine in
`runtime/kapampangan_morphbpe_runtime/tokenizer.py`. The final artifact freezes
the contract in `normalization.json` and `pretokenizer.json`; neither file
contains linguistic resources.

## Tested edge cases

Property and unit tests cover empty input, repeated spaces/tabs/newlines,
punctuation, apostrophes, hyphens, decomposed accents normalized to NFC,
accented letters, `ñ`, arbitrary non-surrogate Unicode, exact reconstruction,
and offset slices. Morphology-specific splitting is deliberately absent here.

