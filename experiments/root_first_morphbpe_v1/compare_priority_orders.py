"""Compare fresh matched priority orders without selecting or installing a model."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def load_result(directory: Path) -> dict:
    return json.loads((directory / "comparison-result.json").read_text(encoding="utf-8"))


def boundary_f1(rows: list[dict], indices: list[int]) -> float:
    tp = sum(rows[i]["tp"] for i in indices)
    fp = sum(rows[i]["fp"] for i in indices)
    fn = sum(rows[i]["fn"] for i in indices)
    denominator = 2 * tp + fp + fn
    return 2 * tp / denominator if denominator else 0.0


def compare(root_dir: Path, affix_dir: Path, output_dir: Path, old_root_artifact: Path | None) -> None:
    root = load_result(root_dir)
    affix = load_result(affix_dir)
    assert root["inputs"] == affix["inputs"]
    for result in (root, affix):
        assert result["config"]["crossing_penalty"] == 32
        assert result["vocabulary_size"] == result["config"]["vocabulary_budget"] == 6080
        assert result["config"]["root_token_budget"] == 2244
        assert result["config"]["affix_token_budget"] == 256
        assert result["installed_inventory_unchanged"]
        assert not result["held_out_test_used"]
        assert sum(p["new_vocabulary_tokens"] for p in result["training_report"]["phase_statistics"].values()) == 4488
    assert root["config"]["priority_order"] == ["root", "affix", "weighted"]
    assert affix["config"]["priority_order"] == ["affix", "root", "weighted"]
    assert root["evaluations"]["current32"] == affix["evaluations"]["current32"]
    assert root["validation"]["current32"] == affix["validation"]["current32"]
    old_equivalence = None
    if old_root_artifact is not None:
        before = json.loads((old_root_artifact / "tokenizer.json").read_text(encoding="utf-8"))
        after = json.loads((root_dir / "root-first-penalty32/tokenizer.json").read_text(encoding="utf-8"))
        old_equivalence = {key: before[key] == after[key] for key in ("vocabulary", "merges")}
        assert all(old_equivalence.values())

    candidates = [
        ("Current32", root, "current32"),
        ("Root then affix", root, "root_first32"),
        ("Affix then root", affix, "affix_first32"),
    ]
    if "um_first32" in root["evaluations"]:
        candidates.append(("Previous um seed", root, "um_first32"))
    main_rows = root["evaluations"]["root_first32"]["dev_predictions"]
    affix_rows = affix["evaluations"]["affix_first32"]["dev_predictions"]
    assert len(main_rows) == len(affix_rows) == 272
    assert [(row["surface"], row["reference"]) for row in main_rows] == [
        (row["surface"], row["reference"]) for row in affix_rows
    ]
    rng = random.Random(20261010)
    deltas = []
    for _ in range(5000):
        indices = [rng.randrange(len(main_rows)) for _ in main_rows]
        deltas.append(boundary_f1(affix_rows, indices) - boundary_f1(main_rows, indices))
    deltas.sort()
    bootstrap = {
        "resamples": 5000,
        "seed": 20261010,
        "affix_minus_root_f1": affix["evaluations"]["affix_first32"]["dev_metrics"]["boundary_f1"]
        - root["evaluations"]["root_first32"]["dev_metrics"]["boundary_f1"],
        "percentile95": [deltas[124], deltas[4874]],
        "caveat": "exploratory type bootstrap; does not account for shared root families, label uncertainty or earlier DEV-driven choices",
    }
    scores = {}
    for label, result, key in candidates:
        evaluation = result["evaluations"][key]
        counts = evaluation["dev_counts"]
        metrics = evaluation["dev_metrics"]
        assert abs(metrics["boundary_f1"] - 2 * counts["tp"] / (2 * counts["tp"] + counts["fp"] + counts["fn"])) < 1e-12
        scores[label] = {
            **metrics, **counts,
            "um_isolated": evaluation["infixes"]["um"]["isolated"],
            "in_isolated": evaluation["infixes"]["in"]["isolated"],
            "validation": result["validation"][key],
            "roles": evaluation["role_diagnostics"]["counts"],
            "roles_by_length": evaluation["role_diagnostics"]["by_length"],
            "root_controls": result["root_controls"]["totals"][key],
        }
    root_score = scores["Root then affix"]["boundary_f1"]
    affix_score = scores["Affix then root"]["boundary_f1"]
    baseline_score = scores["Current32"]["boundary_f1"]
    merge_ranks = {}
    for label, artifact in (("Root then affix", root_dir / "root-first-penalty32"),
                            ("Affix then root", affix_dir / "affix-first-penalty32")):
        doc = json.loads((artifact / "tokenizer.json").read_text(encoding="utf-8"))
        wanted = {"an", "ma", "in", "um", "ku", "bu", "sum", "sin"}
        merge_ranks[label] = {rule["result"]: rule["rank"] for rule in doc["merges"] if rule["result"] in wanted}
    observed_order = "affix_first" if affix_score > root_score else "root_first" if root_score > affix_score else "tie"
    summary = {
        "inputs": root["inputs"],
        "matched_caps": {"root": 2244, "affix": 256},
        "scores": scores,
        "observed_order_by_dev_f1": observed_order,
        "affix_first_exceeds_current_dev_f1": affix_score > baseline_score,
        "phase_statistics": {"root_first": root["training_report"]["phase_statistics"],
                             "affix_first": affix["training_report"]["phase_statistics"]},
        "merge_ranks": merge_ranks,
        "root_first_reproduces_previous_vocab_and_merges": old_equivalence,
        "bootstrap": bootstrap,
        "held_out_test_used": False,
        "translation_training_or_quality_evaluation": False,
        "installed_tokenizer_replaced": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Fresh affix-first versus root-first comparison", "",
        "Both candidates were freshly trained on identical original inputs, roles, penalty32 and vocabulary6080. Both use root cap2244 and affix cap256, and identical within-phase ranking. Only the priority order differs. The previous um seed is a supplemental runtime reference, not a newly trained all-affix candidate.", "",
        "| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 | DEV tokens/word | Validation tokens/word |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, row in scores.items():
        lines.append(f"| {name} | {100*row['boundary_f1']:.2f}% | {row['exact']} | {row['um_isolated']} | {row['in_isolated']} | {row['fertility']:.4f} | {row['validation']['word_fertility']:.6f} |")
    lines += ["", f"Better observed phase order by DEV F1: {observed_order}. Affix-first exceeds installed32 DEV F1: {affix_score > baseline_score}.",
              "", "| Word | " + " | ".join(name for name, _, _ in candidates) + " |",
              "|---|" + "---|" * len(candidates)]
    for word in ("kumain", "kuman", "sumulat", "sinulat", "bumasa", "suminulat", "lumapit", "tumula", "minum"):
        lines.append("| " + word + " | " + " | ".join(" + ".join(result["evaluations"][key]["probe_tokens"][word]) for _, result, key in candidates) + " |")
    lines += ["", "Selected global merge ranks (zero-based):", "", "```json",
              json.dumps(merge_ranks, indent=2), "```", "",
              "Early competing affix rules can cross a boundary at runtime before an infix forms; later root-supported rules can absorb an already formed infix. The training boundary constraint does not carry over to ordinary global inference. Prioritizing all affixes therefore differs from forcing um at rank0."]
    lines += ["", "| Tokenizer | Root spans isolated /97 | Affix spans isolated /80 | Whole root controls /74 |",
              "|---|---:|---:|---:|"]
    for name, row in scores.items():
        lines.append(f"| {name} | {row['roles']['root']['isolated']} | {row['roles']['affix']['isolated']} | {row['root_controls']['kept_whole']} |")
    lines += ["", "Role diagnostics cover72 analyzer/reference-aligned words. Labels and74 root controls are provisional, not independent human gold. Full272-word boundary F1 and original5um/41in denominators remain the primary frozen comparison.",
              "", "Actual new-token phase usage:", "", "```json",
              json.dumps(summary["phase_statistics"], indent=2), "```", "",
              f"Fresh root-first reproduces previous ordered vocabulary/merges: {old_equivalence}.",
              "", "Exploratory paired DEV bootstrap (affix minus root F1):", "", "```json", json.dumps(bootstrap, indent=2), "```", "",
              "DEV is mixed silver/user-derived with270/272 words seen in training and only five um cases. This compares the tested schedules, not all possible affix/root algorithms. Validation3284 records measures fertility/coverage rather than gold morphology. No final test text, translation training or translation-quality evaluation was used. Installed artifacts remain unchanged."]
    (output_dir / "comparison-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"observed_order": observed_order, "scores": {name: {k: row[k] for k in ("boundary_f1", "exact", "um_isolated", "in_isolated")} for name, row in scores.items()}, "bootstrap": bootstrap}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-dir", type=Path, required=True)
    parser.add_argument("--affix-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--old-root-artifact", type=Path)
    args = parser.parse_args()
    compare(args.root_dir.resolve(), args.affix_dir.resolve(), args.output_dir.resolve(), args.old_root_artifact)
