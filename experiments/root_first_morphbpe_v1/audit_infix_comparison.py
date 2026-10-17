"""Independently audit completed infix-priority comparisons without retraining.

This uses the exported runtime, frozen DEV CSV, and analyzer directly. It does
not import the experiment runner or its evaluation functions. Full validation
corpus scores are reported as unaudited by this script. Training annotations
and analyzer-derived role diagnostics remain provisional, not independent gold.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
for extra in (ROOT / "src", ROOT / "runtime", ROOT / "experiments/expanded_morphology_v4"):
    sys.path.insert(0, str(extra))

from expanded_morphology import ExpandedMorphologicalSegmenter  # noqa: E402
from kapampangan_morphbpe.artifact import validate_artifact_files  # noqa: E402
from kapampangan_morphbpe.lexicon import load_lexicon  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402

DEV = ROOT / "experiments/tokenizer_selection_v1/data/dev.csv"
CURRENT = ROOT / "webapp/backend/tokenizer/artifacts/morphbpe-penalty32"
STREAM_SHA = "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7"
LEXICON_SHA = "5219e018bcd9c4aec44e377f0ba37b07dd2ce38485173102b5462501651050d8"
DEV_SHA = "c36f662b31d882503d7bde33a245cba6626e8b34c780a082628e1cd992b34275"
PROBES = ("kumain", "kuman", "sumulat", "sinulat", "bumasa", "sulat", "basa", "kain",
          "suminulat", "lumapit", "minum")
EXPECTED_ORDERS = {
    "infix-only": ["infix", "weighted"],
    "infix-root-affix": ["infix", "root", "affix", "weighted"],
}
KEYS = {"infix-only": "infix_only32", "infix-root-affix": "infix_root_affix32"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def snapshot(directory):
    return {p.relative_to(directory).as_posix(): sha256_file(p)
            for p in directory.rglob("*") if p.is_file()}


def load_dev():
    require(sha256_file(DEV) == DEV_SHA, "Frozen DEV checksum mismatch")
    with DEV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 272, "Expected 272 frozen DEV rows")
    require(len({r["surface"] for r in rows}) == 272, "Duplicate DEV surfaces")
    for row in rows:
        boundaries = set(map(int, row["boundaries"].split()))
        edges = [0, *sorted(boundaries), len(row["surface"])]
        row["gold"] = boundaries
        row["gold_pieces"] = [row["surface"][a:b] for a, b in zip(edges, edges[1:])]
    return rows


def classify(kind, surface, lexicon):
    if kind in {"root", "root_fragment"}:
        return "root"
    if kind == "root_or_compound":
        key = comparison_key(surface)
        return "root" if key in lexicon.valid_hosts and key not in lexicon.compounds else None
    if kind == "infix":
        return "infix"
    if kind in {"prefix", "suffix", "circumfix_prefix", "circumfix_suffix"}:
        return "affix"
    return None


def build_role_references(rows, analyzer, lexicon):
    references = []
    skipped = Counter()
    included_words = set()
    for row in rows:
        analysis = analyzer.segment(row["surface"])
        if list(analysis.segments) != row["gold_pieces"] or set(analysis.protected_boundaries) != row["gold"]:
            skipped["analyzer_reference_disagreement"] += 1
            continue
        if analysis.status not in {"accepted", "protected_root"}:
            skipped[analysis.status] += 1
            continue
        position = 0
        for surface, unit in zip(analysis.segments, analysis.underlying_units, strict=True):
            end = position + len(surface)
            role = classify(unit.kind, surface, lexicon)
            if role is not None:
                references.append({"word": row["surface"], "start": position, "end": end,
                                   "role": role, "surface": surface, "unit_kind": unit.kind,
                                   "underlying": unit.underlying})
                included_words.add(row["surface"])
            position = end
        require(position == len(row["surface"]), "Role reference offsets do not reconstruct word")
    return references, skipped, included_words


def score(runtime, rows, references):
    total = Counter()
    predictions = []
    infixes = {p: {"rows": 0, "isolated": 0, "details": []} for p in ("um", "in")}
    encodings = {}
    for row in rows:
        word = row["surface"]
        encoding = runtime.encode(word)
        tokens = encoding.tokens
        encodings[word] = tokens
        require(runtime.decode(encoding.ids) == word, f"DEV round-trip failure: {word}")
        pieces = [token.token for token in tokens]
        predicted = {token.end for token in tokens[:-1]}
        counts = {"tp": len(predicted & row["gold"]), "fp": len(predicted - row["gold"]),
                  "fn": len(row["gold"] - predicted), "exact": pieces == row["gold_pieces"]}
        record = {"surface": word, "pieces": pieces, "reference": row["gold_pieces"], **counts}
        predictions.append(record)
        total.update(counts)
        total["tokens"] += len(tokens)
        if not row["gold"]:
            total["zero_boundary_rows"] += 1
            total["kept_whole"] += len(tokens) == 1
        if (row["process"] == "infixation" and row["gold"] == {1, 3}
                and row["gold_pieces"][1] in infixes):
            infix = row["gold_pieces"][1]
            isolated = any(token.start == 1 and token.end == 3 and token.token == infix for token in tokens)
            infixes[infix]["rows"] += 1
            infixes[infix]["isolated"] += isolated
            infixes[infix]["details"].append({**record, "isolated": isolated})
    precision = total["tp"] / (total["tp"] + total["fp"]) if total["tp"] + total["fp"] else 0.0
    recall = total["tp"] / (total["tp"] + total["fn"]) if total["tp"] + total["fn"] else 0.0
    denominator = 2 * total["tp"] + total["fp"] + total["fn"]
    metrics = {"boundary_precision": precision, "boundary_recall": recall,
               "boundary_f1": 2 * total["tp"] / denominator if denominator else 0.0,
               "exact_match": total["exact"] / len(rows), "fertility": total["tokens"] / len(rows),
               "kept_whole_rate": total["kept_whole"] / total["zero_boundary_rows"]}
    role_counts = {p: Counter() for p in ("root", "affix", "infix")}
    lengths = {p: {k: Counter() for k in ("single_character", "multiple_characters")}
               for p in role_counts}
    families = {}
    details = []
    for span in references:
        role = span["role"]
        size = span["end"] - span["start"]
        isolated = any(token.start == span["start"] and token.end == span["end"]
                       and token.token == span["surface"] for token in encodings[span["word"]])
        role_counts[role].update({"spans": 1, "isolated": isolated, "characters": size})
        length = "single_character" if size == 1 else "multiple_characters"
        lengths[role][length].update({"spans": 1, "isolated": isolated})
        if role in {"affix", "infix"}:
            family = f"{span['unit_kind']}:{span['underlying']}"
            families.setdefault(family, Counter()).update({"spans": 1, "isolated": isolated})
        details.append({**span, "isolated": isolated})
    return {"metrics": metrics, "counts": {k: total[k] for k in ("tp", "fp", "fn", "exact")},
            "predictions": predictions, "infixes": infixes, "role_counts": role_counts,
            "role_lengths": lengths, "role_families": families, "role_details": details}


def compare_record(observed, stored, skipped, label):
    require(observed["predictions"] == stored["dev_predictions"], f"{label}: DEV predictions differ")
    require(observed["counts"] == stored["dev_counts"], f"{label}: DEV counts differ")
    require(stored["dev_rows"] == 272, f"{label}: DEV denominator differs")
    for key, value in observed["metrics"].items():
        require(abs(stored["dev_metrics"][key] - value) < 1e-12, f"{label}: metric differs: {key}")
    for infix in ("um", "in"):
        for key in ("rows", "isolated", "details"):
            require(observed["infixes"][infix][key] == stored["infixes"][infix][key],
                    f"{label}: {infix} diagnostic differs: {key}")
    role_diagnostics = stored["role_diagnostics"]
    stored_roles = set(role_diagnostics["counts"])
    require(stored_roles in ({"root", "affix"}, {"root", "affix", "infix"}), f"{label}: unexpected diagnostic roles")
    # The runner may retain its earlier combined-affix diagnostics for direct
    # comparison. Our fresh audit additionally breaks infixes out explicitly.
    combine_infixes = "infix" not in stored_roles
    compared_counts = {role: Counter(counts) for role, counts in observed["role_counts"].items()}
    compared_lengths = {role: {length: Counter(group) for length, group in groups.items()}
                        for role, groups in observed["role_lengths"].items()}
    compared_details = [dict(span) for span in observed["role_details"]]
    if combine_infixes:
        compared_counts["affix"].update(compared_counts.pop("infix"))
        for length, group in compared_lengths.pop("infix").items():
            compared_lengths["affix"][length].update(group)
        for span in compared_details:
            if span["role"] == "infix":
                span["role"] = "affix"
    require(dict(skipped) == role_diagnostics["skipped_rows"], f"{label}: skipped role rows differ")
    require(compared_details == role_diagnostics["details"], f"{label}: role span details differ")
    for role, counts in compared_counts.items():
        for key in ("spans", "isolated", "characters"):
            require(counts[key] == role_diagnostics["counts"][role][key], f"{label}: role count differs: {role}/{key}")
        rate = counts["isolated"] / counts["spans"] if counts["spans"] else None
        require(rate == role_diagnostics["counts"][role]["isolation_rate"], f"{label}: role rate differs: {role}")
        for length, group in compared_lengths[role].items():
            for key in ("spans", "isolated"):
                require(group[key] == role_diagnostics["by_length"][role][length][key],
                        f"{label}: length count differs: {role}/{length}/{key}")
    for family, group in role_diagnostics["families"].items():
        require(family in observed["role_families"], f"{label}: unknown role family")
        for key in ("spans", "isolated"):
            require(group[key] == observed["role_families"][family][key], f"{label}: family count differs: {family}/{key}")


def audit_annotations(path, prepared, lexicon, summary):
    counts = Counter()
    frequencies = Counter()
    previous_index = -1
    annotated = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            index = row["sequence_index"]
            require(previous_index < index < len(prepared), "Annotation indices are unordered or out of bounds")
            previous_index = index
            item = prepared[index]
            require(row["surface"] == item.surface and row["frequency"] == item.frequency,
                    "Annotation does not match frozen training sequence")
            edges = {0, len(item.surface), *item.protected_boundaries}
            previous_end = 0
            for span in row["spans"]:
                start, end = span["start"], span["end"]
                require(previous_end <= start < end <= len(item.surface), "Annotation spans overlap or exceed surface")
                require(start in edges and end in edges, "Annotation edges do not match frozen boundaries")
                require(not any(start < b < end for b in item.protected_boundaries), "Annotation crosses frozen boundary")
                surface = item.surface[start:end]
                require(surface == span["surface"], "Annotation surface differs from frozen slice")
                require(classify(span["unit_kind"], surface, lexicon) == span["role"], "Annotation role classification differs")
                previous_end = end
                counts[span["role"]] += 1
                frequencies[span["role"]] += item.frequency
            annotated += 1
    require(dict(counts) == summary["role_span_types"], "Training role counts differ")
    require(dict(frequencies) == summary["role_span_occurrences"], "Training role frequencies differ")
    require(annotated == summary["annotated_sequences"], "Annotated training denominator differs")
    return {"annotated_sequences": annotated, "role_span_types": dict(counts),
            "role_span_occurrences": dict(frequencies), "frozen_boundaries_checked": True}


def audit(args):
    comparison_dir = args.comparison_dir.resolve()
    input_dir = args.input_dir.resolve()
    supplied = input_dir / "provenance/penalty32-tokenizer-manifest.json"
    require(supplied.read_bytes() == (CURRENT / "tokenizer-manifest.json").read_bytes(), "Installed baseline manifest drift")
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
    artifact_paths = {"current32": CURRENT, "um_first32": args.prior_um.resolve()}
    annotations = {}
    for order, expected in EXPECTED_ORDERS.items():
        directory = comparison_dir / order
        result = json.loads((directory / "comparison-result.json").read_text(encoding="utf-8"))
        require(result["config"]["priority_order"] == expected, f"{order}: priority config differs")
        require(result["training_report"]["priority_order"] == expected, f"{order}: priority report differs")
        require([event["phase"] for event in result["training_report"]["phase_transitions"]] == expected,
                f"{order}: actual phase order differs")
        require(result["config"]["crossing_penalty"] == 32 and result["vocabulary_size"] == 6080,
                f"{order}: penalty or vocabulary differs")
        statistics = result["training_report"]["phase_statistics"]
        require(sum(group["new_vocabulary_tokens"] for group in statistics.values())
                == result["vocabulary_size"] - result["initial_vocabulary"],
                f"{order}: phase token budgets do not account for vocabulary")
        require(sum(group["merge_rules"] for group in statistics.values()) == result["merge_count"],
                f"{order}: phase merge counts do not account for learned rules")
        for role, group in statistics.items():
            if role not in expected:
                require(group["merge_rules"] == 0 and group["new_vocabulary_tokens"] == 0,
                        f"{order}: inactive role received priority merges")
        require(not result["held_out_test_used"] and not result["translation_training_or_quality_evaluation"],
                f"{order}: unexpected final-test or translation evaluation")
        for key, path in source_paths.items():
            require(sha256_file(path) == result["inputs"][key], f"{order}: source/input drift: {key}")
        role_path = directory / "training-role-spans.jsonl"
        require(sha256_file(role_path) == result["inputs"]["role_spans_sha256"], f"{order}: role checksum differs")
        annotations[order] = audit_annotations(role_path, prepared, lexicon, result["annotation_summary"])
        artifact_paths[KEYS[order]] = directory / f"{order}-penalty32"
        results[order] = result
    require(results["infix-only"]["inputs"] == results["infix-root-affix"]["inputs"], "Comparison source/input hashes differ")
    inventories = {}
    scores = {}
    runtimes = {}
    merge_examples = {}
    for key, path in artifact_paths.items():
        inventories[key] = validate_artifact_files(path)
        require(inventories[key]["checksums_match"], f"{key}: inventory differs")
        document = json.loads((path / "tokenizer.json").read_text(encoding="utf-8"))
        require(len(document["vocabulary"]) == 6080, f"{key}: vocabulary differs")
        for order, result in results.items():
            if key == KEYS[order]:
                require(len(document["merges"]) == result["merge_count"], f"{key}: exported merge count differs")
                require(document["metadata"]["priority_order"] == EXPECTED_ORDERS[order],
                        f"{key}: exported priority order differs")
        if key != "current32":
            require(document["metadata"]["training_stream_sha256"] == STREAM_SHA, f"{key}: original stream provenance differs")
            require(document["metadata"]["crossing_penalty"] == 32, f"{key}: penalty differs")
            require(document["metadata"]["lexicon_used_at_runtime"] is False, f"{key}: runtime morphology unexpectedly enabled")
        runtime = load_runtime_tokenizer(path)
        runtimes[key] = runtime
        scores[key] = score(runtime, rows, references)
        merge_examples[key] = [m for m in document["merges"]
                               if m["result"] in {"in", "um", "ma", "an", "ku", "bu", "su", "sin", "sum", "uman"}]
    compared = 0
    for order, result in results.items():
        for key, stored in result["evaluations"].items():
            require(key in scores, f"Unknown stored comparator: {key}")
            compare_record(scores[key], stored, skipped, f"{order}/{key}")
            compared += 1
    root_words = sorted(word for word in lexicon.valid_hosts if "um" in word)
    controls = {}
    for key, runtime in runtimes.items():
        details = {}
        for word in root_words:
            encoded = runtime.encode(word)
            require(runtime.decode(encoded.ids) == word, f"{key}: root-control round-trip failure")
            details[word] = [token.token for token in encoded.tokens]
        controls[key] = {"tokens": sum(len(pieces) for pieces in details.values()),
                         "kept_whole": sum(pieces == [word] for word, pieces in details.items())}
        for order, result in results.items():
            if key not in result["root_controls"]["totals"]:
                continue
            require(result["root_controls"]["rows"] == len(root_words), f"{order}: root-control denominator differs")
            require(result["root_controls"]["totals"][key] == controls[key], f"{order}/{key}: root-control totals differ")
            stored = {r["surface"]: r[key] for r in result["root_controls"]["details"]}
            require(stored == details, f"{order}/{key}: root-control pieces differ")
    require(snapshot(CURRENT) == preserved, "Installed baseline changed during audit")
    summaries = {}
    for key, observed in scores.items():
        summaries[key] = {"dev_rows": 272, "metrics": observed["metrics"], "counts": observed["counts"],
                          "infixes": {p: {k: d[k] for k in ("rows", "isolated")} for p, d in observed["infixes"].items()},
                          "role_counts": observed["role_counts"], "role_lengths": observed["role_lengths"],
                          "probe_tokens": {word: [token.token for token in runtimes[key].encode(word).tokens] for word in PROBES}}
    summary = {
        "passed": True, "audited_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_script_sha256": sha256_file(Path(__file__)), "stored_evaluations_compared": compared,
        "distinct_artifacts_reencoded": len(scores), "fresh_dev_encodings": len(scores) * len(rows),
        "shared_source_input_role_hashes_match": True, "artifact_inventories": inventories,
        "training_annotations": annotations, "role_reference_words": len(role_words),
        "role_reference_skipped_rows": dict(skipped), "evaluations": summaries,
        "phase_statistics": {order: result["training_report"]["phase_statistics"] for order, result in results.items()},
        "merge_examples": merge_examples, "root_controls": {"rows": len(root_words), "totals": controls},
        "installed_inventory_unchanged_during_audit": True,
        "limits": ["No retraining in this audit", "Full validation corpus metrics are not independently recomputed",
                   "MCF1 and full training-corpus fertility are not independently recomputed",
                   "Role labels and root controls derive from the provisional training analyzer/lexicon",
                   "DEV is mixed silver/user-derived; only five genuine um cases and 41 in cases",
                   "No final test text or translation model evaluated"],
    }
    output = args.output.resolve() if args.output else comparison_dir / "audit-summary.json"
    write_json(output, summary)
    print(json.dumps({"passed": True, "output": str(output), "dev_encodings": summary["fresh_dev_encodings"],
                      "stored_evaluations_compared": compared,
                      "metrics": {k: {"F1": v["metrics"]["boundary_f1"], "exact": v["counts"]["exact"],
                                       "um": v["infixes"]["um"]["isolated"], "in": v["infixes"]["in"]["isolated"]}
                                  for k, v in summaries.items()}}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison-dir", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--prior-um", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    audit(parser.parse_args())
