"""Train the new crossing_penalty=64 configuration on the exact prepared
stream that produced the real (already-shipped-in-the-webapp)
expanded_morphology_v4 penalty-1/2/4/8 artifacts -- verified byte-identical
provenance, see README.md. Evaluates against the real data/validation.csv
using the same resources/training-lexicon.json gold lexicon used
everywhere else in this session, for direct comparability.
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
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer  # noqa: E402

INPUTS_DIR = EXPERIMENT_ROOT / "inputs"
STREAM_PATH = INPUTS_DIR / "training-stream.jsonl"
EXPECTED_STREAM_SHA256 = "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7"

EVAL_LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
OUTPUT_PATH = REPORTS_DIR / "official-validation-scores.json"

TARGETS = (6080, 8192, 16384)
PENALTIES = (16, 32, 64, 128, 256)


def _tokenizer_card(target: int, penalty: int) -> str:
    return f"""# expanded_morphology_v4 penalty-{penalty} extension tokenizer ({target:,})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Extends the frozen expanded_morphology_v4 penalty-1/2/4/8 grid to
crossing_penalty={penalty}, trained on the exact prepared stream (verified
byte-identical provenance -- see README.md) that produced the real,
already-deployed penalty-1/2/4/8 artifacts. Ranks merge pair p by
`allowed_frequency(p) - {penalty} * crossing_frequency(p)`. Inference is
ordinary lexicon-free BPE. Not selected, not a frozen thesis artifact.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root).resolve()

    actual_sha256 = sha256_file(STREAM_PATH)
    if actual_sha256 != EXPECTED_STREAM_SHA256:
        raise ValueError(
            f"training-stream.jsonl sha256 mismatch: expected {EXPECTED_STREAM_SHA256}, "
            f"got {actual_sha256} -- refusing to train on an unverified stream"
        )

    prepared = load_prepared_stream(STREAM_PATH)
    print(f"Loaded {len(prepared)} prepared sequences (verified sha256 match).")

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
                raise AssertionError(f"penalty={penalty} crossed a training boundary")
            print(f"Trained penalty={penalty}: {report['merge_rules_learned']} merges learned.")
            for target in TARGETS:
                export_tokenizer_artifact(
                    models[target],
                    artifact_dirs[target],
                    artifact_type="kapampangan_morphbpe",
                    metadata={
                        "candidate": True,
                        "condition": f"penalty-{penalty}",
                        "crossing_penalty": penalty,
                        "current_validation_re_evaluated": True,
                        "held_out_test_used": False,
                        "lexicon_used_at_runtime": False,
                        "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
                        "selection_performed": False,
                        "training_stream_source": "expanded_morphology_v4 (verified byte-identical "
                        "to the stream that produced the real penalty-1/2/4/8 artifacts)",
                        "training_stream_sha256": actual_sha256,
                    },
                    tokenizer_card=_tokenizer_card(target, penalty),
                )
        for target in TARGETS:
            artifact_dir = artifact_dirs[target]
            eval_report = evaluate_candidate(dataset_root, EVAL_LEXICON_PATH, artifact_dir)
            metrics = cast(dict[str, Any], eval_report["metrics"])
            boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
            consistency = cast(dict[str, Any], metrics["morphological_consistency"])
            row = {
                "condition": "penalty_expanded_morphology_v4_stream",
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
                f"penalty={penalty:<3} vocab={target:<6} boundary_f1={boundary['f1']:.4f} "
                f"consistency_f1={consistency['f1']:.4f} "
                f"morph_distance={metrics['morphological_distance']:.4f} "
                f"fertility={metrics['fertility_rate']:.4f}"
            )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        OUTPUT_PATH,
        {
            "evidence_status": "official_validation_evaluation_of_newly_trained_artifact",
            "dataset_root": str(dataset_root),
            "eval_lexicon_path": str(EVAL_LEXICON_PATH),
            "training_stream_sha256": actual_sha256,
            "note": "penalty=64 trained on the verified expanded_morphology_v4 stream "
            "(3,311-root lexicon, rule-refined). See README.md for provenance "
            "verification. No selection performed here.",
            "rows": rows,
        },
    )
    print(f"\nWrote {OUTPUT_PATH.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
