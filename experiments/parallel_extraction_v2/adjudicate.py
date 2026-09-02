"""Phase 3 data step (parallel_extraction_v2), part 3: turn the reviewed
candidate sweep into a tiered SILVER pair set, merged with the v1 gold.

Inputs (all read-only):
  resources/user-evaluated-candidates-2026-09-01.csv
      -- the candidate sweep + the user's automated dictionary-alignment
         verdicts (accept / review). NOT a native-speaker review; the user
         explicitly flagged "grain of salt, not a native speaker".
  ../parallel_extraction_v1/reports/matched-pairs.csv        (38 PLD gold)
  ../parallel_extraction_v1/reports/external-vocab-pairs.csv (182 vocab gold)

Three signals are combined transparently:
  * mutual_best  -- reciprocal nearest neighbour in the LaBSE sweep
  * emb_cosine   -- LaBSE cosine
  * user_verdict -- accept / review from the dictionary-alignment pass
plus a small, explicitly-justified EXCLUDE list for rows a Claude
read-through found to be clear topic mismatches (write name vs write on
board, "how old" vs "how much", etc.) and for whole units that are
structurally not translation pairs (Iso_MinPairs = within-language minimal
pairs; Iso_Kinship/Iso_Time = degenerate).

Output: data/verified-pairs.csv, tiered:
  gold_v1  -- the 220 v1 pairs, unchanged
  silver_a -- high-confidence sweep pairs (mutual_best & strong signal)
  silver_b -- medium-confidence sweep pairs
None of silver_* is native-speaker verified. It is usable for Phase 5
low-resource fine-tuning AS SILVER, and needs a native-speaker validation
pass before any thesis-gold claim.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
EVAL_CSV = EXPERIMENT_ROOT / "resources/user-evaluated-candidates-2026-09-01.csv"
STORY_CSV = EXPERIMENT_ROOT / "data/story-pairs.csv"
CLAUDE_REVIEW_CSV = EXPERIMENT_ROOT / "resources/claude-review-2026-09-02.csv"
V1_MATCHED = REPO_ROOT / "experiments/parallel_extraction_v1/reports/matched-pairs.csv"
V1_VOCAB = REPO_ROOT / "experiments/parallel_extraction_v1/reports/external-vocab-pairs.csv"
OUT_CSV = EXPERIMENT_ROOT / "data/verified-pairs.csv"
MANIFEST = EXPERIMENT_ROOT / "reports/verified-pairs-manifest.json"
SUMMARY_MD = EXPERIMENT_ROOT / "reports/verified-pairs-summary.md"

# whole units that are structurally not translation pairs
EXCLUDE_UNITS = {"Iso_MinPairs.txt", "Iso_Kinship.txt", "Iso_Time.txt"}

# individual rows a read-through flagged as clear topic mismatches, keyed by
# the exact PAM text. Conservative: only unambiguous non-pairs are listed;
# borderline rows are kept in silver_b, not excluded.
EXCLUDE_PAM = {
    "Isulat ing lagiu.",
    "Isulat ing lagiu king papil.",
    "Iwasan ing mangopia.",
    "Nanu ing linutu nang Michelle?",
    "Magcanta ta pa mu.",
    "Pilang banua na co hu?",
    "Tigtig ya wari?",
    "Tigtig ya, e wari?",
    "Cuanan ing libru.",
    "Ninu ing cayabe mu?",
    "Ninung e na aintindian?",
    "Baual mangan.",
    "Lumaue keni.",
    "Mengatacutan la at mibalic king capatagan a e de man ikit i Bernardo.",
}

_WS = re.compile(r"\s+")


def norm(text: str) -> str:
    return _WS.sub(" ", text.strip())


def key(pam: str, fil: str) -> str:
    return f"{norm(pam).casefold()}\t{norm(fil).casefold()}"


def load_csv(path: Path, enc: str = "utf-8") -> list[dict[str, str]]:
    with path.open(encoding=enc) as handle:
        return list(csv.DictReader(handle))


def tier_of(row: dict[str, str]) -> str | None:
    unit = row["unit"].split("(")[0].strip()
    if unit in EXCLUDE_UNITS:
        return None
    if norm(row["pam_text"]) in EXCLUDE_PAM:
        return None
    mnn = row["mutual_best"].strip().lower() == "true"
    emb = float(row["emb_cosine"])
    accepted = row["reviewer_verdict"].strip().lower() == "accept"

    # trivial identical named entities carry no training signal
    if norm(row["pam_text"]).casefold() == norm(row["fil_text"]).casefold():
        return None

    if mnn and (accepted or emb >= 0.66):
        return "silver_a"
    if (mnn and emb >= 0.58) or (accepted and emb >= 0.50):
        return "silver_b"
    return None


def main() -> int:
    rows: list[dict[str, object]] = []
    seen: set[str] = set()

    # Claude read-through of the review sheet (2026-09-02; NON-native, silver):
    # key(pam,fil) -> (verdict, note). 'n' rows are dropped; 'p' rows kept with
    # the caveat recorded in a claude_review column.
    claude_review: dict[str, tuple[str, str]] = {}
    if CLAUDE_REVIEW_CSV.exists():
        for r in load_csv(CLAUDE_REVIEW_CSV):
            claude_review[key(r["pam_text"], r["fil_text"])] = (r["verdict"], r["note"])
    review_counts = {"n_dropped": 0, "partial": 0}

    def review_of(pam: str, fil: str) -> str | None:
        """None -> drop the row; else the value for the claude_review column."""
        hit = claude_review.get(key(pam, fil))
        if hit is None:
            return "ok"
        verdict, note = hit
        if verdict == "n":
            review_counts["n_dropped"] += 1
            return None
        review_counts["partial"] += 1
        return f"partial: {note}"

    # ---- v1 gold, unchanged ----
    for r in load_csv(V1_MATCHED):
        k = key(r["pam_text"], r["fil_text"])
        if k in seen:
            continue
        seen.add(k)
        rows.append(
            {
                "pair_id": r["pair_id"],
                "tier": "gold_v1",
                "source": "parallel_extraction_v1/matched-pairs.csv",
                "pam_text": norm(r["pam_text"]),
                "fil_text": norm(r["fil_text"]),
                "unit": r["pam_source_domain"],
                "signal": r["confidence"],
                "note": r["note"],
            }
        )
    for r in load_csv(V1_VOCAB):
        k = key(r["pam_text"], r["fil_text"])
        if k in seen:
            continue
        seen.add(k)
        rows.append(
            {
                "pair_id": r["pair_id"],
                "tier": "gold_v1",
                "source": "parallel_extraction_v1/external-vocab-pairs.csv",
                "pam_text": norm(r["pam_text"]),
                "fil_text": norm(r["fil_text"]),
                "unit": "external_vocab",
                "signal": r["confidence"],
                "note": r["note"],
            }
        )

    # ---- native-authored story pairs (highest-quality connected narrative) ----
    story_added = 0
    if STORY_CSV.exists():
        for r in load_csv(STORY_CSV):
            k = key(r["pam_text"], r["fil_text"])
            if k in seen:
                continue
            seen.add(k)
            story_added += 1
            rows.append(
                {
                    "pair_id": r["pair_id"],
                    "tier": "gold_stories",
                    "source": "parallel_extraction_v2/story-pairs.csv (native-authored)",
                    "pam_text": norm(r["pam_text"]),
                    "fil_text": norm(r["fil_text"]),
                    "unit": f"story {r['story_num']}: {r['story_title']}",
                    "signal": "native_speaker_authored",
                    "note": "",
                }
            )

    # ---- v2 sweep, tiered silver ----
    counts = {"silver_a": 0, "silver_b": 0, "excluded": 0, "dup_of_gold": 0}
    n = 0
    for r in load_csv(EVAL_CSV, enc="utf-8-sig"):
        tier = tier_of(r)
        if tier is None:
            counts["excluded"] += 1
            continue
        k = key(r["pam_text"], r["fil_text"])
        if k in seen:
            counts["dup_of_gold"] += 1
            continue
        seen.add(k)
        n += 1
        counts[tier] += 1
        rows.append(
            {
                "pair_id": f"v2pair_{n:04d}",
                "tier": tier,
                "source": "parallel_extraction_v2 sweep",
                "pam_text": norm(r["pam_text"]),
                "fil_text": norm(r["fil_text"]),
                "unit": r["unit"].split("(")[0].strip(),
                "signal": (
                    f"mnn={r['mutual_best']};emb={r['emb_cosine']};"
                    f"dict={r['reviewer_verdict'].strip()}"
                ),
                "note": "",
            }
        )

    # ---- apply the Claude read-through: drop 'n', tag 'p', mark the rest ok ----
    reviewed: list[dict[str, object]] = []
    for pr in rows:
        verdict = review_of(str(pr["pam_text"]), str(pr["fil_text"]))
        if verdict is None:
            continue
        pr["claude_review"] = verdict
        reviewed.append(pr)
    rows = reviewed

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    fields = [
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
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    tier_counts: dict[str, int] = {}
    for pr in rows:
        tier_counts[str(pr["tier"])] = tier_counts.get(str(pr["tier"]), 0) + 1

    manifest = {
        "output": OUT_CSV.name,
        "output_sha256": hashlib.sha256(OUT_CSV.read_bytes()).hexdigest(),
        "total_pairs": len(rows),
        "by_tier": tier_counts,
        "story_pairs_added": story_added,
        "claude_read_through_2026_09_02": {
            "dropped_not_a_pair": review_counts["n_dropped"],
            "kept_flagged_partial": review_counts["partial"],
            "note": "non-native read-through; the ENTIRE set is SILVER for Phase 5",
        },
        "v2_sweep_disposition": counts,
        "label": (
            "THE ENTIRE SET IS SILVER for Phase 5. A native-speaker "
            "validation pass on reports/native-speaker-review-sheet.csv is "
            "still the gate for any thesis-gold claim. Tiers: gold_stories = "
            "native-authored connected narrative (user-vouched, modern/"
            "cultural register); gold_v1 = 220 user spot-checked pairs (user "
            "is not a native speaker); silver_a/b = PLD sweep, three "
            "non-native passes (LaBSE+MNN, the user's dictionary-alignment "
            "script, a full Claude read-through 2026-09-02). The Claude "
            "read-through dropped 3 rows as not-a-pair and flagged 27 in the "
            "claude_review column as 'partial'."
        ),
        "inputs": {
            "user_evaluated_csv_sha256": hashlib.sha256(EVAL_CSV.read_bytes()).hexdigest(),
            "story_csv_sha256": (
                hashlib.sha256(STORY_CSV.read_bytes()).hexdigest() if STORY_CSV.exists() else None
            ),
            "v1_matched_sha256": hashlib.sha256(V1_MATCHED.read_bytes()).hexdigest(),
            "v1_vocab_sha256": hashlib.sha256(V1_VOCAB.read_bytes()).hexdigest(),
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    by_unit: dict[str, dict[str, int]] = {}
    for pr in rows:
        if not str(pr["tier"]).startswith("silver"):
            continue
        bucket = by_unit.setdefault(str(pr["unit"]), {"silver_a": 0, "silver_b": 0})
        bucket[str(pr["tier"])] += 1
    lines = [
        "# parallel_extraction_v2 -- verified pair set (tiered)",
        "",
        "**gold_v1** is the 220 user-spot-checked v1 pairs, unchanged. "
        "**silver_a/b** are PLD full-pool sweep pairs adjudicated by three "
        "non-native passes (LaBSE+lexical sweep, the user's dictionary-"
        "alignment script, a Claude read-through). **Not native-speaker "
        "gold** -- a native-speaker validation pass is still required before "
        "any thesis-gold claim. Usable now for Phase 5 low-resource "
        "fine-tuning as silver.",
        "",
        f"- **{len(rows)} pairs total**: "
        + ", ".join(f"{k} {v}" for k, v in sorted(tier_counts.items())),
        f"- v2 sweep disposition: {counts}",
        "",
        "## silver pairs by PLD unit",
        "",
        "| unit | silver_a | silver_b |",
        "|---|---:|---:|",
    ]
    for unit_name, bucket in sorted(
        by_unit.items(), key=lambda kv: -(kv[1]["silver_a"] + kv[1]["silver_b"])
    ):
        lines.append(f"| {unit_name} | {bucket['silver_a']} | {bucket['silver_b']} |")
    lines.append("")
    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
