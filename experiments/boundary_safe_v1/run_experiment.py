from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, cast

from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files
from kapampangan_morphbpe.boundary_safe_bpe import BoundarySafeBPETrainer
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION, SPECIAL_TOKENS
from kapampangan_morphbpe.models import PreparedSequence
from kapampangan_morphbpe.morphology import MorphologicalSegmenter
from kapampangan_morphbpe.prepare import load_prepared_stream
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.serialization import (
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
POLICY_PATH = EXPERIMENT_ROOT / "experiment-policy.json"

SOURCE_ROOT = REPOSITORY_ROOT / "experiments/source_adjudicated_v1"
SOURCE_STREAM_PATH = SOURCE_ROOT / "runs/prepared/training-stream.jsonl"
SOURCE_STREAM_MANIFEST_PATH = SOURCE_ROOT / "runs/prepared/training-stream-manifest.json"
SOURCE_LEXICON_PATH = SOURCE_ROOT / "resources/training-lexicon.json"
SOURCE_LEXICON_MANIFEST_PATH = SOURCE_ROOT / "resources/training-lexicon-manifest.json"
CANONICAL_LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
CANONICAL_LEXICON_MANIFEST_PATH = REPOSITORY_ROOT / "resources/training-lexicon-manifest.json"

SEGMENTATION_DIR = EXPERIMENT_ROOT / "runs/segmentations"
SEGMENTATION_LIST_PATH = SEGMENTATION_DIR / "accepted-segmentations.jsonl"
BOUNDARY_AUDIT_LIST_PATH = SEGMENTATION_DIR / "boundary-audit-segmentations.jsonl"
SEGMENTATION_MANIFEST_PATH = SEGMENTATION_DIR / "accepted-segmentations-manifest.json"
CANDIDATES_DIR = EXPERIMENT_ROOT / "artifacts/candidates"
REBUILD_DIR = EXPERIMENT_ROOT / "artifacts/determinism-rebuild"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
TRAINING_REPORT_PATH = REPORTS_DIR / "training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "runtime-boundary-audit.json"
SUMMARY_PATH = REPORTS_DIR / "experiment-summary.json"

TARGETS = (6080, 8192, 16384)
ACCEPTED_STATUSES = {"accepted", "protected_compound", "protected_root"}
RICHARDS_IDS = {"ocr-010", "ocr-011", "ocr-012"}
DIAGNOSTIC_TEXT = "Bukas na datang ing pangulo."

PLAIN_ARTIFACTS = {
    6080: SOURCE_ROOT / "artifacts/plain-bpe-tokenizer",
    8192: REPOSITORY_ROOT / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
    16384: REPOSITORY_ROOT / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
}

PRESERVED_ARTIFACTS = {
    "canonical-6080": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "source-adjudicated-6080": SOURCE_ROOT / "artifacts/selected-tokenizer",
    "plain-6080": PLAIN_ARTIFACTS[6080],
    "source-adjudicated-8192": REPOSITORY_ROOT
    / "experiments/vocab_ablation_v1/artifacts/source-adjudicated/candidates/vocab-8192",
    "source-adjudicated-16384": REPOSITORY_ROOT
    / "experiments/vocab_ablation_v1/artifacts/source-adjudicated/candidates/vocab-16384",
    "plain-8192": PLAIN_ARTIFACTS[8192],
    "plain-16384": PLAIN_ARTIFACTS[16384],
}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _policy() -> dict[str, Any]:
    policy = _object(read_json(POLICY_PATH), "boundary-safe experiment policy")
    if policy.get("target_vocabulary_sizes") != list(TARGETS):
        raise ValueError("boundary-safe target vocabulary policy changed")
    if set(cast(list[str], policy.get("accepted_segmentation_statuses"))) != ACCEPTED_STATUSES:
        raise ValueError("accepted segmentation status policy changed")
    if set(cast(list[str], policy.get("richards_candidate_ids_held"))) != RICHARDS_IDS:
        raise ValueError("Richards hold policy changed")
    if policy.get("morpheme_seed_augmentation") is not False:
        raise ValueError("this comparison must not alter source surface frequencies")
    if policy.get("runtime_lexicon_used") is not False:
        raise ValueError("boundary-safe runtime must remain lexicon-free")
    return policy


def _source_manifests() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    prepared = _object(read_json(SOURCE_STREAM_MANIFEST_PATH), "source prepared manifest")
    lexicon = _object(read_json(SOURCE_LEXICON_MANIFEST_PATH), "source lexicon manifest")
    canonical_lexicon = _object(
        read_json(CANONICAL_LEXICON_MANIFEST_PATH), "canonical lexicon manifest"
    )
    if prepared.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("source prepared dataset fingerprint mismatch")
    if lexicon.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("source lexicon dataset fingerprint mismatch")
    if sha256_file(SOURCE_STREAM_PATH) != prepared.get("stream_sha256"):
        raise ValueError("source prepared stream hash mismatch")
    if sha256_file(SOURCE_LEXICON_PATH) != lexicon.get("lexicon_file_sha256"):
        raise ValueError("source lexicon hash mismatch")
    if sha256_file(CANONICAL_LEXICON_PATH) != canonical_lexicon.get("lexicon_file_sha256"):
        raise ValueError("canonical lexicon hash mismatch")
    if set(cast(list[str], lexicon.get("richards_candidate_ids_held"))) != RICHARDS_IDS:
        raise ValueError("source lexicon no longer holds the Richards candidates")
    return prepared, lexicon, canonical_lexicon


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_preserved_artifacts() -> dict[str, dict[str, str]]:
    return {name: _directory_hashes(path) for name, path in PRESERVED_ARTIFACTS.items()}


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(stable_compact_json(row) + "\n")


def _read_segmentations() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with SEGMENTATION_LIST_PATH.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            rows.append(_object(json.loads(line), f"segmentation line {line_number}"))
    return rows


def freeze_segmentations() -> dict[str, Any]:
    policy = _policy()
    prepared_manifest, lexicon_manifest, canonical_lexicon_manifest = _source_manifests()
    sequences = load_prepared_stream(SOURCE_STREAM_PATH)
    segmenter = MorphologicalSegmenter.from_path(SOURCE_LEXICON_PATH)
    canonical_segmenter = MorphologicalSegmenter.from_path(CANONICAL_LEXICON_PATH)

    rows: list[dict[str, object]] = []
    boundary_audit_rows: list[dict[str, object]] = []
    status_types: Counter[str] = Counter()
    status_occurrences: Counter[str] = Counter()
    accepted_occurrences = 0
    boundary_types = 0
    boundary_occurrences = 0
    for sequence in sequences:
        if sequence.kind != "word":
            continue
        analysis = segmenter.segment(sequence.surface)
        canonical_analysis = canonical_segmenter.segment(sequence.surface)
        if analysis.token != sequence.surface:
            raise AssertionError("prepared word and segmenter normalization differ")
        if analysis.protected_boundaries != sequence.protected_boundaries:
            raise AssertionError(f"prepared boundaries changed for {sequence.surface!r}")
        status_types[analysis.status] += 1
        status_occurrences[analysis.status] += sequence.frequency
        if analysis.status not in ACCEPTED_STATUSES:
            continue
        row: dict[str, object] = {
            "canonical_protected_boundaries": list(canonical_analysis.protected_boundaries),
            "canonical_status": canonical_analysis.status,
            "frequency": sequence.frequency,
            "kind": analysis.kind,
            "protected_boundaries": list(analysis.protected_boundaries),
            "rule_id": analysis.rule_id,
            "segments": list(analysis.segments),
            "status": analysis.status,
            "surface": analysis.token,
            "trace": list(analysis.trace),
        }
        rows.append(row)
        accepted_occurrences += sequence.frequency
        if analysis.protected_boundaries:
            boundary_types += 1
            boundary_occurrences += sequence.frequency
            if analysis.protected_boundaries != canonical_analysis.protected_boundaries:
                boundary_audit_rows.append(row)

    rows.sort(key=lambda row: cast(str, row["surface"]).encode("utf-8"))
    boundary_audit_rows.sort(key=lambda row: cast(str, row["surface"]).encode("utf-8"))
    _write_jsonl(SEGMENTATION_LIST_PATH, rows)
    _write_jsonl(BOUNDARY_AUDIT_LIST_PATH, boundary_audit_rows)
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "evidence_label": policy.get("evidence_label"),
        "independent_evaluation_gold": False,
        "accepted_statuses": sorted(ACCEPTED_STATUSES),
        "accepted_types": len(rows),
        "accepted_occurrences": accepted_occurrences,
        "boundary_types": boundary_types,
        "boundary_occurrences": boundary_occurrences,
        "boundary_audit_scope": policy.get("boundary_audit_scope"),
        "boundary_audit_types": len(boundary_audit_rows),
        "boundary_audit_occurrences": sum(
            cast(int, row["frequency"]) for row in boundary_audit_rows
        ),
        "boundary_audit_list_sha256": sha256_file(BOUNDARY_AUDIT_LIST_PATH),
        "status_types": dict(sorted(status_types.items())),
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "segmentation_list_sha256": sha256_file(SEGMENTATION_LIST_PATH),
        "source_prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "source_stream_sha256": prepared_manifest.get("stream_sha256"),
        "source_lexicon_manifest_fingerprint": lexicon_manifest.get("manifest_fingerprint"),
        "source_lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "canonical_lexicon_manifest_fingerprint": canonical_lexicon_manifest.get(
            "manifest_fingerprint"
        ),
        "experiment_policy_sha256": sha256_file(POLICY_PATH),
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    manifest = {**body, "manifest_fingerprint": fingerprint(body)}
    write_json(SEGMENTATION_MANIFEST_PATH, manifest)
    return cast(dict[str, Any], manifest)


