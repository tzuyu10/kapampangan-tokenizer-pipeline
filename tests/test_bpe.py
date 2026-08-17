from __future__ import annotations

from kapampangan_morphbpe.bpe import ConstrainedBPETrainer
from kapampangan_morphbpe.models import PreparedSequence


def test_deterministic_pair_tie_uses_lexical_pair_order() -> None:
    prepared = [
        PreparedSequence("ab", (), "word", 1),
        PreparedSequence("ac", (), "word", 1),
    ]
    initial_size = 4 + 3
    models, report = ConstrainedBPETrainer(prepared).train([initial_size + 1])
    model = models[initial_size + 1]
    assert model.merges[0].left == "a"
    assert model.merges[0].right == "b"
    assert report["protected_boundary_merge_violations"] == 0


def test_protected_boundary_pair_is_never_merged() -> None:
    prepared = [
        PreparedSequence("masulat", (2,), "word", 10),
        PreparedSequence("sulat", (), "word", 2),
    ]
    initial_size = 4 + len(set("masulat"))
    models, _ = ConstrainedBPETrainer(prepared).train([initial_size + 4])
    model = models[initial_size + 4]
    assert all(
        not (merge.left.endswith("a") and merge.right.startswith("s")) for merge in model.merges
    )
    assert model.protected_boundary_merge_violations == 0


def test_repeated_training_is_identical() -> None:
    prepared = [
        PreparedSequence("abab", (), "word", 4),
        PreparedSequence("abac", (2,), "word", 3),
    ]
    initial_size = 4 + len(set("abac"))
    first, _ = ConstrainedBPETrainer(prepared).train([initial_size + 3])
    second, _ = ConstrainedBPETrainer(prepared).train([initial_size + 3])
    assert first[initial_size + 3].to_dict() == second[initial_size + 3].to_dict()
