#!/usr/bin/env python3
"""Kapampangan MorphBPE — presentation demo (3-way).

Compares three subword tokenizers, all trained on the same Kapampangan
corpus at vocab 6,080 with the same special tokens:

  * MorphBPE   — penalty-8, the Phase-3-selected tokenizer
  * Plain BPE  — identical BPE, morphology penalty switched off
  * Unigram-LM — NLLB's own subword algorithm (SentencePiece Unigram),
                 trained from scratch on this corpus (the `unigram-ablation`
                 artifact); decoded here with a small stdlib Viterbi that
                 matches the `tokenizers` library exactly

Shows the raw split for a handful of words, a shared-root consistency
demo, and the three intrinsic thesis metrics per sentence:

    1.1  Fertility Rate                 pieces per word; lower = tighter
    1.2  Morpheme Boundary F1           do cuts land on gold boundaries?
    1.3  Morphological Consistency F1   is a shared morpheme cut alike?

Scoring functions are lifted verbatim from the research repo
`experiments/tokenizer_selection_v1/run_selection.py`; gold morpheme splits
are from that experiment's frozen `reference-morphology.csv` (silver, not
native gold).

Pure standard library. Python 3.11+. No `pip install`, no internet.

    python demo.py
    python demo.py "malagu ya at masanting"          # split + fertility (1.1)
    python demo.py "d|in|atang ya s|in|ulat ne"      # '|' = gold morpheme
                                                     #  boundary -> all 3 metrics
"""

from __future__ import annotations

import contextlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

with contextlib.suppress(Exception):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from kapampangan_morphbpe_runtime import Tokenizer  # noqa: E402

SKIP_KINDS = {"whitespace"}
MCF1_MIN_LEN = 2
MCF1_MAX_GROUP = 300


class UnigramLM:
    """Minimal SentencePiece-Unigram decoder (Viterbi best-path).

    Reads a Hugging Face `tokenizers` Unigram `tokenizer.json` (a list of
    ``[piece, log_prob]``). Verified piece-for-piece against
    `tokenizers.Tokenizer.from_file(...).encode()`.
    """

    def __init__(self, tokenizer_json: Path) -> None:
        doc = json.loads(tokenizer_json.read_text(encoding="utf-8"))
        model = doc["model"]
        if model.get("type") != "Unigram":
            raise ValueError("not a Unigram tokenizer.json")
        specials = {"<pad>", "<s>", "</s>"}
        self.score: dict[str, float] = {
            piece: logp for piece, logp in model["vocab"] if piece not in specials
        }
        self.vocabulary_size = len(model["vocab"])
        self._unk = min(s for s in self.score.values() if s < 0) - 10.0

    def encode(self, word: str) -> list[str]:
        n = len(word)
        best: list[tuple[float, int, str]] = [(-math.inf, -1, "")] * (n + 1)
        best[0] = (0.0, -1, "")
        for i in range(1, n + 1):
            choice = (-math.inf, -1, "")
            for j in range(i):
                if best[j][0] == -math.inf:
                    continue
                piece = word[j:i]
                sc = self.score.get(piece)
                if sc is not None:
                    cand = (best[j][0] + sc, j, piece)
                    if cand[0] > choice[0]:
                        choice = cand
            unk = (best[i - 1][0] + self._unk, i - 1, "<unk>")
            if best[i - 1][0] != -math.inf and unk[0] > choice[0]:
                choice = unk
            best[i] = choice
        out: list[str] = []
        i = n
        while i > 0:
            _, j, piece = best[i]
            out.append(piece)
            i = j
        out.reverse()
        merged: list[str] = []
        for p in out:
            if p == "<unk>" and merged and merged[-1] == "<unk>":
                continue
            merged.append(p)
        return merged


