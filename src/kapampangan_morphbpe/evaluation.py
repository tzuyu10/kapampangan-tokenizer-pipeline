from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION
from .dataset import read_id_text
from .lexicon import load_lexicon
from .models import Segmentation
from .morphology import MorphologicalSegmenter
from .pretokenizer import pretokenize_normalized
from .runtime_bridge import RuntimeTokenizer, load_runtime_tokenizer
from .serialization import fingerprint, read_json, sha256_file, write_json


@dataclass(frozen=True, slots=True)
class WordEvaluation:
    surface: str
    frequency: int
    segmentation: Segmentation
    predicted_boundaries: frozenset[int]
    tokens: tuple[str, ...]
    token_kinds: tuple[str, ...]
    token_lengths: tuple[int, ...]


def _f1(precision: float, recall: float) -> float:
    return 0.0 if precision + recall == 0.0 else 2.0 * precision * recall / (precision + recall)


def _mcf1(words: list[WordEvaluation]) -> dict[str, float | int]:
    eligible = [
        word
        for word in words
        if word.segmentation.status in {"accepted", "protected_root", "protected_compound"}
    ]
    count = len(eligible)
    if count < 2:
        return {
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "shared_token_pairs": 0,
            "shared_morpheme_pairs": 0,
            "shared_both_pairs": 0,
            "word_types": count,
        }

    token_bits: dict[str, int] = defaultdict(int)
    morpheme_bits: dict[str, int] = defaultdict(int)
    for index, word in enumerate(eligible):
        bit = 1 << index
        for token in set(word.tokens):
            token_bits[token] |= bit
        for morpheme in {segment.lower() for segment in word.segmentation.segments}:
            morpheme_bits[morpheme] |= bit

    all_mask = (1 << count) - 1
    shared_token_pairs = 0
    shared_morpheme_pairs = 0
    shared_both_pairs = 0
    for index, word in enumerate(eligible):
        token_neighbors = 0
        for token in set(word.tokens):
            token_neighbors |= token_bits[token]
        morpheme_neighbors = 0
        for morpheme in {segment.lower() for segment in word.segmentation.segments}:
            morpheme_neighbors |= morpheme_bits[morpheme]
        higher_mask = all_mask & ~((1 << (index + 1)) - 1)
        token_neighbors &= higher_mask
        morpheme_neighbors &= higher_mask
        shared_token_pairs += token_neighbors.bit_count()
        shared_morpheme_pairs += morpheme_neighbors.bit_count()
        shared_both_pairs += (token_neighbors & morpheme_neighbors).bit_count()

    precision = shared_both_pairs / shared_token_pairs if shared_token_pairs else 0.0
    recall = shared_both_pairs / shared_morpheme_pairs if shared_morpheme_pairs else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": _f1(precision, recall),
        "shared_token_pairs": shared_token_pairs,
        "shared_morpheme_pairs": shared_morpheme_pairs,
        "shared_both_pairs": shared_both_pairs,
        "word_types": count,
    }


def _evaluate_word(
    surface: str,
    frequency: int,
    segmenter: MorphologicalSegmenter,
    tokenizer: RuntimeTokenizer,
) -> WordEvaluation:
    segmentation = segmenter.segment(surface)
    encoding = tokenizer.encode(surface)
    word_tokens = tuple(token for token in encoding.tokens if token.pretoken_kind == "word")
    if not word_tokens and surface:
        raise ValueError(f"runtime produced no lexical tokens for {surface!r}")
    predicted_boundaries = frozenset(token.end for token in word_tokens[:-1])
    return WordEvaluation(
        surface=surface,
        frequency=frequency,
        segmentation=segmentation,
        predicted_boundaries=predicted_boundaries,
        tokens=tuple(token.token for token in word_tokens),
        token_kinds=tuple(token.vocabulary_kind for token in word_tokens),
        token_lengths=tuple(token.end - token.start for token in word_tokens),
    )


