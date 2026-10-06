from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, cast

from pypdf import PdfReader

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from kapampangan_morphbpe.constants import (  # noqa: E402
    CLITICS,
    DATASET_FINGERPRINT,
    INFIXES,
    PANG_VARIANTS,
    PREFIXES,
    SUFFIXES,
)
from kapampangan_morphbpe.morphology import MorphologicalSegmenter  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.serialization import (  # noqa: E402
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)

SOURCE_STREAM_PATH = (
    REPOSITORY_ROOT / "experiments/source_adjudicated_v1/runs/prepared/training-stream.jsonl"
)
SOURCE_STREAM_MANIFEST_PATH = SOURCE_STREAM_PATH.with_name("training-stream-manifest.json")
SOURCE_LEXICON_PATH = (
    REPOSITORY_ROOT / "experiments/source_adjudicated_v1/resources/training-lexicon.json"
)
SOURCE_LEXICON_MANIFEST_PATH = SOURCE_LEXICON_PATH.with_name("training-lexicon-manifest.json")
CANONICAL_LEXICON_PATH = REPOSITORY_ROOT / "resources/training-lexicon.json"
CANONICAL_LEXICON_MANIFEST_PATH = CANONICAL_LEXICON_PATH.with_name("training-lexicon-manifest.json")
SOURCE_REGISTRY_PATH = EXPERIMENT_ROOT / "source-registry.json"
DEFAULT_REPORTS_DIR = EXPERIMENT_ROOT / "reports"
SOURCE_INDEX_DIR = EXPERIMENT_ROOT / "runs/source-indexes"

EXPECTED_WORD_TYPES = 143_529
EXPECTED_STREAM_SHA256 = "fa1a59212353f288fe90ca205ef16a657237d89ddccd79c891987d4d91719336"
RICHARDS_IDS = {"ocr-010", "ocr-011", "ocr-012"}
ROOT_EVIDENCE_ROLES = {"explicit_root", "root_or_stem_headword"}
ACCEPTED_STATUSES = {"accepted", "protected_compound", "protected_root"}
STRESS_MARKS = {"\u0300", "\u0301", "\u0302", "\u0304"}
STRESS_PUNCTUATION = {"'", "\u2019", "`", "\u00b4", "\u02c8", "\u02cc", ":", "\ufffd"}

PRESERVED_PATHS = {
    "canonical_lexicon": CANONICAL_LEXICON_PATH,
    "canonical_lexicon_manifest": CANONICAL_LEXICON_MANIFEST_PATH,
    "canonical_selected_artifact": REPOSITORY_ROOT / "artifacts/selected-tokenizer",
    "source_lexicon": SOURCE_LEXICON_PATH,
    "source_lexicon_manifest": SOURCE_LEXICON_MANIFEST_PATH,
    "source_selected_artifact": REPOSITORY_ROOT
    / "experiments/source_adjudicated_v1/artifacts/selected-tokenizer",
}


@dataclass(frozen=True, slots=True)
class SourceForm:
    source_id: str
    raw_form: str
    role: str
    tier: str
    location: str
    source_record_id: str


@dataclass(frozen=True, slots=True)
class EvidenceHit:
    source_id: str
    raw_form: str
    role: str
    tier: str
    location: str
    source_record_id: str
    match_mode: str


@dataclass(frozen=True, slots=True)
class MechanicalCandidate:
    analysis_kind: str
    rule_id: str
    root_surface: str
    segments: tuple[str, ...]
    boundaries: tuple[int, ...]


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return cast(dict[str, Any], value)


def _ordered(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(values, key=lambda value: (-len(value), value)))


def _rule_fragment(value: str) -> str:
    return value.upper().replace("-", "_")


