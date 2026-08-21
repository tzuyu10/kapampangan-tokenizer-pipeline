"""The JSONL record schema, and the checks that keep it source-faithful."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field


@dataclass
class Source:
    dictionary: str = ""
    page: int | None = None
    original_text: str = ""


@dataclass
class Entry:
    entry_id: str = ""
    headword: str = ""
    definition: object = ""          # str, or list[str] when the source gives senses
    part_of_speech: list[str] = field(default_factory=list)
    pronunciation: str = ""
    syllables: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    derived_forms: list[str] = field(default_factory=list)
    spelling_variants: list[str] = field(default_factory=list)
    cross_references: list[str] = field(default_factory=list)
    source: Source = field(default_factory=Source)
    ocr_status: str = "clear"        # "clear" | "needs_review"
    notes: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def new_entry(**kw) -> Entry:
    src = kw.pop("source", None)
    e = Entry(**kw)
    if src is not None:
        e.source = src if isinstance(src, Source) else Source(**src)
    return e


# --------------------------------------------------------------------------- #
# OCR damage detection — flags only. Nothing here rewrites the extracted text.
# --------------------------------------------------------------------------- #
#: Confusions this specific scan actually exhibits, checked against the pages.
KNOWN_OCR_CONFUSIONS = {
    "ft.": "'ft.' is very likely 'n.' — 'n' reads as 'ft' throughout this scan",
    "S ee": "likely 'See'",
    "rt.": "possibly 'n.'",
}
_BROKEN_WORD = re.compile(r"\b[a-z]{1,2} [a-z]{2,}\b")     # "as awa", "pis amb an"
_STRAY_PIPE = re.compile(r"\|")
_ODD_CHARS = re.compile(r"[£§¶©®¬~^`{}\\]")
_DIGIT_IN_WORD = re.compile(r"[a-zA-Z][0-9][a-zA-Z]")      # "t3ya", "kuts£rang"


def assess_ocr(text: str) -> tuple[str, list[str]]:
    """Return ``(status, notes)``. Never modifies *text*."""
    notes: list[str] = []
    for bad, hint in KNOWN_OCR_CONFUSIONS.items():
        if bad in text:
            notes.append(f"Possible OCR error: contains {bad!r} — {hint}.")
    if _DIGIT_IN_WORD.search(text):
        notes.append("Possible OCR error: digit inside an alphabetic word.")
    if _ODD_CHARS.search(text):
        notes.append("Possible OCR error: unexpected symbol characters present.")
    if _STRAY_PIPE.search(text):
        notes.append("Layout artefact: column-separator bars retained in the text.")
    if len(_BROKEN_WORD.findall(text)) >= 2:
        notes.append("Possible OCR error: words appear split by spurious spaces.")
    if any(unicodedata.category(c) == "Co" for c in text):
        notes.append("Possible OCR error: private-use Unicode characters present.")
    return ("needs_review" if notes else "clear"), notes


def make_id(dictionary: str, page: int | None, index: int, headword: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", headword.lower()).strip("-")[:32] or "x"
    return f"{dictionary}:p{page or 0:04d}:{index:03d}:{slug}"


def sort_key(word: str) -> str:
    """Accent- and case-insensitive key, for verifying alphabetical ordering.

    Used only to VALIDATE that detected headwords run in dictionary order —
    never to alter a headword.
    """
    s = unicodedata.normalize("NFD", word.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z]", "", s)
