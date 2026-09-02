"""Phase 3 data step (parallel_extraction_v2), part 1: build distinct
sentence pools per shared-name PLD elicitation file.

Second-pass finding (2026-08-31): parallel_extraction_v1 aligned from the
1,924-row *canonical inventory*, which collapsed `(file, ordinal)` slots to
one representative each. The raw parse in
`resources/pld_prompt_entries_pam_fil.csv` actually holds ~4,700 distinct
PAM / ~4,200 distinct FIL sentences, because `prompt_ordinal` was
per-speaker randomised. This script rebuilds the full distinct-sentence
pools so an alignment sweep can work over everything, not the collapsed
slice.

Reads ONLY `resources/pld_prompt_entries_pam_fil.csv` (copied with a
SHA-256 provenance manifest). Writes:
  data/sentence-pools.json   -- {unit: {"pam": [...], "fil": [...]}}
  reports/pool-summary.csv    -- per-unit distinct counts
  reports/pools-manifest.json -- source hash + totals

`prompt_text` is the elicitation prompt each speaker was asked to produce,
NOT a spoken transcription. Redistribution rights for the PLD archive are
unresolved -> local research use only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
SOURCE_CSV = EXPERIMENT_ROOT / "resources/pld_prompt_entries_pam_fil.csv"
DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
POOLS_JSON = DATA_DIR / "sentence-pools.json"
SUMMARY_CSV = REPORTS_DIR / "pool-summary.csv"
MANIFEST_JSON = REPORTS_DIR / "pools-manifest.json"

# granularities worth aligning (word / number lists are not translation pairs)
KEEP_GRANULARITY = {"sentence", "phrase"}

# The five Kapampangan folktale files whose sentences the single Filipino
# Utt_Story.txt interleaves (established in parallel_extraction_v1).
STORY_PAM_FILES = {
    "Utt_StoryBernardo.txt",
    "Utt_StoryIputipot.txt",
    "Utt_StoryMatsing.txt",
    "Utt_StoryGamugamo.txt",
    "Utt_StoryAraw.txt",
}
STORY_FIL_FILE = "Utt_Story.txt"
STORY_UNIT = "STORY_folktales(PAM 5 files vs FIL Utt_Story.txt)"

_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    return _WS.sub(" ", text.strip())


def load_rows() -> list[dict[str, str]]:
    with SOURCE_CSV.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def distinct_pool(texts: list[str]) -> list[str]:
    """Case-insensitive de-dupe, keeping the most frequent surface form,
    then the first-seen; drop 1-word items (not sentences/phrases to align)."""
    by_key: dict[str, Counter[str]] = defaultdict(Counter)
    order: list[str] = []
    for raw in texts:
        norm = normalize(raw)
        if len(norm.split()) < 2:
            continue
        key = norm.casefold()
        if key not in by_key:
            order.append(key)
        by_key[key][norm] += 1
    out: list[str] = []
    for key in order:
        surface = by_key[key].most_common(1)[0][0]
        out.append(surface)
    return out


def main() -> int:
    if not SOURCE_CSV.exists():
        print(f"missing {SOURCE_CSV}; run the copy step first", file=sys.stderr)
        return 1
    rows = load_rows()

    kept = [
        r
        for r in rows
        if r["granularity"] in KEEP_GRANULARITY
        and r["is_placeholder_prompt"] != "True"
        and normalize(r["prompt_text"])
    ]

    per_file: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"PAM": [], "FIL": []})
    for r in kept:
        per_file[r["source_name_normalized"]][r["lang_code"]].append(r["prompt_text"])

    units: dict[str, dict[str, list[str]]] = {}

    # 1. shared-name files with content on both sides
    for fname, sides in sorted(per_file.items()):
        if fname in STORY_PAM_FILES or fname == STORY_FIL_FILE:
            continue
        pam = distinct_pool(sides["PAM"])
        fil = distinct_pool(sides["FIL"])
        if pam and fil:
            units[fname] = {"pam": pam, "fil": fil}

    # 2. the folktale cross-file unit
    story_pam_raw: list[str] = []
    for fname in STORY_PAM_FILES:
        story_pam_raw.extend(per_file.get(fname, {}).get("PAM", []))
    story_fil_raw = per_file.get(STORY_FIL_FILE, {}).get("FIL", [])
    story_pam = distinct_pool(story_pam_raw)
    story_fil = distinct_pool(story_fil_raw)
    if story_pam and story_fil:
        units[STORY_UNIT] = {"pam": story_pam, "fil": story_fil}

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    POOLS_JSON.write_text(json.dumps(units, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.writer(handle, lineterminator="\n")
        w.writerow(["unit", "pam_sentences", "fil_sentences", "candidate_pairs_pam_x_fil"])
        tot_p = tot_f = tot_x = 0
        for unit, d in units.items():
            p, f = len(d["pam"]), len(d["fil"])
            w.writerow([unit, p, f, p * f])
            tot_p += p
            tot_f += f
            tot_x += p * f
        w.writerow(["TOTAL", tot_p, tot_f, tot_x])

    manifest = {
        "source_csv": SOURCE_CSV.name,
        "source_csv_sha256": hashlib.sha256(SOURCE_CSV.read_bytes()).hexdigest(),
        "rows_total": len(rows),
        "rows_kept_sentence_or_phrase": len(kept),
        "alignment_units": len(units),
        "distinct_pam_sentences": tot_p,
        "distinct_fil_sentences": tot_f,
        "total_candidate_pairs": tot_x,
        "note": (
            "prompt_text is the elicitation prompt, not a spoken transcription; "
            "PLD redistribution rights unresolved -> local research use only"
        ),
    }
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    for unit, d in units.items():
        print(f"  {unit:<48} PAM {len(d['pam']):>4}  FIL {len(d['fil']):>4}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