def _remove_vowel_stress(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    output: list[str] = []
    base = ""
    for character in decomposed:
        if unicodedata.combining(character):
            if character in STRESS_MARKS and base.casefold() in "aeiou":
                continue
            output.append(character)
            continue
        base = character
        if character not in STRESS_PUNCTUATION:
            output.append(character)
    return unicodedata.normalize("NFC", "".join(output))


def lexical_key(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = _remove_vowel_stress(normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    normalized = normalized.strip('-\u2013\u2014/.,;()[]{}"')
    return comparison_key(normalized)


def normalization_aliases(text: str) -> dict[str, str]:
    key = lexical_key(text)
    if not key:
        return {}
    aliases = {key: "normalized_exact"}
    if key.startswith("q") or key.endswith("q"):
        relaxed = key.strip("q")
        if relaxed:
            aliases.setdefault(relaxed, "edge_q_glottal_relaxed")
    if "-" in key:
        aliases.setdefault(key.replace("-", ""), "hyphen_relaxed")
    return aliases


class EvidenceIndex:
    def __init__(self) -> None:
        self._hits: dict[str, dict[tuple[str, ...], EvidenceHit]] = {}

    def add(self, form: SourceForm) -> None:
        for key, match_mode in normalization_aliases(form.raw_form).items():
            hit = EvidenceHit(**asdict(form), match_mode=match_mode)
            identity = (
                hit.source_id,
                hit.role,
                hit.location,
                hit.source_record_id,
                hit.raw_form,
                hit.match_mode,
            )
            self._hits.setdefault(key, {})[identity] = hit

    def add_alias(self, key: str, form: SourceForm, match_mode: str) -> None:
        normalized = lexical_key(key)
        if not normalized:
            return
        hit = EvidenceHit(**asdict(form), match_mode=match_mode)
        identity = (
            hit.source_id,
            hit.role,
            hit.location,
            hit.source_record_id,
            hit.raw_form,
            hit.match_mode,
        )
        self._hits.setdefault(normalized, {})[identity] = hit

    def lookup(self, form: str) -> tuple[EvidenceHit, ...]:
        hits = self._hits.get(lexical_key(form), {})
        return tuple(
            sorted(
                hits.values(),
                key=lambda hit: (
                    hit.tier,
                    hit.source_id,
                    hit.role,
                    hit.match_mode,
                    hit.location,
                    hit.raw_form,
                ),
            )
        )

    @property
    def unique_keys(self) -> int:
        return len(self._hits)


def _headword_parts(value: str) -> tuple[str, ...]:
    parts = re.split(r"\s*/\s*", value.strip())
    output: list[str] = []
    for part in parts:
        cleaned = part.strip().strip(",.;")
        if cleaned and any(character.isalpha() for character in cleaned):
            output.append(cleaned)
    return tuple(output)


def _forman_role(definition: str) -> str:
    lowered = definition.casefold().strip()
    if not lowered:
        return "unclassified_headword"
    if re.search(r"(?:^|[.;])\s*(?:see|c\.f\.)\s", lowered):
        return "cross_reference_headword"
    class_match = re.match(r"\(([^)]+)\)", lowered)
    if class_match is not None:
        word_class = class_match.group(1)
        unaffixable_markers = (
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
        if any(marker in word_class for marker in unaffixable_markers):
            return "unaffixable_headword"
    return "root_or_stem_headword"


def extract_forman(path: Path) -> list[SourceForm]:
    reader = PdfReader(path)
    forms: list[SourceForm] = []

    def append_entry(page_number: int, ordinal: int, raw_headword: str, definition: str) -> None:
        if len(raw_headword) > 60 or not any(char.isalpha() for char in raw_headword):
            return
        if raw_headword.isupper() and len(raw_headword) <= 4:
            return
        role = _forman_role(definition)
        for part_number, headword in enumerate(_headword_parts(raw_headword), 1):
            forms.append(
                SourceForm(
                    source_id="forman1971",
                    raw_form=headword,
                    role=role,
                    tier="A",
                    location=f"PDF page {page_number}",
                    source_record_id=(
                        f"forman1971-p{page_number:03d}-{ordinal:03d}-{part_number:02d}"
                    ),
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
    return forms


def extract_bergano(path: Path) -> list[SourceForm]:
    reader = PdfReader(path)
    forms: list[SourceForm] = []
    headword_pattern = re.compile(r"^([^\W\d_][^.,]{0,45})[.,]\s*(.*)$", re.UNICODE)
    last_page_index = min(459, len(reader.pages))
    for page_index in range(27, last_page_index):
        text = reader.pages[page_index].extract_text() or ""
        ordinal = 0
        for line in text.splitlines():
            match = headword_pattern.match(line.strip())
            if match is None:
                continue
            raw_headword = match.group(1).strip()
            if raw_headword != raw_headword.upper():
                continue
            if len(raw_headword.split()) > 3 or not any(char.isalpha() for char in raw_headword):
                continue
            role = (
                "explicit_root"
                if re.search(r"\broot\b", match.group(2)[:120], flags=re.IGNORECASE)
                else "historical_headword"
            )
            for headword in _headword_parts(raw_headword):
                ordinal += 1
                forms.append(
                    SourceForm(
                        source_id="bergano1732_samson_translation",
                        raw_form=headword,
                        role=role,
                        tier="B",
                        location=f"PDF page {page_index + 1}",
                        source_record_id=f"bergano-p{page_index + 1:03d}-{ordinal:03d}",
                    )
                )
    return forms


def _samson_column_headword(column: str) -> str | None:
    if not column or column[0].isspace():
        return None
    match = re.match(r"^([^\s,.;:()]+)(?:,|\.)\s+\S", column)
    if match is None:
        return None
    headword = match.group(1).strip()
    if len(headword) > 60 or not any(char.isalpha() for char in headword):
        return None
    return headword


def extract_samson(path: Path) -> list[SourceForm]:
    reader = PdfReader(path)
    forms: list[SourceForm] = []
    last_page_index = min(833, len(reader.pages))
    for page_index in range(10, last_page_index):
        text = reader.pages[page_index].extract_text(extraction_mode="layout") or ""
        ordinal = 0
        for line in text.splitlines():
            columns = (line[:61], line[61:])
            for column in columns:
                headword = _samson_column_headword(column)
                if headword is None:
                    continue
                ordinal += 1
                forms.append(
                    SourceForm(
                        source_id="samson2011",
                        raw_form=headword,
                        role="modern_headword",
                        tier="B",
                        location=f"PDF page {page_index + 1}",
                        source_record_id=f"samson2011-p{page_index + 1:03d}-{ordinal:03d}",
                    )
                )
    return forms


def extract_kaikki(path: Path) -> list[SourceForm]:
    forms: list[SourceForm] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = _object(json.loads(line), f"Kaikki line {line_number}")
            word = row.get("word")
            if not isinstance(word, str) or not word.strip():
                continue
            forms.append(
                SourceForm(
                    source_id="kaikki_enwiktionary",
                    raw_form=word,
                    role="community_headword",
                    tier="C",
                    location=f"JSONL line {line_number}",
                    source_record_id=f"kaikki-{line_number:06d}",
                )
            )
    return forms


def extract_acd(forms_path: Path, languages_path: Path) -> list[SourceForm]:
    language_ids: set[str] = set()
    with languages_path.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            name = (row.get("Name") or "").casefold()
            iso = (row.get("ISO639P3code") or "").casefold()
            if name == "kapampangan" or iso == "pam":
                language_id = row.get("ID")
                if language_id:
                    language_ids.add(language_id)
    if not language_ids:
        raise ValueError("ACD languages.csv has no Kapampangan/pam language row")

    forms: list[SourceForm] = []
    with forms_path.open("r", encoding="utf-8-sig", newline="") as stream:
        for line_number, row in enumerate(csv.DictReader(stream), 2):
            if row.get("Language_ID") not in language_ids:
                continue
            value = row.get("Form") or row.get("Value")
            if not value:
                continue
            forms.append(
                SourceForm(
                    source_id="acd_v1_2",
                    raw_form=value,
                    role="comparative_lexical_form",
                    tier="B",
                    location=f"forms.csv line {line_number}",
                    source_record_id=row.get("ID") or f"acd-{line_number}",
                )
            )
    return forms


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.casefold() == "tr":
            self._row = []
        elif tag.casefold() in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.casefold()
        if lowered in {"td", "th"} and self._row is not None and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif lowered == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None


def extract_ucla(directory: Path) -> list[SourceForm]:
    forms: list[SourceForm] = []
    for path in sorted(directory.glob("ucla-pam-*.html")):
        parser = _TableParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        orthography_index: int | None = None
        data_start = 0
        for row_index, row in enumerate(parser.rows):
            for column_index, value in enumerate(row):
                if "orthography" in value.casefold():
                    orthography_index = column_index
                    data_start = row_index + 1
                    break
            if orthography_index is not None:
                break
        if orthography_index is None:
            continue
        for row_index, row in enumerate(parser.rows[data_start:], data_start + 1):
            if orthography_index >= len(row):
                continue
            word = row[orthography_index].strip()
            if not word or not any(char.isalpha() for char in word):
                continue
            forms.append(
                SourceForm(
                    source_id="ucla_phonetics_archive",
                    raw_form=word,
                    role="speaker_wordlist_form",
                    tier="B",
                    location=f"{path.name} table row {row_index}",
                    source_record_id=f"{path.stem}-{row_index:04d}",
                )
            )
    return forms


def _write_source_index(source_id: str, forms: list[SourceForm]) -> Path:
    path = SOURCE_INDEX_DIR / f"{source_id}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for form in sorted(
            forms,
            key=lambda row: (lexical_key(row.raw_form).encode("utf-8"), row.source_record_id),
        ):
            stream.write(stable_compact_json(asdict(form)) + "\n")
    return path


def _mark_boundaries(segments: tuple[str, ...]) -> tuple[int, ...]:
    boundaries: list[int] = []
    position = 0
    for segment in segments[:-1]:
        position += len(segment)
        boundaries.append(position)
    return tuple(boundaries)


def mechanical_candidates(token: str) -> tuple[MechanicalCandidate, ...]:
    lower = comparison_key(token)
    candidates: list[MechanicalCandidate] = [
        MechanicalCandidate("direct_root", "DIRECT_ROOT", token, (token,), ())
    ]

    pairs = [
        ("ka", "an", "KA"),
        ("pa", "an", "PA"),
        ("pang", "an", "PANG"),
        *((variant, "an", f"PANG_{_rule_fragment(variant)}") for variant in PANG_VARIANTS),
    ]
    pairs.sort(key=lambda item: (-len(item[0]), item[0], item[2]))
    for prefix, suffix, name in pairs:
        if (
            lower.startswith(prefix)
            and lower.endswith(suffix)
            and len(token) > len(prefix) + len(suffix)
        ):
            root = token[len(prefix) : len(token) - len(suffix)]
            segments = (token[: len(prefix)], root, token[len(token) - len(suffix) :])
            candidates.append(
                MechanicalCandidate(
                    "circumfix",
                    f"CIRCUMFIX_{name}_AN",
                    root,
                    segments,
                    _mark_boundaries(segments),
                )
            )

    for prefix in _ordered(PREFIXES):
        if lower.startswith(prefix) and len(token) > len(prefix):
            root = token[len(prefix) :]
            segments = (token[: len(prefix)], root)
            candidates.append(
                MechanicalCandidate(
                    "prefix",
                    f"PREFIX_{_rule_fragment(prefix)}",
                    root,
                    segments,
                    _mark_boundaries(segments),
                )
            )

    for infix in _ordered(INFIXES):
        position = 1
        if len(token) > position + len(infix) and lower[position : position + len(infix)] == infix:
            root = token[:position] + token[position + len(infix) :]
            segments = (
                token[:position],
                token[position : position + len(infix)],
                token[position + len(infix) :],
            )
            candidates.append(
                MechanicalCandidate(
                    "infix",
                    f"INFIX_{_rule_fragment(infix)}",
                    root,
                    segments,
                    _mark_boundaries(segments),
                )
            )

    for suffix in _ordered(SUFFIXES):
        if lower.endswith(suffix) and len(token) > len(suffix):
            root = token[: -len(suffix)]
            segments = (root, token[-len(suffix) :])
            candidates.append(
                MechanicalCandidate(
                    "suffix",
                    f"SUFFIX_{_rule_fragment(suffix)}",
                    root,
                    segments,
                    _mark_boundaries(segments),
                )
            )

    for clitic in _ordered(CLITICS):
        if lower.endswith(clitic) and len(token) > len(clitic):
            root = token[: -len(clitic)]
            segments = (root, token[-len(clitic) :])
            candidates.append(
                MechanicalCandidate(
                    "clitic",
                    f"CLITIC_{_rule_fragment(clitic)}",
                    root,
                    segments,
                    _mark_boundaries(segments),
                )
            )

    distinct = {
        (row.analysis_kind, row.rule_id, row.root_surface, row.segments, row.boundaries): row
        for row in candidates
    }
    return tuple(
        sorted(
            distinct.values(),
            key=lambda row: (
                row.analysis_kind,
                row.rule_id,
                lexical_key(row.root_surface),
                row.segments,
            ),
        )
    )


def _quality_flags(token: str) -> tuple[str, ...]:
    flags: list[str] = []
    if "�" in token or "\ufffd" in token:
        flags.append("replacement_character")
    if any(character.isdigit() for character in token):
        flags.append("contains_digit")
    if "http" in token.casefold() or "www" in token.casefold() or "@" in token:
        flags.append("url_or_email_like")
    if len(token) > 40:
        flags.append("length_gt_40")
    if any(unicodedata.category(character).startswith("C") for character in token):
        flags.append("contains_control")
    letter_names = [unicodedata.name(character, "") for character in token if character.isalpha()]
    if any(name and "LATIN" not in name for name in letter_names):
        flags.append("contains_non_latin_letter")
    return tuple(flags)


def _hit_label(hit: EvidenceHit) -> str:
    return ":".join(
        (
            hit.source_id,
            hit.role,
            hit.match_mode,
            hit.source_record_id,
        )
    )


def _compact_hits(hits: tuple[EvidenceHit, ...], limit: int = 12) -> str:
    labels = [_hit_label(hit) for hit in hits[:limit]]
    if len(hits) > limit:
        labels.append(f"...+{len(hits) - limit}")
    return " | ".join(labels)


def _candidate_evidence(hits: tuple[EvidenceHit, ...]) -> tuple[str, str, bool]:
    root_hits = tuple(hit for hit in hits if hit.role in ROOT_EVIDENCE_ROLES)
    if root_hits:
        exact = any(hit.match_mode == "normalized_exact" for hit in root_hits)
        return (
            "source_supported_root_exact" if exact else "source_supported_root_variant",
            min(hit.tier for hit in root_hits),
            True,
        )
    if hits:
        return "lexically_attested_only", min(hit.tier for hit in hits), False
    return "no_source_match", "", False


def _current_root(analysis_kind: str | None, segments: tuple[str, ...]) -> str:
    if not segments:
        return ""
    if analysis_kind == "circumfix" and len(segments) == 3:
        return segments[1]
    if analysis_kind == "infix" and len(segments) == 3:
        return segments[0] + segments[2]
    if analysis_kind in {"prefix", "suffix", "clitic"} and len(segments) == 2:
        return segments[1] if analysis_kind == "prefix" else segments[0]
    return segments[0]


def _candidate_is_current(
    candidate: MechanicalCandidate,
    status: str,
    rule_id: str | None,
    current_root: str,
) -> bool:
    if status in {"protected_compound", "protected_root"}:
        return candidate.analysis_kind == "direct_root"
    return candidate.rule_id == rule_id and lexical_key(candidate.root_surface) == lexical_key(
        current_root
    )


def _snapshot_preserved() -> dict[str, dict[str, str]]:
    snapshot: dict[str, dict[str, str]] = {}
    for name, path in PRESERVED_PATHS.items():
        if path.is_file():
            snapshot[name] = {path.name: sha256_file(path)}
            continue
        if not path.is_dir():
            raise FileNotFoundError(path)
        snapshot[name] = {
            child.relative_to(path).as_posix(): sha256_file(child)
            for child in sorted(path.rglob("*"))
            if child.is_file()
        }
    return snapshot


def _verify_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    prepared = _object(read_json(SOURCE_STREAM_MANIFEST_PATH), "prepared manifest")
    lexicon = _object(read_json(SOURCE_LEXICON_MANIFEST_PATH), "source lexicon manifest")
    canonical = _object(read_json(CANONICAL_LEXICON_MANIFEST_PATH), "canonical lexicon manifest")
    if prepared.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("prepared dataset fingerprint changed")
    actual_stream_hash = sha256_file(SOURCE_STREAM_PATH)
    if actual_stream_hash != EXPECTED_STREAM_SHA256:
        raise ValueError(f"preserved stream hash changed: {actual_stream_hash}")
    if prepared.get("stream_sha256") != actual_stream_hash:
        raise ValueError("prepared stream manifest hash mismatch")
    if sha256_file(SOURCE_LEXICON_PATH) != lexicon.get("lexicon_file_sha256"):
        raise ValueError("source lexicon hash mismatch")
    if sha256_file(CANONICAL_LEXICON_PATH) != canonical.get("lexicon_file_sha256"):
        raise ValueError("canonical lexicon hash mismatch")
    held = set(cast(list[str], lexicon.get("richards_candidate_ids_held")))
    if held != RICHARDS_IDS:
        raise ValueError("Richards held-source policy changed")
    return prepared, lexicon


def _load_sources(args: argparse.Namespace) -> tuple[EvidenceIndex, dict[str, dict[str, Any]]]:
    loaders: list[tuple[str, list[SourceForm]]] = [
        ("forman1971", extract_forman(args.forman_pdf)),
        ("bergano1732_samson_translation", extract_bergano(args.bergano_pdf)),
        ("samson2011", extract_samson(args.samson_pdf)),
        ("kaikki_enwiktionary", extract_kaikki(args.kaikki_jsonl)),
        ("acd_v1_2", extract_acd(args.acd_forms, args.acd_languages)),
        ("ucla_phonetics_archive", extract_ucla(args.ucla_html_dir)),
    ]
    index = EvidenceIndex()
    summary: dict[str, dict[str, Any]] = {}
    for source_id, forms in loaders:
        for form in forms:
            index.add(form)
            if source_id == "acd_v1_2" and ("<" in form.raw_form or "-" in form.raw_form):
                surface = re.sub(r"[<>\-\s]", "", form.raw_form)
                index.add_alias(surface, form, "acd_notation_collapsed")
        index_path = _write_source_index(source_id, forms)
        summary[source_id] = {
            "extracted_forms": len(forms),
            "index_path": index_path.relative_to(EXPERIMENT_ROOT).as_posix(),
            "index_sha256": sha256_file(index_path),
            "role_counts": dict(sorted(Counter(row.role for row in forms).items())),
            "unique_normalized_forms": len({lexical_key(row.raw_form) for row in forms}),
        }
    summary["all_sources"] = {"unique_normalized_alias_keys": index.unique_keys}
    return index, summary


WORD_FIELDS = (
    "surface",
    "comparison_key",
    "frequency",
    "current_status",
    "current_kind",
    "current_rule_id",
    "current_segments",
    "current_boundaries",
    "current_root",
    "quality_flags",
    "whole_form_sources",
    "candidate_count",
    "source_supported_candidate_count",
    "lexically_attested_candidate_count",
    "best_candidates",
    "decision",
    "proposed_action",
)

CANDIDATE_FIELDS = (
    "surface",
    "frequency",
    "analysis_kind",
    "rule_id",
    "root_hypothesis",
    "segments",
    "boundaries",
    "current_selected",
    "evidence_status",
    "best_evidence_tier",
    "root_evidence",
    "evidence_sources",
)


def reconcile(
    index: EvidenceIndex,
    reports_dir: Path,
    expected_word_types: int,
) -> dict[str, Any]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    segmenter = MorphologicalSegmenter.from_path(SOURCE_LEXICON_PATH)
    word_sequences = [
        sequence for sequence in load_prepared_stream(SOURCE_STREAM_PATH) if sequence.kind == "word"
    ]
    word_sequences.sort(key=lambda row: row.surface.encode("utf-8"))
    if len(word_sequences) != expected_word_types:
        raise ValueError(f"expected {expected_word_types} word types, found {len(word_sequences)}")

    word_path = reports_dir / "word-evidence.csv"
    candidate_path = reports_dir / "candidate-evidence.csv"
    decision_types: Counter[str] = Counter()
    decision_occurrences: Counter[str] = Counter()
    current_status_types: Counter[str] = Counter()
    current_status_occurrences: Counter[str] = Counter()
    source_match_types: Counter[str] = Counter()
    candidate_evidence_counts: Counter[str] = Counter()
    candidate_count = 0
    new_examples: list[tuple[int, str, str, str]] = []
    conflict_examples: list[tuple[int, str, str]] = []
    diagnostic_rows: dict[str, dict[str, str]] = {}

    with (
        word_path.open("w", encoding="utf-8", newline="") as word_stream,
        candidate_path.open("w", encoding="utf-8", newline="") as candidate_stream,
    ):
        word_writer = csv.DictWriter(word_stream, fieldnames=WORD_FIELDS, lineterminator="\n")
        candidate_writer = csv.DictWriter(
            candidate_stream, fieldnames=CANDIDATE_FIELDS, lineterminator="\n"
        )
        word_writer.writeheader()
        candidate_writer.writeheader()

        for sequence in word_sequences:
            token = sequence.surface
            analysis = segmenter.segment(token)
            if analysis.protected_boundaries != sequence.protected_boundaries:
                raise AssertionError(f"prepared segmentation changed for {token!r}")
            current_root = _current_root(analysis.kind, analysis.segments)
            whole_hits = index.lookup(token)
            candidates = mechanical_candidates(token)
            supported: list[MechanicalCandidate] = []
            lexical: list[MechanicalCandidate] = []
            best_labels: list[str] = []

            for candidate in candidates:
                hits = index.lookup(candidate.root_surface)
                evidence_status, best_tier, root_evidence = _candidate_evidence(hits)
                if evidence_status == "source_supported_root_exact":
                    supported.append(candidate)
                    best_labels.append(
                        f"{candidate.rule_id}:{candidate.root_surface}:{evidence_status}"
                    )
                elif hits:
                    lexical.append(candidate)
                candidate_writer.writerow(
                    {
                        "surface": token,
                        "frequency": sequence.frequency,
                        "analysis_kind": candidate.analysis_kind,
                        "rule_id": candidate.rule_id,
                        "root_hypothesis": candidate.root_surface,
                        "segments": " + ".join(candidate.segments),
                        "boundaries": "|".join(map(str, candidate.boundaries)),
                        "current_selected": str(
                            _candidate_is_current(
                                candidate,
                                analysis.status,
                                analysis.rule_id,
                                current_root,
                            )
                        ).lower(),
                        "evidence_status": evidence_status,
                        "best_evidence_tier": best_tier,
                        "root_evidence": str(root_evidence).lower(),
                        "evidence_sources": _compact_hits(hits),
                    }
                )
                candidate_count += 1
                candidate_evidence_counts[evidence_status] += 1

            flags = _quality_flags(token)
            if analysis.status in ACCEPTED_STATUSES:
                decision = "already_analyzed"
                action = "retain_for_adjudication"
            elif analysis.status == "ambiguous":
                decision = "current_rule_conflict"
                action = "human_adjudication_required"
            elif len(supported) == 1:
                decision = "new_exact_root_matched_hypothesis"
                action = (
                    "review_add_provisional_root"
                    if supported[0].analysis_kind == "direct_root"
                    else "review_root_and_segmentation"
                )
                new_examples.append(
                    (
                        sequence.frequency,
                        token,
                        supported[0].rule_id,
                        supported[0].root_surface,
                    )
                )
            elif len(supported) > 1:
                decision = "conflicting_exact_root_matched_hypotheses"
                action = "human_adjudication_required"
                conflict_examples.append(
                    (
                        sequence.frequency,
                        token,
                        " | ".join(
                            f"{candidate.rule_id}:{candidate.root_surface}"
                            for candidate in supported
                        ),
                    )
                )
            elif lexical or whole_hits:
                decision = "lexically_attested_unresolved"
                action = "do_not_promote_without_root_evidence"
            elif flags:
                decision = "probable_noise_unresolved"
                action = "review_or_filter_corpus_item"
            else:
                decision = "unresolved_no_source_match"
                action = "leave_unchanged"

            source_ids = {hit.source_id for hit in whole_hits}
            for source_id in source_ids:
                source_match_types[source_id] += 1
            current_status_types[analysis.status] += 1
            current_status_occurrences[analysis.status] += sequence.frequency
            decision_types[decision] += 1
            decision_occurrences[decision] += sequence.frequency
            word_row = {
                "surface": token,
                "comparison_key": comparison_key(token),
                "frequency": sequence.frequency,
                "current_status": analysis.status,
                "current_kind": analysis.kind or "",
                "current_rule_id": analysis.rule_id or "",
                "current_segments": " + ".join(analysis.segments),
                "current_boundaries": "|".join(map(str, analysis.protected_boundaries)),
                "current_root": current_root,
                "quality_flags": "|".join(flags),
                "whole_form_sources": _compact_hits(whole_hits),
                "candidate_count": len(candidates),
                "source_supported_candidate_count": len(supported),
                "lexically_attested_candidate_count": len(lexical),
                "best_candidates": " | ".join(best_labels),
                "decision": decision,
                "proposed_action": action,
            }
            word_writer.writerow(word_row)
            if comparison_key(token) in {"sinulat", "kabukasan"}:
                diagnostic_rows[comparison_key(token)] = {
                    key: str(value) for key, value in word_row.items()
                }

    summary: dict[str, Any] = {
        "candidate_evidence_counts": dict(sorted(candidate_evidence_counts.items())),
        "candidate_rows": candidate_count,
        "current_status_occurrences": dict(sorted(current_status_occurrences.items())),
        "current_status_types": dict(sorted(current_status_types.items())),
        "decision_occurrences": dict(sorted(decision_occurrences.items())),
        "decision_types": dict(sorted(decision_types.items())),
        "diagnostic_rows": diagnostic_rows,
        "source_whole_form_match_types": dict(sorted(source_match_types.items())),
        "top_conflicts": [
            {"frequency": freq, "surface": surface, "candidates": candidates}
            for freq, surface, candidates in sorted(conflict_examples, reverse=True)[:20]
        ],
        "top_new_exact_root_matched": [
            {"frequency": freq, "surface": surface, "rule_id": rule, "root": root}
            for freq, surface, rule, root in sorted(new_examples, reverse=True)[:30]
        ],
        "word_occurrences": sum(sequence.frequency for sequence in word_sequences),
        "word_types": len(word_sequences),
    }
    return summary


def _markdown_table(values: dict[str, int]) -> str:
    rows = ["| Status | Types |", "|---|---:|"]
    rows.extend(f"| `{key}` | {value:,} |" for key, value in sorted(values.items()))
    return "\n".join(rows)


def _write_summary(
    path: Path,
    audit: dict[str, Any],
    sources: dict[str, dict[str, Any]],
) -> None:
    new_examples = cast(list[dict[str, Any]], audit["top_new_exact_root_matched"])
    conflicts = cast(list[dict[str, Any]], audit["top_conflicts"])
    diagnostics = cast(dict[str, dict[str, str]], audit["diagnostic_rows"])
    lines = [
        "# Internet Root Reconciliation V1",
        "",
        "Status: evidence pass complete; no lexicon mutation or retraining performed.",
        "",
        "## Coverage",
        "",
        f"- Distinct dataset word pretokens: **{cast(int, audit['word_types']):,}**.",
        f"- Word-token occurrences represented: **{cast(int, audit['word_occurrences']):,}**.",
        f"- Mechanical candidate rows: **{cast(int, audit['candidate_rows']):,}**.",
        f"- Dataset fingerprint: `{DATASET_FINGERPRINT}`.",
        f"- Preserved stream SHA-256: `{EXPECTED_STREAM_SHA256}`.",
        "",
        "## Word decisions",
        "",
        _markdown_table(cast(dict[str, int], audit["decision_types"])),
        "",
        "## Current segmenter statuses",
        "",
        _markdown_table(cast(dict[str, int], audit["current_status_types"])),
        "",
        "## Source indexes",
        "",
        "| Source | Extracted forms | Unique normalized forms |",
        "|---|---:|---:|",
    ]
    for source_id, source in sorted(sources.items()):
        if source_id == "all_sources":
            continue
        lines.append(
            f"| `{source_id}` | {cast(int, source['extracted_forms']):,} | "
            f"{cast(int, source['unique_normalized_forms']):,} |"
        )
    registry = _object(read_json(SOURCE_REGISTRY_PATH), "source registry")
    registry_sources = cast(list[dict[str, Any]], registry.get("sources"))
    forman_roles = cast(dict[str, int], sources["forman1971"]["role_counts"])
    lines.extend(
        [
            "",
            "## Source links",
            "",
            *[
                f"- [{source['title']}]({source['url']}) - tier `{source['tier']}`."
                for source in registry_sources
            ],
            "",
            "Forman role partition: "
            + ", ".join(f"`{role}` {count:,}" for role, count in sorted(forman_roles.items()))
            + ".",
            "",
            "Forman is the only broadly parsed source treated as root-oriented. "
            "Bergaño counts as root evidence only when an entry explicitly says `Root`. "
            "Samson, ACD, UCLA, and Kaikki matches establish lexical attestation, not "
            "productive-root status.",
            "",
            "## Highest-frequency new exact-root-matched hypotheses",
            "",
            "| Frequency | Word | Mechanical rule | Reconstructed root |",
            "|---:|---|---|---|",
        ]
    )
    for row in new_examples[:20]:
        lines.append(
            f"| {cast(int, row['frequency']):,} | `{row['surface']}` | "
            f"`{row['rule_id']}` | `{row['root']}` |"
        )
    lines.extend(
        [
            "",
            "## Highest-frequency conflicts",
            "",
            "| Frequency | Word | Supported hypotheses |",
            "|---:|---|---|",
        ]
    )
    for row in conflicts[:15]:
        lines.append(
            f"| {cast(int, row['frequency']):,} | `{row['surface']}` | `{row['candidates']}` |"
        )
    lines.extend(["", "## Diagnostics", ""])
    for word in ("sinulat", "kabukasan"):
        row = diagnostics.get(word)
        if row is None:
            lines.append(f"- `{word}` was not found as an exact dataset surface.")
            continue
        lines.append(
            f"- `{word}`: current `{row['current_status']}` / `{row['current_rule_id']}` -> "
            f"`{row['current_segments']}`; decision `{row['decision']}`; candidates "
            f"`{row['best_candidates'] or 'none'}`."
        )
    lines.extend(
        [
            "",
            "## Retraining gate",
            "",
            "1. Review every `new_exact_root_matched_hypothesis` and every conflict; "
            "a reconstructed root match does not prove that the proposed affix relationship "
            "is correct.",
            "2. Do not promote `lexically_attested_unresolved` rows as roots. That "
            "would protect derived words and hide valid affix boundaries.",
            "3. Freeze an adjudicated boundary list independently of the training "
            "corpus, then measure conflicts before training. The complete automatic "
            "list is not guaranteed to be globally consistent for context-free BPE merges.",
            "4. Retrain only in a new experiment folder and compare Plain BPE, "
            "paper-aligned MorphBPE, and the boundary-safe extension on held-out "
            "morphology plus downstream translation.",
            "",
            "## Limitations",
            "",
            "- Exact normalized matching does not solve productive allomorphy, nasal "
            "assimilation, reduplication, dialect variation, or global historical "
            "`c/k` conversion. No global `c -> k` rewrite was used.",
            "- ACD Kapampangan records can cite Forman, and Kaikki/Wiktionary can "
            "overlap the current lexicon; these are not always independent confirmations.",
            "- Obvious corruption is flagged, but unmatched text is not automatically "
            "labelled non-Kapampangan.",
            "- Richards evidence IDs `ocr-010` through `ocr-012` remained held and "
            "were not indexed.",
            "- The full source indexes and CSVs are local research outputs; "
            "publication/redistribution rights require a separate review.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def run(args: argparse.Namespace) -> dict[str, Any]:
    prepared_manifest, lexicon_manifest = _verify_inputs()
    before = _snapshot_preserved()
    index, source_summary = _load_sources(args)
    audit = reconcile(index, args.reports_dir, args.expected_word_types)
    after = _snapshot_preserved()
    if before != after:
        raise AssertionError("an operational lexicon or tokenizer artifact changed during audit")

    word_path = args.reports_dir / "word-evidence.csv"
    candidate_path = args.reports_dir / "candidate-evidence.csv"
    summary_path = args.reports_dir / "reconciliation-summary.md"
    manifest_path = args.reports_dir / "reconciliation-manifest.json"
    input_paths = {
        "acd_forms": args.acd_forms,
        "acd_languages": args.acd_languages,
        "bergano_pdf": args.bergano_pdf,
        "forman_pdf": args.forman_pdf,
        "kaikki_jsonl": args.kaikki_jsonl,
        "reconciliation_runner": Path(__file__).resolve(),
        "samson_pdf": args.samson_pdf,
        "source_registry": SOURCE_REGISTRY_PATH,
        "source_stream": SOURCE_STREAM_PATH,
    }
    for html_path in sorted(args.ucla_html_dir.glob("ucla-pam-*.html")):
        input_paths[f"ucla_{html_path.stem}"] = html_path
    body: dict[str, Any] = {
        "audit": audit,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "input_sha256": {name: sha256_file(path) for name, path in input_paths.items()},
        "operational_resources_preserved": True,
        "output_sha256": {
            "candidate_evidence_csv": sha256_file(candidate_path),
            "word_evidence_csv": sha256_file(word_path),
        },
        "prepared_manifest_fingerprint": prepared_manifest.get("manifest_fingerprint"),
        "richards_candidate_ids_held": sorted(RICHARDS_IDS),
        "source_lexicon_fingerprint": lexicon_manifest.get("lexicon_fingerprint"),
        "source_summary": source_summary,
        "training_lexicon_mutated": False,
        "tokenizer_artifacts_mutated": False,
        "tokenizers_retrained": False,
    }
    _write_summary(summary_path, audit, source_summary)
    body["output_sha256"]["summary_markdown"] = sha256_file(summary_path)
    manifest = {**body, "manifest_fingerprint": fingerprint(body)}
    write_json(manifest_path, manifest)
    return manifest


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconcile all preserved dataset words with root and lexical evidence."
    )
    parser.add_argument("--forman-pdf", type=Path, required=True)
    parser.add_argument("--bergano-pdf", type=Path, required=True)
    parser.add_argument("--samson-pdf", type=Path, required=True)
    parser.add_argument("--kaikki-jsonl", type=Path, required=True)
    parser.add_argument("--acd-forms", type=Path, required=True)
    parser.add_argument("--acd-languages", type=Path, required=True)
    parser.add_argument("--ucla-html-dir", type=Path, required=True)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument("--expected-word-types", type=int, default=EXPECTED_WORD_TYPES)
    args = parser.parse_args(argv)
    required_paths = (
        args.forman_pdf,
        args.bergano_pdf,
        args.samson_pdf,
        args.kaikki_jsonl,
        args.acd_forms,
        args.acd_languages,
        args.ucla_html_dir,
    )
    for path in required_paths:
        if not path.exists():
            parser.error(f"input path does not exist: {path}")
    return args


def main() -> None:
    manifest = run(parse_args())
    print(stable_compact_json(manifest))


if __name__ == "__main__":
    main()
