from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "runtime"))
sys.path.insert(0, str(EXPERIMENT_ROOT))

import expanded_morphology as em  # noqa: E402

from kapampangan_morphbpe.artifact import (  # noqa: E402
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.bpe import ConstrainedBPETrainer  # noqa: E402
from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.lexicon import load_lexicon  # noqa: E402
from kapampangan_morphbpe.models import PreparedSequence  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import (  # noqa: E402
    RuntimeTokenizer,
    load_runtime_tokenizer,
)
from kapampangan_morphbpe.serialization import (  # noqa: E402
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)
from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer  # noqa: E402

V2_ROOT = REPOSITORY_ROOT / "experiments/source_adjudicated_v2"
V2_LEXICON_PATH = V2_ROOT / "resources/training-lexicon.json"
V2_LEXICON_MANIFEST_PATH = V2_ROOT / "resources/training-lexicon-manifest.json"
V2_STREAM_PATH = V2_ROOT / "runs/prepared/training-stream.jsonl"
V2_PREPARED_MANIFEST_PATH = V2_ROOT / "runs/prepared/training-stream-manifest.json"

REPORTS_DIR = EXPERIMENT_ROOT / "reports"
RUNS_DIR = EXPERIMENT_ROOT / "runs"
PREPARED_DIR = RUNS_DIR / "prepared"
STREAM_PATH = PREPARED_DIR / "training-stream.jsonl"
PLAIN_STREAM_PATH = PREPARED_DIR / "plain-training-stream.jsonl"
PREPARED_MANIFEST_PATH = PREPARED_DIR / "training-stream-manifest.json"
SEGMENTATION_DIR = RUNS_DIR / "segmentations"
RESEGMENTATION_AUDIT_PATH = SEGMENTATION_DIR / "resegmentation-audit.jsonl"
SEGMENTATION_MANIFEST_PATH = SEGMENTATION_DIR / "segmentation-manifest.json"
MORPHOLOGY_INDEX_PATH = SEGMENTATION_DIR / "morphology-index.jsonl"

ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
TRAINING_REPORT_PATH = REPORTS_DIR / "training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "runtime-evaluation.json"
AUDIT_JSON_PATH = REPORTS_DIR / "audit.json"
AUDIT_MARKDOWN_PATH = REPORTS_DIR / "audit.md"
EXPERIMENT_REPORT_PATH = REPORTS_DIR / "experiment-report.json"

TARGETS = (6080, 8192, 16384)
PENALTIES = (1, 2, 4, 8)
ACCEPTED_STATUSES = {"accepted", "protected_root", "protected_compound"}

PRESERVED_ARTIFACTS = {
    "canonical": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "source-v1": REPOSITORY_ROOT / "experiments/source_adjudicated_v1/artifacts",
    "source-v2": V2_ROOT / "artifacts",
    "weighted-v3": REPOSITORY_ROOT / "experiments/weighted_morphbpe_v3/artifacts",
    "boundary-safe-v1": REPOSITORY_ROOT / "experiments/boundary_safe_v1/artifacts",
    "vocab-ablation-v1": REPOSITORY_ROOT / "experiments/vocab_ablation_v1/artifacts",
}

# Rejected/deferred items from EVIDENCE.md, recorded here so the audit report
# can cite them without re-deriving the reasoning at report time.
REJECTED_ITEMS = (
    {
        "item": "paki-...-an circumfix",
        "disposition": "rejected",
        "reason": (
            "The only -an-suffixed forms near paki- resolve to something else: "
            "pakitanan is pa- + kit(a) + -anan (Mirikitani p.635), and pakidinan "
            "is paki- + the irregular suppletive stem dinan ('give to', Mirikitani "
            "p.570 item 5). Neither is a productive paki-...-an pattern."
        ),
    },
    {
        "item": "-in suffix",
        "disposition": "rejected",
        "reason": "Not found in any reviewed Kapampangan source.",
    },
    {
        "item": "-ng linker",
        "disposition": "rejected (out of scope for v4)",
        "reason": (
            "User instruction: model only as a linker with exact-host/context "
            "safeguards, not as an ordinary derivational suffix; left for a "
            "separately scoped experiment."
        ),
    },
    {
        "item": "Tagalog pinaka-",
        "disposition": "rejected",
        "reason": "Not Kapampangan. Kapampangan's own superlative peka- is operationalized.",
    },
    {
        "item": "'mi' in misamban treated as an infix",
        "disposition": "rejected",
        "reason": (
            "misamban is analyzed through the mi-...-an circumfix applied to the "
            "attested root samba, not through any infix rule."
        ),
    },
    {
        "item": "mekipag- (aspect pair of makipag-)",
        "disposition": "deferred",
        "reason": (
            "meki- and makipag- are each directly attested but no source shows "
            "mekipag- itself; adding it would be paradigm analogy, not attestation."
        ),
    },
    {
        "item": "peN-/piN- as aspect-marked paN- allomorphs",
        "disposition": "deferred",
        "reason": (
            "Mirikitani pp.744, 795, 945 glossary entries are internally inconsistent "
            "about whether they mark aspect on pag- or on paN-."
        ),
    },
    {
        "item": "Tense-conditioned root vowel alternation (a<->e, u<->i)",
        "disposition": "documented, not operationalized",
        "reason": "Forman: lexically conditioned per root, not a general phonological rule.",
    },
    {
        "item": "min- unfolded-tense variant of maN- (vs. operationalized men-)",
        "disposition": "documented, not operationalized",
        "reason": "Same lexical-conditioning problem; no reliable surface trigger.",
    },
    {
        "item": "Vowel lengthening for continuing/progressive tense",
        "disposition": "documented, not operationalized",
        "reason": (
            "Not consistently marked in the plain-text training corpus and does not "
            "correspond to a segment boundary."
        ),
    },
    {
        "item": "Medial d->r alternation as a general standalone rule",
        "disposition": "partially operationalized",
        "reason": "Only accepted as a reduplication hypothesis, exactly where documented.",
    },
)


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_preserved() -> dict[str, dict[str, str]]:
    return {name: _directory_hashes(path) for name, path in PRESERVED_ARTIFACTS.items()}


def _verified_v2_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    lexicon_manifest = _object(read_json(V2_LEXICON_MANIFEST_PATH), "v2 lexicon manifest")
    prepared_manifest = _object(read_json(V2_PREPARED_MANIFEST_PATH), "v2 prepared manifest")
    if lexicon_manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("v2 lexicon dataset fingerprint mismatch")
    if sha256_file(V2_LEXICON_PATH) != lexicon_manifest.get("lexicon_file_sha256"):
        raise ValueError("v2 lexicon file hash mismatch")
    if prepared_manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("v2 prepared stream dataset fingerprint mismatch")
    if sha256_file(V2_STREAM_PATH) != prepared_manifest.get("stream_sha256"):
        raise ValueError("v2 prepared stream hash mismatch")
    return lexicon_manifest, prepared_manifest


def _write_stream(path: Path, sequences: list[PreparedSequence]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for sequence in sequences:
            stream.write(
                stable_compact_json(
                    {
                        "surface": sequence.surface,
                        "protected_boundaries": list(sequence.protected_boundaries),
                        "kind": sequence.kind,
                        "frequency": sequence.frequency,
                    }
                )
                + "\n"
            )


def prepare() -> dict[str, Any]:
    before = _snapshot_preserved()
    lexicon_manifest, prepared_manifest = _verified_v2_inputs()
    lexicon = load_lexicon(V2_LEXICON_PATH)
    segmenter = em.ExpandedMorphologicalSegmenter(lexicon)
    v2_sequences = load_prepared_stream(V2_STREAM_PATH)

    word_surfaces = sorted(
        {sequence.surface for sequence in v2_sequences if sequence.kind == "word"}
    )
    analyses = {surface: segmenter.segment(surface) for surface in word_surfaces}

    new_sequences: list[PreparedSequence] = []
    plain_sequences: list[PreparedSequence] = []
    status_occurrences: Counter[str] = Counter()
    status_types: Counter[str] = Counter()
    rule_occurrences: Counter[str] = Counter()
    rule_types: Counter[str] = Counter()
    changed_rows: list[dict[str, Any]] = []
    ambiguous_types: list[dict[str, Any]] = []
    word_occurrences = 0

    for sequence in v2_sequences:
        if sequence.kind != "word":
            new_sequences.append(sequence)
            plain_sequences.append(
                PreparedSequence(sequence.surface, (), sequence.kind, sequence.frequency)
            )
            continue
        analysis = analyses[sequence.surface]
        boundaries = analysis.protected_boundaries if analysis.status in ACCEPTED_STATUSES else ()
        new_sequences.append(
            PreparedSequence(sequence.surface, boundaries, sequence.kind, sequence.frequency)
        )
        plain_sequences.append(
            PreparedSequence(sequence.surface, (), sequence.kind, sequence.frequency)
        )

        status_occurrences[analysis.status] += sequence.frequency
        status_types[analysis.status] += 1
        word_occurrences += sequence.frequency
        if analysis.rule_id is not None:
            rule_occurrences[analysis.rule_id] += sequence.frequency
            rule_types[analysis.rule_id] += 1
        if analysis.status == "ambiguous":
            ambiguous_types.append(
                {
                    "surface": sequence.surface,
                    "frequency": sequence.frequency,
                    "trace": list(analysis.trace),
                }
            )
        if boundaries != sequence.protected_boundaries:
            changed_rows.append(
                {
                    "surface": sequence.surface,
                    "frequency": sequence.frequency,
                    "v2_protected_boundaries": list(sequence.protected_boundaries),
                    "v4_protected_boundaries": list(boundaries),
                    "v4_segments": list(analysis.segments),
                    "v4_underlying_display": analysis.underlying_display,
                    "v4_rule_id": analysis.rule_id,
                    "v4_status": analysis.status,
                }
            )

    # Exact surface/kind/frequency parity gate: v4 must only change boundaries.
    v2_identity = sorted(
        (sequence.surface, sequence.kind, sequence.frequency) for sequence in v2_sequences
    )
    v4_identity = sorted(
        (sequence.surface, sequence.kind, sequence.frequency) for sequence in new_sequences
    )
    if v2_identity != v4_identity:
        raise AssertionError("v4 resegmentation changed a surface, kind, or frequency")
    plain_identity = sorted(
        (sequence.surface, sequence.kind, sequence.frequency) for sequence in plain_sequences
    )
    if v2_identity != plain_identity:
        raise AssertionError("v4 plain stream changed a surface, kind, or frequency")

    _write_stream(STREAM_PATH, new_sequences)
    _write_stream(PLAIN_STREAM_PATH, plain_sequences)

    changed_rows.sort(key=lambda row: cast(str, row["surface"]))
    ambiguous_types.sort(key=lambda row: cast(str, row["surface"]))
    SEGMENTATION_DIR.mkdir(parents=True, exist_ok=True)
    with RESEGMENTATION_AUDIT_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        for row in changed_rows:
            handle.write(stable_compact_json(row) + "\n")

    # Structured per-word morpheme inventory for every analyzed word type,
    # independent of whether its boundaries changed from v2. This is the input
    # to Morphological Consistency F1 (MCF1): grouping words by shared
    # (kind, underlying-label) morpheme lets validate() check whether the
    # trained tokenizer represents that morpheme with the same token(s)
    # everywhere it occurs. Protected roots/compounds are recorded as their
    # own single morpheme so they can match the same root/compound appearing
    # inside a decomposed word elsewhere (e.g. root "samba" standalone vs. the
    # "samba" morpheme inside "misamban").
    morphology_index_rows: list[dict[str, Any]] = []
    for surface in word_surfaces:
        analysis = analyses[surface]
        if analysis.status not in ACCEPTED_STATUSES:
            continue
        if analysis.underlying_units:
            morphemes = [
                {"kind": unit.kind, "underlying": unit.underlying}
                for unit in analysis.underlying_units
            ]
        else:
            morphemes = [{"kind": analysis.status, "underlying": comparison_key(surface)}]
        morphology_index_rows.append({"surface": surface, "morphemes": morphemes})
    morphology_index_rows.sort(key=lambda row: cast(str, row["surface"]))
    with MORPHOLOGY_INDEX_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        for row in morphology_index_rows:
            handle.write(stable_compact_json(row) + "\n")

    characters = sorted(
        {character for sequence in new_sequences for character in sequence.surface},
        key=lambda value: value.encode("utf-8"),
    )
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "v2_lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "v2_prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "root_inventory_unchanged": True,
        "word_types": len(word_surfaces),
        "word_occurrences": word_occurrences,
        "character_inventory_size": len(characters),
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "status_types": dict(sorted(status_types.items())),
        "rule_occurrences": dict(sorted(rule_occurrences.items())),
        "rule_types": dict(sorted(rule_types.items())),
        "changed_from_v2_types": len(changed_rows),
        "changed_from_v2_occurrences": sum(cast(int, row["frequency"]) for row in changed_rows),
        "ambiguous_types": len(ambiguous_types),
        "stream_file": STREAM_PATH.name,
        "stream_sha256": sha256_file(STREAM_PATH),
        "plain_stream_file": PLAIN_STREAM_PATH.name,
        "plain_stream_sha256": sha256_file(PLAIN_STREAM_PATH),
    }
    manifest_document = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    PREPARED_DIR.mkdir(parents=True, exist_ok=True)
    write_json(PREPARED_MANIFEST_PATH, manifest_document)

    segmentation_manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "changed_rows": len(changed_rows),
        "ambiguous_rows": len(ambiguous_types),
        "audit_file": RESEGMENTATION_AUDIT_PATH.name,
        "audit_sha256": sha256_file(RESEGMENTATION_AUDIT_PATH),
        "morphology_index_rows": len(morphology_index_rows),
        "morphology_index_file": MORPHOLOGY_INDEX_PATH.name,
        "morphology_index_sha256": sha256_file(MORPHOLOGY_INDEX_PATH),
    }
    segmentation_manifest = {
        **segmentation_manifest_body,
        "manifest_fingerprint": fingerprint(segmentation_manifest_body),
    }
    write_json(SEGMENTATION_MANIFEST_PATH, segmentation_manifest)

    audit_document: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "root_inventory_unchanged": True,
        "reused_v2_lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "word_types_resegmented": len(word_surfaces),
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "status_types": dict(sorted(status_types.items())),
        "rule_occurrences": dict(sorted(rule_occurrences.items())),
        "rule_types": dict(sorted(rule_types.items())),
        "newly_analyzed_types_vs_v2": len(changed_rows),
        "newly_analyzed_occurrences_vs_v2": sum(
            cast(int, row["frequency"]) for row in changed_rows
        ),
        "ambiguous_types": len(ambiguous_types),
        "ambiguous_examples": ambiguous_types[:25],
        "newly_analyzed_examples": changed_rows[:40],
        "rejected_and_deferred_items": list(REJECTED_ITEMS),
    }
    write_json(AUDIT_JSON_PATH, audit_document)
    _write_audit_markdown(audit_document)

    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("v4 prepare stage changed an existing artifact")
    return manifest_document


