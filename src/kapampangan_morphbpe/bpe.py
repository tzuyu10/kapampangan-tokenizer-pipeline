from __future__ import annotations

import heapq
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION, SPECIAL_TOKENS
from .models import PreparedSequence
from .prepare import load_prepared_stream
from .serialization import fingerprint, read_json, sha256_file, write_json

Pair = tuple[str, str]


@dataclass(slots=True)
class SymbolSpan:
    text: str
    start: int
    end: int


@dataclass(slots=True)
class MutableSequence:
    symbols: list[SymbolSpan]
    protected: frozenset[int]
    frequency: int


@dataclass(frozen=True, slots=True)
class MergeRule:
    rank: int
    left: str
    right: str
    result: str
    result_id: int

    def to_dict(self) -> dict[str, object]:
        return {
            "rank": self.rank,
            "left": self.left,
            "right": self.right,
            "result": self.result,
            "result_id": self.result_id,
        }


@dataclass(frozen=True, slots=True)
class BPEModel:
    target_vocabulary_size: int
    vocabulary: tuple[str, ...]
    character_tokens: frozenset[str]
    merges: tuple[MergeRule, ...]
    protected_boundary_merge_violations: int

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": SCHEMA_VERSION,
            "target_vocabulary_size": self.target_vocabulary_size,
            "actual_vocabulary_size": len(self.vocabulary),
            "vocabulary": list(self.vocabulary),
            "character_tokens": sorted(
                self.character_tokens, key=lambda value: value.encode("utf-8")
            ),
            "merges": [merge.to_dict() for merge in self.merges],
            "protected_boundary_merge_violations": self.protected_boundary_merge_violations,
        }


def _sequence_pairs(sequence: MutableSequence) -> Counter[Pair]:
    counts: Counter[Pair] = Counter()
    for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
        if left.end != right.start:
            raise AssertionError("BPE symbols lost contiguity")
        if left.end in sequence.protected:
            continue
        counts[(left.text, right.text)] += 1
    return counts


def _apply_pair(sequence: MutableSequence, pair: Pair) -> int:
    output: list[SymbolSpan] = []
    index = 0
    applied = 0
    while index < len(sequence.symbols):
        if index + 1 < len(sequence.symbols):
            left = sequence.symbols[index]
            right = sequence.symbols[index + 1]
            if (
                (left.text, right.text) == pair
                and left.end == right.start
                and left.end not in sequence.protected
            ):
                merged = SymbolSpan(left.text + right.text, left.start, right.end)
                if any(merged.start < boundary < merged.end for boundary in sequence.protected):
                    raise AssertionError("merge crossed a protected morpheme boundary")
                output.append(merged)
                index += 2
                applied += 1
                continue
        output.append(sequence.symbols[index])
        index += 1
    sequence.symbols = output
    return applied


