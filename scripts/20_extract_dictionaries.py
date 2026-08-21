"""Stage 20 — extract lexical entries from the source PDFs into JSONL.

    python scripts/20_extract_dictionaries.py --pdf-dir "C:/Users/Gabo/Downloads/DATASET/UNANNOTATED"

EXTRACTION ONLY. No morphological analysis, no guessed roots or affixes, no
translation, no spelling correction. Syllable data stays under `syllables`.
Missing information is left empty, never invented. Every record keeps its
dictionary name, page number and the original extracted text so it can be
checked against the PDF.

Outputs (data/extracted/):
    samson.jsonl                 Samson, Kapampangan Dictionary
    trilingual.jsonl             Kapampangan-English-Pilipino wordlist
    mirikitani_pam_eng.jsonl     Speaking Kapampangan, Kapampangan-English glossary
    mirikitani_eng_pam.jsonl     Speaking Kapampangan, English-Kapampangan vocabulary
    dayalekto.jsonl              Mga Salita sa Iba't Ibang Dayalekto
    all_entries.jsonl            all of the above concatenated
    extraction_report.json       per-source counts and OCR-flag rates
"""
from __future__ import annotations

import argparse, json, sys, time
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.extract import glossaries, samson
from kapampangan_mt.extract.schema import sort_key

#: Files that are NOT dictionaries. They are grammars and comparative papers:
#: valuable references, but they contain no lexical entries to extract, and
#: mining example words out of running prose would violate the rule that words
#: appearing only inside explanations must not become headwords.
NOT_DICTIONARIES = {
    "SL-030-forman-kapampangan-grammar-notes.pdf":
        "Forman, Kapampangan Grammar Notes — grammar, not a dictionary. "
        "Use it as the source for the affix inventory in a later stage.",
    "ilide.info-an-introduction-to-the-kapampangan-langu-pdf-pr_0f5aabe15f5d068f64c9a0185ad5b4cb.pdf":
        "Introductory lecture notes — prose with scattered examples, no entry structure.",
    "ilide.info-paghahambing-ng-wikang-kapampangan-pr_69a3c87aa6fb68cc16d0b0c89adba32f.pdf":
        "Comparative linguistics paper in Filipino — documents orthography and "
        "morphology rules; cite it, but it has no lexical entries.",
}

MIRIKITANI = ("Speaking Kapampangan -- Leatrice T_ Mirikitani -- PALI Language "
              "Texts--Philippines, Honolulu, 2021 -- University of Hawaii Press "
              "-- isbn13 9780824885922 -- 9118b77d66e91401f045c2a65ec6e26b -- "
              "Anna\u2019s Archive.pdf")


def find(pdf_dir: Path, needle: str) -> Path | None:
    for p in sorted(pdf_dir.glob("*.pdf")):
        if needle.lower() in p.name.lower():
            return p
    return None