def _write_audit_markdown(audit: dict[str, Any]) -> None:
    lines = [
        "# Expanded morphology v4 - resegmentation audit",
        "",
        "Status: local-test, source-supported, provisional. Not independent gold.",
        "Root inventory reused byte-for-byte from `source_adjudicated_v2`; only new",
        "affix/morphophonology rules were added. See `EVIDENCE.md` for full citations.",
        "",
        f"- Word types resegmented: **{audit['word_types_resegmented']:,}**",
        f"- Types newly analyzed vs. v2 (boundaries changed): "
        f"**{audit['newly_analyzed_types_vs_v2']:,}** "
        f"({audit['newly_analyzed_occurrences_vs_v2']:,} occurrences)",
        f"- Ambiguous types (preserved, not resolved): **{audit['ambiguous_types']:,}**",
        "",
        "## Rule counts (occurrences)",
        "",
        "| Rule ID | Occurrences | Types |",
        "|---|---:|---:|",
    ]
    rule_occurrences = cast(dict[str, int], audit["rule_occurrences"])
    rule_types = cast(dict[str, int], audit["rule_types"])
    for rule_id in sorted(rule_occurrences, key=lambda key: (-rule_occurrences[key], key)):
        lines.append(
            f"| `{rule_id}` | {rule_occurrences[rule_id]:,} | {rule_types.get(rule_id, 0):,} |"
        )
    lines.extend(
        [
            "",
            "## Newly analyzed examples (first 40, alphabetical)",
            "",
            "| Surface | v4 segments | Underlying | Rule | Frequency |",
            "|---|---|---|---|---:|",
        ]
    )
    for row in cast(list[dict[str, Any]], audit["newly_analyzed_examples"]):
        segments = " || ".join(cast(list[str], row["v4_segments"]))
        lines.append(
            f"| `{row['surface']}` | `{segments}` | {row['v4_underlying_display']} | "
            f"`{row['v4_rule_id']}` | {row['frequency']:,} |"
        )
    lines.extend(
        [
            "",
            "## Ambiguous forms (first 25, alphabetical)",
            "",
            "| Surface | Frequency |",
            "|---|---:|",
        ]
    )
    for row in cast(list[dict[str, Any]], audit["ambiguous_examples"]):
        lines.append(f"| `{row['surface']}` | {row['frequency']:,} |")
    lines.extend(
        ["", "## Rejected / deferred items", "", "| Item | Disposition | Reason |", "|---|---|---|"]
    )
    for row in cast(list[dict[str, Any]], audit["rejected_and_deferred_items"]):
        lines.append(f"| {row['item']} | {row['disposition']} | {row['reason']} |")
    lines.append("")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def _verified_prepared_inputs() -> dict[str, Any]:
    manifest = _object(read_json(PREPARED_MANIFEST_PATH), "v4 prepared manifest")
    if sha256_file(STREAM_PATH) != manifest.get("stream_sha256"):
        raise ValueError("v4 morphbpe stream hash mismatch")
    if sha256_file(PLAIN_STREAM_PATH) != manifest.get("plain_stream_sha256"):
        raise ValueError("v4 plain stream hash mismatch")
    return manifest


