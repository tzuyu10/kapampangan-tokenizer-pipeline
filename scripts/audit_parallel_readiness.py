from __future__ import annotations

import argparse
import csv
import hashlib
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    csv.field_size_limit(2**31 - 1)
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def _neutral_id(text: str, known_suffixes: dict[str, str]) -> str | None:
    digest = hashlib.sha256(unicodedata.normalize("NFC", text).encode("utf-8")).hexdigest()
    for length in sorted({len(value) for value in known_suffixes}, reverse=True):
        identifier = known_suffixes.get(digest[:length])
        if identifier is not None:
            return identifier
    return None


def audit(dataset_root: Path) -> dict[str, object]:
    parallel_path = dataset_root / "data/parallel-pam-tgl.csv"
    split_path = dataset_root / "metadata/split-manifest.csv"
    source_path = dataset_root / "metadata/source-map.csv"
    record_path = dataset_root / "metadata/record-metadata.csv"
    manifest_path = dataset_root / "metadata/dataset-manifest.json"

    rows = _read_csv(parallel_path)
    split_rows = _read_csv(split_path)
    source_rows = _read_csv(source_path)
    record_rows = _read_csv(record_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    split_by_id = {row["id"]: row["split"] for row in split_rows}
    suffix_to_id = {row["id"][4:]: row["id"] for row in split_rows}
    source_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        source_by_id[row["id"]].append(row)
    metadata_by_id = {row["id"]: row for row in record_rows}

    split_counts: Counter[str] = Counter()
    document_keys: set[str] = set()
    source_keys: set[str] = set()
    ocr_source_rows = 0
    mapped_ids: set[str] = set()
    for row in rows:
        identifier = _neutral_id(row["pam_text"], suffix_to_id)
        if identifier is None:
            split_counts["unassigned"] += 1
            continue
        mapped_ids.add(identifier)
        split_counts[split_by_id[identifier]] += 1
        for source in source_by_id.get(identifier, []):
            document_keys.add(source["document_key"])
            source_keys.add(source["source_key"])
        if metadata_by_id.get(identifier, {}).get("ocr_derived") == "true":
            ocr_source_rows += 1

    pair_ids = [row["id"] for row in rows]
    sources = [unicodedata.normalize("NFC", row["pam_text"]) for row in rows]
    targets = [unicodedata.normalize("NFC", row["target_text"]) for row in rows]
    target_labels = Counter(row["target_language"] for row in rows)
    return {
        "schema_version": "1.0.0",
        "dataset_fingerprint": manifest["corpus_fingerprint"],
        "method": {
            "parallel_file_read": "data/parallel-pam-tgl.csv",
            "split_assignment_source": "metadata/split-manifest.csv",
            "neutral_id_rule": "kgc- plus the first 24 SHA-256 hex characters of NFC text",
            "held_out_test_csv_parsed": False,
        },
        "counts": {
            "rows": len(rows),
            "unique_pair_ids": len(set(pair_ids)),
            "unique_pam_sources": len(set(sources)),
            "duplicate_pam_source_rows_beyond_first": len(sources) - len(set(sources)),
            "unique_targets": len(set(targets)),
            "duplicate_target_rows_beyond_first": len(targets) - len(set(targets)),
            "nonempty_pairs": sum(
                bool(source and target) for source, target in zip(sources, targets, strict=True)
            ),
            "nfc_pairs": sum(
                row["pam_text"] == source and row["target_text"] == target
                for row, source, target in zip(rows, sources, targets, strict=True)
            ),
        },
        "language_contract": {
            "target_labels": dict(sorted(target_labels.items())),
            "tgl_interpretation": "Tagalog label; equivalence to Filipino is not established",
            "paper_filipino_requirement_satisfied": False,
        },
        "split_availability": {
            "parallel_rows_have_split_column": False,
            "neutral_source_assignments": {
                key: split_counts.get(key, 0)
                for key in ("train", "validation", "test", "unassigned")
            },
            "unique_neutral_source_ids_mapped": len(mapped_ids),
        },
        "provenance": {
            "source_keys": sorted(source_keys),
            "document_keys": sorted(document_keys),
            "document_key_count": len(document_keys),
            "semantic_domains": "not encoded in the portable parallel table",
            "mapped_rows_marked_ocr_derived": ocr_source_rows,
        },
        "technical_assessment": {
            "csv_schema_and_nonempty_rows_usable": True,
            "safe_for_tokenizer_training": False,
            "safe_for_translation_smoke_test": False,
            "reason": (
                "Only 45 Tagalog-labeled pairs exist; sources repeat, 30 source rows map to "
                "the neutral held-out assignment, and translation/linguistic quality is not "
                "human-validated."
            ),
        },
        "adequacy": {
            "paper_expected_pairs_approximately": 13_000,
            "paper_expected_aligned_test_sentences": 1_300,
            "available_pairs": len(rows),
            "requirement_satisfied": False,
            "nllb_training_authorized": False,
        },
        "input_sha256": {
            "parallel_pam_tgl": _sha256(parallel_path),
            "split_manifest": _sha256(split_path),
            "source_map": _sha256(source_path),
            "record_metadata": _sha256(record_path),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.dataset_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
