from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files
from kapampangan_morphbpe.bpe import ConstrainedBPETrainer, train_candidate_models
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION
from kapampangan_morphbpe.models import PreparedSequence, PretokenKind
from kapampangan_morphbpe.pipeline import export_candidate_models
from kapampangan_morphbpe.prepare import load_prepared_stream
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.serialization import (
    fingerprint,
    read_json,
    sha256_file,
    write_json,
)

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
TARGETS = (8192, 16384)
DIAGNOSTIC_TEXT = "Bukas na datang ing pangulo."
PLAIN_STREAM_PATH = (
    REPOSITORY_ROOT / "experiments/source_adjudicated_v1/runs/plain-bpe/training-stream.jsonl"
)
PLAIN_STREAM_MANIFEST_PATH = (
    REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/runs/plain-bpe/training-stream-manifest.json"
)

CONDITIONS = {
    "original": {
        "stream": REPOSITORY_ROOT / "runs/prepared/training-stream.jsonl",
        "prepared_manifest": REPOSITORY_ROOT / "runs/prepared/training-stream-manifest.json",
        "lexicon_manifest": REPOSITORY_ROOT / "resources/training-lexicon-manifest.json",
    },
    "source-adjudicated": {
        "stream": REPOSITORY_ROOT
        / "experiments/source_adjudicated_v1/runs/prepared/training-stream.jsonl",
        "prepared_manifest": REPOSITORY_ROOT
        / "experiments/source_adjudicated_v1/runs/prepared/training-stream-manifest.json",
        "lexicon_manifest": REPOSITORY_ROOT
        / "experiments/source_adjudicated_v1/resources/training-lexicon-manifest.json",
    },
}

PRESERVED_6080_DIRS = {
    "original-candidate": REPOSITORY_ROOT / "artifacts/candidates/vocab-6080",
    "original-determinism-rebuild": REPOSITORY_ROOT / "artifacts/determinism-rebuild",
    "original-selected": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "source-adjudicated-candidate": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/candidates/vocab-6080",
    "source-adjudicated-determinism-rebuild": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/determinism-rebuild",
    "source-adjudicated-plain": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer",
    "source-adjudicated-plain-rebuild": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/plain-bpe-determinism-rebuild",
    "source-adjudicated-selected": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/selected-tokenizer",
}

MORPH_ABLATION_DIRS = {
    f"{condition}-{target}": EXPERIMENT_ROOT
    / "artifacts"
    / condition
    / "candidates"
    / f"vocab-{target}"
    for condition in CONDITIONS
    for target in TARGETS
}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, Any], value)


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_preserved_artifacts() -> dict[str, dict[str, object]]:
    snapshots: dict[str, dict[str, object]] = {}
    for name, directory in PRESERVED_6080_DIRS.items():
        if not directory.is_dir():
            continue
        manifest = _object(read_json(directory / "tokenizer-manifest.json"), f"{name} manifest")
        target = _integer(manifest.get("target_vocabulary_size"), f"{name} target")
        if target != 6080:
            raise AssertionError(f"preserved artifact {name} is not a 6,080 build")
        hashes = _directory_hashes(directory)
        snapshots[name] = {
            "artifact_fingerprint": manifest.get("artifact_fingerprint"),
            "directory_fingerprint": fingerprint(hashes),
            "file_count": len(hashes),
            "path": directory.relative_to(REPOSITORY_ROOT).as_posix(),
        }
    required = {"original-selected", "source-adjudicated-selected"}
    if not required.issubset(snapshots):
        raise FileNotFoundError("both selected 6,080 artifacts must exist")
    return snapshots


def _snapshot_morph_ablation_artifacts() -> dict[str, dict[str, object]]:
    snapshots: dict[str, dict[str, object]] = {}
    for name, directory in MORPH_ABLATION_DIRS.items():
        manifest = _object(read_json(directory / "tokenizer-manifest.json"), f"{name} manifest")
        hashes = _directory_hashes(directory)
        snapshots[name] = {
            "artifact_fingerprint": manifest.get("artifact_fingerprint"),
            "directory_fingerprint": fingerprint(hashes),
            "file_count": len(hashes),
        }
    return snapshots


