"""Parallel Kapampangan-Filipino corpus loading (thesis Ch.3, Sources of Data).

Schema contract (CSV, UTF-8, header row required):
    id        unique string identifier for the pair
    pam_text  Kapampangan source sentence
    tgl_text  Filipino (or Tagalog-labelled, see docs) target sentence
    split     one of: train, validation, test

This module has no torch/transformers dependency; it is safe to import from
the base (non-`mt`-extra) environment for dataset auditing.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from ..serialization import fingerprint

VALID_SPLITS = ("train", "validation", "test")
REQUIRED_COLUMNS = frozenset({"id", "pam_text", "tgl_text", "split"})


@dataclass(frozen=True, slots=True)
class ParallelPair:
    pair_id: str
    pam_text: str
    tgl_text: str
    split: str


@dataclass(frozen=True, slots=True)
class ParallelDataset:
    pairs: tuple[ParallelPair, ...]
    dataset_fingerprint: str
    source_path: Path

    def split(self, name: str) -> tuple[ParallelPair, ...]:
        if name not in VALID_SPLITS:
            raise ValueError(f"unknown split: {name!r}")
        return tuple(pair for pair in self.pairs if pair.split == name)

    def summary(self) -> dict[str, object]:
        return {
            "dataset_fingerprint": self.dataset_fingerprint,
            "source_path": str(self.source_path),
            "total_pairs": len(self.pairs),
            "split_counts": {name: len(self.split(name)) for name in VALID_SPLITS},
        }


def load_parallel_dataset(path: Path) -> ParallelDataset:
    """Load and validate a Kapampangan-Filipino parallel corpus CSV.

    Raises ValueError on missing columns, empty fields, unknown split names,
    or duplicate ids. Does not silently drop or coerce bad rows: a malformed
    corpus must fail loudly rather than train on a silently truncated set.
    """
    rows: list[ParallelPair] = []
    seen_ids: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = set(reader.fieldnames or ())
        if not REQUIRED_COLUMNS.issubset(fieldnames):
            missing = sorted(REQUIRED_COLUMNS - fieldnames)
            raise ValueError(f"parallel corpus is missing required columns: {missing}")
        for line_number, row in enumerate(reader, start=2):
            pair_id = (row["id"] or "").strip()
            pam_text = (row["pam_text"] or "").strip()
            tgl_text = (row["tgl_text"] or "").strip()
            split_name = (row["split"] or "").strip()
            if not pair_id or not pam_text or not tgl_text:
                raise ValueError(f"line {line_number}: id/pam_text/tgl_text must be non-empty")
            if split_name not in VALID_SPLITS:
                raise ValueError(
                    f"line {line_number}: split {split_name!r} must be one of {VALID_SPLITS}"
                )
            if pair_id in seen_ids:
                raise ValueError(f"line {line_number}: duplicate id {pair_id!r}")
            seen_ids.add(pair_id)
            rows.append(ParallelPair(pair_id, pam_text, tgl_text, split_name))
    if not rows:
        raise ValueError(f"{path} contains no data rows")
    fp = fingerprint([[pair.pair_id, pair.pam_text, pair.tgl_text, pair.split] for pair in rows])
    return ParallelDataset(pairs=tuple(rows), dataset_fingerprint=fp, source_path=path.resolve())
