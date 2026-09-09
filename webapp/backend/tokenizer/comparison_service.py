"""3-way tokenizer comparison (MorphBPE penalty-8 vs Plain BPE vs Unigram-LM).

Everything computed here reuses, unchanged:
  - the real Tokenizer.encode() for MorphBPE and Plain BPE
  - the real UnigramLM.encode() (verbatim from demo.py, see unigram_lm.py)
  - the scoring functions in reference_data.py (also verbatim from demo.py)
  - reference_data.rows_for(), for turning "|"-marked gold morphemes into
    the same boundary/piece representation demo.py itself uses

`_bpe_groups`, `groups_by_tokenizer`, and `split_word` are straight ports of
the same-named functions in the team's own demo.py.

The Comparison tab always compares whatever text you last tokenized on the
Tokenizer tab (there is no separate example showcase or static input box
here anymore) — `custom_compare()` is the single entry point, called for
every request.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from kapampangan_morphbpe_runtime import Tokenizer

import reference_data as ref
import scoring_explain
from unigram_lm import UnigramLM

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"

MORPH = Tokenizer(ARTIFACTS / "morphbpe-penalty8")
PLAIN = Tokenizer(ARTIFACTS / "plain-bpe")
UNI = UnigramLM(ARTIFACTS / "unigram-lm-6080" / "tokenizer.json")
NAMES = ("MorphBPE", "Plain BPE", "Unigram-LM")

SKIP_KINDS = {"whitespace"}


def _bpe_groups(tok: Tokenizer, text: str) -> list[list[str]]:
    groups: list[list[str]] = [[]]
    for t in tok.encode(text).tokens:
        if t.pretoken_kind in SKIP_KINDS:
            if groups[-1]:
                groups.append([])
            continue
        groups[-1].append(t.token)
    return [g for g in groups if g]


def groups_by_tokenizer(text: str) -> dict[str, list[tuple[str, ...]]]:
    """Per-word piece tuples for each tokenizer, aligned word-for-word."""
    m = [tuple(g) for g in _bpe_groups(MORPH, text)]
    p = [tuple(g) for g in _bpe_groups(PLAIN, text)]
    surfaces = ["".join(g) for g in m]  # normalized + pretokenized word surfaces
    u = [tuple(UNI.encode(s)) for s in surfaces]
    return {"MorphBPE": m, "Plain BPE": p, "Unigram-LM": u}


def split_word(word: str) -> dict[str, list[str]]:
    return {
        "MorphBPE": [t.token for t in MORPH.encode(word).tokens],
        "Plain BPE": [t.token for t in PLAIN.encode(word).tokens],
        "Unigram-LM": UNI.encode(word),
    }


def custom_compare(raw_text: str) -> dict[str, Any] | None:
    """3-way comparison for whatever text was just tokenized on the
    Tokenizer tab: same '|' gold-boundary convention as trace_service.analyze
    (mark gold morpheme boundaries with e.g. `s|in|ulat`), scored against all
    three tokenizers side by side instead of just MorphBPE.
    """
    if not raw_text or not raw_text.strip():
        return None
    raw_tokens = raw_text.split()
    sentence = [(t.replace("|", ""), t if "|" in t else "") for t in raw_tokens]
    text = " ".join(surface for surface, _ in sentence)
    has_gold = any(spec for _surface, spec in sentence)

    enc = groups_by_tokenizer(text)
    result: dict[str, Any] = {
        "input": raw_text,
        "clean_text": text,
        "splits": {n: [list(g) for g in enc[n]] for n in NAMES},
        "fertility": {
            n: {
                "tokens": sum(len(g) for g in enc[n]),
                "words": len(sentence),
                "score": (sum(len(g) for g in enc[n]) / len(sentence)) if sentence else 0.0,
            }
            for n in NAMES
        },
        "gold": None,
    }
    if has_gold and all(len(enc[n]) == len(sentence) for n in NAMES):
        rows = ref.rows_for(sentence)
        shared_pairs = int(ref.mcf1(rows, enc["MorphBPE"])["mcf1_gold_pairs"])
        metrics = {n: ref.score(rows, enc[n]) for n in NAMES}
        explain = {
            n: {
                "boundary": scoring_explain.explain_boundary(rows, enc[n]),
                "consistency": scoring_explain.explain_consistency(rows, enc[n]),
            }
            for n in NAMES
        }
        result["gold"] = {
            "gold_pieces": [list(r["gold_pieces"]) for r in rows],
            "shared_pairs": shared_pairs,
            "metrics": metrics,
            "explain": explain,
        }
    return result


def verify_scoring_fidelity() -> tuple[int, int]:
    """Cross-check scoring_explain's precision/recall/F1 against
    reference_data.score()/mcf1() on the project's own gold data (pooled
    SENTENCES for boundary+consistency, FAMILIES forms for consistency),
    for all three tokenizers. Raises AssertionError on any mismatch.
    """
    checks = 0

    pooled_rows: list[dict[str, Any]] = []
    pooled_enc: dict[str, list[tuple[str, ...]]] = {n: [] for n in NAMES}
    for sentence in ref.SENTENCES:
        text = " ".join(w for w, _ in sentence)
        rows = ref.rows_for(sentence)
        enc = groups_by_tokenizer(text)
        pooled_rows += rows
        for n in NAMES:
            pooled_enc[n] += enc[n]

    for n in NAMES:
        real = ref.score(pooled_rows, pooled_enc[n])
        mine_b = scoring_explain.explain_boundary(pooled_rows, pooled_enc[n])
        mine_c = scoring_explain.explain_consistency(pooled_rows, pooled_enc[n])
        assert math.isclose(real["boundary_precision"], mine_b["precision"], abs_tol=1e-9), n
        assert math.isclose(real["boundary_recall"], mine_b["recall"], abs_tol=1e-9), n
        assert math.isclose(real["boundary_f1"], mine_b["f1"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_precision"], mine_c["precision"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_recall"], mine_c["recall"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1"], mine_c["f1"], abs_tol=1e-9), n
        assert int(real["mcf1_gold_pairs"]) == mine_c["shared_morpheme_pairs"], n
        checks += 1

    family_rows: list[dict[str, Any]] = []
    family_enc: dict[str, list[tuple[str, ...]]] = {n: [] for n in NAMES}
    for _root, _gloss, forms in ref.FAMILIES:
        for surface, seg in forms:
            family_rows.append(
                {"surface": surface, "gold_boundaries": set(), "gold_pieces": tuple(seg.split("|"))}
            )
        splits = {n: [tuple(split_word(s)[n]) for s, _ in forms] for n in NAMES}
        for n in NAMES:
            family_enc[n] += splits[n]

    for n in NAMES:
        real = ref.mcf1(family_rows, family_enc[n])
        mine_c = scoring_explain.explain_consistency(family_rows, family_enc[n])
        assert math.isclose(real["mcf1_precision"], mine_c["precision"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_recall"], mine_c["recall"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1"], mine_c["f1"], abs_tol=1e-9), n
        checks += 1

    return checks, checks
