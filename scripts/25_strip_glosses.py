"""Stage 25 — remove copyrighted definition text from the committed lexicon.

    python scripts/25_strip_glosses.py           # show what would change
    python scripts/25_strip_glosses.py --apply   # do it

`roots.tsv` carries a `gloss_fil` column filled with definitions copied
verbatim from the source dictionaries — 8,458 rows, mostly Samson. In a PUBLIC
repository that republishes copyrighted text.

The segmenter never reads that column. `Lexicon.load()` uses `root` only, so
blanking the glosses changes nothing about how the tokenizer behaves. The
`source` column (dictionary name + page) is kept, because that is what makes
each entry checkable — a citation, not a reproduction.
"""
from __future__ import annotations

import argparse, csv, sys
from pathlib import Path

TARGETS = {
    "roots.tsv": "gloss_fil",
    "prefixes.tsv": "gloss",
    "infixes.tsv": "gloss",
    "suffixes.tsv": "gloss",
    "circumfixes.tsv": "gloss",
    "clitics.tsv": "gloss",
    "compounds.tsv": "gloss",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lexicon-dir", default="data/lexicon")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    d = Path(a.lexicon_dir)
    total_chars = total_rows = 0

    for name, col in TARGETS.items():
        p = d / name
        if not p.exists():
            continue
        with p.open(encoding="utf-8", newline="") as fh:
            lines = [l for l in fh if l.strip() and not l.lstrip().startswith("#")]
        if not lines:
            continue
        rows = list(csv.DictReader(lines, delimiter="\t"))
        if not rows or col not in rows[0]:
            continue
        hits = [r for r in rows if (r.get(col) or "").strip()]
        chars = sum(len(r.get(col) or "") for r in rows)
        total_chars += chars
        total_rows += len(hits)
        print(f"  {name:<20} {len(hits):>6,} rows with text  ({chars:,} chars)")
        if a.apply:
            header = list(rows[0])
            for r in rows:
                r[col] = ""
            with p.open("w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=header, delimiter="\t",
                                   lineterminator="\n")
                w.writeheader()
                w.writerows(rows)

    print(f"\n{total_rows:,} rows, {total_chars:,} characters of dictionary text")
    if a.apply:
        print("REMOVED. The `source` column (dictionary + page) is kept as a citation.")
        print("Re-run scripts/01_validate_lexicon.py — coverage should be unchanged.")
    else:
        print("Dry run. Re-run with --apply to remove.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
