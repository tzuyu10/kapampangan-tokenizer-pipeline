"""Train a new, explicitly-labeled MorphBPE extension: `StochasticWeightedMorphBPETrainer`
(`src/kapampangan_morphbpe/stochastic_bpe.py`), which adds train-time-only
stochastic dropout of intra-morpheme merge applications on top of
`WeightedMorphBPETrainer`'s existing penalty score. Boundary-crossing merges
remain strictly forbidden, exactly like every other condition in this
repository; only how the merge table was learned differs. The exported
artifact uses ordinary, fully deterministic, lexicon-free greedy BPE
inference -- identical in kind to `plain`/`penalty-*`/every other condition
here (`lexicon_used_at_runtime: false`).

This is NOT the unmodified MorphBPE algorithm from Asgari et al. (2025), nor
a literal reproduction of BPE-dropout (Provilkov et al., 2020) or Unigram's
own subword sampling -- it is a new, clearly-labeled thesis extension, in
the same spirit as the existing weighted-penalty conditions
(`weighted_morphbpe_v3`, this experiment's own `penalty-*`). See
`stochastic_bpe.py`'s module docstring for the exact mechanism and its
determinism guarantee (seeded RNG, fixed traversal order -> two independent
training runs with the same seed produce byte-identical results, verified
below exactly like every other trainer in this repository).

Trains at a fixed crossing_penalty=4 (this experiment's own established
"representative mid-grid" choice) crossed with two dropout rates (0.1, 0.2)
at all three vocabulary sizes (6,080/8,192/16,384), on the exact same
morphology-resegmented stream (`runs/prepared/training-stream.jsonl`) the
`penalty-*` conditions already train on. Reuses `run_experiment.py`'s own
boundary-F1/MCF1 evaluation functions directly (this trainer produces a
real `RuntimeTokenizer`-protocol artifact via the same
`export_tokenizer_artifact` pipeline, unlike the Unigram ablation, which
needed its own parallel metric implementation because it is not built on
this project's runtime bridge).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(EXPERIMENT_ROOT))

import run_experiment as v4run  # noqa: E402

from kapampangan_morphbpe.artifact import (  # noqa: E402
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json  # noqa: E402
from kapampangan_morphbpe.stochastic_bpe import StochasticWeightedMorphBPETrainer  # noqa: E402

TARGETS = (6080, 8192, 16384)
CROSSING_PENALTY = 4
DROPOUT_RATES = (0.1, 0.2)
# Fixed, documented seed (this session's date) so training is reproducible
# by construction, not by accident -- matches this trainer's own
# determinism contract (see stochastic_bpe.py).
SEED = 20260822

ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
TRAINING_REPORT_PATH = REPORTS_DIR / "stochastic-morphbpe-training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "stochastic-morphbpe-runtime-evaluation.json"

# Every other v4 artifact family that must stay byte-unchanged by this script.
OTHER_V4_ARTIFACT_DIRS = {
    "plain": ARTIFACTS_DIR / "plain",
    "penalty-1": ARTIFACTS_DIR / "penalty-1",
    "penalty-2": ARTIFACTS_DIR / "penalty-2",
    "penalty-4": ARTIFACTS_DIR / "penalty-4",
    "penalty-8": ARTIFACTS_DIR / "penalty-8",
    "unigram-ablation": ARTIFACTS_DIR / "unigram-ablation",
}


def _condition_name(dropout_rate: float) -> str:
    return f"stochastic-p{CROSSING_PENALTY}-d{dropout_rate:g}"


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        return {}
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_other_artifacts() -> dict[str, dict[str, str]]:
    return {name: _directory_hashes(path) for name, path in OTHER_V4_ARTIFACT_DIRS.items()}


def _tokenizer_card(condition: str, target: int, dropout_rate: float) -> str:
    return f"""# Expanded morphology v4 tokenizer ({condition}; {target:,})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Stochastic MorphBPE thesis extension (NOT the unmodified MorphBPE paper
