from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from kapampangan_morphbpe.artifact import export_tokenizer_artifact
from kapampangan_morphbpe.models import PreparedSequence
from kapampangan_morphbpe.root_priority_bpe import Role, RoleSpan, RootPriorityMorphBPETrainer
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer


def _trainer(
    prepared: list[PreparedSequence],
    spans: list[list[RoleSpan]],
    root_budget: int = 20,
    affix_budget: int = 20,
    priority_order: tuple[Role, ...] = ("root", "affix"),
    infix_budget: int = 0,
) -> RootPriorityMorphBPETrainer:
    return RootPriorityMorphBPETrainer(
        prepared,
        crossing_penalty=32,
        spans_by_sequence=spans,
        root_token_budget=root_budget,
        affix_token_budget=affix_budget,
        infix_token_budget=infix_budget,
        priority_order=priority_order,
    )


def _fresh_counts(trainer: RootPriorityMorphBPETrainer) -> dict[str, Counter]:
    """Independently recount occurrences from the current symbol offsets."""
    counts = {name: Counter() for name in ("root", "affix", "infix", "allowed", "crossing")}
    for sequence, spans in zip(trainer.sequences, trainer.spans_by_sequence, strict=True):
        for left, right in zip(sequence.symbols, sequence.symbols[1:], strict=False):
            pair = (left.text, right.text)
            crossing = left.end in sequence.protected
            counts["crossing" if crossing else "allowed"][pair] += sequence.frequency
            if not crossing:
                for span in spans:
                    if left.start >= span.start and right.end <= span.end:
                        counts[span.role][pair] += sequence.frequency
    return counts


def test_root_then_affix_then_weighted_order_with_fixed_token_budgets() -> None:
    prepared = [
        PreparedSequence("abc", (), "word", 2),
        PreparedSequence("xy", (), "word", 100),
        PreparedSequence("pq", (), "word", 1000),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 3, "root")], [RoleSpan(0, 2, "affix")], []],
        root_budget=1,
        affix_budget=1,
    )
    models, report = trainer.train([len(trainer.vocabulary) + 4])
    model = models[report["final_vocabulary_size"]]

    assert [(rule.left, rule.right) for rule in model.merges[:3]] == [
        ("a", "b"),
        ("x", "y"),
        ("p", "q"),
    ]
    assert [sample["phase"] for sample in report["priority_merge_samples"]] == [
        "root", "affix", "weighted", "weighted"
    ]
    assert report["phase_statistics"] == {
        "root": {"merge_rules": 1, "new_vocabulary_tokens": 1},
        "affix": {"merge_rules": 1, "new_vocabulary_tokens": 1},
        "weighted": {"merge_rules": 2, "new_vocabulary_tokens": 2},
    }
    assert [event["reason"] for event in report["phase_transitions"]] == [
        "initial_phase", "token_budget_reached", "token_budget_reached"
    ]
    assert report["training_roles_used_at_runtime"] is False
    assert report["algorithm"] == "root_priority_then_affix_priority_then_weighted"
    assert report["priority_order"] == ["root", "affix", "weighted"]


def test_affix_then_root_then_weighted_order_with_same_role_budgets() -> None:
    prepared = [
        PreparedSequence("abc", (), "word", 2),
        PreparedSequence("xy", (), "word", 100),
        PreparedSequence("pq", (), "word", 1000),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 3, "root")], [RoleSpan(0, 2, "affix")], []],
        root_budget=1,
        affix_budget=1,
        priority_order=("affix", "root"),
    )
    models, report = trainer.train([len(trainer.vocabulary) + 4])
    model = models[report["final_vocabulary_size"]]

    assert [(rule.left, rule.right) for rule in model.merges[:3]] == [
        ("x", "y"),
        ("a", "b"),
        ("p", "q"),
    ]
    assert [sample["phase"] for sample in report["priority_merge_samples"]] == [
        "affix", "root", "weighted", "weighted"
    ]
    assert report["phase_statistics"] == {
        "root": {"merge_rules": 1, "new_vocabulary_tokens": 1},
        "affix": {"merge_rules": 1, "new_vocabulary_tokens": 1},
        "weighted": {"merge_rules": 2, "new_vocabulary_tokens": 2},
    }
    assert [event["phase"] for event in report["phase_transitions"]] == [
        "affix", "root", "weighted"
    ]
    assert report["algorithm"] == "affix_priority_then_root_priority_then_weighted"
    assert report["priority_order"] == ["affix", "root", "weighted"]


