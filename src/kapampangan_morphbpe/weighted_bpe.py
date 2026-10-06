from __future__ import annotations

import heapq
from collections import Counter, defaultdict
from dataclasses import dataclass

from .bpe import BPEModel, MergeRule
from .constants import SPECIAL_TOKENS
from .models import PreparedSequence

Pair = tuple[str, str]


@dataclass(frozen=True, slots=True)
class _SymbolSpan:
    text: str
    start: int
    end: int


@dataclass(slots=True)
class _MutableSequence:
    symbols: list[_SymbolSpan]
    protected: frozenset[int]
    frequency: int


def _initial_sequence(item: PreparedSequence) -> _MutableSequence:
    return _MutableSequence(
        [_SymbolSpan(character, index, index + 1) for index, character in enumerate(item.surface)],
        frozenset(item.protected_boundaries),
        item.frequency,
    )


def _sequence_pair_counts(
    sequence: _MutableSequence,
) -> tuple[Counter[Pair], Counter[Pair]]:
    allowed: Counter[Pair] = Counter()
    crossing: Counter[Pair] = Counter()
    for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
        if left.end != right.start:
            raise AssertionError("BPE symbols lost contiguity")
        if any(left.start < boundary < left.end for boundary in sequence.protected):
            raise AssertionError("left symbol already crosses a protected boundary")
        if any(right.start < boundary < right.end for boundary in sequence.protected):
            raise AssertionError("right symbol already crosses a protected boundary")
        pair = (left.text, right.text)
        if left.end in sequence.protected:
            crossing[pair] += 1
        else:
            allowed[pair] += 1
    return allowed, crossing


def _apply_allowed_pair(sequence: _MutableSequence, pair: Pair) -> int:
    output: list[_SymbolSpan] = []
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
                merged = _SymbolSpan(left.text + right.text, left.start, right.end)
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