def evaluate_candidate(
    dataset_root: Path,
    lexicon_path: Path,
    artifact_dir: Path,
) -> dict[str, object]:
    tokenizer = load_runtime_tokenizer(artifact_dir)
    segmenter = MorphologicalSegmenter(load_lexicon(lexicon_path))
    word_counts: Counter[str] = Counter()
    sentences = 0
    nonwhitespace_tokens = 0
    all_runtime_tokens = 0
    for record in read_id_text(dataset_root / "data/validation.csv", role="validation"):
        sentences += 1
        for pretoken in pretokenize_normalized(record.text):
            if pretoken.kind == "word":
                word_counts[pretoken.surface] += 1
        encoding = tokenizer.encode(record.text)
        all_runtime_tokens += len(encoding.tokens)
        nonwhitespace_tokens += sum(
            token.pretoken_kind != "whitespace" for token in encoding.tokens
        )

    words = [
        _evaluate_word(surface, word_counts[surface], segmenter, tokenizer)
        for surface in sorted(word_counts)
    ]
    word_occurrences = sum(word_counts.values())
    produced_word_tokens = sum(len(word.tokens) * word.frequency for word in words)
    character_tokens = sum(
        sum(kind == "character" for kind in word.token_kinds) * word.frequency for word in words
    )
    unknown_tokens = sum(
        sum(token == "<unk>" for token in word.tokens) * word.frequency for word in words
    )
    total_token_codepoints = sum(sum(word.token_lengths) * word.frequency for word in words)

    true_positive = false_positive = false_negative = 0
    distance_weighted_sum = 0.0
    distance_occurrences = 0
    validation_boundary_crossings = 0
    protected_unsegmented_extra_boundaries = 0
    proxy_status_occurrences: Counter[str] = Counter()
    for word in words:
        proxy_status_occurrences[word.segmentation.status] += word.frequency
        gold = frozenset(word.segmentation.protected_boundaries)
        predicted = word.predicted_boundaries
        if word.segmentation.status == "accepted":
            true_positive += len(gold & predicted) * word.frequency
            false_positive += len(predicted - gold) * word.frequency
            false_negative += len(gold - predicted) * word.frequency
            validation_boundary_crossings += len(gold - predicted) * word.frequency
            possible = max(1, len(word.surface) - 1)
            distance_weighted_sum += len(gold ^ predicted) / possible * word.frequency
            distance_occurrences += word.frequency
        elif word.segmentation.status in {"protected_root", "protected_compound"}:
            protected_unsegmented_extra_boundaries += len(predicted) * word.frequency

    boundary_precision = (
        true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    )
    boundary_recall = (
        true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    )
    mcf1 = _mcf1(words)

    manifest_raw: Any = read_json(artifact_dir / "tokenizer-manifest.json")
    if not isinstance(manifest_raw, dict):
        raise ValueError("candidate manifest malformed")
    manifest = cast(dict[str, Any], manifest_raw)
    metrics: dict[str, object] = {
        "fertility_rate": produced_word_tokens / word_occurrences if word_occurrences else 0.0,
        "morpheme_boundary": {
            "precision": boundary_precision,
            "recall": boundary_recall,
            "f1": _f1(boundary_precision, boundary_recall),
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
        },
        "morphological_consistency": mcf1,
        "morphological_distance": (
            distance_weighted_sum / distance_occurrences if distance_occurrences else 0.0
        ),
        "training_protected_boundary_merge_violations": manifest.get(
            "protected_boundary_merge_violations"
        ),
        "validation_proxy_boundary_crossings": validation_boundary_crossings,
        "protected_root_or_compound_extra_boundaries": protected_unsegmented_extra_boundaries,
        "character_fallback_rate": (
            character_tokens / produced_word_tokens if produced_word_tokens else 0.0
        ),
        "unknown_fallback_rate": (
            unknown_tokens / produced_word_tokens if produced_word_tokens else 0.0
        ),
        "average_token_length_codepoints": (
            total_token_codepoints / produced_word_tokens if produced_word_tokens else 0.0
        ),
        "tokens_per_sentence_nonwhitespace": (
            nonwhitespace_tokens / sentences if sentences else 0.0
        ),
        "tokens_per_sentence_with_whitespace": (
            all_runtime_tokens / sentences if sentences else 0.0
        ),
        "tokens_per_word": produced_word_tokens / word_occurrences if word_occurrences else 0.0,
    }
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "evidence_status": "provisional_development_proxy_not_gold",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "validation_sha256": sha256_file(dataset_root / "data/validation.csv"),
        "artifact_fingerprint": manifest.get("artifact_fingerprint"),
        "target_vocabulary_size": manifest.get("target_vocabulary_size"),
        "actual_vocabulary_size": manifest.get("actual_vocabulary_size"),
        "validation_records": sentences,
        "word_occurrences": word_occurrences,
        "word_types": len(words),
        "proxy_scored_occurrences": distance_occurrences,
        "proxy_status_occurrences": dict(sorted(proxy_status_occurrences.items())),
        "metrics": metrics,
        "held_out_test_used": False,
    }
    return {**body, "report_fingerprint": fingerprint(body)}


