from __future__ import annotations

from pathlib import Path

from kapampangan_morphbpe.artifact import export_tokenizer_artifact
from kapampangan_morphbpe.boundary_safe_bpe import BoundarySafeBPETrainer
from kapampangan_morphbpe.models import PreparedSequence
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer


def test_boundary_safe_training_defers_crossing_pair_and_keeps_standard_runtime_safe(
    tmp_path: Path,
) -> None:
    prepared = [
        PreparedSequence("ka", (), "word", 100),
        PreparedSequence("kab", (), "word", 200),
        PreparedSequence("bukas", (), "word", 80),
        PreparedSequence("an", (), "word", 70),
        PreparedSequence("kabukasan", (2, 7), "word", 50),
    ]
    audit = [PreparedSequence("kabukasan", (2, 7), "word", 1)]
    models, report = BoundarySafeBPETrainer(prepared, audit).train([16])

    assert report["trained_targets"] == [16]
    assert report["protected_boundary_merge_violations"] == 0
    assert report["runtime_boundary_deferred_candidate_events"] >= 1
    deferred = report["runtime_boundary_deferred_pairs"]
    assert any(item["left"] == "ka" and item["right"] == "b" for item in deferred)  # type: ignore[union-attr]

    artifact = tmp_path / "safe"
    export_tokenizer_artifact(models[16], artifact, metadata={"condition": "boundary_safe"})
    encoding = load_runtime_tokenizer(artifact).encode("kabukasan")
    assert all(
        not token.start < boundary < token.end for token in encoding.tokens for boundary in (2, 7)
    )
    assert load_runtime_tokenizer(artifact).decode(encoding.ids) == "kabukasan"


def test_boundary_safe_training_requires_real_audit_boundaries() -> None:
    prepared = [PreparedSequence("ab", (), "word", 1)]
    audit = [PreparedSequence("ab", (), "word", 1)]

    try:
        BoundarySafeBPETrainer(prepared, audit)
    except ValueError as error:
        assert str(error) == "boundary audit sequences must contain a protected boundary"
    else:
        raise AssertionError("boundary-free audit input should have been rejected")
