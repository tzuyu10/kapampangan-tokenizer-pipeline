"""Parsers for the tabular glossaries.

``trilingual``  KAPAMPANGAN / ENGLISH / PILIPINO wordlist, 56 pp, 3 columns.
``dayalekto``   TAGALOG / CEBUANO / WARAY / KAPAMPANGAN / HILIGAYNON, 11 pp.
``mirikitani``  Glossaries at the back of *Speaking Kapampangan* (PALI), 2 cols.

All three are word lists: a headword and a gloss, no part of speech, no
examples. Fields the source does not provide stay empty — nothing is inferred.
"""
from __future__ import annotations

import re

from .columns import pair, split_columns
from .pdf_text import n_pages, page_text
from .schema import Entry, Source, assess_ocr, make_id

_HEADER = re.compile(
    r"^(KAP\s?AMP\s?ANGAN|ENGLISH|PILIPINO|TAGALOG|CEBUANO|WARAY|HILIGAYNON"
    r"|GLOSSARY|VOCABULARY|ABBREVIATIONS?"
    r"|KAPAMPANGAN[- ]ENGLISH(\s+GLOSSARY)?"
    r"|ENGLISH[- ]KAPAMPANGAN(\s+VOCABULARY)?)$",
    re.IGNORECASE)
_PAGENUM = re.compile(r"^\d{1,4}$")
_WORDY = re.compile(r"[^\W\d_]", re.UNICODE)


def _usable(text: str) -> bool:
    t = text.strip()
    return bool(t) and not _HEADER.match(t) and not _PAGENUM.match(t) and bool(_WORDY.search(t))


# --------------------------------------------------------------------------- #
def trilingual(path: str, dictionary: str = "Kapampangan-English-Pilipino wordlist"
               ) -> list[Entry]:
    """Three fixed columns at x ≈ 36 / 216 / 396."""
    entries: list[Entry] = []
    for pg in range(n_pages(path)):
        cols = split_columns(path, pg, [150.0, 330.0])
        if len(cols) < 3:
            continue
        kap = [(y, t) for y, t in cols[0] if _usable(t)]
        eng = [(y, t) for y, t in cols[1] if _usable(t)]
        fil = [(y, t) for y, t in cols[2] if _usable(t)]
        if not kap:
            continue
        aligned_eng = pair(kap, eng)
        aligned_fil = pair(kap, fil)
        # Flag per column, not per page. In this source the English column
        # tracks the headwords faithfully while the Pilipino column accumulates
        # drift; lumping them together would mark 98% of good English glosses
        # as unreliable and hide which field actually needs checking.
        eng_ok = len(kap) == len(eng)
        fil_ok = len(kap) == len(fil)

        for i, ((_, head), e, f) in enumerate(zip(kap, aligned_eng, aligned_fil)):
            notes: list[str] = []
            senses = [x for x in (e, f) if x]
            if e is None:
                notes.append("English gloss not confidently aligned to this "
                             "headword; left empty rather than guessed.")
            if f is None:
                notes.append("Pilipino gloss not confidently aligned to this "
                             "headword; left empty rather than guessed.")
            if not eng_ok:
                notes.append(f"English column length ({len(eng)}) differs from "
                             f"the headword column ({len(kap)}) on this page; "
                             f"verify against page {pg + 1}.")
            if not fil_ok:
                notes.append(f"Pilipino column length ({len(fil)}) differs from "
                             f"the headword column ({len(kap)}) on this page; the "
                             f"Pilipino gloss in particular may belong to a "
                             f"neighbouring row — verify against page {pg + 1}.")
            status, ocr_notes = assess_ocr(f"{head} {e or ''} {f or ''}")
            if notes:
                status = "needs_review"
            entries.append(Entry(
                entry_id=make_id("trilingual", pg + 1, i, head),
                headword=head,
                definition=senses if len(senses) > 1 else (senses[0] if senses else ""),
                part_of_speech=[],
                pronunciation="", syllables=[], examples=[],
                derived_forms=[], spelling_variants=[], cross_references=[],
                source=Source(dictionary=dictionary, page=pg + 1,
                              original_text=f"{head}\t{e or ''}\t{f or ''}"),
                ocr_status=status,
                notes=" ".join(ocr_notes + notes),
            ))
    return entries


