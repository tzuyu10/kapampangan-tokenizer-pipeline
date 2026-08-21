"""Column-aligned extraction for tabular glossaries.

Naive reading order interleaves columns and pairs the wrong headword with the
wrong gloss, which would mean *fabricating* definitions. These helpers instead
work from the text chunks' x/y positions.

Alignment method
----------------
Columns rarely line up on identical baselines: the scan drifts, and a gloss that
wraps onto two lines pushes everything after it. So instead of zipping by index
(unsafe: the columns have different lengths on 53 of 56 pages of the trilingual
glossary) we:

1. assign chunks to columns by x
2. estimate ONE vertical offset per column per page, as the median of each
   headword's nearest-neighbour distance
3. pair only within a tight window after correcting for that offset
4. leave the field null and flag the entry when no pairing is inside the window

Step 4 is the important one. An unpaired gloss is recorded as missing, never
guessed.
"""
from __future__ import annotations

import statistics
from collections import defaultdict

from .pdf_text import page_rows


def split_columns(path: str, page_index: int, boundaries: list[float]
                  ) -> list[list[tuple[float, str]]]:
    """Split a page's chunks into columns at the given x boundaries."""
    cols: dict[int, list[tuple[float, str]]] = defaultdict(list)
    for y, cells in page_rows(path, page_index):
        for x, text in cells:
            t = text.strip()
            if not t:
                continue
            idx = sum(1 for b in boundaries if x >= b)
            cols[idx].append((y, t))
    out = []
    for i in range(len(boundaries) + 1):
        items = sorted(cols.get(i, []), key=lambda p: -p[0])
        merged: list[tuple[float, str]] = []
        for y, t in items:                    # join chunks on the same baseline
            if merged and abs(merged[-1][0] - y) < 1.5:
                merged[-1] = (merged[-1][0], merged[-1][1] + " " + t)
            else:
                merged.append((y, t))
        out.append(merged)
    return out


def estimate_offset(anchor: list[tuple[float, str]],
                    other: list[tuple[float, str]]) -> float:
    """Median vertical shift of *other* relative to *anchor*."""
    if not anchor or not other:
        return 0.0
    diffs = []
    for y, _ in anchor:
        best = min(other, key=lambda p: abs(p[0] - y))
        d = best[0] - y
        if abs(d) <= 14:
            diffs.append(d)
    return statistics.median(diffs) if diffs else 0.0


def pair(anchor: list[tuple[float, str]], other: list[tuple[float, str]],
         window: float = 4.0) -> list[str | None]:
    """For each anchor item, the aligned text from *other*, or None.

    ``None`` means "the source did not give us a confident pairing here" and the
    caller must record the field as missing rather than guessing.
    """
    if not other:
        return [None] * len(anchor)
    off = estimate_offset(anchor, other)
    used: set[int] = set()
    out: list[str | None] = []
    for y, _ in anchor:
        target = y + off
        best_i, best_d = None, None
        for i, (oy, _t) in enumerate(other):
            if i in used:
                continue
            d = abs(oy - target)
            if best_d is None or d < best_d:
                best_i, best_d = i, d
        if best_i is not None and best_d is not None and best_d <= window:
            used.add(best_i)
            out.append(other[best_i][1])
        else:
            out.append(None)
    return out
