"""One consolidated run: score the shipped/original tokenizer and every
richer-lexicon penalty variant (1,2,4,8 official + 16,32,64,128,256 new)
against the real, sealed data/validation.csv, using evaluate_candidate()
-- the same function and gold lexicon (resources/training-lexicon.json)
that produced configs/selected-candidate.json's own numbers.

Consolidates numbers that were previously computed piecemeal across several
ad hoc commands into one reproducible script and one report file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kapampangan_morphbpe.evaluation import evaluate_candidate  # noqa: E402
from kapampangan_morphbpe.serialization import write_json  # noqa: E402

EVAL_LEXICON_PATH = REPO_ROOT / "resources/training-lexicon.json"
V4_ART = REPO_ROOT / "experiments/expanded_morphology_v4/artifacts"
EXT_ART = REPO_ROOT / "experiments/expanded_morphology_v4_penalty_extension_v1/artifacts"
SHIPPED_ART = REPO_ROOT / "artifacts/selected-tokenizer"

VOCAB = 6080
EXISTING_PENALTIES = (1, 2, 4, 8)
NEW_PENALTIES = (16, 32, 64, 128, 256)


def _artifact_for(penalty: int) -> Path:
    base = V4_ART if penalty in EXISTING_PENALTIES else EXT_ART
    return base / f"penalty-{penalty}" / "candidates" / f"vocab-{VOCAB}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root).resolve()

    candidates: list[tuple[str, Path]] = [("original_hard_constrained", SHIPPED_ART)]
    for penalty in (*EXISTING_PENALTIES, *NEW_PENALTIES):
        candidates.append((f"penalty-{penalty}", _artifact_for(penalty)))

    rows: list[dict[str, Any]] = []
    print(f"{'condition':<28} {'boundary_f1':>11} {'consistency_f1':>15} {'morph_dist':>11} {'fertility':>10}")
    for name, artifact_dir in candidates:
        report = evaluate_candidate(dataset_root, EVAL_LEXICON_PATH, artifact_dir)
        metrics = cast(dict[str, Any], report["metrics"])
        boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
        consistency = cast(dict[str, Any], metrics["morphological_consistency"])
        row = {
            "condition": name,
            "artifact_path": str(artifact_dir.relative_to(REPO_ROOT)),
            "target_vocabulary_size": VOCAB,
            "boundary_precision": boundary["precision"],
            "boundary_recall": boundary["recall"],
            "boundary_f1": boundary["f1"],
            "consistency_f1": consistency["f1"],
            "morphological_distance": metrics["morphological_distance"],
            "fertility_rate": metrics["fertility_rate"],
            "character_fallback_rate": metrics["character_fallback_rate"],
            "unknown_fallback_rate": metrics["unknown_fallback_rate"],
            "training_protected_boundary_merge_violations": metrics[
                "training_protected_boundary_merge_violations"
            ],
        }
        rows.append(row)
        print(
            f"{name:<28} {boundary['f1']:>11.4f} {consistency['f1']:>15.4f} "
            f"{metrics['morphological_distance']:>11.4f} {metrics['fertility_rate']:>10.4f}"
        )

    output_path = Path(__file__).resolve().parent / "reports" / "all-conditions-vs-validation-csv.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(
        output_path,
        {
            "evidence_status": "official_evaluate_candidate_methodology_vs_real_validation_csv",
            "dataset_root": str(dataset_root),
            "eval_lexicon_path": str(EVAL_LEXICON_PATH),
            "vocab_size": VOCAB,
            "rows": rows,
        },
    )
    print(f"\nWrote {output_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
