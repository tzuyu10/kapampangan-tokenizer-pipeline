from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol, cast

from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION, SPECIAL_TOKENS
from .dataset import read_id_text
from .lexicon import TrainingLexicon, load_lexicon
from .models import PreparedSequence, PretokenKind, Segmentation
from .morphology import MorphologicalSegmenter
from .pretokenizer import pretokenize_normalized
from .rust_bridge import RustMorphologicalSegmenter
from .serialization import (
    fingerprint,
    read_json,
    sha256_file,
    stable_compact_json,
    write_json,
)


class SegmenterProtocol(Protocol):
    def segment_many(self, tokens: list[str]) -> list[Segmentation]: ...


def _make_segmenter(engine: str, lexicon: TrainingLexicon) -> SegmenterProtocol:
    if engine == "python":
        return MorphologicalSegmenter(lexicon)
    if engine == "rust":
        return RustMorphologicalSegmenter(lexicon)
    raise ValueError(f"unsupported segmentation engine: {engine}")


def _initial_pair_stats(sequences: Iterable[PreparedSequence]) -> tuple[int, int]:
    pair_types: set[tuple[str, str]] = set()
    merge_upper_bound = 0
    for sequence in sequences:
        characters = list(sequence.surface)
        protected = set(sequence.protected_boundaries)
        for position in range(len(characters) - 1):
            if position + 1 in protected:
                continue
            pair_types.add((characters[position], characters[position + 1]))
            merge_upper_bound += 1
    return len(pair_types), merge_upper_bound


def prepare_training_stream(
    dataset_root: Path,
    lexicon_path: Path,
    output_dir: Path,
    *,
    engine: str = "rust",
) -> dict[str, object]:
    dataset_root = dataset_root.resolve()
    lexicon = load_lexicon(lexicon_path)
    segmenter = _make_segmenter(engine, lexicon)

    pretoken_counts: Counter[tuple[str, PretokenKind]] = Counter()
    record_count = 0
    sentence_codepoints = 0
    for record in read_id_text(dataset_root / "data/train.csv", role="train"):
        record_count += 1
        sentence_codepoints += len(record.text)
        for token in pretokenize_normalized(record.text):
            pretoken_counts[(token.surface, token.kind)] += 1

    word_surfaces = sorted(surface for surface, kind in pretoken_counts if kind == "word")
    segmentations = segmenter.segment_many(word_surfaces)
    segmentation_by_surface = dict(zip(word_surfaces, segmentations, strict=True))

    sequence_counts: Counter[tuple[str, tuple[int, ...], PretokenKind]] = Counter()
    status_occurrences: Counter[str] = Counter()
    status_types: Counter[str] = Counter()
    rule_occurrences: Counter[str] = Counter()
    word_occurrences = 0
    for (surface, kind), frequency in pretoken_counts.items():
        boundaries: tuple[int, ...] = ()
        if kind == "word":
            segmentation = segmentation_by_surface[surface]
            boundaries = segmentation.protected_boundaries
            status_occurrences[segmentation.status] += frequency
            status_types[segmentation.status] += 1
            if segmentation.rule_id is not None:
                rule_occurrences[segmentation.rule_id] += frequency
            word_occurrences += frequency
        sequence_counts[(surface, boundaries, kind)] += frequency

    sequences = [
        PreparedSequence(surface, boundaries, kind, frequency)
        for (surface, boundaries, kind), frequency in sorted(
            sequence_counts.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])
        )
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    stream_path = output_dir / "training-stream.jsonl"
    with stream_path.open("w", encoding="utf-8", newline="\n") as stream:
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

    characters = sorted(
        {character for sequence in sequences for character in sequence.surface},
        key=lambda value: value.encode("utf-8"),
    )
    initial_pair_types, feasible_merge_upper_bound = _initial_pair_stats(sequences)
    analyzed_occurrences = status_occurrences["accepted"]
    ambiguous_occurrences = status_occurrences["ambiguous"]
    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "input_train_sha256": sha256_file(dataset_root / "data/train.csv"),
        "lexicon_fingerprint": lexicon.lexicon_fingerprint,
        "segmentation_engine": engine,
        "training_records": record_count,
        "training_codepoints": sentence_codepoints,
        "pretoken_occurrences": sum(pretoken_counts.values()),
        "unique_prepared_sequences": len(sequences),
        "word_occurrences": word_occurrences,
        "word_types": len(word_surfaces),
        "character_inventory": characters,
        "character_inventory_size": len(characters),
        "special_token_count": len(SPECIAL_TOKENS),
        "initial_vocabulary_size": len(characters) + len(SPECIAL_TOKENS),
        "initial_permitted_pair_types": initial_pair_types,
        "feasible_merge_upper_bound": feasible_merge_upper_bound,
        "status_occurrences": dict(sorted(status_occurrences.items())),
        "status_types": dict(sorted(status_types.items())),
        "rule_occurrences": dict(sorted(rule_occurrences.items())),
        "segmentation_coverage": (
            analyzed_occurrences / word_occurrences if word_occurrences else 0.0
        ),
        "ambiguous_unchanged_occurrences": ambiguous_occurrences,
        "stream_file": stream_path.name,
        "stream_sha256": sha256_file(stream_path),
    }
    manifest_document = {**manifest_body, "manifest_fingerprint": fingerprint(manifest_body)}
    write_json(output_dir / "training-stream-manifest.json", manifest_document)
    return manifest_document


