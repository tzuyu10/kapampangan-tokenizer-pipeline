from __future__ import annotations

from pathlib import Path

import pytest

from kapampangan_morphbpe.dataset import assert_not_test_path, read_id_text


def test_held_out_test_path_is_rejected(tmp_path: Path) -> None:
    test_path = tmp_path / "test.csv"
    test_path.write_text("id,text\nx,secret\n", encoding="utf-8")
    with pytest.raises(ValueError, match="held-out"):
        assert_not_test_path(test_path)
    with pytest.raises(ValueError):
        list(read_id_text(test_path, role="validation"))


def test_split_role_requires_explicit_filename(tmp_path: Path) -> None:
    path = tmp_path / "development.csv"
    path.write_text("id,text\nx,sulat\n", encoding="utf-8")
    with pytest.raises(ValueError, match="explicit validation"):
        list(read_id_text(path, role="validation"))


def test_large_csv_field_is_preserved(tmp_path: Path) -> None:
    path = tmp_path / "train.csv"
    text = "a" * 150_000
    path.write_text(f"id,text\nx,{text}\n", encoding="utf-8")
    records = list(read_id_text(path, role="train"))
    assert records[0].text == text
