"""Identity and data checks for matched infix-first adaptation notebooks.

The CSV policy follows the supplied matched source-embedding notebook. The
installed Plain30 CSV hash, audit, and ordered split IDs provide additional
locks. The matched recipe permits at most 30 epochs; preparing a notebook is
not evidence of completed training. No rows are deduplicated and evaluation
rows are never moved or removed. Torch is not imported by this module.
"""

import csv
import hashlib
import io
import json
import math
import unicodedata
import zipfile
from collections import Counter
from pathlib import Path


SPLITS = ("train", "validation", "test")
DATA_POLICY = "exclude training source overlap with evaluation; preserve evaluation"
REQUIRED_FIELDS = ("id", "source", "target", "split", "group_id")
AUDIT_LOCKS = (
    "csv_sha256",
    "original_counts",
    "used_counts",
    "excluded_train_ids",
    "policy",
    "within_split_duplicate_excess",
)


def normalize(text):
    """Normalize only comparison keys; preserve the actual CSV training text."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def _metadata(value, name):
    if isinstance(value, (str, Path)):
        value = json.loads(Path(value).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object or a path to one")
    return value


def _duplicate_excess(rows):
    counts = Counter(normalize(row["source"]).casefold() for row in rows)
    return sum(count - 1 for count in counts.values())


def read_matched_csv(path, expected_sha, expected_audit, expected_split_manifest):
    """Return ``(splits, audit)`` after checking the installed Plain30 data locks.

    ``expected_audit`` and ``expected_split_manifest`` accept dictionaries or JSON
    paths. Returned source/target strings are unchanged, matching the supplied
    original CSV loader. ``raw_source`` and ``raw_target`` are explicit aliases
    for evaluations needing the original references. Only overlap and duplicate
    comparison keys use NFC, whitespace normalization, and case folding.
    Group leakage is checked before training overlap exclusion, and duplicate
    excess is counted afterward, as in the original loader. Within-split
    duplicates retain their original order and IDs.
    """
    expected_audit = _metadata(expected_audit, "expected_audit")
    expected_ids = _metadata(expected_split_manifest, "expected_split_manifest")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise ValueError("expected_sha must be a SHA-256 hex digest")
    try:
        int(expected_sha, 16)
    except ValueError as error:
        raise ValueError("expected_sha must be a SHA-256 hex digest") from error
    expected_sha = expected_sha.lower()
    if set(expected_ids) != set(SPLITS):
        raise ValueError("Expected split manifest must contain train, validation, test")
    for split in SPLITS:
        values = expected_ids[split]
        if not isinstance(values, list) or any(not isinstance(i, str) for i in values):
            raise ValueError(f"Expected split IDs must be a list of strings: {split}")
    for field in AUDIT_LOCKS:
        if field not in expected_audit:
            raise ValueError(f"Baseline data audit is missing {field}")
    if expected_audit["csv_sha256"] != expected_sha:
        raise ValueError("Expected CSV digest and baseline audit disagree")
    if expected_audit["policy"] != DATA_POLICY:
        raise ValueError("Unsupported baseline data policy")

    raw = Path(path).read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        raise ValueError("CSV SHA-256 differs from the installed Plain30 baseline")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
    if reader.fieldnames is None or not set(REQUIRED_FIELDS).issubset(reader.fieldnames):
        raise ValueError("CSV requires id, source, target, split, group_id columns")
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError("Duplicate CSV column names")
    original = {split: [] for split in SPLITS}
    seen_ids = set()
    group_splits = {}
    for line, record in enumerate(reader, start=2):
        if None in record:
            raise ValueError(f"Unexpected extra CSV fields at line {line}")
        for field in REQUIRED_FIELDS:
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f"Missing/non-string {field} at CSV line {line}")
        split = record["split"]
        if split not in original:
            raise ValueError(f"Invalid split {split!r} at CSV line {line}")
        if record["id"] in seen_ids:
            raise ValueError(f"Duplicate record ID: {record['id']}")
        seen_ids.add(record["id"])
        group = record["group_id"]
        if group in group_splits and group_splits[group] != split:
            raise ValueError(f"Document/group leakage across original splits: {group}")
        group_splits[group] = split
        row = dict(record)
        row["raw_source"], row["raw_target"] = row["source"], row["target"]
        original[split].append(row)
    if any(not original[split] for split in SPLITS):
        raise ValueError("Every original split must contain at least one row")

    evaluation_sources = {
        normalize(row["source"]).casefold()
        for split in ("validation", "test")
        for row in original[split]
    }
    excluded_ids = [
        row["id"] for row in original["train"]
        if normalize(row["source"]).casefold() in evaluation_sources
    ]
    excluded_set = set(excluded_ids)
    splits = {
        "train": [row for row in original["train"] if row["id"] not in excluded_set],
        "validation": original["validation"],
        "test": original["test"],
    }
    if not splits["train"]:
        raise ValueError("Training split is empty after the recorded overlap policy")

    # Detect leakage rather than changing fixed evaluation partitions to hide it.
    validation_sources = {normalize(row["source"]).casefold() for row in splits["validation"]}
    test_sources = {normalize(row["source"]).casefold() for row in splits["test"]}
    if validation_sources & test_sources:
        raise ValueError("Normalized source overlap between validation and test")

    audit = {
        "csv_sha256": actual_sha,
        "original_counts": {split: len(original[split]) for split in SPLITS},
        "used_counts": {split: len(splits[split]) for split in SPLITS},
        "excluded_train_ids": excluded_ids,
        "policy": DATA_POLICY,
        "within_split_duplicate_excess": {
            split: _duplicate_excess(splits[split]) for split in SPLITS
        },
        "tokenizer_corpus_vs_translation_test": expected_audit.get(
            "tokenizer_corpus_vs_translation_test",
            "Unverified: original tokenizer training corpus required",
        ),
        "policy_provenance": "Supplied matched source-embedding notebook CSV policy; installed Plain30 audit and ordered split IDs verified",
        "original_notebook_training_evidence": "Matched recipe allows up to 30 epochs; notebook preparation does not establish completed training",
        "text_normalization": "Source and target CSV strings preserved; comparison keys alone are normalized",
        "overlap_key": "NFC and collapsed whitespace, then casefold",
        "duplicate_count_scope": "used splits after training overlap exclusion; duplicates preserved",
        "validation_test_source_overlap": 0,
        "cross_split_group_overlap": 0,
    }
    for field in AUDIT_LOCKS:
        if audit[field] != expected_audit[field]:
            raise ValueError(f"Baseline data audit mismatch: {field}")
    for split in SPLITS:
        if [row["id"] for row in splits[split]] != expected_ids[split]:
            raise ValueError(f"Ordered split IDs differ from Plain30 baseline: {split}")
    return splits, audit


SUPPORTED_PENALTIES = (16, 48)
VARIANT_FIELDS = (
    "tokenizer_variant", "crossing_penalty", "weighted_penalty_used",
    "infix_priority_used", "priority_order", "tokenizer_training_algorithm",
    "infix_token_budget", "root_token_budget", "affix_token_budget",
    "infixes_have_separate_training_role",
)
RUNTIME_IDENTITY_FILES = {
    "source_artifact/tokenizer.json": "tokenizer_sha256",
    "source_artifact/tokenizer-manifest.json": "artifact_manifest_sha256",
    "nllb_source_adapter.py": "helper_sha256",
    "runtime/kapampangan_morphbpe_runtime/tokenizer.py": "runtime_sha256",
    "training_support.py": "training_support_sha256",
    "evaluation_support.py": "evaluation_support_sha256",
    "target_tokenizer/tokenizer.json": "target_tokenizer_sha256",
    "split_manifest.json": "split_manifest_sha256",
}


def variant_fields(penalty):
    """Return new independent metadata for an authorized infix-first variant."""
    if isinstance(penalty, bool) or not isinstance(penalty, int) or penalty not in SUPPORTED_PENALTIES:
        raise ValueError("Supported infix-first penalties are 16 and 48")
    return {
        "tokenizer_variant": f"infix_first_penalty{penalty}",
        "crossing_penalty": penalty,
        "weighted_penalty_used": True,
        "infix_priority_used": True,
        "priority_order": ["infix", "weighted"],
        "tokenizer_training_algorithm": "infix_priority_then_weighted",
        "infix_token_budget": 32,
        "root_token_budget": 0,
        "affix_token_budget": 0,
        "infixes_have_separate_training_role": True,
    }


def _require_fields(actual, expected, label):
    if not isinstance(actual, dict):
        raise ValueError(f"{label} must be a dictionary")
    for key, value in expected.items():
        if actual.get(key) != value or (isinstance(value, bool) and actual.get(key) is not value):
            raise ValueError(f"{label} mismatch: {key}")


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _check_sha(value, label):
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"Invalid SHA-256 identity: {label}")
    try:
        int(value, 16)
    except ValueError as error:
        raise ValueError(f"Invalid SHA-256 identity: {label}") from error


def identity_digest(identity):
    """Bind a reload report to every identity field, including runtime controls."""
    return hashlib.sha256(
        json.dumps(identity, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def validate_variant_artifact(artifact_manifest, tokenizer_document, expected_penalty,
                              expected_fingerprint):
    """Check actual infix scheduling and penalty before adapting source weights."""
    artifact_manifest = _metadata(artifact_manifest, "artifact_manifest")
    tokenizer_document = _metadata(tokenizer_document, "tokenizer_document")
    _check_sha(expected_fingerprint, "tokenizer fingerprint")
    fields = variant_fields(expected_penalty)
    _require_fields(artifact_manifest, {
        "artifact_fingerprint": expected_fingerprint,
        "actual_vocabulary_size": 6080,
        "target_vocabulary_size": 6080,
        "merge_count": 4488,
        "artifact_type": "kapampangan_morphbpe",
        "protected_boundary_merge_violations": 0,
    }, "Tokenizer manifest")
    expected_metadata = {
        key: fields[key] for key in (
            "crossing_penalty", "priority_order", "infix_token_budget",
            "root_token_budget", "affix_token_budget", "infixes_have_separate_training_role",
        )
    }
    expected_metadata.update({
        "algorithm": fields["tokenizer_training_algorithm"],
        "vocabulary_budget": 6080,
        "lexicon_used_at_runtime": False,
        "surface_specific_overrides": [],
    })
    for label, document in (("Tokenizer manifest", artifact_manifest),
                            ("Tokenizer JSON", tokenizer_document)):
        _require_fields(document.get("metadata"), expected_metadata, label + " metadata")
    vocabulary = tokenizer_document.get("vocabulary")
    merges = tokenizer_document.get("merges")
    if (not isinstance(vocabulary, list) or len(vocabulary) != 6080 or
            not isinstance(merges, list) or len(merges) != 4488):
        raise ValueError("Tokenizer vocabulary or merge count mismatch")
    if any(entry.get("id") != index for index, entry in enumerate(vocabulary)):
        raise ValueError("Tokenizer vocabulary IDs are not ordered and contiguous")
    if any(entry.get("rank") != index for index, entry in enumerate(merges)):
        raise ValueError("Tokenizer merge ranks are not ordered and contiguous")
    if [entry.get("result") for entry in merges[:4]] != ["in", "um", "IN", "UM"]:
        raise ValueError("Tokenizer does not prioritize the recorded infix inventory")
    return fields


def validate_variant_identity(identity):
    """Require application-compatible routing and exact research variant fields."""
    if not isinstance(identity, dict):
        raise ValueError("Run identity must be a dictionary")
    fields = variant_fields(identity.get("crossing_penalty"))
    _require_fields(identity, {"condition": "morph_bpe", **fields}, "Run identity")
    _check_sha(identity.get("tokenizer_fingerprint"), "tokenizer_fingerprint")
    for key in RUNTIME_IDENTITY_FILES.values():
        _check_sha(identity.get(key), key)
    return fields


def validate_saved_manifest(info, identity, cfg):
    """Reject a resume, reload or export belonging to another exact run."""
    info = _metadata(info, "saved manifest")
    fields = validate_variant_identity(identity)
    if info.get("identity") != identity or info.get("cfg") != cfg:
        raise ValueError("Saved bundle identity/configuration mismatch")
    _require_fields(info, {
        **fields,
        "model_id": identity["model_id"], "revision": identity["revision"],
        "source_vocab_size": 6080, "source_format": "kapampangan_project",
        "source_id_mapping": "swap_0_1", "adaptation": "source_embedding_only",
        "target_language": "tgl_Latn", "source_marker": "<s>",
    }, "Saved manifest")
    if info.get("training_status") not in ("prepared", "completed"):
        raise ValueError("Saved manifest has unsupported training status")
    if info["training_status"] == "completed":
        completed = info.get("completed_epochs")
        selected = info.get("selected_epoch")
        loss = info.get("selected_validation_loss")
        if (isinstance(completed, bool) or not isinstance(completed, int) or
                isinstance(selected, bool) or not isinstance(selected, int) or
                not 1 <= selected <= completed <= cfg["epochs"] or
                isinstance(loss, bool) or not isinstance(loss, (int, float)) or
                not math.isfinite(loss)):
            raise ValueError("Saved completed manifest has invalid epoch/selection metadata")
    return fields


def validate_runtime_files(bundle_root, identity):
    """Verify tokenizer, helper, runtime, target, support and ordered split bytes."""
    validate_variant_identity(identity)
    root = Path(bundle_root).resolve()
    for name, key in RUNTIME_IDENTITY_FILES.items():
        path = root / name
        if not path.is_file() or _digest(path) != identity[key]:
            raise ValueError("Bundle identity mismatch: " + name)
    artifact = root / "source_artifact"
    artifact_manifest = _metadata(artifact / "tokenizer-manifest.json", "artifact manifest")
    validate_variant_artifact(
        artifact_manifest, artifact / "tokenizer.json",
        identity["crossing_penalty"], identity["tokenizer_fingerprint"],
    )
    core_files = artifact_manifest.get("core_file_sha256")
    if not isinstance(core_files, dict) or set(core_files) != {
        "tokenizer.json", "vocab.json", "merges.json", "normalization.json",
        "pretokenizer.json", "special_tokens.json",
    }:
        raise ValueError("Tokenizer core inventory is incomplete")
    for name, checksum in core_files.items():
        path = artifact / name
        if not path.is_file() or _digest(path) != checksum:
            raise ValueError("Tokenizer core inventory mismatch: " + name)
    inventory = artifact / "checksums.sha256"
    if not inventory.is_file():
        raise ValueError("Tokenizer inventory is missing")
    seen = set()
    for line in inventory.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        checksum, name = line.split(maxsplit=1)
        path = (artifact / name.lstrip("*")).resolve()
        if not path.is_relative_to(artifact.resolve()) or path in seen:
            raise ValueError("Unsafe or duplicate tokenizer inventory path")
        seen.add(path)
        if not path.is_file() or _digest(path) != checksum:
            raise ValueError("Tokenizer inventory mismatch: " + name)
    expected_files = {path.resolve() for path in artifact.rglob("*")
                      if path.is_file() and path.name != "checksums.sha256"}
    if seen != expected_files:
        raise ValueError("Tokenizer inventory does not cover every artifact file")


def validate_best_weights(weight, tensor_is_finite):
    """Validate source tensor shape/dtype without importing Torch in this module."""
    if (tuple(weight.shape) != (6080, 1024) or str(weight.dtype) != "torch.float32"
            or not bool(tensor_is_finite(weight))):
        raise ValueError("Invalid source embedding weights")


def validate_checkpoint(saved, identity, cfg, tensor_is_finite):
    """Check a safely loaded epoch-boundary optimizer checkpoint before resume."""
    validate_variant_identity(identity)
    if not isinstance(saved, dict) or saved.get("identity") != identity or saved.get("cfg") != cfg:
        raise ValueError("Saved optimizer checkpoint identity/configuration mismatch")
    validate_best_weights(saved["source_weight"], tensor_is_finite)
    next_epoch = saved.get("next_epoch")
    history = saved.get("history")
    if (isinstance(next_epoch, bool) or not isinstance(next_epoch, int) or
            not 1 <= next_epoch <= cfg["epochs"] or not isinstance(history, list) or
            len(history) != next_epoch or any(not isinstance(row, dict) for row in history) or
            [row.get("epoch") for row in history] != list(range(1, next_epoch + 1))):
        raise ValueError("Inconsistent resumed history or epoch count")
    for row in history:
        for name in ("train_loss", "validation_loss"):
            value = row.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError("Nonfinite or invalid resumed history loss")
    best = saved.get("best")
    if (isinstance(best, bool) or not isinstance(best, (int, float)) or not math.isfinite(best)
            or best != min(row["validation_loss"] for row in history)):
        raise ValueError("Inconsistent resumed checkpoint selection")
    if not isinstance(saved.get("optimizer"), dict) or not isinstance(saved.get("scaler"), dict):
        raise ValueError("Resume requires optimizer and scaler state")
    return next_epoch


def reload_report_matches(report, info, bundle_root):
    """Allow inference export only for the current identity, weights and selection.

    An absent/stale report returns False so a full resume backup can still be
    preserved. Corrupt bundle identity/runtime bytes raise rather than export.
    """
    info = _metadata(info, "saved manifest")
    identity = info["identity"]
    fields = validate_saved_manifest(info, identity, info["cfg"])
    validate_runtime_files(bundle_root, identity)
    if not isinstance(report, dict) or info["training_status"] != "completed":
        return False
    root = Path(bundle_root)
    weight_path = root / "best_source.safetensors"
    if not weight_path.is_file():
        return False
    expected = {
        **fields, "status": "passed", "identity_sha256": identity_digest(identity),
        "weights_sha256": _digest(weight_path),
        "tokenizer_sha256": identity["tokenizer_sha256"],
        "base_revision": info["revision"], "selected_epoch": info.get("selected_epoch"),
        "beams": identity["beams"], "max_new_tokens": identity["max_new_tokens"],
        "precision": "fp32",
    }
    return all(report.get(key) == value for key, value in expected.items())


def extract_safe_zip(archive_path, destination):
    """Validate all archive paths and links before extracting package/resume bytes."""
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    seen = set()
    with zipfile.ZipFile(archive_path) as archive:
        for entry in archive.infolist():
            name = entry.orig_filename
            target = (destination / name).resolve()
            if ("\\" in name or ":" in name or not target.is_relative_to(destination)
                    or name.startswith("/") or target == destination):
                raise ValueError("Unsafe ZIP path")
            key = target.as_posix().casefold()
            if key in seen:
                raise ValueError("Duplicate ZIP path")
            seen.add(key)
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("ZIP links are not supported")
        archive.extractall(destination)
    return destination