def _load_verified_segmentations() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = _object(read_json(SEGMENTATION_MANIFEST_PATH), "segmentation manifest")
    if sha256_file(SEGMENTATION_LIST_PATH) != manifest.get("segmentation_list_sha256"):
        raise ValueError("frozen segmentation list hash mismatch")
    if manifest.get("independent_evaluation_gold") is not False:
        raise ValueError("rule-derived segmentations must not be labelled independent gold")
    rows = _read_segmentations()
    if len(rows) != manifest.get("accepted_types"):
        raise ValueError("frozen segmentation count mismatch")
    return rows, manifest


def _load_boundary_audit_segmentations(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if sha256_file(BOUNDARY_AUDIT_LIST_PATH) != manifest.get("boundary_audit_list_sha256"):
        raise ValueError("frozen boundary-audit list hash mismatch")
    rows: list[dict[str, Any]] = []
    with BOUNDARY_AUDIT_LIST_PATH.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if line.strip():
                rows.append(_object(json.loads(line), f"boundary audit line {line_number}"))
    if len(rows) != manifest.get("boundary_audit_types"):
        raise ValueError("frozen boundary-audit count mismatch")
    return rows


def _audit_sequences(rows: list[dict[str, Any]]) -> list[PreparedSequence]:
    audit: list[PreparedSequence] = []
    for row in rows:
        surface = row.get("surface")
        boundaries = row.get("protected_boundaries")
        if not isinstance(surface, str) or not isinstance(boundaries, list):
            raise ValueError("frozen segmentation row malformed")
        if boundaries:
            audit.append(PreparedSequence(surface, tuple(cast(list[int], boundaries)), "word", 1))
    return audit


def _training_metadata(
    target: int,
    segmentation_manifest: dict[str, Any],
    training_report: dict[str, Any],
) -> dict[str, object]:
    return {
        "candidate": True,
        "current_validation_re_evaluated": False,
        "held_out_test_used": False,
        "independent_evaluation_gold_used": False,
        "lexicon_used_at_runtime": False,
        "morpheme_seed_augmentation": False,
        "runtime_boundary_guarantee_scope": "source_adjudicated_boundary_changes",
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "selection_performed": False,
        "source_stream_sha256": segmentation_manifest.get("source_stream_sha256"),
        "target_vocabulary_size": target,
        "tokenizer_condition": "global_boundary_safe_morphbpe_extension",
        "training_report_fingerprint": training_report.get("report_fingerprint"),
        "training_runtime_contract": "standard_bpe_without_lexicon",
    }


def _tokenizer_card(target: int) -> str:
    return f"""# Boundary-safe MorphBPE extension ({target:,} tokens)

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This isolated local-test artifact extends MorphBPE training with an offline
standard-runtime audit. A proposed merge is deferred whenever it would cross a
boundary in the frozen source-adjudicated training-word segmentation list at
that merge rank. Runtime remains ordinary artifact-only BPE and loads no
lexicon or segmentation list.

The frozen list is deterministic rule-derived provisional/silver data, not an
independent human- or linguist-adjudicated gold evaluation set. The guarantee
is closed-set boundary preservation only; exact one-token-per-morpheme output
and generalization to unseen forms are measured rather than assumed. This is a
training extension, not an unmodified replication of the MorphBPE paper.
"""


def train_artifacts() -> dict[str, Any]:
    _policy()
    prepared_manifest, _lexicon_manifest, _canonical_lexicon_manifest = _source_manifests()
    rows, segmentation_manifest = _load_verified_segmentations()
    boundary_audit_rows = _load_boundary_audit_segmentations(segmentation_manifest)
    prepared = load_prepared_stream(SOURCE_STREAM_PATH)
    audit = _audit_sequences(boundary_audit_rows)
    initial_vocabulary_size = len(SPECIAL_TOKENS) + len(
        {character for sequence in prepared for character in sequence.surface}
    )
    if initial_vocabulary_size != prepared_manifest.get("initial_vocabulary_size"):
        raise AssertionError("source initial vocabulary size changed")

    first_models, first_family = BoundarySafeBPETrainer(prepared, audit).train(list(TARGETS))
    second_models, second_family = BoundarySafeBPETrainer(prepared, audit).train(list(TARGETS))
    if first_family != second_family:
        raise AssertionError("boundary-safe family training report is not deterministic")
    if first_family.get("trained_targets") != list(TARGETS):
        raise AssertionError("boundary-safe training did not reach every target")
    if first_family.get("failed_targets") != []:
        raise AssertionError("boundary-safe training reported failed targets")
    if first_family.get("protected_boundary_merge_violations") != 0:
        raise AssertionError("boundary-safe training crossed a protected training boundary")
    for target in TARGETS:
        if first_models[target].to_dict() != second_models[target].to_dict():
            raise AssertionError(f"boundary-safe model {target} is not deterministic")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "target_vocabulary_sizes": list(TARGETS),
        "source_prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "initial_vocabulary_size": initial_vocabulary_size,
        "family_training": first_family,
        "model_fingerprints": {
            str(target): fingerprint(first_models[target].to_dict()) for target in TARGETS
        },
        "second_build_model_fingerprints": {
            str(target): fingerprint(second_models[target].to_dict()) for target in TARGETS
        },
        "deterministic_in_memory_rebuild": True,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(TRAINING_REPORT_PATH, report)

    candidate_manifests: dict[str, object] = {}
    for target in TARGETS:
        metadata = _training_metadata(target, segmentation_manifest, report)
        candidate_dir = CANDIDATES_DIR / f"vocab-{target}"
        rebuild_dir = REBUILD_DIR / f"vocab-{target}"
        candidate_manifest = export_tokenizer_artifact(
            first_models[target],
            candidate_dir,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target),
        )
        rebuild_manifest = export_tokenizer_artifact(
            second_models[target],
            rebuild_dir,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target),
        )
        if _directory_hashes(candidate_dir) != _directory_hashes(rebuild_dir):
            raise AssertionError(f"boundary-safe artifact {target} rebuild is not byte-identical")
        if candidate_manifest != rebuild_manifest:
            raise AssertionError("deterministic artifact manifests differ")
        if candidate_manifest.get("actual_vocabulary_size") != target:
            raise AssertionError("boundary-safe artifact vocabulary target mismatch")
        validate_artifact_files(candidate_dir)
        candidate_manifests[str(target)] = candidate_manifest

    return {**report, "candidate_manifests": candidate_manifests}