def _validate_inputs(
    stream_path: Path, prepared_manifest_path: Path, lexicon_manifest_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    for path in (stream_path, prepared_manifest_path, lexicon_manifest_path):
        if not path.is_file():
            raise FileNotFoundError(path)
    prepared = _object(read_json(prepared_manifest_path), "prepared manifest")
    lexicon = _object(read_json(lexicon_manifest_path), "lexicon manifest")
    if prepared.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("prepared manifest dataset mismatch")
    if lexicon.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("lexicon manifest dataset mismatch")
    if sha256_file(stream_path) != prepared.get("stream_sha256"):
        raise ValueError("prepared stream hash mismatch")
    if prepared.get("lexicon_fingerprint") != lexicon.get("lexicon_fingerprint"):
        raise ValueError("prepared stream and lexicon fingerprints differ")
    return prepared, lexicon


def _surface_kind_frequencies(
    sequences: list[PreparedSequence],
) -> dict[tuple[str, PretokenKind], int]:
    counts: dict[tuple[str, PretokenKind], int] = {}
    for sequence in sequences:
        key = (sequence.surface, sequence.kind)
        counts[key] = counts.get(key, 0) + sequence.frequency
    return counts


def _write_grid(condition: str, prepared: dict[str, Any], output_path: Path) -> dict[str, Any]:
    initial_size = _integer(prepared.get("initial_vocabulary_size"), "initial vocabulary")
    feasible_merges = _integer(
        prepared.get("feasible_merge_upper_bound"), "feasible merge upper bound"
    )
    if TARGETS[0] <= initial_size or TARGETS[-1] > initial_size + feasible_merges:
        raise ValueError("requested vocabulary targets are infeasible")
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "frozen_before_validation",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "prepared_manifest_fingerprint": prepared.get("manifest_fingerprint"),
        "word_types": prepared.get("word_types"),
        "initial_vocabulary_size": initial_size,
        "initial_permitted_pair_types": prepared.get("initial_permitted_pair_types"),
        "feasible_merge_upper_bound": feasible_merges,
        "formula": "user-requested vocabulary ablation targets [8192,16384]",
        "candidate_vocabulary_sizes": list(TARGETS),
        "selection_hierarchy": [],
        "validation_results_observed_when_frozen": False,
        "experiment_condition": condition,
        "selection_performed": False,
    }
    grid = {**body, "grid_fingerprint": fingerprint(body)}
    write_json(output_path, grid)
    return cast(dict[str, Any], grid)


