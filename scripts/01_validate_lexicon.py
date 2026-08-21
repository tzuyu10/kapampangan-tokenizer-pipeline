"""Stage 1 — validate the Lexicon Dictionary and report segmenter coverage.

    python scripts/01_validate_lexicon.py
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.pretokenize import normalized_words
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--strict", action="store_true", help="fail on warnings")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    print("Lexicon Dictionary:", json.dumps(lex.stats(), indent=2))
    warnings = lex.validate()
    for w in warnings:
        print("  WARNING:", w)

    norm = Normalizer.from_rules_file(
        Path(cfg.get_path("paths.lexicon_dir")) / "orthography_rules.tsv",
        lowercase=True, strip_accents=True)
    seg = MorphologicalSegmenter(
        lex, normalizer=norm, config=SegmenterConfig(**cfg.get_path("segmenter", {}))
    )
    train_path = Path(cfg.get_path("paths.processed_dir")) / "train.tsv"
    if train_path.exists():
        import csv
        with train_path.open(encoding="utf-8", newline="") as fh:
            words = [w for r in csv.DictReader(fh, delimiter="\t")
                     for w in normalized_words(r["pam"])]
        cov = seg.coverage(words)
        types = sorted(set(words))
        rules = {}
        for t in types:
            rules[seg.segment(t).rule] = rules.get(seg.segment(t).rule, 0) + 1
        print(f"\nSegmenter type coverage on train: {cov:.1%} "
              f"({len(types)} word types)")
        print("Rule usage:", json.dumps(dict(sorted(rules.items(),
              key=lambda kv: -kv[1])), indent=2))
        print("\nUnanalysed sample:",
              [t for t in types if not seg.segment(t).analyzed][:25])
        if cov < 0.5:
            warnings.append(f"segmenter analyses only {cov:.1%} of training word types")
    else:
        print(f"\n(no {train_path} yet — run 00_prepare_data.py first)")

    if warnings and a.strict:
        print(f"\nFAILED: {len(warnings)} warning(s) with --strict")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
