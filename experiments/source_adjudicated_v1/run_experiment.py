from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any, cast

from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files
from kapampangan_morphbpe.bpe import ConstrainedBPETrainer, train_candidate_models
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION, SPECIAL_TOKENS
from kapampangan_morphbpe.lexicon import load_lexicon
from kapampangan_morphbpe.models import PreparedSequence, PretokenKind, Segmentation
from kapampangan_morphbpe.morphology import MorphologicalSegmenter
from kapampangan_morphbpe.normalization import comparison_key
from kapampangan_morphbpe.pipeline import export_candidate_models
from kapampangan_morphbpe.prepare import freeze_candidate_grid, load_prepared_stream
from kapampangan_morphbpe.pretokenizer import pretokenize
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.rust_bridge import RustMorphologicalSegmenter
from kapampangan_morphbpe.serialization import (
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
POLICY_PATH = EXPERIMENT_ROOT / "adjudication-policy.json"

BASE_LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
BASE_LEXICON_MANIFEST_PATH = REPOSITORY_ROOT / "resources/training-lexicon-manifest.json"
BASE_STREAM_PATH = REPOSITORY_ROOT / "runs/prepared/training-stream.jsonl"
BASE_PREPARED_MANIFEST_PATH = REPOSITORY_ROOT / "runs/prepared/training-stream-manifest.json"
BASE_SELECTION_PATH = REPOSITORY_ROOT / "configs/selected-candidate.json"
CANONICAL_SELECTED_DIR = REPOSITORY_ROOT / "artifacts/selected-tokenizer"

LEXICON_DIR = EXPERIMENT_ROOT / "resources"
LEXICON_PATH = LEXICON_DIR / "training-lexicon.json"
LEXICON_MANIFEST_PATH = LEXICON_DIR / "training-lexicon-manifest.json"
PREPARED_DIR = EXPERIMENT_ROOT / "runs/prepared"
STREAM_PATH = PREPARED_DIR / "training-stream.jsonl"
PREPARED_MANIFEST_PATH = PREPARED_DIR / "training-stream-manifest.json"
CONFIG_DIR = EXPERIMENT_ROOT / "configs"
GRID_PATH = CONFIG_DIR / "candidate-grid.json"
SELECTION_PATH = CONFIG_DIR / "selected-candidate.json"
CANDIDATES_DIR = EXPERIMENT_ROOT / "artifacts/candidates"
SELECTED_DIR = EXPERIMENT_ROOT / "artifacts/selected-tokenizer"
REBUILD_DIR = EXPERIMENT_ROOT / "artifacts/determinism-rebuild"
PLAIN_PREPARED_DIR = EXPERIMENT_ROOT / "runs/plain-bpe"
PLAIN_STREAM_PATH = PLAIN_PREPARED_DIR / "training-stream.jsonl"
PLAIN_MANIFEST_PATH = PLAIN_PREPARED_DIR / "training-stream-manifest.json"
PLAIN_ARTIFACT_DIR = EXPERIMENT_ROOT / "artifacts/plain-bpe-tokenizer"
PLAIN_REBUILD_DIR = EXPERIMENT_ROOT / "artifacts/plain-bpe-determinism-rebuild"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"

SENTENCE = "Bukas na datang ing pangulo."
RICHARDS_IDS = {"ocr-010", "ocr-011", "ocr-012"}
ROOT_OPERATIONS = {"add_provisional_root", "add_exact_provisional_borrowed_root"}


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string")
    return value


def _integer(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _policy() -> dict[str, Any]:
    policy = _object(read_json(POLICY_PATH), "adjudication policy")
    held_raw = policy.get("richards_candidate_ids_held")
    if not isinstance(held_raw, list) or set(held_raw) != RICHARDS_IDS:
        raise ValueError("the policy must hold exactly Richards rows ocr-010 through ocr-012")

    decisions_raw = policy.get("decisions")
    if not isinstance(decisions_raw, list):
        raise ValueError("the policy decision list is missing")
    richards_operations: dict[str, str] = {}
    for raw in decisions_raw:
        decision = _object(raw, "adjudication decision")
        candidate_ids = decision.get("candidate_ids")
        operation = decision.get("operation")
        if not isinstance(candidate_ids, list) or not isinstance(operation, str):
            raise ValueError("an adjudication decision is malformed")
        for candidate_id in candidate_ids:
            if candidate_id in RICHARDS_IDS:
                richards_operations[str(candidate_id)] = operation
    if richards_operations != {item: "hold_richards_evidence" for item in RICHARDS_IDS}:
        raise ValueError("Richards evidence cannot become operational in this experiment")
    return policy


def _verify_base_inputs(policy: dict[str, Any]) -> dict[str, Any]:
    expected = _object(policy.get("base_inputs"), "base input policy")
    base_lexicon = _object(read_json(BASE_LEXICON_PATH), "base lexicon")
    base_lexicon_manifest = _object(read_json(BASE_LEXICON_MANIFEST_PATH), "base lexicon manifest")
    base_prepared_manifest = _object(
        read_json(BASE_PREPARED_MANIFEST_PATH), "base prepared manifest"
    )
    base_selection = _object(read_json(BASE_SELECTION_PATH), "base selection")

    checks = {
        "dataset_fingerprint": base_prepared_manifest.get("dataset_fingerprint"),
        "lexicon_fingerprint": base_lexicon.get("lexicon_fingerprint"),
        "lexicon_sha256": sha256_file(BASE_LEXICON_PATH),
        "prepared_manifest_fingerprint": base_prepared_manifest.get("manifest_fingerprint"),
        "prepared_stream_sha256": sha256_file(BASE_STREAM_PATH),
        "train_sha256": base_prepared_manifest.get("input_train_sha256"),
    }
    for name, actual in checks.items():
        if actual != expected.get(name):
            raise ValueError(
                f"base {name} mismatch: expected {expected.get(name)!r}, got {actual!r}"
            )
    if base_lexicon_manifest.get("lexicon_file_sha256") != checks["lexicon_sha256"]:
        raise ValueError("base lexicon manifest does not match the base lexicon file")
    if base_prepared_manifest.get("lexicon_fingerprint") != checks["lexicon_fingerprint"]:
        raise ValueError("base prepared stream was not built with the expected lexicon")

    selection_policy = _object(policy.get("selection_policy"), "selection policy")
    inherited = selection_policy.get("inherited_canonical_selection_fingerprint")
    if base_selection.get("selection_fingerprint") != inherited:
        raise ValueError("canonical selection fingerprint changed")
    if selection_policy.get("current_validation_re_evaluated") is not False:
        raise ValueError("this experiment must not claim current validation re-evaluation")
    return {
        "base_lexicon": base_lexicon,
        "base_lexicon_manifest": base_lexicon_manifest,
        "base_prepared_manifest": base_prepared_manifest,
        "base_selection": base_selection,
        "checks": checks,
    }


def _word_frequencies(sequences: list[PreparedSequence]) -> Counter[str]:
    frequencies: Counter[str] = Counter()
    for sequence in sequences:
        if sequence.kind == "word":
            frequencies[comparison_key(sequence.surface)] += sequence.frequency
    return frequencies


def _source_record(
    decision: dict[str, Any], *, record_type: str = "local_adjudicated_root"
) -> dict[str, str]:
    candidate_ids = decision.get("candidate_ids")
    sources = decision.get("sources", [])
    if not isinstance(candidate_ids, list) or not isinstance(sources, list):
        raise ValueError("operational adjudication source metadata is malformed")
    form = _string(decision.get("form"), "adjudicated form")
    return {
        "id": "local-adjudication-" + "-".join(str(item) for item in candidate_ids),
        "form": form,
        "type": record_type,
        "description": _string(decision.get("rationale"), "adjudication rationale"),
        "example": SENTENCE if form in {"bukas", "pangulo"} else "",
        "source": ";".join(str(item) for item in sources),
    }


def _build_experimental_lexicon(
    policy: dict[str, Any],
    verified: dict[str, Any],
    frequencies: Counter[str],
) -> dict[str, Any]:
    document = copy.deepcopy(_object(verified["base_lexicon"], "base lexicon"))
    document.pop("lexicon_fingerprint", None)
    roots_raw = document.get("roots")
    variants_raw = document.get("spelling_variants")
    if not isinstance(roots_raw, list) or not isinstance(variants_raw, list):
        raise ValueError("base lexicon inventories are malformed")

    root_keys = {
        _string(_object(item, "root entry").get("comparison_key"), "root comparison key")
        for item in roots_raw
    }
    variant_keys = {
        _string(_object(item, "variant entry").get("comparison_key"), "variant key")
        for item in variants_raw
    }
    decisions_raw = policy.get("decisions")
    if not isinstance(decisions_raw, list):
        raise ValueError("adjudication decisions are missing")

    added_roots: list[str] = []
    added_variants: list[str] = []
    for raw in decisions_raw:
        decision = _object(raw, "adjudication decision")
        operation = _string(decision.get("operation"), "adjudication operation")
        form = _string(decision.get("form"), "adjudicated form")
        key = comparison_key(form)
        if operation in ROOT_OPERATIONS:
            if key in root_keys:
                raise ValueError(f"adjudicated root {form!r} already exists in the base lexicon")
            roots_raw.append(
                {
                    "attested_in_train": frequencies[key] > 0,
                    "canonical_surface": form,
                    "comparison_key": key,
                    "provisional": True,
                    "sources": [_source_record(decision)],
                    "surfaces": [form],
                    "train_frequency": frequencies[key],
                }
            )
            root_keys.add(key)
            added_roots.append(form)
        elif operation == "add_exact_historical_variant":
            canonical = _string(decision.get("canonical_form"), "canonical variant form")
            if comparison_key(canonical) not in root_keys:
                raise ValueError(f"variant host {canonical!r} is not an operational root")
            if key in variant_keys:
                raise ValueError(f"adjudicated variant {form!r} already exists")
            variants_raw.append(
                {
                    "canonical_comparison_key": comparison_key(canonical),
                    "comparison_key": key,
                    "form": form,
                    "mapping_scope": "exact_form_only",
                    "operational": True,
                    "provisional": True,
                    "source": _source_record(
                        decision, record_type="local_adjudicated_historical_variant"
                    ),
                    "train_frequency": frequencies[key],
                }
            )
            variant_keys.add(key)
            added_variants.append(form)

    roots_raw.sort(key=lambda item: _object(item, "root entry")["comparison_key"])
    variants_raw.sort(key=lambda item: _object(item, "variant entry")["comparison_key"])
    document["evidence_status"] = "local_source_adjudicated_experiment_not_canonical"
    construction_policy = _object(document.get("construction_policy"), "construction policy")
    construction_policy.update(
        {
            "local_source_adjudication": True,
            "richards_evidence_operational": False,
            "targeted_historical_variant_only": "bucas->bukas",
        }
    )
    document["local_adjudication"] = {
        "added_roots": added_roots,
        "added_variants": added_variants,
        "policy_file": POLICY_PATH.name,
        "policy_sha256": sha256_file(POLICY_PATH),
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    lexicon_fingerprint = fingerprint(document)
    output_document = {**document, "lexicon_fingerprint": lexicon_fingerprint}
    write_json(LEXICON_PATH, output_document)

    base_manifest = _object(verified["base_lexicon_manifest"], "base lexicon manifest")
    counts = copy.deepcopy(_object(base_manifest.get("counts"), "base lexicon counts"))
    counts["operational_root_keys"] = len(roots_raw)
    counts["operational_root_surfaces"] = sum(
        len(_object(item, "root entry").get("surfaces", [])) for item in roots_raw
    )
    counts["spelling_variant_mappings"] = len(variants_raw)
    input_files = copy.deepcopy(
        _object(base_manifest.get("input_files"), "base lexicon input files")
    )
    input_files.update(
        {
            "adjudication_policy_sha256": sha256_file(POLICY_PATH),
            "base_lexicon_sha256": sha256_file(BASE_LEXICON_PATH),
            "base_prepared_stream_sha256": sha256_file(BASE_STREAM_PATH),
        }
    )
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "evidence_status": "local_source_adjudicated_experiment_not_canonical",
        "lexicon_fingerprint": lexicon_fingerprint,
        "lexicon_file_sha256": sha256_file(LEXICON_PATH),
        "input_files": input_files,
        "counts": counts,
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    manifest = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(LEXICON_MANIFEST_PATH, manifest)
    load_lexicon(LEXICON_PATH)
    return manifest


def _initial_pair_stats(sequences: list[PreparedSequence]) -> tuple[int, int]:
    pair_types: set[tuple[str, str]] = set()
    merge_upper_bound = 0
    for sequence in sequences:
        characters = list(sequence.surface)
        protected = set(sequence.protected_boundaries)
        for position in range(len(characters) - 1):
            if position + 1 in protected:
                continue
            pair_types.add((characters[position], characters[position + 1]))
            merge_upper_bound += 1
    return len(pair_types), merge_upper_bound


def _segmentation_equal(left: Segmentation, right: Segmentation) -> bool:
    return left.to_dict() == right.to_dict()


def _write_sentence_report(segmenter: MorphologicalSegmenter) -> dict[str, Any]:
    normalized, pretokens = pretokenize(SENTENCE)
    rows: list[dict[str, object]] = []
    display: list[str] = []
    for token in pretokens:
        analysis = segmenter.segment(token.surface) if token.kind == "word" else None
        shown = analysis.display if analysis is not None else token.surface
        rows.append(
            {
                "analysis": analysis.to_dict() if analysis is not None else None,
                "display": shown,
                "end": token.end,
                "kind": token.kind,
                "start": token.start,
                "surface": token.surface,
            }
        )
        display.append(shown)
    word_rows = [row for row in rows if row["kind"] == "word"]
    if any(
        _object(row["analysis"], "sentence word analysis").get("status") != "protected_root"
        for row in word_rows
    ):
        raise AssertionError(
            "every word in the diagnostic sentence must be an atomic protected root"
        )
    report: dict[str, Any] = {
        "display": "".join(display),
        "normalized_text": normalized,
        "pretokens": rows,
        "richards_evidence_used": False,
    }
    report["report_fingerprint"] = fingerprint(report)
    write_json(REPORTS_DIR / "sentence-analysis.json", report)
    return report


def _resegment_preserved_stream(
    base_sequences: list[PreparedSequence],
    verified: dict[str, Any],
    lexicon_manifest: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    pretoken_counts: Counter[tuple[str, PretokenKind]] = Counter()
    base_boundaries: dict[tuple[str, PretokenKind], tuple[int, ...]] = {}
    for sequence in base_sequences:
        key = (sequence.surface, sequence.kind)
        pretoken_counts[key] += sequence.frequency
        prior = base_boundaries.setdefault(key, sequence.protected_boundaries)
        if prior != sequence.protected_boundaries:
            raise ValueError(f"base stream has inconsistent boundaries for {key!r}")

    word_surfaces = sorted(surface for surface, kind in pretoken_counts if kind == "word")
    lexicon = load_lexicon(LEXICON_PATH)
    python_segmenter = MorphologicalSegmenter(lexicon)
    rust_segmenter = RustMorphologicalSegmenter(lexicon)
    segmentation_by_surface: dict[str, Segmentation] = {}
    discrepancies: list[dict[str, object]] = []
    batch_size = 10_000
    for offset in range(0, len(word_surfaces), batch_size):
        batch = word_surfaces[offset : offset + batch_size]
        python_results = python_segmenter.segment_many(batch)
        rust_results = rust_segmenter.segment_many(batch)
        for surface, python_result, rust_result in zip(
            batch, python_results, rust_results, strict=True
        ):
            if not _segmentation_equal(python_result, rust_result):
                discrepancies.append(
                    {
                        "python": python_result.to_dict(),
                        "rust": rust_result.to_dict(),
                        "surface": surface,
                    }
                )
            segmentation_by_surface[surface] = rust_result
    if discrepancies:
        report = {
            "discrepancy_count": len(discrepancies),
            "discrepancies": discrepancies[:100],
            "python_rust_equal": False,
            "word_types": len(word_surfaces),
        }
        write_json(REPORTS_DIR / "segmentation-parity.json", report)
        raise AssertionError("Python/Rust morphology parity failed")

    sequence_counts: Counter[tuple[str, tuple[int, ...], PretokenKind]] = Counter()
    status_occurrences: Counter[str] = Counter()
    status_types: Counter[str] = Counter()
    rule_occurrences: Counter[str] = Counter()
    changed: list[dict[str, object]] = []
    word_occurrences = 0
    for (surface, kind), frequency in pretoken_counts.items():
        boundaries: tuple[int, ...] = ()
        if kind == "word":
            segmentation = segmentation_by_surface[surface]
            boundaries = segmentation.protected_boundaries
            status_occurrences[segmentation.status] += frequency
            status_types[segmentation.status] += 1
            if segmentation.rule_id is not None:
                rule_occurrences[segmentation.rule_id] += frequency
            word_occurrences += frequency
            old_boundaries = base_boundaries[(surface, kind)]
            if boundaries != old_boundaries:
                changed.append(
                    {
                        "frequency": frequency,
                        "new_boundaries": list(boundaries),
                        "new_display": segmentation.display,
                        "new_rule_id": segmentation.rule_id,
                        "new_status": segmentation.status,
                        "old_boundaries": list(old_boundaries),
                        "surface": surface,
                    }
                )
        sequence_counts[(surface, boundaries, kind)] += frequency

    sequences = [
        PreparedSequence(surface, boundaries, kind, frequency)
        for (surface, boundaries, kind), frequency in sorted(
            sequence_counts.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])
        )
    ]
    PREPARED_DIR.mkdir(parents=True, exist_ok=True)
    with STREAM_PATH.open("w", encoding="utf-8", newline="\n") as stream:
        for sequence in sequences:
            stream.write(
                stable_compact_json(
                    {
                        "frequency": sequence.frequency,
                        "kind": sequence.kind,
                        "protected_boundaries": list(sequence.protected_boundaries),
                        "surface": sequence.surface,
                    }
                )
                + "\n"
            )

    characters = sorted(
        {character for sequence in sequences for character in sequence.surface},
        key=lambda value: value.encode("utf-8"),
    )
    initial_pair_types, feasible_merge_upper_bound = _initial_pair_stats(sequences)
    analyzed_occurrences = status_occurrences["accepted"]
    ambiguous_occurrences = status_occurrences["ambiguous"]
    base_manifest = _object(verified["base_prepared_manifest"], "base prepared manifest")
    reconstructed_codepoints = sum(
        len(sequence.surface) * sequence.frequency for sequence in sequences
    )
    if reconstructed_codepoints != base_manifest.get("training_codepoints"):
        raise ValueError("preserved stream does not reconstruct the recorded training codepoints")
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "input_train_sha256": base_manifest.get("input_train_sha256"),
        "lexicon_fingerprint": lexicon_manifest["lexicon_fingerprint"],
        "segmentation_engine": "rust_verified_against_python_preserved_aggregate",
        "training_records": base_manifest.get("training_records"),
        "training_codepoints": reconstructed_codepoints,
        "pretoken_occurrences": sum(pretoken_counts.values()),
        "unique_prepared_sequences": len(sequences),
        "word_occurrences": word_occurrences,
        "word_types": len(word_surfaces),
        "character_inventory": characters,
        "character_inventory_size": len(characters),
        "special_token_count": len(SPECIAL_TOKENS),
        "initial_vocabulary_size": len(characters) + len(SPECIAL_TOKENS),
        "initial_permitted_pair_types": initial_pair_types,
        "feasible_merge_upper_bound": feasible_merge_upper_bound,
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "status_types": dict(sorted(status_types.items())),
        "rule_occurrences": dict(sorted(rule_occurrences.items())),
        "segmentation_coverage": (
            analyzed_occurrences / word_occurrences if word_occurrences else 0.0
        ),
        "ambiguous_unchanged_occurrences": ambiguous_occurrences,
        "stream_file": STREAM_PATH.name,
        "stream_sha256": sha256_file(STREAM_PATH),
        "reconstruction": {
            "base_prepared_manifest_fingerprint": base_manifest.get("manifest_fingerprint"),
            "base_stream_sha256": sha256_file(BASE_STREAM_PATH),
            "method": "resegment_all_preserved_aggregate_word_types_keep_exact_frequencies",
            "sentence_order_reconstructed": False,
            "raw_train_csv_available": False,
            "raw_validation_csv_available": False,
        },
    }
    manifest = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(PREPARED_MANIFEST_PATH, manifest)

    changed.sort(key=lambda item: (-_integer(item["frequency"], "frequency"), item["surface"]))
    parity_report: dict[str, Any] = {
        "base_boundary_changed_occurrences": sum(
            _integer(item["frequency"], "changed frequency") for item in changed
        ),
        "base_boundary_changed_types": len(changed),
        "changed_types": changed,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "discrepancy_count": 0,
        "lexicon_fingerprint": lexicon_manifest["lexicon_fingerprint"],
        "python_rust_equal": True,
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
        "word_types": len(word_surfaces),
    }
    parity_report["report_fingerprint"] = fingerprint(parity_report)
    write_json(REPORTS_DIR / "segmentation-parity.json", parity_report)
    _write_sentence_report(python_segmenter)
    return manifest, parity_report


def prepare_stage() -> dict[str, Any]:
    policy = _policy()
    verified = _verify_base_inputs(policy)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    LEXICON_DIR.mkdir(parents=True, exist_ok=True)
    base_sequences = load_prepared_stream(BASE_STREAM_PATH)
    lexicon_manifest = _build_experimental_lexicon(
        policy, verified, _word_frequencies(base_sequences)
    )
    prepared_manifest, parity_report = _resegment_preserved_stream(
        base_sequences, verified, lexicon_manifest
    )
    grid = freeze_candidate_grid(PREPARED_MANIFEST_PATH, GRID_PATH)
    selection_policy = _object(policy.get("selection_policy"), "selection policy")
    expected_targets = selection_policy.get("candidate_vocabulary_sizes")
    if grid.get("candidate_vocabulary_sizes") != expected_targets:
        raise ValueError("reconstructed stream changed the frozen candidate sizes")
    summary: dict[str, Any] = {
        "candidate_vocabulary_sizes": expected_targets,
        "lexicon_fingerprint": lexicon_manifest["lexicon_fingerprint"],
        "prepared_manifest_fingerprint": prepared_manifest["manifest_fingerprint"],
        "python_rust_equal": parity_report["python_rust_equal"],
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
        "stage": "prepare",
        "stream_sha256": prepared_manifest["stream_sha256"],
    }
    summary["report_fingerprint"] = fingerprint(summary)
    write_json(REPORTS_DIR / "prepare-summary.json", summary)
    return summary


def train_stage() -> dict[str, Any]:
    policy = _policy()
    _verify_base_inputs(policy)
    if not all(
        path.is_file()
        for path in (LEXICON_MANIFEST_PATH, PREPARED_MANIFEST_PATH, STREAM_PATH, GRID_PATH)
    ):
        raise FileNotFoundError("run the prepare stage before training")
    models, training_report = train_candidate_models(
        STREAM_PATH, PREPARED_MANIFEST_PATH, GRID_PATH, CANDIDATES_DIR
    )
    artifacts = export_candidate_models(
        models,
        CANDIDATES_DIR,
        training_report_path=CANDIDATES_DIR / "candidate-training-report.json",
        grid_path=GRID_PATH,
        lexicon_manifest_path=LEXICON_MANIFEST_PATH,
        prepared_manifest_path=PREPARED_MANIFEST_PATH,
    )
    family = _object(training_report.get("family_training"), "family training report")
    targets = _object(policy.get("selection_policy"), "selection policy").get(
        "candidate_vocabulary_sizes"
    )
    if family.get("trained_targets") != targets or family.get("failed_targets") != []:
        raise AssertionError("not every frozen candidate target was trained")
    if family.get("protected_boundary_merge_violations") != 0:
        raise AssertionError("candidate training crossed a protected boundary")

    selection_policy = _object(policy.get("selection_policy"), "selection policy")
    selected_target = _integer(
        selection_policy.get("selected_target_vocabulary_size"), "selected target"
    )
    candidate_manifests = _object(
        artifacts.get("candidate_manifests"), "candidate artifact manifests"
    )
    selected_candidate = _object(
        candidate_manifests.get(str(selected_target)), "selected candidate manifest"
    )
    grid = _object(read_json(GRID_PATH), "candidate grid")
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "current_validation_re_evaluated": False,
        "held_out_test_used": False,
        "inherited_canonical_selection_fingerprint": selection_policy.get(
            "inherited_canonical_selection_fingerprint"
        ),
        "selected_artifact_fingerprint": selected_candidate.get("artifact_fingerprint"),
        "selected_by_validation": False,
        "selected_target_vocabulary_size": selected_target,
        "selection_reason": selection_policy.get("strategy"),
        "warning": (
            "No new validation metric is claimed because the raw validation split is absent."
        ),
    }
    selection = {**body, "selection_fingerprint": fingerprint(body)}
    write_json(SELECTION_PATH, selection)
    summary: dict[str, Any] = {
        "candidate_artifacts": {
            target: _object(manifest, "candidate manifest").get("artifact_fingerprint")
            for target, manifest in candidate_manifests.items()
        },
        "family_training": family,
        "selected_target_vocabulary_size": selected_target,
        "selection_fingerprint": selection["selection_fingerprint"],
        "stage": "train",
    }
    summary["report_fingerprint"] = fingerprint(summary)
    write_json(REPORTS_DIR / "training-summary.json", summary)
    return summary


