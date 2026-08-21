"""Stage 2 — generate the human-annotation template for Morpheme Boundary F1.

    python scripts/02_build_gold_template.py --n 1500

Writes data/gold/morpheme_gold.TEMPLATE.tsv with one row per sampled word
type, pre-filled with the rule-based analysis as a SUGGESTION only.  The
annotator must review every row and set provenance=human.

Why this script exists: MBF1 needs gold boundaries and the proposal never says
where they come from.  Scoring against the segmenter's own output is circular
(Issue M-2), so the loader in metrics/boundary_f1.py refuses provenance=auto.

Sampling is stratified by frequency band so the gold set is not all high
frequency function words, and it draws from train+val+test word types with the
test-set share marked, so you can report MBF1 on unseen types separately.
"""
from __future__ import annotations

import argparse, csv, random, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.pretokenize import normalized_words
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig


def read_words(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return [w for r in csv.DictReader(fh, delimiter="\t") for w in normalized_words(r["pam"])]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--n", type=int, default=1500)
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)
    rng = random.Random(cfg.get_path("seed", 13))

    proc = Path(cfg.get_path("paths.processed_dir"))
    train = Counter(read_words(proc / "train.tsv"))
    test = Counter(read_words(proc / "test.tsv"))
    allw = train + Counter(read_words(proc / "val.tsv")) + test
    if not allw:
        print("ERROR: run 00_prepare_data.py first"); return 1

    bands = {"high": [], "mid": [], "low": [], "hapax": []}
    for w, c in allw.items():
        bands["hapax" if c == 1 else "low" if c < 5 else "mid" if c < 50 else "high"].append(w)
    quota = {"high": 0.15, "mid": 0.30, "low": 0.30, "hapax": 0.25}

    chosen: list[str] = []
    for band, share in quota.items():
        pool = sorted(bands[band]); rng.shuffle(pool)
        chosen += pool[: int(a.n * share)]
    chosen = sorted(set(chosen))

    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    norm = Normalizer.from_rules_file(
        Path(cfg.get_path("paths.lexicon_dir")) / "orthography_rules.tsv",
        lowercase=True, strip_accents=True)
    seg = MorphologicalSegmenter(lex, normalizer=norm, config=SegmenterConfig(**cfg.get_path("segmenter", {})))

    out = Path(cfg.get_path("paths.gold_morphemes")).with_name("morpheme_gold.TEMPLATE.tsv")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["word", "segmentation", "suggested", "rule", "count",
                    "in_test_only", "annotator", "provenance", "notes"])
        for word in chosen:
            s = seg.segment(word)
            sug = "|".join(s.surfaces)
            w.writerow([word, sug, sug, s.rule, allw[word],
                        int(word in test and word not in train), "", "auto", ""])
    print(f"wrote {len(chosen)} rows -> {out}")
    print("NEXT: two annotators review independently, report Cohen's kappa on "
          "boundary agreement, then save as data/gold/morpheme_gold.tsv with "
          "provenance=human.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
