"""Sweep the crossing-penalty axis past weighted_morphbpe_v3's frozen grid
(1, 2, 4, 8) to see where boundary-F1 gains stop, using a self-contained
prepared stream built from the canonical resources/training-lexicon.json
(no external reference dictionaries needed -- see README.md for why this
isn't a byte-identical extension of v3).

Trains penalties 1, 2, 4, 8, 16, 32, 64 at vocab targets 6080/8192/16384,
exports each candidate, then scores every one against the real
data/validation.csv with the same evaluate_candidate() used for the
official selected-candidate.json.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from kapampangan_morphbpe.artifact import export_tokenizer_artifact  # noqa: E402
from kapampangan_morphbpe.evaluation import evaluate_candidate  # noqa: E402
from kapampangan_morphbpe.prepare import (  # noqa: E402
    load_prepared_stream,
    prepare_training_stream,
)
from kapampangan_morphbpe.serialization import write_json  # noqa: E402
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer  # noqa: E402

LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
RUNS_DIR = EXPERIMENT_ROOT / "runs" / "prepared"
STREAM_PATH = RUNS_DIR / "training-stream.jsonl"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
OUTPUT_PATH = REPORTS_DIR / "official-validation-scores.json"

TARGETS = (6080, 8192, 16384)
PENALTIES = (1, 2, 4, 8, 16, 32, 64, 128, 256)


def _tokenizer_card(target: int, penalty: int) -> str:
    return f"""# Weighted MorphBPE penalty-extension tokenizer ({target:,}; penalty {penalty})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Exploratory extension of weighted_morphbpe_v3's crossing-penalty sweep,
trained on the canonical resources/training-lexicon.json (not v2's
adjudicated lexicon -- see this experiment's README.md). Ranks merge pair p
by `allowed_frequency(p) - {penalty} * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root).resolve()

    if not STREAM_PATH.is_file():
        print(f"Preparing training stream from {LEXICON_PATH} (engine=python)...")
        prepare_training_stream(dataset_root, LEXICON_PATH, RUNS_DIR, engine="python")
    prepared = load_prepared_stream(STREAM_PATH)
    print(f"Loaded {len(prepared)} prepared sequences.")

    rows: list[dict[str, Any]] = []
    for penalty in PENALTIES:
        artifact_dirs = {
            target: ARTIFACTS_DIR / f"penalty-{penalty}" / "candidates" / f"vocab-{target}"
            for target in TARGETS
        }
        already_trained = all(
            (directory / "tokenizer-manifest.json").is_file() for directory in artifact_dirs.values()
        )
        if already_trained:
            print(f"penalty={penalty:<3} already trained, reusing artifacts")
        else:
            models, report = WeightedMorphBPETrainer(prepared, penalty).train(list(TARGETS))
            if report.get("protected_boundary_merge_violations") != 0:
                raise AssertionError(f"penalty {penalty} crossed a training boundary")
            for target in TARGETS:
                export_tokenizer_artifact(
                    models[target],
                    artifact_dirs[target],
                    artifact_type="kapampangan_morphbpe",
                    metadata={
                        "candidate": True,
                        "condition": "weighted_morphbpe_penalty_extension",
                        "crossing_penalty": penalty,
                        "current_validation_re_evaluated": True,
                        "held_out_test_used": False,
                        "lexicon_used_at_runtime": False,
                        "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
                        "selection_performed": False,
                        "canonical_lexicon_used_for_training": True,
                    },
                    tokenizer_card=_tokenizer_card(target, penalty),
                )
        for target in TARGETS:
            artifact_dir = artifact_dirs[target]
            eval_report = evaluate_candidate(dataset_root, LEXICON_PATH, artifact_dir)
            metrics = cast(dict[str, Any], eval_report["metrics"])
            boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
            consistency = cast(dict[str, Any], metrics["morphological_consistency"])
            row = {
                "condition": "weighted_morphbpe_canonical_lexicon",
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
            rows.append(row)
            print(
                f"penalty={penalty:<3} vocab={target:<6} "
                f"boundary_f1={boundary['f1']:.4f} "
                f"consistency_f1={consistency['f1']:.4f} "
                f"morph_distance={metrics['morphological_distance']:.4f} "
                f"fertility={metrics['fertility_rate']:.4f}"
            )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUTPUT_PATH,
        {
            "evidence_status": "exploratory_official_validation_evaluation",
            "dataset_root": str(dataset_root),
            "lexicon_path": str(LEXICON_PATH),
            "note": "Canonical-lexicon-trained penalty sweep extending past weighted_morphbpe_v3's "
            "frozen grid (1,2,4,8) to 16,32,64. Not byte-identical to v3 -- see README.md. "
            "No selection performed here.",
            "rows": rows,
        },
    )
    print(f"\nWrote {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