MORPH = Tokenizer(HERE / "morphbpe-penalty8")
PLAIN = Tokenizer(HERE / "plain-bpe")
UNI = UnigramLM(HERE / "unigram-lm-6080" / "tokenizer.json")
NAMES = ("MorphBPE", "Plain BPE", "Unigram-LM")

# --- raw-split showcase (no metrics) --------------------------------------
WORDS = [
    ("sinulat", "wrote"),
    ("kabukasan", "tomorrow / the future"),
    ("magsalita", "to speak"),
    ("pipaglutuan", "kitchen / place for cooking"),
    ("mamangan", "to eat"),
    ("sumulat", "to write"),
]

# --- scored sentences ----------------------------------------------------
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

# --- word families for consistency (1.3): one root, several affixed forms ---
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


# ---------------------------------------------------------------------------
# scoring — verbatim from experiments/tokenizer_selection_v1/run_selection.py
# ---------------------------------------------------------------------------
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


def _mcf1(rows: list[dict[str, Any]], encoded_pieces: list[tuple[str, ...]]) -> dict[str, float]:
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


def _score(rows: list[dict[str, Any]], encoded: list[tuple[str, ...]]) -> dict[str, float]:
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
        "fertility": produced / len(rows),
    }
    out.update(_mcf1(rows, encoded))
    return out


# ---------------------------------------------------------------------------
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


def rule(char: str = "-") -> None:
    print(char * 70)


def header() -> None:
    rule("=")
    print("  Kapampangan tokenizers  ·  MorphBPE vs Plain BPE vs Unigram-LM")
    rule("=")
    print("  boundary F1 on the full held-out morphology set  (Phase 3)")
    print("  all rows: same Kapampangan corpus, vocab 6,080, same specials")
    print("     MorphBPE  penalty-8        0.4639 dev   0.4093 test   <- selected")
    print("     Unigram-LM (NLLB's algo)   0.293  dev")
    print("     MorphBPE  hard-constrained 0.268  dev")
    print("     Plain BPE                  0.198  dev")


def word_section() -> None:
    print()
    rule()
    print("  WORD SPLITS      '+' = subword join")
    rule()
    for w, gloss in WORDS:
        print(f"  {w}   — {gloss}")
        for name, pieces in split_word(w).items():
            print(f"      {name:<11}({len(pieces)})  {' + '.join(pieces)}")
        print()


def family_section() -> None:
    print()
    rule()
    print("  CONSISTENCY (1.3) — one root, several forms")
    rule()
    print("  consistency F1: of the word-pairs that share a gold morpheme,")
    print("  how many also share a token?  (root kept as one piece everywhere)")
    print()
    for root, gloss, forms in FAMILIES:
        rows = [
            {"surface": s, "gold_boundaries": set(), "gold_pieces": tuple(seg.split("|"))}
            for s, seg in forms
        ]
        enc = {n: [tuple(split_word(s)[n]) for s, _ in forms] for n in NAMES}
        scored = {n: _mcf1(rows, enc[n]) for n in NAMES}
        pairs = int(scored["MorphBPE"]["mcf1_gold_pairs"])
        print(f"  root '{root}'  ({gloss})  — {pairs} word-pairs share this root")
        print((f"      {'form':<13}{'gold':<15}" + "".join(f"{n:<15}" for n in NAMES)).rstrip())
        for i, (s, seg) in enumerate(forms):
            cells = "".join(f"{'+'.join(enc[n][i]):<15}" for n in NAMES)
            print(f"      {s:<13}{'·'.join(seg.split('|')):<15}{cells}".rstrip())
        summary = "   ".join(f"{n.split()[0]} {scored[n]['mcf1']:.2f}" for n in NAMES)
        print(f"      consistency F1:  {summary}")
        print()


def _bf1(m: dict[str, float]) -> str:
    return f"{m['boundary_f1']:.2f} (P{m['boundary_precision']:.2f} R{m['boundary_recall']:.2f})"


