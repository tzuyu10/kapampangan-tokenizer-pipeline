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
    surface: str
    symbols: list[_SymbolSpan]
    protected: frozenset[int]
    frequency: int


def _initial_sequence(item: PreparedSequence) -> _MutableSequence:
    return _MutableSequence(
        item.surface,
        [_SymbolSpan(character, index, index + 1) for index, character in enumerate(item.surface)],
        frozenset(item.protected_boundaries),
        item.frequency,
    )


def _sequence_pairs(sequence: _MutableSequence, *, respect_boundaries: bool) -> Counter[Pair]:
    counts: Counter[Pair] = Counter()
    for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
        if left.end != right.start:
            raise AssertionError("BPE symbols lost contiguity")
        if respect_boundaries and left.end in sequence.protected:
            continue
        counts[(left.text, right.text)] += 1
    return counts


def _crosses_boundary(
    left: _SymbolSpan,
    right: _SymbolSpan,
    protected: frozenset[int],
) -> bool:
    return any(left.start < boundary < right.end for boundary in protected)


def _apply_pair(
    sequence: _MutableSequence,
    pair: Pair,
    *,
    respect_boundaries: bool,
) -> int:
    output: list[_SymbolSpan] = []
    index = 0
    applied = 0
    while index < len(sequence.symbols):
        if index + 1 < len(sequence.symbols):
            left = sequence.symbols[index]
            right = sequence.symbols[index + 1]
            allowed = not respect_boundaries or left.end not in sequence.protected
            if (left.text, right.text) == pair and left.end == right.start and allowed:
                if _crosses_boundary(left, right, sequence.protected):
                    raise AssertionError("merge crossed a protected morpheme boundary")
                output.append(_SymbolSpan(left.text + right.text, left.start, right.end))
                index += 2
                applied += 1
                continue
        output.append(sequence.symbols[index])
        index += 1
    sequence.symbols = output
    return applied


