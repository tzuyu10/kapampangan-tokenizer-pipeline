from __future__ import annotations

import heapq
import random
from collections import Counter, defaultdict
from dataclasses import dataclass

_MAX_STALLED_ROUNDS = 10_000

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


def _crosses_boundary(left: _SymbolSpan, right: _SymbolSpan, protected: frozenset[int]) -> bool:
    return any(left.start < boundary < right.end for boundary in protected)


def _training_pair_counts(sequence: _MutableSequence) -> tuple[Counter[Pair], Counter[Pair]]:
    allowed: Counter[Pair] = Counter()
    crossing: Counter[Pair] = Counter()
    for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
        pair = (left.text, right.text)
        if left.end in sequence.protected:
            crossing[pair] += 1
        else:
            allowed[pair] += 1
    return allowed, crossing


def _audit_pair_counts(sequence: _MutableSequence) -> tuple[Counter[Pair], Counter[Pair]]:
    """Same idea as _training_pair_counts, but over the audit sequence's
    unconstrained (real lexicon-free runtime) symbolization: every adjacent
    pair is a candidate regardless of boundaries, and we separately count
    which occurrences would cross this audit word's protected boundary.
    """
    safe: Counter[Pair] = Counter()
    conflicting: Counter[Pair] = Counter()
    for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
        pair = (left.text, right.text)
        if _crosses_boundary(left, right, sequence.protected):
            conflicting[pair] += 1
        else:
            safe[pair] += 1
    return safe, conflicting


def _apply_pair_unconstrained(sequence: _MutableSequence, pair: Pair) -> int:
    output: list[_SymbolSpan] = []
    index = 0
    applied = 0
    while index < len(sequence.symbols):
        if index + 1 < len(sequence.symbols):
            left = sequence.symbols[index]
            right = sequence.symbols[index + 1]
            if (left.text, right.text) == pair and left.end == right.start:
                output.append(_SymbolSpan(left.text + right.text, left.start, right.end))
                index += 2
                applied += 1
                continue
        output.append(sequence.symbols[index])
        index += 1
    sequence.symbols = output
    return applied


def _apply_pair_constrained(sequence: _MutableSequence, pair: Pair) -> int:
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
                if any(left.start < b < right.end for b in sequence.protected):
                    raise AssertionError("merge crossed a protected morpheme boundary")
                output.append(_SymbolSpan(left.text + right.text, left.start, right.end))
                index += 2
                applied += 1
                continue
        output.append(sequence.symbols[index])
        index += 1
    sequence.symbols = output
    return applied