algorithm, and NOT a literal reproduction of BPE-dropout or Unigram subword
sampling). Built on WeightedMorphBPETrainer's own scoring
(`allowed_frequency(p) - {CROSSING_PENALTY} * crossing_frequency(p)`,
summed globally across the v4-resegmented training corpus), plus train-time
-only stochastic dropout: each individual allowed (never boundary-crossing)
occurrence of the selected merge pair is skipped with probability
{dropout_rate:g} (seed {SEED}), so the trained vocabulary is exposed to
more than one greedy segmentation path per word during training. A merge is
still never applied across a protected boundary. Standard runtime is
ordinary, fully deterministic, lexicon-free BPE -- morphology and dropout
only affect merge learning; nothing about inference changes. Not
independently evaluated on held-out data.
"""


def train() -> dict[str, Any]:
    before = _snapshot_other_artifacts()
    prepared_manifest = v4run._verified_prepared_inputs()
    morph = load_prepared_stream(v4run.STREAM_PATH)

    family_reports: dict[str, object] = {}
    manifests: dict[str, object] = {}

    for dropout_rate in DROPOUT_RATES:
        condition = _condition_name(dropout_rate)
        first, first_report = StochasticWeightedMorphBPETrainer(
            morph, CROSSING_PENALTY, dropout_rate, SEED
        ).train(list(TARGETS))
        second, second_report = StochasticWeightedMorphBPETrainer(
            morph, CROSSING_PENALTY, dropout_rate, SEED
        ).train(list(TARGETS))
        if first_report != second_report:
            raise AssertionError(f"{condition} training report differs on rebuild")
        if first_report.get("trained_targets") != list(TARGETS):
            raise AssertionError(f"{condition} failed to reach every target")
        if first_report.get("protected_boundary_merge_violations") != 0:
            raise AssertionError(f"{condition} crossed a training boundary")
        for target in TARGETS:
            if first[target].to_dict() != second[target].to_dict():
                raise AssertionError(f"{condition} target {target} in-memory rebuild differs")
        family_reports[condition] = first_report

        condition_manifests: dict[str, object] = {}
        for target in TARGETS:
            metadata: dict[str, object] = {
                "candidate": True,
                "condition": condition,
                "current_validation_re_evaluated": False,
                "held_out_test_used": False,
                "independent_evaluation_gold_used": False,
                "lexicon_used_at_runtime": False,
                "paper_replication_training": False,
                "root_inventory_unchanged_from_source_adjudicated_v2": True,
                "runtime_boundary_guarantee_scope": "none",
                "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
                "selection_performed": False,
                "surface_specific_runtime_guarantees": [],
                "surface_specific_training_overrides": [],
                "crossing_penalty": CROSSING_PENALTY,
                "dropout_rate": dropout_rate,
                "dropout_seed": SEED,
                "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
                "not_asgari_et_al_2025_algorithm": True,
                "not_literal_bpe_dropout_or_unigram_sampling": True,
            }
            output = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
            rebuild = ARTIFACTS_DIR / condition / "determinism-rebuild" / f"vocab-{target}"
            first_manifest = export_tokenizer_artifact(
                first[target],
                output,
                artifact_type="kapampangan_morphbpe",
                metadata=metadata,
                tokenizer_card=_tokenizer_card(condition, target, dropout_rate),
            )
            second_manifest = export_tokenizer_artifact(
                second[target],
                rebuild,
                artifact_type="kapampangan_morphbpe",
                metadata=metadata,
                tokenizer_card=_tokenizer_card(condition, target, dropout_rate),
            )
            if first_manifest != second_manifest:
                raise AssertionError(f"{condition} target {target} manifest differs on rebuild")
            if _directory_hashes(output) != _directory_hashes(rebuild):
                raise AssertionError(f"{condition} target {target} files differ on rebuild")
            validate_artifact_files(output)
            condition_manifests[str(target)] = first_manifest
        manifests[condition] = condition_manifests

    after = _snapshot_other_artifacts()
    if before != after:
        raise AssertionError("stochastic MorphBPE training changed an existing v4 artifact")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "conditions": [_condition_name(rate) for rate in DROPOUT_RATES],
        "crossing_penalty": CROSSING_PENALTY,
        "dropout_rates": list(DROPOUT_RATES),
        "seed": SEED,
        "target_vocabulary_sizes": list(TARGETS),
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "not_asgari_et_al_2025_algorithm": True,
        "surface_specific_runtime_guarantees": [],
        "surface_specific_training_overrides": [],
        "family_reports": family_reports,
        "artifact_manifests": manifests,
        "deterministic_in_memory_rebuilds": True,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(TRAINING_REPORT_PATH, report)
    return report


def validate() -> dict[str, Any]:
    boundary_rows = v4run._load_jsonl(v4run.RESEGMENTATION_AUDIT_PATH)
    morphology_rows = v4run._load_jsonl(v4run.MORPHOLOGY_INDEX_PATH)

    targets: dict[str, object] = {}
    for target in TARGETS:
        conditions: dict[str, object] = {}
        for dropout_rate in DROPOUT_RATES:
            condition = _condition_name(dropout_rate)
            artifact = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
            validate_artifact_files(artifact)
            tokenizer = load_runtime_tokenizer(artifact)
            conditions[condition] = v4run._condition_metrics(
                tokenizer, artifact, boundary_rows, morphology_rows
            )
        targets[str(target)] = conditions

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "conditions": [_condition_name(rate) for rate in DROPOUT_RATES],
        "independent_evaluation_gold": False,
        "gold_source": (
            "this experiment's own rule-derived resegmentation audit / morphology "
            "index (silver, not independent gold) -- identical gold source already "
            "used for plain_bpe/penalty_* in reports/runtime-evaluation.json"
        ),
        "selection_performed": False,
        "targets": targets,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(RUNTIME_REPORT_PATH, report)
    return report


def main() -> int:
    training_report = train()
    runtime_report = validate()
    print(f"Wrote {TRAINING_REPORT_PATH}")
    print(f"Wrote {RUNTIME_REPORT_PATH}")
    print(f"training report fingerprint: {training_report['report_fingerprint']}")
    print(f"runtime report fingerprint: {runtime_report['report_fingerprint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