def _tokenizer_card(condition: str, target: int, penalty: int | None = None) -> str:
    if penalty is None:
        body = "Ordinary Plain-BPE control: no morphology boundaries of any kind."
    else:
        body = f"""Weighted MorphBPE thesis extension (not the unmodified MorphBPE paper
algorithm). Each candidate merge pair p is ranked by

`allowed_frequency(p) - {penalty} * crossing_frequency(p)`

where both quantities are summed globally across the v4-resegmented training
corpus (see EVIDENCE.md for the new affix/circumfix/suffix/reduplication rules
that produced its protected boundaries), not only within one word. A merge is
still never applied across a protected boundary during training; the penalty
only demotes a pair's global rank when it frequently conflicts with a
boundary elsewhere in the corpus."""
    return f"""# Expanded morphology v4 tokenizer ({condition}; {target:,})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

This is an isolated, source-enriched extension of the Table 1 baseline. It adds
new linguistically evidenced affixes/morphophonological processes (see
`EVIDENCE.md`) on top of the unmodified `source_adjudicated_v2` root inventory.
{body}
Standard runtime is ordinary lexicon-free BPE; morphology only constrains merge
learning during training. Not independently evaluated on held-out data.
"""


def _export_family(
    condition: str,
    first: dict[int, Any],
    second: dict[int, Any],
    family_fingerprint: str,
    prepared_manifest_fingerprint: object,
    *,
    penalty: int | None = None,
) -> dict[str, object]:
    manifests: dict[str, object] = {}
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
            "prepared_manifest_fingerprint": prepared_manifest_fingerprint,
            "selection_performed": False,
            "surface_specific_runtime_guarantees": [],
            "surface_specific_training_overrides": [],
            "training_family_fingerprint": family_fingerprint,
        }
        if penalty is not None:
            metadata["crossing_penalty"] = penalty
            metadata["merge_score"] = "allowed_frequency-crossing_penalty*crossing_frequency"
        output = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
        rebuild = ARTIFACTS_DIR / condition / "determinism-rebuild" / f"vocab-{target}"
        artifact_type = "kapampangan_plain_bpe" if condition == "plain" else "kapampangan_morphbpe"
        first_manifest = export_tokenizer_artifact(
            first[target],
            output,
            artifact_type=artifact_type,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(condition, target, penalty),
        )
        second_manifest = export_tokenizer_artifact(
            second[target],
            rebuild,
            artifact_type=artifact_type,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(condition, target, penalty),
        )
        if first_manifest != second_manifest:
            raise AssertionError(f"{condition} target {target} manifest differs on rebuild")
        if _directory_hashes(output) != _directory_hashes(rebuild):
            raise AssertionError(f"{condition} target {target} files differ on rebuild")
        validate_artifact_files(output)
        manifests[str(target)] = first_manifest
    return manifests