def _train_condition(condition: str) -> dict[str, object]:
    paths = CONDITIONS[condition]
    stream_path = paths["stream"]
    prepared_manifest_path = paths["prepared_manifest"]
    lexicon_manifest_path = paths["lexicon_manifest"]
    prepared, lexicon = _validate_inputs(stream_path, prepared_manifest_path, lexicon_manifest_path)

    condition_root = EXPERIMENT_ROOT / "artifacts" / condition / "candidates"
    grid_path = EXPERIMENT_ROOT / "configs" / condition / "candidate-grid.json"
    grid_path.parent.mkdir(parents=True, exist_ok=True)
    grid = _write_grid(condition, prepared, grid_path)
    models, training_report = train_candidate_models(
        stream_path, prepared_manifest_path, grid_path, condition_root
    )
    artifacts = export_candidate_models(
        models,
        condition_root,
        training_report_path=condition_root / "candidate-training-report.json",
        grid_path=grid_path,
        lexicon_manifest_path=lexicon_manifest_path,
        prepared_manifest_path=prepared_manifest_path,
    )
    family = _object(training_report.get("family_training"), "family training")
    if family.get("trained_targets") != list(TARGETS):
        raise AssertionError(f"{condition} did not reach every target")
    if family.get("failed_targets") != []:
        raise AssertionError(f"{condition} reported failed targets")
    if family.get("protected_boundary_merge_violations") != 0:
        raise AssertionError(f"{condition} crossed a protected boundary")

    candidate_manifests = _object(artifacts.get("candidate_manifests"), "candidate manifests")
    candidates: dict[str, object] = {}
    initial_size = _integer(prepared.get("initial_vocabulary_size"), "initial vocabulary")
    for target in TARGETS:
        artifact_dir = condition_root / f"vocab-{target}"
        manifest = _object(candidate_manifests.get(str(target)), "candidate manifest")
        if manifest.get("target_vocabulary_size") != target:
            raise AssertionError("candidate target metadata mismatch")
        if manifest.get("actual_vocabulary_size") != target:
            raise AssertionError("candidate did not reach its requested vocabulary size")
        if manifest.get("merge_count") != target - initial_size:
            raise AssertionError("candidate merge count does not match vocabulary growth")
        if manifest.get("protected_boundary_merge_violations") != 0:
            raise AssertionError("candidate manifest reports a protected-boundary violation")
        checksum_validation = validate_artifact_files(artifact_dir)
        tokenizer = load_runtime_tokenizer(artifact_dir)
        encoding = tokenizer.encode(DIAGNOSTIC_TEXT)
        if tokenizer.decode(encoding.ids) != DIAGNOSTIC_TEXT:
            raise AssertionError("runtime round trip changed the diagnostic sentence")
        candidates[str(target)] = {
            "actual_vocabulary_size": manifest.get("actual_vocabulary_size"),
            "artifact_fingerprint": manifest.get("artifact_fingerprint"),
            "checksum_validation": checksum_validation,
            "merge_count": manifest.get("merge_count"),
            "protected_boundary_merge_violations": manifest.get(
                "protected_boundary_merge_violations"
            ),
            "runtime_diagnostic_token_count": len(encoding.tokens),
        }

    return {
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "candidates": candidates,
        "condition": condition,
        "lexicon_fingerprint": lexicon.get("lexicon_fingerprint"),
        "prepared_manifest_fingerprint": prepared.get("manifest_fingerprint"),
        "stream_sha256": prepared.get("stream_sha256"),
        "training_report_fingerprint": training_report.get("report_fingerprint"),
    }


def _plain_bpe_card(target: int) -> str:
    return f"""# Kapampangan plain-BPE vocabulary-ablation control

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This shared {target:,}-token control retains the original and source-adjudicated
training surfaces, kinds, frequencies, pre-tokenizer, character inventory,
special tokens, and deterministic BPE trainer. Its sole training difference is
that every protected morphology boundary is cleared before BPE learning.

It is an unselected local comparison candidate. The unavailable raw validation
split was not reconstructed or re-evaluated, and its subwords must not be
interpreted as gold morphemes.
"""


def _load_morph_manifests() -> dict[str, dict[str, dict[str, Any]]]:
    manifests: dict[str, dict[str, dict[str, Any]]] = {}
    for condition in CONDITIONS:
        condition_manifests: dict[str, dict[str, Any]] = {}
        for target in TARGETS:
            path = MORPH_ABLATION_DIRS[f"{condition}-{target}"]
            manifest = _object(
                read_json(path / "tokenizer-manifest.json"),
                f"{condition} {target} MorphBPE manifest",
            )
            if manifest.get("artifact_type") != "kapampangan_morphbpe":
                raise ValueError("comparison MorphBPE artifact has the wrong type")
            if manifest.get("actual_vocabulary_size") != target:
                raise ValueError("comparison MorphBPE artifact has the wrong size")
            condition_manifests[str(target)] = manifest
        manifests[condition] = condition_manifests
    return manifests


