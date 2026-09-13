"""Gold morpheme reference data and scoring functions.

Everything in this file is copied UNCHANGED from the research team's own
`demo.py` (which itself states these scoring functions are "lifted verbatim
from experiments/tokenizer_selection_v1/run_selection.py"). Nothing here was
written or altered by this integration — it is reused as-is so that Boundary
F1 / Consistency F1 shown by the API are the exact same numbers the thesis
demo would produce, never an approximation invented for the web app.

Only words/sentences that appear in this file have gold morpheme annotations.
Arbitrary user input that is not one of these has NO gold reference, so the
API reports boundary_f1 / consistency_f1 as unavailable for it rather than
fabricating a score (see trace_service.py).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

# ---------------------------------------------------------------------------
# Gold data — copied verbatim from demo.py
# ---------------------------------------------------------------------------

# Lower-case example inputs (the Phase 3 reference set is lower-case and the
# tokenizers are case-sensitive). Each word carries its gold morpheme split
# ("" = one morpheme). Splits are from reference-morphology.csv.
SENTENCES: list[list[tuple[str, str]]] = [
    [("dinatang", "d|in|atang"), ("ya", ""), ("at", ""),
     ("sinulat", "s|in|ulat"), ("ne", "")],
    [("sinabi", "s|in|abi"), ("na", ""), ("king", ""),
     ("linub", "l|in|ub"), ("ke", "")],
    [("ing", ""), ("kaburian", "ka|buri|an"), ("at", ""),
     ("ing", ""), ("kabengian", "ka|bengi|an")],
    [("malagu", "ma|lagu"), ("at", ""), ("masaya", "ma|saya"), ("ya", "")],
]

# Word families for consistency (1.3): one root, several affixed forms.
FAMILIES: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("ligtas", "save, rescue", [
        ("kaligtasan", "ka|ligtas|an"),
        ("magligtas", "mag|ligtas"),
        ("pangaligtas", "panga|ligtas"),
    ]),
    ("ibat", "come from, origin", [
        ("manibat", "man|ibat"),
        ("menibat", "men|ibat"),
        ("menibatan", "men|ibat|an"),
    ]),
]

# Raw-split showcase words (no gold boundaries — glosses only).
WORDS: list[tuple[str, str]] = [
    ("sinulat", "wrote"),
    ("kabukasan", "tomorrow / the future"),
    ("magsalita", "to speak"),
    ("pipaglutuan", "kitchen / place for cooking"),
    ("mamangan", "to eat"),
    ("sumulat", "to write"),
]

MCF1_MIN_LEN = 2
MCF1_MAX_GROUP = 300


def _pieces_from_boundaries(surface: str, bnds: tuple[int, ...]) -> tuple[str, ...]:
    prev = 0
    out: list[str] = []
    for b in bnds:
        out.append(surface[prev:b])
        prev = b
    out.append(surface[prev:])
    return tuple(out)


def _f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if p + r else 0.0


def _capped_pairs(members: list[int], cap: int) -> set[tuple[int, int]]:
    if len(members) > cap:
        members = members[:cap]
    return {
        (members[i], members[j])
        for i in range(len(members))
        for j in range(i + 1, len(members))
    }


def mcf1(rows: list[dict[str, Any]], encoded_pieces: list[tuple[str, ...]]) -> dict[str, float]:
    morpheme_sets = [
        frozenset(p for p in r["gold_pieces"] if len(p) >= MCF1_MIN_LEN) for r in rows
    ]
    token_sets = [
        frozenset(p for p in pieces if len(p) >= MCF1_MIN_LEN) for pieces in encoded_pieces
    ]
    morpheme_groups: dict[str, list[int]] = defaultdict(list)
    for i, ms in enumerate(morpheme_sets):
        for m in ms:
            morpheme_groups[m].append(i)
    token_groups: dict[str, list[int]] = defaultdict(list)
    for i, ts in enumerate(token_sets):
        for t in ts:
            token_groups[t].append(i)
    mpairs: set[tuple[int, int]] = set()
    for members in morpheme_groups.values():
        if len(members) >= 2:
            mpairs |= _capped_pairs(members, MCF1_MAX_GROUP)
    tpairs: set[tuple[int, int]] = set()
    for members in token_groups.values():
        if len(members) >= 2:
            tpairs |= _capped_pairs(members, MCF1_MAX_GROUP)
    tp = len(mpairs & tpairs)
    fn = len(mpairs - tpairs)
    fp = len(tpairs - mpairs)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {
        "mcf1_precision": p,
        "mcf1_recall": r,
        "mcf1": _f1(p, r),
        "mcf1_gold_pairs": float(len(mpairs)),
    }


def score(rows: list[dict[str, Any]], encoded: list[tuple[str, ...]]) -> dict[str, float]:
    tp = fp = fn = 0
    produced = 0
    for row, pieces in zip(rows, encoded, strict=True):
        pred = set()
        acc = 0
        for piece in pieces[:-1]:
            acc += len(piece)
            pred.add(acc)
        gold = row["gold_boundaries"]
        tp += len(gold & pred)
        fp += len(pred - gold)
        fn += len(gold - pred)
        produced += len(pieces)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    out = {
        "boundary_precision": p,
        "boundary_recall": r,
        "boundary_f1": _f1(p, r),
        "fertility": produced / len(rows) if rows else 0.0,
    }
    out.update(mcf1(rows, encoded))
    return out


def rows_for(sentence: list[tuple[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface, spec in sentence:
        pieces = tuple(spec.split("|")) if spec else (surface,)
        acc, bnds = 0, []
        for piece in pieces[:-1]:
            acc += len(piece)
            bnds.append(acc)
        rows.append(
            {
                "surface": surface,
                "gold_boundaries": set(bnds),
                "gold_pieces": _pieces_from_boundaries(surface, tuple(bnds)),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Lookup tables built from the gold data above (integration code, not part of
# the "algorithm" — just indexes the same data by surface word for quick
# matching against arbitrary user input).
# ---------------------------------------------------------------------------

def _build_word_gold_index() -> dict[str, tuple[str, ...]]:
    index: dict[str, tuple[str, ...]] = {}
    for sentence in SENTENCES:
        for surface, spec in sentence:
            pieces = tuple(spec.split("|")) if spec else (surface,)
            index[surface] = pieces
    for _root, _gloss, forms in FAMILIES:
        for surface, spec in forms:
            pieces = tuple(spec.split("|")) if spec else (surface,)
            index[surface] = pieces
    return index


WORD_GOLD_INDEX: dict[str, tuple[str, ...]] = _build_word_gold_index()


def family_for(word: str) -> tuple[str, str, list[tuple[str, str]]] | None:
    """Return the (root, gloss, forms) family entry that contains `word`, if any."""
    for root, gloss, forms in FAMILIES:
        for surface, _spec in forms:
            if surface == word:
                return (root, gloss, forms)
    return None
