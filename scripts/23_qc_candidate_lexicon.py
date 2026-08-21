"""Stage 23 — the 24 quality-control checks on the candidate lexicon.

    python scripts/23_qc_candidate_lexicon.py --pdf-dir "C:/.../UNANNOTATED"

Reports only; nothing is modified.
"""
from __future__ import annotations

import argparse, json, random, re, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.extract.pdf_text import page_text

VALID_STATUS = {"simple", "derived", "inflected", "compound", "variant", "unknown"}
VALID_SOURCE = {"dictionary_explicit", "AI_proposed", "unknown"}
VALID_CONF = {"high", "medium", "low"}

ENGLISH_DEFN_WORDS = {
    "drown", "water", "house", "person", "the", "and", "with", "from", "that",
    "which", "abbreviation", "abortion", "embrace", "fertilizer", "anchor",
    "morning", "become", "someone", "something", "another", "himself",
}
# 'tubig' is deliberately absent: it is a real Samson headword
# ("tubig. Tubigtubigan. n. pimples which are watery..."), not a Filipino
# definition word that leaked in. Homographs across the two languages are
# expected and must not be filtered out.
FILIPINO_DEFN_WORDS = {"kain", "bahay", "araw", "gabi", "lahat", "ganda"}
METADATA = {"bibliography", "copyright", "isbn", "dictionary", "glossary",
            "vocabulary", "abbreviations", "appendix", "preface", "index"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lexicon", default="data/lexicon_candidate/candidate_lexicon.jsonl")
    ap.add_argument("--pdf-dir", default=None)
    ap.add_argument("--samples", type=int, default=12)
    a = ap.parse_args()

    rows = [json.loads(l) for l in
            Path(a.lexicon).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"loaded {len(rows):,} candidate entries\n")
    inv = json.loads(Path("data/lexicon_candidate/affix_inventory.json")
                     .read_text(encoding="utf-8"))
    licensed = {k: set(v) for k, v in inv["licensed"].items()}
    checks: list[tuple[str, bool, str]] = []

    def chk(name, bad, detail=""):
        checks.append((name, not bad, detail or (f"{len(bad)} offending" if bad else "")))

    # 1-6 what may be an entry ------------------------------------------------
    chk("1. every entry has a non-empty headword",
        [r for r in rows if not r["headword"].strip()])
    chk("2. no English definition word as headword",
        [r for r in rows if r["headword"].lower() in ENGLISH_DEFN_WORDS])
    chk("3. no Filipino definition word as headword",
        [r for r in rows if r["headword"].lower() in FILIPINO_DEFN_WORDS])
    # Mirikitani prints verb roots in full capitals as an editorial convention
    # (ALIKABOK, DAGDAG, BATING), so "all caps" does not mean "page header".
    # Only actual section titles are disqualifying.
    SECTION_TITLES = {"GLOSSARY", "VOCABULARY", "ABBREVIATIONS", "KAPAMPANGAN",
                      "ENGLISH", "PILIPINO", "TAGALOG", "BIBLIOGRAPHY", "INDEX"}
    chk("4. no page headers or section titles as entries",
        [r for r in rows if r["headword"].strip().upper() in SECTION_TITLES
         and not r["entry_id"].startswith("samson:")])
    chk("5. no page numbers as entries",
        [r for r in rows if r["headword"].strip().isdigit()])
    chk("6. no dictionary metadata as entries",
        [r for r in rows if r["headword"].lower() in METADATA])

    # 7-8 the two cardinal errors --------------------------------------------
    bad7 = [r for r in rows
            if r["morphology"]["root"]
            and r["morphology"]["root"] == r["headword"].lower()
            and r["morphology"]["status"] != "simple"]
    chk("7. root never silently copied from the headword", bad7)
    # a segmentation whose parts are just the syllable list would mean syllables
    # were read as morphemes
    bad8 = [r for r in rows
            if r["syllables"]
            and r["morphology"]["segmentation"].replace(" + ", "") ==
            "".join(r["syllables"])
            and len(r["syllables"]) > 1
            and r["morphology"]["segmentation"].count("+") == len(r["syllables"]) - 1]
    chk("8. syllables never treated as morphemes", bad8)

    # 9-13 no invented affixes ------------------------------------------------
    def unlicensed(field, kind, strip):
        out = []
        for r in rows:
            for aff in r["morphology"][field]:
                if strip(aff) not in licensed[kind]:
                    out.append((r["entry_id"], aff))
        return out

    chk("9.  no unlicensed prefixes",
        unlicensed("prefixes", "prefix", lambda s: s.rstrip("-")))
    chk("10. no unlicensed infixes",
        unlicensed("infixes", "infix", lambda s: s.strip("-")))
    chk("11. no unlicensed suffixes",
        unlicensed("suffixes", "suffix", lambda s: s.lstrip("-")))
    chk("12. no unlicensed circumfixes",
        unlicensed("circumfixes", "circumfix", lambda s: s))
    chk("13. no clitics invented (none are dictionary-attested)",
        [r for r in rows if r["morphology"]["clitics"]])

    # 14-15 variants and derived forms ---------------------------------------
    chk("14. spelling variants only where the source gave one",
        [r for r in rows if r["spelling_variants"]
         and "explicit" not in r["evidence"] and r["morphology"]["status"] != "variant"
         and r["annotation_source"] != "dictionary_explicit"])
    chk("15. derived forms only from printed paradigms",
        [r for r in rows if r["derived_forms"]
         and r["annotation_source"] != "dictionary_explicit"])

    # 16-19 provenance --------------------------------------------------------
    ids = Counter(r["entry_id"] for r in rows)
    chk("16. entries not merged (ids unique)", [k for k, v in ids.items() if v > 1])
    chk("17. original spelling preserved (headword in original_text)",
        [r for r in rows
         if r["headword"][:4].lower() not in r["source"]["original_text"].lower()])
    chk("18. page number preserved", [r for r in rows if r["source"]["page"] is None])
    chk("19. OCR problems flagged",
        [r for r in rows if "Possible OCR error" in r["notes"] and r["ocr_status"] != "needs_review"])

    # 20-24 annotation discipline ---------------------------------------------
    chk("20. every inferred analysis marked AI_proposed",
        [r for r in rows
         if r["morphology"]["segmentation"] and "Heuristic inference" in r["evidence"]
         and r["annotation_source"] != "AI_proposed"])
    chk("21. uncertain analyses marked (status unknown => no root/segmentation)",
        [r for r in rows if r["morphology"]["status"] == "unknown"
         and (r["morphology"]["root"] or r["morphology"]["segmentation"])])
    chk("22. every entry validation_status=unvalidated",
        [r for r in rows if r["validation_status"] != "unvalidated"])
    chk("23. every non-trivial analysis carries evidence",
        [r for r in rows if r["morphology"]["segmentation"] and not r["evidence"].strip()])
    chk("24. controlled vocabularies respected",
        [r for r in rows if r["morphology"]["status"] not in VALID_STATUS
         or r["annotation_source"] not in VALID_SOURCE
         or r["confidence"] not in VALID_CONF])

    width = max(len(n) for n, _, _ in checks) + 2
    for name, ok, detail in checks:
        print(f"{name:<{width}}{'PASS' if ok else 'FAIL':<7}{detail}")
    failed = [n for n, ok, _ in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")

    # traceability spot-check against the PDF --------------------------------
    if a.pdf_dir:
        pdfs = list(Path(a.pdf_dir).glob("*.pdf"))
        sam = [p for p in pdfs if "samson" in p.name.lower()]
        if sam:
            print(f"\ntraceability: {a.samples} random dictionary_explicit analyses vs the PDF")
            rng = random.Random(7)
            pool = [r for r in rows if r["annotation_source"] == "dictionary_explicit"
                    and r["entry_id"].startswith("samson:") and r["morphology"]["root"]]
            hits = 0
            for r in rng.sample(pool, min(a.samples, len(pool))):
                m = re.search(r"page (\d+)", r["evidence"])
                pg = int(m.group(1)) if m else r["source"]["page"]
                txt = page_text(str(sam[0]), pg - 1).lower().replace("\n", " ")
                ok = r["headword"].lower()[:6] in txt
                hits += ok
                print(f"  p{pg:<5} {r['headword'][:20]:<22} root={str(r['morphology']['root'])[:16]:<18}"
                      f"{'verified on page' if ok else 'NOT ON PAGE'}")
            print(f"  -> {hits}/{a.samples} verified against the original PDF")

    print("\nreminder: validation_status is 'unvalidated' on every record. "
          "This is a CANDIDATE lexicon, not a validated linguistic resource.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
