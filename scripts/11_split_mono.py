"""Stage 11 — 80/10/10 split of the MONOLINGUAL Kapampangan corpus.

    python scripts/11_split_mono.py

The tokenizer only needs Kapampangan text; the Filipino side is required later,
for the translation arms. This script therefore writes train/val/test.tsv with
a `pam` column and an EMPTY `fil` column, so stages 03 and 04 run unchanged
while stages 05 and 06 will correctly refuse to run until parallel data exists.

Stratified by (sentence-length band x morphological-complexity band x domain),
exactly as the proposal requires (p. 35).
"""
from __future__ import annotations

import argparse, csv, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.data.split import stratified_split
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--mono", default="data/raw/mono_pam.tsv")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    src = Path(a.mono)
    if not src.exists():
        print(f"ERROR: {src} not found — run 10_ingest_dataset.py first")
        return 1
    with src.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    pairs = [(r["pam"], "") for r in rows]
    domains = [r.get("domain") or "unknown" for r in rows]
    print(f"read {len(pairs):,} monolingual lines")

    norm = Normalizer.from_rules_file(
        Path(cfg.get_path("paths.lexicon_dir")) / "orthography_rules.tsv",
        lowercase=True, strip_accents=True)
    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    seg = MorphologicalSegmenter(lex, normalizer=norm,
                                 config=SegmenterConfig(**cfg.get_path("segmenter", {})))

    split = stratified_split(pairs, segmenter=seg, domains=domains,
                             ratios=tuple(cfg.get_path("split.ratios")),
                             seed=cfg.get_path("seed", 13))
    out = Path(cfg.get_path("paths.processed_dir")); out.mkdir(parents=True, exist_ok=True)
    for name in ("train", "val", "test"):
        p = out / f"{name}.tsv"
        with p.open("w", encoding="utf-8", newline="") as fh:
            wcsv = csv.writer(fh, delimiter="\t", lineterminator="\n")
            wcsv.writerow(["pam", "fil"])
            wcsv.writerows(split[name])
        print(f"  {name}: {len(split[name]):,} lines -> {p}")
    (out / "split_report.json").write_text(json.dumps(
        {"mode": "monolingual", "fil_side": "EMPTY — translation arms blocked",
         "sizes": {k: len(split[k]) for k in ("train", "val", "test")},
         "per_stratum": split["per_stratum"], "seed": split["seed"]}, indent=2))
    print("\nNOTE: the `fil` column is empty. Stages 03/04 (tokenizer) will run.")
    print("      Stages 05/06 (translation) need real Filipino references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
