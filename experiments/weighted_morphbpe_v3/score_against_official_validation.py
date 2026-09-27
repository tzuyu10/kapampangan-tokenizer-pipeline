"""Score the 12 already-trained weighted_morphbpe_v3 artifacts against the
official, sealed data/validation.csv (evaluate_candidate), instead of the
1,197-form training-derived silver audit this experiment originally used.

No training happens here. This only answers: does the crossing-penalty
mechanism hold up on the real validation split, and how does it compare to
the shipped ConstrainedBPETrainer candidate recorded in
configs/selected-candidate.json?
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from kapampangan_morphbpe.evaluation import evaluate_candidate  # noqa: E402
from kapampangan_morphbpe.serialization import read_json, write_json  # noqa: E402

LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
OUTPUT_PATH = REPORTS_DIR / "official-validation-scores.json"

TARGETS = (6080, 8192, 16384)
PENALTIES = (1, 2, 4, 8)


def _selected_candidate_row() -> dict[str, Any]:
    selected = read_json(REPOSITORY_ROOT / "configs/selected-candidate.json")
    if not isinstance(selected, dict):
        raise ValueError("selected-candidate.json malformed")
    metrics = cast(dict[str, Any], selected["selected_metrics"])
    boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
    consistency = cast(dict[str, Any], metrics["morphological_consistency"])
    return {
        "condition": "shipped_constrained_bpe",
        "target_vocabulary_size": selected["selected_target_vocabulary_size"],
        "crossing_penalty": None,
        "boundary_f1": boundary["f1"],
        "consistency_f1": consistency["f1"],
        "morphological_distance": metrics["morphological_distance"],
        "fertility_rate": metrics["fertility_rate"],
        "training_protected_boundary_merge_violations": metrics[
            "training_protected_boundary_merge_violations"
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset-root",
        required=True,
        type=Path,
        help="Directory containing metadata/dataset-manifest.json and data/ "
        "(e.g. C:\\DevTools\\KapampanganTokenizer\\kapampangan-general-corpus-v1)",
    )
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root)

    validation_csv = dataset_root / "data/validation.csv"
    if not validation_csv.is_file():
        raise FileNotFoundError(f"expected {validation_csv} to exist")
    if not LEXICON_PATH.is_file():
        raise FileNotFoundError(f"expected {LEXICON_PATH} to exist")

    rows: list[dict[str, Any]] = [_selected_candidate_row()]
    raw_reports: dict[str, Any] = {}
    for penalty in PENALTIES:
        for target in TARGETS:
            artifact_dir = ARTIFACTS_DIR / f"penalty-{penalty}" / "candidates" / f"vocab-{target}"
            if not artifact_dir.is_dir():
                raise FileNotFoundError(f"expected {artifact_dir} to exist")
            report = evaluate_candidate(dataset_root, LEXICON_PATH, artifact_dir)
            raw_reports[f"penalty-{penalty}/vocab-{target}"] = report
            metrics = cast(dict[str, Any], report["metrics"])
            boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
            consistency = cast(dict[str, Any], metrics["morphological_consistency"])
            rows.append(
                {
                    "condition": "weighted_morphbpe",
                    "target_vocabulary_size": target,
                    "crossing_penalty": penalty,
                    "boundary_f1": boundary["f1"],
                    "consistency_f1": consistency["f1"],
                    "morphological_distance": metrics["morphological_distance"],
                    "fertility_rate": metrics["fertility_rate"],
                    "training_protected_boundary_merge_violations": metrics[
                        "training_protected_boundary_merge_violations"
                    ],
                }
            )
            print(
                f"penalty={penalty:<2} vocab={target:<6} "
                f"boundary_f1={boundary['f1']:.4f} "
                f"consistency_f1={consistency['f1']:.4f} "
                f"morph_distance={metrics['morphological_distance']:.4f} "
                f"fertility={metrics['fertility_rate']:.4f} "
                f"violations={metrics['training_protected_boundary_merge_violations']}"
            )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUTPUT_PATH,
        {
            "evidence_status": "official_validation_evaluation_of_previously_trained_artifacts",
            "dataset_root": str(dataset_root),
            "lexicon_path": str(LEXICON_PATH),
            "note": "Scoring only; no retraining. Compares weighted_morphbpe_v3's already "
            "-trained artifacts against the real data/validation.csv, replacing the "
            "1,197-form silver audit those artifacts were previously judged on. "
            "No selection is performed here.",
            "rows": rows,
            "full_reports": raw_reports,
        },
    )
    print(f"\nWrote {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")

    best = max(
        (row for row in rows if row["condition"] == "weighted_morphbpe"),
        key=lambda row: cast(float, row["boundary_f1"]),
    )
    shipped = rows[0]
    print(
        f"\nBest weighted config on real validation.csv: "
        f"penalty={best['crossing_penalty']} vocab={best['target_vocabulary_size']} "
        f"boundary_f1={best['boundary_f1']:.4f}"
    )
    print(
        f"Shipped ConstrainedBPETrainer (vocab={shipped['target_vocabulary_size']}): "
        f"boundary_f1={shipped['boundary_f1']:.4f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