def _train_plain() -> dict[str, object]:
    original_paths = CONDITIONS["original"]
    adjudicated_paths = CONDITIONS["source-adjudicated"]
    original_prepared, _original_lexicon = _validate_inputs(
        original_paths["stream"],
        original_paths["prepared_manifest"],
        original_paths["lexicon_manifest"],
    )
    adjudicated_prepared, _adjudicated_lexicon = _validate_inputs(
        adjudicated_paths["stream"],
        adjudicated_paths["prepared_manifest"],
        adjudicated_paths["lexicon_manifest"],
    )
    if not PLAIN_STREAM_PATH.is_file() or not PLAIN_STREAM_MANIFEST_PATH.is_file():
        raise FileNotFoundError("the verified shared plain-BPE stream is unavailable")
    plain_stream_manifest = _object(read_json(PLAIN_STREAM_MANIFEST_PATH), "plain stream manifest")
    if plain_stream_manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("plain stream dataset mismatch")
    if sha256_file(PLAIN_STREAM_PATH) != plain_stream_manifest.get("stream_sha256"):
        raise ValueError("plain stream hash mismatch")

    original_sequences = load_prepared_stream(original_paths["stream"])
    adjudicated_sequences = load_prepared_stream(adjudicated_paths["stream"])
    plain_sequences = load_prepared_stream(PLAIN_STREAM_PATH)
    original_counts = _surface_kind_frequencies(original_sequences)
    adjudicated_counts = _surface_kind_frequencies(adjudicated_sequences)
    plain_counts = _surface_kind_frequencies(plain_sequences)
    if original_counts != adjudicated_counts or original_counts != plain_counts:
        raise AssertionError(
            "plain, original, and source-adjudicated surface/kind/frequency inputs differ"
        )
    if any(sequence.protected_boundaries for sequence in plain_sequences):
        raise AssertionError("plain-BPE stream still contains a protected boundary")

    initial_size = _integer(original_prepared.get("initial_vocabulary_size"), "initial vocabulary")
    if adjudicated_prepared.get("initial_vocabulary_size") != initial_size:
        raise AssertionError("MorphBPE conditions have different initial vocabularies")
    grid_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "frozen_before_validation",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
        "source_prepared_manifest_fingerprints": {
            "original": original_prepared.get("manifest_fingerprint"),
            "source_adjudicated": adjudicated_prepared.get("manifest_fingerprint"),
        },
        "initial_vocabulary_size": initial_size,
        "candidate_vocabulary_sizes": list(TARGETS),
        "formula": "user-requested vocabulary ablation targets [8192,16384]",
        "validation_results_observed_when_frozen": False,
        "selection_performed": False,
        "experiment_condition": "plain_bpe_shared_control",
    }
    grid = {**grid_body, "grid_fingerprint": fingerprint(grid_body)}
    write_json(EXPERIMENT_ROOT / "configs/plain/candidate-grid.json", grid)

    models, family = ConstrainedBPETrainer(plain_sequences).train(list(TARGETS))
    if family.get("trained_targets") != list(TARGETS) or family.get("failed_targets") != []:
        raise AssertionError("plain BPE did not reach every target")
    if family.get("protected_boundary_merge_violations") != 0:
        raise AssertionError("plain BPE reported an impossible boundary violation")
    training_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
        "family_training": family,
        "model_fingerprints": {
            str(target): fingerprint(model.to_dict()) for target, model in sorted(models.items())
        },
    }
    training_report = {
        **training_body,
        "report_fingerprint": fingerprint(training_body),
    }
    candidates_dir = EXPERIMENT_ROOT / "artifacts/plain/candidates"
    write_json(candidates_dir / "candidate-training-report.json", training_report)

    morph_manifests = _load_morph_manifests()
    candidates: dict[str, object] = {}
    artifact_manifests: dict[str, object] = {}
    for target in TARGETS:
        model = models.get(target)
        if model is None:
            raise AssertionError("plain-BPE model snapshot is missing")
        comparison_fingerprints = {
            condition: morph_manifests[condition][str(target)].get("artifact_fingerprint")
            for condition in CONDITIONS
        }
        metadata: dict[str, object] = {
            "candidate": True,
            "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
            "candidate_training_report_fingerprint": training_report.get("report_fingerprint"),
            "comparison_morphbpe_artifact_fingerprints": comparison_fingerprints,
            "current_validation_re_evaluated": False,
            "held_out_test_used": False,
            "morphology_boundaries_used": False,
            "only_training_difference": "all_protected_morphology_boundaries_cleared",
            "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
            "same_original_and_adjudicated_surface_kind_frequencies": True,
            "same_pretokenizer": True,
            "same_special_tokens": True,
            "same_target_vocabulary_size": True,
            "selection_performed": False,
            "tokenizer_condition": "plain_bpe",
            "training_records": original_prepared.get("training_records"),
            "train_sha256": original_prepared.get("input_train_sha256"),
        }
        artifact_dir = candidates_dir / f"vocab-{target}"
        manifest = export_tokenizer_artifact(
            model,
            artifact_dir,
            metadata=metadata,
            tokenizer_card=_plain_bpe_card(target),
            artifact_type="kapampangan_plain_bpe",
        )
        if manifest.get("actual_vocabulary_size") != target:
            raise AssertionError("plain artifact did not reach its requested size")
        if manifest.get("merge_count") != target - initial_size:
            raise AssertionError("plain artifact merge count is inconsistent")
        validation = validate_artifact_files(artifact_dir)
        tokenizer = load_runtime_tokenizer(artifact_dir)
        encoding = tokenizer.encode(DIAGNOSTIC_TEXT)
        if tokenizer.decode(encoding.ids) != DIAGNOSTIC_TEXT:
            raise AssertionError("plain runtime round trip changed the diagnostic sentence")
        plain_merge_hash = sha256_file(artifact_dir / "merges.json")
        merge_files_differ = {
            condition: plain_merge_hash
            != sha256_file(MORPH_ABLATION_DIRS[f"{condition}-{target}"] / "merges.json")
            for condition in CONDITIONS
        }
        candidates[str(target)] = {
            "actual_vocabulary_size": manifest.get("actual_vocabulary_size"),
            "artifact_fingerprint": manifest.get("artifact_fingerprint"),
            "artifact_type": manifest.get("artifact_type"),
            "checksum_validation": validation,
            "comparison_morphbpe_artifact_fingerprints": comparison_fingerprints,
            "merge_count": manifest.get("merge_count"),
            "merge_files_differ_from_morphbpe": merge_files_differ,
            "runtime_diagnostic_token_count": len(encoding.tokens),
        }
        artifact_manifests[str(target)] = manifest

    artifact_summary: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidate_manifests": artifact_manifests,
    }
    write_json(candidates_dir / "candidate-artifacts.json", artifact_summary)
    return {
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "candidates": candidates,
        "condition": "plain_bpe_shared_control",
        "original_and_adjudicated_surface_kind_frequencies_match": True,
        "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
        "plain_stream_sha256": plain_stream_manifest.get("stream_sha256"),
        "training_report_fingerprint": training_report.get("report_fingerprint"),
    }


