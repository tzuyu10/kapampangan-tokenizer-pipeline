"""Standard-library data checks for the matched penalty-32 adaptation notebook.

The CSV policy matches cell 9 of the supplied ``nllb-600m-kpm-tgl-1.ipynb``.
The installed Plain30 CSV hash, audit, and ordered split IDs provide additional
locks. The supplied notebook's saved configuration says 15 epochs; its saved
execution is not evidence of the installed 30-epoch runs. No rows are
deduplicated and evaluation rows are never moved or removed.
"""

import csv
import hashlib
import io
import json
import unicodedata
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
        "policy_provenance": "Supplied nllb-600m-kpm-tgl-1.ipynb cell 9 CSV policy; installed Plain30 audit and ordered split IDs verified",
        "original_notebook_training_evidence": "Saved configuration is 15 epochs; saved execution does not establish completed 30-epoch training",
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