class BoundarySafeBPETrainer:
    """Learn BPE merges that remain boundary-safe under standard runtime order.

    Training sequences retain the ordinary MorphBPE local boundary constraint.
    Audit sequences independently simulate lexicon-free BPE inference. A proposed
    pair is deferred whenever applying it at the current rank would cross any
    frozen audit boundary. The pair may become eligible at a later rank after
    earlier, safe merges change the relevant runtime symbolization.
    """

    def __init__(
        self,
        prepared: list[PreparedSequence],
        audit_sequences: list[PreparedSequence],
    ) -> None:
        if not prepared:
            raise ValueError("boundary-safe training requires prepared sequences")
        if any(not item.protected_boundaries for item in audit_sequences):
            raise ValueError("boundary audit sequences must contain a protected boundary")

        characters = sorted(
            {
                character
                for sequence in (*prepared, *audit_sequences)
                for character in sequence.surface
            },
            key=lambda value: value.encode("utf-8"),
        )
        special_surfaces = [surface for surface, _identifier, _role in SPECIAL_TOKENS]
        self.vocabulary: list[str] = special_surfaces + characters
        self.token_to_id = {token: index for index, token in enumerate(self.vocabulary)}
        self.character_tokens = frozenset(characters)

        self.sequences = [_initial_sequence(item) for item in prepared]
        self.pair_counts: Counter[Pair] = Counter()
        self.pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.sequence_pair_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]
        self.heap: list[tuple[int, bytes, bytes, str, str]] = []

        self.audit_sequences = [_initial_sequence(item) for item in audit_sequences]
        self.audit_pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.audit_sequence_pair_counts: list[Counter[Pair]] = [
            Counter() for _ in self.audit_sequences
        ]

        self.merges: list[MergeRule] = []
        self.protected_boundary_merge_violations = 0
        self.deferred_candidate_events = 0
        self.deferred_pairs: Counter[Pair] = Counter()
        self.deferred_examples: dict[Pair, dict[str, object]] = {}

        for sequence_id in range(len(self.sequences)):
            self._register_training(sequence_id)
        for sequence_id in range(len(self.audit_sequences)):
            self._register_audit(sequence_id)

    def _push(self, pair: Pair) -> None:
        count = self.pair_counts[pair]
        if count > 0:
            heapq.heappush(
                self.heap,
                (-count, pair[0].encode("utf-8"), pair[1].encode("utf-8"), pair[0], pair[1]),
            )

    def _register_training(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        counts = _sequence_pairs(sequence, respect_boundaries=True)
        self.sequence_pair_counts[sequence_id] = counts
        for pair, occurrences in counts.items():
            self.pair_counts[pair] += occurrences * sequence.frequency
            self.pair_sequences[pair].add(sequence_id)
            self._push(pair)

    def _unregister_training(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        for pair, occurrences in self.sequence_pair_counts[sequence_id].items():
            self.pair_counts[pair] -= occurrences * sequence.frequency
            if self.pair_counts[pair] < 0:
                raise AssertionError("negative pair count")
            self.pair_sequences[pair].discard(sequence_id)
            self._push(pair)
        self.sequence_pair_counts[sequence_id] = Counter()

    def _register_audit(self, sequence_id: int) -> None:
        counts = _sequence_pairs(
            self.audit_sequences[sequence_id],
            respect_boundaries=False,
        )
        self.audit_sequence_pair_counts[sequence_id] = counts
        for pair in counts:
            self.audit_pair_sequences[pair].add(sequence_id)

    def _unregister_audit(self, sequence_id: int) -> None:
        for pair in self.audit_sequence_pair_counts[sequence_id]:
            self.audit_pair_sequences[pair].discard(sequence_id)
        self.audit_sequence_pair_counts[sequence_id] = Counter()

    def _best_pair(self) -> Pair | None:
        while self.heap:
            negative_count, _left_bytes, _right_bytes, left, right = heapq.heappop(self.heap)
            pair = (left, right)
            if self.pair_counts[pair] == -negative_count and self.pair_counts[pair] > 0:
                return pair
        return None

    def _boundary_conflict(self, pair: Pair) -> dict[str, object] | None:
        for sequence_id in sorted(self.audit_pair_sequences[pair]):
            sequence = self.audit_sequences[sequence_id]
            for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
                if (left.text, right.text) != pair:
                    continue
                if _crosses_boundary(left, right, sequence.protected):
                    return {
                        "surface": sequence.surface,
                        "protected_boundaries": sorted(sequence.protected),
                        "crossed_boundaries": [
                            boundary
                            for boundary in sorted(sequence.protected)
                            if left.start < boundary < right.end
                        ],
                        "left_span": [left.start, left.end],
                        "right_span": [right.start, right.end],
                    }
        return None

    def _best_safe_pair(self) -> Pair | None:
        suppressed: dict[Pair, int] = {}
        selected: Pair | None = None
        while pair := self._best_pair():
            conflict = self._boundary_conflict(pair)
            if conflict is None:
                selected = pair
                break
            count = self.pair_counts[pair]
            suppressed[pair] = count
            self.pair_counts[pair] = 0
            self.deferred_candidate_events += 1
            self.deferred_pairs[pair] += 1
            self.deferred_examples.setdefault(pair, conflict)

        for pair, count in suppressed.items():
            self.pair_counts[pair] = count
            self._push(pair)
        return selected

    def _apply_training_pair(self, pair: Pair) -> int:
        affected = sorted(self.pair_sequences[pair])
        applied = 0
        for sequence_id in affected:
            self._unregister_training(sequence_id)
            applied += _apply_pair(
                self.sequences[sequence_id],
                pair,
                respect_boundaries=True,
            )
            self._register_training(sequence_id)
        return applied

    def _apply_audit_pair(self, pair: Pair) -> int:
        affected = sorted(self.audit_pair_sequences[pair])
        applied = 0
        for sequence_id in affected:
            self._unregister_audit(sequence_id)
            applied += _apply_pair(
                self.audit_sequences[sequence_id],
                pair,
                respect_boundaries=False,
            )
            self._register_audit(sequence_id)
        return applied

    def _merge_once(self) -> bool:
        pair = self._best_safe_pair()
        if pair is None:
            return False
        applied = self._apply_training_pair(pair)
        if applied <= 0:
            raise AssertionError("selected pair was not applied to training data")
        self._apply_audit_pair(pair)

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
                        self.protected_boundary_merge_violations,
                    )

        failures = [target for target in ordered_targets if target not in snapshots]
        deferred = [
            {
                "left": pair[0],
                "right": pair[1],
                "events": events,
                "example": self.deferred_examples[pair],
            }
            for pair, events in sorted(
                self.deferred_pairs.items(),
                key=lambda item: (-item[1], item[0][0].encode(), item[0][1].encode()),
            )
        ]
        report: dict[str, object] = {
            "requested_targets": ordered_targets,
            "trained_targets": sorted(snapshots),
            "failed_targets": failures,
            "final_vocabulary_size": len(self.vocabulary),
            "merge_rules_learned": len(self.merges),
            "protected_boundary_merge_violations": self.protected_boundary_merge_violations,
            "runtime_boundary_audit_sequence_count": len(self.audit_sequences),
            "runtime_boundary_deferred_candidate_events": self.deferred_candidate_events,
            "runtime_boundary_unique_deferred_pairs": len(self.deferred_pairs),
            "runtime_boundary_deferred_pairs": deferred,
            "stopped_because": "no_globally_safe_pair" if failures else "maximum_target_reached",
        }
        return snapshots, report