def test_priority_frequency_precedes_score_and_score_resolves_ties() -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 2),
        PreparedSequence("ab", (1,), "word", 1000),
        PreparedSequence("xy", (), "word", 1),
        PreparedSequence("pq", (), "word", 1),
        PreparedSequence("pq", (), "word", 10),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 2, "root")], [], [RoleSpan(0, 2, "root")],
         [RoleSpan(0, 2, "root")], []],
    )
    assert trainer._merge_once()
    assert trainer.merges[-1].result == "ab"  # Root support 2 beats support 1.
    assert trainer._merge_once()
    assert trainer.merges[-1].result == "pq"  # Tied support, higher weighted score.
    assert [symbol.text for symbol in trainer.sequences[1].symbols] == ["a", "b"]


@pytest.mark.parametrize("priority_order", [("root", "affix"), ("affix", "root")])
def test_same_pair_can_have_root_affix_and_unlabelled_occurrences(
    priority_order: tuple[Role, Role],
) -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 2),
        PreparedSequence("ab", (), "word", 7),
        PreparedSequence("ab", (), "word", 11),
        PreparedSequence("ab", (1,), "word", 13),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 2, "root")], [RoleSpan(0, 2, "affix")], [], []],
        root_budget=1,
        affix_budget=1,
        priority_order=priority_order,
    )
    assert trainer.role_counts["root"][("a", "b")] == 2
    assert trainer.role_counts["affix"][("a", "b")] == 7
    assert trainer.allowed_counts[("a", "b")] == 20
    assert trainer.crossing_counts[("a", "b")] == 13
    assert trainer._merge_once()
    assert [[symbol.text for symbol in item.symbols] for item in trainer.sequences] == [
        ["ab"], ["ab"], ["ab"], ["a", "b"]
    ]
    assert trainer.priority_merge_samples[0]["root_frequency"] == 2
    assert trainer.priority_merge_samples[0]["affix_frequency"] == 7
    assert not trainer._merge_once()
    assert trainer.phase == "weighted"
    assert trainer.phase_statistics[priority_order[0]]["new_vocabulary_tokens"] == 1
    assert trainer.phase_statistics[priority_order[1]]["new_vocabulary_tokens"] == 0


@pytest.mark.parametrize("priority_order", [("root", "affix"), ("affix", "root")])
def test_dynamic_counts_match_independent_recount_after_every_merge(
    priority_order: tuple[Role, Role],
) -> None:
    prepared = [
        PreparedSequence("ababa", (), "word", 3),
        PreparedSequence("abxcd", (3,), "word", 2),
        PreparedSequence("abcd", (2,), "word", 7),
        PreparedSequence("ab", (), "word", 1),
    ]
    trainer = _trainer(
        prepared,
        [
            [RoleSpan(0, 5, "root")],
            [RoleSpan(0, 3, "root"), RoleSpan(3, 5, "affix")],
            [RoleSpan(0, 2, "root"), RoleSpan(2, 4, "affix")],
            [],
        ],
        root_budget=2,
        affix_budget=1,
        priority_order=priority_order,
    )
    merges = 0
    while True:
        fresh = _fresh_counts(trainer)
        assert trainer.role_counts["root"] == fresh["root"]
        assert trainer.role_counts["affix"] == fresh["affix"]
        assert trainer.allowed_counts == fresh["allowed"]
        assert trainer.crossing_counts == fresh["crossing"]
        for sequence in trainer.sequences:
            assert "".join(symbol.text for symbol in sequence.symbols) in {
                item.surface for item in prepared
            }
            assert all(
                not (symbol.start < boundary < symbol.end)
                for symbol in sequence.symbols for boundary in sequence.protected
            )
        if not trainer._merge_once():
            break
        merges += 1
        assert merges < 30
    assert merges > 3


@pytest.mark.parametrize("priority_order", [("root", "affix"), ("affix", "root")])
def test_phase_exhaustion_advances_without_consuming_unused_budget(
    priority_order: tuple[Role, Role],
) -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 1),
        PreparedSequence("xy", (), "word", 10),
        PreparedSequence("pq", (), "word", 100),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 2, "root")], [RoleSpan(0, 2, "affix")], []],
        priority_order=priority_order,
    )
    _, report = trainer.train([len(trainer.vocabulary) + 3])
    role_results = {"root": "ab", "affix": "xy"}
    assert [rule.result for rule in trainer.merges] == [
        role_results[priority_order[0]], role_results[priority_order[1]], "pq"
    ]
    assert [event["reason"] for event in report["phase_transitions"]] == [
        "initial_phase", "no_supported_pair", "no_supported_pair"
    ]
    assert report["phase_statistics"]["root"]["new_vocabulary_tokens"] == 1
    assert report["phase_statistics"]["affix"]["new_vocabulary_tokens"] == 1


