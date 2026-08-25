from __future__ import annotations

import random
from typing import cast

import pytest

from kapampangan_morphbpe.constants import SPECIAL_TOKENS
from kapampangan_morphbpe.models import PreparedSequence
from kapampangan_morphbpe.stochastic_bpe import (
    _MAX_STALLED_ROUNDS,
    StochasticWeightedMorphBPETrainer,
)
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer


def _prepared() -> list[PreparedSequence]:
    return [
        PreparedSequence("ab", (1,), "word", 100),
        PreparedSequence("abx", (), "word", 120),
        PreparedSequence("ac", (), "word", 110),
    ]


def test_zero_dropout_matches_weighted_morphbpe() -> None:
    target = len(SPECIAL_TOKENS) + 4 + 3
    expected, _expected_report = WeightedMorphBPETrainer(_prepared(), crossing_penalty=2).train(
        [target]
    )
    actual, report = StochasticWeightedMorphBPETrainer(
        _prepared(), crossing_penalty=2, dropout_rate=0.0, seed=7
    ).train([target])

    assert actual[target].to_dict() == expected[target].to_dict()
    assert report["dropout_rate"] == 0.0
    assert report["dropped_occurrences"] == 0
    assert report["fully_dropped_rounds"] == 0
    assert report["surface_specific_runtime_guarantees"] == []


def test_repeated_training_with_dropout_is_byte_identical() -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 10),
        PreparedSequence("abz", (), "word", 10),
        PreparedSequence("aby", (), "word", 10),
        PreparedSequence("abw", (), "word", 10),
        PreparedSequence("cd", (), "word", 35),
    ]
    target = 16
    first, first_report = StochasticWeightedMorphBPETrainer(
        prepared, crossing_penalty=0, dropout_rate=0.6, seed=5
    ).train([target])
    second, second_report = StochasticWeightedMorphBPETrainer(
        prepared, crossing_penalty=0, dropout_rate=0.6, seed=5
    ).train([target])

    assert first[target].to_dict() == second[target].to_dict()
    assert first_report == second_report
    # The dropout mechanism actually fired for this corpus/seed/rate.
    assert cast(int, first_report["dropped_occurrences"]) > 0


def test_different_seeds_can_produce_different_dropout_counts() -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 10),
        PreparedSequence("abz", (), "word", 10),
        PreparedSequence("aby", (), "word", 10),
        PreparedSequence("abw", (), "word", 10),
        PreparedSequence("cd", (), "word", 35),
    ]
    target = 16
    dropped_counts = {
        StochasticWeightedMorphBPETrainer(
            prepared, crossing_penalty=0, dropout_rate=0.6, seed=seed
        ).train([target])[1]["dropped_occurrences"]
        for seed in range(10)
    }
    assert len(dropped_counts) > 1


def test_duplicate_merge_from_leftover_dropout_occurrences_is_not_double_logged() -> None:
    # A dominant pair ((a,b), allowed count 40) can still be selected again
    # in a later round for occurrences that survived an earlier round's
    # dropout; the resulting (a, b) -> ab merge already exists in the
    # vocabulary, so it must not be logged a second time in `merges`.
    prepared = [
        PreparedSequence("ab", (), "word", 10),
        PreparedSequence("abz", (), "word", 10),
        PreparedSequence("aby", (), "word", 10),
        PreparedSequence("abw", (), "word", 10),
        PreparedSequence("cd", (), "word", 35),
    ]
    target = 16
    model, report = StochasticWeightedMorphBPETrainer(
        prepared, crossing_penalty=0, dropout_rate=0.6, seed=0
    ).train([target])
    pairs = [(merge.left, merge.right) for merge in model[target].merges]
    assert len(pairs) == len(set(pairs))
    assert cast(int, report["dropped_occurrences"]) > 0


