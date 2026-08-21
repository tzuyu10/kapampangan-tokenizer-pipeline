"""Stage 7 — render Tables 2-5 as Markdown, ready to paste into Chapter 4.

    python scripts/07_report.py
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
from kapampangan_mt.config import load_config

F = lambda v, n=4: ("—" if v is None else f"{v:.{n}f}" if isinstance(v, float) else str(v))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)
    res = Path(cfg.get_path("paths.artifacts_dir")) / "results"
    out = [f"# Results\n"]

    tp = res / "tokenizer_level.json"
    if tp.exists():
        d = json.loads(tp.read_text())
        cols = list(d["table2"])
        out += ["## Table 2 — Tokenizer-Level Performance\n",
                "| Metric | " + " | ".join(cols) + " |",
                "|---|" + "---|" * len(cols)]
        for key, label in [("vocab_size", "Vocabulary size"),
                           ("fertility_corpus", "Fertility Rate (corpus)"),
                           ("fertility_sentence_mean", "Fertility Rate (sentence mean)"),
                           ("mbf1_micro", "Morpheme Boundary F1"),
                           ("mcf1", "Morphological Consistency F1")]:
            out.append(f"| {label} | " +
                       " | ".join(F(d["table2"][c].get(key)) for c in cols) + " |")
        out.append("")
        out.append("## Table 4 — Statistical Test Results (Tokenizer-Level)\n")
        out.append("| Metric | Mean (Proposed) | Mean (Baseline) | Test | p | Cohen's dz | Decision (Holm) |")
        out.append("|---|---|---|---|---|---|---|")
        for blk in d["table4"]:
            for r in blk["paired_tests"]:
                out.append(f"| {r['metric']} | {F(r['mean_proposed'])} | "
                           f"{F(r['mean_baseline'])} | {r['test_used']} | "
                           f"{r['p_value']:.4g} | {F(r['cohens_dz'],3)} | {r['decision_holm']} |")
            b = blk["mcf1_paired_bootstrap"]
            out.append(f"| Morphological Consistency F1 (vs {blk['baseline']}) | — | — | "
                       f"paired bootstrap | {b['p_value']:.4g} | — | "
                       f"{'reject H0' if b['p_value'] < 0.05 else 'fail to reject H0'} |")
        out.append("")

    lp = res / "translation_level.json"
    if lp.exists():
        d = json.loads(lp.read_text())
        arms = list(d["table3"])
        out += ["## Table 3 — Translation-Level Performance\n",
                "| Metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
        for key, label in [("bleu", "BLEU"), ("chrf++", "chrF++")]:
            out.append(f"| {label} | " + " | ".join(F(d['table3'][x][key], 2) for x in arms) + " |")
        out += ["", "## Table 5 — Statistical Test Results (Translation-Level)\n",
                "| Metric | Mean (Adapted) | Mean (Baseline) | Test | p | Cohen's dz | Decision (Holm) |",
                "|---|---|---|---|---|---|---|"]
        for blk in d["table5"]:
            for r in blk["paired_tests"]:
                out.append(f"| {r['metric']} | {F(r['mean_proposed'],2)} | "
                           f"{F(r['mean_baseline'],2)} | {r['test_used']} | "
                           f"{r['p_value']:.4g} | {F(r['cohens_dz'],3)} | {r['decision_holm']} |")
            for b in blk["corpus_paired_bootstrap"]:
                out.append(f"| corpus {b['metric']} (vs {blk['baseline']}) | "
                           f"{F(b['score_proposed'],2)} | {F(b['score_baseline'],2)} | "
                           f"paired bootstrap | {b['p_value']:.4g} | — | {b['decision']} |")

    text = "\n".join(out) + "\n"
    (res / "REPORT.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"saved -> {res / 'REPORT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
