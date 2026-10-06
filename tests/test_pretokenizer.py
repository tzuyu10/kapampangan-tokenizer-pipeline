from __future__ import annotations

import unicodedata

from hypothesis import given
from hypothesis import strategies as st

from kapampangan_morphbpe.pretokenizer import pretokenize


def test_empty_and_repeated_whitespace() -> None:
    normalized, tokens = pretokenize("  \t\n")
    assert normalized == "  \t\n"
    assert len(tokens) == 1
    assert tokens[0].kind == "whitespace"
    assert (tokens[0].start, tokens[0].end) == (0, 4)


def test_punctuation_accents_enye_and_internal_joiners() -> None:
    normalized, tokens = pretokenize("Ápu, d'yan bahay-basa; ñ!")
    assert "".join(token.surface for token in tokens) == normalized
    assert [(token.surface, token.kind) for token in tokens] == [
        ("Ápu", "word"),
        (",", "punctuation"),
        (" ", "whitespace"),
        ("d'yan", "word"),
        (" ", "whitespace"),
        ("bahay-basa", "word"),
        (";", "punctuation"),
        (" ", "whitespace"),
        ("ñ", "word"),
        ("!", "punctuation"),
    ]


def test_nfc_offsets_are_into_normalized_text() -> None:
    source = "A\u0301 ñ"
    normalized, tokens = pretokenize(source)
    assert normalized == "Á ñ"
    assert normalized == unicodedata.normalize("NFC", source)
    for token in tokens:
        assert normalized[token.start : token.end] == token.surface


@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cs",),
            blacklist_characters=("\x00",),
        ),
        max_size=80,
    )
)
def test_pretokenization_is_lossless_for_normalized_input(value: str) -> None:
    normalized, tokens = pretokenize(value)
    assert "".join(token.surface for token in tokens) == normalized
    assert all(normalized[token.start : token.end] == token.surface for token in tokens)
