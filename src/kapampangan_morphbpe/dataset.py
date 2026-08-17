from __future__ import annotations

import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any, cast

from .constants import (
    DATASET_FINGERPRINT,
    DATASET_NAME,
    DATASET_VERSION,
    EXPECTED_COUNTS,
    PORTABLE_ZIP_SHA256,
)
from .models import CorpusRecord, ReferenceRecord
from .normalization import normalize_text
from .serialization import read_json, sha256_file

ID_TEXT_HEADER = ("id", "text")
REFERENCE_HEADER = ("id", "form", "type", "description", "example", "source")
PARALLEL_HEADER = ("id", "pam_text", "target_text", "target_language")
MAX_CSV_FIELD_SIZE = 2**31 - 1


def _configure_csv_parser() -> None:
    csv.field_size_limit(MAX_CSV_FIELD_SIZE)


def assert_not_test_path(path: Path) -> None:
    if path.name.casefold() == "test.csv":
        raise ValueError("held-out test content is unavailable during tokenizer development")


def read_id_text(path: Path, *, role: str) -> Iterator[CorpusRecord]:
    if role not in {"train", "validation"}:
        raise ValueError(f"unsupported development split role: {role}")
    assert_not_test_path(path)
    if path.name.casefold() != f"{role}.csv":
        raise ValueError(f"expected explicit {role}.csv path, got {path.name}")
    _configure_csv_parser()
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != ID_TEXT_HEADER:
            raise ValueError(f"invalid id,text schema: {path}")
        for line_number, row in enumerate(reader, 2):
            identifier = row.get("id")
            text = row.get("text")
            if not identifier or text is None or not text:
                raise ValueError(f"invalid row at {path}:{line_number}")
            if normalize_text(text) != text:
                raise ValueError(f"non-NFC text at {path}:{line_number}")
            yield CorpusRecord(identifier, text)


def read_references(path: Path) -> Iterator[ReferenceRecord]:
    if path.name not in {"morphology-reference.csv", "linguistic-evidence.csv"}:
        raise ValueError(f"reference path not permitted: {path.name}")
    _configure_csv_parser()
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != REFERENCE_HEADER:
            raise ValueError(f"invalid reference schema: {path}")
        for line_number, row in enumerate(reader, 2):
            values = [row.get(name) for name in REFERENCE_HEADER]
            if values[0] is None or any(value is None for value in values):
                raise ValueError(f"incomplete reference row at {path}:{line_number}")
            yield ReferenceRecord(
                identifier=cast(str, values[0]),
                form=cast(str, values[1]),
                kind=cast(str, values[2]),
                description=cast(str, values[3]),
                example=cast(str, values[4]),
                source=cast(str, values[5]),
            )


def parse_checksum_inventory(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        digest, separator, relative = line.partition("  ")
        if not separator or len(digest) != 64 or not relative:
            raise ValueError(f"malformed checksum inventory line {line_number}")
        checksums[relative] = digest
    return checksums


def _verify_file(root: Path, inventory: dict[str, str], relative: str) -> str:
    expected = inventory.get(relative)
    if expected is None:
        raise ValueError(f"checksum missing for {relative}")
    actual = sha256_file(root / Path(relative))
    if actual != expected:
        raise ValueError(f"checksum mismatch for {relative}")
    return actual


def _count_csv_rows(path: Path, expected_header: tuple[str, ...]) -> int:
    _configure_csv_parser()
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != expected_header:
            raise ValueError(f"invalid CSV schema: {path}")
        return sum(1 for _ in reader)


def verify_dataset(root: Path) -> dict[str, object]:
    root = root.resolve()
    manifest_raw: Any = read_json(root / "metadata/dataset-manifest.json")
    if not isinstance(manifest_raw, dict):
        raise ValueError("dataset manifest must be an object")
    manifest = cast(dict[str, Any], manifest_raw)
    if manifest.get("dataset_name") != DATASET_NAME:
        raise ValueError("dataset name mismatch")
    if manifest.get("dataset_version") != DATASET_VERSION:
        raise ValueError("dataset version mismatch")
    if manifest.get("corpus_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("neutral corpus fingerprint mismatch")

    inventory = parse_checksum_inventory(root / "checksums.sha256")
    verified_hashes = {
        relative: _verify_file(root, inventory, relative)
        for relative in (
            "data/all-clean-kapampangan.csv",
            "data/train.csv",
            "data/validation.csv",
            "data/test.csv",
            "data/code-switched-optional.csv",
            "data/morphology-reference.csv",
            "data/linguistic-evidence.csv",
            "data/parallel-pam-eng.csv",
            "data/parallel-pam-tgl.csv",
            "metadata/dataset-manifest.json",
        )
    }

    manifest_counts = manifest.get("counts")
    if not isinstance(manifest_counts, dict):
        raise ValueError("manifest counts missing")
    split_counts = manifest_counts.get("split_counts")
    if split_counts != {
        "train": EXPECTED_COUNTS["train"],
        "validation": EXPECTED_COUNTS["validation"],
        "test": EXPECTED_COUNTS["test"],
    }:
        raise ValueError("manifest split counts mismatch")
    counts = {
        "neutral": manifest_counts.get("neutral_kapampangan_count"),
        "train": sum(1 for _ in read_id_text(root / "data/train.csv", role="train")),
        "validation": sum(1 for _ in read_id_text(root / "data/validation.csv", role="validation")),
        "test": cast(dict[str, int], split_counts)["test"],
        "code_switched_optional": _count_csv_rows(
            root / "data/code-switched-optional.csv", ID_TEXT_HEADER
        ),
        "parallel_pam_eng": _count_csv_rows(root / "data/parallel-pam-eng.csv", PARALLEL_HEADER),
        "parallel_pam_tgl": _count_csv_rows(root / "data/parallel-pam-tgl.csv", PARALLEL_HEADER),
        "morphology_reference": sum(
            1 for _ in read_references(root / "data/morphology-reference.csv")
        ),
        "linguistic_evidence": sum(
            1 for _ in read_references(root / "data/linguistic-evidence.csv")
        ),
    }
    for key, actual in counts.items():
        if actual != EXPECTED_COUNTS[key]:
            raise ValueError(f"record count mismatch for {key}: {actual}")

    zip_path = root.with_suffix(".zip")
    zip_result: dict[str, object] = {"path": str(zip_path), "present": zip_path.is_file()}
    if zip_path.is_file():
        zip_digest = sha256_file(zip_path)
        if zip_digest != PORTABLE_ZIP_SHA256:
            raise ValueError("portable ZIP SHA-256 mismatch")
        zip_result["sha256"] = zip_digest

    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "corpus_fingerprint": DATASET_FINGERPRINT,
        "counts": counts,
        "held_out_test": {
            "records_from_manifest": EXPECTED_COUNTS["test"],
            "content_parsed": False,
            "sha256": verified_hashes["data/test.csv"],
        },
        "verified_file_hashes": verified_hashes,
        "checksum_inventory_sha256": sha256_file(root / "checksums.sha256"),
        "portable_zip": zip_result,
    }
