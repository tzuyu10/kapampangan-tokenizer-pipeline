"""Compare frozen infix-priority penalty sweeps without installing a tokenizer."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from compare_infix_orders import paired_bootstrap
from compare_priority_orders import boundary_f1, load_result

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from kapampangan_morphbpe.artifact import validate_artifact_files  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file  # noqa: E402

PENALTIES = (8, 16, 32, 48)
WANTED_MERGES = (
    "in", "um", "IN", "UM", "an", "ma", "ku", "bu", "sin", "sum", "uma", "uman", "minum",
)
PROBES = (
    "kumain", "kuman", "sumulat", "sinulat", "bumasa", "suminulat", "lumapit", "tumula", "minum",
)


def check_evaluation(evaluation: dict, validation: dict) -> None:
    """Recompute primary arithmetic from paired prediction rows."""
    assert evaluation["dev_rows"] == len(evaluation["dev_predictions"]) == 272
    predictions = evaluation["dev_predictions"]
    counts = evaluation["dev_counts"]
    for field in ("tp", "fp", "fn", "exact"):
        assert counts[field] == sum(row[field] for row in predictions)
    for row in predictions:
        assert "".join(row["pieces"]) == "".join(row["reference"]) == row["surface"]
        assert row["exact"] == (row["pieces"] == row["reference"])
        boundaries = []
        for pieces in (row["pieces"], row["reference"]):
            position = 0
            positions = set()
            for piece in pieces[:-1]:
                position += len(piece)
                positions.add(position)
            boundaries.append(positions)
        predicted, gold = boundaries
        assert row["tp"] == len(predicted & gold)
        assert row["fp"] == len(predicted - gold)
        assert row["fn"] == len(gold - predicted)
    metrics = evaluation["dev_metrics"]
    assert abs(metrics["boundary_f1"] - boundary_f1(predictions, list(range(272)))) < 1e-12
    assert abs(metrics["exact_match"] - counts["exact"] / 272) < 1e-12
    assert abs(metrics["fertility"] - sum(len(row["pieces"]) for row in predictions) / 272) < 1e-12
    assert evaluation["artifact_validation"]["checksums_match"]
    for infix, denominator in (("um", 5), ("in", 41)):
        group = evaluation["infixes"][infix]
        assert group["rows"] == len(group["details"]) == denominator
        assert group["isolated"] == sum(row["isolated"] for row in group["details"])
    assert validation["records"] == 3284
    assert validation["word_occurrences"] == 198790
    assert validation["unknown_tokens"] == 118 and validation["rows_with_unknown"] == 39
    assert abs(
        validation["word_fertility"] - validation["word_tokens"] / validation["word_occurrences"]
    ) < 1e-12


def extract_score(result: dict, key: str) -> dict:
    evaluation = result["evaluations"][key]
    check_evaluation(evaluation, result["validation"][key])
    return {
        **evaluation["dev_metrics"], **evaluation["dev_counts"],
        "um_isolated": evaluation["infixes"]["um"]["isolated"],
        "in_isolated": evaluation["infixes"]["in"]["isolated"],
        "validation": result["validation"][key],
        "roles": evaluation["role_diagnostics"]["counts"],
        "roles_by_length": evaluation["role_diagnostics"]["by_length"],
        "affix_families": evaluation["role_diagnostics"]["families"],
        "training_corpus": evaluation["training_corpus"],
        "root_controls": result["root_controls"]["totals"][key],
    }


def check_result(result: dict, directory: Path, penalty: int) -> dict:
    config = result["config"]
    assert config["crossing_penalty"] == penalty
    assert config["priority_order"] == ["infix", "weighted"]
    assert config["root_token_budget"] == config["affix_token_budget"] == 0
    assert config["infix_token_budget"] == 32
    assert config["infixes_have_separate_training_role"]
    assert result["vocabulary_size"] == config["vocabulary_budget"] == 6080
    assert result["initial_vocabulary"] == 1592 and result["merge_count"] == 4488
    assert result["installed_inventory_unchanged"]
    assert not result["held_out_test_used"]
    assert not result["translation_training_or_quality_evaluation"]
    assert result["annotation_summary"]["infixes_have_separate_training_role"]
    assert sha256_file(directory / "training-role-spans.jsonl") == result["inputs"]["role_spans_sha256"]
    report = result["training_report"]
    assert report["algorithm"] == "infix_priority_then_weighted"
    assert report["crossing_penalty"] == penalty
    assert report["protected_boundary_merge_violations"] == 0
    assert report["training_roles_used_at_runtime"] is False
    assert report["phase_statistics"] == {
        "root": {"merge_rules": 0, "new_vocabulary_tokens": 0},
        "affix": {"merge_rules": 0, "new_vocabulary_tokens": 0},
        "infix": {"merge_rules": 4, "new_vocabulary_tokens": 4},
        "weighted": {"merge_rules": 4484, "new_vocabulary_tokens": 4484},
    }
    assert [(event["phase"], event["merge_rank"], event["reason"])
            for event in report["phase_transitions"]] == [
        ("infix", 0, "initial_phase"), ("weighted", 4, "no_supported_pair"),
    ]
    artifact = directory / f"infix-only-penalty{penalty}"
    assert validate_artifact_files(artifact)["checksums_match"]
    document = json.loads((artifact / "tokenizer.json").read_text(encoding="utf-8"))
    assert len(document["vocabulary"]) == 6080 and len(document["merges"]) == 4488
    metadata = document["metadata"]
    for key, value in config.items():
        assert metadata[key] == value
    for key, value in result["inputs"].items():
        assert metadata[key] == value
    assert metadata["algorithm"] == "infix_priority_then_weighted"
    assert metadata["protected_boundary_merge_violations"] == 0
    assert not metadata["lexicon_used_at_runtime"]
    assert not metadata["held_out_test_used"] and not metadata["selection_performed"]
    assert metadata["surface_specific_overrides"] == []
    assert [rule["result"] for rule in document["merges"][:4]] == ["in", "um", "IN", "UM"]
    return document


def check_prior(new_artifact: Path, prior_artifact: Path | None) -> dict | None:
    if prior_artifact is None:
        return None
    assert validate_artifact_files(prior_artifact)["checksums_match"]
    before = json.loads((prior_artifact / "tokenizer.json").read_text(encoding="utf-8"))
    after = json.loads((new_artifact / "tokenizer.json").read_text(encoding="utf-8"))
    for key in ("crossing_penalty", "vocabulary_budget", "infix_token_budget", "priority_order"):
        assert before["metadata"][key] == after["metadata"][key]
    for key in ("training_stream_sha256", "training_lexicon_sha256", "role_spans_sha256"):
        assert before["metadata"][key] == after["metadata"][key]
    equivalence = {
        "ordered_vocabulary_equal": before["vocabulary"] == after["vocabulary"],
        "ordered_merge_rules_equal": before["merges"] == after["merges"],
        "vocab_json_byte_equal": (prior_artifact / "vocab.json").read_bytes()
        == (new_artifact / "vocab.json").read_bytes(),
        "merges_json_byte_equal": (prior_artifact / "merges.json").read_bytes()
        == (new_artifact / "merges.json").read_bytes(),
    }
    assert all(equivalence.values())
    return equivalence


def earliest_ranks(document: dict) -> dict:
    ranks = {token: None for token in WANTED_MERGES}
    for rule in document["merges"]:
        if rule["result"] in ranks and ranks[rule["result"]] is None:
            ranks[rule["result"]] = rule["rank"]
    return ranks


def compare(comparison_dir: Path, output_dir: Path, prior_infix32: Path | None) -> dict:
    runs = {}
    documents = {}
    for penalty in PENALTIES:
        directory = comparison_dir / f"penalty-{penalty}"
        runs[penalty] = load_result(directory)
        documents[penalty] = check_result(runs[penalty], directory, penalty)
    first = runs[8]
    source_paths = {
        "analyzer_sha256": ROOT / "experiments/expanded_morphology_v4/expanded_morphology.py",
        "trainer_sha256": ROOT / "src/kapampangan_morphbpe/root_priority_bpe.py",
        "base_trainer_sha256": ROOT / "src/kapampangan_morphbpe/weighted_bpe.py",
        "runner_sha256": ROOT / "experiments/root_first_morphbpe_v1/run_experiment.py",
        "selection_evaluator_sha256": ROOT / "experiments/tokenizer_selection_v1/run_selection.py",
    }
    for key, path in source_paths.items():
        assert sha256_file(path) == first["inputs"][key]
    for result in runs.values():
        assert result["inputs"] == first["inputs"]
        assert result["annotation_summary"] == first["annotation_summary"]
        assert result["evaluations"]["current32"] == first["evaluations"]["current32"]
        assert result["validation"]["current32"] == first["validation"]["current32"]
        assert result["root_controls"]["rows"] == first["root_controls"]["rows"] == 74
        assert result["root_controls"]["totals"]["current32"] == first["root_controls"]["totals"]["current32"]
        assert [row["surface"] for row in result["root_controls"]["details"]] == [
            row["surface"] for row in first["root_controls"]["details"]
        ]
    assert {
        key: value for key, value in runs[32]["evaluations"]["matched_weighted32"].items()
        if key != "artifact_validation"
    } == {
        key: value for key, value in runs[32]["evaluations"]["current32"].items()
        if key != "artifact_validation"
    }
    assert runs[32]["validation"]["matched_weighted32"] == runs[32]["validation"]["current32"]
    assert runs[32]["root_controls"]["totals"]["matched_weighted32"] == runs[32]["root_controls"]["totals"]["current32"]
    reproduction = check_prior(
        comparison_dir / "penalty-32/infix-only-penalty32", prior_infix32,
    )
    scores = {"current32": extract_score(first, "current32")}
    matched = {}
    probes = {"current32": first["evaluations"]["current32"]["probe_tokens"]}
    bootstrap = {}
    baseline_rows = first["evaluations"]["current32"]["dev_predictions"]
    for penalty, result in runs.items():
        candidate_key = f"infix_only{penalty}"
        ordinary_key = f"matched_weighted{penalty}"
        candidate_score = extract_score(result, candidate_key)
        ordinary_score = extract_score(result, ordinary_key)
        scores[candidate_key] = candidate_score
        matched[str(penalty)] = {
            "ordinary_weighted": ordinary_score, "infix_priority": candidate_score,
            "infix_minus_ordinary_f1": candidate_score["boundary_f1"] - ordinary_score["boundary_f1"],
        }
        probes[candidate_key] = result["evaluations"][candidate_key]["probe_tokens"]
        candidate_rows = result["evaluations"][candidate_key]["dev_predictions"]
        bootstrap[f"{candidate_key}_minus_current32"] = paired_bootstrap(candidate_rows, baseline_rows)
        bootstrap[f"{candidate_key}_minus_{ordinary_key}"] = paired_bootstrap(
            candidate_rows, result["evaluations"][ordinary_key]["dev_predictions"],
        )
    bootstrap["infix_only48_minus_infix_only32"] = paired_bootstrap(
        runs[48]["evaluations"]["infix_only48"]["dev_predictions"],
        runs[32]["evaluations"]["infix_only32"]["dev_predictions"],
    )
    maximum = max(row["boundary_f1"] for row in scores.values())
    summary = {
        "inputs": first["inputs"], "annotation_summary": first["annotation_summary"],
        "scores": scores, "matched_penalty_scores": matched, "probe_tokens": probes,
        "configs": {str(p): runs[p]["config"] for p in PENALTIES},
        "phase_statistics": {str(p): runs[p]["training_report"]["phase_statistics"] for p in PENALTIES},
        "merge_ranks": {str(p): earliest_ranks(documents[p]) for p in PENALTIES},
        "bootstrap": bootstrap, "fresh32_reproduces_prior_infix32": reproduction,
        "remaining_um_errors": {
            f"infix_only{p}": [
                {key: row[key] for key in ("surface", "reference", "pieces")}
                for row in runs[p]["evaluations"][f"infix_only{p}"]["infixes"]["um"]["details"]
                if not row["isolated"]
            ] for p in PENALTIES
        },
        "best_observed_dev_f1": [key for key, row in scores.items() if row["boundary_f1"] == maximum],
        "ordinary_comparators_freshly_evaluated_not_retrained": True,
        "current32_baseline_equal_across_runs": True,
        "source_hashes_match_current_files": True,
        "matched_weighted32_behavior_equal_current32": True,
        "held_out_test_used": False, "translation_training_or_quality_evaluation": False,
        "installed_tokenizer_replaced": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n",
    )
    write_report(summary, output_dir)
    print(json.dumps({
        "scores": {key: {field: row[field] for field in (
            "boundary_f1", "exact", "um_isolated", "in_isolated",
        )} for key, row in scores.items()},
        "best_observed_dev_f1": summary["best_observed_dev_f1"],
        "fresh32_reproduces_prior_infix32": reproduction,
    }), flush=True)
    return summary


def write_report(summary: dict, output_dir: Path) -> None:
    scores = summary["scores"]
    labels = {"current32": "Current Morph-BPE32"}
    labels.update({f"infix_only{p}": f"Infix -> weighted, penalty {p}" for p in PENALTIES})
    lines = [
        "# Infix priority penalty comparison", "",
        "Four infix -> weighted candidates were freshly trained on the same original stream, "
        "lexicon and role annotations, with penalty 8/16/32/48 and vocabulary 6,080. "
        "The installed penalty32 baseline and ordinary weighted artifacts at each matching "
        "penalty were freshly evaluated with the same evaluator; those comparators were not retrained.", "",
        "All candidates use active caps infix32/root0/affix0. Actual usage is four infix merges "
        "(in, um, IN, UM), followed by 4,484 weighted merges. The protected training boundary "
        "rule and standard global inference stay fixed.", "",
        "| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 | DEV tokens/word | Validation tokens/word |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key, row in scores.items():
        lines.append(
            f"| {labels[key]} | {100*row['boundary_f1']:.2f}% | {row['exact']} | "
            f"{row['um_isolated']} | {row['in_isolated']} | {row['fertility']:.4f} | "
            f"{row['validation']['word_fertility']:.6f} |"
        )
    lines += ["", "Highest observed DEV F1: " + ", ".join(labels[key] for key in summary["best_observed_dev_f1"]) + ".", "",
              "## Effect of infix priority at the same penalty", "",
              "| Penalty | Ordinary F1 | Infix F1 | Difference, percentage points | Ordinary exact | Infix exact | Ordinary um/in | Infix um/in |",
              "|---|---:|---:|---:|---:|---:|---|---|"]
    for penalty, row in summary["matched_penalty_scores"].items():
        ordinary, infix = row["ordinary_weighted"], row["infix_priority"]
        lines.append(
            f"| {penalty} | {100*ordinary['boundary_f1']:.2f}% | {100*infix['boundary_f1']:.2f}% | "
            f"{100*row['infix_minus_ordinary_f1']:+.2f} | {ordinary['exact']} | {infix['exact']} | "
            f"{ordinary['um_isolated']}/5, {ordinary['in_isolated']}/41 | "
            f"{infix['um_isolated']}/5, {infix['in_isolated']}/41 |"
        )
    lines += ["", "## Examples", "", "| Word | " + " | ".join(labels.values()) + " |",
              "|---|" + "---|" * len(labels)]
    for word in PROBES:
        lines.append("| " + word + " | " + " | ".join(
            " + ".join(summary["probe_tokens"][key][word]) for key in scores
        ) + " |")
    lines += ["", "Remaining um isolation errors for the highest observed candidate:", "",
              "| Candidate | Word | Reference | Predicted |", "|---|---|---|---|"]
    for key in summary["best_observed_dev_f1"]:
        for row in summary["remaining_um_errors"].get(key, []):
            lines.append(f"| {labels[key]} | {row['surface']} | "
                         + " + ".join(row["reference"]) + " | "
                         + " + ".join(row["pieces"]) + " |")
    lines += ["", "## Role diagnostics and provisional root controls", "",
              "| Tokenizer | Root isolation | Affix isolation | Multiple-character roots | Multiple-character affixes | Whole root controls /74 |",
              "|---|---:|---:|---:|---:|---:|"]
    for key, row in scores.items():
        groups = [row["roles"]["root"], row["roles"]["affix"],
                  row["roles_by_length"]["root"]["multiple_characters"],
                  row["roles_by_length"]["affix"]["multiple_characters"]]
        lines.append(f"| {labels[key]} | " + " | ".join(
            f"{group['isolated']}/{group['spans']}" for group in groups
        ) + f" | {row['root_controls']['kept_whole']} |")
    lines += ["", "Evaluation's affix diagnostic includes infixes to retain comparable denominators. "
              "Training annotations separate them. Role labels and root controls come from the provisional "
              "training analyzer/lexicon, not independent human gold. Family-level diagnostics and matched "
              "ordinary fertility/control results are retained in summary.json.", "",
              "## Earliest global merge ranks", "", "Zero-based ranks; null means no rule constructs the token.",
              "", "```json", json.dumps(summary["merge_ranks"], indent=2), "```", "",
              "Forming infixes early does not prevent later global rules from absorbing them. "
              "Protected training boundaries do not constrain ordinary runtime BPE. "
              "An interrupted root remains continuous surface fragments; BPE cannot join them by skipping an infix.", "",
              "## Exploratory paired bootstrap", "", "Positive differences favor the infix candidate. "
              "Each interval uses 5,000 paired DEV resamples with seed20261010. "
              "These are exploratory intervals, without corrections for shared root families, uncertain "
              "labels, repeated experiments or prior DEV-driven design choices.", "", "```json",
              json.dumps(summary["bootstrap"], indent=2), "```", "",
              "Fresh penalty32 reproduces the prior infix-only ordered vocabulary, merge rules and "
              "core artifact bytes:", "", "```json",
              json.dumps(summary["fresh32_reproduces_prior_infix32"], indent=2), "```", "",
              "DEV has272 mixed silver/user-derived words,270 seen in training and only five genuine um "
              "examples. The observed ranking does not establish unseen-root, gold morphology or translation "
              "superiority. Validation3284 records measures token length and coverage rather than morphology "
              "accuracy. All candidates retain118 unknown tokens across39 validation records. "
              "No final test text or translation training/evaluation was used. Installed artifacts remain "
              "unchanged; changed tokenizer IDs require compatible new source embeddings before deployment."]
    (output_dir / "comparison-report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prior-infix32", type=Path)
    args = parser.parse_args()
    compare(args.comparison_dir.resolve(), args.output_dir.resolve(),
            args.prior_infix32.resolve() if args.prior_infix32 else None)
