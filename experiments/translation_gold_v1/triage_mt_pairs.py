"""Phase 1 AI-assisted triage of the 250-row PAM-FIL MT candidate set.

Reads the byte-identical copy under resources/ (never the external
original) and joins it against reports/mt-pair-rubric-scores.tsv -- a
documented, stated 0-3 rubric applied to every row by direct reading (not a
single opaque LLM score), with a short reason recorded for each row so the
judgment is auditable, not just asserted:

  0 = no_correspondence   -- no plausible semantic connection between source
      and target.
  1 = same_domain_wrong_specific -- both texts belong to the same elicitation
      domain (kinship, time, greetings, medical, economic news, proverbs...)
      but do not mean the same thing. This is the dominant category, and it
      is the same failure mode already documented for this dataset generally
      (AGENT_CONTEXT.md 2026-08-25 dataset-audit entry): rows were generated
      by cross-matching within a shared elicitation domain, not by aligning
      real translations.
  2 = plausible_partial_match -- meaningful overlap (a shared formulaic
      structure, a shared core concept, or the same topic with unverified
      exact detail) without being a confirmed correct translation.
  3 = correct_translation -- a clear, verifiable correct translation.

A separate category, dictionary_gloss_pair (rows 42-50), is not scored 0-3
at all: those rows are homonym/homograph dictionary illustration entries
(two senses of one Kapampangan word, each glossed), not sentence or phrase
translation pairs, and are out of scope for MT candidacy regardless of their
target text.

Output remains silver/ai_triaged, never gold; see
reports/mt-pair-triage-summary.md for the full methodology writeup.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
RESOURCES = EXPERIMENT_ROOT / "resources"
REPORTS = EXPERIMENT_ROOT / "reports"

MT_CSV = RESOURCES / "kapampangan_mt_pld_pam_fil_curated.csv"
RUBRIC_TSV = REPORTS / "mt-pair-rubric-scores.tsv"

TIER_BY_SCORE = {
    "3": "A_correct_translation",
    "2": "B_plausible_partial_match",
    "1": "C_same_domain_wrong_specific",
    "0": "D_no_correspondence",
}


def _load_rubric() -> list[dict[str, str]]:
    with RUBRIC_TSV.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def main() -> None:
    with MT_CSV.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    rubric = _load_rubric()

    if len(rows) != len(rubric):
        raise SystemExit(
            f"row count mismatch: {len(rows)} source rows vs {len(rubric)} rubric rows"
        )

    scored = []
    for source_row, rubric_row in zip(rows, rubric, strict=True):
        score = rubric_row["score"]
        if rubric_row["category"] == "dictionary_gloss_pair":
            tier = "E_dictionary_gloss_not_a_pair"
        else:
            tier = TIER_BY_SCORE[score]
        scored.append(
            {
                "row_index": rubric_row["row_index"],
                "mt_id": source_row["mt_id"],
                "granularity": source_row["granularity"],
                "source_text": source_row["source_text"],
                "target_text": source_row["target_text"],
                "prompt_family": source_row["prompt_family"],
                "score": score,
                "category": rubric_row["category"],
                "note": rubric_row["note"],
                "tier": tier,
            }
        )

    REPORTS.mkdir(parents=True, exist_ok=True)
    out_csv = REPORTS / "mt-pair-triage.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scored[0].keys()))
        writer.writeheader()
        writer.writerows(scored)

    from collections import Counter

    tier_counts = Counter(r["tier"] for r in scored)
    summary = {
        "total_rows": len(scored),
        "tier_counts": dict(sorted(tier_counts.items())),
        "shuffle_evidence_rows": sum(
            1 for r in scored if "correct match" in r["note"] or "true match" in r["note"] or "shift" in r["note"]
        ),
    }
    (REPORTS / "mt-pair-triage-stats.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
