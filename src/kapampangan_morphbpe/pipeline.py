from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from .artifact import export_tokenizer_artifact
from .bpe import BPEModel, ConstrainedBPETrainer
from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION
from .prepare import load_prepared_stream
from .serialization import read_json, sha256_file, write_json


def export_candidate_models(
    models: dict[int, BPEModel],
    candidates_dir: Path,
    *,
    training_report_path: Path,
    grid_path: Path,
    lexicon_manifest_path: Path,
    prepared_manifest_path: Path,
) -> dict[str, object]:
    training_raw = read_json(training_report_path)
    grid_raw = read_json(grid_path)
    lexicon_raw = read_json(lexicon_manifest_path)
    prepared_raw = read_json(prepared_manifest_path)
    for value, label in (
        (training_raw, "training report"),
        (grid_raw, "candidate grid"),
        (lexicon_raw, "lexicon manifest"),
        (prepared_raw, "prepared manifest"),
    ):
        if not isinstance(value, dict):
            raise ValueError(f"{label} must be an object")
    training = cast(dict[str, Any], training_raw)
    grid = cast(dict[str, Any], grid_raw)
    lexicon = cast(dict[str, Any], lexicon_raw)
    prepared = cast(dict[str, Any], prepared_raw)
    manifests: dict[str, object] = {}
    for target, model in sorted(models.items()):
        metadata: dict[str, object] = {
            "candidate": True,
            "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
            "candidate_training_report_fingerprint": training.get("report_fingerprint"),
            "lexicon_fingerprint": lexicon.get("lexicon_fingerprint"),
            "prepared_manifest_fingerprint": prepared.get("manifest_fingerprint"),
            "segmentation_engine": prepared.get("segmentation_engine"),
            "training_records": prepared.get("training_records"),
            "train_sha256": prepared.get("input_train_sha256"),
            "held_out_test_used": False,
        }
        manifest = export_tokenizer_artifact(
            model,
            candidates_dir / f"vocab-{target}",
            metadata=metadata,
        )
        manifests[str(target)] = manifest
    summary: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidate_manifests": manifests,
    }
    write_json(candidates_dir / "candidate-artifacts.json", summary)
    return summary


def _tokenizer_card(target: int) -> str:
    return f"""# Kapampangan MorphBPE Tokenizer Card

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

## Intended use

This is the independently trained, paper-defined Kapampangan source tokenizer
selected at target vocabulary size {target}. It is a technical research artifact
for local tokenizer experiments and a future controlled NLLB-200 source adapter.

## Training data

The tokenizer was trained only on the 26,268-record neutral training split from
`kapampangan-general-corpus-v1`, fingerprint
`{DATASET_FINGERPRINT}`. Validation selected the vocabulary size using provisional
proxy morphology diagnostics. Held-out test text was not used.

## Runtime

Runtime uses NFC normalization, deterministic Unicode pre-tokenization, this
artifact's vocabulary and merge precedence, and character/`<unk>` fallback. It
does not load a lexicon, corpus, morphology reference, or training segmentation.

## Limitations

Morphology resources were not human-validated under the thesis methodology.
Development morphology scores are proxies, not final thesis results. Formal
held-out evaluation and NLLB translation evaluation remain pending.
"""


def finalize_selected_tokenizer(
    prepared_stream_path: Path,
    selection_path: Path,
    selected_dir: Path,
    rebuild_dir: Path,
    *,
    lexicon_manifest_path: Path,
    prepared_manifest_path: Path,
) -> dict[str, object]:
    selection_raw = read_json(selection_path)
    lexicon_raw = read_json(lexicon_manifest_path)
    prepared_raw = read_json(prepared_manifest_path)
    if (
        not isinstance(selection_raw, dict)
        or not isinstance(lexicon_raw, dict)
        or not isinstance(prepared_raw, dict)
    ):
        raise ValueError("selection, lexicon, and prepared manifests must be objects")
    selection = cast(dict[str, Any], selection_raw)
    lexicon = cast(dict[str, Any], lexicon_raw)
    prepared = cast(dict[str, Any], prepared_raw)
    target = selection.get("selected_target_vocabulary_size")
    if not isinstance(target, int):
        raise ValueError("selected target vocabulary size missing")

    prepared_sequences = load_prepared_stream(prepared_stream_path)
    first_models, first_report = ConstrainedBPETrainer(prepared_sequences).train([target])
    second_models, second_report = ConstrainedBPETrainer(prepared_sequences).train([target])
    if target not in first_models or target not in second_models:
        raise ValueError("selected vocabulary target could not be rebuilt")
    if first_models[target].to_dict() != second_models[target].to_dict():
        raise AssertionError("deterministic in-memory model rebuild mismatch")

    metadata: dict[str, object] = {
        "candidate": False,
        "selected_by_validation": True,
        "selection_fingerprint": selection.get("selection_fingerprint"),
        "lexicon_fingerprint": lexicon.get("lexicon_fingerprint"),
        "prepared_manifest_fingerprint": prepared.get("manifest_fingerprint"),
        "segmentation_engine": prepared.get("segmentation_engine"),
        "training_records": prepared.get("training_records"),
        "train_sha256": prepared.get("input_train_sha256"),
        "validation_absorbed_into_training": False,
        "held_out_test_used": False,
    }
    selected_manifest = export_tokenizer_artifact(
        first_models[target],
        selected_dir,
        metadata=metadata,
        tokenizer_card=_tokenizer_card(target),
    )
    rebuild_manifest = export_tokenizer_artifact(
        second_models[target],
        rebuild_dir,
        metadata=metadata,
        tokenizer_card=_tokenizer_card(target),
    )
    selected_files = {
        path.relative_to(selected_dir).as_posix(): sha256_file(path)
        for path in selected_dir.rglob("*")
        if path.is_file()
    }
    rebuild_files = {
        path.relative_to(rebuild_dir).as_posix(): sha256_file(path)
        for path in rebuild_dir.rglob("*")
        if path.is_file()
    }
    deterministic = selected_files == rebuild_files
    if not deterministic:
        raise AssertionError("selected artifact rebuild was not byte-identical")
    report: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "selected_target_vocabulary_size": target,
        "selected_artifact_fingerprint": selected_manifest.get("artifact_fingerprint"),
        "rebuild_artifact_fingerprint": rebuild_manifest.get("artifact_fingerprint"),
        "first_training_report": first_report,
        "second_training_report": second_report,
        "byte_identical_core_and_documentation": deterministic,
        "file_count": len(selected_files),
    }
    write_json(rebuild_dir.parent / "deterministic-rebuild-report.json", report)
    return report
