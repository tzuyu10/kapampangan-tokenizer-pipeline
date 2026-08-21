"""Stage 12 — the prioritised lexicon worklist.

    python scripts/12_lexicon_worklist.py --n 800

Ranks the word types the segmenter CANNOT analyse by corpus frequency, so an
hour of annotation buys the largest possible coverage gain. Writes
data/lexicon/WORKLIST_unanalysed.tsv with a suggested category for each row.

Coverage is the ceiling on Morpheme Boundary F1 for the proposed tokenizer, and
it is set by lexicon completeness, not by the algorithm — so this file is the
highest-value manual task in the project.
"""
from __future__ import annotations

import argparse, csv, re, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.pretokenize import words_only
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig

PRONOUN_HINT = re.compile(r"^(k|d|r|n|m|y|l)(a|e|i|o|u)")
SPANISH_HINT = re.compile(r"(qu|c[aou]|ll|gui|gue|ñ)")


def guess_category(word: str, count: int, caps_ratio: float) -> str:
    if caps_ratio > 0.85:
        return "proper_noun"
    if SPANISH_HINT.search(word):
        return "spanish_era_spelling"
    if len(word) <= 3 and count >= 50:
        return "particle_or_pronoun"
    if len(word) <= 6 and count >= 100 and PRONOUN_HINT.match(word):
        return "pronoun_or_clitic_cluster"
    if count == 1:
        return "hapax_check_ocr"
    return "content_word"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--n", type=int, default=800)
    ap.add_argument("--mono", default="data/raw/mono_pam.tsv")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    lex_dir = Path(cfg.get_path("paths.lexicon_dir"))
    norm = Normalizer.from_rules_file(lex_dir / "orthography_rules.tsv",
                                      lowercase=True, strip_accents=True)
    lex = Lexicon.load(lex_dir)
    seg = MorphologicalSegmenter(lex, normalizer=norm,
                                 config=SegmenterConfig(**cfg.get_path("segmenter", {})))

    src = Path(a.mono)
    with src.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    freq: Counter[str] = Counter()
    caps: Counter[str] = Counter()
    for r in rows:
        raw = r["pam"]
        for w in words_only(norm.normalize_text(raw)):
            freq[w] += 1
        for w in re.findall(r"\b[A-Z][a-zA-Z'’-]+", raw):
            caps[norm.normalize_token(w)] += 1

    total = sum(freq.values())
    missing = [(w, c) for w, c in freq.items() if not seg.segment(w).analyzed]
    missing.sort(key=lambda x: -x[1])
    covered_now = 1 - sum(c for _, c in missing) / total

    out = lex_dir / "WORKLIST_unanalysed.tsv"
    cum = 0
    with out.open("w", encoding="utf-8", newline="") as fh:
        cw = csv.writer(fh, delimiter="\t", lineterminator="\n")
        cw.writerow(["rank", "word", "corpus_count", "cumulative_token_gain_pct",
                     "suggested_category", "root", "segmentation", "gloss_fil",
                     "decision", "annotator"])
        for i, (w, c) in enumerate(missing[: a.n], 1):
            cum += c
            cw.writerow([i, w, c, f"{100*cum/total:.2f}",
                         guess_category(w, c, caps.get(w, 0) / max(c, 1)),
                         "", "", "", "", ""])

    print(f"corpus: {total:,} tokens | {len(freq):,} types")
    print(f"current token coverage : {covered_now:.1%}")
    print(f"unanalysed types       : {len(missing):,} ({sum(c for _,c in missing):,} tokens)")
    print(f"\nwrote top {min(a.n, len(missing)):,} -> {out}")
    print(f"  completing all {min(a.n, len(missing)):,} rows lifts token coverage to "
          f"~{covered_now + cum/total:.1%}")
    print("\nFill in `root` (and `segmentation` where the word is complex), then move")
    print("the rows into roots.tsv / clitics.tsv / variants.tsv and re-run stage 01.")
    cats = Counter(guess_category(w, c, caps.get(w, 0) / max(c, 1))
                   for w, c in missing[: a.n])
    print("\nsuggested categories in this batch:", dict(cats.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