def _runtime_audit_for_target(
    target: int,
    rows: list[dict[str, Any]],
    boundary_audit_surfaces: set[str],
) -> dict[str, object]:
    artifact = CANDIDATES_DIR / f"vocab-{target}"
    tokenizer = load_runtime_tokenizer(artifact)
    if tokenizer.vocabulary_size != target:
        raise AssertionError("runtime vocabulary size mismatch")

    exact_types = 0
    exact_occurrences = 0
    missed_boundary_types = 0
    missed_boundary_occurrences = 0
    audit_missed_boundary_types = 0
    audit_missed_boundary_occurrences = 0
    extra_boundary_types = 0
    extra_boundary_occurrences = 0
    exact_failures: list[dict[str, object]] = []
    regression_results: dict[str, object] = {}
    expected_regressions = set(cast(list[str], _policy().get("exact_runtime_regressions")))

    for row in rows:
        surface = cast(str, row["surface"])
        segments = tuple(cast(list[str], row["segments"]))
        gold = set(cast(list[int], row["protected_boundaries"]))
        frequency = cast(int, row["frequency"])
        encoding = tokenizer.encode(surface)
        if tokenizer.decode(encoding.ids) != surface:
            raise AssertionError(f"runtime round trip changed {surface!r}")
        pieces = tuple(token.token for token in encoding.tokens)
        predicted = {token.end for token in encoding.tokens[:-1]}
        missed = gold - predicted
        extra = predicted - gold
        if missed:
            missed_boundary_types += 1
            missed_boundary_occurrences += frequency
            if surface in boundary_audit_surfaces:
                audit_missed_boundary_types += 1
                audit_missed_boundary_occurrences += frequency
        if extra:
            extra_boundary_types += 1
            extra_boundary_occurrences += frequency
        if pieces == segments:
            exact_types += 1
            exact_occurrences += frequency
        elif len(exact_failures) < 100:
            exact_failures.append(
                {
                    "surface": surface,
                    "expected_segments": list(segments),
                    "runtime_pieces": list(pieces),
                    "frequency": frequency,
                }
            )
        if surface in expected_regressions:
            regression_results[surface] = {
                "expected_segments": list(segments),
                "runtime_pieces": list(pieces),
                "exact": pieces == segments,
            }

    missing_regressions = expected_regressions - set(regression_results)
    if missing_regressions:
        raise AssertionError(
            f"exact runtime regression forms missing: {sorted(missing_regressions)}"
        )
    failed_regressions = [
        surface
        for surface, result in regression_results.items()
        if not cast(dict[str, Any], result).get("exact")
    ]
    if failed_regressions:
        raise AssertionError(
            f"boundary-safe artifact {target} failed exact regressions: {failed_regressions}"
        )
    if audit_missed_boundary_types:
        raise AssertionError(
            f"boundary-safe artifact {target} crossed {audit_missed_boundary_types} audit forms"
        )

    total_types = len(rows)
    total_occurrences = sum(cast(int, row["frequency"]) for row in rows)
    diagnostic = tokenizer.encode(DIAGNOSTIC_TEXT)
    if tokenizer.decode(diagnostic.ids) != DIAGNOSTIC_TEXT:
        raise AssertionError("runtime changed the diagnostic sentence")
    return {
        "artifact_fingerprint": _object(
            read_json(artifact / "tokenizer-manifest.json"), "artifact manifest"
        ).get("artifact_fingerprint"),
        "vocabulary_size": target,
        "accepted_types": total_types,
        "accepted_occurrences": total_occurrences,
        "missed_boundary_types": missed_boundary_types,
        "missed_boundary_occurrences": missed_boundary_occurrences,
        "boundary_audit_types": len(boundary_audit_surfaces),
        "boundary_audit_missed_types": audit_missed_boundary_types,
        "boundary_audit_missed_occurrences": audit_missed_boundary_occurrences,
        "extra_boundary_types": extra_boundary_types,
        "extra_boundary_occurrences": extra_boundary_occurrences,
        "exact_segment_types": exact_types,
        "exact_segment_occurrences": exact_occurrences,
        "exact_segment_type_rate": exact_types / total_types,
        "exact_segment_occurrence_rate": exact_occurrences / total_occurrences,
        "exact_failure_samples": exact_failures,
        "exact_runtime_regressions": regression_results,
        "lexicon_used_at_runtime": False,
        "runtime_boundary_crossings_in_guaranteed_scope": 0,
        "runtime_condition": "standard_bpe_without_lexicon",
    }


