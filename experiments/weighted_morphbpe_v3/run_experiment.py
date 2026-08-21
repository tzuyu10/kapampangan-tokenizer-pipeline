from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "runtime"))

from kapampangan_morphbpe.artifact import (  # noqa: E402
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import (  # noqa: E402
    fingerprint,
    read_json,
    sha256_file,
    write_json,
)
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer  # noqa: E402

V2_ROOT = REPOSITORY_ROOT / "experiments/source_adjudicated_v2"
V2_STREAM_PATH = V2_ROOT / "runs/prepared/training-stream.jsonl"
V2_PREPARED_MANIFEST_PATH = V2_ROOT / "runs/prepared/training-stream-manifest.json"
V2_AUDIT_PATH = V2_ROOT / "runs/segmentations/externally-supported-boundary-audit.jsonl"
V2_SEGMENTATION_MANIFEST_PATH = V2_ROOT / "runs/segmentations/segmentation-manifest.json"

POLICY_PATH = EXPERIMENT_ROOT / "experiment-policy.json"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
TRAINING_REPORT_PATH = REPORTS_DIR / "training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "runtime-evaluation.json"
SUMMARY_PATH = REPORTS_DIR / "experiment-summary.md"

TARGETS = (6080, 8192, 16384)
PENALTIES = (1, 2, 4, 8)
PRESERVED_ARTIFACTS = {
    "canonical": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "v2-plain": V2_ROOT / "artifacts/plain",
    "v2-paper": V2_ROOT / "artifacts/morphbpe",
    "v2-boundary-safe": V2_ROOT / "artifacts/boundary-safe",
}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _policy() -> dict[str, Any]:
    policy = _object(read_json(POLICY_PATH), "v3 policy")
    if tuple(policy.get("crossing_penalties", [])) != PENALTIES:
        raise ValueError("v3 penalty grid differs from the frozen policy")
    if tuple(policy.get("target_vocabulary_sizes", [])) != TARGETS:
        raise ValueError("v3 vocabulary grid differs from the frozen policy")
    if policy.get("surface_specific_runtime_guarantees") != []:
        raise ValueError("v3 must not contain surface-specific runtime guarantees")
    if policy.get("surface_specific_training_overrides") != []:
        raise ValueError("v3 must not contain surface-specific training overrides")
    return policy


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            value: Any = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} must contain a JSON object")
            rows.append(cast(dict[str, Any], value))
    return rows


def _verified_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    prepared_manifest = _object(read_json(V2_PREPARED_MANIFEST_PATH), "v2 prepared manifest")
    segmentation_manifest = _object(
        read_json(V2_SEGMENTATION_MANIFEST_PATH), "v2 segmentation manifest"
    )
    if prepared_manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("v2 prepared stream dataset mismatch")
    if sha256_file(V2_STREAM_PATH) != prepared_manifest.get("stream_sha256"):
        raise ValueError("v2 prepared stream hash mismatch")
    if sha256_file(V2_AUDIT_PATH) != segmentation_manifest.get("audit_sha256"):
        raise ValueError("v2 external relation audit hash mismatch")
    return prepared_manifest, segmentation_manifest


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_preserved() -> dict[str, dict[str, str]]:
    return {name: _directory_hashes(path) for name, path in PRESERVED_ARTIFACTS.items()}


def _tokenizer_card(target: int, penalty: int) -> str:
    return f"""# Weighted MorphBPE v3 tokenizer ({target:,}; penalty {penalty})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This thesis extension ranks merge pair p by:

`allowed_frequency(p) - {penalty} * crossing_frequency(p)`

There are no surface-specific overrides or runtime guarantees. Inference is
ordinary lexicon-free BPE. This is an unselected provisional local-test artifact
evaluated against silver training-derived morphology, not independent gold.
"""


def _export_family(
    penalty: int,
    first: dict[int, Any],
    second: dict[int, Any],
    family_fingerprint: str,
    segmentation_fingerprint: str,
) -> dict[str, object]:
    manifests: dict[str, object] = {}
    for target in TARGETS:
        metadata: dict[str, object] = {
            "candidate": True,
            "condition": "weighted_morphbpe_extension",
            "crossing_penalty": penalty,
            "current_validation_re_evaluated": False,
            "held_out_test_used": False,
            "independent_evaluation_gold_used": False,
            "lexicon_used_at_runtime": False,
            "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
            "paper_replication_training": False,
            "runtime_boundary_guarantee_scope": "none",
            "segmentation_manifest_fingerprint": segmentation_fingerprint,
            "selection_performed": False,
            "source_adjudicated_v2_input": True,
            "surface_specific_runtime_guarantees": [],
            "surface_specific_training_overrides": [],
            "training_family_fingerprint": family_fingerprint,
        }
        output = ARTIFACTS_DIR / f"penalty-{penalty}" / "candidates" / f"vocab-{target}"
        rebuild = ARTIFACTS_DIR / f"penalty-{penalty}" / "determinism-rebuild" / f"vocab-{target}"
        first_manifest = export_tokenizer_artifact(
            first[target],
            output,
            artifact_type="kapampangan_morphbpe",
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target, penalty),
        )
        second_manifest = export_tokenizer_artifact(
            second[target],
            rebuild,
            artifact_type="kapampangan_morphbpe",
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target, penalty),
        )
        if first_manifest != second_manifest:
            raise AssertionError(f"penalty {penalty} target {target} manifest differs on rebuild")
        if _directory_hashes(output) != _directory_hashes(rebuild):
            raise AssertionError(f"penalty {penalty} target {target} files differ on rebuild")
        validate_artifact_files(output)
        manifests[str(target)] = first_manifest
    return manifests


