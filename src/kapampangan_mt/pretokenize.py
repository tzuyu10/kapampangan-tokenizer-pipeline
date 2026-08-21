"""Pre-Tokenizing component (thesis p. 37-38).

Splits normalised text into *word units* and marks word starts with the
SentencePiece-style meta symbol ``▁`` so that detokenisation is lossless
(``"".join(tokens).replace("▁", " ")`` reproduces the sentence).

The pre-tokenizer output is the unit over which BOTH the morphological
segmenter and the BPE merge search operate.  A merge can therefore never
cross a whitespace or punctuation boundary, which is standard BPE behaviour
(Sennrich et al., 2016) and is assumed by the thesis.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

WORD_BOUNDARY = "▁"  # ▁

# A "word" = run of letters (incl. ñ and combining marks), apostrophe-internal
# (e.g. ``ta'nan``) and hyphen-internal (e.g. ``pepa-pa``) sequences.
_WORD_RE = re.compile(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", re.UNICODE)
_NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
_TOKEN_RE = re.compile(
    rf"(?P<word>{_WORD_RE.pattern})|(?P<num>{_NUM_RE.pattern})|(?P<punct>[^\s\w])",
    re.UNICODE,
)


@dataclass(frozen=True)
class PreToken:
    """One pre-tokenised unit."""

    surface: str          # the raw string, e.g. "kinan"
    kind: str             # "word" | "num" | "punct"
    starts_word: bool     # True when preceded by whitespace / start of string

    @property
    def marked(self) -> str:
        """Surface with the word-start marker attached (BPE training unit)."""
        return (WORD_BOUNDARY + self.surface) if self.starts_word else self.surface


def pre_tokenize(text: str) -> list[PreToken]:
    """Split *normalised* text into PreTokens.

    >>> [t.marked for t in pre_tokenize("kinan ne ing pamangan.")]
    ['▁kinan', '▁ne', '▁ing', '▁pamangan', '.']
    """
    out: list[PreToken] = []
    prev_end = 0
    for m in _TOKEN_RE.finditer(text):
        gap = text[prev_end : m.start()]
        starts = (m.start() == 0) or (gap != "" and gap.isspace())
        kind = m.lastgroup or "punct"
        out.append(PreToken(surface=m.group(0), kind=kind, starts_word=starts))
        prev_end = m.end()
    return out


def words_only(text: str) -> list[str]:
    """Convenience: the alphabetic word surfaces, used for Fertility Rate.

    Fertility Rate (thesis eq. 1) is ``tokens / source words``.  ``W`` is
    defined here as the number of *word* pre-tokens (punctuation and digits
    excluded) so that a sentence rich in commas does not artificially lower the
    fertility of both tokenizers.  Report this definition in Chapter 3.
    """
    return [t.surface for t in pre_tokenize(text) if t.kind == "word"]


def normalized_words(text: str, normalizer=None) -> list[str]:
    """Normalise then extract word surfaces.

    Every stage that produces or consumes word *types* (gold template, MCF1
    type list, lexicon coverage) must agree on casing, otherwise "Akitan" and
    "akitan" become two different types and the gold file stops matching the
    tokenizer output.
    """
    from .normalize import Normalizer

    normalizer = normalizer or Normalizer()
    return words_only(normalizer.normalize_text(text))


def detokenize(pieces: list[str]) -> str:
    """Inverse of pre-tokenisation + BPE, for reading model output."""
    return "".join(pieces).replace(WORD_BOUNDARY, " ").strip()
