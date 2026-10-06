"""Train the paper-aligned, hard-constrained MorphBPE condition for v4.

This is the *literal* MorphBPE training constraint from Asgari et al. (2025)
as this repository operationalizes it everywhere else
(`experiments/source_adjudicated_v2`'s `morphbpe` family, `source_adjudicated_v1`,
`vocab_ablation_v1`): ordinary greedy BPE merge learning, with the single
rule that a merge is never applied across a protected morpheme boundary.
Unlike the weighted `penalty-*` grid (a thesis *extension* that also demotes
a pair's global rank by its total boundary-crossing frequency), the
hard constraint here is purely local: a pair straddling a boundary in one
word can still be learned wholesale from its unprotected occurrences
elsewhere. No penalty, no dropout, no scoring change of any kind.

Why v4 lacked this until now: the 2026-08-21 v4 rebuild replaced the earlier
unweighted `morphbpe` family with the `plain` + `penalty-1/2/4/8` weighted
grid (see `AGENT_CONTEXT.md`). Phase 5's NLLB integration is committed to the
paper-aligned condition specifically (2026-08-25 user decision), so v4 needs
its own hard-constrained family trained on v4's full expanded-morphology
resegmented stream -- the most linguistically complete boundary set in the
repo -- combined with the unmodified paper algorithm.

Isolated and additive, exactly like `train_stochastic_morphbpe.py` /
`train_unigram_ablation.py`:
  - trains `ConstrainedBPETrainer` on `runs/prepared/training-stream.jsonl`
    (v4's morphology-boundary stream) at 6,080 / 8,192 / 16,384;
  - writes only a new `artifacts/morphbpe/` family plus two new reports;
  - asserts every pre-existing v4 artifact family and every repo-wide
    preserved artifact is byte-unchanged (before/after directory hashing);
  - verifies determinism via two independent in-memory builds and a
    separate on-disk determinism-rebuild directory.

Standard runtime is ordinary, lexicon-free, deterministic greedy BPE --
identical in kind to every other condition here
(`lexicon_used_at_runtime: false`). The silver boundary-F1 / MCF1 numbers
this script's `validate()` writes are the same training-corpus diagnostic
the other families report; the genuine held-out selection lives in
`experiments/tokenizer_selection_v1/` (Phase 3).
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
from kapampangan_morphbpe.bpe import ConstrainedBPETrainer  # noqa: E402
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json  # noqa: E402

TARGETS = (6080, 8192, 16384)
CONDITION = "morphbpe"

ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
TRAINING_REPORT_PATH = REPORTS_DIR / "constrained-morphbpe-training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "constrained-morphbpe-runtime-evaluation.json"

# Every other v4 artifact family that must stay byte-unchanged by this script.
OTHER_V4_ARTIFACT_DIRS = {
    "plain": ARTIFACTS_DIR / "plain",
    "penalty-1": ARTIFACTS_DIR / "penalty-1",
    "penalty-2": ARTIFACTS_DIR / "penalty-2",
    "penalty-4": ARTIFACTS_DIR / "penalty-4",
    "penalty-8": ARTIFACTS_DIR / "penalty-8",
    "stochastic-p4-d0.1": ARTIFACTS_DIR / "stochastic-p4-d0.1",
    "stochastic-p4-d0.2": ARTIFACTS_DIR / "stochastic-p4-d0.2",
    "unigram-ablation": ARTIFACTS_DIR / "unigram-ablation",
}


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


def _tokenizer_card(target: int) -> str:
    return f"""# Expanded morphology v4 tokenizer ({CONDITION}; {target:,})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