def train() -> dict[str, Any]:
    policy = _policy()
    prepared_manifest, segmentation_manifest = _verified_inputs()
    before = _snapshot_preserved()
    prepared = load_prepared_stream(V2_STREAM_PATH)

    first_models: dict[int, dict[int, Any]] = {}
    second_models: dict[int, dict[int, Any]] = {}
    family_reports: dict[str, object] = {}
    for penalty in PENALTIES:
        first, first_report = WeightedMorphBPETrainer(prepared, penalty).train(list(TARGETS))
        second, second_report = WeightedMorphBPETrainer(prepared, penalty).train(list(TARGETS))
        if first_report != second_report:
            raise AssertionError(f"penalty {penalty} training report differs on rebuild")
        if first_report.get("trained_targets") != list(TARGETS):
            raise AssertionError(f"penalty {penalty} failed to reach every target")
        if first_report.get("protected_boundary_merge_violations") != 0:
            raise AssertionError(f"penalty {penalty} crossed a training boundary")
        if first_report.get("surface_specific_runtime_guarantees") != []:
            raise AssertionError(f"penalty {penalty} contains a word-specific guarantee")
        for target in TARGETS:
            if first[target].to_dict() != second[target].to_dict():
                raise AssertionError(f"penalty {penalty} target {target} in-memory rebuild differs")
        first_models[penalty] = first
        second_models[penalty] = second
        family_reports[str(penalty)] = first_report

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": "weighted_morphbpe_extension",
        "merge_score": policy["merge_score"],
        "crossing_penalties": list(PENALTIES),
        "target_vocabulary_sizes": list(TARGETS),
        "v2_prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "v2_segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "surface_specific_runtime_guarantees": [],
        "surface_specific_training_overrides": [],
        "family_reports": family_reports,
        "deterministic_in_memory_rebuilds": True,
    }
    family_fingerprint = fingerprint(body)
    manifests = {
        str(penalty): _export_family(
            penalty,
            first_models[penalty],
            second_models[penalty],
            family_fingerprint,
            cast(str, segmentation_manifest["manifest_fingerprint"]),
        )
        for penalty in PENALTIES
    }
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("weighted v3 training changed an existing artifact")

    final_body: dict[str, object] = {
        **body,
        "artifact_manifests": manifests,
        "existing_artifacts_unchanged": True,
        "training_family_fingerprint": family_fingerprint,
    }
    report = {**final_body, "report_fingerprint": fingerprint(final_body)}
    write_json(TRAINING_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0.0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


def _runtime_metrics(artifact: Path, rows: list[dict[str, Any]]) -> dict[str, object]:
    tokenizer = load_runtime_tokenizer(artifact)
    true_positive = false_positive = false_negative = 0
    missed_types = extra_types = exact_types = 0
    exact_occurrences = produced_tokens = total_occurrences = 0
    distance_sum = 0.0
    for row in rows:
        surface = str(row["surface"])
        segments = tuple(cast(list[str], row["segments"]))
        gold = set(cast(list[int], row["protected_boundaries"]))
        frequency = int(row["frequency"])
        encoding = tokenizer.encode(surface)
        if tokenizer.decode(encoding.ids) != surface:
            raise AssertionError(f"runtime failed to round-trip {surface!r}")
        pieces = tuple(token.token for token in encoding.tokens)
        predicted = {token.end for token in encoding.tokens[:-1]}
        missed = gold - predicted
        extra = predicted - gold
        true_positive += len(gold & predicted) * frequency
        false_positive += len(extra) * frequency
        false_negative += len(missed) * frequency
        missed_types += bool(missed)
        extra_types += bool(extra)
        exact_types += pieces == segments
        if pieces == segments:
            exact_occurrences += frequency
        produced_tokens += len(pieces) * frequency
        total_occurrences += frequency
        distance_sum += len(gold ^ predicted) / max(1, len(surface) - 1) * frequency

    precision = (
        true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    )
    return {
        "artifact": artifact.relative_to(REPOSITORY_ROOT).as_posix(),
        "vocabulary_size": tokenizer.vocabulary_size,
        "evaluated_types": len(rows),
        "evaluated_occurrences": total_occurrences,
        "exact_segment_types": exact_types,
        "exact_segment_occurrences": exact_occurrences,
        "missed_boundary_types": missed_types,
        "extra_boundary_types": extra_types,
        "boundary_precision": precision,
        "boundary_recall": recall,
        "boundary_f1": _f1(precision, recall),
        "normalized_morphological_distance": (
            distance_sum / total_occurrences if total_occurrences else 0.0
        ),
        "fertility": produced_tokens / total_occurrences if total_occurrences else 0.0,
        "lexicon_used_at_runtime": False,
    }


def validate() -> dict[str, Any]:
    _policy()
    _prepared_manifest, segmentation_manifest = _verified_inputs()
    rows = _load_jsonl(V2_AUDIT_PATH)
    if not rows or any(not cast(list[int], row["protected_boundaries"]) for row in rows):
        raise ValueError("v2 external relation audit must contain protected boundaries")

    targets: dict[str, object] = {}
    for target in TARGETS:
        plain = V2_ROOT / "artifacts/plain/candidates" / f"vocab-{target}"
        paper = V2_ROOT / "artifacts/morphbpe/candidates" / f"vocab-{target}"
        validate_artifact_files(plain)
        validate_artifact_files(paper)
        conditions: dict[str, object] = {
            "plain_bpe": _runtime_metrics(plain, rows),
            "paper_morphbpe": _runtime_metrics(paper, rows),
        }
        for penalty in PENALTIES:
            artifact = ARTIFACTS_DIR / f"penalty-{penalty}" / "candidates" / f"vocab-{target}"
            validate_artifact_files(artifact)
            manifest = _object(read_json(artifact / "tokenizer-manifest.json"), "artifact")
            metadata = _object(manifest.get("metadata"), "artifact metadata")
            if metadata.get("surface_specific_runtime_guarantees") != []:
                raise AssertionError("weighted artifact contains a surface-specific guarantee")
            if metadata.get("runtime_boundary_guarantee_scope") != "none":
                raise AssertionError("weighted artifact claims a runtime boundary guarantee")
            conditions[f"weighted_penalty_{penalty}"] = _runtime_metrics(artifact, rows)
        targets[str(target)] = conditions

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": "weighted_morphbpe_extension",
        "independent_evaluation_gold": False,
        "selection_performed": False,
        "silver_audit_sha256": sha256_file(V2_AUDIT_PATH),
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "surface_specific_runtime_guarantees": [],
        "targets": targets,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(RUNTIME_REPORT_PATH, report)
    _write_summary(report)
    return cast(dict[str, Any], report)


def _write_summary(report: dict[str, Any]) -> None:
    targets = _object(report["targets"], "runtime targets")
    lines = [
        "# Weighted MorphBPE v3 experiment",
        "",
        "This extension uses `allowed_frequency - penalty * crossing_frequency`.",
        "It has no word-specific training override or runtime guarantee.",
        "All results below use the 1,197-form training-derived silver audit, not independent gold.",
        "",
        "| Vocab | Condition | Exact types | Missed-boundary types | Boundary F1 | Fertility |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    order = (
        "plain_bpe",
        "paper_morphbpe",
        "weighted_penalty_1",
        "weighted_penalty_2",
        "weighted_penalty_4",
        "weighted_penalty_8",
    )
    for target in TARGETS:
        conditions = _object(targets[str(target)], f"target {target}")
        for name in order:
            metrics = _object(conditions[name], name)
            lines.append(
                f"| {target:,} | `{name}` | {metrics['exact_segment_types']:,} | "
                f"{metrics['missed_boundary_types']:,} | {metrics['boundary_f1']:.6f} | "
                f"{metrics['fertility']:.6f} |"
            )
    lines.extend(
        [
            "",
            "No penalty or vocabulary has been selected. Freeze independent development/test",
            "morphology before choosing a configuration or making a thesis effectiveness claim.",
            "",
        ]
    )
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run_all() -> dict[str, Any]:
    before = _snapshot_preserved()
    training = train()
    runtime = validate()
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("weighted v3 run changed an existing artifact")
    return {
        "status": "complete",
        "training_report_fingerprint": training["report_fingerprint"],
        "runtime_report_fingerprint": runtime["report_fingerprint"],
        "existing_artifacts_unchanged": True,
        "surface_specific_runtime_guarantees": [],
        "selection_performed": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the isolated weighted MorphBPE v3 study")
    parser.add_argument("stage", choices=("train", "validate", "all"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.stage == "train":
        result = train()
    elif args.stage == "validate":
        result = validate()
    else:
        result = run_all()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
