"""Stage 3 — train the proposed Morph-BPE tokenizer (and the matched control).

    python scripts/03_train_tokenizer.py                # proposed, with vocab search
    python scripts/03_train_tokenizer.py --plain-bpe    # unconstrained control
    python scripts/03_train_tokenizer.py --vocab-size 8000   # skip the search

Outputs (artifacts/tokenizer/):
    morphbpe.json / plainbpe.json      runtime tokenizer
    vocab_search.json                  the selection table for Chapter 4
    segmentation_train.jsonl           training-time analyses (audit trail)
"""
from __future__ import annotations

import argparse, csv, json, sys
from collections import Counter
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.morph_bpe import MorphBPEConfig, MorphBPETrainer
from kapampangan_mt.pretokenize import WORD_BOUNDARY, pre_tokenize
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig
from kapampangan_mt.tokenizer import BYTE_TOKENS, RESERVED, KapampanganTokenizer
from kapampangan_mt.vocab_search import search_vocab_size


def load_split(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as fh:
        return [r["pam"] for r in csv.DictReader(fh, delimiter="\t")]


def build_training_units(sentences, segmenter):
    """marked_word -> (frequency, morpheme surfaces)."""
    freqs: Counter[str] = Counter()
    segs: dict[str, list[str]] = {}
    for s in sentences:
        for pt in pre_tokenize(segmenter.norm.normalize_text(s)):
            marked = pt.marked
            freqs[marked] += 1
            if marked not in segs:
                if pt.kind == "word":
                    segs[marked] = segmenter.segment(pt.surface).surfaces
                else:
                    segs[marked] = [pt.surface]
    return freqs, segs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--plain-bpe", action="store_true",
                    help="train the unconstrained matched control tokenizer")
    ap.add_argument("--vocab-size", type=int, default=None)
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    proc = Path(cfg.get_path("paths.processed_dir"))
    art = Path(cfg.get_path("paths.artifacts_dir")) / "tokenizer"
    art.mkdir(parents=True, exist_ok=True)

    train_s, val_s = load_split(proc / "train.tsv"), load_split(proc / "val.tsv")
    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    norm = Normalizer.from_rules_file(
        Path(cfg.get_path("paths.lexicon_dir")) / "orthography_rules.tsv",
        lowercase=True, strip_accents=True)
    seg = MorphologicalSegmenter(lex, normalizer=norm, config=SegmenterConfig(**cfg.get_path("segmenter", {})))

    freqs, segs = build_training_units(train_s, seg)
    print(f"{len(freqs)} word types / {sum(freqs.values())} tokens in train")

    with (art / "segmentation_train.jsonl").open("w", encoding="utf-8") as fh:
        for w, parts in sorted(segs.items()):
            fh.write(json.dumps({"word": w, "morphs": parts}, ensure_ascii=False) + "\n")

    constrain = not a.plain_bpe
    reserved = len(RESERVED) + len(BYTE_TOKENS)
    tcfg = cfg.get_path("tokenizer", {})

    if a.vocab_size:
        model = MorphBPETrainer(MorphBPEConfig(
            vocab_size=a.vocab_size,
            min_pair_frequency=tcfg.get("min_pair_frequency", 2),
            constrain_to_morpheme_boundaries=constrain,
        )).train(segs, freqs, reserved=reserved)
        tok = KapampanganTokenizer.from_model(model, lowercase=tcfg.get("lowercase", True))
        chosen = a.vocab_size
        table = None
    else:
        # Validation gold for the search uses the RULE-BASED analysis on purpose:
        # this selects a hyper-parameter, it does not report a result. The
        # reported MBF1 in stage 4 uses the human gold file.
        val_gold = {}
        for s in val_s:
            for pt in pre_tokenize(seg.norm.normalize_text(s)):
                if pt.kind != "word" or pt.surface in val_gold:
                    continue
                analysis = seg.segment(pt.surface)
                if analysis.analyzed:
                    val_gold[pt.surface] = analysis.boundaries
        print(f"vocab-size search on {len(val_gold)} analysable validation word types")
        best, results = search_vocab_size(
            segs, freqs, val_gold, val_s,
            candidates=tcfg.get("candidates", [2000, 4000, 8000, 16000, 32000]),
            constrain=constrain,
            fertility_target=tcfg.get("fertility_target", 1.6),
            lam=tcfg.get("lambda_fertility", 0.5),
        )
        tok, chosen = best.tokenizer, best.vocab_size
        table = [{"vocab_size": r.vocab_size, "morph_distance": r.morph_distance,
                  "fertility": r.fertility, "objective": r.objective} for r in results]
        (art / ("vocab_search_plain.json" if a.plain_bpe else "vocab_search.json")
         ).write_text(json.dumps({"chosen": chosen, "table": table}, indent=2))

    name = "plainbpe.json" if a.plain_bpe else "morphbpe.json"
    tok.save(art / name)
    print(f"chosen vocab size = {chosen}; actual vocab = {tok.vocab_size}")
    print(f"saved -> {art / name}")
    print("sample:", tok.tokenize("Kinan ne ing pamangan king bale."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