def _train_condition(
    condition: str, first_report: dict[str, object], second_report: dict[str, object]
) -> None:
    if first_report != second_report:
        raise AssertionError(f"{condition} training report differs on rebuild")
    if first_report.get("trained_targets") != list(TARGETS):
        raise AssertionError(f"{condition} failed to reach every target")
    if first_report.get("protected_boundary_merge_violations") != 0:
        raise AssertionError(f"{condition} crossed a training boundary")


def train() -> dict[str, Any]:
    before = _snapshot_preserved()
    prepared_manifest = _verified_prepared_inputs()
    plain = load_prepared_stream(PLAIN_STREAM_PATH)
    morph = load_prepared_stream(STREAM_PATH)

    family_reports: dict[str, object] = {}
    first_models: dict[str, dict[int, Any]] = {}
    second_models: dict[str, dict[int, Any]] = {}

    first_plain, plain_report = ConstrainedBPETrainer(plain).train(list(TARGETS))
    second_plain, second_plain_report = ConstrainedBPETrainer(plain).train(list(TARGETS))
    _train_condition("plain", plain_report, second_plain_report)
    for target in TARGETS:
        if first_plain[target].to_dict() != second_plain[target].to_dict():
            raise AssertionError(f"plain target {target} in-memory rebuild differs")
    first_models["plain"] = first_plain
    second_models["plain"] = second_plain
    family_reports["plain"] = plain_report

    # Weighted MorphBPE penalty grid, reusing WeightedMorphBPETrainer unmodified
    # (same algorithm weighted_morphbpe_v3 validated) against v4's own expanded
    # boundary set instead of v2's. Replaces the earlier unweighted "morphbpe"
    # condition: the plain ConstrainedBPETrainer used here only rejects a
    # crossing merge for the one occurrence where it crosses, so a pair like
    # ("i","s") straddling the "mi-" boundary in "misamban" could still be
    # learned wholesale from every OTHER unprotected occurrence and then
    # reapplied to "misamban" at standard runtime. Weighted training demotes
    # that pair's global rank by its total crossing frequency across the whole
    # corpus, which can let boundary-respecting merges win the race instead.
    for penalty in PENALTIES:
        condition = f"penalty-{penalty}"
        first, first_report = WeightedMorphBPETrainer(morph, penalty).train(list(TARGETS))
        second, second_report = WeightedMorphBPETrainer(morph, penalty).train(list(TARGETS))
        _train_condition(condition, first_report, second_report)
        for target in TARGETS:
            if first[target].to_dict() != second[target].to_dict():
                raise AssertionError(f"{condition} target {target} in-memory rebuild differs")
        first_models[condition] = first
        second_models[condition] = second
        family_reports[condition] = first_report

    conditions = ["plain", *[f"penalty-{penalty}" for penalty in PENALTIES]]
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "conditions": conditions,
        "crossing_penalties": list(PENALTIES),
        "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
        "target_vocabulary_sizes": list(TARGETS),
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "surface_specific_runtime_guarantees": [],
        "surface_specific_training_overrides": [],
        "family_reports": family_reports,
        "deterministic_in_memory_rebuilds": True,
    }
    family_fingerprint = fingerprint(body)
    manifests: dict[str, object] = {
        "plain": _export_family(
            "plain",
            first_models["plain"],
            second_models["plain"],
            family_fingerprint,
            prepared_manifest.get("manifest_fingerprint"),
        )
    }
    for penalty in PENALTIES:
        condition = f"penalty-{penalty}"
        manifests[condition] = _export_family(
            condition,
            first_models[condition],
            second_models[condition],
            family_fingerprint,
            prepared_manifest.get("manifest_fingerprint"),
            penalty=penalty,
        )
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("v4 training changed an existing artifact")

    final_body: dict[str, object] = {
        **body,
        "artifact_manifests": manifests,
        "existing_artifacts_unchanged": True,
        "training_family_fingerprint": family_fingerprint,
    }
    report = {**final_body, "report_fingerprint": fingerprint(final_body)}
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(TRAINING_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0.0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value: Any = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} must contain a JSON object")
            rows.append(cast(dict[str, Any], value))
    return rows


