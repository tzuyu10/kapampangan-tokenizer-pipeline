"""Compute the same boundary-F1 / Morphological-Consistency-F1 (MCF1) silver
diagnostics that `run_experiment.py validate()` already computes for the
`plain`/`penalty-1/2/4/8` conditions, but for the Unigram ablation (see
`train_unigram_ablation.py`) -- so "does Unigram look more morphologically
accurate than MorphBPE" can be checked as a corpus-wide number against this
experiment's own resegmentation audit, instead of a handful of hand-picked
sentences.

This is a READ-ONLY consumer of `run_experiment.py`'s existing outputs
(`runs/segmentations/resegmentation-audit.jsonl`,
`runs/segmentations/morphology-index.jsonl`, and, if already generated,
`reports/runtime-evaluation.json` for the existing plain/penalty numbers to
show alongside). It does not modify `run_experiment.py`, its report, or any
existing artifact -- it writes its own separate report instead.

Same caveats as everywhere else this repository reports these metrics: the
"gold" here is this experiment's own rule-derived resegmentation audit and
morphology index (silver, not independent/human-annotated gold), and this
is a training-corpus diagnostic, not a held-out evaluation.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))
sys.path.insert(0, str(EXPERIMENT_ROOT))

import run_experiment as v4run  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402

from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, read_json, write_json  # noqa: E402

TARGET_VOCAB_SIZES = (6080, 8192, 16384)
MIN_MORPHEME_LENGTH = 2
MIN_TOKEN_LENGTH = 2
MAX_GROUP_SIZE = 300

REPORTS_DIR = EXPERIMENT_ROOT / "reports"
REPORT_JSON_PATH = REPORTS_DIR / "unigram-ablation-boundary-metrics.json"
REPORT_MARKDOWN_PATH = REPORTS_DIR / "unigram-ablation-boundary-metrics.md"

EXISTING_CONDITIONS = ("plain_bpe", "penalty_1", "penalty_2", "penalty_4", "penalty_8")


def _unigram_boundary_metrics(
    tokenizer: Tokenizer, rows: list[dict[str, Any]]
) -> dict[str, object]:
    # Mirrors run_experiment.py's _runtime_metrics exactly (same formula),
    # adapted for a raw tokenizers.Tokenizer (list[str] tokens/offsets)
    # instead of this project's RuntimeTokenizer protocol.
    true_positive = false_positive = false_negative = 0
    missed_types = extra_types = exact_types = 0
    exact_occurrences = produced_tokens = total_occurrences = 0
    for row in rows:
        surface = str(row["surface"])
        segments = tuple(cast(list[str], row["v4_segments"]))
        gold = set(cast(list[int], row["v4_protected_boundaries"]))
        frequency = int(row["frequency"])
        encoding = tokenizer.encode(surface)
        pieces = tuple(encoding.tokens)
        if "".join(pieces) != surface:
            raise AssertionError(f"unigram ablation failed to round-trip {surface!r}")
        predicted = {end for _, end in encoding.offsets[:-1]}
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
        "vocabulary_size": tokenizer.get_vocab_size(),
        "evaluated_types": len(rows),
        "evaluated_occurrences": total_occurrences,
        "exact_segment_types": exact_types,
        "exact_segment_occurrences": exact_occurrences,
        "missed_boundary_types": missed_types,
        "extra_boundary_types": extra_types,
        "boundary_precision": precision,
        "boundary_recall": recall,
        "boundary_f1": v4run._f1(precision, recall),
        "fertility": produced_tokens / total_occurrences if total_occurrences else 0.0,
        "lexicon_used_at_runtime": False,
    }


def _unigram_mcf1(tokenizer: Tokenizer, index_rows: list[dict[str, Any]]) -> dict[str, object]:
    # Mirrors run_experiment.py's _morphological_consistency_f1 exactly (same
    # definitions, same deterministic group capping via v4run._capped_pairs),
    # adapted for a raw tokenizers.Tokenizer.
    surfaces = [cast(str, row["surface"]) for row in index_rows]
    morpheme_sets: list[frozenset[tuple[str, str]]] = []
    token_sets: list[frozenset[str]] = []
    for row, surface in zip(index_rows, surfaces, strict=True):
        morphemes = cast(list[dict[str, str]], row["morphemes"])
        morpheme_sets.append(
            frozenset(
                (unit["kind"], unit["underlying"])
                for unit in morphemes
                if len(unit["underlying"]) >= MIN_MORPHEME_LENGTH
            )
        )
        encoding = tokenizer.encode(surface)
        token_sets.append(
            frozenset(token for token in encoding.tokens if len(token) >= MIN_TOKEN_LENGTH)
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
    active_morpheme_groups = 0
    for members in morpheme_groups.values():
        if len(members) < 2:
            continue
        active_morpheme_groups += 1
        morpheme_pairs |= v4run._capped_pairs(members, MAX_GROUP_SIZE)

    token_pairs: set[tuple[int, int]] = set()
    active_token_groups = 0
    for members in token_groups.values():
        if len(members) < 2:
            continue
        active_token_groups += 1
        token_pairs |= v4run._capped_pairs(members, MAX_GROUP_SIZE)

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
        "morpheme_sharing_pairs": len(morpheme_pairs),
        "token_sharing_pairs": len(token_pairs),
        "true_positive_pairs": true_positive,
        "false_positive_pairs": false_positive,
        "false_negative_pairs": false_negative,
        "morphological_consistency_precision": precision,
        "morphological_consistency_recall": recall,
        "morphological_consistency_f1": v4run._f1(precision, recall),
    }


def _write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# Unigram ablation vs. Plain BPE / MorphBPE: boundary F1 and MCF1",
        "",
        "Silver diagnostics against this experiment's own resegmentation audit "
        "and morphology index (not independent/human-annotated gold), computed "
        "identically across every condition below.",
        "",
        "| vocab | condition | boundary F1 | boundary P | boundary R | MCF1 | MCF1 P | MCF1 R |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for vocab_size in TARGET_VOCAB_SIZES:
        conditions = report["targets"][str(vocab_size)]
        for condition_name in (*EXISTING_CONDITIONS, "unigram_ablation"):
            metrics = conditions.get(condition_name)
            if metrics is None:
                continue
            lines.append(
                "| {vocab} | {condition} | {bf1:.4f} | {bp:.4f} | {br:.4f} "
                "| {mcf1:.4f} | {mp:.4f} | {mr:.4f} |".format(
                    vocab=vocab_size,
                    condition=condition_name,
                    bf1=metrics.get("boundary_f1", 0.0),
                    bp=metrics.get("boundary_precision", 0.0),
                    br=metrics.get("boundary_recall", 0.0),
                    mcf1=metrics.get("morphological_consistency_f1", 0.0),
                    mp=metrics.get("morphological_consistency_precision", 0.0),
                    mr=metrics.get("morphological_consistency_recall", 0.0),
                )
            )
    lines += [
        "",
        "'unigram_ablation' is NOT NLLB's tokenizer -- a fresh Unigram-LM model "
        "trained on this project's own corpus at the matched local vocabulary "
        "size (see train_unigram_ablation.py / nllb_baseline_report.py).",
    ]
    REPORT_MARKDOWN_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MARKDOWN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    if not v4run.RESEGMENTATION_AUDIT_PATH.exists() or not v4run.MORPHOLOGY_INDEX_PATH.exists():
        raise SystemExit(
            "resegmentation audit / morphology index missing; run "
            "`python run_experiment.py prepare` for this experiment first."
        )
    boundary_rows = v4run._load_jsonl(v4run.RESEGMENTATION_AUDIT_PATH)
    morphology_rows = v4run._load_jsonl(v4run.MORPHOLOGY_INDEX_PATH)

    existing_report: Any = (
        read_json(v4run.RUNTIME_REPORT_PATH) if v4run.RUNTIME_REPORT_PATH.exists() else None
    )

    results: dict[str, Any] = {}
    for vocab_size in TARGET_VOCAB_SIZES:
        tokenizer_path = (
            EXPERIMENT_ROOT / f"artifacts/unigram-ablation/vocab-{vocab_size}/tokenizer.json"
        )
        if not tokenizer_path.exists():
            raise SystemExit(f"{tokenizer_path} missing; run train_unigram_ablation.py first.")
        tokenizer = Tokenizer.from_file(str(tokenizer_path))

        metrics = _unigram_boundary_metrics(tokenizer, boundary_rows)
        metrics.update(_unigram_mcf1(tokenizer, morphology_rows))

        comparison: dict[str, Any] = {"unigram_ablation": metrics}
        if existing_report is not None:
            size_entry = existing_report.get("targets", {}).get(str(vocab_size), {})
            for condition_name in EXISTING_CONDITIONS:
                if condition_name in size_entry:
                    comparison[condition_name] = size_entry[condition_name]
        results[str(vocab_size)] = comparison

    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "condition": "unigram_ablation",
        "not_nllb_tokenizer": True,
        "independent_evaluation_gold": False,
        "gold_source": (
            "this experiment's own rule-derived resegmentation audit / morphology "
            "index (silver, not independent gold) -- identical to the gold source "
            "already used for plain_bpe/penalty_* in reports/runtime-evaluation.json"
        ),
        "existing_v4_runtime_report_included": existing_report is not None,
        "existing_v4_runtime_report_fingerprint": (
            existing_report.get("report_fingerprint") if existing_report is not None else None
        ),
        "targets": results,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    write_json(REPORT_JSON_PATH, report)
    _write_markdown(report)
    print(f"Wrote {REPORT_JSON_PATH}")
    print(f"Wrote {REPORT_MARKDOWN_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