def _cf1(m: dict[str, float]) -> str:
    if m["mcf1_gold_pairs"] == 0:
        return "n/a"
    return f"{m['mcf1']:.2f} (P{m['mcf1_precision']:.2f} R{m['mcf1_recall']:.2f})"


def _metric_table(rows: list[dict[str, Any]], enc: dict[str, list[tuple[str, ...]]]) -> None:
    print(f"      {'':<11}{'1.1 fert':<10}{'1.2 boundary F1':<21}1.3 consistency F1")
    for name in NAMES:
        m = _score(rows, enc[name])
        print(f"      {name:<11}{m['fertility']:<10.3f}{_bf1(m):<21}{_cf1(m)}")


def _print_splits(enc: dict[str, list[tuple[str, ...]]]) -> None:
    for name in NAMES:
        print(f"      {name:<11}{'  |  '.join('+'.join(g) for g in enc[name])}")


def sentence_section() -> None:
    print()
    rule()
    print("  SENTENCES — the three intrinsic metrics, per sentence")
    rule()
    print("  1.1 fertility        pieces / word          — lower = tighter")
    print("  1.2 boundary F1      cuts that land on a gold morpheme boundary")
    print("  1.3 consistency F1   a morpheme shared by two words, cut alike")
    print()
    pooled_rows: list[dict[str, Any]] = []
    pooled: dict[str, list[tuple[str, ...]]] = {n: [] for n in NAMES}
    for sentence in SENTENCES:
        text = " ".join(w for w, _ in sentence)
        rows = rows_for(sentence)
        enc = groups_by_tokenizer(text)
        pairs = int(_mcf1(rows, enc["MorphBPE"])["mcf1_gold_pairs"])
        print(f'  "{text}"')
        print(
            f"      gold: {'  '.join('-'.join(r['gold_pieces']) for r in rows)}"
            f"   ({pairs} shared-morpheme pair{'s' if pairs != 1 else ''})"
        )
        _print_splits(enc)
        _metric_table(rows, enc)
        print()
        pooled_rows += rows
        for n in NAMES:
            pooled[n] += enc[n]
    rule()
    print(f"  POOLED over all {len(SENTENCES)} sentences ({len(pooled_rows)} words)")
    _metric_table(pooled_rows, pooled)
    print()
    print("  (hand-picked words — the header has the real Phase 3 aggregate.)")


def custom_section(sentences: list[str]) -> None:
    print()
    rule()
    print("  CUSTOM INPUT")
    rule()
    print("  Mark gold morpheme boundaries with '|' to score all three metrics:")
    print('     python demo.py "d|in|atang ya at s|in|ulat ne"')
    print("  Unmarked words count as one morpheme. No '|' anywhere -> 1.1 only.")
    print()
    for s in sentences:
        tokens = s.split()
        sentence = [(t.replace("|", ""), t if "|" in t else "") for t in tokens]
        text = " ".join(w for w, _ in sentence)
        enc = groups_by_tokenizer(text)
        print(f'  "{text}"')
        if any(spec for _, spec in sentence):
            rows = rows_for(sentence)
            pairs = int(_mcf1(rows, enc["MorphBPE"])["mcf1_gold_pairs"])
            print(
                f"      gold: {'  '.join('-'.join(r['gold_pieces']) for r in rows)}"
                f"   ({pairs} shared-morpheme pair{'s' if pairs != 1 else ''})"
            )
            _print_splits(enc)
            _metric_table(rows, enc)
        else:
            nwords = len(tokens)
            _print_splits(enc)
            cells = "   ".join(
                f"{n.split()[0]} {sum(len(g) for g in enc[n]) / nwords:.3f}" for n in NAMES
            )
            print(f"      1.1 fertility   {cells}   ({nwords} words)")
        print()


def main() -> int:
    header()
    word_section()
    args = sys.argv[1:]
    if args:
        custom_section(args)
    else:
        family_section()
        sentence_section()
    print()
    rule("=")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
