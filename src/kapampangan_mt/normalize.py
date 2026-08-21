"""Surface normalisation for Kapampangan text.

This is the first half of the thesis' "Pre-Tokenizing" component (p. 37-38):
"normalizes spelling variants, handles whitespace and punctuation boundaries,
and isolates word tokens as discrete units".

IMPORTANT
---------
Kapampangan has no single official orthography. Two systems circulate:
the Spanish-derived one (``quing``, ``cacu``, ``ualu``) and the modern
Filipino-derived one (``king``, ``kaku``, ``walu``).  The rules below are
therefore NOT hard-coded linguistic truth: they are loaded from
``data/lexicon/orthography_rules.tsv`` so a Kapampangan validator can sign off
on them.  Only the Unicode-level operations are built in.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

# Characters that are always collapsed regardless of orthography choice.
_QUOTE_MAP = {
    "‘": "'", "’": "'", "‛": "'", "′": "'",
    "“": '"', "”": '"', "„": '"',
    "–": "-", "—": "-", "−": "-",
    " ": " ", "​": "", "﻿": "",
}
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_WS_RE = re.compile(r"\s+")


@dataclass
class Normalizer:
    """Deterministic, reversible-enough text normaliser.

    Parameters
    ----------
    lowercase:
        Fold case. Recommended True for a 13k-sentence corpus: casing triples
        the number of word types the BPE has to learn and Kapampangan has no
        case-bearing morphology.
    unicode_form:
        NFC keeps ``ñ`` as one code point, which keeps character-level
        fallback aligned with what a human sees.
    orthography_rules:
        Ordered ``(pattern, replacement)`` regex pairs applied *after* Unicode
        normalisation. Empty by default.
    """

    lowercase: bool = True
    unicode_form: str = "NFC"
    strip_accents: bool = False
    orthography_rules: list[tuple[re.Pattern, str]] = field(default_factory=list)

    # ------------------------------------------------------------------ #
    @classmethod
    def from_rules_file(cls, path: str | Path | None, **kw) -> "Normalizer":
        rules: list[tuple[re.Pattern, str]] = []
        if path is not None and Path(path).exists():
            for line in Path(path).read_text(encoding="utf-8").splitlines():
                line = line.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) < 2:
                    raise ValueError(f"Bad orthography rule (need 2 tab fields): {line!r}")
                pattern, repl = parts[0], parts[1]
                rules.append((re.compile(pattern), repl))
        return cls(orthography_rules=rules, **kw)

    # ------------------------------------------------------------------ #
    def normalize_text(self, text: str) -> str:
        """Normalise a whole sentence / document."""
        text = unicodedata.normalize(self.unicode_form, text)
        text = "".join(_QUOTE_MAP.get(ch, ch) for ch in text)
        text = _CONTROL_RE.sub(" ", text)
        if self.lowercase:
            text = text.lower()
        if self.strip_accents:
            text = "".join(
                c for c in unicodedata.normalize("NFD", text)
                if unicodedata.category(c) != "Mn"
            )
            text = unicodedata.normalize(self.unicode_form, text)
        for pattern, repl in self.orthography_rules:
            text = pattern.sub(repl, text)
        return _WS_RE.sub(" ", text).strip()

    def normalize_token(self, token: str) -> str:
        """Normalise a single already-isolated word (used by the segmenter)."""
        return self.normalize_text(token)


def default_normalizer(rules_path: str | Path | None = None) -> Normalizer:
    return Normalizer.from_rules_file(rules_path)
