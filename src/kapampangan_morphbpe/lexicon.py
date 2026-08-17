from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .constants import (
    CIRCUMFIXES,
    CLITICS,
    DATASET_FINGERPRINT,
    INFIXES,
    PANG_VARIANTS,
    PREFIXES,
    ROOT_REFERENCE_TYPES,
    SCHEMA_VERSION,
    SUFFIXES,
)
from .dataset import read_id_text, read_references
from .models import ReferenceRecord
from .normalization import comparison_key, normalize_text
from .pretokenizer import pretokenize_normalized
from .serialization import fingerprint, read_json, sha256_file, write_json


@dataclass(frozen=True, slots=True)
class TrainingLexicon:
    roots: frozenset[str]
    compounds: frozenset[str]
    variants: frozenset[str]
    lexicon_fingerprint: str

    @property
    def valid_hosts(self) -> frozenset[str]:
        return self.roots | self.variants


def _reference_dict(record: ReferenceRecord) -> dict[str, str]:
    return {
        "id": record.identifier,
        "form": record.form,
        "type": record.kind,
        "description": record.description,
        "example": record.example,
        "source": record.source,
    }


def _is_operational_root(form: str) -> bool:
    if len(form) < 2 or normalize_text(form) != form:
        return False
    return all(
        unicodedata.category(character)[0] in {"L", "M"} or character in {"'", "\u2019"}
        for character in form
    )


def _is_one_word_pretoken(form: str) -> bool:
    tokens = pretokenize_normalized(form)
    return len(tokens) == 1 and tokens[0].kind == "word" and tokens[0].surface == form


def _training_word_frequencies(dataset_root: Path) -> Counter[str]:
    frequencies: Counter[str] = Counter()
    for record in read_id_text(dataset_root / "data/train.csv", role="train"):
        for token in pretokenize_normalized(record.text):
            if token.kind == "word":
                frequencies[comparison_key(token.surface)] += 1
    return frequencies


