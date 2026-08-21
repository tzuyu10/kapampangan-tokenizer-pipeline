"""Stage 24 — merge the candidate lexicon into the working Lexicon Dictionary.

    python scripts/24_merge_candidate_lexicon.py                       # safe default
    python scripts/24_merge_candidate_lexicon.py --include AI_proposed # riskier

This is the missing link between `data/lexicon_candidate/` (what the dictionary
extraction produced) and `data/lexicon/` (what the tokenizer actually loads).

Two decisions it makes explicit
-------------------------------
**Which claims to admit.** Default is `dictionary_explicit` only: analyses the
dictionary itself prints. Admitting `AI_proposed` means unvalidated machine
guesses shape Morph-BPE training, which is a question you will be asked at your
defence. Use `--include AI_proposed --min-confidence medium` if you want them,
and say so in Chapter 3.

**Orthography.** Samson is written in the Spanish-era system (`acu`, `quing`,
`cacu`, `manğacû`); the corpus uses the modern one (`aku`, `king`, `kaku`).
Without normalisation almost none of Samson's 9,000 headwords match a corpus
token, so the merge would add bulk and no coverage. Rules come from
`data/lexicon/orthography_rules.tsv` — the same file the segmenter uses, so
lexicon and corpus are normalised identically.

Both the normalised form and the original spelling are written: the normalised
form becomes the root, the original goes to `variants.tsv`, so nothing from the
source is lost and every entry stays traceable.
"""
from __future__ import annotations

import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.pretokenize import words_only
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig

CONF_RANK = {"low": 0, "medium": 1, "high": 2}