def _tokenizer_card(target: int) -> str:
    return f"""# Kapampangan MorphBPE local source-adjudicated tokenizer

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This isolated local-test artifact uses the source-adjudicated experimental
lexicon and a reconstructed BPE input made by resegmenting every word type in
the hash-verified canonical aggregate training stream. It does not replace the
canonical tokenizer.

Vocabulary size {target} is inherited from the canonical precommitted selection.
The unavailable raw validation split was not reconstructed or re-evaluated, so
this artifact makes no new validation-performance claim. Richards-derived
evidence rows ocr-010 through ocr-012 were held and had no operational effect.

Runtime uses only NFC normalization, deterministic Unicode pre-tokenization,
the exported vocabulary, and learned merge precedence. Morphological analysis
requires the separate experimental lexicon and is not performed by the runtime
tokenizer.
"""


def _file_hashes(directory: Path) -> dict[str, str]:
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in directory.rglob("*")
        if path.is_file()
    }


def finalize_stage() -> dict[str, Any]:
    policy = _policy()
    _verify_base_inputs(policy)
    if not all(
        path.is_file()
        for path in (LEXICON_MANIFEST_PATH, PREPARED_MANIFEST_PATH, STREAM_PATH, SELECTION_PATH)
    ):
        raise FileNotFoundError("run the prepare and train stages before finalization")
    selection = _object(read_json(SELECTION_PATH), "experimental selection")
    selected_target = _integer(selection.get("selected_target_vocabulary_size"), "selected target")
    prepared_sequences = load_prepared_stream(STREAM_PATH)
    first_models, first_report = ConstrainedBPETrainer(prepared_sequences).train([selected_target])
    second_models, second_report = ConstrainedBPETrainer(prepared_sequences).train(
        [selected_target]
    )
    first_model = first_models.get(selected_target)
    second_model = second_models.get(selected_target)
    if first_model is None or second_model is None:
        raise AssertionError("selected target could not be rebuilt")
    if first_model.to_dict() != second_model.to_dict():
        raise AssertionError("two independent selected-model rebuilds differ")

    lexicon_manifest = _object(read_json(LEXICON_MANIFEST_PATH), "lexicon manifest")
    prepared_manifest = _object(read_json(PREPARED_MANIFEST_PATH), "prepared manifest")
    metadata: dict[str, object] = {
        "candidate": False,
        "current_validation_re_evaluated": False,
        "held_out_test_used": False,
        "lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "reconstructed_from_verified_aggregate_stream": True,
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
        "selected_by_validation": False,
        "selection_fingerprint": selection.get("selection_fingerprint"),
        "selection_strategy": selection.get("selection_reason"),
        "segmentation_engine": prepared_manifest.get("segmentation_engine"),
        "train_sha256": prepared_manifest.get("input_train_sha256"),
        "training_records": prepared_manifest.get("training_records"),
    }
    selected_manifest = export_tokenizer_artifact(
        first_model,
        SELECTED_DIR,
        metadata=metadata,
        tokenizer_card=_tokenizer_card(selected_target),
    )
    rebuild_manifest = export_tokenizer_artifact(
        second_model,
        REBUILD_DIR,
        metadata=metadata,
        tokenizer_card=_tokenizer_card(selected_target),
    )
    selected_files = _file_hashes(SELECTED_DIR)
    rebuild_files = _file_hashes(REBUILD_DIR)
    if selected_files != rebuild_files:
        raise AssertionError("selected and deterministic rebuild directories differ")

    candidate_manifest = _object(
        read_json(CANDIDATES_DIR / f"vocab-{selected_target}/tokenizer-manifest.json"),
        "selected candidate manifest",
    )
    selected_core = _object(selected_manifest.get("core_file_sha256"), "final core hashes")
    candidate_core = _object(candidate_manifest.get("core_file_sha256"), "candidate core hashes")
    model_files = {
        "merges.json",
        "normalization.json",
        "pretokenizer.json",
        "special_tokens.json",
        "vocab.json",
    }
    if any(selected_core.get(name) != candidate_core.get(name) for name in model_files):
        raise AssertionError("final model files differ from the retrained family candidate")
    selected_validation = validate_artifact_files(SELECTED_DIR)
    rebuild_validation = validate_artifact_files(REBUILD_DIR)
    tokenizer = load_runtime_tokenizer(SELECTED_DIR)
    encoding = tokenizer.encode(SENTENCE)
    decoded = tokenizer.decode(encoding.ids)
    if decoded != SENTENCE:
        raise AssertionError("runtime round trip changed the diagnostic sentence")

    report_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "byte_identical_selected_and_rebuild": True,
        "candidate_model_files_match_final": True,
        "current_validation_re_evaluated": False,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "decoded_sentence": decoded,
        "file_count": len(selected_files),
        "first_training_report": first_report,
        "rebuild_artifact_fingerprint": rebuild_manifest.get("artifact_fingerprint"),
        "rebuild_validation": rebuild_validation,
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
        "second_training_report": second_report,
        "selected_artifact_fingerprint": selected_manifest.get("artifact_fingerprint"),
        "selected_target_vocabulary_size": selected_target,
        "selected_validation": selected_validation,
        "token_count_for_diagnostic_sentence": len(encoding.tokens),
    }
    report = {**report_body, "report_fingerprint": fingerprint(report_body)}
    write_json(REPORTS_DIR / "finalization-report.json", report)
    return cast(dict[str, Any], report)