def write(entries, path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(e.to_json() + "\n")
    return len(entries)


def summarise(entries, name: str) -> dict:
    flagged = sum(1 for e in entries if e.ocr_status == "needs_review")
    with_def = sum(1 for e in entries if e.definition)
    with_pos = sum(1 for e in entries if e.part_of_speech)
    heads = [e.headword for e in entries]
    # a real dictionary is sorted; measure how monotone the headwords are
    keys = [sort_key(h) for h in heads]
    mono = sum(1 for a, b in zip(keys, keys[1:]) if a <= b)
    return {
        "source": name,
        "entries": len(entries),
        "unique_headwords": len(set(heads)),
        "with_definition": with_def,
        "with_part_of_speech": with_pos,
        "needs_review": flagged,
        "needs_review_pct": round(100 * flagged / max(len(entries), 1), 1),
        "alphabetical_monotonicity_pct": round(100 * mono / max(len(keys) - 1, 1), 1),
        "pages_covered": len({e.source.page for e in entries}),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--out", default="data/extracted")
    ap.add_argument("--skip", nargs="*", default=[],
                    help="source keys to skip: samson trilingual mirikitani dayalekto")
    a = ap.parse_args()

    pdf_dir = Path(a.pdf_dir)
    out = Path(a.out)
    if not pdf_dir.exists():
        print(f"ERROR: {pdf_dir} not found")
        return 1

    report: dict = {"sources": [], "skipped_not_dictionaries": [], "generated": time.ctime()}
    everything = []

    # ---------------------------------------------------------------- Samson
    if "samson" not in a.skip:
        p = find(pdf_dir, "kapampangandictionaryamongsamson")
        if p:
            print(f"\n[1/4] {p.name}")
            t0 = time.time()
            es = samson.parse(str(p), first_page=15, last_page=830)
            print(f"      {len(es)} entries in {time.time() - t0:.0f}s")
            write(es, out / "samson.jsonl")
            report["sources"].append(summarise(es, "samson"))
            everything += es

    # ----------------------------------------------------------- trilingual
    if "trilingual" not in a.skip:
        p = find(pdf_dir, "ka-pampanga-n-pr")
        if p:
            print(f"\n[2/4] {p.name}")
            es = glossaries.trilingual(str(p))
            print(f"      {len(es)} entries")
            write(es, out / "trilingual.jsonl")
            report["sources"].append(summarise(es, "trilingual"))
            everything += es

    # ----------------------------------------------------------- Mirikitani
    if "mirikitani" not in a.skip:
        p = find(pdf_dir, "Speaking Kapampangan")
        if p:
            print(f"\n[3/4] {p.name[:60]}...")
            a1 = glossaries.mirikitani(str(p), 894, 967, "pam-eng")
            a2 = glossaries.mirikitani(str(p), 970, 1010, "eng-pam")
            print(f"      Kapampangan-English: {len(a1)}  English-Kapampangan: {len(a2)}")
            write(a1, out / "mirikitani_pam_eng.jsonl")
            write(a2, out / "mirikitani_eng_pam.jsonl")
            report["sources"].append(summarise(a1, "mirikitani_pam_eng"))
            report["sources"].append(summarise(a2, "mirikitani_eng_pam"))
            everything += a1 + a2

    # ------------------------------------------------------------ dayalekto
    if "dayalekto" not in a.skip:
        p = find(pdf_dir, "dayalekto")
        if p:
            print(f"\n[4/4] {p.name}")
            es = glossaries.dayalekto(str(p))
            print(f"      {len(es)} entries")
            write(es, out / "dayalekto.jsonl")
            report["sources"].append(summarise(es, "dayalekto"))
            everything += es

    # --------------------------------------------------------------- combine
    write(everything, out / "all_entries.jsonl")

    for name, why in NOT_DICTIONARIES.items():
        if (pdf_dir / name).exists():
            report["skipped_not_dictionaries"].append({"file": name, "reason": why})

    report["total_entries"] = len(everything)
    report["total_unique_headwords"] = len({e.headword.lower() for e in everything})
    (out / "extraction_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 72)
    print(f"{'source':<24}{'entries':>9}{'unique':>9}{'w/ defn':>9}"
          f"{'flagged':>9}{'sorted%':>9}")
    for s in report["sources"]:
        print(f"{s['source']:<24}{s['entries']:>9,}{s['unique_headwords']:>9,}"
              f"{s['with_definition']:>9,}{s['needs_review_pct']:>8.1f}%"
              f"{s['alphabetical_monotonicity_pct']:>8.1f}%")
    print(f"{'TOTAL':<24}{len(everything):>9,}{report['total_unique_headwords']:>9,}")
    print("\nnot extracted (not dictionaries):")
    for s in report["skipped_not_dictionaries"]:
        print(f"  - {s['file'][:58]}\n      {s['reason']}")
    print(f"\n-> {out}/all_entries.jsonl  and  {out}/extraction_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
