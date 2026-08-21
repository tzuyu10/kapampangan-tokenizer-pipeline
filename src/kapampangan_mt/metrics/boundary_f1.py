"""Morpheme Boundary F1 — thesis eqs. (2)-(4).

A *boundary* is a character offset strictly inside a word.  For the word
``kapampangan`` with gold analysis ``ka|pampang|an`` the gold boundary set is
``{2, 9}``.  A tokenizer that outputs ``["▁ka","pam","pangan"]`` predicts
``{2, 5}`` — one true positive (2), one false positive (5), one false
negative (9).

    P_b = TP / (TP + FP)      R_b = TP / (TP + FN)      MBF1 = 2PR / (P + R)

CRITICAL — read before running this
-----------------------------------
``gold`` must come from a **human-annotated** file, not from
``MorphologicalSegmenter``.  If the gold boundaries are produced by the same
rule+lexicon system that constrained Morph-BPE training, this metric is
circular: the proposed tokenizer is being graded against its own training
signal and will win by construction.  ``load_gold`` therefore refuses files
that carry the ``auto`` provenance tag unless ``allow_auto=True`` is passed
explicitly (use only for smoke tests).  See Issue M-2.
"""
from __future__ import annotations

import csv
from pathlib import Path


def word_boundaries_from_segments(segments: list[str]) -> set[int]:
    out, pos = set(), 0
    for s in segments[:-1]:
        pos += len(s)
        out.add(pos)
    return out


def load_gold(path: str | Path, allow_auto: bool = False) -> list[tuple[str, set[int], int]]:
    """Read ``data/gold/morpheme_gold.tsv``.

    Columns: ``word``, ``segmentation`` (``ka|pampang|an``), ``annotator``,
    ``provenance`` (``human`` | ``auto``), ``notes``.
    Returns ``[(word, gold_boundaries, count)]``; ``count`` is the token
    frequency used for micro-averaging (defaults to 1 = type-level scoring).
    """
    rows: list[tuple[str, set[int], int]] = []
    auto_rows = 0
    with Path(path).open(encoding="utf-8", newline="") as fh:
        lines = [l for l in fh if l.strip() and not l.lstrip().startswith("#")]
    for r in csv.DictReader(lines, delimiter="\t"):
        word = (r.get("word") or "").strip()
        seg = (r.get("segmentation") or "").strip()
        if not word or not seg:
            continue
        if (r.get("provenance") or "human").strip().lower() == "auto":
            auto_rows += 1
        parts = [p for p in seg.split("|") if p]
        if "".join(parts) != word:
            raise ValueError(
                f"gold row for {word!r}: segments {parts} do not concatenate back. "
                "Morphophonemic alternations must be written with the SURFACE "
                "pieces (bas|an for basan), not the underlying form."
            )
        rows.append((word, word_boundaries_from_segments(parts),
                     int(r.get("count") or 1)))
    if auto_rows and not allow_auto:
        raise ValueError(
            f"{auto_rows} rows in {path} are tagged provenance=auto. Morpheme "
            "Boundary F1 computed against machine-generated gold data is "
            "circular and will not survive a defence. Pass allow_auto=True only "
            "for pipeline smoke tests."
        )
    return rows


def boundary_scores_per_word(tokenizer, gold: list[tuple[str, set[int], int]]) -> list[dict]:
    """Per-word TP/FP/FN and F1 — the paired observations for RQ3.2."""
    out = []
    for word, gold_b, count in gold:
        pred = tokenizer.boundaries(word)
        tp = len(pred & gold_b)
        fp = len(pred - gold_b)
        fn = len(gold_b - pred)
        p = tp / (tp + fp) if (tp + fp) else 1.0
        r = tp / (tp + fn) if (tp + fn) else 1.0
        f1 = 2 * p * r / (p + r) if (p + r) else 0.0
        out.append({"word": word, "count": count, "tp": tp, "fp": fp, "fn": fn,
                    "precision": p, "recall": r, "f1": f1})
    return out


def boundary_f1_corpus(tokenizer, gold: list[tuple[str, set[int], int]]) -> dict:
    """Micro-averaged (corpus-level) MBF1 plus the macro/per-word mean."""
    per = boundary_scores_per_word(tokenizer, gold)
    TP = sum(x["tp"] * x["count"] for x in per)
    FP = sum(x["fp"] * x["count"] for x in per)
    FN = sum(x["fn"] * x["count"] for x in per)
    P = TP / (TP + FP) if (TP + FP) else 0.0
    R = TP / (TP + FN) if (TP + FN) else 0.0
    F1 = 2 * P * R / (P + R) if (P + R) else 0.0
    n = len(per) or 1
    return {
        "boundary_precision": P,
        "boundary_recall": R,
        "mbf1_micro": F1,
        "mbf1_macro": sum(x["f1"] for x in per) / n,
        "n_words": len(per),
        "tp": TP, "fp": FP, "fn": FN,
    }
