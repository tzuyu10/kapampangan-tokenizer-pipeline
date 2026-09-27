"""Recommendation #3: soften BoundarySafeBPETrainer's hard defer into a
penalty, combined with recommendations #1 (dropout) and #2 (fine-tuned
penalty) via HybridBoundaryPenaltyBPETrainer.

Base configuration: crossing_penalty=36, dropout_rate=0.05 (the winning
"+1+2" combo from step1, confirmed against the authoritative reference).
Sweeps runtime_penalty (the new mechanism) on top of that base, using ALL
9,026 training-stream words with a resolved protected-boundary analysis as
the runtime-order audit set (not an arbitrary sample -- full coverage,
confirmed tractable: ~45s per run).

This produces the "+1+2+3" candidates for the final comparison table.
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
from kapampangan_morphbpe.hybrid_boundary_penalty_bpe import (  # noqa: E402
    HybridBoundaryPenaltyBPETrainer,
)
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402

STREAM_PATH = (
    REPO_ROOT
    / "experiments/expanded_morphology_v4_penalty_extension_v1/inputs/training-stream.jsonl"
)
EXPECTED_STREAM_SHA256 = "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7"
EVAL_LEXICON_PATH = REPO_ROOT / "resources/training-lexicon.json"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts" / "hybrid"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"

VOCAB = 6080
BASE_CROSSING_PENALTY = 36
BASE_DROPOUT = 0.05
SEED = 20260913
RUNTIME_PENALTIES = (1, 4, 16, 64)


def _card(label: str) -> str:
    return f"""# training_improvements_v1 hybrid candidate: {label}

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Recommendation #3: HybridBoundaryPenaltyBPETrainer, combining the proven
crossing-frequency penalty with a NEW soft runtime-order-audit penalty
(BoundarySafeBPETrainer's mechanism, softened from a hard defer). This
mechanism has not been validated before this experiment -- exploratory.
Not selected, not a frozen thesis artifact.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True, type=Path)
    args = parser.parse_args()
    dataset_root = cast(Path, args.dataset_root).resolve()

    actual_sha256 = sha256_file(STREAM_PATH)
    if actual_sha256 != EXPECTED_STREAM_SHA256:
        raise ValueError("training-stream.jsonl sha256 mismatch -- refusing to train")
    prepared = load_prepared_stream(STREAM_PATH)
    audit = [p for p in prepared if p.kind == "word" and p.protected_boundaries]
    print(f"Loaded {len(prepared)} prepared sequences, {len(audit)} audit words.\n")

    rows: list[dict[str, Any]] = []
    for runtime_penalty in RUNTIME_PENALTIES:
        label = f"crossing36_dropout0.05_runtime{runtime_penalty}"
        artifact_dir = ARTIFACTS_DIR / f"runtime-{runtime_penalty}"
        if not (artifact_dir / "tokenizer-manifest.json").is_file():
            trainer = HybridBoundaryPenaltyBPETrainer(
                prepared,
                audit,
                crossing_penalty=BASE_CROSSING_PENALTY,
                runtime_penalty=runtime_penalty,
                dropout_rate=BASE_DROPOUT,
                seed=SEED,
            )
            models, report = trainer.train([VOCAB])
            if report.get("protected_boundary_merge_violations") != 0:
                raise AssertionError(f"runtime_penalty={runtime_penalty} crossed a training boundary")
            print(
                f"trained runtime_penalty={runtime_penalty}: "
                f"{report['merge_rules_learned']} merges, "
                f"fully_dropped_rounds={report['fully_dropped_rounds']}"
            )
            export_tokenizer_artifact(
                models[VOCAB],
                artifact_dir,
                artifact_type="kapampangan_morphbpe",
                metadata={
                    "candidate": True,
                    "condition": "hybrid_boundary_penalty",
                    "crossing_penalty": BASE_CROSSING_PENALTY,
                    "runtime_penalty": runtime_penalty,
                    "dropout_rate": BASE_DROPOUT,
                    "seed": SEED,
                    "audit_sequence_count": len(audit),
                    "training_stream_sha256": actual_sha256,
                    "selection_performed": False,
                },
                tokenizer_card=_card(label),
            )
        report = evaluate_candidate(dataset_root, EVAL_LEXICON_PATH, artifact_dir)
        metrics = cast(dict[str, Any], report["metrics"])
        boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
        consistency = cast(dict[str, Any], metrics["morphological_consistency"])
        row = {
            "label": label,
            "crossing_penalty": BASE_CROSSING_PENALTY,
            "runtime_penalty": runtime_penalty,
            "dropout_rate": BASE_DROPOUT,
            "boundary_f1": boundary["f1"],
            "consistency_f1": consistency["f1"],
            "morphological_distance": metrics["morphological_distance"],
            "fertility_rate": metrics["fertility_rate"],
        }
        rows.append(row)
        print(
            f"  eval: boundary_f1={boundary['f1']:.4f} consistency_f1={consistency['f1']:.4f} "
            f"morph_distance={metrics['morphological_distance']:.4f} fertility={metrics['fertility_rate']:.4f}"
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(REPORTS_DIR / "step2-hybrid-runtime-penalty.json", {"vocab": VOCAB, "rows": rows})
    print(f"\nWrote {REPORTS_DIR / 'step2-hybrid-runtime-penalty.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
