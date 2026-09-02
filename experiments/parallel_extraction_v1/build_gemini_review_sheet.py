"""Build a flat, reviewer-ready CSV from the Gemini 500-sentence batch,
for sending to a native-speaker/linguist reviewer.

Reuses verify_gemini_batch.load_rows() (the same parser already used for
the mechanical word-attestation check) so the review sheet and the
attestation report are guaranteed to be reading the same 500 rows -- no
separate hand-transcription. Adds a category label (derived from which of
the source file's 11 section headers each row falls under) and two blank
columns for the reviewer to fill in, mirroring the verdict/notes pattern
this project used for translation_gold_v1's own user spot-check.
"""

from __future__ import annotations

import csv
from pathlib import Path

import verify_gemini_batch as vgb

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = BASE_DIR / "reports" / "gemini-batch-review-sheet.csv"

# (max item_num included, category label) -- matches the source file's own
# section headers, in order.
CATEGORY_BOUNDARIES = [
    (25, "Negation & Denial"),
    (50, "Varied Tense & Aspect"),
    (75, "Subordinate Clauses & Complex Sentences"),
    (100, "Comparatives, Superlatives & Equality"),
    (125, "Everyday Routines & Domestic Life"),
    (150, "Workplace, Technology & Remote Work"),
    (175, "Travel, Commuting & Navigation"),
    (200, "Health, Weather, Food & Environment"),
    (300, "Extended batch (201-300)"),
    (400, "Extended batch (301-400)"),
    (500, "Extended batch (401-500)"),
]


def category_for(num: int) -> str:
    for boundary, label in CATEGORY_BOUNDARIES:
        if num <= boundary:
            return label
    return "unknown"


def main() -> None:
    rows = vgb.load_rows()
    fieldnames = [
        "item_num",
        "category",
        "kapampangan",
        "filipino_tagalog",
        "english_gloss",
        "grammatical_feature_as_labeled",
        "reviewer_verdict",
        "reviewer_notes",
    ]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "item_num": row["num"],
                    "category": category_for(row["num"]),
                    "kapampangan": row["pam"],
                    "filipino_tagalog": row["fil"],
                    "english_gloss": row["eng"],
                    "grammatical_feature_as_labeled": row["feature"],
                    "reviewer_verdict": "",
                    "reviewer_notes": "",
                }
            )
    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
