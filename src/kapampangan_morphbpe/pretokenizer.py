from __future__ import annotations

import unicodedata

from .models import Pretoken, PretokenKind
from .normalization import normalize_text

_INTERNAL_JOINERS = frozenset({"'", "\u2019", "-"})


def _is_word_core(character: str) -> bool:
    return unicodedata.category(character)[0] in {"L", "M", "N"}


def _nonword_kind(character: str) -> PretokenKind:
    return "punctuation" if unicodedata.category(character).startswith("P") else "symbol"


def pretokenize_normalized(normalized: str) -> tuple[Pretoken, ...]:
    tokens: list[Pretoken] = []
    index = 0
    length = len(normalized)
    while index < length:
        character = normalized[index]
        if character.isspace():
            end = index + 1
            while end < length and normalized[end].isspace():
                end += 1
            tokens.append(Pretoken(normalized[index:end], index, end, "whitespace"))
            index = end
            continue

        if _is_word_core(character):
            end = index + 1
            while end < length:
                current = normalized[end]
                if _is_word_core(current):
                    end += 1
                    continue
                if (
                    current in _INTERNAL_JOINERS
                    and end + 1 < length
                    and _is_word_core(normalized[end - 1])
                    and _is_word_core(normalized[end + 1])
                ):
                    end += 1
                    continue
                break
            tokens.append(Pretoken(normalized[index:end], index, end, "word"))
            index = end
            continue

        kind = _nonword_kind(character)
        tokens.append(Pretoken(character, index, index + 1, kind))
        index += 1

    if "".join(token.surface for token in tokens) != normalized:
        raise AssertionError("pretokenizer failed lossless reconstruction")
    return tuple(tokens)


def pretokenize(text: str) -> tuple[str, tuple[Pretoken, ...]]:
    normalized = normalize_text(text)
    return normalized, pretokenize_normalized(normalized)
