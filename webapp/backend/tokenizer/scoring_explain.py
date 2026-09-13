"""Diagnostic ("show your work") versions of reference_data.py's scoring.

reference_data.py stays byte-for-byte the verbatim copy of the team's own
scoring code (see its module docstring) — nothing there is touched. The
functions below are a *second*, deliberately transparent implementation of
the exact same two loops (`score()`'s boundary comparison and `mcf1()`'s
pair-matching), except they keep every intermediate value — per-word
predicted/gold cut positions, which words got grouped by which shared
morpheme/token, which pairs counted as a true/false positive/negative —
instead of collapsing straight to precision/recall/F1. That intermediate
bookkeeping is what the Comparison tab's "How these scores are computed"
panel renders.

Because this is necessarily a second implementation (mirroring
`trace_service.trace_word` mirroring the real tokenizer's merge loop), it
carries the same safety net: `comparison_service.verify_scoring_fidelity()`
runs at server startup and asserts these functions produce the exact same
precision/recall/F1 as `reference_data.score()` / `reference_data.mcf1()`
for the project's own gold data. If the two ever disagreed, the server
would refuse to start — the "how it's computed" numbers shown to a
panelist can never drift from the real Boundary F1 / Consistency F1.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import reference_data as ref


def explain_boundary(rows: list[dict[str, Any]], encoded: list[tuple[str, ...]]) -> dict[str, Any]:
    """Same loop as reference_data.score(), with per-word bookkeeping kept.

    For each word: the tokenizer's pieces are turned into predicted cut
    positions (running character offset after every piece except the last —
    identical to score()'s `acc`/`pred` construction), then compared against
    that word's gold cut positions.
    """
    per_word: list[dict[str, Any]] = []
    tp = fp = fn = 0
    produced = 0
    for row, pieces in zip(rows, encoded, strict=True):
        pred: set[int] = set()
        acc = 0
        for piece in pieces[:-1]:
            acc += len(piece)
            pred.add(acc)
        gold = row["gold_boundaries"]
        word_tp = sorted(gold & pred)
        word_fp = sorted(pred - gold)
        word_fn = sorted(gold - pred)
        tp += len(word_tp)
        fp += len(word_fp)
        fn += len(word_fn)
        produced += len(pieces)
        per_word.append(
            {
                "surface": row["surface"],
                "gold_pieces": list(row["gold_pieces"]),
                "pred_pieces": list(pieces),
                "gold_boundaries": sorted(gold),
                "pred_boundaries": sorted(pred),
                "tp_boundaries": word_tp,
                "fp_boundaries": word_fp,
                "fn_boundaries": word_fn,
            }
        )
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return {
        "per_word": per_word,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": p,
        "recall": r,
        "f1": f1,
        "tokens_produced": produced,
        "word_count": len(rows),
    }


def _pair_words(rows: list[dict[str, Any]], pairs: set[tuple[int, int]]) -> list[list[str]]:
    return [[rows[i]["surface"], rows[j]["surface"]] for (i, j) in sorted(pairs)]


def explain_consistency(rows: list[dict[str, Any]], encoded: list[tuple[str, ...]]) -> dict[str, Any]:
    """Same grouping/pairing as reference_data.mcf1(), with the groups and
    the actual word-pairs behind TP/FP/FN kept instead of only their counts.
    """
    morpheme_sets = [
        frozenset(p for p in r["gold_pieces"] if len(p) >= ref.MCF1_MIN_LEN) for r in rows
    ]
    token_sets = [
        frozenset(p for p in pieces if len(p) >= ref.MCF1_MIN_LEN) for pieces in encoded
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
    contributing_morpheme_groups = []
    for morpheme, members in morpheme_groups.items():
        if len(members) >= 2:
            pairs = ref._capped_pairs(members, ref.MCF1_MAX_GROUP)
            mpairs |= pairs
            contributing_morpheme_groups.append(
                {"morpheme": morpheme, "words": [rows[i]["surface"] for i in members]}
            )

    tpairs: set[tuple[int, int]] = set()
    contributing_token_groups = []
    for token, members in token_groups.items():
        if len(members) >= 2:
            pairs = ref._capped_pairs(members, ref.MCF1_MAX_GROUP)
            tpairs |= pairs
            contributing_token_groups.append(
                {"token": token, "words": [rows[i]["surface"] for i in members]}
            )

    tp_pairs = mpairs & tpairs
    fn_pairs = mpairs - tpairs
    fp_pairs = tpairs - mpairs
    tp, fn, fp = len(tp_pairs), len(fn_pairs), len(fp_pairs)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0

    return {
        "morpheme_groups": contributing_morpheme_groups,
        "token_groups": contributing_token_groups,
        "shared_morpheme_pairs": len(mpairs),
        "shared_token_pairs": len(tpairs),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tp_pairs": _pair_words(rows, tp_pairs),
        "fp_pairs": _pair_words(rows, fp_pairs),
        "fn_pairs": _pair_words(rows, fn_pairs),
        "precision": p,
        "recall": r,
        "f1": f1,
    }
