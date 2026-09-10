"""Qualitative retest: run a chosen word list through EVERY v4 tokenizer
candidate and lay the segmentations side by side.

Phase 3's selection picked `penalty-8 @ 6,080` by aggregate boundary F1 on
a *silver* reference. F1 rewards recall (catching boundaries), so it can
favour a tokenizer that over-splits. This script is the eyeball / native-
review companion: per word, see exactly how each of the 25 candidates
(8 MorphBPE-family conditions x 3 vocab sizes + the Unigram-LM ablation)
slices it, whether it matches the silver gold, and a re-scored leaderboard
on *this* word set.

Reads only frozen artifacts + the frozen reference. Writes into a NEW
subdir `reports/segmentation-comparison/`; nothing existing is touched.

    .venv\\Scripts\\python.exe experiments\\tokenizer_selection_v1\\compare_segmentations.py
    ... --words "sumulat,misamban,kabukasan"      # custom list (no gold column)
    ... --n 8                                      # 8 words per process family (default 6)
    ... --all                                      # the whole 534-row reference
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(EXPERIMENT_ROOT))

from run_selection import (  # noqa: E402
    UNIGRAM_CONDITION,
    VOCAB_SIZES,
    _artifact_path,
    _encode_runtime,
    _encode_unigram,
    _pieces_from_boundaries,
    _score,
)

RUNTIME_CONDITIONS = (
    "plain",
    "morphbpe",
    "penalty-1",
    "penalty-2",
    "penalty-4",
    "penalty-8",
    "stochastic-p4-d0.1",
    "stochastic-p4-d0.2",
)
REFERENCE_CSV = EXPERIMENT_ROOT / "data" / "reference-morphology.csv"
OUT_DIR = EXPERIMENT_ROOT / "reports" / "segmentation-comparison"

# always-included illustrative cases (project flagship + the ones the user
# has been eyeballing); deduped against the sample
FLAGSHIP = [
    "misamban",
    "sinulat",
    "sumulat",
    "kabukasan",
    "mamangan",
    "magpakalma",
    "mekipagapir",
    "pemalagyu",
    "sinabi",
    "balayan",
]


def candidates() -> list[tuple[str, int]]:
    out = [(c, v) for c in RUNTIME_CONDITIONS for v in VOCAB_SIZES]
    out.append((UNIGRAM_CONDITION, 6080))  # only vocab-6080 exists for unigram
    return out


def label(condition: str, vocab: int) -> str:
    return f"{condition}@{vocab}"


def load_reference() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    with REFERENCE_CSV.open(encoding="utf-8") as handle:
        for r in csv.DictReader(handle):
            bnds = tuple(int(x) for x in r["boundaries"].split()) if r["boundaries"].strip() else ()
            rows[r["surface"]] = {
                "surface": r["surface"],
                "gold_boundaries": set(bnds),
                "gold_pieces": _pieces_from_boundaries(r["surface"], bnds),
                "n_boundaries": len(bnds),
                "process": r["process"],
                "provenance": r["provenance"],
                "tier": r["source_tier"],
                "freq": int(r["freq_in_sources"]) if r["freq_in_sources"].strip() else 0,
            }
    return rows


def _stub(w: str) -> dict[str, Any]:
    return {
        "surface": w,
        "gold_boundaries": set(),
        "gold_pieces": (w,),
        "n_boundaries": 0,
        "process": "(flagship, no ref gold)",
        "provenance": "(custom)",
        "tier": "(custom)",
        "freq": 0,
    }


def pick_words(args: argparse.Namespace, ref: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if args.words:
        return [ref.get(w.strip(), _stub(w.strip())) for w in args.words.split(",") if w.strip()]
    if args.all:
        return sorted(ref.values(), key=lambda r: (r["process"], -r["freq"], r["surface"]))
    # default: the flagship set (always) + a frequency-SPREAD sample per
    # process family, so the sample has both memorised-whole high-freq words
    # and lower-freq words where the tokenizers actually diverge.
    by_process: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in ref.values():
        by_process[r["process"]].append(r)
    chosen: dict[str, dict[str, Any]] = {w: ref.get(w, _stub(w)) for w in FLAGSHIP}
    for _proc, group in sorted(by_process.items()):
        ordered = sorted(group, key=lambda r: (-r["freq"], r["surface"]))
        step = max(1, len(ordered) // args.n)
        for r in ordered[::step][: args.n]:
            chosen.setdefault(r["surface"], r)
    return sorted(chosen.values(), key=lambda r: (r["process"], -r["freq"], r["surface"]))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--words", help="comma-separated custom word list (no gold column)")
    ap.add_argument("--n", type=int, default=6, help="words per process family in the sample")
    ap.add_argument("--all", action="store_true", help="use the whole reference set")
    args = ap.parse_args()

    ref = load_reference()
    rows = pick_words(args, ref)
    have_gold = not args.words
    # custom / --all runs write their own files so nothing clobbers the canonical sample
    suffix = ".custom" if args.words else (".all" if args.all else "")
    print(f"{len(rows)} words x {len(candidates())} candidates")

    # encode every word through every candidate
    seg: dict[str, list[tuple[str, ...]]] = {}
    scores: dict[str, dict[str, float]] = {}
    for condition, vocab in candidates():
        path = _artifact_path(condition, vocab)
        if not path.exists():
            continue
        enc = (
            _encode_unigram(path, rows)
            if condition == UNIGRAM_CONDITION
            else _encode_runtime(path, rows)
        )
        seg[label(condition, vocab)] = enc
        if have_gold:
            scores[label(condition, vocab)] = _score(rows, enc)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    names = list(seg)

    # ---- wide.csv ----
    with (OUT_DIR / f"wide{suffix}.csv").open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle, lineterminator="\n")
        head = ["surface", "process", "tier"] + (["silver_gold"] if have_gold else []) + names
        w.writerow(head)
        for i, r in enumerate(rows):
            cells = [r["surface"], r["process"], r["tier"]]
            if have_gold:
                cells.append("+".join(r["gold_pieces"]))
            cells += ["+".join(seg[n][i]) for n in names]
            w.writerow(cells)

    # ---- native-review.csv ----
    with (OUT_DIR / f"native-review{suffix}.csv").open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle, lineterminator="\n")
        w.writerow(
            ["surface", "process"]
            + (["silver_gold_guess"] if have_gold else [])
            + names
            + ["correct_segmentation", "best_version", "notes"]
        )
        for i, r in enumerate(rows):
            cells = [r["surface"], r["process"]]
            if have_gold:
                cells.append("+".join(r["gold_pieces"]))
            cells += ["+".join(seg[n][i]) for n in names]
            w.writerow([*cells, "", "", ""])

    # ---- by-word.md ----
    lines = [
        "# v4 tokenizer segmentation - side by side",
        "",
        f"{len(rows)} words, {len(names)} candidates. `silver_gold` is the "
        "held-out reference used by Phase 3 selection - **silver, not native "
        "gold**. `==` marks an exact whole-word match.",
        "",
    ]
    for i, r in enumerate(rows):
        lines.append(f"## `{r['surface']}`  ({r['process']}, tier {r['tier']})")
        lines.append("")
        if have_gold:
            lines.append(f"**silver gold:** `{'+'.join(r['gold_pieces'])}`")
            lines.append("")
        lines.append("| candidate | segmentation | == gold | n |")
        lines.append("|---|---|:--:|--:|")
        for n in names:
            pieces = seg[n][i]
            hit = "OK" if have_gold and pieces == r["gold_pieces"] else ""
            lines.append(f"| {n} | `{'+'.join(pieces)}` | {hit} | {len(pieces)} |")
        lines.append("")
    (OUT_DIR / f"by-word{suffix}.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")

    # ---- summary.md : re-scored leaderboard on THIS word set ----
    if have_gold:
        ranked = sorted(scores.items(), key=lambda kv: -kv[1]["boundary_f1"])
        s = [
            "# Re-scored on this word set",
            "",
            f"{len(rows)} words. Same metrics as Phase 3 selection, this subset "
            "only. `exact` = whole-word match rate; `fert` = mean pieces/word.",
            "",
            "| candidate | F1 | prec | recall | exact | MCF1 | fert |",
            "|---|--:|--:|--:|--:|--:|--:|",
        ]
        for name, m in ranked:
            s.append(
                f"| {name} | {m['boundary_f1']:.3f} | {m['boundary_precision']:.3f} | "
                f"{m['boundary_recall']:.3f} | {m['exact_match']:.3f} | {m['mcf1']:.3f} | "
                f"{m['fertility']:.2f} |"
            )
        s.append("")
        s.append("Top by each metric:")
        for mk, lbl in (
            ("boundary_f1", "F1"),
            ("exact_match", "exact-match"),
            ("boundary_precision", "precision"),
            ("mcf1", "MCF1"),
        ):
            top_name, top_m = max(scores.items(), key=lambda kv: kv[1][mk])
            s.append(f"- **{lbl}**: `{top_name}` = {top_m[mk]:.3f}")
        (OUT_DIR / f"summary{suffix}.md").write_text(
            "\n".join(s) + "\n", encoding="utf-8", newline="\n"
        )
        print("\n".join(s))

    print(
        f"\nwrote {OUT_DIR}/  (by-word.md, wide.csv, native-review.csv"
        + (", summary.md" if have_gold else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