class HybridBoundaryPenaltyBPETrainer:
    """Combines two independently-validated mechanisms into one merge score:

    1. WeightedMorphBPETrainer's frequency-based crossing penalty (this is
       the mechanism behind the deployed penalty-32 tokenizer): a pair that
       crosses a protected boundary ANYWHERE in the training corpus has its
       rank demoted, in proportion to how often that happens.
    2. BoundarySafeBPETrainer's runtime-order audit, turned into a soft
       penalty instead of a hard defer: a set of audit words independently
       simulates real lexicon-free BPE inference (the actual algorithm a
       trained tokenizer runs at encode time). If applying a candidate pair
       right now would, at the audit word's CURRENT partially-merged
       runtime state, cross that word's protected boundary, the pair's rank
       is demoted again -- proportional to how many audit words currently
       have that conflict, not blocked outright as BoundarySafeBPETrainer
       does (which was found to collapse toward character tokenization
       when scaled beyond a handful of hand-picked words).

    score(pair) = allowed_frequency(pair)
                  - crossing_penalty * crossing_frequency(pair)
                  - runtime_penalty  * runtime_conflict_frequency(pair)

    Optionally also applies BPE-dropout (see StochasticWeightedMorphBPETrainer):
    each allowed training occurrence is independently skipped with
    probability dropout_rate, drawn from a seeded RNG in a fixed
    left-to-right, sequence-major order, so two runs with the same inputs,
    seed, and dropout_rate are byte-identical.

    Exploratory: unlike the other trainers in this module, this one has not
    been validated against a held-out reference before being written. Any
    result from it should be treated as a first attempt, not a mature,
    previously-confirmed mechanism.
    """

    def __init__(
        self,
        prepared: list[PreparedSequence],
        audit_sequences: list[PreparedSequence],
        crossing_penalty: int,
        runtime_penalty: int,
        *,
        dropout_rate: float = 0.0,
        seed: int = 0,
    ) -> None:
        if not prepared:
            raise ValueError("training requires prepared sequences")
        if any(not item.protected_boundaries for item in audit_sequences):
            raise ValueError("audit sequences must contain a protected boundary")
        if crossing_penalty < 0 or runtime_penalty < 0:
            raise ValueError("penalties must be non-negative")
        if not (0.0 <= dropout_rate < 1.0):
            raise ValueError("dropout_rate must be in [0.0, 1.0)")

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
        self.crossing_penalty = crossing_penalty
        self.runtime_penalty = runtime_penalty
        self.dropout_rate = dropout_rate
        self.seed = seed
        self._rng = random.Random(seed)

        self.sequences = [_initial_sequence(item) for item in prepared]
        self.allowed_counts: Counter[Pair] = Counter()
        self.crossing_counts: Counter[Pair] = Counter()
        self.allowed_pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.sequence_allowed_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]
        self.sequence_crossing_counts: list[Counter[Pair]] = [Counter() for _ in self.sequences]

        self.audit_sequences = [_initial_sequence(item) for item in audit_sequences]
        self.audit_conflict_counts: Counter[Pair] = Counter()
        self.audit_pair_sequences: dict[Pair, set[int]] = defaultdict(set)
        self.audit_sequence_safe_counts: list[Counter[Pair]] = [
            Counter() for _ in self.audit_sequences
        ]
        self.audit_sequence_conflict_counts: list[Counter[Pair]] = [
            Counter() for _ in self.audit_sequences
        ]

        self.heap: list[tuple[int, int, bytes, bytes, str, str]] = []
        self.merges: list[MergeRule] = []
        self.dropped_occurrences = 0
        self.fully_dropped_rounds = 0

        for sequence_id in range(len(self.sequences)):
            self._register_training(sequence_id)
        for sequence_id in range(len(self.audit_sequences)):
            self._register_audit(sequence_id)

    def _score(self, pair: Pair) -> int:
        return (
            self.allowed_counts[pair]
            - self.crossing_penalty * self.crossing_counts[pair]
            - self.runtime_penalty * self.audit_conflict_counts[pair]
        )

    def _push(self, pair: Pair) -> None:
        if self.allowed_counts[pair] <= 0:
            return
        score = self._score(pair)
        heapq.heappush(
            self.heap,
            (
                -score,
                -self.allowed_counts[pair],
                pair[0].encode("utf-8"),
                pair[1].encode("utf-8"),
                pair[0],
                pair[1],
            ),
        )

    def _register_training(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        allowed, crossing = _training_pair_counts(sequence)
        self.sequence_allowed_counts[sequence_id] = allowed
        self.sequence_crossing_counts[sequence_id] = crossing
        for pair, occurrences in allowed.items():
            self.allowed_counts[pair] += occurrences * sequence.frequency
            self.allowed_pair_sequences[pair].add(sequence_id)
        for pair, occurrences in crossing.items():
            self.crossing_counts[pair] += occurrences * sequence.frequency
        for pair in set(allowed) | set(crossing):
            self._push(pair)

    def _unregister_training(self, sequence_id: int) -> None:
        sequence = self.sequences[sequence_id]
        allowed = self.sequence_allowed_counts[sequence_id]
        crossing = self.sequence_crossing_counts[sequence_id]
        for pair, occurrences in allowed.items():
            self.allowed_counts[pair] -= occurrences * sequence.frequency
            if self.allowed_counts[pair] < 0:
                raise AssertionError("negative allowed pair count")
            self.allowed_pair_sequences[pair].discard(sequence_id)
        for pair, occurrences in crossing.items():
            self.crossing_counts[pair] -= occurrences * sequence.frequency
            if self.crossing_counts[pair] < 0:
                raise AssertionError("negative crossing pair count")
        for pair in set(allowed) | set(crossing):
            self._push(pair)
        self.sequence_allowed_counts[sequence_id] = Counter()
        self.sequence_crossing_counts[sequence_id] = Counter()

    def _register_audit(self, sequence_id: int) -> None:
        sequence = self.audit_sequences[sequence_id]
        safe, conflicting = _audit_pair_counts(sequence)
        self.audit_sequence_safe_counts[sequence_id] = safe
        self.audit_sequence_conflict_counts[sequence_id] = conflicting
        for pair in safe:
            self.audit_pair_sequences[pair].add(sequence_id)
        for pair in conflicting:
            self.audit_pair_sequences[pair].add(sequence_id)
            self.audit_conflict_counts[pair] += conflicting[pair]
        for pair in set(safe) | set(conflicting):
            self._push(pair)

    def _unregister_audit(self, sequence_id: int) -> None:
        safe = self.audit_sequence_safe_counts[sequence_id]
        conflicting = self.audit_sequence_conflict_counts[sequence_id]
        for pair in safe:
            self.audit_pair_sequences[pair].discard(sequence_id)
        for pair, occurrences in conflicting.items():
            self.audit_conflict_counts[pair] -= occurrences
            if self.audit_conflict_counts[pair] < 0:
                raise AssertionError("negative audit conflict count")
            self.audit_pair_sequences[pair].discard(sequence_id)
        for pair in set(safe) | set(conflicting):
            self._push(pair)
        self.audit_sequence_safe_counts[sequence_id] = Counter()
        self.audit_sequence_conflict_counts[sequence_id] = Counter()

    def _best_pair(self) -> Pair | None:
        while self.heap:
            negative_score, negative_allowed, _lb, _rb, left, right = heapq.heappop(self.heap)
            pair = (left, right)
            if (
                self.allowed_counts[pair] == -negative_allowed
                and self._score(pair) == -negative_score
                and self.allowed_counts[pair] > 0
            ):
                return pair
        return None

    def _apply_allowed_pair_with_dropout(self, sequence: _MutableSequence, pair: Pair) -> int:
        if self.dropout_rate == 0.0:
            return _apply_pair_constrained(sequence, pair)
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
                    if self._rng.random() < self.dropout_rate:
                        self.dropped_occurrences += 1
                    else:
                        if any(left.start < b < right.end for b in sequence.protected):
                            raise AssertionError("merge crossed a protected morpheme boundary")
                        output.append(_SymbolSpan(left.text + right.text, left.start, right.end))
                        index += 2
                        applied += 1
                        continue
            output.append(sequence.symbols[index])
            index += 1
        sequence.symbols = output
        return applied

    def _merge_once(self) -> bool:
        pair = self._best_pair()
        if pair is None:
            return False

        affected = sorted(self.allowed_pair_sequences[pair])
        if not affected:
            raise AssertionError("selected pair has no allowed sequence occurrences")
        applied = 0
        for sequence_id in affected:
            self._unregister_training(sequence_id)
            applied += self._apply_allowed_pair_with_dropout(self.sequences[sequence_id], pair)
            self._register_training(sequence_id)
        if applied <= 0:
            # Every eligible occurrence of the selected pair was dropped this
            # round (only possible when dropout_rate > 0). Counts are
            # unchanged, so the caller's loop will deterministically
            # reselect the same pair immediately with freshly-advanced RNG
            # state -- not an error, just a rare event to track (see
            # _MAX_STALLED_ROUNDS in train()).
            self.fully_dropped_rounds += 1
            return True

        audit_affected = sorted(self.audit_pair_sequences[pair])
        for sequence_id in audit_affected:
            self._unregister_audit(sequence_id)
            _apply_pair_unconstrained(self.audit_sequences[sequence_id], pair)
            self._register_audit(sequence_id)

        result = pair[0] + pair[1]
        result_id = self.token_to_id.get(result)
        if result_id is not None:
            # This exact (left, right) -> result merge was already learned in
            # an earlier round; the occurrences applied just now are
            # leftovers that survived dropout that time. Training made real
            # progress (applied > 0), but a second, functionally dead-weight
            # MergeRule for the same pair would only bloat the exported
            # artifact -- at inference the first occurrence of this rule
            # already consumes every such pair before a later rank could
            # ever apply. Skip logging it.
            return True

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
        stalled_rounds = 0
        while len(self.vocabulary) < ordered_targets[-1]:
            vocabulary_before = len(self.vocabulary)
            if not self._merge_once():
                break
            if len(self.vocabulary) == vocabulary_before:
                stalled_rounds += 1
                if stalled_rounds > _MAX_STALLED_ROUNDS:
                    raise AssertionError(
                        "training stalled with no vocabulary growth for "
                        f"{_MAX_STALLED_ROUNDS} consecutive rounds; dropout_rate="
                        f"{self.dropout_rate} is likely too high for this corpus"
                    )
                continue
            stalled_rounds = 0
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
            "algorithm": "hybrid_crossing_and_runtime_audit_penalty",
            "crossing_penalty": self.crossing_penalty,
            "runtime_penalty": self.runtime_penalty,
            "dropout_rate": self.dropout_rate,
            "seed": self.seed,
            "dropped_occurrences": self.dropped_occurrences,
            "fully_dropped_rounds": self.fully_dropped_rounds,
            "audit_sequence_count": len(self.audit_sequences),
            "requested_targets": ordered_targets,
            "trained_targets": sorted(snapshots),
            "failed_targets": failures,
            "final_vocabulary_size": len(self.vocabulary),
            "merge_rules_learned": len(self.merges),
            "protected_boundary_merge_violations": 0,
            "stopped_because": "no_permitted_pair" if failures else "maximum_target_reached",
        }
        return snapshots, report
