"""Phase 3 Part 1, step 3: score every trained candidate on the frozen
DEV/TEST morphology reference and select a configuration.

Candidates (27 = 9 conditions x 3 vocab sizes), all already trained under
`experiments/expanded_morphology_v4/artifacts/`:
    plain, penalty-1, penalty-2, penalty-4, penalty-8,
    stochastic-p4-d0.1, stochastic-p4-d0.2, morphbpe (paper-aligned
    hard-constrained, added Phase 3 Part 2), unigram-ablation (not NLLB's
    tokenizer -- a matched-vocab Unigram-LM control).

Metric (type-weighted -- every reference word counts once, unlike the
frequency-weighted training-corpus diagnostic in v4's run_experiment.py):
    boundary P/R/F1   -- internal morpheme-boundary character offsets
    exact_match       -- fraction of words whose whole piece sequence == gold
    fertility         -- mean pieces per word
    mcf1              -- pairwise morpheme/token consistency, within the split
    kept_whole        -- of the zero-boundary rows, fraction emitted as 1 token

Selection: on DEV, maximise boundary F1; tie-break by exact_match, then by
lower fertility. Reported per condition family (best vocab) AND as a single
global winner, then re-scored on TEST for confirmation.

Reads only frozen inputs; writes reports/selection-report.{json,md}.
NOT independent native-speaker gold -- see reference-build-manifest.json.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "runtime"))

from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json  # noqa: E402

DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
DEV_CSV = DATA_DIR / "dev.csv"
TEST_CSV = DATA_DIR / "test.csv"
V4_ART = REPO_ROOT / "experiments/expanded_morphology_v4/artifacts"

VOCAB_SIZES = (6080, 8192, 16384)
RUNTIME_CONDITIONS = (
    "plain",
    "penalty-1",
    "penalty-2",
    "penalty-4",
    "penalty-8",
    "stochastic-p4-d0.1",
    "stochastic-p4-d0.2",
    "morphbpe",
)
UNIGRAM_CONDITION = "unigram-ablation"

MCF1_MIN_LEN = 2
MCF1_MAX_GROUP = 300


def load_split(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            bnds = (
                tuple(int(x) for x in row["boundaries"].split())
                if row["boundaries"].strip()
                else ()
            )
            rows.append(
                {
                    "surface": row["surface"],
                    "gold_boundaries": set(bnds),
                    "gold_pieces": _pieces_from_boundaries(row["surface"], bnds),
                    "n_boundaries": len(bnds),
                    "process": row["process"],
                    "provenance": row["provenance"],
                }
            )
    return rows


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
        (members[i], members[j]) for i in range(len(members)) for j in range(i + 1, len(members))
    }


def _mcf1(rows: list[dict[str, Any]], encoded_pieces: list[tuple[str, ...]]) -> dict[str, float]:
    morpheme_sets = [frozenset(p for p in r["gold_pieces"] if len(p) >= MCF1_MIN_LEN) for r in rows]
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
    return {"mcf1_precision": p, "mcf1_recall": r, "mcf1": _f1(p, r)}


def _encode_runtime(artifact: Path, rows: list[dict[str, Any]]) -> list[tuple[str, ...]]:
    tok = load_runtime_tokenizer(artifact)
    out: list[tuple[str, ...]] = []
    for row in rows:
        enc = tok.encode(row["surface"])
        pieces = tuple(t.token for t in enc.tokens)
        if tok.decode(enc.ids) != row["surface"]:
            raise AssertionError(f"round-trip failed for {row['surface']!r} in {artifact}")
        out.append(pieces)
    return out


def _encode_unigram(tokenizer_json: Path, rows: list[dict[str, Any]]) -> list[tuple[str, ...]]:
    from tokenizers import Tokenizer

    tok = Tokenizer.from_file(str(tokenizer_json))
    out: list[tuple[str, ...]] = []
    for row in rows:
        enc = tok.encode(row["surface"])
        pieces = tuple(enc.tokens)
        if "".join(pieces) != row["surface"]:
            raise AssertionError(f"unigram round-trip failed for {row['surface']!r}")
        out.append(pieces)
    return out


def _score(rows: list[dict[str, Any]], encoded: list[tuple[str, ...]]) -> dict[str, float]:
    tp = fp = fn = 0
    exact = produced = 0
    kept_whole = zero_rows = 0
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
        if pieces == row["gold_pieces"]:
            exact += 1
        if row["n_boundaries"] == 0:
            zero_rows += 1
            if len(pieces) == 1:
                kept_whole += 1
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    out = {
        "boundary_precision": p,
        "boundary_recall": r,
        "boundary_f1": _f1(p, r),
        "exact_match": exact / len(rows),
        "fertility": produced / len(rows),
        "kept_whole_rate": (kept_whole / zero_rows) if zero_rows else 0.0,
    }
    out.update(_mcf1(rows, encoded))
    return out


def _artifact_path(condition: str, vocab: int) -> Path:
    if condition == UNIGRAM_CONDITION:
        return V4_ART / "unigram-ablation" / f"vocab-{vocab}" / "tokenizer.json"
    return V4_ART / condition / "candidates" / f"vocab-{vocab}"


def _grid(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, float]]]:
    grid: dict[str, dict[str, dict[str, float]]] = {}
    for condition in (*RUNTIME_CONDITIONS, UNIGRAM_CONDITION):
        grid[condition] = {}
        for vocab in VOCAB_SIZES:
            art = _artifact_path(condition, vocab)
            if condition == UNIGRAM_CONDITION:
                encoded = _encode_unigram(art, rows)
            else:
                encoded = _encode_runtime(art, rows)
            grid[condition][str(vocab)] = _score(rows, encoded)
    return grid


def _select(dev_grid: dict[str, dict[str, dict[str, float]]]) -> dict[str, Any]:
    def key(m: dict[str, float]) -> tuple[float, float, float]:
        return (m["boundary_f1"], m["exact_match"], -m["fertility"])

    per_family: dict[str, Any] = {}
    best_overall: tuple[tuple[float, float, float], str, int] | None = None
    for condition, by_vocab in dev_grid.items():
        best_vocab = max(VOCAB_SIZES, key=lambda v: key(by_vocab[str(v)]))
        per_family[condition] = {
            "best_vocab": best_vocab,
            "dev_metrics": by_vocab[str(best_vocab)],
        }
        cand = (key(by_vocab[str(best_vocab)]), condition, best_vocab)
        if best_overall is None or cand[0] > best_overall[0]:
            best_overall = cand
    assert best_overall is not None
    return {
        "per_family_best_vocab": per_family,
        "global_winner": {"condition": best_overall[1], "vocab": best_overall[2]},
    }


def main() -> int:
    dev = load_split(DEV_CSV)
    test = load_split(TEST_CSV)

    dev_grid = _grid(dev)
    test_grid = _grid(test)
    selection = _select(dev_grid)

    win = selection["global_winner"]
    confirm = {
        "dev": dev_grid[win["condition"]][str(win["vocab"])],
        "test": test_grid[win["condition"]][str(win["vocab"])],
    }

    body: dict[str, Any] = {
        "reference": "experiments/tokenizer_selection_v1/data/reference-morphology.csv",
        "label": "silver + partial user adjudication; NOT independent native-speaker gold",
        "dev_csv_sha256": sha256_file(DEV_CSV),
        "test_csv_sha256": sha256_file(TEST_CSV),
        "dev_rows": len(dev),
        "test_rows": len(test),
        "metric": "type-weighted boundary F1; tie-break exact_match then lower fertility",
        "selection_on": "dev",
        "selection": selection,
        "global_winner_confirmation": confirm,
        "dev_grid": dev_grid,
        "test_grid": test_grid,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(REPORTS_DIR / "selection-report.json", report)
    _write_markdown(report)
    print(f"global winner (DEV): {win['condition']} @ vocab {win['vocab']}")
    print(
        f"  DEV  F1={confirm['dev']['boundary_f1']:.4f} "
        f"exact={confirm['dev']['exact_match']:.4f} fert={confirm['dev']['fertility']:.3f}"
    )
    print(
        f"  TEST F1={confirm['test']['boundary_f1']:.4f} "
        f"exact={confirm['test']['exact_match']:.4f} fert={confirm['test']['fertility']:.3f}"
    )
    print(f"wrote {REPORTS_DIR / 'selection-report.json'}")
    print(f"wrote {REPORTS_DIR / 'selection-report.md'}")
    return 0


def _row(name: str, m: dict[str, float]) -> str:
    return (
        f"| {name} | {m['boundary_f1']:.4f} | {m['boundary_precision']:.4f} | "
        f"{m['boundary_recall']:.4f} | {m['exact_match']:.4f} | {m['mcf1']:.4f} | "
        f"{m['fertility']:.3f} | {m['kept_whole_rate']:.3f} |"
    )


def _write_markdown(report: dict[str, Any]) -> None:
    win = report["selection"]["global_winner"]
    lines = [
        "# Phase 3 tokenizer selection -- morphology segmentation quality",
        "",
        "Held-out reference: `data/reference-morphology.csv` "
        f"(dev {report['dev_rows']} / test {report['test_rows']} rows, root-family disjoint).",
        "",
        "**Label: silver + partial user adjudication -- NOT independent "
        "native-speaker gold.** Tier A/B rows are this project's own "
        "corroborated-silver analyses; the folded-in Tier F rows carry the "
        "user's 2026-08-25 adjudication (the only human-verified subset). "
        "Selection is on DEV; TEST is a one-shot confirmation.",
        "",
        f"## Global winner (DEV): `{win['condition']}` @ vocab {win['vocab']:,}",
        "",
        "| split | boundary F1 | P | R | exact | MCF1 | fertility | kept-whole |",
        "|---|---|---|---|---|---|---|---|",
        _row("DEV", report["global_winner_confirmation"]["dev"]),
        _row("TEST", report["global_winner_confirmation"]["test"]),
        "",
        "## Best vocab per condition family (selected on DEV)",
        "",
        "| condition | best vocab | DEV F1 | DEV P | DEV R | DEV exact "
        "| DEV MCF1 | DEV fert | kept-whole |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    pfb = report["selection"]["per_family_best_vocab"]
    for condition, entry in pfb.items():
        m = entry["dev_metrics"]
        lines.append(
            f"| {condition} | {entry['best_vocab']:,} | {m['boundary_f1']:.4f} | "
            f"{m['boundary_precision']:.4f} | {m['boundary_recall']:.4f} | "
            f"{m['exact_match']:.4f} | {m['mcf1']:.4f} | {m['fertility']:.3f} | "
            f"{m['kept_whole_rate']:.3f} |"
        )
    for split_name in ("dev_grid", "test_grid"):
        lines += [
            "",
            f"## Full grid -- {split_name.split('_')[0].upper()}",
            "",
            "| condition | vocab | boundary F1 | P | R | exact | MCF1 | fertility | kept-whole |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        grid = report[split_name]
        for condition, by_vocab in grid.items():
            for vocab in ("6080", "8192", "16384"):
                m = by_vocab[vocab]
                lines.append(
                    f"| {condition} | {int(vocab):,} | {m['boundary_f1']:.4f} | "
                    f"{m['boundary_precision']:.4f} | {m['boundary_recall']:.4f} | "
                    f"{m['exact_match']:.4f} | {m['mcf1']:.4f} | {m['fertility']:.3f} | "
                    f"{m['kept_whole_rate']:.3f} |"
                )
    lines += [
        "",
        "`unigram-ablation` is NOT NLLB's tokenizer -- a matched-vocab "
        "Unigram-LM control trained on this project's own corpus.",
        "",
    ]
    (REPORTS_DIR / "selection-report.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