def test_protected_boundary_never_crossed_regardless_of_dropout_rate() -> None:
    prepared = [
        PreparedSequence("masulat", (2,), "word", 10),
        PreparedSequence("sulat", (), "word", 2),
    ]
    initial_size = 4 + len(set("masulat"))
    for dropout_rate in (0.0, 0.3, 0.7, 0.99):
        model, report = StochasticWeightedMorphBPETrainer(
            prepared, crossing_penalty=4, dropout_rate=dropout_rate, seed=1
        ).train([initial_size + 4])
        merges = model[initial_size + 4].merges
        assert all(
            not (merge.left.endswith("a") and merge.right.startswith("s")) for merge in merges
        )
        assert report["protected_boundary_merge_violations"] == 0


def test_same_pair_allowed_at_one_position_and_protected_at_another_in_one_word() -> None:
    # Regression test for a real bug found training on the full v4 corpus:
    # "abcab" with a protected boundary at 4 means the (a, b) pair is
    # *allowed* at its first occurrence (positions 0-1) but *crossing* at
    # its second occurrence (positions 3-4) in the very same word. An
    # earlier version of _apply_allowed_pair_with_dropout treated any
    # protected-position match of a selected "allowed" pair as a fatal
    # AssertionError, instead of silently leaving that one occurrence
    # unmerged (matching weighted_bpe.py's own _apply_allowed_pair). This
    # never surfaced in small synthetic corpora -- only training on the
    # real, much larger corpus hit a case where the pair selected as
    # globally allowed also happened to recur at a protected position
    # within one word.
    prepared = [
        PreparedSequence("abcab", (4,), "word", 50),
        PreparedSequence("cd", (), "word", 10),
    ]
    target = 4 + len(set("abcabcd")) + 2
    model, report = StochasticWeightedMorphBPETrainer(
        prepared, crossing_penalty=0, dropout_rate=0.3, seed=1
    ).train([target])
    assert report["protected_boundary_merge_violations"] == 0
    assert [(merge.left, merge.right) for merge in model[target].merges] == [
        ("a", "b"),
        ("ab", "c"),
    ]


def test_stochastic_training_rejects_invalid_inputs() -> None:
    try:
        StochasticWeightedMorphBPETrainer([], crossing_penalty=1, dropout_rate=0.1, seed=0)
    except ValueError as error:
        assert str(error) == "stochastic MorphBPE training requires prepared sequences"
    else:
        raise AssertionError("empty training input should have been rejected")

    try:
        StochasticWeightedMorphBPETrainer(
            _prepared(), crossing_penalty=-1, dropout_rate=0.1, seed=0
        )
    except ValueError as error:
        assert str(error) == "crossing penalty must be non-negative"
    else:
        raise AssertionError("negative crossing penalty should have been rejected")

    for bad_rate in (-0.1, 1.0, 1.5):
        try:
            StochasticWeightedMorphBPETrainer(
                _prepared(), crossing_penalty=1, dropout_rate=bad_rate, seed=0
            )
        except ValueError as error:
            assert str(error) == "dropout_rate must be in [0.0, 1.0)"
        else:
            raise AssertionError(f"dropout_rate={bad_rate} should have been rejected")


def test_pathological_dropout_rate_raises_instead_of_looping_forever(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Force every dropout draw to land below any positive dropout_rate, so
    # the selected pair's occurrences are always skipped and training can
    # never make vocabulary progress -- exercising the defensive
    # _MAX_STALLED_ROUNDS cap instead of hanging.
    monkeypatch.setattr(random.Random, "random", lambda self: 0.0)
    target = len(SPECIAL_TOKENS) + 4 + 1
    trainer = StochasticWeightedMorphBPETrainer(
        _prepared(), crossing_penalty=0, dropout_rate=0.5, seed=0
    )
    with pytest.raises(AssertionError, match="stalled training"):
        trainer.train([target])
    assert trainer.fully_dropped_rounds >= _MAX_STALLED_ROUNDS
