from __future__ import annotations

from pathlib import Path

import pytest

from kapampangan_morphbpe.artifact import export_tokenizer_artifact
from kapampangan_morphbpe.bpe import BPEModel, MergeRule


@pytest.fixture
def toy_model() -> BPEModel:
    characters = frozenset(
        {
            " ",
            "!",
            ".",
            "D",
            "M",
            "a",
            "b",
            "c",
            "g",
            "i",
            "k",
            "l",
            "m",
            "n",
            "s",
            "t",
            "u",
            "á",
            "ñ",
        }
    )
    vocabulary = (
        "<pad>",
        "<unk>",
        "<s>",
        "</s>",
        *sorted(characters, key=lambda value: value.encode("utf-8")),
        "ab",
    )
    result_id = vocabulary.index("ab")
    return BPEModel(
        target_vocabulary_size=len(vocabulary),
        vocabulary=vocabulary,
        character_tokens=characters,
        merges=(MergeRule(0, "a", "b", "ab", result_id),),
        protected_boundary_merge_violations=0,
    )


@pytest.fixture
def toy_artifact(tmp_path: Path, toy_model: BPEModel) -> Path:
    artifact = tmp_path / "artifact"
    export_tokenizer_artifact(
        toy_model,
        artifact,
        metadata={
            "lexicon_fingerprint": "synthetic",
            "train_sha256": "0" * 64,
            "held_out_test_used": False,
        },
    )
    return artifact
