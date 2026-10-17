"""Combine declared root budget runs without selecting or installing a tokenizer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarize(output_dir: Path) -> None:
    default = json.loads((output_dir / "comparison-result.json").read_text(encoding="utf-8"))
    smaller = json.loads(
        (output_dir / "root-budget-512/comparison-result.json").read_text(encoding="utf-8")
    )
    assert default["inputs"] == smaller["inputs"]
    assert default["evaluations"]["current32"] == smaller["evaluations"]["current32"]
    assert default["validation"]["current32"] == smaller["validation"]["current32"]
    assert default["config"]["root_token_budget"] == 2244
    assert smaller["config"]["root_token_budget"] == 512
    for result in (default, smaller):
        assert result["installed_inventory_unchanged"]
        assert result["vocabulary_size"] == 6080
        assert sum(
            phase["new_vocabulary_tokens"]
            for phase in result["training_report"]["phase_statistics"].values()
        ) == 4488

    candidates = [
        ("Current Morph-BPE32", default, "current32"),
        ("Root first2244", default, "root_first32"),
        ("Root first512", smaller, "root_first32"),
        ("Previous um first", default, "um_first32"),
    ]
    lines = [
        "# Root-first comparison summary",
        "",
        "Implemented and fully trained two root-first, affix-next candidates. "
        "Both use the exact original stream, penalty32 and vocabulary6080. "
        "The installed tokenizer was freshly evaluated and preserved.",
        "",
        "| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 | "
        "DEV tokens/word | Validation tokens/word | Root controls whole /74 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    rows = {}
    for name, result, key in candidates:
        evaluation = result["evaluations"][key]
        metrics = evaluation["dev_metrics"]
        controls = result["root_controls"]["totals"][key]
        row = {
            **metrics,
            **evaluation["dev_counts"],
            "um_isolated": evaluation["infixes"]["um"]["isolated"],
            "in_isolated": evaluation["infixes"]["in"]["isolated"],
            "validation_word_fertility": result["validation"][key]["word_fertility"],
            "root_controls_whole": controls["kept_whole"],
            "root_control_tokens": controls["tokens"],
        }
        rows[name] = row
        lines.append(
            f"| {name} | {100*row['boundary_f1']:.2f}% | {row['exact']} | "
            f"{row['um_isolated']} | {row['in_isolated']} | {row['fertility']:.4f} | "
            f"{row['validation_word_fertility']:.6f} | {row['root_controls_whole']} |"
        )
    lines += [
        "",
        "Recommendation: keep the installed tokenizer. Both tested strict "
        "root-first schedules underperform on frozen DEV morphology. They retain "
        "more provisional standalone roots, but root and affix isolation inside "
        "inflected words deteriorate. Lower fertility does not establish better morphology.",
        "",
        "| Word | " + " | ".join(name for name, _, _ in candidates) + " |",
        "|---|" + "---|" * len(candidates),
    ]
    for word in ("kumain", "kuman", "sumulat", "sinulat", "bumasa", "lumapit"):
        pieces = [
            " + ".join(result["evaluations"][key]["probe_tokens"][word])
            for _, result, key in candidates
        ]
        lines.append("| " + word + " | " + " | ".join(pieces) + " |")
    lines += [
        "",
        "The default run learns um at rank221, after ku19, bu37, lu47 and su169. "
        "Those earlier global rules can consume u before um forms in an infixed "
        "word. It also learns s+in->sin at rank550, producing sin|ulat. Protected "
        "training occurrences remain separate; global inference does not enforce "
        "the same boundaries.",
        "",
        "Actual phase allocations:",
        "",
        "| Root cap | Root new tokens | Affix new tokens | Weighted new tokens |",
        "|---|---:|---:|---:|",
    ]
    for result in (default, smaller):
        phases = result["training_report"]["phase_statistics"]
        lines.append(
            f"| {result['config']['root_token_budget']} | "
            f"{phases['root']['new_vocabulary_tokens']} | "
            f"{phases['affix']['new_vocabulary_tokens']} | "
            f"{phases['weighted']['new_vocabulary_tokens']} |"
        )
    lines += [
        "",
        "The 2244 root cap and256 affix cap were declared before DEV evaluation. "
        "The512 root cap was a diagnostic follow-up after the default underperformed. "
        "These exploratory runs are not an unbiased selection or final test result.",
        "",
        "DEV has272 mixed silver/user-derived words,270 seen in training and only "
        "five um cases. General role diagnostics cover72 analyzer/reference-aligned "
        "words (97 root and80 affix spans), not all DEV. Root controls are74 "
        "provisional lexicon hosts, not independent human gold. All3284 source "
        "validation records were scored per comparator; all retain118 UNK in39 "
        "records. No final test text or translation training/evaluation was used.",
        "",
        "Focused verification:20 tests pass; full training protected-span "
        "constraints, inventories and known-character runtime round-trips pass. "
        "A capped root bonus within the existing boundary-penalty score is a "
        "possible next experiment; it is not implemented or tested here.",
    ]
    (output_dir / "summary-report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )
    summary = {
        "inputs": default["inputs"],
        "candidates": rows,
        "recommendation": "retain installed tokenizer; tested strict priorities underperform",
        "root_cap512_followup_selected_after_default_results": True,
        "held_out_test_used": False,
        "translation_training_or_quality_evaluation": False,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(rows), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    summarize(parser.parse_args().output_dir.resolve())