@pytest.mark.parametrize("empty_roles", [False, True])
@pytest.mark.parametrize(
    "priority_order",
    [("root", "affix"), ("affix", "root"), ("infix",), ("infix", "root", "affix")],
)
def test_disabled_or_unsupported_priorities_match_original_weighted_model(
    empty_roles: bool,
    priority_order: tuple[Role, ...],
) -> None:
    prepared = [
        PreparedSequence("ab", (1,), "word", 100),
        PreparedSequence("abx", (), "word", 120),
        PreparedSequence("ac", (), "word", 110),
    ]
    spans = [[], [], []] if empty_roles else [[], [RoleSpan(0, 3, "root")], []]
    trainer = _trainer(
        prepared, spans, root_budget=20 if empty_roles else 0,
        affix_budget=20 if empty_roles else 0,
        priority_order=priority_order,
    )
    target = len(trainer.vocabulary) + 3
    original, _ = WeightedMorphBPETrainer(prepared, crossing_penalty=32).train([target])
    candidate, report = trainer.train([target])
    assert candidate[target].to_dict() == original[target].to_dict()
    assert report["phase_statistics"]["root"]["merge_rules"] == 0
    assert report["phase_statistics"]["affix"]["merge_rules"] == 0


@pytest.mark.parametrize("priority_order", [("root", "affix"), ("affix", "root")])
def test_infix_root_fragments_remain_separate_contiguous_spans(
    priority_order: tuple[Role, Role],
) -> None:
    prepared = [PreparedSequence("kumain", (1, 3), "word", 5)]
    trainer = _trainer(
        prepared,
        [[RoleSpan(0, 1, "root"), RoleSpan(1, 3, "affix"), RoleSpan(3, 6, "root")]],
        priority_order=priority_order,
    )
    while trainer._merge_once():
        pass
    expected = ["ai", "ain", "um"] if priority_order[0] == "root" else ["um", "ai", "ain"]
    assert [rule.result for rule in trainer.merges] == expected
    assert [symbol.text for symbol in trainer.sequences[0].symbols] == ["k", "um", "ain"]
    assert "kain" not in trainer.vocabulary


@pytest.mark.parametrize(
    "spans",
    [
        [[RoleSpan(0, 5, "root")]],  # Out of bounds.
        [[RoleSpan(0, 4, "root")]],  # Includes a protected boundary.
        [[RoleSpan(0, 1, "root")]],  # Endpoint is not a morpheme boundary.
        [[RoleSpan(2, 4, "affix"), RoleSpan(0, 2, "root")]],  # Unordered.
        [[RoleSpan(0, 2, "root"), RoleSpan(0, 2, "affix")]],  # Overlapping.
        [],  # Does not align with the prepared list.
    ],
)
def test_rejects_invalid_role_span_alignment(spans: list[list[RoleSpan]]) -> None:
    with pytest.raises(ValueError):
        _trainer([PreparedSequence("abcd", (2,), "word", 1)], spans)


def test_rejects_invalid_roles_offsets_and_budgets() -> None:
    with pytest.raises(ValueError):
        RoleSpan(-1, 2, "root")
    with pytest.raises(ValueError):
        RoleSpan(2, 2, "root")
    with pytest.raises(ValueError):
        RoleSpan(0, 2, "other")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        _trainer([PreparedSequence("ab", (), "word", 1)], [[]], root_budget=-1)
    with pytest.raises(ValueError):
        _trainer([PreparedSequence("ab", (), "word", 1)], [[]], infix_budget=-1)


@pytest.mark.parametrize(
    "priority_order",
    [(), ("root", "root"), ("affix", "affix"), ("weighted", "root"),
     ("root", "affix", "root"), ("infix", "infix"), ["root", "affix"]],
)
def test_rejects_invalid_priority_orders(priority_order: object) -> None:
    with pytest.raises(ValueError, match="distinct supported roles"):
        _trainer(
            [PreparedSequence("ab", (), "word", 1)],
            [[]],
            priority_order=priority_order,  # type: ignore[arg-type]
        )


