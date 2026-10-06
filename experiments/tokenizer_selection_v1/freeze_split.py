"""Phase 3 Part 1, step 2: freeze a disjoint DEV/TEST split of the reference set.

Reads `data/reference-morphology.csv` (built by build_reference.py). Writes
`data/dev.csv`, `data/test.csv`, and `reports/split-manifest.json`.

Design (agreed with the user 2026-08-28):
  * 50/50 -- the set is small (534 rows); TEST needs enough boundaries for a
    stable confirmation of the DEV-selected config.
  * stratified by (process family, has-boundary) so both halves see the same
    mix of prefix/suffix/infix/circumfix/reduplication and the same share of
    zero-boundary "do not over-split" rows.
  * ROOT-FAMILY DISJOINT: no root key appears in both halves. After the
    stratified assignment, every root that straddles the split is pulled
    wholesale to the side that currently holds more of its rows (ties -> dev).
    This trades a little stratum balance for zero lexical leakage, which
    matters for MCF1 and removes "did the tokenizer just memorise this exact
    root" optimism from the boundary numbers.
  * seed 20260828, fixed and documented.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
REFERENCE_CSV = DATA_DIR / "reference-morphology.csv"
DEV_CSV = DATA_DIR / "dev.csv"
TEST_CSV = DATA_DIR / "test.csv"
SPLIT_MANIFEST = REPORTS_DIR / "split-manifest.json"

SEED = 20260828

# affix / marker strings that must never be picked as a row's "root key"
AFFIX_STRINGS = {
    "m",
    "ma",
    "mag",
    "man",
    "mam",
    "mang",
    "manga",
    "men",
    "mem",
    "meng",
    "maki",
    "meki",
    "makipag",
    "paki",
    "peka",
    "mi",
    "magpa",
    "migpa",
    "megpa",
    "magka",
    "migka",
    "megka",
    "ka",
    "pa",
    "pan",
    "pam",
    "pang",
    "panga",
    "pi",
    "pag",
    "par",
    "in",
    "um",
    "an",
    "en",
    "anan",
    "nan",
    "n",
    "i",
    "ipa",
    "ika",
    "ke",
    "ta",
    "la",
    "ba",
    "sa",
    "tu",
    "ga",
    "na",
    "ya",
    "pe",
    "ca",
    "y",
    "g",
}


def root_key(surface: str, segmentation: str) -> str:
    if not segmentation.strip():
        return surface.lower()
    pieces = [p.strip().lower() for p in segmentation.split("|")]
    content = [p for p in pieces if len(p) >= 3 and p not in AFFIX_STRINGS]
    if content:
        return max(content, key=len)
    # fall back to the longest piece of any kind
    return max((p for p in pieces if p), key=len, default=surface.lower())


def process_family(process: str) -> str:
    if "+" in process:
        return "combo"
    return process


def load_reference() -> list[dict[str, str]]:
    with REFERENCE_CSV.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    rows = load_reference()
    rng = random.Random(SEED)

    for row in rows:
        row["_root_key"] = root_key(row["surface"], row["segmentation"])
        has_boundary = "b" if int(row["n_boundaries"]) > 0 else "0"
        row["_stratum"] = f"{process_family(row['process'])}:{has_boundary}"

    # 1) stratified alternating assignment, root groups kept intact from the start
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["_root_key"]].append(row)

    # order root groups deterministically: by dominant stratum, then shuffled
    strata_groups: dict[str, list[str]] = defaultdict(list)
    for key, members in groups.items():
        dominant = Counter(m["_stratum"] for m in members).most_common(1)[0][0]
        strata_groups[dominant].append(key)

    assignment: dict[str, str] = {}
    for stratum in sorted(strata_groups):
        keys = strata_groups[stratum]
        rng.shuffle(keys)
        dev_count = sum(len(groups[k]) for k in keys if assignment.get(k) == "dev")
        test_count = sum(len(groups[k]) for k in keys if assignment.get(k) == "test")
        for key in keys:
            side = "dev" if dev_count <= test_count else "test"
            assignment[key] = side
            if side == "dev":
                dev_count += len(groups[key])
            else:
                test_count += len(groups[key])

    dev = [r for r in rows if assignment[r["_root_key"]] == "dev"]
    test = [r for r in rows if assignment[r["_root_key"]] == "test"]

    # 2) verify root disjointness (guaranteed by construction, assert anyway)
    dev_roots = {r["_root_key"] for r in dev}
    test_roots = {r["_root_key"] for r in test}
    overlap = dev_roots & test_roots
    if overlap:
        raise AssertionError(f"root leakage between dev and test: {sorted(overlap)[:10]}")

    dev.sort(key=lambda r: r["id"])
    test.sort(key=lambda r: r["id"])

    fields = [c for c in rows[0] if not c.startswith("_")]
    for path, part in ((DEV_CSV, dev), (TEST_CSV, test)):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            for row in part:
                writer.writerow({k: row[k] for k in fields})

    def summarize(part: list[dict[str, str]]) -> dict[str, object]:
        return {
            "rows": len(part),
            "gold_boundaries": sum(int(r["n_boundaries"]) for r in part),
            "zero_boundary_rows": sum(1 for r in part if int(r["n_boundaries"]) == 0),
            "by_process": dict(Counter(r["process"] for r in part).most_common()),
            "by_provenance": dict(Counter(r["provenance"] for r in part).most_common()),
            "root_families": len({r["_root_key"] for r in part}),
        }

    manifest = {
        "seed": SEED,
        "ratio": "50/50 stratified, root-family disjoint",
        "reference_csv_sha256": hashlib.sha256(REFERENCE_CSV.read_bytes()).hexdigest(),
        "dev_csv_sha256": hashlib.sha256(DEV_CSV.read_bytes()).hexdigest(),
        "test_csv_sha256": hashlib.sha256(TEST_CSV.read_bytes()).hexdigest(),
        "dev": summarize(dev),
        "test": summarize(test),
        "root_leakage": 0,
    }
    SPLIT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