def _runtime_metrics(artifact: Path, rows: list[dict[str, Any]]) -> dict[str, object]:
    tokenizer = load_runtime_tokenizer(artifact)
    true_positive = false_positive = false_negative = 0
    missed_types = extra_types = exact_types = 0
    exact_occurrences = produced_tokens = total_occurrences = 0
    for row in rows:
        surface = str(row["surface"])
        segments = tuple(cast(list[str], row["v4_segments"]))
        gold = set(cast(list[int], row["v4_protected_boundaries"]))
        frequency = int(row["frequency"])
        encoding = tokenizer.encode(surface)
        if tokenizer.decode(encoding.ids) != surface:
            raise AssertionError(f"runtime failed to round-trip {surface!r}")
        pieces = tuple(token.token for token in encoding.tokens)
        predicted = {token.end for token in encoding.tokens[:-1]}
        missed = gold - predicted
        extra = predicted - gold
        true_positive += len(gold & predicted) * frequency
        false_positive += len(extra) * frequency
        false_negative += len(missed) * frequency
        missed_types += bool(missed)
        extra_types += bool(extra)
        exact_types += pieces == segments
        if pieces == segments:
            exact_occurrences += frequency
        produced_tokens += len(pieces) * frequency
        total_occurrences += frequency

    precision = (
        true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    )
    return {
        "artifact": artifact.relative_to(REPOSITORY_ROOT).as_posix(),
        "vocabulary_size": tokenizer.vocabulary_size,
        "evaluated_types": len(rows),
        "evaluated_occurrences": total_occurrences,
        "exact_segment_types": exact_types,
        "exact_segment_occurrences": exact_occurrences,
        "missed_boundary_types": missed_types,
        "extra_boundary_types": extra_types,
        "boundary_precision": precision,
        "boundary_recall": recall,
        "boundary_f1": _f1(precision, recall),
        "fertility": produced_tokens / total_occurrences if total_occurrences else 0.0,
        "lexicon_used_at_runtime": False,
    }


