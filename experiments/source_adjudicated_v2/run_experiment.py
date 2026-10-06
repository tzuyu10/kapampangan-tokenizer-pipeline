from __future__ import annotations

import argparse
import copy
import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(REPOSITORY_ROOT / "runtime"))

from kapampangan_morphbpe.artifact import (  # noqa: E402
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.boundary_safe_bpe import BoundarySafeBPETrainer  # noqa: E402
from kapampangan_morphbpe.bpe import ConstrainedBPETrainer  # noqa: E402
from kapampangan_morphbpe.constants import (  # noqa: E402
    DATASET_FINGERPRINT,
    SCHEMA_VERSION,
    SPECIAL_TOKENS,
)
from kapampangan_morphbpe.lexicon import load_lexicon  # noqa: E402
from kapampangan_morphbpe.models import PreparedSequence, PretokenKind  # noqa: E402
from kapampangan_morphbpe.morphology import MorphologicalSegmenter  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key, normalize_text  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import (  # noqa: E402
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)

POLICY_PATH = EXPERIMENT_ROOT / "adjudication-policy.json"
RECONCILIATION_ROOT = REPOSITORY_ROOT / "experiments/internet_root_reconciliation_v1"
RECONCILIATION_MANIFEST_PATH = RECONCILIATION_ROOT / "reports/reconciliation-manifest.json"
WORD_EVIDENCE_PATH = RECONCILIATION_ROOT / "reports/word-evidence.csv"
CANDIDATE_EVIDENCE_PATH = RECONCILIATION_ROOT / "reports/candidate-evidence.csv"
FORMAN_INDEX_PATH = RECONCILIATION_ROOT / "runs/source-indexes/forman1971.jsonl"
ACD_INDEX_PATH = RECONCILIATION_ROOT / "runs/source-indexes/acd_v1_2.jsonl"

SOURCE_ROOT = REPOSITORY_ROOT / "experiments/source_adjudicated_v1"
SOURCE_LEXICON_PATH = SOURCE_ROOT / "resources/training-lexicon.json"
SOURCE_LEXICON_MANIFEST_PATH = SOURCE_ROOT / "resources/training-lexicon-manifest.json"
SOURCE_STREAM_PATH = SOURCE_ROOT / "runs/prepared/training-stream.jsonl"
SOURCE_STREAM_MANIFEST_PATH = SOURCE_ROOT / "runs/prepared/training-stream-manifest.json"

REPORTS_DIR = EXPERIMENT_ROOT / "reports"
RUNS_DIR = EXPERIMENT_ROOT / "runs"
ADJUDICATION_DIR = RUNS_DIR / "adjudication"
DIRECT_ROOTS_PATH = ADJUDICATION_DIR / "accepted-direct-roots.jsonl"
DERIVATIONS_PATH = ADJUDICATION_DIR / "accepted-derived-segmentations.jsonl"
DECISIONS_PATH = REPORTS_DIR / "adjudication-decisions.csv"
ADJUDICATION_MANIFEST_PATH = REPORTS_DIR / "adjudication-manifest.json"
ADJUDICATION_SUMMARY_PATH = REPORTS_DIR / "adjudication-summary.md"

RESOURCES_DIR = EXPERIMENT_ROOT / "resources"
LEXICON_PATH = RESOURCES_DIR / "training-lexicon.json"
LEXICON_MANIFEST_PATH = RESOURCES_DIR / "training-lexicon-manifest.json"
PREPARED_DIR = RUNS_DIR / "prepared"
STREAM_PATH = PREPARED_DIR / "training-stream.jsonl"
PREPARED_MANIFEST_PATH = PREPARED_DIR / "training-stream-manifest.json"
PLAIN_DIR = RUNS_DIR / "plain-bpe"
PLAIN_STREAM_PATH = PLAIN_DIR / "training-stream.jsonl"
PLAIN_MANIFEST_PATH = PLAIN_DIR / "training-stream-manifest.json"
SEGMENTATION_DIR = RUNS_DIR / "segmentations"
SEGMENTATION_PATH = SEGMENTATION_DIR / "accepted-segmentations.jsonl"
AUDIT_PATH = SEGMENTATION_DIR / "externally-supported-boundary-audit.jsonl"
SEGMENTATION_MANIFEST_PATH = SEGMENTATION_DIR / "segmentation-manifest.json"

ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"
TRAINING_REPORT_PATH = REPORTS_DIR / "training-report.json"
RUNTIME_REPORT_PATH = REPORTS_DIR / "runtime-evaluation.json"
EXPERIMENT_REPORT_PATH = REPORTS_DIR / "experiment-report.json"
EXPERIMENT_SUMMARY_PATH = REPORTS_DIR / "experiment-summary.md"

TARGETS = (6080, 8192, 16384)
RICHARDS_IDS = {"ocr-010", "ocr-011", "ocr-012"}
ACCEPTED_BASE_STATUSES = {"accepted", "protected_compound", "protected_root"}
EXPECTED_RECONCILIATION_FINGERPRINT = (
    "060ae78414674a83464ce2e3d4bdfd1ee276bc019297120a9822c34b4af0485f"
)
EXPECTED_FORMAN_SHA256 = "cf2d2963d75577804ae5bdf688d24ccfbedcf84230a94e5f119f949c0cbf12e9"
STRESS_MARKS = {"\u0300", "\u0301", "\u0302", "\u0304"}
STRESS_PUNCTUATION = {"'", "\u2019", "`", "\u00b4", "\u02c8", "\u02cc", ":", "\ufffd"}

PRESERVED_ARTIFACTS = {
    "canonical-6080": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "source-v1-6080": SOURCE_ROOT / "artifacts/selected-tokenizer",
    "plain-6080": SOURCE_ROOT / "artifacts/plain-bpe-tokenizer",
    "plain-8192": REPOSITORY_ROOT
    / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
    "plain-16384": REPOSITORY_ROOT
    / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
    "boundary-safe-v1-6080": REPOSITORY_ROOT
    / "experiments/boundary_safe_v1/artifacts/candidates/vocab-6080",
}


@dataclass(frozen=True, slots=True)
class FormanEntry:
    headword: str
    definition: str
    role: str
    page: int
    record_id: str


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _policy() -> dict[str, Any]:
    policy = _object(read_json(POLICY_PATH), "v2 adjudication policy")
    if policy.get("target_vocabulary_sizes") != list(TARGETS):
        raise ValueError("v2 vocabulary targets changed")
    if set(cast(list[str], policy.get("richards_candidate_ids_held"))) != RICHARDS_IDS:
        raise ValueError("v2 must hold exactly Richards rows ocr-010 through ocr-012")
    if (
        _object(policy.get("selection_policy"), "selection policy").get("selection_performed")
        is not False
    ):
        raise ValueError("v2 candidates must not claim validation-based selection")
    return policy


def _remove_vowel_stress(text: str) -> str:
    output: list[str] = []
    base = ""
    for character in unicodedata.normalize("NFD", text):
        if unicodedata.combining(character):
            if character in STRESS_MARKS and base.casefold() in "aeiou":
                continue
            output.append(character)
            continue
        base = character
        if character not in STRESS_PUNCTUATION:
            output.append(character)
    return unicodedata.normalize("NFC", "".join(output))


def _lexical_key(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = _remove_vowel_stress(normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    normalized = normalized.strip('-\u2013\u2014/.,;()[]{}"')
    return comparison_key(normalized)


def _forman_role(definition: str) -> str:
    lowered = definition.casefold().strip()
    if not lowered:
        return "unclassified_headword"
    if re.search(r"(?:^|[.;])\s*(?:see|c\.f\.)\s", lowered):
        return "cross_reference_headword"
    class_match = re.match(r"\(([^)]+)\)", lowered)
    if class_match is not None:
        unaffixable = (
            "particle",
            "substitute",
            "subs",
            "cmp",
            "prep",
            "cocomb",
            "subcomb",
            "neg",
            "adjunct",
            "pronoun",
            "excl",
            "interj",
        )
        if any(marker in class_match.group(1) for marker in unaffixable):
            return "unaffixable_headword"
    return "root_or_stem_headword"


def _headword_parts(value: str) -> tuple[str, ...]:
    output: list[str] = []
    for part in re.split(r"\s*/\s*", value.strip()):
        cleaned = part.strip().strip(",.;")
        if cleaned and any(character.isalpha() for character in cleaned):
            output.append(cleaned)
    return tuple(output)


def _parse_forman_entries(path: Path) -> list[FormanEntry]:
    try:
        from pypdf import PdfReader  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - depends on the selected runtime
        raise RuntimeError(
            "The adjudicate stage needs pypdf; use the bundled Codex Python runtime."
        ) from exc

    reader = PdfReader(path)
    entries: list[FormanEntry] = []

    def append_entry(page: int, ordinal: int, headword: str, definition: str) -> None:
        if len(headword) > 60 or not any(character.isalpha() for character in headword):
            return
        if headword.isupper() and len(headword) <= 4:
            return
        role = _forman_role(definition)
        for part_number, part in enumerate(_headword_parts(headword), 1):
            entries.append(
                FormanEntry(
                    headword=part,
                    definition=definition,
                    role=role,
                    page=page,
                    record_id=f"forman1971-p{page:03d}-{ordinal:03d}-{part_number:02d}",
                )
            )

    for page_index in range(15, len(reader.pages)):
        text = reader.pages[page_index].extract_text(extraction_mode="layout") or ""
        ordinal = 0
        current_headword: str | None = None
        current_definition: list[str] = []
        for line in text.splitlines():
            if not line:
                continue
            if line[0].isspace():
                if current_headword is not None and line.strip():
                    current_definition.append(line.strip())
                continue
            if current_headword is not None:
                ordinal += 1
                append_entry(
                    page_index + 1,
                    ordinal,
                    current_headword,
                    " ".join(current_definition),
                )
            match = re.match(r"(.+?)\s{2,}(\S.*)$", line)
            current_headword = match.group(1).strip() if match else line.strip()
            current_definition = [match.group(2).strip()] if match else []
        if current_headword is not None:
            ordinal += 1
            append_entry(
                page_index + 1,
                ordinal,
                current_headword,
                " ".join(current_definition),
            )
    return entries


def _definition_forms(definition: str) -> frozenset[str]:
    forms: set[str] = set()
    for token in re.findall(
        r"[^\W\d_]+(?:['\u2019:`\u00b4\u02c8\u02cc\ufffd-][^\W\d_]+)*", definition
    ):
        key = _lexical_key(token)
        if key:
            forms.add(key)
    return frozenset(forms)


def _cross_reference_targets(definition: str) -> frozenset[str]:
    targets: set[str] = set()
    for match in re.finditer(r"(?:^|[.;])\s*(?:see|c\.f\.)\s+([^.;]+)", definition, re.I):
        targets.update(_definition_forms(match.group(1)))
    return frozenset(targets)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if line.strip():
                rows.append(_object(json.loads(line), f"{path.name} line {line_number}"))
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(stable_compact_json(row) + "\n")


def _split_segments(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in value.split(" + ") if part.strip())


def _split_boundaries(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("|") if part)


def _letter_count(value: str) -> int:
    return sum(character.isalpha() for character in value)


def _operational_root(value: str, minimum_letters: int) -> bool:
    normalized = normalize_text(value)
    return (
        normalized == value
        and _letter_count(value) >= minimum_letters
        and all(
            unicodedata.category(character)[0] in {"L", "M"} or character in {"'", "\u2019"}
            for character in value
        )
    )


def _verify_reconciliation() -> dict[str, Any]:
    manifest = _object(read_json(RECONCILIATION_MANIFEST_PATH), "reconciliation manifest")
    body = {key: value for key, value in manifest.items() if key != "manifest_fingerprint"}
    if fingerprint(body) != manifest.get("manifest_fingerprint"):
        raise ValueError("reconciliation manifest fingerprint mismatch")
    if manifest.get("manifest_fingerprint") != EXPECTED_RECONCILIATION_FINGERPRINT:
        raise ValueError("the frozen reconciliation result changed")
    output_hashes = _object(manifest.get("output_sha256"), "reconciliation output hashes")
    expected = {
        WORD_EVIDENCE_PATH: output_hashes.get("word_evidence_csv"),
        CANDIDATE_EVIDENCE_PATH: output_hashes.get("candidate_evidence_csv"),
    }
    for path, expected_hash in expected.items():
        if sha256_file(path) != expected_hash:
            raise ValueError(f"reconciliation output changed: {path}")
    source_summary = _object(manifest.get("source_summary"), "source summary")
    for source_id, path in (("forman1971", FORMAN_INDEX_PATH), ("acd_v1_2", ACD_INDEX_PATH)):
        source = _object(source_summary.get(source_id), source_id)
        if sha256_file(path) != source.get("index_sha256"):
            raise ValueError(f"source index changed: {source_id}")
    return manifest


def _candidate_relation_evidence(
    candidate: dict[str, str],
    forman_by_headword: dict[str, list[FormanEntry]],
    acd_by_surface: dict[str, list[dict[str, Any]]],
) -> list[dict[str, str]]:
    surface = candidate["surface"]
    root = candidate["root_hypothesis"]
    segments = _split_segments(candidate["segments"])
    surface_key = _lexical_key(surface)
    root_key = _lexical_key(root)
    evidence: list[dict[str, str]] = []

    for entry in forman_by_headword.get(surface_key, []):
        if entry.role != "cross_reference_headword":
            continue
        if root_key in _cross_reference_targets(entry.definition):
            evidence.append(
                {
                    "kind": "forman_cross_reference_to_root",
                    "location": f"PDF page {entry.page}",
                    "record_id": entry.record_id,
                    "source_id": "forman1971",
                }
            )

    for entry in forman_by_headword.get(root_key, []):
        if entry.role != "root_or_stem_headword":
            continue
        if surface_key in _definition_forms(entry.definition):
            evidence.append(
                {
                    "kind": "forman_root_entry_lists_derived_form",
                    "location": f"PDF page {entry.page}",
                    "record_id": entry.record_id,
                    "source_id": "forman1971",
                }
            )

    expected_segments = tuple(_lexical_key(segment) for segment in segments)
    for row in acd_by_surface.get(surface_key, []):
        raw_form = str(row.get("raw_form", ""))
        raw_segments = tuple(key for part in raw_form.split("-") if (key := _lexical_key(part)))
        if len(raw_segments) < 2 or raw_segments != expected_segments:
            continue
        evidence.append(
            {
                "kind": "acd_explicit_hyphenated_segmentation",
                "location": str(row.get("location", "")),
                "record_id": str(row.get("source_record_id", "")),
                "source_id": "acd_v1_2",
            }
        )
    unique = {(row["kind"], row["source_id"], row["record_id"]): row for row in evidence}
    return [unique[key] for key in sorted(unique)]


def adjudicate(forman_pdf: Path) -> dict[str, Any]:
    policy = _policy()
    reconciliation = _verify_reconciliation()
    if sha256_file(forman_pdf) != EXPECTED_FORMAN_SHA256:
        raise ValueError("Forman PDF does not match the reconciled source")

    word_rows: dict[str, dict[str, str]] = {}
    with WORD_EVIDENCE_PATH.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            word_rows[row["surface"]] = row

    candidates: list[dict[str, str]] = []
    with CANDIDATE_EVIDENCE_PATH.open("r", encoding="utf-8", newline="") as stream:
        candidates.extend(csv.DictReader(stream))

    forman_entries = _parse_forman_entries(forman_pdf)
    forman_by_headword: dict[str, list[FormanEntry]] = defaultdict(list)
    for entry in forman_entries:
        forman_by_headword[_lexical_key(entry.headword)].append(entry)

    acd_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in _load_jsonl(ACD_INDEX_PATH):
        raw_form = str(row.get("raw_form", ""))
        parts = [_lexical_key(part) for part in raw_form.split("-")]
        collapsed = "".join(part for part in parts if part)
        if collapsed:
            acd_by_surface[collapsed].append(row)

    direct_policy = _object(policy.get("direct_root_policy"), "direct-root policy")
    derived_policy = _object(policy.get("derived_policy"), "derived policy")
    minimum_direct = int(direct_policy["minimum_letters"])
    minimum_derived = int(derived_policy["minimum_root_letters"])
    allowed_kinds = set(cast(list[str], derived_policy["accepted_analysis_kinds"]))
    allowed_decisions = set(cast(list[str], derived_policy["accepted_word_decisions"]))

    base_lexicon = load_lexicon(SOURCE_LEXICON_PATH)
    accepted_roots: dict[str, dict[str, object]] = {}
    accepted_derivations: list[dict[str, object]] = []
    decision_counts: Counter[str] = Counter()
    decision_occurrences: Counter[str] = Counter()
    relation_counts: Counter[str] = Counter()
    decision_rows: list[dict[str, object]] = []

    for candidate in candidates:
        surface = candidate["surface"]
        word = word_rows[surface]
        frequency = int(candidate["frequency"])
        decision = "held"
        reason = "outside_conservative_v2_policy"
        relation: list[dict[str, str]] = []

        if (
            word["decision"] == direct_policy["decision"]
            and candidate["analysis_kind"] == direct_policy["candidate_kind"]
            and candidate["evidence_status"] == direct_policy["required_evidence_status"]
            and not word["quality_flags"]
            and _operational_root(candidate["root_hypothesis"], minimum_direct)
        ):
            key = comparison_key(candidate["root_hypothesis"])
            root = accepted_roots.setdefault(
                key,
                {
                    "comparison_key": key,
                    "frequency": 0,
                    "root_evidence": set(),
                    "surfaces": set(),
                    "support": set(),
                },
            )
            cast(set[str], root["surfaces"]).add(candidate["root_hypothesis"])
            cast(set[str], root["root_evidence"]).update(
                item.strip() for item in candidate["evidence_sources"].split(" | ") if item
            )
            cast(set[str], root["support"]).add("direct_exact_root_match")
            root["frequency"] = cast(int, root["frequency"]) + frequency
            decision = "accepted_direct_root"
            reason = "exact_eligible_root_entry_and_clean_operational_form"

        if (
            candidate["analysis_kind"] in allowed_kinds
            and word["decision"] in allowed_decisions
            and candidate["evidence_status"] == derived_policy["required_evidence_status"]
            and not word["quality_flags"]
            and _operational_root(candidate["root_hypothesis"], minimum_derived)
            and (word["decision"] != "already_analyzed" or candidate["current_selected"] == "true")
        ):
            relation = _candidate_relation_evidence(candidate, forman_by_headword, acd_by_surface)
            if relation:
                segments = _split_segments(candidate["segments"])
                boundaries = _split_boundaries(candidate["boundaries"])
                if "".join(segments) != surface:
                    raise ValueError(f"candidate segments do not reconstruct {surface!r}")
                accepted_derivations.append(
                    {
                        "analysis_kind": candidate["analysis_kind"],
                        "boundaries": list(boundaries),
                        "current_selected": candidate["current_selected"] == "true",
                        "evidence_sources": candidate["evidence_sources"],
                        "frequency": frequency,
                        "relation_evidence": relation,
                        "root": candidate["root_hypothesis"],
                        "rule_id": candidate["rule_id"],
                        "segments": list(segments),
                        "surface": surface,
                        "word_decision": word["decision"],
                    }
                )
                for item in relation:
                    relation_counts[item["kind"]] += 1
                root_key = comparison_key(candidate["root_hypothesis"])
                if root_key not in base_lexicon.valid_hosts:
                    root = accepted_roots.setdefault(
                        root_key,
                        {
                            "comparison_key": root_key,
                            "frequency": 0,
                            "root_evidence": set(),
                            "surfaces": set(),
                            "support": set(),
                        },
                    )
                    cast(set[str], root["surfaces"]).add(candidate["root_hypothesis"])
                    cast(set[str], root["root_evidence"]).update(
                        item.strip() for item in candidate["evidence_sources"].split(" | ") if item
                    )
                    cast(set[str], root["support"]).add("explicit_derived_relation_host")
                decision = (
                    "accepted_existing_derived_confirmation"
                    if candidate["current_selected"] == "true"
                    else "accepted_new_derived_segmentation"
                )
                reason = "+".join(sorted({item["kind"] for item in relation}))

        decision_counts[decision] += 1
        decision_occurrences[decision] += frequency
        if decision != "held":
            decision_rows.append(
                {
                    "analysis_kind": candidate["analysis_kind"],
                    "decision": decision,
                    "frequency": frequency,
                    "reason": reason,
                    "root": candidate["root_hypothesis"],
                    "rule_id": candidate["rule_id"],
                    "surface": surface,
                }
            )

    accepted_derivations.sort(
        key=lambda row: (cast(str, row["surface"]).encode("utf-8"), cast(str, row["rule_id"]))
    )
    duplicate_surfaces = [
        surface
        for surface, count in Counter(
            cast(str, row["surface"]) for row in accepted_derivations
        ).items()
        if count > 1
    ]
    if duplicate_surfaces:
        raise ValueError(
            f"v2 relation policy produced ambiguous surfaces: {duplicate_surfaces[:20]}"
        )

    root_rows: list[dict[str, object]] = []
    for key, row in sorted(accepted_roots.items()):
        surfaces = sorted(
            cast(set[str], row["surfaces"]), key=lambda value: (value.casefold(), value)
        )
        root_rows.append(
            {
                "canonical_surface": min(
                    surfaces, key=lambda value: (value != value.casefold(), value)
                ),
                "comparison_key": key,
                "frequency": row["frequency"],
                "root_evidence": sorted(cast(set[str], row["root_evidence"])),
                "support": sorted(cast(set[str], row["support"])),
                "surfaces": surfaces,
            }
        )

    required = set(cast(list[str], policy.get("required_boundary_safe_regressions")))
    derivation_surfaces = {cast(str, row["surface"]) for row in accepted_derivations}
    missing_required = required - derivation_surfaces
    if missing_required:
        raise AssertionError(
            f"required regressions lack explicit source relationships: {sorted(missing_required)}"
        )

    _write_jsonl(DIRECT_ROOTS_PATH, root_rows)
    _write_jsonl(DERIVATIONS_PATH, accepted_derivations)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with DECISIONS_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
                "surface",
                "frequency",
                "decision",
                "analysis_kind",
                "rule_id",
                "root",
                "reason",
            ),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(decision_rows, key=lambda row: str(row["surface"]).encode()))

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "evidence_label": policy.get("evidence_label"),
        "independent_evaluation_gold": False,
        "policy_sha256": sha256_file(POLICY_PATH),
        "reconciliation_manifest_fingerprint": reconciliation.get("manifest_fingerprint"),
        "forman_pdf_sha256": sha256_file(forman_pdf),
        "forman_entries_parsed": len(forman_entries),
        "accepted_root_keys": len(root_rows),
        "accepted_derived_types": len(accepted_derivations),
        "accepted_derived_occurrences": sum(
            cast(int, row["frequency"]) for row in accepted_derivations
        ),
        "decision_candidate_counts": dict(sorted(decision_counts.items())),
        "decision_candidate_occurrences": dict(sorted(decision_occurrences.items())),
        "relation_evidence_counts": dict(sorted(relation_counts.items())),
        "direct_roots_sha256": sha256_file(DIRECT_ROOTS_PATH),
        "derivations_sha256": sha256_file(DERIVATIONS_PATH),
        "decisions_csv_sha256": sha256_file(DECISIONS_PATH),
        "required_regressions": sorted(required),
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    manifest = {**body, "manifest_fingerprint": fingerprint(body)}
    write_json(ADJUDICATION_MANIFEST_PATH, manifest)
    _write_adjudication_summary(manifest)
    return cast(dict[str, Any], manifest)


def _write_adjudication_summary(manifest: dict[str, Any]) -> None:
    decisions = _object(manifest.get("decision_candidate_counts"), "decision counts")
    relations = _object(manifest.get("relation_evidence_counts"), "relation counts")
    lines = [
        "# Source-adjudicated v2 decision summary",
        "",
        "Status: frozen provisional local-test decisions; not independent linguistic gold.",
        "",
        f"- Accepted root keys: **{manifest['accepted_root_keys']:,}**.",
        f"- Explicitly supported derived word types: **{manifest['accepted_derived_types']:,}**.",
        f"- Supported derived occurrences: **{manifest['accepted_derived_occurrences']:,}**.",
        "- Conflicts, clitic hypotheses, noisy rows, and root-only affix guesses remain held.",
        "",
        "## Accepted candidate decisions",
        "",
        "| Decision | Candidate rows |",
        "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {value:,} |" for key, value in sorted(decisions.items()))
    lines.extend(
        [
            "",
            "## Explicit relationship evidence",
            "",
            "| Evidence | Accepted rows |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{key}` | {value:,} |" for key, value in sorted(relations.items()))
    lines.extend(
        [
            "",
            "`sinulat` and `kabukasan` are mandatory externally supported boundary-safe audits.",
            "A dictionary root match by itself never authorizes a new affix segmentation.",
            "",
        ]
    )
    ADJUDICATION_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def _verified_adjudication() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = _object(read_json(ADJUDICATION_MANIFEST_PATH), "adjudication manifest")
    body = {key: value for key, value in manifest.items() if key != "manifest_fingerprint"}
    if fingerprint(body) != manifest.get("manifest_fingerprint"):
        raise ValueError("adjudication manifest fingerprint mismatch")
    if sha256_file(POLICY_PATH) != manifest.get("policy_sha256"):
        raise ValueError("adjudication policy changed")
    if sha256_file(DIRECT_ROOTS_PATH) != manifest.get("direct_roots_sha256"):
        raise ValueError("accepted root list changed")
    if sha256_file(DERIVATIONS_PATH) != manifest.get("derivations_sha256"):
        raise ValueError("accepted derivation list changed")
    roots = _load_jsonl(DIRECT_ROOTS_PATH)
    derivations = _load_jsonl(DERIVATIONS_PATH)
    if len(roots) != manifest.get("accepted_root_keys"):
        raise ValueError("accepted root count mismatch")
    if len(derivations) != manifest.get("accepted_derived_types"):
        raise ValueError("accepted derivation count mismatch")
    return manifest, roots, derivations


def _source_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    stream_manifest = _object(read_json(SOURCE_STREAM_MANIFEST_PATH), "source stream manifest")
    lexicon_manifest = _object(read_json(SOURCE_LEXICON_MANIFEST_PATH), "source lexicon manifest")
    if sha256_file(SOURCE_STREAM_PATH) != stream_manifest.get("stream_sha256"):
        raise ValueError("source-v1 stream hash mismatch")
    if sha256_file(SOURCE_LEXICON_PATH) != lexicon_manifest.get("lexicon_file_sha256"):
        raise ValueError("source-v1 lexicon hash mismatch")
    if set(cast(list[str], lexicon_manifest.get("richards_candidate_ids_held"))) != RICHARDS_IDS:
        raise ValueError("source-v1 Richards hold changed")
    return stream_manifest, lexicon_manifest


def _build_lexicon(
    adjudication: dict[str, Any],
    root_rows: list[dict[str, Any]],
    word_frequencies: Counter[str],
) -> dict[str, Any]:
    source_document = _object(read_json(SOURCE_LEXICON_PATH), "source-v1 lexicon")
    document = copy.deepcopy(source_document)
    document.pop("lexicon_fingerprint", None)
    roots = cast(list[dict[str, Any]], document.get("roots"))
    existing = {str(row["comparison_key"]) for row in roots}
    added = 0
    for row in root_rows:
        key = str(row["comparison_key"])
        if key in existing:
            continue
        surfaces = cast(list[str], row["surfaces"])
        sources = cast(list[str], row["root_evidence"])
        roots.append(
            {
                "attested_in_train": word_frequencies[key] > 0,
                "canonical_surface": str(row["canonical_surface"]),
                "comparison_key": key,
                "provisional": True,
                "sources": [
                    {
                        "description": "Conservative v2 exact root evidence; local-test only.",
                        "example": "",
                        "form": str(row["canonical_surface"]),
                        "id": f"source-adjudicated-v2-{key}",
                        "source": ";".join(sources),
                        "type": "external_source_provisional_root",
                    }
                ],
                "surfaces": surfaces,
                "train_frequency": word_frequencies[key],
            }
        )
        existing.add(key)
        added += 1
    roots.sort(key=lambda row: str(row["comparison_key"]))
    document["evidence_status"] = "external_source_supported_provisional_silver_not_gold"
    construction = _object(document.get("construction_policy"), "construction policy")
    construction.update(
        {
            "exact_word_adjudication_allowlist": True,
            "root_match_alone_authorizes_affix_segmentation": False,
            "richards_evidence_operational": False,
            "source_adjudicated_v2": True,
        }
    )
    document["source_adjudicated_v2"] = {
        "added_root_keys": added,
        "adjudication_manifest_fingerprint": adjudication.get("manifest_fingerprint"),
        "exact_derived_segmentations": adjudication.get("accepted_derived_types"),
        "independent_evaluation_gold": False,
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    lexicon_fingerprint = fingerprint(document)
    output = {**document, "lexicon_fingerprint": lexicon_fingerprint}
    write_json(LEXICON_PATH, output)

    source_manifest = _object(read_json(SOURCE_LEXICON_MANIFEST_PATH), "source lexicon manifest")
    counts = copy.deepcopy(_object(source_manifest.get("counts"), "source lexicon counts"))
    counts["operational_root_keys"] = len(roots)
    counts["operational_root_surfaces"] = sum(
        len(cast(list[str], row["surfaces"])) for row in roots
    )
    counts["v2_added_root_keys"] = added
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "evidence_status": document["evidence_status"],
        "lexicon_fingerprint": lexicon_fingerprint,
        "lexicon_file_sha256": sha256_file(LEXICON_PATH),
        "counts": counts,
        "input_files": {
            "adjudication_manifest_sha256": sha256_file(ADJUDICATION_MANIFEST_PATH),
            "source_v1_lexicon_sha256": sha256_file(SOURCE_LEXICON_PATH),
            "source_v1_stream_sha256": sha256_file(SOURCE_STREAM_PATH),
        },
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
    }
    manifest = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(LEXICON_MANIFEST_PATH, manifest)
    load_lexicon(LEXICON_PATH)
    return cast(dict[str, Any], manifest)


def _surface_kind_frequencies(
    sequences: list[PreparedSequence],
) -> Counter[tuple[str, PretokenKind]]:
    counts: Counter[tuple[str, PretokenKind]] = Counter()
    for sequence in sequences:
        counts[(sequence.surface, sequence.kind)] += sequence.frequency
    return counts


def _write_stream(path: Path, sequences: list[PreparedSequence]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for sequence in sequences:
            stream.write(
                stable_compact_json(
                    {
                        "frequency": sequence.frequency,
                        "kind": sequence.kind,
                        "protected_boundaries": list(sequence.protected_boundaries),
                        "surface": sequence.surface,
                    }
                )
                + "\n"
            )


def prepare() -> dict[str, Any]:
    policy = _policy()
    adjudication, root_rows, derivations = _verified_adjudication()
    source_manifest, source_lexicon_manifest = _source_inputs()
    source_sequences = load_prepared_stream(SOURCE_STREAM_PATH)
    frequencies: Counter[str] = Counter()
    for sequence in source_sequences:
        if sequence.kind == "word":
            frequencies[comparison_key(sequence.surface)] += sequence.frequency
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    lexicon_manifest = _build_lexicon(adjudication, root_rows, frequencies)

    derivation_by_surface = {str(row["surface"]): row for row in derivations}
    sequence_by_surface = {
        sequence.surface: sequence for sequence in source_sequences if sequence.kind == "word"
    }
    missing = set(derivation_by_surface) - set(sequence_by_surface)
    if missing:
        raise ValueError(f"accepted derivations missing from source stream: {sorted(missing)[:20]}")

    changed: list[dict[str, object]] = []
    prepared: list[PreparedSequence] = []
    for sequence in source_sequences:
        row = derivation_by_surface.get(sequence.surface) if sequence.kind == "word" else None
        boundaries = sequence.protected_boundaries
        if row is not None:
            proposed = tuple(cast(list[int], row["boundaries"]))
            if bool(row["current_selected"]):
                if proposed != boundaries:
                    raise ValueError(f"confirmed current analysis changed: {sequence.surface!r}")
            else:
                if boundaries:
                    raise ValueError(
                        f"new v2 derivation replaces an existing analysis: {sequence.surface!r}"
                    )
                boundaries = proposed
                changed.append(
                    {
                        "frequency": sequence.frequency,
                        "new_boundaries": list(boundaries),
                        "rule_id": row["rule_id"],
                        "segments": row["segments"],
                        "surface": sequence.surface,
                    }
                )
        prepared.append(
            PreparedSequence(sequence.surface, boundaries, sequence.kind, sequence.frequency)
        )

    if _surface_kind_frequencies(prepared) != _surface_kind_frequencies(source_sequences):
        raise AssertionError("v2 preparation changed surfaces, kinds, or frequencies")
    _write_stream(STREAM_PATH, prepared)

    plain = [
        PreparedSequence(surface, (), kind, frequency)
        for (surface, kind), frequency in sorted(_surface_kind_frequencies(prepared).items())
    ]
    _write_stream(PLAIN_STREAM_PATH, plain)

    characters = sorted(
        {character for sequence in prepared for character in sequence.surface},
        key=lambda value: value.encode("utf-8"),
    )
    status_types: Counter[str] = Counter()
    status_occurrences: Counter[str] = Counter()
    base_segmenter = MorphologicalSegmenter.from_path(SOURCE_LEXICON_PATH)
    added_root_keys = {
        str(row["comparison_key"])
        for row in root_rows
        if str(row["comparison_key"]) not in base_segmenter.lexicon.valid_hosts
    }
    segmentation_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []
    for sequence in prepared:
        if sequence.kind != "word":
            continue
        override = derivation_by_surface.get(sequence.surface)
        base = base_segmenter.segment(sequence.surface)
        if override is not None:
            row = {
                "evidence": override["relation_evidence"],
                "frequency": sequence.frequency,
                "kind": override["analysis_kind"],
                "protected_boundaries": override["boundaries"],
                "rule_id": override["rule_id"],
                "segments": override["segments"],
                "status": "accepted",
                "surface": sequence.surface,
                "trace": ["source_adjudicated_v2:explicit_relation"],
            }
            segmentation_rows.append(row)
            audit_rows.append(row)
            status = "accepted"
        elif base.status in ACCEPTED_BASE_STATUSES:
            segmentation_rows.append(
                {
                    "evidence": "source_adjudicated_v1",
                    "frequency": sequence.frequency,
                    "kind": base.kind,
                    "protected_boundaries": list(base.protected_boundaries),
                    "rule_id": base.rule_id,
                    "segments": list(base.segments),
                    "status": base.status,
                    "surface": sequence.surface,
                    "trace": list(base.trace),
                }
            )
            status = base.status
        elif comparison_key(sequence.surface) in added_root_keys:
            segmentation_rows.append(
                {
                    "evidence": "source_adjudicated_v2:exact_root",
                    "frequency": sequence.frequency,
                    "kind": "root",
                    "protected_boundaries": [],
                    "rule_id": "ROOT",
                    "segments": [sequence.surface],
                    "status": "protected_root",
                    "surface": sequence.surface,
                    "trace": ["source_adjudicated_v2:protected_root"],
                }
            )
            status = "protected_root"
        else:
            status = base.status
        status_types[status] += 1
        status_occurrences[status] += sequence.frequency

    segmentation_rows.sort(key=lambda row: cast(str, row["surface"]).encode())
    audit_rows.sort(key=lambda row: cast(str, row["surface"]).encode())
    _write_jsonl(SEGMENTATION_PATH, segmentation_rows)
    _write_jsonl(AUDIT_PATH, audit_rows)
    required = set(cast(list[str], policy.get("required_boundary_safe_regressions")))
    audit_surfaces = {cast(str, row["surface"]) for row in audit_rows}
    if not required <= audit_surfaces:
        raise AssertionError("required boundary-safe regressions are not in the audit list")

    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "input_train_sha256": source_manifest.get("input_train_sha256"),
        "lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "source_v1_stream_sha256": sha256_file(SOURCE_STREAM_PATH),
        "source_v1_prepared_manifest_fingerprint": source_manifest.get("manifest_fingerprint"),
        "source_v1_lexicon_manifest_fingerprint": source_lexicon_manifest.get(
            "manifest_fingerprint"
        ),
        "adjudication_manifest_fingerprint": adjudication.get("manifest_fingerprint"),
        "stream_sha256": sha256_file(STREAM_PATH),
        "plain_stream_sha256": sha256_file(PLAIN_STREAM_PATH),
        "surface_kind_frequencies_preserved": True,
        "unique_prepared_sequences": len(prepared),
        "pretoken_occurrences": sum(sequence.frequency for sequence in prepared),
        "word_types": sum(sequence.kind == "word" for sequence in prepared),
        "word_occurrences": sum(
            sequence.frequency for sequence in prepared if sequence.kind == "word"
        ),
        "character_inventory": characters,
        "character_inventory_size": len(characters),
        "initial_vocabulary_size": len(characters) + len(SPECIAL_TOKENS),
        "new_boundary_types": len(changed),
        "new_boundary_occurrences": sum(cast(int, row["frequency"]) for row in changed),
        "new_boundary_rows": changed,
        "status_types": dict(sorted(status_types.items())),
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "raw_validation_csv_available": False,
        "independent_evaluation_gold": False,
    }
    prepared_manifest = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(PREPARED_MANIFEST_PATH, prepared_manifest)

    plain_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "tokenizer_condition": "plain_bpe",
        "source_prepared_manifest_fingerprint": prepared_manifest["manifest_fingerprint"],
        "source_stream_sha256": prepared_manifest["stream_sha256"],
        "stream_sha256": sha256_file(PLAIN_STREAM_PATH),
        "surface_kind_frequencies_preserved": True,
        "only_training_difference": "all_protected_morphology_boundaries_cleared",
    }
    write_json(PLAIN_MANIFEST_PATH, {**plain_body, "manifest_fingerprint": fingerprint(plain_body)})

    segmentation_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "accepted_types": len(segmentation_rows),
        "accepted_occurrences": sum(cast(int, row["frequency"]) for row in segmentation_rows),
        "external_relation_audit_types": len(audit_rows),
        "external_relation_audit_occurrences": sum(
            cast(int, row["frequency"]) for row in audit_rows
        ),
        "accepted_segmentations_sha256": sha256_file(SEGMENTATION_PATH),
        "audit_sha256": sha256_file(AUDIT_PATH),
        "required_regressions": sorted(required),
        "independent_evaluation_gold": False,
    }
    segmentation_manifest = {
        **segmentation_body,
        "manifest_fingerprint": fingerprint(segmentation_body),
    }
    write_json(SEGMENTATION_MANIFEST_PATH, segmentation_manifest)
    return cast(dict[str, Any], prepared_manifest)


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


