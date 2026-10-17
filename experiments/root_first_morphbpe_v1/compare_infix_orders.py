"""Compare separately trained infix orders on the frozen exploratory DEV set."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from compare_priority_orders import boundary_f1, load_result


def paired_bootstrap(left, right):
    assert [(r["surface"], r["reference"]) for r in left] == [
        (r["surface"], r["reference"]) for r in right
    ]
    rng = random.Random(20261010)
    deltas = []
    for _ in range(5000):
        indices = [rng.randrange(len(left)) for _ in left]
        deltas.append(boundary_f1(left, indices) - boundary_f1(right, indices))
    deltas.sort()
    return {
        "resamples": 5000, "seed": 20261010,
        "observed_f1_difference": boundary_f1(left, list(range(len(left))))
        - boundary_f1(right, list(range(len(right)))),
        "percentile95": [deltas[124], deltas[4874]],
        "scope": "exploratory type bootstrap; ignores root-family dependence, label uncertainty and prior DEV-driven choices",
    }


def compare(infix_dir: Path, full_dir: Path, output_dir: Path):
    infix = load_result(infix_dir)
    full = load_result(full_dir)
    assert infix["inputs"] == full["inputs"]
    assert infix["annotation_summary"] == full["annotation_summary"]
    assert infix["config"]["priority_order"] == ["infix", "weighted"]
    assert full["config"]["priority_order"] == ["infix", "root", "affix", "weighted"]
    assert infix["config"]["root_token_budget"] == infix["config"]["affix_token_budget"] == 0
    assert full["config"]["root_token_budget"] == 2244
    assert full["config"]["affix_token_budget"] == 256
    for result in (infix, full):
        assert result["config"]["infix_token_budget"] == 32
        assert result["config"]["crossing_penalty"] == 32
        assert result["vocabulary_size"] == result["config"]["vocabulary_budget"] == 6080
        assert result["initial_vocabulary"] == 1592
        assert result["merge_count"] == 4488
        assert result["installed_inventory_unchanged"]
        assert not result["held_out_test_used"]
        assert not result["translation_training_or_quality_evaluation"]
        assert result["annotation_summary"]["infixes_have_separate_training_role"]
        assert sum(p["new_vocabulary_tokens"] for p in result["training_report"]["phase_statistics"].values()) == 4488
        assert any(t["phase"] != "infix" and t["reason"] == "no_supported_pair"
                   for t in result["training_report"]["phase_transitions"])
    for key in ("current32", "um_first32"):
        assert infix["evaluations"][key] == full["evaluations"][key]
        assert infix["validation"][key] == full["validation"][key]

    candidates = [
        ("Current Morph-BPE", infix, "current32"),
        ("Previous um seed", infix, "um_first32"),
        ("Infix then weighted", infix, "infix_only32"),
        ("Infix then root then other affix", full, "infix_root_affix32"),
    ]
    scores = {}
    rows = {}
    probes = {}
    for label, result, key in candidates:
        evaluation = result["evaluations"][key]
        assert evaluation["dev_rows"] == 272
        counts = evaluation["dev_counts"]
        metrics = evaluation["dev_metrics"]
        assert abs(metrics["boundary_f1"] - 2 * counts["tp"] /
                   (2 * counts["tp"] + counts["fp"] + counts["fn"])) < 1e-12
        scores[label] = {
            **metrics, **counts,
            "um_isolated": evaluation["infixes"]["um"]["isolated"],
            "in_isolated": evaluation["infixes"]["in"]["isolated"],
            "validation": result["validation"][key],
            "roles": evaluation["role_diagnostics"]["counts"],
            "roles_by_length": evaluation["role_diagnostics"]["by_length"],
            "root_controls": result["root_controls"]["totals"][key],
        }
        rows[label] = evaluation["dev_predictions"]
        probes[label] = evaluation["probe_tokens"]
    baseline, previous, only, ordered = [label for label, _, _ in candidates]
    comparisons = [(only, baseline), (ordered, baseline), (ordered, only), (only, previous)]
    bootstrap = {f"{left} minus {right}": paired_bootstrap(rows[left], rows[right])
                 for left, right in comparisons}
    ranks = {}
    for label, directory, name in ((only, infix_dir, "infix-only"),
                                    (ordered, full_dir, "infix-root-affix")):
        doc = json.loads((directory / f"{name}-penalty32/tokenizer.json").read_text(encoding="utf-8"))
        assert doc["metadata"]["protected_boundary_merge_violations"] == 0
        assert not doc["metadata"]["lexicon_used_at_runtime"]
        wanted = {"in", "um", "an", "ma", "ku", "bu", "sin", "sum", "uma", "uman", "minum"}
        ranks[label] = {}
        for rule in doc["merges"]:
            if rule["result"] in wanted:
                ranks[label].setdefault(rule["result"], rule["rank"])
    gains, losses = [], []
    for a, b in zip(rows[only], rows[ordered], strict=True):
        assert a["surface"] == b["surface"]
        detail = {"surface": a["surface"], "reference": a["reference"],
                  "infix_weighted": a["pieces"], "infix_root_affix": b["pieces"]}
        if b["exact"] and not a["exact"]:
            gains.append(detail)
        elif a["exact"] and not b["exact"]:
            losses.append(detail)
    summary = {
        "inputs": infix["inputs"], "scores": scores, "probe_tokens": probes,
        "annotation_summary": infix["annotation_summary"],
        "configs": {"infix_only": infix["config"], "infix_root_affix": full["config"]},
        "phase_statistics": {"infix_only": infix["training_report"]["phase_statistics"],
                             "infix_root_affix": full["training_report"]["phase_statistics"]},
        "merge_ranks": ranks, "bootstrap": bootstrap,
        "root_other_affix_phase_exact_gains": gains, "root_other_affix_phase_exact_losses": losses,
        "best_observed_dev_f1": max(scores, key=lambda label: scores[label]["boundary_f1"]),
        "held_out_test_used": False, "translation_training_or_quality_evaluation": False,
        "installed_tokenizer_replaced": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Infix priority comparison", "",
        "Both new candidates were trained on the exact original prepared stream and lexicon with penalty32, vocabulary6080 and standard global inference. The current tokenizer and previous um-only seed were freshly evaluated. The previous seed was not retrained.", "",
        "New schedules: infix -> weighted, and infix -> root -> other_affix -> weighted. Both prioritize every supported internal infix pair; the analyzer supports in/um and observed casing. Infix cap32 is above actual usage. The full order retains the previously declared root cap2244 and other-affix cap256. The control has no root/other-affix priority phases. Only training role scheduling changes, without runtime morphology or surface overrides.", "",
        "| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 | DEV tokens/word | Validation tokens/word |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for label, score in scores.items():
        lines.append(f"| {label} | {100*score['boundary_f1']:.2f}% | {score['exact']} | {score['um_isolated']} | {score['in_isolated']} | {score['fertility']:.4f} | {score['validation']['word_fertility']:.6f} |")
    lines += ["", f"Highest observed DEV F1: {summary['best_observed_dev_f1']}.", "",
              "| Word | " + " | ".join(scores) + " |", "|---|" + "---|" * len(scores)]
    for word in ("kumain", "kuman", "sumulat", "sinulat", "bumasa", "suminulat", "lumapit", "tumula", "minum"):
        lines.append("| " + word + " | " + " | ".join(" + ".join(probes[label][word]) for label in scores) + " |")
    lines += ["", "| Tokenizer | Root isolated /97 | All affixes isolated /80 | Whole root controls /74 |",
              "|---|---:|---:|---:|"]
    for label, score in scores.items():
        lines.append(f"| {label} | {score['roles']['root']['isolated']} | {score['roles']['affix']['isolated']} | {score['root_controls']['kept_whole']} |")
    lines += ["", "Evaluation's all-affix diagnostic still includes infixes for comparable denominators. Only training annotations separate them. Role diagnostics cover72 analyzer/reference-aligned words; role labels and standalone root controls are provisional, not independent human gold.",
              "", "Actual phase usage:", "", "```json", json.dumps(summary["phase_statistics"], indent=2), "```",
              "", "Selected earliest global merge ranks (zero-based):", "", "```json", json.dumps(ranks, indent=2), "```",
              "", "Early infix formation cannot guarantee final isolation: later global merges can absorb formed infixes. Contiguous root fragments remain separate around an infix; BPE cannot skip it to reconstruct a single root token.",
              "", f"Adding root/other-affix phases gains {len(gains)} exact words and loses {len(losses)} relative to infix-only priority.",
              "", "Exploratory paired DEV bootstrap:", "", "```json", json.dumps(bootstrap, indent=2), "```",
              "", "DEV contains272 mixed silver/user-derived words,270 seen in training, and only five genuine um examples. Prior experiments informed this proposal. Intervals are exploratory and do not establish unseen-root or translation superiority. Validation3284 records has no gold morphology and measures length/coverage only. No final test text or translation model training/evaluation was used. Installed artifacts remain unchanged. Changed token identities require new source-embedding adaptation before translation deployment."]
    (output_dir / "comparison-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"scores": {label: {k: score[k] for k in ("boundary_f1", "exact", "um_isolated", "in_isolated")} for label, score in scores.items()}, "bootstrap": bootstrap}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--infix-dir", type=Path, required=True)
    parser.add_argument("--full-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    compare(args.infix_dir.resolve(), args.full_dir.resolve(), args.output_dir.resolve())
