"""Stage 10 — ingest the project's real DATASET folder.

    python scripts/10_ingest_dataset.py --dataset "C:/Users/<you>/Downloads/DATASET"

Reads:
    CLEANED_JSON/Kapampangan_Religious_Text-1_cleaned.json
    CLEANED_JSON/Kapampangan_Literary_Text-1_cleaned.json
    CLEANED_JSON/kapampangan_annotated.json

Writes:
    data/raw/mono_pam.tsv           cleaned monolingual Kapampangan (tokenizer training)
    data/lexicon/*.tsv              Lexicon Dictionary derived from the dictionary
    data/gold/segmentation_candidates.tsv   pre-filled MBF1 annotation candidates
    data/raw/ingest_report.json     full audit trail of what was dropped and why

The lexicon files are OVERWRITTEN. Keep any hand-validated rows in a separate
branch or pass --lexicon-out to write elsewhere and merge manually.
"""
from __future__ import annotations

import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.data.ingest import (
    clean_corpus_json, parse_annotated_dictionary, strip_pali,
)
from kapampangan_mt.pretokenize import normalized_words


def w(path: Path, header: list[str], rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="") as fh:
        cw = csv.writer(fh, delimiter="\t", lineterminator="\n")
        cw.writerow(header)
        for r in rows:
            cw.writerow(r); n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="path to the DATASET folder")
    ap.add_argument("--out", default="data")
    ap.add_argument("--lexicon-out", default=None)
    ap.add_argument("--min-affix-count", type=int, default=2,
                    help="ignore affixes attested fewer than this many times")
    a = ap.parse_args()

    ds = Path(a.dataset)
    cj = ds / "CLEANED_JSON"
    out = Path(a.out)
    lex_dir = Path(a.lexicon_out) if a.lexicon_out else out / "lexicon"
    report: dict = {}

    # ------------------------------------------------ 1. corpus text
    sources = [
        ("religious", cj / "Kapampangan_Religious_Text-1_cleaned.json"),
        ("literary", cj / "Kapampangan_Literary_Text-1_cleaned.json"),
    ]
    lines = []
    for domain, path in sources:
        if not path.exists():
            print(f"  MISSING {path}"); continue
        recs, rep = clean_corpus_json(path, domain)
        lines += recs
        report[domain] = rep.as_dict()
        print(f"[{domain}] kept {rep.kept:,} of {rep.as_dict()['total']:,} records")
        for k, v in rep.dropped.most_common():
            print(f"      dropped {v:>6,}  {k}")

    n = w(out / "raw" / "mono_pam.tsv", ["pam", "domain", "ref"],
          ((r.text, r.domain, r.ref) for r in lines))
    toks = [t for r in lines for t in normalized_words(r.text)]
    types = Counter(toks)
    print(f"\nmonolingual corpus -> {out/'raw'/'mono_pam.tsv'}")
    print(f"  {n:,} lines | {len(toks):,} word tokens | {len(types):,} word types")
    report["corpus"] = {"lines": n, "tokens": len(toks), "types": len(types),
                        "hapax_share": sum(1 for c in types.values() if c == 1) / max(len(types), 1)}

    # ------------------------------------------------ 2. lexicon
    ann = cj / "kapampangan_annotated.json"
    if not ann.exists():
        print(f"MISSING {ann}"); return 1
    D = parse_annotated_dictionary(ann)
    print(f"\ndictionary: {D['stats']}")

    # A dictionary lists derived lemmas as headwords (sumulat, masanting,
    # mangabala). If those land in roots.tsv, Figure 7's rule 2 matches them
    # first and returns them UNSEGMENTED. Demote any headword the dictionary
    # itself analyses as an affixed form of a different, known root.
    demoted = {f for f, d in D["derived"].items()
               if f in D["roots"] and d["root"] in D["roots"] and d["root"] != f}
    root_rows = [(r, v["gloss"][:80].replace("\t", " "), v["pos"], f"PALI:{v['headword']}")
                 for r, v in sorted(D["roots"].items()) if r not in demoted]
    # The PALI dictionary lists content words only. Grammatical morphemes
    # (ing, king, ding, ya, la, ku, ala, e ...) carry roughly a third of all
    # corpus tokens; without them the segmenter cannot analyse a third of the
    # text no matter how good the algorithm is. Merge the hand-written set.
    fw = lex_dir / "function_words.tsv"
    n_fw = 0
    if fw.exists():
        have = {r[0] for r in root_rows}
        with fw.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(
                    [l for l in fh if l.strip() and not l.lstrip().startswith("#")],
                    delimiter="\t"):
                w_ = (r.get("root") or "").strip()
                if w_ and w_ not in have:
                    root_rows.append((w_, r.get("gloss_fil", ""), r.get("pos", ""),
                                      r.get("source", "SEED-FUNC")))
                    have.add(w_); n_fw += 1
        root_rows.sort()
    print(f"  merged {n_fw} grammatical morphemes from function_words.tsv")
    nr = w(lex_dir / "roots.tsv", ["root", "gloss_fil", "pos", "source"], root_rows)
    w(lex_dir / "derived_forms.tsv",
      ["form", "segmentation", "root", "note", "source"],
      ((f, d["segmentation"], d["root"],
        "demoted from roots.tsv" if f in demoted else "", "annotated")
       for f, d in sorted(D["derived"].items())))
    print(f"  demoted {len(demoted):,} derived headwords out of roots.tsv "
          f"(they would have blocked segmentation)")

    pref_rows = [(p, "", "", f"annotated x{c}")
                 for p, c in sorted(D["prefixes"].items()) if c >= a.min_affix_count]
    np_ = w(lex_dir / "prefixes.tsv", ["prefix", "gloss", "allomorphs", "source"], pref_rows)
    ni = w(lex_dir / "infixes.tsv", ["infix", "gloss", "source"],
           ((i, "", f"annotated x{c}") for i, c in sorted(D["infixes"].items()) if c >= a.min_affix_count))
    ns = w(lex_dir / "suffixes.tsv", ["suffix", "gloss", "allomorphs", "source"],
           ((s, "", "", f"annotated x{c}") for s, c in sorted(D["suffixes"].items()) if c >= a.min_affix_count))
    nc = w(lex_dir / "circumfixes.tsv", ["prefix", "suffix", "gloss", "source"],
           ((l, r, "", f"annotated x{c}") for (l, r), c in sorted(D["circumfixes"].items()) if c >= a.min_affix_count))
    nv = w(lex_dir / "variants.tsv", ["variant", "canonical", "note", "source"],
           ((v, c, "PALI orthography / attested surface form", "annotated")
            for v, c in sorted(D["variants"].items())
            if v != c and v.isalpha() and c in D["roots"]))

    for name, header, rows in [
        ("clitics.tsv", ["clitic", "type", "gloss", "source"], []),
        ("compounds.tsv", ["compound", "parts", "gloss", "source"], []),
    ]:
        p = lex_dir / name
        if not p.exists():
            w(p, header, rows)

    print(f"lexicon -> {lex_dir}")
    print(f"  roots {nr:,} | prefixes {np_} | infixes {ni} | suffixes {ns} "
          f"| circumfixes {nc} | variants {nv:,}")
    print("  NOTE: clitics.tsv was NOT overwritten — the dictionary has no clitic "
          "inventory, keep the hand-written one.")
    report["lexicon"] = {"roots": nr, "prefixes": np_, "infixes": ni,
                         "suffixes": ns, "circumfixes": nc, "variants": nv,
                         "reduplication_patterns": len(D["redup"])}

    # ------------------------------------------------ 3. gold candidates
    usable = [s for s in D["segmentations"] if s["concatenates"] and s["segmentation"]]
    seen: set[str] = set()
    rows = []
    for s in usable:
        if s["form"] in seen:
            continue
        seen.add(s["form"])
        rows.append((s["form"], s["segmentation"], s["segmentation"],
                     s["affix_type"], s["affix"], s["root"],
                     types.get(s["form"], 0), "", "auto", s["confidence"]))
    ng = w(out / "gold" / "segmentation_candidates.tsv",
           ["word", "segmentation", "suggested", "affix_type", "affix", "root",
            "corpus_count", "annotator", "provenance", "notes"], rows)
    in_corpus = sum(1 for r in rows if r[6] > 0)
    print(f"\ngold candidates -> {out/'gold'/'segmentation_candidates.tsv'}")
    print(f"  {ng:,} dictionary-segmented forms ({in_corpus:,} of them occur in the corpus)")
    print("  provenance=auto — a human must review before these count as gold.")
    report["gold_candidates"] = {"rows": ng, "occurring_in_corpus": in_corpus,
                                 "unusable_segmentations": D["stats"].get("seg_unusable", 0)}

    (out / "raw" / "ingest_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    print(f"\naudit -> {out/'raw'/'ingest_report.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