_MCF1_MIN_MORPHEME_LENGTH = 2
_MCF1_MIN_TOKEN_LENGTH = 2
_MCF1_MAX_GROUP_SIZE = 300


def _capped_pairs(members: list[int], cap: int) -> set[tuple[int, int]]:
    if len(members) > cap:
        # Deterministic prefix, not a random sample: every group is built
        # from a stable, sorted word-index list, so this is reproducible
        # without a seeded RNG.
        members = members[:cap]
    pairs: set[tuple[int, int]] = set()
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            pairs.add((members[i], members[j]))
    return pairs


def _morphological_consistency_f1(
    tokenizer: RuntimeTokenizer, index_rows: list[dict[str, Any]]
) -> dict[str, object]:
    """Approximates the thesis's Morphological Consistency F1-Score (MCF1),
    adapted from the MorphBPE evaluation framework of Asgari et al. (2025):
    "whether words that share morphemes are assigned shared tokens and
    whether shared tokens correspond to shared morphemes." Neither source
    specifies an exact algorithm, so this is one explicit, documented
    operationalization, not a literal reproduction:

    - Two words "share a morpheme" if their accepted v4 analyses contain the
      same (kind, underlying-label) pair (protected roots/compounds count as
      a single morpheme equal to themselves, so a standalone root matches
      the same root appearing inside a decomposed word elsewhere, e.g. root
      "samba" alone vs. the "samba" morpheme inside "misamban").
    - Two words "share a token" if the tokenizer's standard-runtime encodings
      contain at least one identical piece of length >= 2 (single-character
      pieces are excluded as trivially frequent noise, not meaningful
      morphology).
    - TP = word pairs that both share a morpheme and share a token.
      FN = pairs that share a morpheme but no token (the tokenizer failed to
      represent the shared morpheme consistently).
      FP = pairs that share a token but no morpheme (an accidental/spurious
      token-level match with no morphological basis).
    - Groups larger than _MCF1_MAX_GROUP_SIZE are capped to a deterministic
      prefix to keep pairwise enumeration tractable; this under-counts very
      common morphemes/tokens rather than over-counting, so the reported
      score should be read as an estimate, not an exhaustive corpus-wide value.
    """
    surfaces = [cast(str, row["surface"]) for row in index_rows]
    morpheme_sets: list[frozenset[tuple[str, str]]] = []
    token_sets: list[frozenset[str]] = []
    for row, surface in zip(index_rows, surfaces, strict=True):
        morphemes = cast(list[dict[str, str]], row["morphemes"])
        morpheme_sets.append(
            frozenset(
                (unit["kind"], unit["underlying"])
                for unit in morphemes
                if len(unit["underlying"]) >= _MCF1_MIN_MORPHEME_LENGTH
            )
        )
        encoding = tokenizer.encode(surface)
        token_sets.append(
            frozenset(
                token.token
                for token in encoding.tokens
                if len(token.token) >= _MCF1_MIN_TOKEN_LENGTH
            )
        )

    morpheme_groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, morphemes_for_word in enumerate(morpheme_sets):
        for morpheme in morphemes_for_word:
            morpheme_groups[morpheme].append(index)
    token_groups: dict[str, list[int]] = defaultdict(list)
    for index, tokens_for_word in enumerate(token_sets):
        for token in tokens_for_word:
            token_groups[token].append(index)

    morpheme_pairs: set[tuple[int, int]] = set()
    capped_morpheme_groups = 0
    active_morpheme_groups = 0
    for members in morpheme_groups.values():
        if len(members) < 2:
            continue
        active_morpheme_groups += 1
        if len(members) > _MCF1_MAX_GROUP_SIZE:
            capped_morpheme_groups += 1
        morpheme_pairs |= _capped_pairs(members, _MCF1_MAX_GROUP_SIZE)

    token_pairs: set[tuple[int, int]] = set()
    capped_token_groups = 0
    active_token_groups = 0
    for members in token_groups.values():
        if len(members) < 2:
            continue
        active_token_groups += 1
        if len(members) > _MCF1_MAX_GROUP_SIZE:
            capped_token_groups += 1
        token_pairs |= _capped_pairs(members, _MCF1_MAX_GROUP_SIZE)

    true_positive = len(morpheme_pairs & token_pairs)
    false_negative = len(morpheme_pairs - token_pairs)
    false_positive = len(token_pairs - morpheme_pairs)
    precision = (
        true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    )
    recall = (
        true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    )
    return {
        "evaluated_words": len(index_rows),
        "morpheme_groups": active_morpheme_groups,
        "token_groups": active_token_groups,
        "capped_morpheme_groups": capped_morpheme_groups,
        "capped_token_groups": capped_token_groups,
        "morpheme_sharing_pairs": len(morpheme_pairs),
        "token_sharing_pairs": len(token_pairs),
        "true_positive_pairs": true_positive,
        "false_positive_pairs": false_positive,
        "false_negative_pairs": false_negative,
        "morphological_consistency_precision": precision,
        "morphological_consistency_recall": recall,
        "morphological_consistency_f1": _f1(precision, recall),
    }