def read_tsv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        lines = [l for l in fh if l.strip() and not l.lstrip().startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t")) if lines else []


def write_tsv(path: Path, header: list[str], rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def coverage(lex_dir: Path, norm: Normalizer, seg_cfg: dict, corpus: list[str]) -> tuple[float, float]:
    lex = Lexicon.load(lex_dir)
    seg = MorphologicalSegmenter(lex, normalizer=norm, config=SegmenterConfig(**seg_cfg))
    freq = Counter(w for s in corpus for w in words_only(norm.normalize_text(s)))
    t = k = 0
    for w, c in freq.items():
        if seg.segment(w).analyzed:
            t += 1
            k += c
    return t / max(len(freq), 1), k / max(sum(freq.values()), 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--candidate", default="data/lexicon_candidate/candidate_lexicon.jsonl")
    ap.add_argument("--inventory", default="data/lexicon_candidate/affix_inventory.json")
    ap.add_argument("--include", nargs="*", default=["dictionary_explicit"],
                    choices=["dictionary_explicit", "AI_proposed"])
    ap.add_argument("--min-confidence", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--roots-from", default="all-headwords",
                    choices=["analysed", "all-headwords"],
                    help=("analysed: only entries carrying a morphological analysis. "
                          "all-headwords: every dictionary headword EXCEPT those the "
                          "dictionary itself analyses as derived. A headword is a "
                          "lexical entry whether or not its morphology is known, and "
                          "roots.tsv is an INVENTORY of word forms, not a set of "
                          "analyses."))
    ap.add_argument("--keep-analysable-roots", action="store_true",
                    help=("By default a headword that decomposes into a licensed "
                          "affix plus ANOTHER headword is written to "
                          "derived_forms.tsv instead of roots.tsv. Figure 7 tests "
                          "bare roots BEFORE any affix rule, so leaving `masanting` "
                          "in roots.tsv makes the segmenter return it whole instead "
                          "of ma- + santing. Pass this flag to disable the demotion "
                          "and see the difference."))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cfg = load_config(a.config)

    lex_dir = Path(cfg.get_path("paths.lexicon_dir"))
    norm = Normalizer.from_rules_file(lex_dir / "orthography_rules.tsv",
                                      lowercase=True, strip_accents=True)
    seg_cfg = cfg.get_path("segmenter", {})

    cand_path = Path(a.candidate)
    if not cand_path.exists():
        print(f"ERROR: {cand_path} not found — run scripts/22_build_candidate_lexicon.py first")
        return 1
    cands = [json.loads(l) for l in cand_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    inv = json.loads(Path(a.inventory).read_text(encoding="utf-8"))

    corpus_path = Path(cfg.get_path("paths.processed_dir")) / "train.tsv"
    corpus = [r["pam"] for r in read_tsv(corpus_path)] if corpus_path.exists() else []
    before = coverage(lex_dir, norm, seg_cfg, corpus) if corpus else (0.0, 0.0)

    # ---------------------------------------------------------------- filter
    floor = CONF_RANK[a.min_confidence]
    analysed = [c for c in cands
                if c["annotation_source"] in a.include
                and CONF_RANK[c["confidence"]] >= floor]
    if a.roots_from == "analysed":
        kept = analysed
    else:
        # Entries the dictionary itself analyses as DERIVED are excluded on
        # purpose. Adding `sumulat` to roots.tsv would make Figure 7's rule 2
        # (bare-root match) fire before any affix rule and return the word
        # unsegmented — the exact failure this pipeline exists to prevent.
        kept = [c for c in cands if c["morphology"]["status"] != "derived"]
    print(f"candidate entries          {len(cands):>8,}")
    print(f"  carrying an accepted analysis {len(analysed):>6,}   "
          f"(source in {a.include}, confidence >= {a.min_confidence})")
    print(f"  admitted as roots            {len(kept):>6,}   (--roots-from {a.roots_from})")

    # ------------------------------------------------------------- roots
    existing_roots = {r["root"]: r for r in read_tsv(lex_dir / "roots.tsv") if r.get("root")}
    func_rows = read_tsv(lex_dir / "function_words.tsv")
    new_roots: dict[str, tuple] = {}
    variants: dict[str, str] = {}
    skipped_nonalpha = 0

    for c in kept:
        # `simple` means the dictionary treats the headword as a base form;
        # `derived` gives us the base in morphology.root. Both yield a root.
        root_src = (c["morphology"]["root"] if c["morphology"]["status"] == "derived"
                    else c["headword"])
        if not root_src:
            continue
        original = str(root_src)
        normalised = norm.normalize_token(original)
        if not normalised or not normalised.replace("-", "").isalpha():
            skipped_nonalpha += 1
            continue
        gloss = c["definition"] if isinstance(c["definition"], str) else "; ".join(
            x for x in c["definition"] if x)
        pos = c["part_of_speech"][0] if c["part_of_speech"] else ""
        page = c["source"].get("page")
        book = c["source"].get("dictionary", "").split(",")[0]
        new_roots.setdefault(normalised,
                             (normalised, gloss[:80].replace("\t", " "), pos,
                              f"{book} p{page} [{c['annotation_source']}/{c['confidence']}]"))
        if original.lower() != normalised:
            variants[original.lower()] = normalised
        for v in c["spelling_variants"]:
            vn = norm.normalize_token(v)
            if vn and vn != normalised and vn.isalpha():
                variants[vn] = normalised

    lic = inv["licensed"]

    # ---- demote derived lemmas out of the root inventory -----------------
    # Dictionaries list derived lemmas as headwords (masanting, kapampangan,
    # sumulat). Figure 7 checks "is this a root?" BEFORE trying any affix rule,
    # so any such headword left in roots.tsv is returned UNSEGMENTED — the
    # tokenizer then learns nothing about its structure. Same evidence standard
    # as everywhere else: a licensed affix, and a remainder that is itself a
    # headword.
    demoted: dict[str, str] = {}
    if not a.keep_analysable_roots:
        pool = set(new_roots) | set(existing_roots)
        n_pre_lic = {norm.normalize_token(x): c for x, c in lic["prefix"].items()}
        n_suf_lic = {norm.normalize_token(x): c for x, c in lic["suffix"].items()}
        n_cir_lic = {tuple(norm.normalize_token(y) for y in x.split("-...-")): c
                     for x, c in lic["circumfix"].items()}
        n_inf_lic = {norm.normalize_token(x): c for x, c in lic["infix"].items()}
        for w in sorted(new_roots):
            if len(w) < 5:
                continue
            hit = None
            for aff in sorted(n_pre_lic, key=len, reverse=True):
                if w.startswith(aff) and w[len(aff):] in pool and len(w[len(aff):]) >= 3:
                    hit = f"{aff}- + {w[len(aff):]}"; break
            if hit is None:
                for (l_, r_) in sorted(n_cir_lic, key=lambda t: -(len(t[0]) + len(t[1]))):
                    core = w[len(l_): len(w) - len(r_)]
                    if w.startswith(l_) and w.endswith(r_) and core in pool and len(core) >= 3:
                        hit = f"{l_}- + {core} + -{r_}"; break
            if hit is None:
                for aff in sorted(n_suf_lic, key=len, reverse=True):
                    if w.endswith(aff) and w[: len(w) - len(aff)] in pool \
                            and len(w) - len(aff) >= 3:
                        hit = f"{w[: len(w) - len(aff)]} + -{aff}"; break
            if hit is None:
                for aff in sorted(n_inf_lic, key=lambda x: -n_inf_lic[x]):
                    if w[1: 1 + len(aff)] == aff:
                        cand = w[:1] + w[1 + len(aff):]
                        if cand in pool and len(cand) >= 3:
                            hit = f"{w[0]} + -{aff}- + {cand[1:]}"; break
            if hit:
                demoted[w] = hit
        for w in demoted:
            new_roots.pop(w, None)

    merged = dict(existing_roots)
    added = 0
    for k, row in sorted(new_roots.items()):
        if k not in merged:
            merged[k] = {"root": row[0], "gloss_fil": row[1], "pos": row[2], "source": row[3]}
            added += 1
    for r in func_rows:
        if r.get("root") and r["root"] not in merged:
            merged[r["root"]] = {"root": r["root"], "gloss_fil": r.get("gloss_fil", ""),
                                 "pos": r.get("pos", ""), "source": r.get("source", "SEED-FUNC")}

    # ------------------------------------------------------------- affixes
    pre_rows, inf_rows, suf_rows, cir_rows = [], [], [], []
    for aff, n in sorted(lic["prefix"].items(), key=lambda kv: -kv[1]):
        pre_rows.append((norm.normalize_token(aff), "", "",
                         f"Samson explicit x{n} (orig '{aff}-')"))
    for aff, n in sorted(lic["infix"].items(), key=lambda kv: -kv[1]):
        inf_rows.append((norm.normalize_token(aff), "", f"Samson explicit x{n}"))
    for aff, n in sorted(lic["suffix"].items(), key=lambda kv: -kv[1]):
        suf_rows.append((norm.normalize_token(aff), "", "", f"Samson explicit x{n}"))
    for aff, n in sorted(lic["circumfix"].items(), key=lambda kv: -kv[1]):
        left, right = aff.split("-...-")
        cir_rows.append((norm.normalize_token(left), norm.normalize_token(right), "",
                         f"Samson explicit x{n}"))

    if a.dry_run:
        print("\n--dry-run: nothing written")
        print(f"  would add {added:,} roots (total {len(merged):,}), "
              f"{len(variants):,} variants, {len(pre_rows)} prefixes, "
              f"{len(inf_rows)} infixes, {len(suf_rows)} suffixes, "
              f"{len(cir_rows)} circumfixes")
        return 0

    if demoted:
        write_tsv(lex_dir / "derived_forms.tsv",
                  ["form", "segmentation", "root", "note", "source"],
                  ((w, seg_, seg_.split(" + ")[-1].lstrip("-"), "",
                    "demoted from roots.tsv: decomposes into a licensed affix "
                    "plus another headword") for w, seg_ in sorted(demoted.items())))
        print(f"demoted {len(demoted):,} analysable headwords out of roots.tsv "
              f"-> derived_forms.tsv")

    n_roots = write_tsv(lex_dir / "roots.tsv", ["root", "gloss_fil", "pos", "source"],
                        ((v["root"], v["gloss_fil"], v["pos"], v["source"])
                         for _, v in sorted(merged.items())))
    old_vars = {r["variant"]: r for r in read_tsv(lex_dir / "variants.tsv") if r.get("variant")}
    for v, c_ in variants.items():
        old_vars.setdefault(v, {"variant": v, "canonical": c_,
                                "note": "original dictionary spelling",
                                "source": "merged from candidate lexicon"})
    n_vars = write_tsv(lex_dir / "variants.tsv",
                       ["variant", "canonical", "note", "source"],
                       ((r["variant"], r["canonical"], r.get("note", ""), r.get("source", ""))
                        for _, r in sorted(old_vars.items())
                        if r["canonical"] in merged))
    n_pre = write_tsv(lex_dir / "prefixes.tsv", ["prefix", "gloss", "allomorphs", "source"], pre_rows)
    n_inf = write_tsv(lex_dir / "infixes.tsv", ["infix", "gloss", "source"], inf_rows)
    n_suf = write_tsv(lex_dir / "suffixes.tsv", ["suffix", "gloss", "allomorphs", "source"], suf_rows)
    n_cir = write_tsv(lex_dir / "circumfixes.tsv", ["prefix", "suffix", "gloss", "source"], cir_rows)

    print(f"\nroots        {len(existing_roots):>6,} -> {n_roots:>6,}   (+{added:,})")
    print(f"variants     {len(old_vars) - len(variants):>6,} -> {n_vars:>6,}")
    print(f"prefixes     {n_pre:>6}   infixes {n_inf}   suffixes {n_suf}   circumfixes {n_cir}")
    if skipped_nonalpha:
        print(f"skipped {skipped_nonalpha:,} roots that were not alphabetic after normalisation")

    if corpus:
        after = coverage(lex_dir, norm, seg_cfg, corpus)
        print(f"\nsegmenter coverage on the training corpus")
        print(f"  word types  {before[0]:>6.1%}  ->  {after[0]:>6.1%}")
        print(f"  word tokens {before[1]:>6.1%}  ->  {after[1]:>6.1%}")

    (lex_dir / "MERGE_PROVENANCE.json").write_text(json.dumps({
        "included_annotation_sources": a.include,
        "min_confidence": a.min_confidence,
        "candidates_total": len(cands),
        "candidates_admitted": len(kept),
        "roots_before": len(existing_roots), "roots_after": n_roots,
        "coverage_types_before": before[0], "coverage_types_after": after[0] if corpus else None,
        "coverage_tokens_before": before[1], "coverage_tokens_after": after[1] if corpus else None,
        "warning": ("Every admitted entry is still validation_status=unvalidated in "
                    "the candidate lexicon. Human validation is outstanding."),
    }, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {lex_dir}/MERGE_PROVENANCE.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