class ConstrainedBPETrainer:
    def __init__(self, prepared: list[PreparedSequence]) -> None:
        characters = sorted(
            {character for sequence in prepared for character in sequence.surface},
            key=lambda value: value.encode("utf-8"),
        )
        special_surfaces = [surface for surface, _, _ in SPECIAL_TOKENS]
        self.vocabulary: list[str] = special_surfaces + characters
        self.token_to_id = {token: index for index, token in enumerate(self.vocabulary)}
        self.character_tokens = frozenset(characters)
        self.sequences = [
            MutableSequence(
                [
                    SymbolSpan(character, index, index + 1)
                    for index, character in enumerate(item.surface)
                ],
                frozenset(item.protected_boundaries),
                item.frequency,
            )
            for item in prepared
        ]
        self.pair_counts: Counter[Pair] = Counter()
        self.pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.sequence_pair_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]
        self.heap: list[tuple[int, bytes, bytes, str, str]] = []
        self.merges: list[MergeRule] = []
        self.protected_boundary_merge_violations = 0
        for sequence_id in range(len(self.sequences)):
            self._register(sequence_id)

    def _push(self, pair: Pair) -> None:
        count = self.pair_counts[pair]
        if count > 0:
            heapq.heappush(
                self.heap,
                (-count, pair[0].encode("utf-8"), pair[1].encode("utf-8"), pair[0], pair[1]),
            )

    def _register(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        counts = _sequence_pairs(sequence)
        self.sequence_pair_counts[sequence_id] = counts
        for pair, occurrences in counts.items():
            self.pair_counts[pair] += occurrences * sequence.frequency
            self.pair_sequences[pair].add(sequence_id)
            self._push(pair)

    def _unregister(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        counts = self.sequence_pair_counts[sequence_id]
        for pair, occurrences in counts.items():
            self.pair_counts[pair] -= occurrences * sequence.frequency
            if self.pair_counts[pair] < 0:
                raise AssertionError("negative pair count")
            self.pair_sequences[pair].discard(sequence_id)
            self._push(pair)
        self.sequence_pair_counts[sequence_id] = Counter()

    def _best_pair(self) -> Pair | None:
        while self.heap:
            negative_count, _left_bytes, _right_bytes, left, right = heapq.heappop(self.heap)
            pair = (left, right)
            if self.pair_counts[pair] == -negative_count and self.pair_counts[pair] > 0:
                return pair
        return None

    def _merge_once(self) -> bool:
        pair = self._best_pair()
        if pair is None:
            return False
        affected = sorted(self.pair_sequences[pair])
        if not affected:
            raise AssertionError("selected pair has no sequence occurrences")
        applied_total = 0
        for sequence_id in affected:
            self._unregister(sequence_id)
            applied_total += _apply_pair(self.sequences[sequence_id], pair)
            self._register(sequence_id)
        if applied_total <= 0:
            raise AssertionError("selected pair was not applied")

        result = pair[0] + pair[1]
        result_id = self.token_to_id.get(result)
        if result_id is None:
            result_id = len(self.vocabulary)
            self.token_to_id[result] = result_id
            self.vocabulary.append(result)
        self.merges.append(MergeRule(len(self.merges), pair[0], pair[1], result, result_id))
        return True

    def train(self, targets: list[int]) -> tuple[dict[int, BPEModel], dict[str, object]]:
        ordered_targets = sorted(set(targets))
        if ordered_targets != targets or len(targets) < 1:
            raise ValueError("candidate targets must be sorted and unique")
        if ordered_targets[0] <= len(self.vocabulary):
            raise ValueError("candidate target must exceed initial vocabulary size")
        snapshots: dict[int, BPEModel] = {}
        while len(self.vocabulary) < ordered_targets[-1]:
            if not self._merge_once():
                break
            for target in ordered_targets:
                if target not in snapshots and len(self.vocabulary) >= target:
                    snapshots[target] = BPEModel(
                        target,
                        tuple(self.vocabulary),
                        self.character_tokens,
                        tuple(self.merges),
                        self.protected_boundary_merge_violations,
                    )
        failures = [target for target in ordered_targets if target not in snapshots]
        report: dict[str, object] = {
            "requested_targets": ordered_targets,
            "trained_targets": sorted(snapshots),
            "failed_targets": failures,
            "final_vocabulary_size": len(self.vocabulary),
            "merge_rules_learned": len(self.merges),
            "protected_boundary_merge_violations": self.protected_boundary_merge_violations,
            "stopped_because": "no_permitted_pair" if failures else "maximum_target_reached",
        }
        return snapshots, report


def train_candidate_models(
    prepared_stream_path: Path,
    prepared_manifest_path: Path,
    grid_path: Path,
    output_dir: Path,
) -> tuple[dict[int, BPEModel], dict[str, object]]:
    manifest_raw = read_json(prepared_manifest_path)
    grid_raw = read_json(grid_path)
    if not isinstance(manifest_raw, dict) or not isinstance(grid_raw, dict):
        raise ValueError("prepared manifest and candidate grid must be objects")
    manifest = cast(dict[str, Any], manifest_raw)
    grid = cast(dict[str, Any], grid_raw)
    if manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("prepared manifest dataset mismatch")
    if (
        grid.get("status") != "frozen_before_validation"
        or grid.get("validation_results_observed_when_frozen") is not False
    ):
        raise ValueError("candidate grid was not frozen before validation")
    if sha256_file(prepared_stream_path) != manifest.get("stream_sha256"):
        raise ValueError("prepared stream hash mismatch")
    targets_raw = grid.get("candidate_vocabulary_sizes")
    if not isinstance(targets_raw, list) or not all(isinstance(item, int) for item in targets_raw):
        raise ValueError("candidate vocabulary targets malformed")
    targets = cast(list[int], targets_raw)
    trainer = ConstrainedBPETrainer(load_prepared_stream(prepared_stream_path))
    models, training_report = trainer.train(targets)
    report_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "prepared_manifest_fingerprint": manifest.get("manifest_fingerprint"),
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "family_training": training_report,
        "model_fingerprints": {
            str(target): fingerprint(model.to_dict()) for target, model in sorted(models.items())
        },
    }
    report = {**report_body, "report_fingerprint": fingerprint(report_body)}
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "candidate-training-report.json", report)
    return models, report