def build_lexicon(dataset_root: Path, output_dir: Path) -> dict[str, object]:
    dataset_root = dataset_root.resolve()
    morphology_path = dataset_root / "data/morphology-reference.csv"
    linguistic_path = dataset_root / "data/linguistic-evidence.csv"
    morphology = list(read_references(morphology_path))
    linguistic = list(read_references(linguistic_path))
    training_frequencies = _training_word_frequencies(dataset_root)

    root_sources: dict[str, list[ReferenceRecord]] = defaultdict(list)
    root_surfaces: dict[str, set[str]] = defaultdict(set)
    excluded_root_candidates = 0
    for record in morphology:
        form = normalize_text(record.form.strip())
        if record.kind not in ROOT_REFERENCE_TYPES:
            continue
        if not _is_operational_root(form):
            excluded_root_candidates += 1
            continue
        key = comparison_key(form)
        root_sources[key].append(record)
        root_surfaces[key].add(form)

    roots: list[dict[str, object]] = []
    for key in sorted(root_sources):
        surfaces = sorted(root_surfaces[key], key=lambda value: (value.lower(), value))
        roots.append(
            {
                "comparison_key": key,
                "surfaces": surfaces,
                "canonical_surface": surfaces[0],
                "train_frequency": training_frequencies[key],
                "attested_in_train": training_frequencies[key] > 0,
                "provisional": True,
                "sources": [
                    _reference_dict(record)
                    for record in sorted(root_sources[key], key=lambda item: item.identifier)
                ],
            }
        )

    compound_records = [
        record
        for record in morphology
        if record.form.strip() and record.description.casefold().startswith("compound;")
    ]
    compounds: list[dict[str, object]] = []
    operational_compound_keys: set[str] = set()
    for record in sorted(
        compound_records, key=lambda item: (comparison_key(item.form), item.identifier)
    ):
        form = normalize_text(record.form.strip())
        operational = _is_one_word_pretoken(form)
        if operational:
            operational_compound_keys.add(comparison_key(form))
        compounds.append(
            {
                "form": form,
                "comparison_key": comparison_key(form),
                "operational": operational,
                "train_frequency": training_frequencies[comparison_key(form)],
                "provisional": True,
                "source": _reference_dict(record),
            }
        )

    spelling_evidence = [
        _reference_dict(record)
        for record in linguistic
        if record.kind in {"orthographic_variation", "stress", "dialectal_variation"}
    ]
    sample_forms = [
        _reference_dict(record)
        for record in morphology
        if record.example.strip()
        and (
            record.source.startswith("project-resource:")
            or record.kind == "derived_word_relationship"
        )
    ]

    inventory = {
        "prefixes": list(PREFIXES),
        "infixes": list(INFIXES),
        "suffixes": list(SUFFIXES),
        "circumfixes": [{"prefix": prefix, "suffix": suffix} for prefix, suffix in CIRCUMFIXES],
        "clitics": list(CLITICS),
        "pang_variants": list(PANG_VARIANTS),
        "authority": "thesis proposal Chapter 2 Table 1, printed page 19 (PDF page 22)",
    }
    payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "evidence_status": "provisional_proxy_not_human_validated",
        "paper_inventory": inventory,
        "roots": roots,
        "compounds": compounds,
        "spelling_variants": [],
        "spelling_variant_evidence": spelling_evidence,
        "sample_inflected_forms": sample_forms,
        "construction_policy": {
            "comparison_normalization": "NFC then lowercase; emitted surfaces unchanged",
            "new_roots_from_training": False,
            "nonpaper_affixes_operational": False,
            "unstructured_variant_rewrites": False,
        },
    }
    lexicon_fingerprint = fingerprint(payload)
    lexicon_document = {**payload, "lexicon_fingerprint": lexicon_fingerprint}
    lexicon_path = output_dir / "training-lexicon.json"
    write_json(lexicon_path, lexicon_document)

    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "lexicon_fingerprint": lexicon_fingerprint,
        "lexicon_file_sha256": sha256_file(lexicon_path),
        "input_files": {
            "morphology_reference_sha256": sha256_file(morphology_path),
            "linguistic_evidence_sha256": sha256_file(linguistic_path),
            "train_sha256": sha256_file(dataset_root / "data/train.csv"),
        },
        "counts": {
            "operational_root_keys": len(roots),
            "operational_root_surfaces": sum(
                len(cast(list[str], row["surfaces"])) for row in roots
            ),
            "excluded_root_candidates": excluded_root_candidates,
            "compound_records": len(compounds),
            "operational_compounds": len(operational_compound_keys),
            "spelling_variant_mappings": 0,
            "spelling_variant_evidence": len(spelling_evidence),
            "sample_inflected_form_records": len(sample_forms),
            "prefixes": len(PREFIXES),
            "infixes": len(INFIXES),
            "suffixes": len(SUFFIXES),
            "circumfixes": len(CIRCUMFIXES),
            "clitics": len(CLITICS),
            "pang_variants": len(PANG_VARIANTS),
        },
    }
    manifest_document = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(output_dir / "training-lexicon-manifest.json", manifest_document)
    return manifest_document


def load_lexicon(path: Path) -> TrainingLexicon:
    raw: Any = read_json(path)
    if not isinstance(raw, dict):
        raise ValueError("training lexicon must be an object")
    document = cast(dict[str, Any], raw)
    recorded = document.get("lexicon_fingerprint")
    if not isinstance(recorded, str):
        raise ValueError("training lexicon fingerprint missing")
    payload = {key: value for key, value in document.items() if key != "lexicon_fingerprint"}
    if fingerprint(payload) != recorded:
        raise ValueError("training lexicon fingerprint mismatch")
    if document.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("training lexicon dataset fingerprint mismatch")

    roots_raw = document.get("roots")
    compounds_raw = document.get("compounds")
    variants_raw = document.get("spelling_variants")
    if not isinstance(roots_raw, list) or not isinstance(compounds_raw, list):
        raise ValueError("training lexicon inventories malformed")
    if not isinstance(variants_raw, list):
        raise ValueError("training lexicon variants malformed")
    roots = frozenset(
        str(cast(dict[str, Any], entry)["comparison_key"])
        for entry in roots_raw
        if isinstance(entry, dict)
    )
    compounds = frozenset(
        str(cast(dict[str, Any], entry)["comparison_key"])
        for entry in compounds_raw
        if isinstance(entry, dict) and bool(cast(dict[str, Any], entry).get("operational"))
    )
    variants = frozenset(
        str(cast(dict[str, Any], entry)["comparison_key"])
        for entry in variants_raw
        if isinstance(entry, dict) and "comparison_key" in entry
    )
    return TrainingLexicon(roots, compounds, variants, recorded)
