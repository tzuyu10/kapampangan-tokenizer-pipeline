from __future__ import annotations

import unicodedata


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return unicodedata.normalize("NFC", text)


def comparison_key(text: str) -> str:
    return normalize_text(text).lower()
