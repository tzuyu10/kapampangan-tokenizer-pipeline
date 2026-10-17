from __future__ import annotations

import heapq
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from .bpe import BPEModel
from .models import PreparedSequence
from .weighted_bpe import Pair, WeightedMorphBPETrainer

Role = Literal["root", "affix", "infix"]
Phase = Literal["root", "affix", "infix", "weighted"]
ROLES: tuple[Role, ...] = ("root", "affix", "infix")
PriorityEntry = tuple[int, int, int, bytes, bytes, str, str]


@dataclass(frozen=True, slots=True)
class RoleSpan:
    """A trusted contiguous surface span used only for training priorities."""

    start: int
    end: int
    role: Role

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("role span must have nonnegative, increasing offsets")
        if self.role not in ROLES:
            raise ValueError("role span must identify a root, affix, or infix")


class RootPriorityMorphBPETrainer(WeightedMorphBPETrainer):
    """Learn bounded role-priority merges, then ordinary weighted BPE.

    Roles classify individual surface occurrences, never pair strings. Each
    priority phase selects by current within-role frequency, weighted score,
    allowed frequency, and UTF-8 pair order. The inherited merge application
    still applies a selected pair to every allowed training occurrence and
    never crosses a protected boundary. Exported inference remains ordinary
    global BPE; these priorities do not guarantee runtime morpheme isolation.

    Budgets count newly added vocabulary tokens rather than merge rules. A
    phase ends when its budget is reached or no supported pair remains.
    Roots precede affixes by default; reversing ``priority_order`` provides
    a matched affix-first experiment with the same role budgets.
    A separately labelled infix role supports infix-only or infix-first
    schedules. The caller must exclude infixes from other affix spans.
    """

    def __init__(
        self,
        prepared: list[PreparedSequence],
        crossing_penalty: int,
        spans_by_sequence: Sequence[Sequence[RoleSpan]],
        *,
        root_token_budget: int,
        affix_token_budget: int,
        infix_token_budget: int = 0,
        priority_order: tuple[Role, ...] = ("root", "affix"),
    ) -> None:
        if len(spans_by_sequence) != len(prepared):
            raise ValueError("role spans must align with every prepared sequence")
        if root_token_budget < 0 or affix_token_budget < 0 or infix_token_budget < 0:
            raise ValueError("priority token budgets must be nonnegative")
        if (
            not isinstance(priority_order, tuple)
            or not priority_order
            or any(role not in ROLES for role in priority_order)
            or len(set(priority_order)) != len(priority_order)
        ):
            raise ValueError("priority order must be a nonempty tuple of distinct supported roles")
        self.priority_order = priority_order
        self._priority_phase_index = 0
        self.spans_by_sequence = tuple(tuple(spans) for spans in spans_by_sequence)
        for item, spans in zip(prepared, self.spans_by_sequence, strict=True):
            previous_end = 0
            edges = {0, len(item.surface), *item.protected_boundaries}
            for span in spans:
                if span.end > len(item.surface) or span.start < previous_end:
                    raise ValueError("role spans must be ordered, nonoverlapping, and in bounds")
                if span.start not in edges or span.end not in edges:
                    raise ValueError("role span edges must align with protected or word edges")
                if any(span.start < edge < span.end for edge in item.protected_boundaries):
                    raise ValueError("role span may not contain a protected boundary")
                previous_end = span.end

        # The base constructor invokes our registration and heap methods.
        self.role_counts: dict[Role, Counter[Pair]] = {role: Counter() for role in ROLES}
        self.sequence_role_counts: dict[Role, list[Counter[Pair]]] = {
            role: [Counter() for _ in prepared] for role in ROLES
        }
        self.phase: Phase = self.priority_order[0]
        self.priority_heap: list[PriorityEntry] = []
        self.phase_budgets = {"root": root_token_budget, "affix": affix_token_budget}
        if "infix" in self.priority_order:
            self.phase_budgets["infix"] = infix_token_budget
        self.phase_statistics = {
            phase: {"merge_rules": 0, "new_vocabulary_tokens": 0}
            for phase in (*self.phase_budgets, "weighted")
        }
        self.phase_transitions: list[dict[str, object]] = []
        self.priority_merge_samples: list[dict[str, object]] = []
        self._phase_sample_counts = {phase: 0 for phase in (*ROLES, "weighted")}
        self._selected_context: dict[str, object] | None = None
        super().__init__(prepared, crossing_penalty)
        self.phase_transitions.append(
            {
                "phase": self.phase,
                "reason": "initial_phase",
                "merge_rank": 0,
                "vocabulary_size": len(self.vocabulary),
            }
        )

    def _current_role_counts(self, sequence_id: int) -> dict[Role, Counter[Pair]]:
        sequence = self.sequences[sequence_id]
        spans = self.spans_by_sequence[sequence_id]
        counts: dict[Role, Counter[Pair]] = {role: Counter() for role in ROLES}
        span_index = 0
        for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
            while span_index < len(spans) and spans[span_index].end <= left.start:
                span_index += 1
            if span_index == len(spans):
                break
            span = spans[span_index]
            if (
                span.start <= left.start
                and right.end <= span.end
                and left.end == right.start
                and left.end not in sequence.protected
            ):
                counts[span.role][(left.text, right.text)] += 1
        return counts

    def _register(self, sequence_id: int) -> None:
        current = self._current_role_counts(sequence_id)
        frequency = self.sequences[sequence_id].frequency
        for role in ROLES:
            self.sequence_role_counts[role][sequence_id] = current[role]
            for pair, occurrences in current[role].items():
                self.role_counts[role][pair] += occurrences * frequency
        super()._register(sequence_id)

    def _unregister(self, sequence_id: int) -> None:
        frequency = self.sequences[sequence_id].frequency
        for role in ROLES:
            for pair, occurrences in self.sequence_role_counts[role][sequence_id].items():
                self.role_counts[role][pair] -= occurrences * frequency
                if self.role_counts[role][pair] < 0:
                    raise AssertionError("negative within-role pair count")
            self.sequence_role_counts[role][sequence_id] = Counter()
        super()._unregister(sequence_id)

    def _push_priority(self, pair: Pair) -> None:
        if self.phase == "weighted":
            return
        support = self.role_counts[self.phase][pair]
        allowed = self.allowed_counts[pair]
        if support > 0 and allowed > 0:
            heapq.heappush(
                self.priority_heap,
                (
                    -support,
                    -self._score(pair),
                    -allowed,
                    pair[0].encode("utf-8"),
                    pair[1].encode("utf-8"),
                    pair[0],
                    pair[1],
                ),
            )

    def _push(self, pair: Pair) -> None:
        super()._push(pair)
        self._push_priority(pair)

    def _advance_phase(self, reason: str) -> None:
        self._priority_phase_index += 1
        self.phase = (
            self.priority_order[self._priority_phase_index]
            if self._priority_phase_index < len(self.priority_order)
            else "weighted"
        )
        self.priority_heap.clear()
        self.phase_transitions.append(
            {
                "phase": self.phase,
                "reason": reason,
                "merge_rank": len(self.merges),
                "vocabulary_size": len(self.vocabulary),
            }
        )
        if self.phase != "weighted":
            for pair in self.role_counts[self.phase]:
                self._push_priority(pair)

    def _best_pair(self) -> Pair | None:
        while self.phase != "weighted":
            if (
                self.phase_statistics[self.phase]["new_vocabulary_tokens"]
                >= self.phase_budgets[self.phase]
            ):
                self._advance_phase("token_budget_reached")
                continue
            while self.priority_heap:
                negative_support, negative_score, negative_allowed, _, _, left, right = (
                    heapq.heappop(self.priority_heap)
                )
                pair = (left, right)
                if (
                    self.role_counts[self.phase][pair] == -negative_support
                    and self._score(pair) == -negative_score
                    and self.allowed_counts[pair] == -negative_allowed
                    and self.allowed_counts[pair] > 0
                ):
                    self._record_selection(pair)
                    return pair
            self._advance_phase("no_supported_pair")
        pair = super()._best_pair()
        if pair is not None:
            self._record_selection(pair)
        return pair

    def _record_selection(self, pair: Pair) -> None:
        self._selected_context = {
            "phase": self.phase,
            "rank": len(self.merges),
            "left": pair[0],
            "right": pair[1],
            "root_frequency": self.role_counts["root"][pair],
            "affix_frequency": self.role_counts["affix"][pair],
            "infix_frequency": self.role_counts["infix"][pair],
            "allowed_frequency": self.allowed_counts[pair],
            "crossing_frequency": self.crossing_counts[pair],
            "weighted_score": self._score(pair),
        }

    def _merge_once(self) -> bool:
        previous_size = len(self.vocabulary)
        self._selected_context = None
        if not super()._merge_once():
            return False
        if self._selected_context is None:
            raise AssertionError("merge did not record its selected phase")
        self.phase_statistics[self.phase]["merge_rules"] += 1
        self.phase_statistics[self.phase]["new_vocabulary_tokens"] += (
            len(self.vocabulary) - previous_size
        )
        if self._phase_sample_counts[self.phase] < 40:
            self.priority_merge_samples.append(self._selected_context)
            self._phase_sample_counts[self.phase] += 1
        return True

    def train(self, targets: list[int]) -> tuple[dict[int, BPEModel], dict[str, object]]:
        models, report = super().train(targets)
        report.update(
            {
                "algorithm": (
                    "_then_".join(f"{role}_priority" for role in self.priority_order)
                    + "_then_weighted"
                ),
                "priority_order": [*self.priority_order, "weighted"],
                "priority_strategy": "current_within_span_occurrence_frequency",
                "priority_selection_key": [
                    "role_frequency_descending",
                    "weighted_score_descending",
                    "allowed_frequency_descending",
                    "pair_utf8_ascending",
                ],
                "priority_budget_unit": "new_vocabulary_tokens",
                "priority_token_budgets": dict(self.phase_budgets),
                "phase_statistics": self.phase_statistics,
                "phase_transitions": self.phase_transitions,
                "priority_merge_samples": self.priority_merge_samples,
                "priority_merge_sample_limit_per_phase": 40,
                "final_phase": self.phase,
                "training_roles_used_at_runtime": False,
            }
        )
        return models, report