def load_prepared_stream(path: Path) -> list[PreparedSequence]:
    sequences: list[PreparedSequence] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"prepared stream line {line_number} is not an object")
            surface = value.get("surface")
            boundaries = value.get("protected_boundaries")
            kind = value.get("kind")
            frequency = value.get("frequency")
            if (
                not isinstance(surface, str)
                or not isinstance(boundaries, list)
                or not all(isinstance(item, int) for item in boundaries)
                or kind not in {"word", "whitespace", "punctuation", "symbol"}
                or not isinstance(frequency, int)
            ):
                raise ValueError(f"malformed prepared stream line {line_number}")
            sequences.append(
                PreparedSequence(surface, tuple(boundaries), cast(PretokenKind, kind), frequency)
            )
    return sequences


def _round_to_multiple(value: float, multiple: int) -> int:
    return max(multiple, math.floor(value / multiple + 0.5) * multiple)


def freeze_candidate_grid(prepared_manifest_path: Path, output_path: Path) -> dict[str, object]:
    raw = read_json(prepared_manifest_path)
    if not isinstance(raw, dict):
        raise ValueError("prepared manifest must be an object")
    manifest = cast(dict[str, object], raw)
    if manifest.get("dataset_fingerprint") != DATASET_FINGERPRINT:
        raise ValueError("prepared manifest dataset fingerprint mismatch")
    word_types = int(cast(int, manifest["word_types"]))
    initial_size = int(cast(int, manifest["initial_vocabulary_size"]))
    feasible_upper = int(cast(int, manifest["feasible_merge_upper_bound"]))
    maximum = initial_size + feasible_upper
    raw_targets = [
        _round_to_multiple(multiplier * math.sqrt(word_types), 64) for multiplier in (4, 8, 16)
    ]
    targets: list[int] = []
    for raw_target in raw_targets:
        target = min(maximum, max(initial_size + 64, raw_target))
        if targets and target <= targets[-1]:
            target = min(maximum, targets[-1] + 64)
        if target not in targets:
            targets.append(target)
    if len(targets) < 3:
        raise ValueError("prepared stream cannot support three distinct candidate targets")

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "frozen_before_validation",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "prepared_manifest_fingerprint": manifest.get("manifest_fingerprint"),
        "word_types": word_types,
        "initial_vocabulary_size": initial_size,
        "initial_permitted_pair_types": manifest.get("initial_permitted_pair_types"),
        "feasible_merge_upper_bound": feasible_upper,
        "formula": "nearest_multiple_64(multiplier * sqrt(word_types)); multipliers=[4,8,16]",
        "candidate_vocabulary_sizes": targets,
        "selection_hierarchy": [
            "reject_nonzero_training_protected_boundary_merge_violations",
            "minimize_validation_proxy_morphological_distance",
            "maximize_validation_proxy_mbf1",
            "maximize_validation_proxy_mcf1",
            "minimize_fertility_when_morphology_metrics_are_maintained",
            "prefer_smaller_vocabulary_as_final_tie_breaker",
        ],
        "validation_results_observed_when_frozen": False,
    }
    document = {**body, "grid_fingerprint": fingerprint(body)}
    write_json(output_path, document)
    return document
