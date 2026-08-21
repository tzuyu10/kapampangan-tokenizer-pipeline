"""Stage 6 — decode the test set for both arms and run RQ2/RQ4.

    python scripts/06_translate_eval.py --arms baseline adapted control
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
import torch
from kapampangan_mt.config import load_config
from kapampangan_mt.metrics.translation import corpus_scores, sentence_scores
from kapampangan_mt.nllb.dataset import load_pairs
from kapampangan_mt.nllb.graft import GraftConfig, build_model, load_source_embeddings
from kapampangan_mt.nllb.translate import translate
from kapampangan_mt.stats import holm_bonferroni, paired_bootstrap_corpus, paired_report
from kapampangan_mt.tokenizer import KapampanganTokenizer


def decode_arm(arm, cfg, test_src, device):
    art = Path(cfg.get_path("paths.artifacts_dir"))
    src_tok = (KapampanganTokenizer.load(art / "tokenizer" / "morphbpe.json")
               if arm == "adapted" else None)
    gcfg = GraftConfig(arm=arm, model_name=cfg.get_path("nllb.model_name"),
                       init=cfg.get_path("nllb.init", "subword_average"),
                       tgt_lang=cfg.get_path("nllb.tgt_lang"),
                       seed=cfg.get_path("seed", 13))
    model, nllb_tok, _ = build_model(gcfg, src_tok, device=device)
    ckpt = art / "nmt" / arm / "src_embeddings.best.pt"
    if ckpt.exists():
        load_source_embeddings(model, str(ckpt), map_location=device)
        print(f"[{arm}] loaded {ckpt}")
    else:
        print(f"[{arm}] WARNING: no checkpoint, decoding with the initial embedding")
    if arm != "adapted":
        from kapampangan_mt.baselines import NLLBTokenizerAdapter
        src_tok = NLLBTokenizerAdapter(cfg.get_path("nllb.model_name"),
                                       cfg.get_path("nllb.baseline_src_lang"),
                                       hf_tokenizer=nllb_tok)
    d = cfg.get_path("decode", {})
    hyps = translate(model, src_tok, nllb_tok, test_src,
                     tgt_lang=cfg.get_path("nllb.tgt_lang"),
                     num_beams=d.get("num_beams", 5),
                     max_new_tokens=d.get("max_new_tokens", 128),
                     length_penalty=d.get("length_penalty", 1.0), device=device)
    del model
    torch.cuda.empty_cache()
    return hyps


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--arms", nargs="+", default=["baseline", "adapted"])
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    proc = Path(cfg.get_path("paths.processed_dir"))
    res = Path(cfg.get_path("paths.artifacts_dir")) / "results"
    res.mkdir(parents=True, exist_ok=True)
    pairs = load_pairs(proc / "test.tsv")
    src = [p.src for p in pairs]; refs = [p.tgt for p in pairs]

    hyps, table3 = {}, {}
    for arm in a.arms:
        hyps[arm] = decode_arm(arm, cfg, src, a.device)
        table3[arm] = corpus_scores(hyps[arm], refs)
        (res / f"hyp_{arm}.txt").write_text("\n".join(hyps[arm]), encoding="utf-8")
        print(f"[{arm}] BLEU={table3[arm]['bleu']:.2f} chrF++={table3[arm]['chrf++']:.2f}")

    table5 = []
    if "adapted" in hyps:
        for baseline in [x for x in ("baseline", "control") if x in hyps]:
            sa = sentence_scores(hyps["adapted"], refs)
            sb = sentence_scores(hyps[baseline], refs)
            reports = holm_bonferroni(
                [paired_report(sa["bleu"], sb["bleu"], f"sentence BLEU (vs {baseline})"),
                 paired_report(sa["chrf++"], sb["chrf++"], f"sentence chrF++ (vs {baseline})")],
                cfg.get_path("stats.alpha", 0.05))
            n = cfg.get_path("stats.bootstrap_resamples", 1000)
            boots = [paired_bootstrap_corpus(hyps["adapted"], hyps[baseline], refs, m, n)
                     for m in ("bleu", "chrf")]
            table5.append({"baseline": baseline, "paired_tests": reports,
                           "corpus_paired_bootstrap": boots})
            for r in reports:
                print(f"{r['metric']}: {r['mean_proposed']:.2f} vs {r['mean_baseline']:.2f}, "
                      f"p={r['p_value']:.4g}, dz={r['cohens_dz']:.3f} -> {r['decision_holm']}")
            for b in boots:
                print(f"corpus {b['metric']} bootstrap: diff={b['observed_diff']:.2f} "
                      f"95%CI[{b['ci_low']:.2f},{b['ci_high']:.2f}] p={b['p_value']:.4g}")

    (res / "translation_level.json").write_text(json.dumps(
        {"table3": table3, "table5": table5, "n_test": len(refs)}, indent=2))
    print(f"saved -> {res / 'translation_level.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
