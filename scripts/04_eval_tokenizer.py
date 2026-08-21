"""Stage 4 — tokenizer-level evaluation (Research Questions 1 and 3).

    python scripts/04_eval_tokenizer.py
    python scripts/04_eval_tokenizer.py --allow-auto-gold   # smoke test only

Produces artifacts/results/tokenizer_level.json which fills Tables 2 and 4.
Compares up to three tokenizers on the held-out test set:
    proposed   Morph-BPE
    native     NLLB-200 SentencePiece (the thesis' baseline)
    plain      unconstrained BPE, same corpus + vocab size (the missing control)
"""
from __future__ import annotations

import argparse, csv, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config
from kapampangan_mt.lexicon import Lexicon
from kapampangan_mt.normalize import Normalizer
from kapampangan_mt.metrics.boundary_f1 import boundary_f1_corpus, boundary_scores_per_word, load_gold
from kapampangan_mt.metrics.consistency_f1 import bootstrap_mcf1, morphological_consistency_f1
from kapampangan_mt.metrics.fertility import fertility_corpus, fertility_per_sentence
from kapampangan_mt.pretokenize import normalized_words
from kapampangan_mt.segmenter import MorphologicalSegmenter, SegmenterConfig
from kapampangan_mt.stats import holm_bonferroni, paired_report
from kapampangan_mt.tokenizer import KapampanganTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--allow-auto-gold", action="store_true")
    ap.add_argument("--no-nllb", action="store_true", help="skip the NLLB baseline")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    proc = Path(cfg.get_path("paths.processed_dir"))
    art = Path(cfg.get_path("paths.artifacts_dir"))
    res = art / "results"; res.mkdir(parents=True, exist_ok=True)

    with (proc / "test.tsv").open(encoding="utf-8", newline="") as fh:
        test_src = [r["pam"] for r in csv.DictReader(fh, delimiter="\t")]
    print(f"test sentences: {len(test_src)}")

    toks: dict[str, object] = {}
    p = art / "tokenizer" / "morphbpe.json"
    if not p.exists():
        print("ERROR: run 03_train_tokenizer.py first"); return 1
    toks["proposed"] = KapampanganTokenizer.load(p)
    pp = art / "tokenizer" / "plainbpe.json"
    if pp.exists():
        toks["plain"] = KapampanganTokenizer.load(pp)
    if not a.no_nllb:
        from kapampangan_mt.baselines import NLLBTokenizerAdapter
        toks["native"] = NLLBTokenizerAdapter(
            cfg.get_path("nllb.model_name"), cfg.get_path("nllb.baseline_src_lang"))

    # ---------------- gold morphemes -----------------
    gold_path = Path(cfg.get_path("paths.gold_morphemes"))
    gold = load_gold(gold_path, allow_auto=a.allow_auto_gold) if gold_path.exists() else []
    if not gold:
        print(f"WARNING: {gold_path} missing — MBF1 will be skipped "
              "(run 02_build_gold_template.py and annotate it).")

    lex = Lexicon.load(cfg.get_path("paths.lexicon_dir"))
    norm = Normalizer.from_rules_file(
        Path(cfg.get_path("paths.lexicon_dir")) / "orthography_rules.tsv",
        lowercase=True, strip_accents=True)
    seg = MorphologicalSegmenter(lex, normalizer=norm, config=SegmenterConfig(**cfg.get_path("segmenter", {})))
    test_words = sorted({w for s in test_src for w in normalized_words(s)})
    gold_roots = {}
    for w in test_words:
        s = seg.segment(w)
        if s.analyzed:
            gold_roots[w] = [m.label for m in s.morphs
                             if m.kind in ("root", "unknown")] or [w]

    mcfg = cfg.get_path("metrics", {})
    mkw = dict(min_token_len=mcfg.get("mcf1_min_token_len", 2),
               content_morphemes_only=mcfg.get("mcf1_content_morphemes_only", True),
               max_types=mcfg.get("mcf1_max_types", 5000))

    # ---------------- Table 2 -----------------
    table2, per_sent_fr, per_word_f1 = {}, {}, {}
    for name, tk in toks.items():
        row = fertility_corpus(tk, test_src)
        per_sent_fr[name] = fertility_per_sentence(tk, test_src)
        if gold:
            row.update(boundary_f1_corpus(tk, gold))
            per_word_f1[name] = [x["f1"] for x in boundary_scores_per_word(tk, gold)]
        row.update(morphological_consistency_f1(tk, test_words, gold_roots, **mkw))
        row["vocab_size"] = tk.vocab_size
        table2[name] = row
        print(f"\n[{name}] " + json.dumps(
            {k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()},
            indent=2))

    # ---------------- Table 4 -----------------
    table4 = []
    for baseline in ("native", "plain"):
        if baseline not in toks:
            continue
        reports = [paired_report(per_sent_fr["proposed"], per_sent_fr[baseline],
                                 f"Fertility Rate (vs {baseline})",
                                 higher_is_better=False)]
        if gold:
            reports.append(paired_report(per_word_f1["proposed"], per_word_f1[baseline],
                                         f"Morpheme Boundary F1 (vs {baseline})"))
        boot = bootstrap_mcf1(
            toks["proposed"], toks[baseline], test_words, gold_roots,
            n_resamples=cfg.get_path("stats.bootstrap_resamples", 1000),
            max_types=mcfg.get("mcf1_bootstrap_types", 1200),
            min_token_len=mkw["min_token_len"])
        reports = holm_bonferroni(reports, cfg.get_path("stats.alpha", 0.05))
        table4.append({"baseline": baseline, "paired_tests": reports,
                       "mcf1_paired_bootstrap": boot})
        for r in reports:
            print(f"\n{r['metric']}: mean {r['mean_proposed']:.4f} vs "
                  f"{r['mean_baseline']:.4f}, {r['test_used']}, p={r['p_value']:.4g}, "
                  f"dz={r['cohens_dz']:.3f} -> {r['decision_holm']}")
        print(f"MCF1 paired bootstrap vs {baseline}: diff={boot['mean_diff']:.4f} "
              f"95%CI[{boot['ci_low']:.4f},{boot['ci_high']:.4f}] p={boot['p_value']:.4g}")

    (res / "tokenizer_level.json").write_text(json.dumps(
        {"table2": table2, "table4": table4,
         "gold_rows": len(gold), "n_test_sentences": len(test_src),
         "n_test_word_types": len(test_words)}, indent=2))
    print(f"\nsaved -> {res / 'tokenizer_level.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