def _tokenizer_card(condition: str, target: int) -> str:
    descriptions = {
        "plain": (
            "Plain BPE control trained on the identical surface/kind/frequency stream "
            "with all morphology boundaries cleared."
        ),
        "morphbpe": (
            "Paper-runtime MorphBPE candidate trained with conservative "
            "source-adjudicated v2 boundaries; inference is ordinary lexicon-free BPE."
        ),
        "boundary-safe": (
            "Boundary-safe training extension audited against explicit external source "
            "relationships; inference is ordinary lexicon-free BPE."
        ),
    }
    return f"""# Source-adjudicated v2 {condition} tokenizer ({target:,})

Artifact fingerprint: `{{ARTIFACT_FINGERPRINT}}`

{descriptions[condition]}

This is an isolated provisional local-test artifact, not a selected final model
and not independent linguistic gold. The unavailable validation split was not
reconstructed or re-evaluated. Richards evidence remains held.
"""


def _export_family(
    condition: str,
    first: dict[int, Any],
    second: dict[int, Any],
    training_family_fingerprint: str,
    segmentation_fingerprint: str,
) -> dict[str, object]:
    manifests: dict[str, object] = {}
    artifact_type = "kapampangan_plain_bpe" if condition == "plain" else "kapampangan_morphbpe"
    for target in TARGETS:
        metadata: dict[str, object] = {
            "candidate": True,
            "current_validation_re_evaluated": False,
            "held_out_test_used": False,
            "independent_evaluation_gold_used": False,
            "lexicon_used_at_runtime": False,
            "selection_performed": False,
            "source_adjudicated_v2": True,
            "segmentation_manifest_fingerprint": segmentation_fingerprint,
            "training_family_fingerprint": training_family_fingerprint,
            "tokenizer_condition": condition,
        }
        if condition == "boundary-safe":
            metadata["runtime_boundary_guarantee_scope"] = (
                "lowercase_and_titlecase_sinulat_and_kabukasan"
            )
            metadata["external_relation_list_is_evaluation_only"] = True
        output = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
        rebuild = ARTIFACTS_DIR / condition / "determinism-rebuild" / f"vocab-{target}"
        first_manifest = export_tokenizer_artifact(
            first[target],
            output,
            artifact_type=artifact_type,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(condition, target),
        )
        second_manifest = export_tokenizer_artifact(
            second[target],
            rebuild,
            artifact_type=artifact_type,
            metadata=metadata,
            tokenizer_card=_tokenizer_card(condition, target),
        )
        if first_manifest != second_manifest or _directory_hashes(output) != _directory_hashes(
            rebuild
        ):
            raise AssertionError(f"{condition} {target} deterministic rebuild differs")
        validate_artifact_files(output)
        manifests[str(target)] = first_manifest
    return manifests