def _condition_metrics(
    tokenizer: RuntimeTokenizer,
    artifact: Path,
    boundary_rows: list[dict[str, Any]],
    morphology_rows: list[dict[str, Any]],
) -> dict[str, object] | None:
    if not boundary_rows and not morphology_rows:
        return None
    metrics: dict[str, object] = {}
    if boundary_rows:
        metrics.update(_runtime_metrics(artifact, boundary_rows))
    if morphology_rows:
        metrics.update(_morphological_consistency_f1(tokenizer, morphology_rows))
    return metrics


def validate() -> dict[str, Any]:
    segmentation_manifest = _object(
        read_json(SEGMENTATION_MANIFEST_PATH), "v4 segmentation manifest"
    )
    if sha256_file(RESEGMENTATION_AUDIT_PATH) != segmentation_manifest.get("audit_sha256"):
        raise ValueError("v4 resegmentation audit hash mismatch")
    if sha256_file(MORPHOLOGY_INDEX_PATH) != segmentation_manifest.get("morphology_index_sha256"):
        raise ValueError("v4 morphology index hash mismatch")
    rows = _load_jsonl(RESEGMENTATION_AUDIT_PATH)
    morphology_rows = _load_jsonl(MORPHOLOGY_INDEX_PATH)

    diagnostic_words = ["misamban", "kabukasan", "sinulat"]
    diagnostics: dict[str, object] = {}
    targets: dict[str, object] = {}
    for target in TARGETS:
        plain = ARTIFACTS_DIR / "plain/candidates" / f"vocab-{target}"
        validate_artifact_files(plain)
        plain_tokenizer = load_runtime_tokenizer(plain)
        conditions: dict[str, object] = {
            "plain_bpe": _condition_metrics(plain_tokenizer, plain, rows, morphology_rows),
        }
        target_diagnostics: dict[str, object] = {}
        for penalty in PENALTIES:
            condition = f"penalty_{penalty}"
            artifact = ARTIFACTS_DIR / f"penalty-{penalty}/candidates" / f"vocab-{target}"
            validate_artifact_files(artifact)
            manifest = _object(read_json(artifact / "tokenizer-manifest.json"), "artifact")
            metadata = _object(manifest.get("metadata", {}), "artifact metadata")
            if metadata.get("surface_specific_runtime_guarantees") != []:
                raise AssertionError(
                    f"v4 {condition} artifact contains a surface-specific guarantee"
                )
            tokenizer = load_runtime_tokenizer(artifact)
            conditions[condition] = _condition_metrics(tokenizer, artifact, rows, morphology_rows)
            word_diagnostics = {}
            for word in diagnostic_words:
                encoding = tokenizer.encode(word)
                if tokenizer.decode(encoding.ids) != word:
                    raise AssertionError(f"runtime failed to round-trip {word!r}")
                word_diagnostics[word] = [token.token for token in encoding.tokens]
            target_diagnostics[condition] = word_diagnostics
        targets[str(target)] = conditions
        diagnostics[str(target)] = target_diagnostics

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": "expanded_morphology_v4_weighted",
        "crossing_penalties": list(PENALTIES),
        "independent_evaluation_gold": False,
        "selection_performed": False,
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "diagnostic_round_trips": diagnostics,
        "targets": targets,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RUNTIME_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def run_all() -> dict[str, Any]:
    before = _snapshot_preserved()
    prepared = prepare()
    training = train()
    runtime = validate()
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("v4 full run changed an existing artifact")
    final: dict[str, object] = {
        "status": "complete",
        "prepared_manifest_fingerprint": prepared["manifest_fingerprint"],
        "training_report_fingerprint": training["report_fingerprint"],
        "runtime_report_fingerprint": runtime["report_fingerprint"],
        "existing_artifacts_unchanged": True,
        "selection_performed": False,
    }
    report = {**final, "report_fingerprint": fingerprint(final)}
    write_json(EXPERIMENT_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the isolated expanded morphology v4 experiment"
    )
    parser.add_argument("stage", choices=("prepare", "train", "validate", "all"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.stage == "prepare":
        result = prepare()
    elif args.stage == "train":
        result = train()
    elif args.stage == "validate":
        result = validate()
    else:
        result = run_all()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
