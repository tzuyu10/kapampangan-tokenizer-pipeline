"""Stage 21 — verify the extraction against the source PDFs.

    python scripts/21_verify_extraction.py --pdf-dir "C:/.../UNANNOTATED"

Runs the ten checks from the extraction brief and prints a pass/fail table.
Nothing is modified; this only reports.
"""
from __future__ import annotations

import argparse, json, random, re, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.extract.pdf_text import page_text
from kapampangan_mt.extract.samson import ENGLISH_STOPWORDS
from kapampangan_mt.extract.schema import sort_key

REQUIRED_KEYS = {
    "entry_id", "headword", "definition", "part_of_speech", "pronunciation",
    "syllables", "examples", "derived_forms", "spelling_variants",
    "cross_references", "source", "ocr_status", "notes",
}
#: Fields that would mean morphological analysis leaked into this stage.
FORBIDDEN_KEYS = {"root", "prefix", "suffix", "infix", "circumfix", "clitic",
                  "segmentation", "morphemes", "affix", "affix_type"}


def load(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", default=None)
    ap.add_argument("--extracted", default="data/extracted")
    ap.add_argument("--samples", type=int, default=12)
    a = ap.parse_args()

    d = Path(a.extracted)
    rows = load(d / "all_entries.jsonl")
    print(f"loaded {len(rows):,} entries from {d}/all_entries.jsonl\n")
    results: list[tuple[str, bool, str]] = []
    warnings: list[tuple[str, str]] = []

    # 1 schema -------------------------------------------------------------
    bad_schema = [r for r in rows if set(r) != REQUIRED_KEYS]
    leaked = [k for r in rows[:2000] for k in r if k in FORBIDDEN_KEYS]
    results.append(("schema keys exact on every record", not bad_schema,
                    f"{len(bad_schema)} records with unexpected keys"))
    results.append(("no morphological fields present", not leaked,
                    f"{len(set(leaked))} forbidden keys" if leaked else "none"))

    # 2 headwords ----------------------------------------------------------
    empty = [r for r in rows if not r["headword"].strip()]
    # The English-Kapampangan vocabulary has English headwords by design, so
    # the stopword rule applies only to the Kapampangan-headword sources.
    ENGLISH_HEADWORD_SOURCES = ("mirikitani-eng-pam:",)
    stop = [r for r in rows
            if not r["entry_id"].startswith(ENGLISH_HEADWORD_SOURCES)
            and r["headword"].lower() in ENGLISH_STOPWORDS]
    numeric = [r for r in rows if r["headword"].strip().isdigit()]
    # Only the tabular glossaries have column headers. In Samson, `Pilipino` is
    # a real headword ("Pilipino. (Sp. Filipino), n. any native or citizen of
    # the Philippines") and must not be filtered out.
    headerish = [r for r in rows
                 if not r["entry_id"].startswith("samson:")
                 and re.fullmatch(
                     r"(KAPAMPANGAN|ENGLISH|PILIPINO|TAGALOG|GLOSSARY|VOCABULARY)",
                     r["headword"].strip(), re.I)]
    results.append(("no empty headwords", not empty, f"{len(empty)} empty"))
    # Homographs are real: Kapampangan `are` means 'hay, straw' and collides
    # with English "are". This is reported for review, not failed automatically.
    warnings.append(("English-looking headwords in Kapampangan sources",
                     f"{len(stop)}: {[r['headword'] for r in stop][:8]} "
                     f"— check by hand; some are genuine homographs"))
    results.append(("no page numbers as headwords", not numeric, f"{len(numeric)} found"))
    results.append(("no column headers as headwords", not headerish, f"{len(headerish)} found"))

    # 3 provenance ---------------------------------------------------------
    nopage = [r for r in rows if r["source"]["page"] is None]
    notext = [r for r in rows if not r["source"]["original_text"].strip()]
    nodict = [r for r in rows if not r["source"]["dictionary"].strip()]
    results.append(("every entry carries a page number", not nopage, f"{len(nopage)} missing"))
    results.append(("every entry carries original text", not notext, f"{len(notext)} missing"))
    results.append(("every entry names its dictionary", not nodict, f"{len(nodict)} missing"))

    # 4 ids ----------------------------------------------------------------
    ids = Counter(r["entry_id"] for r in rows)
    dupes = [k for k, v in ids.items() if v > 1]
    results.append(("entry_ids unique", not dupes, f"{len(dupes)} duplicated"))

    # 5 ocr flags ----------------------------------------------------------
    flagged = [r for r in rows if r["ocr_status"] == "needs_review"]
    unflagged_no_note = [r for r in rows
                         if r["ocr_status"] == "clear" and "Possible OCR error" in r["notes"]]
    results.append(("flagged entries all carry a note",
                    all(r["notes"].strip() for r in flagged), ""))
    results.append(("no 'clear' entry hides an OCR note", not unflagged_no_note,
                    f"{len(unflagged_no_note)} inconsistent"))

    # 6 headword appears in its own source text ----------------------------
    missing_head = [r for r in rows
                    if r["headword"][:4].lower() not in r["source"]["original_text"].lower()]
    ok = len(missing_head) / max(len(rows), 1) < 0.02
    results.append(("headword traceable in its original_text", ok,
                    f"{len(missing_head)} ({100*len(missing_head)/len(rows):.1f}%) not found"))

    print(f"{'check':<46}{'result':<8}{'detail'}")
    print("-" * 92)
    for name, passed, detail in results:
        print(f"{name:<46}{'PASS' if passed else 'FAIL':<8}{detail}")

    if warnings:
        print("\nfor human review (not failures):")
        for name, detail in warnings:
            print(f"  {name}: {detail}")

    # 7 alphabetical spot-check against the real pages ---------------------
    if a.pdf_dir:
        pdf_dir = Path(a.pdf_dir)
        sam = [p for p in pdf_dir.glob("*.pdf") if "samson" in p.name.lower()]
        if sam:
            print(f"\nspot-check: {a.samples} random Samson entries vs the actual PDF page")
            rng = random.Random(13)
            pool = [r for r in rows if r["entry_id"].startswith("samson:")]
            hits = 0
            for r in rng.sample(pool, min(a.samples, len(pool))):
                pg = r["source"]["page"]
                txt = page_text(str(sam[0]), pg - 1).lower()
                found = r["headword"].lower()[:6] in txt.replace("\n", " ")
                hits += found
                print(f"  p{pg:<5} {r['headword'][:24]:<26} "
                      f"{'found on page' if found else 'NOT FOUND'}")
            print(f"  -> {hits}/{a.samples} headwords located on their recorded page")

    # 8 note breakdown -----------------------------------------------------
    reasons = Counter()
    for r in rows:
        for part in re.split(r"(?<=\.)\s+", r["notes"]):
            if part.strip():
                reasons[part.strip()[:70]] += 1
    print("\nmost common review reasons:")
    for reason, n in reasons.most_common(8):
        print(f"  {n:>6,}  {reason}")

    failed = [n for n, p, _ in results if not p]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