def _plain_bpe_card(target: int) -> str:
    return f"""# Kapampangan plain-BPE local control tokenizer

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This isolated local-test control uses the same preserved training surfaces,
frequencies, pre-tokenizer, special tokens, character inventory, deterministic
BPE trainer, and target vocabulary size ({target}) as both the original and
source-adjudicated MorphBPE artifacts. Their surface/kind/frequency streams are
identical after boundaries are cleared. The plain control's sole training
difference is removal of every protected morphology boundary before BPE
learning.

This is a tokenizer control, not a morphology analyzer. Its subword pieces must
not be interpreted as gold morphemes. The unavailable raw validation split was
not reconstructed or re-evaluated.
"""


def _plain_training_stream(
    source_sequences: list[PreparedSequence], selected_target: int
) -> tuple[list[PreparedSequence], dict[str, Any]]:
    counts = _surface_kind_frequencies(source_sequences)
    protected_types = 0
    protected_occurrences = 0
    protected_positions = 0
    for sequence in source_sequences:
        if sequence.protected_boundaries:
            protected_types += 1
            protected_occurrences += sequence.frequency
            protected_positions += len(sequence.protected_boundaries) * sequence.frequency
    plain_sequences = [
        PreparedSequence(surface, (), kind, frequency)
        for (surface, kind), frequency in sorted(counts.items())
    ]
    PLAIN_PREPARED_DIR.mkdir(parents=True, exist_ok=True)
    with PLAIN_STREAM_PATH.open("w", encoding="utf-8", newline="\n") as stream:
        for sequence in plain_sequences:
            stream.write(
                stable_compact_json(
                    {
                        "frequency": sequence.frequency,
                        "kind": sequence.kind,
                        "protected_boundaries": [],
                        "surface": sequence.surface,
                    }
                )
                + "\n"
            )
    source_manifest = _object(read_json(PREPARED_MANIFEST_PATH), "MorphBPE manifest")
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "tokenizer_condition": "plain_bpe",
        "comparison_target_vocabulary_size": selected_target,
        "source_prepared_manifest_fingerprint": source_manifest.get("manifest_fingerprint"),
        "source_stream_sha256": source_manifest.get("stream_sha256"),
        "stream_sha256": sha256_file(PLAIN_STREAM_PATH),
        "unique_prepared_sequences": len(plain_sequences),
        "pretoken_occurrences": sum(sequence.frequency for sequence in plain_sequences),
        "word_types": source_manifest.get("word_types"),
        "character_inventory_size": source_manifest.get("character_inventory_size"),
        "protected_boundary_types_cleared": protected_types,
        "protected_boundary_occurrences_cleared": protected_occurrences,
        "protected_boundary_positions_cleared": protected_positions,
        "surface_kind_frequencies_preserved": True,
        "only_training_difference": "all_protected_morphology_boundaries_cleared",
        "raw_validation_csv_available": False,
    }
    manifest = {**body, "manifest_fingerprint": fingerprint(body)}
    write_json(PLAIN_MANIFEST_PATH, manifest)
    return plain_sequences, cast(dict[str, Any], manifest)


