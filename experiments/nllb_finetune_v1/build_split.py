"""Phase 5 step 1: freeze the train / dev / test splits for the NLLB
fine-tuning experiment.

Design (agreed with the user 2026-09-03, Bible-primary refresh):
  The thesis proposal names the PLOC Kapampangan religious corpus as the
  PRIMARY downstream dataset; conversational / news / story material is
  supplementary "for register diversity". So:

  * IN-DOMAIN test  -- `data/test_bible.csv`: whole Bible **chapters** are
    held out (no verse from a held-out chapter appears in train or dev).
    Verse-level random splits leak because the corpus is formulaic
    ("At mika ating bengi at mika ating abak, ing X aldo" recurs).
  * OUT-OF-DOMAIN test -- `data/test_ood.csv`: five whole native-authored
    stories + a sample of clean `gold_v1` sentence pairs. This is the
    register-transfer number (train is ~85% religious register).
  * DEV -- `data/dev.csv`: a held-out sample of Bible chapters (early
    stopping in-register) + a small modern sample (gold_stories / gold_v1 /
    silver_a) so dev is not purely religious register.
  * TRAIN -- `data/train.csv`: everything else, including all silver_b,
    silver_gemini, the short vocabulary pairs, and every `partial`-flagged
    row. No sentence from a held-out chapter / test story.
  * seed 20260903, fixed. Chapter selection is per-book proportional so
    every book contributes to every split.

Input:  ../parallel_extraction_v2/data/verified-pairs.csv
Output: data/{train,dev,test_bible,test_ood}.csv  +  reports/split-manifest.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
SRC_CSV = REPO_ROOT / "experiments/parallel_extraction_v2/data/verified-pairs.csv"
DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
MANIFEST = REPORTS_DIR / "split-manifest.json"

SEED = 20260903

# --- in-domain (Bible) holdout, approximate verse targets; whole chapters ---
BIBLE_TEST_VERSES = 250
BIBLE_DEV_VERSES = 150

# --- out-of-domain (modern) holdout ---
# whole native-authored stories held out entirely (no sentence in train/dev)
TEST_STORY_UNITS = {
    "story 2: Ing Panabilin kang Roy",
    "story 8: Ing kekaming Komunidad, Kanita at Ngeni",
    "story 11: Kebaytan nang Imang Lily",
    "story 12: Transportasyun king Pilipinas",
    "story 13: Kaluguran da ka Ima",
}
OOD_GOLD_V1_SENTENCES = 29  # random clean gold_v1 sentence pairs added to test_ood

# --- modern dev sample (register balance for early stopping) ---
DEV_MODERN_PER_TIER = {"gold_stories": 15, "gold_v1": 15, "silver_a": 15}

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


def book_of(unit: str) -> str:
    # unit == "bible <book> <chapter>"
    return unit.rsplit(" ", 1)[0]


def write_split(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows({k: r[k] for k in FIELDS} for r in rows)


def pick_bible_chapters(
    rows: list[dict[str, str]], rng: random.Random
) -> tuple[set[str], set[str]]:
    """Per-book proportional, whole-chapter selection for test_bible then dev.
    Returns (test_chapters, dev_chapters); everything else is train."""
    by_chapter: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        if r["tier"] == "bible":
            by_chapter[r["unit"]].append(r)
    verses_total = sum(len(v) for v in by_chapter.values())

    by_book: dict[str, list[str]] = defaultdict(list)
    for chap in by_chapter:
        by_book[book_of(chap)].append(chap)

    test_ch: set[str] = set()
    dev_ch: set[str] = set()
    for _book, chapters in sorted(by_book.items()):
        chapters = sorted(chapters, key=lambda c: int(c.rsplit(" ", 1)[1]))
        rng.shuffle(chapters)
        book_verses = sum(len(by_chapter[c]) for c in chapters)
        test_quota = BIBLE_TEST_VERSES * book_verses / verses_total
        dev_quota = BIBLE_DEV_VERSES * book_verses / verses_total
        acc = 0
        it = iter(chapters)
        for c in it:
            test_ch.add(c)
            acc += len(by_chapter[c])
            if acc >= test_quota:
                break
        acc = 0
        for c in it:
            dev_ch.add(c)
            acc += len(by_chapter[c])
            if acc >= dev_quota:
                break
    assert not (test_ch & dev_ch)
    return test_ch, dev_ch


def main() -> int:
    rows = load()
    rng = random.Random(SEED)

    used: set[str] = set()

    # ---------------- in-domain Bible chapter holdout ----------------
    test_bible_ch, dev_bible_ch = pick_bible_chapters(rows, rng)
    test_bible = [r for r in rows if r["tier"] == "bible" and r["unit"] in test_bible_ch]
    dev_bible = [r for r in rows if r["tier"] == "bible" and r["unit"] in dev_bible_ch]
    for r in test_bible + dev_bible:
        used.add(r["pair_id"])

    # ---------------- out-of-domain (modern) test ----------------
    test_ood: list[dict[str, str]] = []
    for r in rows:
        if r["tier"] == "gold_stories" and r["unit"] in TEST_STORY_UNITS and is_ok(r):
            test_ood.append(r)
            used.add(r["pair_id"])
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
    for r in gold_v1_sentences[:OOD_GOLD_V1_SENTENCES]:
        test_ood.append(r)
        used.add(r["pair_id"])

    # ---------------- dev: Bible chapters + modern sample ----------------
    dev = list(dev_bible)
    modern_pool: dict[str, list[dict[str, str]]] = {t: [] for t in DEV_MODERN_PER_TIER}
    for r in rows:
        if r["pair_id"] in used or not is_ok(r):
            continue
        if r["tier"] in modern_pool:
            modern_pool[r["tier"]].append(r)
    for tier, k in DEV_MODERN_PER_TIER.items():
        pool = modern_pool[tier]
        rng.shuffle(pool)
        for r in pool[:k]:
            dev.append(r)
            used.add(r["pair_id"])

    # ---------------- train: everything else ----------------
    # never a sentence from a held-out Bible chapter or a test story
    train = [
        r
        for r in rows
        if r["pair_id"] not in used
        and r["unit"] not in TEST_STORY_UNITS
        and not (r["tier"] == "bible" and r["unit"] in (test_bible_ch | dev_bible_ch))
    ]

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_split(DATA_DIR / "train.csv", train)
    write_split(DATA_DIR / "dev.csv", dev)
    write_split(DATA_DIR / "test_bible.csv", test_bible)
    write_split(DATA_DIR / "test_ood.csv", test_ood)

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
        "bible_test_chapters": sorted(test_bible_ch),
        "bible_dev_chapters": sorted(dev_bible_ch),
        "test_story_units": sorted(TEST_STORY_UNITS),
        "splits": {
            "train": summ(train),
            "dev": summ(dev),
            "test_bible": summ(test_bible),
            "test_ood": summ(test_ood),
        },
        "sha256": {
            name: hashlib.sha256((DATA_DIR / f"{name}.csv").read_bytes()).hexdigest()
            for name in ("train", "dev", "test_bible", "test_ood")
        },
        "label": (
            "ALL SILVER. IN-DOMAIN test_bible = whole held-out Bible "
            "chapters (leakage-safe). OUT-OF-DOMAIN test_ood = 5 whole "
            "native-authored stories + clean gold_v1 sentences (register "
            "transfer). DEV = held-out Bible chapters + a modern sample. "
            "TRAIN keeps silver_b + silver_gemini + partial rows. Bible "
            "corpus rights are UNRESOLVED (see resources manifest)."
        ),
    }

    # ---- hard leakage assertions ----
    train_ch = {r["unit"] for r in train if r["tier"] == "bible"}
    assert not (train_ch & test_bible_ch), "test Bible chapter leaked into train"
    assert not (train_ch & dev_bible_ch), "dev Bible chapter leaked into train"
    dev_ch = {r["unit"] for r in dev if r["tier"] == "bible"}
    assert not (dev_ch & test_bible_ch), "Bible chapter in both dev and test"
    td_units = {r["unit"] for r in train} | {r["unit"] for r in dev}
    assert not (td_units & TEST_STORY_UNITS), "test story leaked into train/dev"
    ids_all = [r["pair_id"] for r in train + dev + test_bible + test_ood]
    assert len(ids_all) == len(set(ids_all)), "duplicate pair across splits"

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
