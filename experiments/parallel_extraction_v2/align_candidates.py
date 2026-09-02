"""Phase 3 data step (parallel_extraction_v2), part 2: score every
PAM x FIL candidate pair inside each alignment unit and emit a
reviewer-ready candidate list.

Two independent signals, kept side by side so the reviewer can weigh them:
  * emb_cosine   -- cosine of multilingual sentence embeddings (LaBSE by
                    default; a model built for translation-pair mining).
                    Kapampangan is not in LaBSE's training languages, but it
                    shares heavy surface vocabulary with Tagalog, so
                    cross-lingual retrieval still surfaces real pairs for a
                    human to confirm.
  * token_jaccard / char3_cosine -- pure lexical overlap. Kapampangan<->
                    Filipino true pairs often share many cognates, so this
                    catches pairs even when the embedding is lukewarm, and
                    flags "too similar" spurious matches (same named entity).
  * mutual_best  -- f is p's top-1 by emb_cosine AND p is f's top-1. The
                    standard high-precision bitext-mining filter.

Output rows are NOT verified pairs. They are candidates for human review
(blank reviewer_verdict / reviewer_notes columns), exactly like
parallel_extraction_v1's process. Nothing here is added to any dataset.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np

EXPERIMENT_ROOT = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
POOLS_JSON = DATA_DIR / "sentence-pools.json"
CANDIDATES_CSV = DATA_DIR / "candidate-pairs.csv"
REVIEW_ORDER_CSV = DATA_DIR / "candidate-pairs-review-order.csv"
SUMMARY_MD = REPORTS_DIR / "alignment-summary.md"
STATS_JSON = REPORTS_DIR / "alignment-stats.json"

DEFAULT_MODEL = "sentence-transformers/LaBSE"
EMB_KEEP = 0.62  # keep a pair if emb_cosine >= this ...
JACCARD_KEEP = 0.30  # ... OR token_jaccard >= this
TOP_K = 3  # per PAM sentence, keep its K best FIL by emb_cosine

_TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
_WS = re.compile(r"\s+")


def tokens(text: str) -> set[str]:
    return {t.casefold() for t in _TOKEN.findall(text)}


def token_jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def char_ngrams(text: str, n: int = 3) -> set[str]:
    collapsed = _WS.sub(" ", text.casefold().strip())
    s = f" {collapsed} "
    return {s[i : i + n] for i in range(len(s) - n + 1)}


def char3_cosine(a: str, b: str) -> float:
    ga, gb = char_ngrams(a), char_ngrams(b)
    if not ga or not gb:
        return 0.0
    inter = len(ga & gb)
    return float(inter / ((len(ga) ** 0.5) * (len(gb) ** 0.5)))


def length_ratio(a: str, b: str) -> float:
    la, lb = len(a.split()), len(b.split())
    if la == 0 or lb == 0:
        return 0.0
    return min(la, lb) / max(la, lb)


def blended(emb: float, jac: float, c3: float, lr: float, mnn: bool) -> float:
    return round(0.6 * emb + 0.2 * jac + 0.1 * c3 + 0.1 * lr + (0.05 if mnn else 0.0), 4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--emb-keep", type=float, default=EMB_KEEP)
    parser.add_argument("--jaccard-keep", type=float, default=JACCARD_KEEP)
    parser.add_argument("--top-k", type=int, default=TOP_K)
    args = parser.parse_args()

    if not POOLS_JSON.exists():
        print(f"missing {POOLS_JSON}; run build_pools.py first", file=sys.stderr)
        return 1
    units: dict[str, dict[str, list[str]]] = json.loads(POOLS_JSON.read_text(encoding="utf-8"))

    from sentence_transformers import SentenceTransformer

    print(f"loading {args.model} ...", flush=True)
    model = SentenceTransformer(args.model)

    rows: list[dict[str, object]] = []
    per_unit_stats: dict[str, dict[str, int]] = {}

    for unit, pool in units.items():
        pam, fil = pool["pam"], pool["fil"]
        if not pam or not fil:
            continue
        pe = model.encode(pam, normalize_embeddings=True, show_progress_bar=False)
        fe = model.encode(fil, normalize_embeddings=True, show_progress_bar=False)
        sim = np.asarray(pe) @ np.asarray(fe).T  # (len(pam), len(fil)), cosine

        fil_argmax_for_pam = sim.argmax(axis=1)
        pam_argmax_for_fil = sim.argmax(axis=0)

        kept = 0
        for i, p in enumerate(pam):
            order = np.argsort(-sim[i])[: args.top_k]
            for j in order:
                emb = float(sim[i, j])
                jac = token_jaccard(p, fil[j])
                if emb < args.emb_keep and jac < args.jaccard_keep:
                    continue
                mnn = bool(fil_argmax_for_pam[i] == j and pam_argmax_for_fil[j] == i)
                c3 = char3_cosine(p, fil[j])
                lr = length_ratio(p, fil[j])
                rows.append(
                    {
                        "unit": unit,
                        "pam_text": p,
                        "fil_text": fil[j],
                        "emb_cosine": round(emb, 4),
                        "token_jaccard": round(jac, 4),
                        "char3_cosine": round(c3, 4),
                        "length_ratio": round(lr, 4),
                        "mutual_best": mnn,
                        "blended_score": blended(emb, jac, c3, lr, mnn),
                        "reviewer_verdict": "",
                        "reviewer_notes": "",
                    }
                )
                kept += 1
        per_unit_stats[unit] = {
            "pam": len(pam),
            "fil": len(fil),
            "candidates_kept": kept,
        }

    rows.sort(key=lambda r: (r["unit"], -float(r["blended_score"])))  # type: ignore[arg-type]

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "unit",
        "pam_text",
        "fil_text",
        "emb_cosine",
        "token_jaccard",
        "char3_cosine",
        "length_ratio",
        "mutual_best",
        "blended_score",
        "reviewer_verdict",
        "reviewer_notes",
    ]
    with CANDIDATES_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    # review-priority ordering: mutual-best first, then by blended score.
    review_rows = sorted(
        rows,
        key=lambda r: (not r["mutual_best"], -float(r["blended_score"])),  # type: ignore[arg-type]
    )
    with REVIEW_ORDER_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(review_rows)

    mnn_rows = [r for r in rows if r["mutual_best"]]
    strong = [r for r in rows if float(r["emb_cosine"]) >= 0.80]  # type: ignore[arg-type]
    stats = {
        "model": args.model,
        "thresholds": {
            "emb_keep": args.emb_keep,
            "jaccard_keep": args.jaccard_keep,
            "top_k": args.top_k,
        },
        "units": len(per_unit_stats),
        "candidate_rows": len(rows),
        "mutual_best_rows": len(mnn_rows),
        "emb_cosine_ge_0.80_rows": len(strong),
        "per_unit": per_unit_stats,
        "label": "CANDIDATES for human review, not verified pairs",
    }
    STATS_JSON.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# parallel_extraction_v2 -- PLD full-pool alignment (candidate sweep)",
        "",
        f"Model: `{args.model}`. Thresholds: emb_cosine >= {args.emb_keep} OR "
        f"token_jaccard >= {args.jaccard_keep}, top-{args.top_k} FIL per PAM.",
        "",
        "**Every row is a CANDIDATE for human review, not a verified pair.** "
        "Same discipline as parallel_extraction_v1: nothing here enters a "
        "dataset until reviewed. `mutual_best` (reciprocal nearest neighbour) "
        "is the highest-precision subset; `emb_cosine >= 0.80` is a strong "
        "secondary signal.",
        "",
        f"- candidate rows: **{len(rows)}**",
        f"- of which mutual-best: **{len(mnn_rows)}**",
        f"- of which emb_cosine >= 0.80: **{len(strong)}**",
        "",
        "| unit | PAM | FIL | candidates | mutual-best |",
        "|---|---:|---:|---:|---:|",
    ]
    for unit, s in per_unit_stats.items():
        mb = sum(1 for r in mnn_rows if r["unit"] == unit)
        lines.append(f"| {unit} | {s['pam']} | {s['fil']} | {s['candidates_kept']} | {mb} |")
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(json.dumps(stats, indent=2))
    print(f"\nwrote {CANDIDATES_CSV}")
    print(f"wrote {SUMMARY_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
