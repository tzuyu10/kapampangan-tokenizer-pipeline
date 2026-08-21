from __future__ import annotations

from kapampangan_morphbpe.bpe import ConstrainedBPETrainer
from kapampangan_morphbpe.constants import SPECIAL_TOKENS
from kapampangan_morphbpe.models import PreparedSequence
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer


def _prepared() -> list[PreparedSequence]:
    return [
        PreparedSequence("ab", (1,), "word", 100),
        PreparedSequence("abx", (), "word", 120),
        PreparedSequence("ac", (), "word", 110),
    ]


def test_zero_penalty_matches_paper_aligned_constrained_bpe() -> None:
    target = len(SPECIAL_TOKENS) + 4 + 3
    expected, _expected_report = ConstrainedBPETrainer(_prepared()).train([target])
    actual, report = WeightedMorphBPETrainer(_prepared(), crossing_penalty=0).train([target])

    assert actual[target].to_dict() == expected[target].to_dict()
    assert report["crossing_penalty"] == 0
    assert report["surface_specific_runtime_guarantees"] == []


def test_crossing_penalty_downranks_globally_conflicted_pair() -> None:
    target = len(SPECIAL_TOKENS) + 4 + 1
    unweighted, _ = WeightedMorphBPETrainer(_prepared(), crossing_penalty=0).train([target])
    weighted, report = WeightedMorphBPETrainer(_prepared(), crossing_penalty=2).train([target])

    assert (unweighted[target].merges[0].left, unweighted[target].merges[0].right) == (
        "a",
        "b",
    )
    assert (weighted[target].merges[0].left, weighted[target].merges[0].right) == (
        "b",
        "x",
    )
    assert report["algorithm"] == "allowed_frequency_minus_crossing_penalty"
    assert report["protected_boundary_merge_violations"] == 0


def test_weighted_training_rejects_invalid_inputs() -> None:
    try:
        WeightedMorphBPETrainer([], crossing_penalty=1)
    except ValueError as error:
        assert str(error) == "weighted MorphBPE training requires prepared sequences"
    else:
        raise AssertionError("empty training input should have been rejected")

    try:
        WeightedMorphBPETrainer(_prepared(), crossing_penalty=-1)
    except ValueError as error:
        assert str(error) == "crossing penalty must be non-negative"
    else:
        raise AssertionError("negative crossing penalty should have been rejected")
