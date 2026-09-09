"""Integration layer between the untouched MorphBPE runtime and the web API.

Nothing in kapampangan_morphbpe_runtime/tokenizer.py or artifacts/ is modified
by this file. What this file adds:

1. `trace_word` — re-runs the exact same merge-selection rule the real
   `Tokenizer._encode_pretoken` uses ("of all adjacent pairs with a learned
   merge rule, apply the one with the lowest rank"), but records every
   intermediate state instead of only the final one, so the UI can render it
   step by step. This is necessarily a *second* implementation of the loop
   (the real one doesn't expose intermediate states), so `verify_fidelity()`
   below cross-checks its output against the real `tokenizer.encode()` for a
   battery of known words at import time and raises if they ever disagree —
   the trace can never silently drift from the real algorithm.

2. `analyze` — orchestrates a whole request: normalizes/pretokenizes with the
   real runtime's own `_pretokenize`, encodes with the real `tokenizer.encode`,
   traces each word for display, and (only when the caller supplies gold
   morpheme boundaries using the SAME "s|in|ulat" convention the team's own
   demo.py CLI uses) scores Boundary F1 / Morphological Consistency F1 using
   the scoring functions copied verbatim into reference_data.py. When no gold
   boundaries are given, only Fertility (which needs no gold data) is
   reported — Boundary F1 / Consistency F1 come back as unavailable rather
   than a fabricated number.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kapampangan_morphbpe_runtime import Tokenizer
from kapampangan_morphbpe_runtime.tokenizer import _pretokenize  # real pretokenizer, reused as-is

import reference_data as ref

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts" / "morphbpe-penalty8"

# Loaded once at import time (same artifact, same checksummed files).
TOKENIZER = Tokenizer(ARTIFACT_DIR)


def trace_word(tok: Tokenizer, surface: str) -> dict[str, Any]:
    """Step-by-step merge trace for one word-pretoken surface string.

    Mirrors Tokenizer._encode_pretoken's rule exactly: repeatedly apply the
    single lowest-rank adjacent-pair merge until none apply. Ties between two
    on-screen occurrences of the *same* rule (same rank) are broken
    left-to-right; since merging non-overlapping duplicates is commutative,
    this never changes the final result versus the real implementation's
    single-pass-per-rank-per-round batching.
    """
    full_id = tok.token_to_id.get(surface)
    if full_id is not None and tok.vocabulary_kind[full_id] != "special":
        return {
            "surface": surface,
            "characters": list(surface),
            "shortcut": True,
            "steps": [],
            "final_tokens": [
                {
                    "token": surface,
                    "id": full_id,
                    "kind": tok.vocabulary_kind[full_id],
                    "start": 0,
                    "end": len(surface),
                }
            ],
        }

    units: list[str] = list(surface)
    # spans track, for every current unit, which slice of the ORIGINAL
    # surface it was built from — kept separate from `units` because an
    # out-of-vocabulary character is displayed as the multi-character
    # "<unk>" placeholder, which must not be confused with its 1-character
    # span in the original word.
    spans: list[tuple[int, int]] = [(i, i + 1) for i in range(len(units))]
    unk_token, unk_id = tok.special_by_role["unk"]
    resolved_units: list[str] = []
    for ch in units:
        if ch in tok.token_to_id:
            resolved_units.append(ch)
        else:
            resolved_units.append(unk_token)
    units = resolved_units

    steps: list[dict[str, Any]] = []
    step_no = 0
    while len(units) > 1:
        candidates = []
        for i in range(len(units) - 1):
            pair = (units[i], units[i + 1])
            ranked = tok.merge_ranks.get(pair)
            if ranked is not None:
                candidates.append((ranked[0], i, pair, ranked[1]))
        if not candidates:
            break
        candidates.sort(key=lambda c: (c[0], c[1]))
        rank, pos, pair, result = candidates[0]
        step_no += 1
        steps.append(
            {
                "step": step_no,
                "candidates": [
                    {"left": c[2][0], "right": c[2][1], "rank": c[0]} for c in candidates
                ],
                "chosen": {
                    "left": pair[0],
                    "right": pair[1],
                    "result": result,
                    "rank": rank,
                    "position": pos,
                },
                "units_after": units[:pos] + [result] + units[pos + 2 :],
            }
        )
        units = units[:pos] + [result] + units[pos + 2 :]
        spans = spans[:pos] + [(spans[pos][0], spans[pos + 1][1])] + spans[pos + 2 :]

    final_tokens = []
    for u, (start, end) in zip(units, spans, strict=True):
        if u == unk_token:
            final_tokens.append(
                {"token": unk_token, "id": unk_id, "kind": "special", "start": start, "end": end}
            )
        else:
            tid = tok.token_to_id[u]
            final_tokens.append(
                {
                    "token": u,
                    "id": tid,
                    "kind": tok.vocabulary_kind[tid],
                    "start": start,
                    "end": end,
                }
            )

    return {
        "surface": surface,
        "characters": list(surface),
        "shortcut": False,
        "steps": steps,
        "final_tokens": final_tokens,
    }


def verify_fidelity() -> tuple[int, int]:
    """Cross-check trace_word() against the real tokenizer.encode() output.

    Returns (passed, total). Raises AssertionError on the first mismatch, so
    a divergence between the display logic and the real algorithm can never
    ship silently.
    """
    test_words: set[str] = set()
    for w, _gloss in ref.WORDS:
        test_words.add(w)
    for sentence in ref.SENTENCES:
        for surface, _spec in sentence:
            test_words.add(surface)
    for _root, _gloss, forms in ref.FAMILIES:
        for surface, _spec in forms:
            test_words.add(surface)
    test_words |= {"kumain", "Kumain", "a", "Masánting", "ing", "mamangan"}

    passed = 0
    for word in sorted(test_words):
        real = [t.token for t in TOKENIZER.encode(word).tokens]
        traced = [t["token"] for t in trace_word(TOKENIZER, word)["final_tokens"]]
        assert real == traced, f"trace/encode mismatch for {word!r}: real={real} traced={traced}"
        passed += 1
    return passed, len(test_words)


def _group_tokens_by_pretoken(tok: Tokenizer, text: str) -> list[list[dict[str, Any]]]:
    """Group tok.encode(text)'s flat token stream back into per-pretoken groups,
    skipping whitespace pretokens as boundaries (mirrors demo.py's _bpe_groups).
    """
    encoding = tok.encode(text)
    groups: list[list[dict[str, Any]]] = [[]]
    for t in encoding.tokens:
        if t.pretoken_kind == "whitespace":
            if groups[-1]:
                groups.append([])
            continue
        groups[-1].append(
            {
                "token": t.token,
                "id": t.identifier,
                "start": t.start,
                "end": t.end,
                "kind": t.vocabulary_kind,
            }
        )
    return [g for g in groups if g]


def analyze(raw_text: str) -> dict[str, Any]:
    if not raw_text or not raw_text.strip():
        return {
            "input": raw_text,
            "clean_text": "",
            "words": [],
            "fertility": None,
            "gold": None,
            "all_tokens": [],
        }

    raw_tokens = raw_text.split()
    sentence: list[tuple[str, str]] = [
        (t.replace("|", ""), t if "|" in t else "") for t in raw_tokens
    ]
    clean_text = " ".join(surface for surface, _ in sentence)
    has_gold = any(spec for _surface, spec in sentence)

    normalized = TOKENIZER.encode(clean_text).normalized_text
    pretokens = _pretokenize(normalized)

    word_reports = []
    for pt in pretokens:
        if pt.kind != "word":
            continue
        word_reports.append(trace_word(TOKENIZER, pt.surface))

    groups = _group_tokens_by_pretoken(TOKENIZER, clean_text)
    group_pieces = [tuple(tok["token"] for tok in g) for g in groups]

    fertility_value = (
        sum(len(g) for g in group_pieces) / len(sentence) if sentence else 0.0
    )

    gold_result = None
    if has_gold and len(group_pieces) == len(sentence):
        rows = ref.rows_for(sentence)
        metrics = ref.score(rows, group_pieces)
        gold_result = {
            "gold_pieces": [list(r["gold_pieces"]) for r in rows],
            "boundary_precision": metrics["boundary_precision"],
            "boundary_recall": metrics["boundary_recall"],
            "boundary_f1": metrics["boundary_f1"],
            "consistency_f1": metrics["mcf1"] if metrics["mcf1_gold_pairs"] > 0 else None,
            "consistency_precision": metrics["mcf1_precision"]
            if metrics["mcf1_gold_pairs"] > 0
            else None,
            "consistency_recall": metrics["mcf1_recall"]
            if metrics["mcf1_gold_pairs"] > 0
            else None,
            "shared_morpheme_pairs": int(metrics["mcf1_gold_pairs"]),
        }

    all_tokens = [
        {
            "token": t.token,
            "id": t.identifier,
            "start": t.start,
            "end": t.end,
            "kind": t.vocabulary_kind,
            "pretoken_kind": t.pretoken_kind,
        }
        for t in TOKENIZER.encode(clean_text).tokens
    ]

    return {
        "input": raw_text,
        "clean_text": clean_text,
        "normalized_text": normalized,
        "words": word_reports,
        "fertility": {
            "tokens": sum(len(g) for g in group_pieces),
            "words": len(sentence),
            "score": fertility_value,
        },
        "gold": gold_result,
        "all_tokens": all_tokens,
    }


def examples() -> dict[str, Any]:
    word_examples = [{"text": w, "gloss": gloss} for w, gloss in ref.WORDS]
    sentence_examples = []
    for sentence in ref.SENTENCES:
        text = " ".join(spec if spec else surface for surface, spec in sentence)
        plain = " ".join(surface for surface, _ in sentence)
        sentence_examples.append({"text": text, "plain": plain})
    family_examples = [
        {
            "root": root,
            "gloss": gloss,
            "text": " ".join(spec for _surface, spec in forms),
        }
        for root, gloss, forms in ref.FAMILIES
    ]
    return {
        "words": word_examples,
        "sentences": sentence_examples,
        "families": family_examples,
    }