def test_infix_first_prevents_competing_ku_and_ma_from_consuming_infix(
    tmp_path: Path,
) -> None:
    prepared = [
        PreparedSequence("kumain", (1, 3), "word", 5),
        PreparedSequence("kuku", (), "word", 1000),
        PreparedSequence("mama", (), "word", 900),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(1, 3, "infix")], [], []],
        root_budget=0,
        affix_budget=0,
        infix_budget=1,
        priority_order=("infix",),
    )
    target = len(trainer.vocabulary) + 2
    candidate, report = trainer.train([target])
    baseline, _ = WeightedMorphBPETrainer(prepared, crossing_penalty=32).train([target])
    assert candidate[target].merges[0].result == "um"
    assert baseline[target].merges[0].result == "ku"
    assert report["algorithm"] == "infix_priority_then_weighted"
    assert report["priority_merge_samples"][0]["infix_frequency"] == 5
    assert report["priority_merge_samples"][0]["affix_frequency"] == 0

    encoded = {}
    for name, model in (("candidate", candidate[target]), ("baseline", baseline[target])):
        artifact = tmp_path / name
        export_tokenizer_artifact(model, artifact, metadata={"synthetic_fixture": True})
        runtime = load_runtime_tokenizer(artifact)
        encoding = runtime.encode("kumain")
        assert runtime.decode(encoding.ids) == "kumain"
        encoded[name] = encoding
    assert [token.token for token in encoded["baseline"].tokens] == ["ku", "ma", "i", "n"]
    assert [token.token for token in encoded["candidate"].tokens] == ["k", "um", "a", "i", "n"]
    assert any(
        token.start == 1 and token.end == 3 and token.token == "um"
        for token in encoded["candidate"].tokens
    )


def test_later_global_merge_can_absorb_a_prioritized_infix_at_runtime(tmp_path: Path) -> None:
    prepared = [
        PreparedSequence("kumain", (1, 3), "word", 5),
        PreparedSequence("kuma", (), "word", 1000),
        PreparedSequence("ku", (), "word", 2000),
    ]
    trainer = _trainer(
        prepared,
        [[RoleSpan(1, 3, "infix")], [], []],
        root_budget=0,
        affix_budget=0,
        infix_budget=1,
        priority_order=("infix",),
    )
    target = len(trainer.vocabulary) + 3
    models, _ = trainer.train([target])
    assert [rule.result for rule in models[target].merges] == ["um", "ku", "kum"]
    assert [symbol.text for symbol in trainer.sequences[0].symbols] == ["k", "um", "a", "i", "n"]
    artifact = tmp_path / "late-absorption"
    export_tokenizer_artifact(models[target], artifact, metadata={"synthetic_fixture": True})
    runtime = load_runtime_tokenizer(artifact)
    encoding = runtime.encode("kumain")
    assert [token.token for token in encoding.tokens] == ["kum", "a", "i", "n"]
    assert runtime.decode(encoding.ids) == "kumain"


def test_three_role_dynamic_counts_and_budgets_preserve_protected_boundaries() -> None:
    prepared = [
        PreparedSequence("kumain", (1, 3), "word", 5),
        PreparedSequence("ababa", (), "word", 3),
        PreparedSequence("xcd", (), "word", 3),
        PreparedSequence("zz", (), "word", 100),
    ]
    trainer = _trainer(
        prepared,
        [
            [RoleSpan(0, 1, "root"), RoleSpan(1, 3, "infix"), RoleSpan(3, 6, "root")],
            [RoleSpan(0, 5, "root")],
            [RoleSpan(0, 3, "affix")],
            [],
        ],
        root_budget=2,
        affix_budget=1,
        infix_budget=1,
        priority_order=("infix", "root", "affix"),
    )
    merges = 0
    while True:
        fresh = _fresh_counts(trainer)
        for role in ("infix", "root", "affix"):
            assert trainer.role_counts[role] == fresh[role]
        assert trainer.allowed_counts == fresh["allowed"]
        assert trainer.crossing_counts == fresh["crossing"]
        for item, sequence in zip(prepared, trainer.sequences, strict=True):
            assert "".join(symbol.text for symbol in sequence.symbols) == item.surface
            assert all(
                not (symbol.start < boundary < symbol.end)
                for symbol in sequence.symbols for boundary in sequence.protected
            )
        if not trainer._merge_once():
            break
        merges += 1
        assert merges < 30
    assert [event["phase"] for event in trainer.phase_transitions] == [
        "infix", "root", "affix", "weighted"
    ]
    assert trainer.phase_statistics["infix"]["new_vocabulary_tokens"] == 1
    assert trainer.phase_statistics["root"]["new_vocabulary_tokens"] == 2
    assert trainer.phase_statistics["affix"]["new_vocabulary_tokens"] == 1
    assert trainer.phase_statistics["weighted"]["new_vocabulary_tokens"] > 0
    assert trainer.merges[0].result == "um"
