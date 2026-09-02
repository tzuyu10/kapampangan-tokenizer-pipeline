"""Phase 5 step 1: freeze a train / dev / test split of the 716-pair
translation set for the NLLB fine-tuning experiment.

Design (agreed with the user 2026-09-02):
  * TEST is a **story-level holdout** -- five whole native-authored stories
    are removed entirely (no sentence from a test story appears in train or
    dev), plus a random sample of `gold_v1` sentence pairs. Test is drawn
    only from the cleanest data and only from `claude_review == "ok"` rows.
  * DEV is a small stratified sample from the remaining gold_stories /
    gold_v1 / silver_a rows (also `ok` only).
  * TRAIN is everything else -- including all `silver_b`, all `partial`-
    flagged rows, and the short vocabulary pairs.
  * seed 20260902, fixed.

Input:  ../parallel_extraction_v2/data/verified-pairs.csv (716 rows)
Output: data/{train,dev,test}.csv  +  reports/split-manifest.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
SRC_CSV = REPO_ROOT / "experiments/parallel_extraction_v2/data/verified-pairs.csv"
DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
MANIFEST = REPORTS_DIR / "split-manifest.json"

SEED = 20260902
# whole stories held out for TEST (no sentence from these appears in train/dev)
TEST_STORY_UNITS = {
    "story 2: Ing Panabilin kang Roy",
    "story 8: Ing kekaming Komunidad, Kanita at Ngeni",
    "story 11: Kebaytan nang Imang Lily",
    "story 12: Transportasyun king Pilipinas",
    "story 13: Kaluguran da ka Ima",
}
TEST_GOLD_V1_SENTENCES = 29  # random gold_v1 sentence pairs added to TEST
DEV_SIZE = 45

FIELDS = [
    "pair_id",
    "tier",
    "source",
    "pam_text",
    "fil_text",
    "unit",
    "signal",
    "claude_review",
    "note",
]


def load() -> list[dict[str, str]]:
    with SRC_CSV.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_ok(row: dict[str, str]) -> bool:
    return row["claude_review"] == "ok"


def write_split(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows({k: r[k] for k in FIELDS} for r in rows)


def main() -> int:
    rows = load()
    rng = random.Random(SEED)

    test: list[dict[str, str]] = []
    used: set[str] = set()

    # 1. whole test stories
    for r in rows:
        if r["tier"] == "gold_stories" and r["unit"] in TEST_STORY_UNITS and is_ok(r):
            test.append(r)
            used.add(r["pair_id"])

    # 2. a random sample of clean gold_v1 sentence pairs (exclude the short
    #    Iso word-level ones and the external-vocab list)
    gold_v1_sentences = [
        r
        for r in rows
        if r["tier"] == "gold_v1"
        and is_ok(r)
        and r["unit"] not in {"external_vocab"}
        and not r["unit"].startswith("Iso_")
        and len(r["pam_text"].split()) >= 4
    ]
    rng.shuffle(gold_v1_sentences)
    for r in gold_v1_sentences[:TEST_GOLD_V1_SENTENCES]:
        test.append(r)
        used.add(r["pair_id"])

    # 3. DEV: stratified sample from the remaining ok gold_stories / gold_v1 / silver_a
    dev_pool_by_tier: dict[str, list[dict[str, str]]] = {
        "gold_stories": [],
        "gold_v1": [],
        "silver_a": [],
    }
    for r in rows:
        if r["pair_id"] in used or not is_ok(r):
            continue
        if r["tier"] in dev_pool_by_tier:
            dev_pool_by_tier[r["tier"]].append(r)
    dev: list[dict[str, str]] = []
    per_tier = {"gold_stories": 15, "gold_v1": 15, "silver_a": 15}
    for tier, k in per_tier.items():
        pool = dev_pool_by_tier[tier]
        rng.shuffle(pool)
        for r in pool[:k]:
            dev.append(r)
            used.add(r["pair_id"])

    # 4. TRAIN: everything not used, and never a sentence from a test story
    #    (the few `partial` rows of the test stories are dropped from all splits)
    train = [
        r for r in rows if r["pair_id"] not in used and r["unit"] not in TEST_STORY_UNITS
    ]

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_split(DATA_DIR / "train.csv", train)
    write_split(DATA_DIR / "dev.csv", dev)
    write_split(DATA_DIR / "test.csv", test)

    def summ(part: list[dict[str, str]]) -> dict[str, object]:
        return {
            "rows": len(part),
            "by_tier": dict(Counter(r["tier"] for r in part).most_common()),
            "partial_flagged": sum(1 for r in part if r["claude_review"] != "ok"),
            "mean_pam_words": round(
                sum(len(r["pam_text"].split()) for r in part) / max(len(part), 1), 1
            ),
        }

    manifest = {
        "seed": SEED,
        "source_csv_sha256": hashlib.sha256(SRC_CSV.read_bytes()).hexdigest(),
        "test_story_units": sorted(TEST_STORY_UNITS),
        "leakage_check": "TEST stories are removed whole; assert below",
        "train": summ(train),
        "dev": summ(dev),
        "test": summ(test),
        "train_csv_sha256": hashlib.sha256((DATA_DIR / "train.csv").read_bytes()).hexdigest(),
        "dev_csv_sha256": hashlib.sha256((DATA_DIR / "dev.csv").read_bytes()).hexdigest(),
        "test_csv_sha256": hashlib.sha256((DATA_DIR / "test.csv").read_bytes()).hexdigest(),
        "label": (
            "ALL SILVER. Story-level holdout for TEST; TEST/DEV are "
            "claude_review=='ok' only; TRAIN keeps silver_b + partial rows."
        ),
    }

    # hard leakage assertions
    train_dev_units = {r["unit"] for r in train} | {r["unit"] for r in dev}
    assert not (train_dev_units & TEST_STORY_UNITS), "test story leaked into train/dev"
    ids_all = [r["pair_id"] for r in train + dev + test]
    assert len(ids_all) == len(set(ids_all)), "duplicate pair across splits"

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