def _surface_kind_frequencies(
    sequences: list[PreparedSequence],
) -> Counter[tuple[str, PretokenKind]]:
    counts: Counter[tuple[str, PretokenKind]] = Counter()
    for sequence in sequences:
        counts[(sequence.surface, sequence.kind)] += sequence.frequency
    return counts


def plain_bpe_stage() -> dict[str, Any]:
    policy = _policy()
    verified = _verify_base_inputs(policy)
    if not all(
        path.is_file()
        for path in (
            STREAM_PATH,
            PREPARED_MANIFEST_PATH,
            SELECTION_PATH,
            SELECTED_DIR / "tokenizer-manifest.json",
        )
    ):
        raise FileNotFoundError("run the prepare, train, and finalize stages first")
    selection = _object(read_json(SELECTION_PATH), "experimental selection")
    selected_target = _integer(selection.get("selected_target_vocabulary_size"), "selected target")
    morph_manifest = _object(
        read_json(SELECTED_DIR / "tokenizer-manifest.json"), "MorphBPE manifest"
    )
    canonical_morph_manifest = _object(
        read_json(CANONICAL_SELECTED_DIR / "tokenizer-manifest.json"),
        "canonical MorphBPE manifest",
    )
    if morph_manifest.get("actual_vocabulary_size") != selected_target:
        raise ValueError("MorphBPE artifact does not match the selected target")
    if canonical_morph_manifest.get("actual_vocabulary_size") != selected_target:
        raise ValueError("canonical MorphBPE artifact does not match the selected target")

    source_sequences = load_prepared_stream(STREAM_PATH)
    canonical_sequences = load_prepared_stream(BASE_STREAM_PATH)
    if _surface_kind_frequencies(source_sequences) != _surface_kind_frequencies(
        canonical_sequences
    ):
        raise AssertionError(
            "original and source-adjudicated streams differ beyond morphology boundaries"
        )
    plain_sequences, plain_stream_manifest = _plain_training_stream(
        source_sequences, selected_target
    )
    first_models, first_training = ConstrainedBPETrainer(plain_sequences).train([selected_target])
    second_models, second_training = ConstrainedBPETrainer(plain_sequences).train([selected_target])
    first_model = first_models.get(selected_target)
    second_model = second_models.get(selected_target)
    if first_model is None or second_model is None:
        raise AssertionError("plain-BPE target could not be trained")
    if first_model.to_dict() != second_model.to_dict():
        raise AssertionError("two independent plain-BPE builds differ")
    if first_model.protected_boundary_merge_violations != 0:
        raise AssertionError(
            "plain-BPE trainer reported an impossible protected-boundary violation"
        )

    metadata: dict[str, object] = {
        "candidate": False,
        "comparison_morphbpe_artifact_fingerprints": {
            "original_canonical": canonical_morph_manifest.get("artifact_fingerprint"),
            "source_adjudicated": morph_manifest.get("artifact_fingerprint"),
        },
        "canonical_prepared_manifest_fingerprint": _object(
            verified["base_prepared_manifest"], "canonical prepared manifest"
        ).get("manifest_fingerprint"),
        "current_validation_re_evaluated": False,
        "held_out_test_used": False,
        "morphology_boundaries_used": False,
        "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
        "same_character_inventory": True,
        "same_original_and_adjudicated_surface_kind_frequencies": True,
        "same_pretokenizer": True,
        "same_special_tokens": True,
        "same_surface_kind_frequencies": True,
        "same_target_vocabulary_size": True,
        "tokenizer_condition": "plain_bpe",
        "train_sha256": _object(read_json(PREPARED_MANIFEST_PATH), "prepared manifest").get(
            "input_train_sha256"
        ),
    }
    plain_manifest = export_tokenizer_artifact(
        first_model,
        PLAIN_ARTIFACT_DIR,
        artifact_type="kapampangan_plain_bpe",
        metadata=metadata,
        tokenizer_card=_plain_bpe_card(selected_target),
    )
    export_tokenizer_artifact(
        second_model,
        PLAIN_REBUILD_DIR,
        artifact_type="kapampangan_plain_bpe",
        metadata=metadata,
        tokenizer_card=_plain_bpe_card(selected_target),
    )
    if _file_hashes(PLAIN_ARTIFACT_DIR) != _file_hashes(PLAIN_REBUILD_DIR):
        raise AssertionError("plain-BPE artifact and deterministic rebuild differ")
    validation = validate_artifact_files(PLAIN_ARTIFACT_DIR)
    tokenizer = load_runtime_tokenizer(PLAIN_ARTIFACT_DIR)
    encoding = tokenizer.encode(SENTENCE)
    if tokenizer.decode(encoding.ids) != SENTENCE:
        raise AssertionError("plain-BPE runtime round trip changed the diagnostic sentence")

    morph_core = _object(morph_manifest.get("core_file_sha256"), "MorphBPE core hashes")
    canonical_morph_core = _object(
        canonical_morph_manifest.get("core_file_sha256"),
        "canonical MorphBPE core hashes",
    )
    plain_core = _object(plain_manifest.get("core_file_sha256"), "plain-BPE core hashes")
    report_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "artifact_fingerprint": plain_manifest.get("artifact_fingerprint"),
        "artifact_type": plain_manifest.get("artifact_type"),
        "byte_identical_rebuild": True,
        "current_validation_re_evaluated": False,
        "first_training_report": first_training,
        "merge_file_differs_from_source_adjudicated_morphbpe": (
            plain_core.get("merges.json") != morph_core.get("merges.json")
        ),
        "merge_file_differs_from_original_morphbpe": (
            plain_core.get("merges.json") != canonical_morph_core.get("merges.json")
        ),
        "morphbpe_artifact_fingerprints": {
            "original_canonical": canonical_morph_manifest.get("artifact_fingerprint"),
            "source_adjudicated": morph_manifest.get("artifact_fingerprint"),
        },
        "original_and_adjudicated_surface_kind_frequencies_match": True,
        "plain_stream_manifest_fingerprint": plain_stream_manifest.get("manifest_fingerprint"),
        "runtime_validation": validation,
        "second_training_report": second_training,
        "selected_target_vocabulary_size": selected_target,
        "tokenizer_condition": "plain_bpe",
    }
    report = {**report_body, "report_fingerprint": fingerprint(report_body)}
    write_json(REPORTS_DIR / "plain-bpe-baseline.json", report)
    return cast(dict[str, Any], report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "train", "finalize", "plain-bpe", "all"))
    args = parser.parse_args()
    results: dict[str, Any] = {}
    if args.stage in {"prepare", "all"}:
        results["prepare"] = prepare_stage()
    if args.stage in {"train", "all"}:
        results["train"] = train_stage()
    if args.stage in {"finalize", "all"}:
        results["finalize"] = finalize_stage()
    if args.stage in {"plain-bpe", "all"}:
        results["plain_bpe"] = plain_bpe_stage()
    print(json.dumps(results, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
