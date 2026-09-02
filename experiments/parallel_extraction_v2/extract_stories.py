"""Phase 3 data step (parallel_extraction_v2), part 4: extract the
native-authored Kapampangan story pairs.

Source: resources/kapampangan-stories-sentence-by-sentence.pdf (copied with a
SHA-256 provenance manifest). Per the user, the Kapampangan stories and
their Filipino sentence-by-sentence translations were written/translated by
a native Kapampangan speaker -- so this is the highest-quality
connected-narrative PAM<->FIL data in the project, and the only source of
modern / everyday / cultural register (the PLD holdings are folklore-only or
short elicitation prompts).

Layout: a heading, then numbered stories `<n>. <title>`, each a run of
lines `KP: <kapampangan sentence>  FIL: <filipino sentence>` (a FIL segment
may wrap across raw PDF lines and runs until the next `KP:` or the next
story heading).

Needs `pymupdf` (global Python; see AGENT_CONTEXT.md 2026-08-31 tooling
notes). Writes:
  data/story-pairs.csv        -- pair_id, story_num, story_title, pam_text, fil_text
  reports/story-pairs-manifest.json
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
PDF = EXPERIMENT_ROOT / "resources/kapampangan-stories-sentence-by-sentence.pdf"
OUT_CSV = EXPERIMENT_ROOT / "data/story-pairs.csv"
MANIFEST = EXPERIMENT_ROOT / "reports/story-pairs-manifest.json"

_HEADER = re.compile(r"\n\s*(\d+)\.\s+([^\n]+?)\s*\n")
_WS = re.compile(r"\s+")
_EN_DASH = chr(0x2013)


def norm(text: str) -> str:
    return _WS.sub(" ", text.replace(_EN_DASH, "-").strip())


def pairs_in(body: str) -> list[tuple[str, str]]:
    # join wrapped lines that are not a new KP:/FIL: marker
    body = re.sub(r"\n(?!KP:|FIL:)", " ", body)
    out: list[tuple[str, str]] = []
    for segment in body.split("KP:")[1:]:
        if "FIL:" not in segment:
            continue
        kp, fil = segment.split("FIL:", 1)
        kp, fil = norm(kp), norm(fil)
        if kp and fil:
            out.append((kp, fil))
    return out


def main() -> int:
    if not PDF.exists():
        print(f"missing {PDF}", file=sys.stderr)
        return 1
    try:
        import pymupdf
    except ImportError:
        print("needs pymupdf (global Python install); see AGENT_CONTEXT.md", file=sys.stderr)
        return 1

    with pymupdf.open(PDF) as doc:
        text = "\n" + "\n".join(page.get_text() for page in doc)

    # split "\n<preamble>\n1. Title\n<body>\n2. Title\n<body>..."
    parts = _HEADER.split(text)
    rows: list[dict[str, str]] = []
    n = 0
    stories = 0
    for i in range(1, len(parts), 3):
        num, title, body = parts[i], norm(parts[i + 1]), parts[i + 2]
        stories += 1
        for kp, fil in pairs_in(body):
            n += 1
            rows.append(
                {
                    "pair_id": f"story_{n:04d}",
                    "story_num": num,
                    "story_title": title,
                    "pam_text": kp,
                    "fil_text": fil,
                }
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(
            handle,
            fieldnames=["pair_id", "story_num", "story_title", "pam_text", "fil_text"],
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(rows)

    from collections import Counter

    per_story = Counter((r["story_num"], r["story_title"]) for r in rows)
    manifest = {
        "source_pdf": PDF.name,
        "source_pdf_sha256": hashlib.sha256(PDF.read_bytes()).hexdigest(),
        "output_csv_sha256": hashlib.sha256(OUT_CSV.read_bytes()).hexdigest(),
        "stories": stories,
        "pairs": len(rows),
        "pairs_per_story": {f"{k[0]}. {k[1]}": v for k, v in per_story.items()},
        "tier": "gold_stories (native-authored per the user)",
        "register": "modern / everyday / cultural connected narrative",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
