"""Stage 0 — clean the raw parallel corpus and produce the 80/10/10 split.

    python scripts/00_prepare_data.py

Input : data/raw/parallel.tsv   (columns: pam, fil, domain, source)
Output: data/processed/{train,val,test}.tsv, split_report.json
"""
from __future__ import annotations

import argparse, csv, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.data.clean import CleanConfig, clean_pairs
from kapampangan_mt.data.split import stratified_split
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig


def write_tsv(path: Path, rows: list[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["pam", "fil"])
        w.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    raw = Path(cfg.get_path("paths.raw_parallel"))
    if not raw.exists():
        print(f"ERROR: {raw} not found. See docs/DATA_REQUIREMENTS.md")
        return 1

    pairs, domains = [], []
    with raw.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            pairs.append(((r.get("pam") or "").strip(), (r.get("fil") or "").strip()))
            domains.append((r.get("domain") or "unknown").strip())
    print(f"read {len(pairs)} raw pairs from {raw}")

    kept, report = clean_pairs(pairs, CleanConfig(**cfg.get_path("clean", {})))
    kept_domains = [domains[i] for i in report.kept_indices]
    print("cleaning:", json.dumps(report.as_dict(), indent=2))

    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    seg = MorphologicalSegmenter(lex, config=SegmenterConfig(**cfg.get_path("segmenter", {})))

    split = stratified_split(
        kept, segmenter=seg, domains=kept_domains,
        ratios=tuple(cfg.get_path("split.ratios")), seed=cfg.get_path("seed", 13),
    )
    out = Path(cfg.get_path("paths.processed_dir"))
    for name in ("train", "val", "test"):
        write_tsv(out / f"{name}.tsv", split[name])
        print(f"{name}: {len(split[name])} pairs -> {out / f'{name}.tsv'}")

    (out / "split_report.json").write_text(json.dumps(
        {"clean": report.as_dict(),
         "sizes": {k: len(split[k]) for k in ("train", "val", "test")},
         "per_stratum": split["per_stratum"], "seed": split["seed"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
