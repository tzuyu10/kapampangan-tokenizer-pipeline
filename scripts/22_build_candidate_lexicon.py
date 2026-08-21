"""Stage 22 — build the AI-assisted CANDIDATE morphological lexicon.

    python scripts/22_build_candidate_lexicon.py

Input : data/extracted/*.jsonl  (stage 20)
Output: data/lexicon_candidate/candidate_lexicon.jsonl
        data/lexicon_candidate/affix_inventory.json
        data/lexicon_candidate/build_report.json

Everything is grounded in what the supplied dictionary asserts. No external
knowledge of Kapampangan licenses an analysis. Every record carries
validation_status="unvalidated" and must be reviewed by a native speaker or
linguist before use.
"""
from __future__ import annotations

import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.extract.morph_candidate import (
    annotate, classify_pair, derive_affix_inventory, explicit_paradigms,
)

#: English headwords by design — excluded from a Kapampangan lexicon.
EXCLUDE_PREFIXES = ("mirikitani-eng-pam:",)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracted", default="data/extracted")
    ap.add_argument("--out", default="data/lexicon_candidate")
    a = ap.parse_args()

    src = Path(a.extracted) / "all_entries.jsonl"
    if not src.exists():
        print(f"ERROR: {src} not found — run scripts/20_extract_dictionaries.py first")
        return 1
    rows = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
    kap = [r for r in rows if not r["entry_id"].startswith(EXCLUDE_PREFIXES)]
    print(f"{len(rows):,} extracted entries -> {len(kap):,} with Kapampangan headwords")
    print(f"  ({len(rows) - len(kap):,} English-headword records excluded: they are the "
          f"English->Kapampangan direction, not Kapampangan lexical entries)")

    samson = [r for r in kap if r["entry_id"].startswith("samson:")]

    # --- what the dictionary explicitly states ---------------------------
    paradigms = explicit_paradigms(samson)
    print(f"\nentries printing an explicit paradigm: {len(paradigms):,}")

    inventory = derive_affix_inventory(paradigms)
    print(f"explicit (headword -> form) statements: {inventory['explicit_pairs']:,}")
    print(f"  of which non-concatenative (morphophonemic): "
          f"{inventory['non_concatenative_pairs']:,} "
          f"({100*inventory['non_concatenative_pairs']/max(inventory['explicit_pairs'],1):.0f}%) "
          f"— these give a root but no segmentation")
    print("\nLICENSED AFFIX INVENTORY (derived from the dictionary's own statements):")
    for kind in ("prefix", "infix", "suffix", "circumfix", "redup"):
        lic = inventory["licensed"][kind]
        shown = sorted(lic.items(), key=lambda kv: -kv[1])[:12]
        pretty = ", ".join(
            f"{(k[0]+'-...-'+k[1]) if isinstance(k, tuple) else k}({v})" for k, v in shown)
        print(f"  {kind:<11} {len(lic):>3} licensed: {pretty}")

    # --- indexes ----------------------------------------------------------
    lemmas: dict[str, dict] = {}
    for r in samson:
        lemmas.setdefault(r["headword"].lower(), {"page": r["source"]["page"]})
    form_owner: dict[str, list] = defaultdict(list)
    for head, rec in paradigms.items():
        for f in rec["forms"]:
            form_owner[f].append((head, rec["page"]))

    # --- annotate ---------------------------------------------------------
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = [annotate(r, lemmas, paradigms, form_owner, inventory) for r in kap]

    with (out_dir / "candidate_lexicon.jsonl").open("w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(e.to_json() + "\n")

    inv_out = {
        "method": (
            "Affixes are counted only over relationships the dictionary itself "
            "prints inside its entries (verb paradigms, infinitives, P.1/P.2 "
            "forms). A plain substring search over headwords was rejected: it "
            "returns artefacts such as p- (94 hits, e.g. plato = p- + lato) and "
            "-s (122 hits), which are string coincidences rather than morphology."
        ),
        "frequency_floors": {"prefix": 20, "infix": 20, "suffix": 5,
                             "circumfix": 5, "reduplication": 3},
        "explicit_pairs": inventory["explicit_pairs"],
        "non_concatenative_pairs": inventory["non_concatenative_pairs"],
        "licensed": {k: {(f"{a[0]}-...-{a[1]}" if isinstance(a, tuple) else a): c
                         for a, c in v.items()}
                     for k, v in inventory["licensed"].items()},
        "all_observed_counts": {k: {(f"{a[0]}-...-{a[1]}" if isinstance(a, tuple) else a): c
                                    for a, c in v.items()}
                                for k, v in inventory["counts"].items()},
        "examples": {k: v for k, v in inventory["examples"].items()},
    }
    (out_dir / "affix_inventory.json").write_text(
        json.dumps(inv_out, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- report -----------------------------------------------------------
    status = Counter(e.morphology.status for e in entries)
    ann = Counter(e.annotation_source for e in entries)
    conf = Counter(e.confidence for e in entries)
    with_root = sum(1 for e in entries if e.morphology.root)
    with_seg = sum(1 for e in entries if e.morphology.segmentation)
    root_eq_head = sum(1 for e in entries
                       if e.morphology.root and e.morphology.root == e.headword.lower()
                       and e.morphology.status != "simple")
    report = {
        "input_entries": len(rows),
        "kapampangan_entries": len(kap),
        "excluded_english_headwords": len(rows) - len(kap),
        "morphological_status": dict(status),
        "annotation_source": dict(ann),
        "confidence": dict(conf),
        "with_root": with_root,
        "with_segmentation": with_seg,
        "root_copied_from_headword_outside_simple": root_eq_head,
        "all_unvalidated": all(e.validation_status == "unvalidated" for e in entries),
    }
    (out_dir / "build_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'':-<58}")
    print(f"candidate entries          {len(entries):>8,}")
    print("morphological status:")
    for k, v in status.most_common():
        print(f"    {k:<12} {v:>8,}  ({100*v/len(entries):>4.1f}%)")
    print("annotation source:")
    for k, v in ann.most_common():
        print(f"    {k:<20} {v:>8,}  ({100*v/len(entries):>4.1f}%)")
    print("confidence:")
    for k, v in conf.most_common():
        print(f"    {k:<12} {v:>8,}")
    print(f"with a root proposed       {with_root:>8,}")
    print(f"with a segmentation        {with_seg:>8,}")
    print(f"\n-> {out_dir}/candidate_lexicon.jsonl")
    print(f"-> {out_dir}/affix_inventory.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