def run(selected_condition: str) -> dict[str, object]:
    before = _snapshot_preserved_artifacts()
    morph_before = _snapshot_morph_ablation_artifacts() if selected_condition == "plain" else {}
    condition_names = (
        tuple(CONDITIONS)
        if selected_condition == "all"
        else (() if selected_condition == "plain" else (selected_condition,))
    )
    results = {condition: _train_condition(condition) for condition in condition_names}
    if selected_condition in {"all", "plain"}:
        results["plain"] = _train_plain()
    after = _snapshot_preserved_artifacts()
    if before != after:
        raise AssertionError("an existing 6,080 artifact changed during ablation training")
    if morph_before and morph_before != _snapshot_morph_ablation_artifacts():
        raise AssertionError("an existing 8K/16K MorphBPE artifact changed")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "diagnostic_text": DIAGNOSTIC_TEXT,
        "existing_6080_artifacts_unchanged": True,
        "existing_morph_ablation_artifacts_unchanged": bool(morph_before),
        "preserved_6080_artifacts": after,
        "raw_validation_available": False,
        "results": results,
        "selected_condition": selected_condition,
        "selection_performed": False,
        "target_vocabulary_sizes": list(TARGETS),
        "warning": (
            "These are vocabulary-size ablation candidates, not validation-selected final "
            "tokenizers."
        ),
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    report_path = EXPERIMENT_ROOT / "reports" / "training-summary.json"
    write_json(report_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--condition",
        choices=("all", "plain", *CONDITIONS),
        default="all",
        help="train both conditions or resume one condition",
    )
    args = parser.parse_args()
    print(json.dumps(run(cast(str, args.condition)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
