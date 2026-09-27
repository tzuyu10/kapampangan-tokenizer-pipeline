"""Recommendations #1 and #2 from the training-improvement discussion:

#2 (fine-grained penalty search): the coarse power-of-2 grid (16/32/64)
   showed a peak between 16 and 32. Fill in 20/24/28/36/40/44/48 to see if
   a non-power-of-2 value beats the current best (penalty=32).

#1 (BPE-dropout): apply StochasticWeightedMorphBPETrainer's dropout_rate
   on top of BOTH the current deployed penalty (32) and whatever wins the
   fine-grained search, to see if regularization improves generalization
   (the DEV->TEST gap) independent of which penalty is used.

Reuses the exact same verified training stream as
expanded_morphology_v4_penalty_extension_v1 (byte-identical provenance to
the real, already-deployed penalty-1/2/4/8/16/32/64 artifacts). Vocab fixed
at 6,080 -- the vocab already established as best for this lexicon.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from kapampangan_morphbpe.artifact import export_tokenizer_artifact  # noqa: E402
from kapampangan_morphbpe.evaluation import evaluate_candidate  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402
from kapampangan_morphbpe.stochastic_bpe import StochasticWeightedMorphBPETrainer  # noqa: E402
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer  # noqa: E402

STREAM_PATH = (
    REPO_ROOT
    / "experiments/expanded_morphology_v4_penalty_extension_v1/inputs/training-stream.jsonl"
)
EXPECTED_STREAM_SHA256 = "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7"
EVAL_LEXICON_PATH = REPO_ROOT / "resources/training-lexicon.json"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"

VOCAB = 6080
FINE_PENALTIES = (20, 24, 28, 36, 40, 44, 48)
DROPOUT_RATES = (0.05, 0.10, 0.20)
CURRENT_BEST_PENALTY = 32
SEED = 20260913


def _card(label: str) -> str:
    return f"""# training_improvements_v1 candidate: {label}

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Exploratory candidate testing training-time improvements beyond the
deployed penalty-32 tokenizer. Not selected, not a frozen thesis artifact.
"""


def _eval_row(dataset_root: Path, artifact_dir: Path, label: str, extra: dict[str, Any]) -> dict[str, Any]:
    report = evaluate_candidate(dataset_root, EVAL_LEXICON_PATH, artifact_dir)
    metrics = cast(dict[str, Any], report["metrics"])
    boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
    consistency = cast(dict[str, Any], metrics["morphological_consistency"])
    row = {
        "label": label,
        "boundary_f1": boundary["f1"],
        "consistency_f1": consistency["f1"],
        "morphological_distance": metrics["morphological_distance"],
        "fertility_rate": metrics["fertility_rate"],
        "training_protected_boundary_merge_violations": metrics[
            "training_protected_boundary_merge_violations"
        ],
        **extra,
    }
    print(
        f"{label:<28} boundary_f1={boundary['f1']:.4f} consistency_f1={consistency['f1']:.4f} "
        f"morph_distance={metrics['morphological_distance']:.4f} fertility={metrics['fertility_rate']:.4f}"
    )
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root).resolve()

    actual_sha256 = sha256_file(STREAM_PATH)
    if actual_sha256 != EXPECTED_STREAM_SHA256:
        raise ValueError("training-stream.jsonl sha256 mismatch -- refusing to train")
    prepared = load_prepared_stream(STREAM_PATH)
    print(f"Loaded {len(prepared)} prepared sequences (verified sha256 match).\n")

    rows: list[dict[str, Any]] = []

    print("=== Fine-grained penalty search (recommendation #2) ===")
    fine_grid_f1: dict[int, float] = {}
    for penalty in FINE_PENALTIES:
        artifact_dir = ARTIFACTS_DIR / "fine_penalty" / f"penalty-{penalty}"
        if not (artifact_dir / "tokenizer-manifest.json").is_file():
            models, report = WeightedMorphBPETrainer(prepared, penalty).train([VOCAB])
            if report.get("protected_boundary_merge_violations") != 0:
                raise AssertionError(f"penalty={penalty} crossed a training boundary")
            export_tokenizer_artifact(
                models[VOCAB],
                artifact_dir,
                artifact_type="kapampangan_morphbpe",
                metadata={
                    "candidate": True,
                    "condition": f"fine_penalty_{penalty}",
                    "crossing_penalty": penalty,
                    "training_stream_sha256": actual_sha256,
                    "selection_performed": False,
                },
                tokenizer_card=_card(f"fine penalty={penalty}"),
            )
        row = _eval_row(
            dataset_root, artifact_dir, f"penalty={penalty}", {"crossing_penalty": penalty, "dropout_rate": 0.0}
        )
        rows.append(row)
        fine_grid_f1[penalty] = row["boundary_f1"]

    best_fine_penalty = max(fine_grid_f1, key=lambda p: fine_grid_f1[p])
    print(f"\nBest fine-grained penalty: {best_fine_penalty} (F1={fine_grid_f1[best_fine_penalty]:.4f})")
    print(f"(for reference, penalty=32 itself scores as already known: see prior report)\n")

    print("=== BPE-dropout sweep at CURRENT deployed penalty=32 (recommendation #1 only) ===")
    dropout_at_32_f1: dict[float, float] = {}
    for dropout in DROPOUT_RATES:
        label = f"penalty=32_dropout={dropout}"
        artifact_dir = ARTIFACTS_DIR / "dropout_at_32" / f"dropout-{dropout}"
        if not (artifact_dir / "tokenizer-manifest.json").is_file():
            models, report = StochasticWeightedMorphBPETrainer(
                prepared, CURRENT_BEST_PENALTY, dropout, SEED
            ).train([VOCAB])
            if report.get("protected_boundary_merge_violations") != 0:
                raise AssertionError(f"dropout={dropout} crossed a training boundary")
            export_tokenizer_artifact(
                models[VOCAB],
                artifact_dir,
                artifact_type="kapampangan_morphbpe",
                metadata={
                    "candidate": True,
                    "condition": "dropout_at_current_best",
                    "crossing_penalty": CURRENT_BEST_PENALTY,
                    "dropout_rate": dropout,
                    "seed": SEED,
                    "training_stream_sha256": actual_sha256,
                    "selection_performed": False,
                },
                tokenizer_card=_card(label),
            )
        row = _eval_row(
            dataset_root, artifact_dir, label, {"crossing_penalty": CURRENT_BEST_PENALTY, "dropout_rate": dropout}
        )
        rows.append(row)
        dropout_at_32_f1[dropout] = row["boundary_f1"]

    best_dropout = max(dropout_at_32_f1, key=lambda d: dropout_at_32_f1[d])
    print(f"\nBest dropout rate at penalty=32: {best_dropout} (F1={dropout_at_32_f1[best_dropout]:.4f})\n")

    print(f"=== Combo #1+#2: best fine penalty ({best_fine_penalty}) + best dropout ({best_dropout}) ===")
    combo_label = f"penalty={best_fine_penalty}_dropout={best_dropout}"
    combo_artifact_dir = ARTIFACTS_DIR / "combo_1_2" / "candidate"
    if not (combo_artifact_dir / "tokenizer-manifest.json").is_file():
        models, report = StochasticWeightedMorphBPETrainer(
            prepared, best_fine_penalty, best_dropout, SEED
        ).train([VOCAB])
        if report.get("protected_boundary_merge_violations") != 0:
            raise AssertionError("combo 1+2 crossed a training boundary")
        export_tokenizer_artifact(
            models[VOCAB],
            combo_artifact_dir,
            artifact_type="kapampangan_morphbpe",
            metadata={
                "candidate": True,
                "condition": "combo_dropout_plus_fine_penalty",
                "crossing_penalty": best_fine_penalty,
                "dropout_rate": best_dropout,
                "seed": SEED,
                "training_stream_sha256": actual_sha256,
                "selection_performed": False,
            },
            tokenizer_card=_card(combo_label),
        )
    row = _eval_row(
        dataset_root, combo_artifact_dir, combo_label,
        {"crossing_penalty": best_fine_penalty, "dropout_rate": best_dropout},
    )
    rows.append(row)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        REPORTS_DIR / "step1-fine-penalty-and-dropout.json",
        {
            "vocab": VOCAB,
            "training_stream_sha256": actual_sha256,
            "best_fine_penalty": best_fine_penalty,
            "best_dropout_at_32": best_dropout,
            "combo_1_2": {"penalty": best_fine_penalty, "dropout": best_dropout},
            "rows": rows,
        },
    )
    print(f"\nWrote {REPORTS_DIR / 'step1-fine-penalty-and-dropout.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
