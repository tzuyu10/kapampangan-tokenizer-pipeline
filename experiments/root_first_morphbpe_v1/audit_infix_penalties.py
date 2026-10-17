"""Independently audit the completed infix-only penalty8/16/32/48 sweep.

Reuse the independent audit's runtime/DEV helpers, never the runner evaluator.
This checks exported models and recorded results without retraining. Original
weighted comparators remain morphology-constrained weighted BPE, not Plain BPE.
Full validation and training-corpus fertility are not recomputed here.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from audit_infix_comparison import (
    CURRENT,
    DEV,
    LEXICON_SHA,
    PROBES,
    ROOT,
    STREAM_SHA,
    ExpandedMorphologicalSegmenter,
    audit_annotations,
    build_role_references,
    compare_record,
    load_dev,
    load_lexicon,
    load_prepared_stream,
    load_runtime_tokenizer,
    require,
    score,
    sha256_file,
    snapshot,
    validate_artifact_files,
    write_json,
)

PENALTIES = (8, 16, 32, 48)
EXPECTED_SEEDS = [("i", "n"), ("u", "m"), ("I", "N"), ("U", "M")]


def audit(args):
    comparison_dir = args.comparison_dir.resolve()
    input_dir = args.input_dir.resolve()
    supplied = input_dir / "provenance/penalty32-tokenizer-manifest.json"
    require(supplied.read_bytes() == (CURRENT / "tokenizer-manifest.json").read_bytes(),
            "Installed baseline manifest drift")
    preserved = snapshot(CURRENT)
    source_paths = {
        "training_stream_sha256": input_dir / "training-inputs/training-stream.jsonl",
        "training_lexicon_sha256": input_dir / "training-inputs/training-lexicon.json",
        "validation_sha256": input_dir / "validation.csv", "dev_sha256": DEV,
        "analyzer_sha256": ROOT / "experiments/expanded_morphology_v4/expanded_morphology.py",
        "trainer_sha256": ROOT / "src/kapampangan_morphbpe/root_priority_bpe.py",
        "base_trainer_sha256": ROOT / "src/kapampangan_morphbpe/weighted_bpe.py",
        "runner_sha256": ROOT / "experiments/root_first_morphbpe_v1/run_experiment.py",
        "selection_evaluator_sha256": ROOT / "experiments/tokenizer_selection_v1/run_selection.py",
    }
    require(sha256_file(source_paths["training_stream_sha256"]) == STREAM_SHA, "Original stream drift")
    require(sha256_file(source_paths["training_lexicon_sha256"]) == LEXICON_SHA, "Original lexicon drift")
    prepared = load_prepared_stream(source_paths["training_stream_sha256"])
    lexicon = load_lexicon(source_paths["training_lexicon_sha256"])
    analyzer = ExpandedMorphologicalSegmenter(lexicon)
    rows = load_dev()
    references, skipped, role_words = build_role_references(rows, analyzer, lexicon)
    results = {}
    annotations = {}
    paths = {"current32": CURRENT}
    for penalty in PENALTIES:
        directory = comparison_dir / f"penalty-{penalty}"
        result = json.loads((directory / "comparison-result.json").read_text(encoding="utf-8"))
        config = result["config"]
        require(config["crossing_penalty"] == penalty, f"penalty{penalty}: configured penalty differs")
        require(config["priority_order"] == ["infix", "weighted"], f"penalty{penalty}: order differs")
        require(result["training_report"]["crossing_penalty"] == penalty, f"penalty{penalty}: trainer penalty differs")
        require(result["training_report"]["priority_order"] == ["infix", "weighted"],
                f"penalty{penalty}: reported order differs")
        require(result["initial_vocabulary"] == 1592 and result["vocabulary_size"] == 6080,
                f"penalty{penalty}: vocabulary capacity differs")
        require(config["vocabulary_budget"] == 6080 and result["merge_count"] == 4488,
                f"penalty{penalty}: vocabulary/merge budget differs")
        require(config["root_token_budget"] == 0 and config["affix_token_budget"] == 0,
                f"penalty{penalty}: inactive roles have priority budgets")
        require(config["infixes_have_separate_training_role"] is True, f"penalty{penalty}: no separate infix role")
        require(not result["held_out_test_used"] and not result["translation_training_or_quality_evaluation"],
                f"penalty{penalty}: final test or translation evaluation unexpectedly used")
        require(result["installed_inventory_unchanged"] is True, f"penalty{penalty}: installed baseline changed")
        statistics = result["training_report"]["phase_statistics"]
        for phase, expected in (("infix", 4), ("weighted", 4484), ("root", 0), ("affix", 0)):
            require(statistics[phase] == {"merge_rules": expected, "new_vocabulary_tokens": expected},
                    f"penalty{penalty}: unexpected phase count: {phase}")
        require([event["phase"] for event in result["training_report"]["phase_transitions"]]
                == ["infix", "weighted"], f"penalty{penalty}: actual phase order differs")
        for key, path in source_paths.items():
            require(sha256_file(path) == result["inputs"][key], f"penalty{penalty}: input/source drift: {key}")
        role_path = directory / "training-role-spans.jsonl"
        require(sha256_file(role_path) == result["inputs"]["role_spans_sha256"], f"penalty{penalty}: annotation checksum differs")
        annotations[str(penalty)] = audit_annotations(role_path, prepared, lexicon, result["annotation_summary"])
        candidate_key = f"infix_only{penalty}"
        require(candidate_key in result["evaluations"], f"penalty{penalty}: missing candidate evaluation")
        paths[candidate_key] = directory / f"infix-only-penalty{penalty}"
        if args.weighted_dir is not None:
            paths[f"matched_weighted{penalty}"] = args.weighted_dir.resolve() / f"penalty-{penalty}"
        results[str(penalty)] = result
    original_inputs = results["8"]["inputs"]
    common_config = {k: v for k, v in results["8"]["config"].items() if k != "crossing_penalty"}
    for penalty, result in results.items():
        require(result["inputs"] == original_inputs, f"penalty{penalty}: shared source/input/role hashes differ")
        require({k: v for k, v in result["config"].items() if k != "crossing_penalty"} == common_config,
                f"penalty{penalty}: additional configuration differences")
    inventories = {}
    runtimes = {}
    scores = {}
    documents = {}
    relevant_rules = {}
    for key, path in paths.items():
        inventories[key] = validate_artifact_files(path)
        require(inventories[key]["checksums_match"], f"{key}: invalid inventory")
        document = json.loads((path / "tokenizer.json").read_text(encoding="utf-8"))
        documents[key] = document
        require(len(document["vocabulary"]) == 6080 and len(document["merges"]) == 4488,
                f"{key}: exported vocabulary/merge count differs")
        if key != "current32":
            penalty = int(key.removeprefix("infix_only").removeprefix("matched_weighted"))
            require(document["metadata"]["crossing_penalty"] == penalty, f"{key}: exported penalty differs")
            require(document["metadata"]["training_stream_sha256"] == STREAM_SHA, f"{key}: original stream provenance differs")
            require(document["metadata"]["lexicon_used_at_runtime"] is False, f"{key}: runtime morphology unexpectedly used")
            if key.startswith("infix_only"):
                require(document["metadata"]["priority_order"] == ["infix", "weighted"], f"{key}: exported order differs")
                require([(m["left"], m["right"]) for m in document["merges"][:4]] == EXPECTED_SEEDS,
                        f"{key}: first four infix rules differ")
                require(document["metadata"]["held_out_test_used"] is False, f"{key}: final test used")
                require(document["metadata"]["selection_performed"] is False, f"{key}: unexpected frozen selection claim")
        runtime = load_runtime_tokenizer(path)
        runtimes[key] = runtime
        scores[key] = score(runtime, rows, references)
        relevant_rules[key] = [m for m in document["merges"]
                               if m["result"] in {"in", "um", "IN", "UM", "ma", "an", "ku", "bu", "su", "sin", "sum", "uman", "uma"}]
    compared = 0
    for penalty, result in results.items():
        for key, stored in result["evaluations"].items():
            require(key in scores, f"{key}: unknown comparator; provide --weighted-dir for matched weighted controls")
            compare_record(scores[key], stored, skipped, f"penalty{penalty}/{key}")
            compared += 1
    prior = args.prior_infix32.resolve()
    require(validate_artifact_files(prior)["checksums_match"], "Previous infix32 artifact inventory differs")
    old = json.loads((prior / "tokenizer.json").read_text(encoding="utf-8"))
    fresh = documents["infix_only32"]
    require(old["vocabulary"] == fresh["vocabulary"] and old["merges"] == fresh["merges"],
            "Fresh penalty32 does not reproduce previous infix-only vocabulary/merges")
    for filename in ("vocab.json", "merges.json"):
        require((prior / filename).read_bytes() == (paths["infix_only32"] / filename).read_bytes(),
                f"Fresh penalty32 does not byte-reproduce previous {filename}")
    if "matched_weighted32" in documents:
        control = documents["matched_weighted32"]
        baseline = documents["current32"]
        require(control["vocabulary"] == baseline["vocabulary"] and control["merges"] == baseline["merges"],
                "Original weighted32 differs from installed baseline")
    root_words = sorted(word for word in lexicon.valid_hosts if "um" in word)
    control_totals = {}
    for key, runtime in runtimes.items():
        details = {}
        for word in root_words:
            encoding = runtime.encode(word)
            require(runtime.decode(encoding.ids) == word, f"{key}: root-control round-trip failure")
            details[word] = [token.token for token in encoding.tokens]
        control_totals[key] = {"tokens": sum(len(pieces) for pieces in details.values()),
                               "kept_whole": sum(pieces == [word] for word, pieces in details.items())}
        for penalty, result in results.items():
            if key not in result["root_controls"]["totals"]:
                continue
            require(result["root_controls"]["rows"] == len(root_words), f"penalty{penalty}: root-control denominator differs")
            require(result["root_controls"]["totals"][key] == control_totals[key], f"penalty{penalty}/{key}: root-control totals differ")
            require({r["surface"]: r[key] for r in result["root_controls"]["details"]} == details,
                    f"penalty{penalty}/{key}: root-control encodings differ")
    require(snapshot(CURRENT) == preserved, "Installed baseline changed during audit")
    summaries = {}
    for key, observed in scores.items():
        probes = {}
        for word in PROBES:
            encoding = runtimes[key].encode(word)
            require(runtimes[key].decode(encoding.ids) == word, f"{key}: probe round-trip failure")
            probes[word] = [token.token for token in encoding.tokens]
        summaries[key] = {"dev_rows": 272, "metrics": observed["metrics"], "counts": observed["counts"],
                          "infixes": {p: {k: d[k] for k in ("rows", "isolated")} for p, d in observed["infixes"].items()},
                          "role_counts": observed["role_counts"], "role_lengths": observed["role_lengths"],
                          "probe_tokens": probes}
    summary = {
        "passed": True, "audited_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_script_sha256": sha256_file(Path(__file__)),
        "independent_audit_helper_sha256": sha256_file(Path(__file__).with_name("audit_infix_comparison.py")),
        "stored_evaluations_compared": compared, "distinct_artifacts_reencoded": len(scores),
        "fresh_dev_encodings": len(scores) * 272, "fresh_root_control_encodings": len(scores) * len(root_words),
        "shared_source_input_role_hashes_match": True, "same_four_initial_infix_rules": True,
        "fresh32_reproduces_previous_infix32_ordered_and_serialized_vocabulary_merges": True,
        "artifact_inventories": inventories, "training_annotations": annotations,
        "role_reference_words": len(role_words), "role_reference_skipped_rows": dict(skipped),
        "evaluations": summaries, "phase_statistics": {p: r["training_report"]["phase_statistics"] for p, r in results.items()},
        "relevant_merge_rules": relevant_rules, "root_controls": {"rows": len(root_words), "totals": control_totals},
        "installed_inventory_unchanged_during_audit": True,
        "limits": ["No retraining in this audit", "Full validation corpus metrics are not independently recomputed",
                   "MCF1 and full training-corpus fertility are not independently recomputed",
                   "Role labels and root controls derive from the provisional training analyzer/lexicon",
                   "DEV is mixed silver/user-derived; only five genuine um cases and 41 in cases",
                   "Matched weighted controls use morphology-constrained weighted BPE, not Plain BPE",
                   "No final test text or translation model evaluated"],
    }
    output = args.output.resolve() if args.output else comparison_dir / "audit-summary.json"
    write_json(output, summary)
    print(json.dumps({"passed": True, "output": str(output), "dev_encodings": summary["fresh_dev_encodings"],
                      "root_control_encodings": summary["fresh_root_control_encodings"],
                      "stored_evaluations_compared": compared,
                      "metrics": {k: {"F1": v["metrics"]["boundary_f1"], "exact": v["counts"]["exact"],
                                       "um": v["infixes"]["um"]["isolated"], "in": v["infixes"]["in"]["isolated"]}
                                  for k, v in summaries.items()}}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison-dir", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--prior-infix32", type=Path, required=True)
    parser.add_argument("--weighted-dir", type=Path)
    parser.add_argument("--output", type=Path)
    audit(parser.parse_args())