def evaluate_candidates(
    dataset_root: Path,
    lexicon_path: Path,
    candidates_dir: Path,
    targets: list[int],
    reports_dir: Path,
) -> dict[str, object]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    candidates: list[dict[str, object]] = []
    for target in targets:
        artifact_dir = candidates_dir / f"vocab-{target}"
        report = evaluate_candidate(dataset_root, lexicon_path, artifact_dir)
        write_json(reports_dir / f"vocab-{target}-validation.json", report)
        candidates.append(report)
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "evidence_status": "provisional_development_proxy_not_gold",
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidates": candidates,
        "held_out_test_used": False,
    }
    document = {**body, "report_fingerprint": fingerprint(body)}
    write_json(reports_dir / "validation-candidates.json", document)
    return document


def select_candidate(
    grid_path: Path,
    validation_report_path: Path,
    output_path: Path,
) -> dict[str, object]:
    grid_raw = read_json(grid_path)
    report_raw = read_json(validation_report_path)
    if not isinstance(grid_raw, dict) or not isinstance(report_raw, dict):
        raise ValueError("grid and validation report must be objects")
    grid = cast(dict[str, Any], grid_raw)
    report = cast(dict[str, Any], report_raw)
    if grid.get("validation_results_observed_when_frozen") is not False:
        raise ValueError("candidate grid was not frozen before validation")
    candidates_raw = report.get("candidates")
    if not isinstance(candidates_raw, list):
        raise ValueError("validation candidate list missing")
    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, object]] = []
    for candidate_raw in candidates_raw:
        if not isinstance(candidate_raw, dict):
            raise ValueError("candidate report malformed")
        candidate = cast(dict[str, Any], candidate_raw)
        metrics = candidate.get("metrics")
        if not isinstance(metrics, dict):
            raise ValueError("candidate metrics malformed")
        if metrics.get("training_protected_boundary_merge_violations") != 0:
            rejected.append(
                {
                    "target_vocabulary_size": candidate.get("target_vocabulary_size"),
                    "reason": "training_protected_boundary_merge_violation",
                }
            )
        else:
            eligible.append(candidate)
    if not eligible:
        raise ValueError("no candidate satisfies protected-boundary training constraint")

    def selection_key(candidate: dict[str, Any]) -> tuple[float, float, float, float, int]:
        metrics = cast(dict[str, Any], candidate["metrics"])
        boundary = cast(dict[str, Any], metrics["morpheme_boundary"])
        consistency = cast(dict[str, Any], metrics["morphological_consistency"])
        return (
            float(metrics["morphological_distance"]),
            -float(boundary["f1"]),
            -float(consistency["f1"]),
            float(metrics["fertility_rate"]),
            int(candidate["target_vocabulary_size"]),
        )

    selected = min(eligible, key=selection_key)
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "candidate_grid_fingerprint": grid.get("grid_fingerprint"),
        "validation_report_fingerprint": report.get("report_fingerprint"),
        "selection_hierarchy": grid.get("selection_hierarchy"),
        "selected_target_vocabulary_size": selected.get("target_vocabulary_size"),
        "selected_artifact_fingerprint": selected.get("artifact_fingerprint"),
        "selected_metrics": selected.get("metrics"),
        "rejected_candidates": rejected,
        "held_out_test_used": False,
        "selection_reason": "lexicographic application of the pre-frozen hierarchy",
    }
    document = {**body, "selection_fingerprint": fingerprint(body)}
    write_json(output_path, document)
    return document