def train() -> dict[str, Any]:
    _policy()
    _verified_adjudication()
    source_manifest, _source_lexicon_manifest = _source_inputs()
    prepared_manifest = _object(read_json(PREPARED_MANIFEST_PATH), "v2 prepared manifest")
    segmentation_manifest = _object(
        read_json(SEGMENTATION_MANIFEST_PATH), "v2 segmentation manifest"
    )
    if sha256_file(STREAM_PATH) != prepared_manifest.get("stream_sha256"):
        raise ValueError("v2 prepared stream hash mismatch")
    if sha256_file(PLAIN_STREAM_PATH) != prepared_manifest.get("plain_stream_sha256"):
        raise ValueError("v2 plain stream hash mismatch")
    if sha256_file(AUDIT_PATH) != segmentation_manifest.get("audit_sha256"):
        raise ValueError("v2 boundary audit hash mismatch")

    before = _snapshot_preserved()
    prepared = load_prepared_stream(STREAM_PATH)
    plain = load_prepared_stream(PLAIN_STREAM_PATH)
    external_audit_rows = _load_jsonl(AUDIT_PATH)
    required = set(cast(list[str], _policy().get("required_boundary_safe_regressions")))
    required_keys = {value.casefold() for value in required}
    audit_rows = [
        row for row in external_audit_rows if str(row["surface"]).casefold() in required_keys
    ]
    if {str(row["surface"]).casefold() for row in audit_rows} != required_keys:
        raise ValueError("the required boundary-safe regression audit is incomplete")
    audit = [
        PreparedSequence(
            str(row["surface"]), tuple(cast(list[int], row["protected_boundaries"])), "word", 1
        )
        for row in audit_rows
        if cast(list[int], row["protected_boundaries"])
    ]
    if not audit:
        raise ValueError("v2 boundary audit is empty")

    first_plain, plain_report = ConstrainedBPETrainer(plain).train(list(TARGETS))
    second_plain, second_plain_report = ConstrainedBPETrainer(plain).train(list(TARGETS))
    first_morph, morph_report = ConstrainedBPETrainer(prepared).train(list(TARGETS))
    second_morph, second_morph_report = ConstrainedBPETrainer(prepared).train(list(TARGETS))
    first_safe, safe_report = BoundarySafeBPETrainer(prepared, audit).train(list(TARGETS))
    second_safe, second_safe_report = BoundarySafeBPETrainer(prepared, audit).train(list(TARGETS))

    reports = {
        "plain": plain_report,
        "plain_rebuild": second_plain_report,
        "morphbpe": morph_report,
        "morphbpe_rebuild": second_morph_report,
        "boundary_safe": safe_report,
        "boundary_safe_rebuild": second_safe_report,
    }
    for name, report in reports.items():
        if report.get("trained_targets") != list(TARGETS) or report.get("failed_targets") != []:
            raise AssertionError(f"{name} did not reach every vocabulary target")
        if report.get("protected_boundary_merge_violations") != 0:
            raise AssertionError(f"{name} crossed a protected training boundary")
    for condition, first, second in (
        ("plain", first_plain, second_plain),
        ("morphbpe", first_morph, second_morph),
        ("boundary-safe", first_safe, second_safe),
    ):
        for target in TARGETS:
            if first[target].to_dict() != second[target].to_dict():
                raise AssertionError(f"{condition} {target} in-memory rebuild differs")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "source_v1_prepared_manifest_fingerprint": source_manifest.get("manifest_fingerprint"),
        "v2_prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "target_vocabulary_sizes": list(TARGETS),
        "boundary_safe_training_audit_scope": "required_exact_regressions_only",
        "boundary_safe_training_audit_types": len(audit_rows),
        "external_relation_evaluation_types": len(external_audit_rows),
        "family_reports": reports,
        "deterministic_in_memory_rebuilds": True,
    }
    training_family_fingerprint = fingerprint(body)
    manifests = {
        "plain": _export_family(
            "plain",
            first_plain,
            second_plain,
            training_family_fingerprint,
            cast(str, segmentation_manifest["manifest_fingerprint"]),
        ),
        "morphbpe": _export_family(
            "morphbpe",
            first_morph,
            second_morph,
            training_family_fingerprint,
            cast(str, segmentation_manifest["manifest_fingerprint"]),
        ),
        "boundary-safe": _export_family(
            "boundary-safe",
            first_safe,
            second_safe,
            training_family_fingerprint,
            cast(str, segmentation_manifest["manifest_fingerprint"]),
        ),
    }
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("an existing tokenizer artifact changed during v2 training")
    final_body = {
        **body,
        "artifact_manifests": manifests,
        "existing_artifacts_unchanged": True,
        "training_family_fingerprint": training_family_fingerprint,
    }
    report = {**final_body, "report_fingerprint": fingerprint(final_body)}
    write_json(TRAINING_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def _runtime_metrics(condition: str, target: int, rows: list[dict[str, Any]]) -> dict[str, object]:
    artifact = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
    tokenizer = load_runtime_tokenizer(artifact)
    missed_types = 0
    missed_occurrences = 0
    extra_types = 0
    exact_types = 0
    exact_occurrences = 0
    required_results: dict[str, object] = {}
    required = set(cast(list[str], _policy().get("required_boundary_safe_regressions")))
    failures: list[dict[str, object]] = []
    for row in rows:
        surface = str(row["surface"])
        segments = tuple(cast(list[str], row["segments"]))
        gold = set(cast(list[int], row["protected_boundaries"]))
        frequency = int(row["frequency"])
        encoding = tokenizer.encode(surface)
        if tokenizer.decode(encoding.ids) != surface:
            raise AssertionError(f"{condition} {target} failed round trip for {surface!r}")
        pieces = tuple(token.token for token in encoding.tokens)
        predicted = {token.end for token in encoding.tokens[:-1]}
        missed = gold - predicted
        extra = predicted - gold
        if missed:
            missed_types += 1
            missed_occurrences += frequency
        if extra:
            extra_types += 1
        if pieces == segments:
            exact_types += 1
            exact_occurrences += frequency
        elif len(failures) < 100:
            failures.append(
                {
                    "expected": list(segments),
                    "pieces": list(pieces),
                    "surface": surface,
                }
            )
        if surface in required:
            required_results[surface] = {
                "boundary_preserved": not missed,
                "exact": pieces == segments,
                "expected": list(segments),
                "pieces": list(pieces),
            }
    return {
        "artifact_fingerprint": _object(
            read_json(artifact / "tokenizer-manifest.json"), "artifact manifest"
        ).get("artifact_fingerprint"),
        "vocabulary_size": tokenizer.vocabulary_size,
        "evaluated_types": len(rows),
        "evaluated_occurrences": sum(int(row["frequency"]) for row in rows),
        "missed_boundary_types": missed_types,
        "missed_boundary_occurrences": missed_occurrences,
        "extra_boundary_types": extra_types,
        "exact_segment_types": exact_types,
        "exact_segment_occurrences": exact_occurrences,
        "exact_failure_samples": failures,
        "required_regressions": required_results,
        "lexicon_used_at_runtime": False,
    }


def validate() -> dict[str, Any]:
    _policy()
    adjudication, _roots, _derivations = _verified_adjudication()
    prepared_manifest = _object(read_json(PREPARED_MANIFEST_PATH), "prepared manifest")
    segmentation_manifest = _object(read_json(SEGMENTATION_MANIFEST_PATH), "segmentation manifest")
    if sha256_file(SEGMENTATION_PATH) != segmentation_manifest.get("accepted_segmentations_sha256"):
        raise ValueError("accepted segmentation list changed")
    if sha256_file(AUDIT_PATH) != segmentation_manifest.get("audit_sha256"):
        raise ValueError("boundary audit list changed")
    accepted = _load_jsonl(SEGMENTATION_PATH)
    audit = _load_jsonl(AUDIT_PATH)

    targets: dict[str, object] = {}
    existing_plain = {
        6080: SOURCE_ROOT / "artifacts/plain-bpe-tokenizer",
        8192: REPOSITORY_ROOT
        / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
        16384: REPOSITORY_ROOT
        / "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
    }
    for target in TARGETS:
        for condition in ("plain", "morphbpe", "boundary-safe"):
            artifact = ARTIFACTS_DIR / condition / "candidates" / f"vocab-{target}"
            validate_artifact_files(artifact)
            manifest = _object(read_json(artifact / "tokenizer-manifest.json"), "artifact manifest")
            if manifest.get("actual_vocabulary_size") != target:
                raise AssertionError(f"{condition} {target} vocabulary mismatch")
        new_plain = ARTIFACTS_DIR / "plain" / "candidates" / f"vocab-{target}"
        if sha256_file(new_plain / "vocab.json") != sha256_file(
            existing_plain[target] / "vocab.json"
        ):
            raise AssertionError(f"v2 plain {target} vocabulary differs from the existing control")
        if sha256_file(new_plain / "merges.json") != sha256_file(
            existing_plain[target] / "merges.json"
        ):
            raise AssertionError(f"v2 plain {target} merges differ from the existing control")
        morph_metrics = _runtime_metrics("morphbpe", target, accepted)
        safe_metrics = _runtime_metrics("boundary-safe", target, accepted)
        safe_external_audit = _runtime_metrics("boundary-safe", target, audit)
        required_surfaces = set(
            cast(list[str], _policy().get("required_boundary_safe_regressions"))
        )
        required_keys = {value.casefold() for value in required_surfaces}
        guarantee_rows = [row for row in audit if str(row["surface"]).casefold() in required_keys]
        safe_guarantee = _runtime_metrics("boundary-safe", target, guarantee_rows)
        if safe_guarantee["missed_boundary_types"] != 0:
            raise AssertionError(f"boundary-safe {target} crossed a guaranteed boundary")
        required = cast(dict[str, dict[str, Any]], safe_guarantee["required_regressions"])
        if any(not result["exact"] for result in required.values()):
            raise AssertionError(
                f"boundary-safe {target} did not emit exact required regression morphemes"
            )
        if safe_guarantee["exact_segment_types"] != len(guarantee_rows):
            raise AssertionError(
                f"boundary-safe {target} did not emit exact title-case regression morphemes"
            )
        targets[str(target)] = {
            "plain_core_matches_existing_control": True,
            "paper_morphbpe": morph_metrics,
            "boundary_safe_all_accepted": safe_metrics,
            "boundary_safe_external_relation_evaluation": safe_external_audit,
            "boundary_safe_required_regression_guarantee": safe_guarantee,
        }

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "adjudication_manifest_fingerprint": adjudication.get("manifest_fingerprint"),
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "segmentation_manifest_fingerprint": segmentation_manifest.get("manifest_fingerprint"),
        "independent_evaluation_gold": False,
        "selection_performed": False,
        "targets": targets,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(RUNTIME_REPORT_PATH, report)
    _write_experiment_summary(report)
    return cast(dict[str, Any], report)


def _write_experiment_summary(report: dict[str, Any]) -> None:
    adjudication = _object(read_json(ADJUDICATION_MANIFEST_PATH), "adjudication manifest")
    prepared = _object(read_json(PREPARED_MANIFEST_PATH), "prepared manifest")
    targets = _object(report.get("targets"), "runtime targets")
    lines = [
        "# Source-adjudicated v2 experiment",
        "",
        "Status: trained and validated provisional local-test candidates; no model selected.",
        "",
        f"- Accepted root keys: **{adjudication['accepted_root_keys']:,}**.",
        f"- Explicitly supported derived types: **{adjudication['accepted_derived_types']:,}**.",
        f"- New training-boundary types versus v1: **{prepared['new_boundary_types']:,}**.",
        "- Plain, paper-runtime MorphBPE, and boundary-safe candidates: 6,080 / 8,192 / 16,384.",
        "- Runtime is lexicon-free standard BPE for every reported tokenizer.",
        "- These are silver training/audit data, not held-out morphology gold.",
        "",
        "## Runtime boundary results",
        "",
        (
            "| Vocab | Paper MorphBPE missed accepted | Boundary-safe missed guaranteed "
            "regressions | `sinulat` | `kabukasan` |"
        ),
        "|---:|---:|---:|---|---|",
    ]
    for target, raw in sorted(targets.items(), key=lambda item: int(item[0])):
        row = _object(raw, f"target {target}")
        paper = _object(row["paper_morphbpe"], "paper metrics")
        safe = _object(row["boundary_safe_required_regression_guarantee"], "safe metrics")
        required = _object(safe["required_regressions"], "required regressions")
        sinulat = " + ".join(cast(list[str], _object(required["sinulat"], "sinulat")["pieces"]))
        kabukasan = " + ".join(
            cast(list[str], _object(required["kabukasan"], "kabukasan")["pieces"])
        )
        lines.append(
            f"| {int(target):,} | {paper['missed_boundary_types']:,} | "
            f"{safe['missed_boundary_types']:,} | `{sinulat}` | `{kabukasan}` |"
        )
    lines.extend(
        [
            "",
            "Keep the original `prop` condition as the paper-replication baseline.",
            "Use `v2prop` as the source-enriched condition with paper-aligned runtime.",
            "Report `v2prop2` separately as a boundary-safe extension/ablation.",
            "The hard exact guarantee covers only lowercase/title-case `sinulat` and "
            "`kabukasan`; all 1,197 source-supported derivations remain a measured "
            "evaluation list.",
            "Vocabulary size remains a downstream validation choice, not a morphology truth claim.",
            "",
        ]
    )
    EXPERIMENT_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run_after_adjudication() -> dict[str, Any]:
    before = _snapshot_preserved()
    prepared = prepare()
    training = train()
    runtime = validate()
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("existing artifacts changed during the v2 run")
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "prepared_manifest_fingerprint": prepared.get("manifest_fingerprint"),
        "training_report_fingerprint": training.get("report_fingerprint"),
        "runtime_report_fingerprint": runtime.get("report_fingerprint"),
        "existing_artifacts_unchanged": True,
        "selection_performed": False,
        "independent_evaluation_gold": False,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(EXPERIMENT_REPORT_PATH, report)
    return cast(dict[str, Any], report)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "stage",
        choices=("adjudicate", "prepare", "train", "validate", "run-after-adjudication"),
    )
    parser.add_argument("--forman-pdf", type=Path)
    args = parser.parse_args()
    if args.stage == "adjudicate":
        if args.forman_pdf is None:
            parser.error("adjudicate requires --forman-pdf")
        result = adjudicate(cast(Path, args.forman_pdf))
    elif args.stage == "prepare":
        result = prepare()
    elif args.stage == "train":
        result = train()
    elif args.stage == "validate":
        result = validate()
    else:
        result = run_after_adjudication()
    concise_keys = (
        "manifest_fingerprint",
        "report_fingerprint",
        "accepted_root_keys",
        "accepted_derived_types",
        "accepted_derived_occurrences",
        "new_boundary_types",
        "new_boundary_occurrences",
        "existing_artifacts_unchanged",
    )
    concise = {"stage": args.stage}
    concise.update({key: result[key] for key in concise_keys if key in result})
    print(stable_compact_json(concise))


if __name__ == "__main__":
    main()