# --------------------------------------------------------------------------- #
def dayalekto(path: str,
              dictionary: str = "Mga Salita sa Iba't Ibang Dayalekto") -> list[Entry]:
    """Five-language comparison table; only the Kapampangan column is a headword.

    Rows are printed as one text line, so this is parsed line-wise rather than
    by coordinates.
    """
    LANGS = ["Tagalog", "Cebuano", "Waray", "Kapampangan", "Hiligaynon"]
    entries: list[Entry] = []
    row_re = re.compile(r"^\s*(\d{1,3})[.)]\s+(.*\S)\s*$")
    for pg in range(n_pages(path)):
        for line in page_text(path, pg).split("\n"):
            m = row_re.match(line)
            if not m:
                continue
            cells = m.group(2).split()
            if len(cells) < 5:
                continue
            # The table is 5 columns but words contain spaces; only rows that
            # tokenise to exactly 5 fields can be split safely.
            if len(cells) != 5:
                continue
            row = dict(zip(LANGS, cells))
            head = row["Kapampangan"]
            status, ocr_notes = assess_ocr(line)
            entries.append(Entry(
                entry_id=make_id("dayalekto", pg + 1, int(m.group(1)), head),
                headword=head,
                definition=row["Tagalog"],
                part_of_speech=[], pronunciation="", syllables=[], examples=[],
                derived_forms=[], spelling_variants=[], cross_references=[],
                source=Source(dictionary=dictionary, page=pg + 1, original_text=line.strip()),
                ocr_status=status,
                notes=" ".join(ocr_notes + [
                    "Definition is the Tagalog equivalent given by the source. "
                    "Cebuano=%s, Waray=%s, Hiligaynon=%s." % (
                        row["Cebuano"], row["Waray"], row["Hiligaynon"])]),
            ))
    return entries


# --------------------------------------------------------------------------- #
def mirikitani(path: str, first_page: int, last_page: int, direction: str,
               dictionary: str = "Mirikitani, Speaking Kapampangan (PALI)"
               ) -> list[Entry]:
    """Two-column glossary at the back of the PALI textbook.

    ``direction`` is ``"pam-eng"`` or ``"eng-pam"``.

    The scan's text layer places the gloss column on baselines that drift
    several lines away from their headword, so pairings here are markedly less
    reliable than in the trilingual wordlist. Every entry is flagged
    ``needs_review`` and carries the full page text, so an annotator can check
    it against the page rather than trusting the alignment.
    """
    entries: list[Entry] = []
    for pg in range(first_page, last_page + 1):
        cols = split_columns(path, pg, [150.0])
        if len(cols) < 2:
            continue
        left = [(y, t) for y, t in cols[0] if _usable(t)]
        right = [(y, t) for y, t in cols[1] if _usable(t)]
        if not left:
            continue
        aligned = pair(left, right, window=6.0)
        raw_page = page_text(path, pg)
        for i, ((_, head), g) in enumerate(zip(left, aligned)):
            _, ocr_notes = assess_ocr(f"{head} {g or ''}")
            note = ("Two-column glossary: the text layer of this scan misaligns "
                    "the gloss column, so this pairing is positional and MUST be "
                    f"verified against page {pg + 1} before use.")
            entries.append(Entry(
                entry_id=make_id(f"mirikitani-{direction}", pg + 1, i, head),
                headword=head,
                definition=g or "",
                part_of_speech=[], pronunciation="", syllables=[], examples=[],
                derived_forms=[], spelling_variants=[], cross_references=[],
                source=Source(dictionary=f"{dictionary} [{direction}]",
                              page=pg + 1, original_text=raw_page.strip()),
                ocr_status="needs_review",
                notes=" ".join(ocr_notes + [note]),
            ))
    return entries