class WeightedMorphBPETrainer:
    """Train MorphBPE with a global frequency-weighted boundary penalty.

    For candidate pair ``p``, the deterministic merge score is::

        allowed_frequency(p) - crossing_penalty * crossing_frequency(p)

    Allowed occurrences are counted and merged exactly as in ordinary
    morphology-constrained BPE. Crossing occurrences are never merged during
    training, but unlike the paper-aligned trainer they also reduce the pair's
    global rank. The exported artifact still uses ordinary lexicon-free BPE
    inference.
    """

    def __init__(self, prepared: list[PreparedSequence], crossing_penalty: int) -> None:
        if not prepared:
            raise ValueError("weighted MorphBPE training requires prepared sequences")
        if crossing_penalty < 0:
            raise ValueError("crossing penalty must be non-negative")

        characters = sorted(
            {character for sequence in prepared for character in sequence.surface},
            key=lambda value: value.encode("utf-8"),
        )
        special_surfaces = [surface for surface, _identifier, _role in SPECIAL_TOKENS]
        self.vocabulary: list[str] = special_surfaces + characters
        self.token_to_id = {token: index for index, token in enumerate(self.vocabulary)}
        self.character_tokens = frozenset(characters)
        self.crossing_penalty = crossing_penalty

        self.sequences = [_initial_sequence(item) for item in prepared]
        self.allowed_counts: Counter[Pair] = Counter()
        self.crossing_counts: Counter[Pair] = Counter()
        self.allowed_pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.sequence_allowed_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]
        self.sequence_crossing_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]
        self.heap: list[tuple[int, int, bytes, bytes, str, str]] = []
        self.merges: list[MergeRule] = []
        self.selected_conflicted_merges = 0
        self.selected_merge_samples: list[dict[str, object]] = []

        for sequence_id in range(len(self.sequences)):
            self._register(sequence_id)

    def _score(self, pair: Pair) -> int:
        return self.allowed_counts[pair] - self.crossing_penalty * self.crossing_counts[pair]

    def _push(self, pair: Pair) -> None:
        allowed = self.allowed_counts[pair]
        if allowed <= 0:
            return
        score = self._score(pair)
        heapq.heappush(
            self.heap,
            (
                -score,
                -allowed,
                pair[0].encode("utf-8"),
                pair[1].encode("utf-8"),
                pair[0],
                pair[1],
            ),
        )

    def _register(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        allowed, crossing = _sequence_pair_counts(sequence)
        self.sequence_allowed_counts[sequence_id] = allowed
        self.sequence_crossing_counts[sequence_id] = crossing
        pairs = set(allowed) | set(crossing)
        for pair, occurrences in allowed.items():
            self.allowed_counts[pair] += occurrences * sequence.frequency
            self.allowed_pair_sequences[pair].add(sequence_id)
        for pair, occurrences in crossing.items():
            self.crossing_counts[pair] += occurrences * sequence.frequency
        for pair in pairs:
            self._push(pair)

    def _unregister(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        allowed = self.sequence_allowed_counts[sequence_id]
        crossing = self.sequence_crossing_counts[sequence_id]
        pairs = set(allowed) | set(crossing)
        for pair, occurrences in allowed.items():
            self.allowed_counts[pair] -= occurrences * sequence.frequency
            if self.allowed_counts[pair] < 0:
                raise AssertionError("negative allowed pair count")
            self.allowed_pair_sequences[pair].discard(sequence_id)
        for pair, occurrences in crossing.items():
            self.crossing_counts[pair] -= occurrences * sequence.frequency
            if self.crossing_counts[pair] < 0:
                raise AssertionError("negative crossing pair count")
        self.sequence_allowed_counts[sequence_id] = Counter()
        self.sequence_crossing_counts[sequence_id] = Counter()
        for pair in pairs:
            self._push(pair)

    def _best_pair(self) -> Pair | None:
        while self.heap:
            negative_score, negative_allowed, _left_bytes, _right_bytes, left, right = (
                heapq.heappop(self.heap)
            )
            pair = (left, right)
            if (
                self.allowed_counts[pair] == -negative_allowed
                and self._score(pair) == -negative_score
                and self.allowed_counts[pair] > 0
            ):
                return pair
        return None

    def _merge_once(self) -> bool:
        pair = self._best_pair()
        if pair is None:
            return False
        allowed = self.allowed_counts[pair]
        crossing = self.crossing_counts[pair]
        score = self._score(pair)
        affected = sorted(self.allowed_pair_sequences[pair])
        if not affected:
            raise AssertionError("selected pair has no allowed sequence occurrences")

        applied = 0
        for sequence_id in affected:
            self._unregister(sequence_id)
            applied += _apply_allowed_pair(self.sequences[sequence_id], pair)
            self._register(sequence_id)
        if applied <= 0:
            raise AssertionError("selected pair was not applied")

        if crossing > 0:
            self.selected_conflicted_merges += 1
        if len(self.selected_merge_samples) < 100:
            self.selected_merge_samples.append(
                {
                    "rank": len(self.merges),
                    "left": pair[0],
                    "right": pair[1],
                    "allowed_frequency": allowed,
                    "crossing_frequency": crossing,
                    "weighted_score": score,
                }
            )

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
        if ordered_targets != targets or not targets:
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
                        0,
                    )

        failures = [target for target in ordered_targets if target not in snapshots]
        report: dict[str, object] = {
            "algorithm": "allowed_frequency_minus_crossing_penalty",
            "crossing_penalty": self.crossing_penalty,
            "requested_targets": ordered_targets,
            "trained_targets": sorted(snapshots),
            "failed_targets": failures,
            "final_vocabulary_size": len(self.vocabulary),
            "merge_rules_learned": len(self.merges),
            "protected_boundary_merge_violations": 0,
            "selected_merges_with_crossing_evidence": self.selected_conflicted_merges,
            "selected_merge_samples": self.selected_merge_samples,
            "surface_specific_runtime_guarantees": [],
            "stopped_because": "no_permitted_pair" if failures else "maximum_target_reached",
        }
        return snapshots, report
