from __future__ import annotations

from pathlib import Path

import pytest

from kapampangan_morphbpe.artifact import (
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.bpe import BPEModel
from kapampangan_morphbpe.nllb_adapter import SourceTokenizerAdapter
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.verification import verify_clean_runtime


def test_artifact_round_trip_offsets_and_unknown(toy_artifact: Path) -> None:
    tokenizer = load_runtime_tokenizer(toy_artifact)
    encoding = tokenizer.encode("ab  ñ!")
    assert encoding.normalized_text == "ab  ñ!"
    assert tokenizer.decode(encoding.ids) == "ab  ñ!"
    assert encoding.tokens[0].token == "ab"
    assert (encoding.tokens[0].start, encoding.tokens[0].end) == (0, 2)
    assert all(
        encoding.normalized_text[token.start : token.end]
        == ("🙂" if token.token == "<unk>" else token.token)
        for token in encoding.tokens
        if token.token != "<unk>"
    )
    unknown = tokenizer.encode("🙂")
    assert [token.token for token in unknown.tokens] == ["<unk>"]
    assert tokenizer.decode(unknown.ids) == "�"


def test_optional_special_tokens_have_stable_ids(toy_artifact: Path) -> None:
    tokenizer = load_runtime_tokenizer(toy_artifact)
    encoding = tokenizer.encode("ab", add_special_tokens=True)
    assert encoding.ids[0] == 2
    assert encoding.ids[-1] == 3
    assert tokenizer.decode(encoding.ids) == "ab"


def test_checksum_corruption_is_rejected(toy_artifact: Path) -> None:
    vocab = toy_artifact / "vocab.json"
    vocab.write_text(vocab.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        load_runtime_tokenizer(toy_artifact)


def test_artifact_export_is_byte_identical(tmp_path: Path, toy_model: BPEModel) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    metadata = {"held_out_test_used": False, "lexicon_fingerprint": "synthetic"}
    export_tokenizer_artifact(toy_model, first, metadata=metadata)
    export_tokenizer_artifact(toy_model, second, metadata=metadata)
    first_files = {
        path.relative_to(first).as_posix(): path.read_bytes()
        for path in first.rglob("*")
        if path.is_file()
    }
    second_files = {
        path.relative_to(second).as_posix(): path.read_bytes()
        for path in second.rglob("*")
        if path.is_file()
    }
    assert first_files == second_files
    assert validate_artifact_files(first)["checksums_match"] is True


def test_standalone_runtime_needs_only_artifact_and_runtime_package(
    tmp_path: Path, toy_artifact: Path
) -> None:
    runtime_root = Path(__file__).resolve().parents[1] / "runtime"
    report = verify_clean_runtime(
        toy_artifact,
        runtime_root,
        tmp_path / "runtime-independence.json",
    )
    assert report["passed"] is True
    assert report["training_resources_present"] is False


def test_future_source_adapter_padding_and_truncation(toy_artifact: Path) -> None:
    adapter = SourceTokenizerAdapter(toy_artifact)
    batch = adapter.encode_batch(["ab!", "a"], padding=True)
    assert batch.input_ids[1][-1] == 0
    assert batch.attention_mask[1][-1] == 0
    assert batch.normalized_offsets[1][-1] == (0, 0)
    assert batch.vocabulary_size > 4
    assert batch.special_tokens["pad"] == {"token": "<pad>", "id": 0}

    with pytest.raises(ValueError, match="truncation is disabled"):
        adapter.encode_batch(["ab!"], max_length=2)
    truncated = adapter.encode_batch(["ab!"], max_length=2, truncation=True)
    assert truncated.truncated == (True,)


def test_missing_checksum_inventory_is_rejected(toy_artifact: Path) -> None:
    (toy_artifact / "checksums.sha256").unlink()
    with pytest.raises(ValueError, match="checksums"):
        load_runtime_tokenizer(toy_artifact)
