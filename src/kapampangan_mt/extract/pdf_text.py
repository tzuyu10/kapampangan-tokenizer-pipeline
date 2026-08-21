"""PDF text access: plain reading order, and coordinate-aware line rebuilding.

``page_lines`` is enough for single-flow dictionaries (Samson).
``page_rows`` recovers x/y positions and is needed for the two-column
glossaries, where naive reading order interleaves the columns.
"""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache

import pypdf


@lru_cache(maxsize=8)
def open_pdf(path: str) -> pypdf.PdfReader:
    return pypdf.PdfReader(path)


def n_pages(path: str) -> int:
    return len(open_pdf(path).pages)


def page_text(path: str, index: int) -> str:
    try:
        return open_pdf(path).pages[index].extract_text() or ""
    except Exception:
        return ""


def page_lines(path: str, index: int) -> list[str]:
    return [ln.rstrip() for ln in page_text(path, index).split("\n")]


def page_rows(path: str, index: int, y_tol: float = 3.0) -> list[tuple[float, list[tuple[float, str]]]]:
    """Rebuild visual lines as ``(y, [(x, text), ...])``, top of page first.

    Text chunks whose baselines are within ``y_tol`` points are treated as one
    visual line; within a line, chunks are ordered by x. This is what makes a
    two-column glossary readable — plain extraction returns the columns
    interleaved in an order that pairs the wrong headword with the wrong gloss.
    """
    chunks: list[tuple[float, float, str]] = []

    def visitor(text, cm, tm, font, size):  # noqa: ANN001
        if text and text.strip():
            chunks.append((float(tm[5]), float(tm[4]), text))

    try:
        open_pdf(path).pages[index].extract_text(visitor_text=visitor)
    except Exception:
        return []

    buckets: dict[float, list[tuple[float, str]]] = defaultdict(list)
    for y, x, t in chunks:
        key = round(y / y_tol) * y_tol
        buckets[key].append((x, t))
    rows = []
    for y in sorted(buckets, reverse=True):
        rows.append((y, sorted(buckets[y], key=lambda p: p[0])))
    return rows
