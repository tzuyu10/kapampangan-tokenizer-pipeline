from __future__ import annotations

from pathlib import Path
from typing import Any

from .bpe import BPEModel
from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION, SPECIAL_TOKENS
from .serialization import fingerprint, sha256_file, write_json


def _vocabulary_entries(model: BPEModel) -> list[dict[str, object]]:
    special_surfaces = {surface for surface, _identifier, _role in SPECIAL_TOKENS}
    entries: list[dict[str, object]] = []
    for identifier, token in enumerate(model.vocabulary):
        if token in special_surfaces:
            kind = "special"
        elif token in model.character_tokens:
            kind = "character"
        else:
            kind = "merge"
        entries.append({"id": identifier, "token": token, "kind": kind})
    return entries


def _write_checksums(output_dir: Path) -> None:
    files = sorted(
        (
            path
            for path in output_dir.rglob("*")
            if path.is_file() and path.name != "checksums.sha256"
        ),
        key=lambda path: path.relative_to(output_dir).as_posix(),
    )
    content = "".join(
        f"{sha256_file(path)}  {path.relative_to(output_dir).as_posix()}\n" for path in files
    )
    (output_dir / "checksums.sha256").write_text(content, encoding="utf-8", newline="\n")


def export_tokenizer_artifact(
    model: BPEModel,
    output_dir: Path,
    *,
    metadata: dict[str, object],
    tokenizer_card: str | None = None,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    vocabulary = _vocabulary_entries(model)
    merges = [merge.to_dict() for merge in model.merges]
    normalization = {"unicode_normalization": "NFC", "spelling_mappings": []}
    pretokenizer = {
        "algorithm": "unicode_category_state_machine",
        "offset_unit": "normalized_unicode_code_points",
        "word_core_categories": ["L", "M", "N"],
        "internal_joiners_when_flanked": ["'", "-", "\u2019"],
        "whitespace_preserved": True,
        "punctuation_preserved": True,
    }
    special_tokens = [
        {"token": surface, "id": identifier, "role": role}
        for surface, identifier, role in SPECIAL_TOKENS
    ]
    vocab_document = {
        "schema_version": SCHEMA_VERSION,
        "target_vocabulary_size": model.target_vocabulary_size,
        "actual_vocabulary_size": len(vocabulary),
        "tokens": vocabulary,
    }
    merges_document = {
        "schema_version": SCHEMA_VERSION,
        "merge_count": len(merges),
        "merges": merges,
    }
    tokenizer_document = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "kapampangan_morphbpe",
        "normalization": normalization,
        "pretokenizer": pretokenizer,
        "special_tokens": special_tokens,
        "vocabulary": vocabulary,
        "merges": merges,
        "metadata": {
            **metadata,
            "dataset_fingerprint": DATASET_FINGERPRINT,
            "target_vocabulary_size": model.target_vocabulary_size,
            "actual_vocabulary_size": len(vocabulary),
            "merge_count": len(merges),
            "protected_boundary_merge_violations": model.protected_boundary_merge_violations,
        },
    }
    write_json(output_dir / "vocab.json", vocab_document)
    write_json(output_dir / "merges.json", merges_document)
    write_json(
        output_dir / "normalization.json",
        {"schema_version": SCHEMA_VERSION, **normalization},
    )
    write_json(output_dir / "pretokenizer.json", {"schema_version": SCHEMA_VERSION, **pretokenizer})
    write_json(
        output_dir / "special_tokens.json",
        {"schema_version": SCHEMA_VERSION, "special_tokens": special_tokens},
    )
    write_json(output_dir / "tokenizer.json", tokenizer_document)

    core_names = (
        "tokenizer.json",
        "vocab.json",
        "merges.json",
        "normalization.json",
        "pretokenizer.json",
        "special_tokens.json",
    )
    core_hashes = {name: sha256_file(output_dir / name) for name in core_names}
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "kapampangan_morphbpe",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "core_file_sha256": core_hashes,
        "metadata": metadata,
        "target_vocabulary_size": model.target_vocabulary_size,
        "actual_vocabulary_size": len(vocabulary),
        "merge_count": len(merges),
        "special_token_count": len(SPECIAL_TOKENS),
        "protected_boundary_merge_violations": model.protected_boundary_merge_violations,
    }
    artifact_fingerprint = fingerprint(manifest_body)
    manifest_document = {**manifest_body, "artifact_fingerprint": artifact_fingerprint}
    write_json(output_dir / "tokenizer-manifest.json", manifest_document)
    if tokenizer_card is not None:
        (output_dir / "TOKENIZER_CARD.md").write_text(
            tokenizer_card.replace("{ARTIFACT_FINGERPRINT}", artifact_fingerprint),
            encoding="utf-8",
            newline="\n",
        )
    _write_checksums(output_dir)
    return manifest_document


def validate_artifact_files(output_dir: Path) -> dict[str, Any]:
    checksum_path = output_dir / "checksums.sha256"
    if not checksum_path.is_file():
        raise ValueError("checksums.sha256 missing")
    expected: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        digest, separator, relative = line.partition("  ")
        if not separator or len(digest) != 64:
            raise ValueError("malformed artifact checksum line")
        expected[relative] = digest
    actual = {
        path.relative_to(output_dir).as_posix(): sha256_file(path)
        for path in output_dir.rglob("*")
        if path.is_file() and path.name != "checksums.sha256"
    }
    if expected != actual:
        raise ValueError("artifact checksum inventory mismatch")
    return {"files": len(actual), "checksums_match": True}