def validate_runtime() -> dict[str, Any]:
    rows, segmentation_manifest = _load_verified_segmentations()
    boundary_audit_rows = _load_boundary_audit_segmentations(segmentation_manifest)
    boundary_audit_surfaces = {cast(str, row["surface"]) for row in boundary_audit_rows}
    targets = {
        str(target): _runtime_audit_for_target(target, rows, boundary_audit_surfaces)
        for target in TARGETS
    }
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "independent_evaluation_gold": False,
        "lexicon_used_at_runtime": False,
        "targets": targets,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(RUNTIME_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def _validate_plain_controls() -> dict[str, object]:
    controls: dict[str, object] = {}
    for target, path in PLAIN_ARTIFACTS.items():
        manifest = _object(read_json(path / "tokenizer-manifest.json"), "plain manifest")
        if manifest.get("artifact_type") != "kapampangan_plain_bpe":
            raise ValueError("prop2 plain control has the wrong artifact type")
        if manifest.get("actual_vocabulary_size") != target:
            raise ValueError("prop2 plain control has the wrong vocabulary size")
        validate_artifact_files(path)
        controls[str(target)] = manifest.get("artifact_fingerprint")
    return controls


def run() -> dict[str, Any]:
    before = _snapshot_preserved_artifacts()
    segmentation_manifest = freeze_segmentations()
    training = train_artifacts()
    runtime = validate_runtime()
    plain_controls = _validate_plain_controls()
    after = _snapshot_preserved_artifacts()
    if before != after:
        raise AssertionError("an existing tokenizer artifact changed during boundary-safe training")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": "global_boundary_safe_morphbpe_extension",
        "target_vocabulary_sizes": list(TARGETS),
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "training_report_fingerprint": training.get("report_fingerprint"),
        "runtime_report_fingerprint": runtime.get("report_fingerprint"),
        "plain_control_artifact_fingerprints": plain_controls,
        "existing_artifacts_unchanged": True,
        "lexicon_used_at_runtime": False,
        "paper_replication_training": False,
        "selection_performed": False,
        "warning": (
            "The frozen segmentation list is rule-derived provisional/silver training data, "
            "not independent human-adjudicated evaluation gold."
        ),
    }
    summary = {**body, "report_fingerprint": fingerprint(body)}
    write_json(SUMMARY_PATH, summary)
    return cast(dict[str, Any], summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stage",
        nargs="?",
        choices=("all", "freeze", "train", "validate"),
        default="all",
    )
    args = parser.parse_args()
    stage = cast(str, args.stage)
    if stage == "freeze":
        result = freeze_segmentations()
    elif stage == "train":
        result = train_artifacts()
    elif stage == "validate":
        result = validate_runtime()
    else:
        result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