Paper-aligned hard-constrained MorphBPE (Asgari et al., 2025, as
operationalized throughout this repository). Ordinary greedy BPE merge
learning over v4's expanded-morphology resegmented training stream
(`runs/prepared/training-stream.jsonl`; see `EVIDENCE.md` for the affix /
circumfix / suffix / reduplication rules that produced its protected
boundaries), with exactly one constraint: a merge is never applied across a
protected morpheme boundary. No penalty, no dropout, no scoring change --
this is the literal paper constraint, not the weighted `penalty-*` thesis
extension. A boundary-crossing pair can still be learned from its
unprotected occurrences elsewhere in the corpus. Standard runtime is
ordinary, deterministic, lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data by
this script (see `experiments/tokenizer_selection_v1/`).
"""


def train() -> dict[str, Any]:
    before_preserved = v4run._snapshot_preserved()
    before_other = _snapshot_other_artifacts()
    prepared_manifest = v4run._verified_prepared_inputs()
    morph = load_prepared_stream(v4run.STREAM_PATH)

    first, first_report = ConstrainedBPETrainer(morph).train(list(TARGETS))
    second, second_report = ConstrainedBPETrainer(morph).train(list(TARGETS))
    if first_report != second_report:
        raise AssertionError("constrained morphbpe training report differs on rebuild")
    if first_report.get("trained_targets") != list(TARGETS):
        raise AssertionError("constrained morphbpe failed to reach every target")
    if first_report.get("protected_boundary_merge_violations") != 0:
        raise AssertionError("constrained morphbpe crossed a training boundary")
    for target in TARGETS:
        if first[target].to_dict() != second[target].to_dict():
            raise AssertionError(f"constrained morphbpe target {target} in-memory rebuild differs")

    manifests: dict[str, object] = {}
    for target in TARGETS:
        metadata: dict[str, object] = {
            "candidate": True,
            "condition": CONDITION,
            "current_validation_re_evaluated": False,
            "held_out_test_used": False,
            "independent_evaluation_gold_used": False,
            "lexicon_used_at_runtime": False,
            "paper_replication_training": True,
            "paper_aligned_hard_constrained": True,
            "merge_constraint": "no_merge_across_protected_boundary",
            "weighted_penalty_used": False,
            "stochastic_dropout_used": False,
            "root_inventory_unchanged_from_source_adjudicated_v2": True,
            "runtime_boundary_guarantee_scope": "none",
            "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
            "selection_performed": False,
            "surface_specific_runtime_guarantees": [],
            "surface_specific_training_overrides": [],
        }
        output = ARTIFACTS_DIR / CONDITION / "candidates" / f"vocab-{target}"
        rebuild = ARTIFACTS_DIR / CONDITION / "determinism-rebuild" / f"vocab-{target}"
        first_manifest = export_tokenizer_artifact(
            first[target],
            output,
            artifact_type="kapampangan_morphbpe",
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target),
        )
        second_manifest = export_tokenizer_artifact(
            second[target],
            rebuild,
            artifact_type="kapampangan_morphbpe",
            metadata=metadata,
            tokenizer_card=_tokenizer_card(target),
        )
        if first_manifest != second_manifest:
            raise AssertionError(f"{CONDITION} target {target} manifest differs on rebuild")
        if _directory_hashes(output) != _directory_hashes(rebuild):
            raise AssertionError(f"{CONDITION} target {target} files differ on rebuild")
        validate_artifact_files(output)
        manifests[str(target)] = first_manifest

    if _snapshot_other_artifacts() != before_other:
        raise AssertionError("constrained morphbpe training changed an existing v4 artifact")
    if v4run._snapshot_preserved() != before_preserved:
        raise AssertionError("constrained morphbpe training changed a repo-preserved artifact")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": CONDITION,
        "algorithm": "paper_aligned_hard_constrained_morphbpe",
        "merge_constraint": "no_merge_across_protected_boundary",
        "weighted_penalty_used": False,
        "stochastic_dropout_used": False,
        "target_vocabulary_sizes": list(TARGETS),
        "training_stream": v4run.STREAM_PATH.name,
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "surface_specific_runtime_guarantees": [],
        "surface_specific_training_overrides": [],
        "family_report": first_report,
        "artifact_manifests": manifests,
        "deterministic_in_memory_rebuilds": True,
        "existing_artifacts_unchanged": True,
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
        artifact = ARTIFACTS_DIR / CONDITION / "candidates" / f"vocab-{target}"
        validate_artifact_files(artifact)
        tokenizer = load_runtime_tokenizer(artifact)
        targets[str(target)] = v4run._condition_metrics(
            tokenizer, artifact, boundary_rows, morphology_rows
        )

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": CONDITION,
        "independent_evaluation_gold": False,
        "gold_source": (
            "this experiment's own rule-derived resegmentation audit / morphology "
            "index (silver, not independent gold) -- identical gold source already "
            "used for plain_bpe/penalty_* in reports/runtime-evaluation.json; the "
            "genuine held-out selection is experiments/tokenizer_selection_v1/"
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
    for target in TARGETS:
        metrics = runtime_report["targets"][str(target)]
        print(
            f"  vocab {target}: boundary_f1={metrics['boundary_f1']:.4f} "
            f"mcf1={metrics['morphological_consistency_f1']:.4f} "
            f"fertility={metrics['fertility']:.4f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
