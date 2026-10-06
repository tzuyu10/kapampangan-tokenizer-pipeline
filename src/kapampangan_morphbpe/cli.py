from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

from .artifact import validate_artifact_files
from .bpe import train_candidate_models
from .dataset import verify_dataset
from .evaluation import evaluate_candidates, select_candidate
from .lexicon import build_lexicon, load_lexicon
from .morphology import MorphologicalSegmenter
from .nllb_contract import export_nllb_contract
from .pipeline import export_candidate_models, finalize_selected_tokenizer
from .prepare import freeze_candidate_grid, prepare_training_stream
from .pretokenizer import pretokenize
from .runtime_bridge import (
    RuntimeEncodedToken,
    RuntimeEncoding,
    RuntimeTokenizer,
    load_runtime_tokenizer,
)
from .serialization import read_json, write_json
from .verification import verify_clean_runtime, verify_python_rust_parity


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))


def _word_piece_display(side: dict[str, object]) -> str:
    raw_tokens = side.get("tokens")
    if not isinstance(raw_tokens, list):
        raise ValueError("comparison token rows are missing")
    groups: list[list[str]] = []
    current: list[str] = []
    previous_end: int | None = None
    for raw_token in raw_tokens:
        if not isinstance(raw_token, dict):
            raise ValueError("comparison token row must be an object")
        token = cast(dict[str, object], raw_token)
        if token.get("pretoken_kind") != "word":
            if current:
                groups.append(current)
                current = []
            previous_end = None
            continue
        surface = token.get("token")
        start = token.get("start")
        end = token.get("end")
        if not isinstance(surface, str) or not isinstance(start, int) or not isinstance(end, int):
            raise ValueError("comparison word token row is malformed")
        if current and start != previous_end:
            groups.append(current)
            current = []
        current.append(surface)
        previous_end = end
    if current:
        groups.append(current)
    return " | ".join(" + ".join(group) for group in groups) or "(no word tokens)"


def _print_comparison(value: dict[str, object]) -> None:
    normalized_text = value.get("normalized_text")
    plain_raw = value.get("plain_bpe")
    morph_raw = value.get("morphbpe")
    if (
        not isinstance(normalized_text, str)
        or not isinstance(plain_raw, dict)
        or not isinstance(morph_raw, dict)
    ):
        raise ValueError("comparison output is malformed")
    plain = cast(dict[str, object], plain_raw)
    morph = cast(dict[str, object], morph_raw)
    plain_count = plain.get("word_token_count")
    morph_count = morph.get("word_token_count")
    if not isinstance(plain_count, int) or not isinstance(morph_count, int):
        raise ValueError("comparison word token counts are missing")

    _normalized, pretokens = pretokenize(normalized_text)
    word_count = sum(pretoken.kind == "word" for pretoken in pretokens)
    plain_fertility = plain_count / word_count if word_count else 0.0
    morph_fertility = morph_count / word_count if word_count else 0.0
    label_width = len("Plain BPE")
    count_width = max(len(str(plain_count)), len(str(morph_count)))
    continuation_width = 2 + label_width + 1 + count_width

    print(normalized_text)
    print(
        f"  {'MorphBPE':<{label_width}} {morph_count:>{count_width}} | {_word_piece_display(morph)}"
    )
    print(
        f"  {'Plain BPE':<{label_width}} {plain_count:>{count_width}} | "
        f"{_word_piece_display(plain)}"
    )
    print(
        f"{'':<{continuation_width}} | fertility morph {morph_fertility:.2f} "
        f"plain {plain_fertility:.2f}"
    )


def _targets(grid_path: Path) -> list[int]:
    raw: Any = read_json(grid_path)
    if not isinstance(raw, dict):
        raise ValueError("candidate grid must be an object")
    values = cast(dict[str, Any], raw).get("candidate_vocabulary_sizes")
    if not isinstance(values, list) or not all(isinstance(item, int) for item in values):
        raise ValueError("candidate grid target list malformed")
    return cast(list[int], values)


def _segment_output(segmenter: MorphologicalSegmenter, text: str) -> dict[str, object]:
    normalized, pretokens = pretokenize(text)
    if len(pretokens) <= 1:
        return segmenter.segment(normalized).to_dict()

    output_pretokens: list[dict[str, object]] = []
    display_parts: list[str] = []
    for pretoken in pretokens:
        analysis = segmenter.segment(pretoken.surface) if pretoken.kind == "word" else None
        display = analysis.display if analysis is not None else pretoken.surface
        output_pretokens.append(
            {
                "surface": pretoken.surface,
                "start": pretoken.start,
                "end": pretoken.end,
                "kind": pretoken.kind,
                "display": display,
                "analysis": analysis.to_dict() if analysis is not None else None,
            }
        )
        display_parts.append(display)

    return {
        "normalized_text": normalized,
        "display": "".join(display_parts),
        "pretokens": output_pretokens,
    }


def _token_output(token: RuntimeEncodedToken, *, offset: int = 0) -> dict[str, object]:
    return {
        "token": token.token,
        "id": token.identifier,
        "start": token.start + offset,
        "end": token.end + offset,
        "pretoken_kind": token.pretoken_kind,
        "vocabulary_kind": token.vocabulary_kind,
    }


def _token_rows_output(normalized_text: str, tokens: list[dict[str, object]]) -> dict[str, object]:
    return {
        "normalized_text": normalized_text,
        "pieces": [token["token"] for token in tokens],
        "tokens": tokens,
        "ids": [token["id"] for token in tokens],
        "token_count": len(tokens),
        "word_token_count": sum(token["pretoken_kind"] == "word" for token in tokens),
        "nonwhitespace_token_count": sum(
            token["pretoken_kind"] != "whitespace" for token in tokens
        ),
    }


def _encoding_output(encoding: RuntimeEncoding) -> dict[str, object]:
    return _token_rows_output(
        encoding.normalized_text, [_token_output(token) for token in encoding.tokens]
    )


def _morphbpe_encoding_output(
    tokenizer: RuntimeTokenizer,
    segmenter: MorphologicalSegmenter,
    text: str,
) -> dict[str, object]:
    normalized, pretokens = pretokenize(text)
    token_rows: list[dict[str, object]] = []
    morphology: list[dict[str, object]] = []
    for pretoken in pretokens:
        if pretoken.kind == "word":
            analysis = segmenter.segment(pretoken.surface)
            segments = analysis.segments
            morphology.append(
                {
                    "surface": pretoken.surface,
                    "start": pretoken.start,
                    "end": pretoken.end,
                    "segments": list(segments),
                    "protected_boundaries": list(analysis.protected_boundaries),
                    "status": analysis.status,
                    "rule_id": analysis.rule_id,
                }
            )
        else:
            segments = (pretoken.surface,)
        segment_offset = 0
        for segment in segments:
            encoding = tokenizer.encode(segment)
            if encoding.normalized_text != segment:
                raise AssertionError("MorphBPE segment normalization changed unexpectedly")
            absolute_offset = pretoken.start + segment_offset
            token_rows.extend(
                _token_output(token, offset=absolute_offset) for token in encoding.tokens
            )
            segment_offset += len(segment)
        if segment_offset != len(pretoken.surface):
            raise AssertionError("MorphBPE segments did not reconstruct their pretoken")
    output = _token_rows_output(normalized, token_rows)
    output["morphology"] = morphology
    output["morphology_boundaries_enforced_at_runtime"] = True
    return output


def _artifact_manifest(artifact: Path, expected_type: str) -> dict[str, Any]:
    raw = read_json(artifact / "tokenizer-manifest.json")
    if not isinstance(raw, dict):
        raise ValueError(f"tokenizer manifest must be an object: {artifact}")
    manifest = cast(dict[str, Any], raw)
    if manifest.get("artifact_type") != expected_type:
        raise ValueError(
            f"expected {expected_type} artifact at {artifact}, "
            f"got {manifest.get('artifact_type')!r}"
        )
    return manifest


def _compare_tokenizers(
    plain_artifact: Path,
    morph_artifact: Path,
    morph_lexicon: Path,
    text: str,
) -> dict[str, object]:
    plain_manifest = _artifact_manifest(plain_artifact, "kapampangan_plain_bpe")
    morph_manifest = _artifact_manifest(morph_artifact, "kapampangan_morphbpe")
    plain_tokenizer = load_runtime_tokenizer(plain_artifact)
    morph_tokenizer = load_runtime_tokenizer(morph_artifact)
    if plain_tokenizer.vocabulary_size != morph_tokenizer.vocabulary_size:
        raise ValueError("plain BPE and MorphBPE vocabulary sizes differ; use matched artifacts")
    plain = _encoding_output(plain_tokenizer.encode(text))
    morph = _morphbpe_encoding_output(
        morph_tokenizer,
        MorphologicalSegmenter(load_lexicon(morph_lexicon)),
        text,
    )
    if plain["normalized_text"] != morph["normalized_text"]:
        raise AssertionError("plain BPE and MorphBPE normalization outputs differ")
    plain_word_count = cast(int, plain["word_token_count"])
    morph_word_count = cast(int, morph["word_token_count"])
    return {
        "comparison_mode": "runtime_constrained_morphology_extension",
        "paper_aligned_standard_runtime": False,
        "lexicon_used_at_runtime": True,
        "normalized_text": plain["normalized_text"],
        "vocabulary_size": plain_tokenizer.vocabulary_size,
        "vocabulary_sizes_match": True,
        "morphology_boundaries_enforced_at_runtime": True,
        "plain_bpe": {
            "artifact_fingerprint": plain_manifest.get("artifact_fingerprint"),
            **plain,
        },
        "morphbpe": {
            "artifact_fingerprint": morph_manifest.get("artifact_fingerprint"),
            **morph,
        },
        "word_token_count_delta_morphbpe_minus_plain": (morph_word_count - plain_word_count),
        "pieces_differ": plain["pieces"] != morph["pieces"],
        "note": "BPE pieces are statistical subwords, not gold morpheme labels.",
    }


def _compare_standard_bpe_runtime(
    plain_artifact: Path,
    morph_artifact: Path,
    text: str,
) -> dict[str, object]:
    plain_manifest = _artifact_manifest(plain_artifact, "kapampangan_plain_bpe")
    morph_manifest = _artifact_manifest(morph_artifact, "kapampangan_morphbpe")
    plain_tokenizer = load_runtime_tokenizer(plain_artifact)
    morph_tokenizer = load_runtime_tokenizer(morph_artifact)
    if plain_tokenizer.vocabulary_size != morph_tokenizer.vocabulary_size:
        raise ValueError("plain BPE and MorphBPE vocabulary sizes differ; use matched artifacts")
    plain = _encoding_output(plain_tokenizer.encode(text))
    morph = _encoding_output(morph_tokenizer.encode(text))
    if plain["normalized_text"] != morph["normalized_text"]:
        raise AssertionError("plain BPE and MorphBPE normalization outputs differ")
    plain_word_count = cast(int, plain["word_token_count"])
    morph_word_count = cast(int, morph["word_token_count"])
    return {
        "comparison_mode": "paper_aligned_standard_bpe_runtime",
        "paper_aligned_standard_runtime": True,
        "lexicon_used_at_runtime": False,
        "morphology_boundaries_enforced_at_runtime": False,
        "normalized_text": plain["normalized_text"],
        "vocabulary_size": plain_tokenizer.vocabulary_size,
        "vocabulary_sizes_match": True,
        "plain_bpe": {
            "artifact_fingerprint": plain_manifest.get("artifact_fingerprint"),
            **plain,
        },
        "morphbpe": {
            "artifact_fingerprint": morph_manifest.get("artifact_fingerprint"),
            "training_condition": "morphology_constrained_merge_learning",
            "runtime_condition": "standard_bpe_without_lexicon",
            **morph,
        },
        "word_token_count_delta_morphbpe_minus_plain": (morph_word_count - plain_word_count),
        "pieces_differ": plain["pieces"] != morph["pieces"],
        "note": (
            "Morphology constrained MorphBPE merge learning only; both artifacts use "
            "standard lexicon-free BPE runtime."
        ),
    }


def _compare_boundary_safe_standard_runtime(
    plain_artifact: Path,
    morph_artifact: Path,
    text: str,
) -> dict[str, object]:
    output = _compare_standard_bpe_runtime(plain_artifact, morph_artifact, text)
    output.update(
        {
            "comparison_mode": "boundary_safe_training_standard_bpe_runtime",
            "paper_replication_training": False,
            "boundary_guarantee_scope": "source_adjudicated_boundary_changes",
            "note": (
                "Training-only boundary-safe MorphBPE extension; both artifacts use "
                "standard lexicon-free BPE runtime. The closed-set guarantee applies only "
                "to frozen source-adjudicated boundary changes."
            ),
        }
    )
    morph = cast(dict[str, object], output["morphbpe"])
    morph["training_condition"] = "global_boundary_safe_morphbpe_extension"
    return output


def _compare_v2_boundary_safe_standard_runtime(
    plain_artifact: Path,
    morph_artifact: Path,
    text: str,
) -> dict[str, object]:
    output = _compare_standard_bpe_runtime(plain_artifact, morph_artifact, text)
    output.update(
        {
            "comparison_mode": "source_adjudicated_v2_boundary_safe_standard_runtime",
            "paper_replication_training": False,
            "boundary_guarantee_scope": (
                "lowercase_and_titlecase_sinulat_and_kabukasan_required_regressions"
            ),
            "note": (
                "Source-adjudicated v2 boundary-safe training extension; both artifacts "
                "use standard lexicon-free BPE runtime. The hard exact guarantee covers "
                "only lowercase/title-case sinulat and kabukasan; the complete "
                "source-supported list is an evaluation set, not a simultaneous guarantee."
            ),
        }
    )
    morph = cast(dict[str, object], output["morphbpe"])
    morph["training_condition"] = "source_adjudicated_v2_boundary_safe_extension"
    return output


def _compare_weighted_standard_runtime(
    plain_artifact: Path,
    morph_artifact: Path,
    text: str,
    crossing_penalty: int,
) -> dict[str, object]:
    output = _compare_standard_bpe_runtime(plain_artifact, morph_artifact, text)
    output.update(
        {
            "comparison_mode": "weighted_morphbpe_standard_runtime",
            "paper_replication_training": False,
            "crossing_penalty": crossing_penalty,
            "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
            "boundary_guarantee_scope": "none",
            "surface_specific_runtime_guarantees": [],
            "note": (
                "Weighted MorphBPE training extension with no word-specific guarantee; "
                "both artifacts use standard lexicon-free BPE runtime."
            ),
        }
    )
    morph = cast(dict[str, object], output["morphbpe"])
    morph["training_condition"] = "weighted_global_boundary_penalty"
    morph["crossing_penalty"] = crossing_penalty
    return output


def _compare_v4_standard_runtime(
    plain_artifact: Path,
    morph_artifact: Path,
    text: str,
    crossing_penalty: int,
) -> dict[str, object]:
    output = _compare_standard_bpe_runtime(plain_artifact, morph_artifact, text)
    output.update(
        {
            "comparison_mode": "expanded_morphology_v4_weighted_standard_runtime",
            "paper_replication_training": False,
            "crossing_penalty": crossing_penalty,
            "merge_score": "allowed_frequency-crossing_penalty*crossing_frequency",
            "boundary_guarantee_scope": "none",
            "surface_specific_runtime_guarantees": [],
            "note": (
                "Isolated, source-enriched expanded-morphology training extension "
                "(new affixes/morphophonological rules layered over the unmodified "
                "source_adjudicated_v2 root inventory), trained with the weighted "
                "MorphBPE penalty score; both artifacts use standard lexicon-free "
                "BPE runtime. Morphology biases merge learning but does not "
                "guarantee exact unseen-word segmentation at runtime."
            ),
        }
    )
    morph = cast(dict[str, object], output["morphbpe"])
    morph["training_condition"] = "expanded_morphology_v4_weighted_extension"
    morph["crossing_penalty"] = crossing_penalty
    return output


def _comparison_paths(repository_root: Path, size: str, condition: str) -> tuple[Path, Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported comparison size: {size}")
    if condition not in {"original", "experimental"}:
        raise ValueError(f"unsupported comparison condition: {condition}")

    if size == "6k":
        plain_artifact = (
            repository_root / "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer"
        )
        if condition == "original":
            morph_artifact = repository_root / "artifacts/selected-tokenizer"
        else:
            morph_artifact = (
                repository_root / "experiments/source_adjudicated_v1/artifacts/selected-tokenizer"
            )
    else:
        vocabulary = {"8k": "8192", "16k": "16384"}[size]
        plain_artifact = (
            repository_root
            / f"experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-{vocabulary}"
        )
        morph_condition = "original" if condition == "original" else "source-adjudicated"
        morph_artifact = (
            repository_root
            / "experiments/vocab_ablation_v1/artifacts"
            / morph_condition
            / "candidates"
            / f"vocab-{vocabulary}"
        )

    if condition == "original":
        morph_lexicon = repository_root / "resources/training-lexicon.json"
    else:
        morph_lexicon = (
            repository_root / "experiments/source_adjudicated_v1/resources/training-lexicon.json"
        )
    return plain_artifact, morph_artifact, morph_lexicon


def _prop2_paths(repository_root: Path, size: str) -> tuple[Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported prop2 size: {size}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    if size == "6k":
        plain_artifact = (
            repository_root / "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer"
        )
    else:
        plain_artifact = (
            repository_root
            / "experiments/vocab_ablation_v1/artifacts/plain/candidates"
            / f"vocab-{vocabulary}"
        )
    morph_artifact = (
        repository_root
        / "experiments/boundary_safe_v1/artifacts/candidates"
        / f"vocab-{vocabulary}"
    )
    return plain_artifact, morph_artifact


def _v2_paths(repository_root: Path, size: str, condition: str) -> tuple[Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported v2 comparison size: {size}")
    if condition not in {"morphbpe", "boundary-safe"}:
        raise ValueError(f"unsupported v2 comparison condition: {condition}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    experiment = repository_root / "experiments/source_adjudicated_v2/artifacts"
    plain_artifact = experiment / "plain" / "candidates" / f"vocab-{vocabulary}"
    morph_artifact = experiment / condition / "candidates" / f"vocab-{vocabulary}"
    return plain_artifact, morph_artifact


def _weighted_v3_paths(
    repository_root: Path,
    size: str,
    crossing_penalty: int,
) -> tuple[Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported v3 comparison size: {size}")
    if crossing_penalty not in {1, 2, 4, 8}:
        raise ValueError(f"unsupported v3 crossing penalty: {crossing_penalty}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    experiment = repository_root / "experiments/weighted_morphbpe_v3"
    plain_artifact = (
        repository_root
        / "experiments/source_adjudicated_v2/artifacts/plain/candidates"
        / f"vocab-{vocabulary}"
    )
    morph_artifact = (
        experiment
        / "artifacts"
        / f"penalty-{crossing_penalty}"
        / "candidates"
        / f"vocab-{vocabulary}"
    )
    return plain_artifact, morph_artifact


def _v4_paths(repository_root: Path, size: str, crossing_penalty: int) -> tuple[Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported v4 comparison size: {size}")
    if crossing_penalty not in {1, 2, 4, 8}:
        raise ValueError(f"unsupported v4 crossing penalty: {crossing_penalty}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    experiment = repository_root / "experiments/expanded_morphology_v4/artifacts"
    plain_artifact = experiment / "plain" / "candidates" / f"vocab-{vocabulary}"
    morph_artifact = (
        experiment / f"penalty-{crossing_penalty}" / "candidates" / f"vocab-{vocabulary}"
    )
    return plain_artifact, morph_artifact


def _nllb_paths(repository_root: Path, size: str) -> tuple[Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported nllbprop size: {size}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    v4_experiment = repository_root / "experiments/expanded_morphology_v4"
    nllb_tokenizer_path = v4_experiment / "resources/nllb-tokenizer/tokenizer.json"
    unigram_ablation_path = (
        v4_experiment / f"artifacts/unigram-ablation/vocab-{vocabulary}/tokenizer.json"
    )
    return nllb_tokenizer_path, unigram_ablation_path


def _load_hf_tokenizer_class() -> Any:
    try:
        from tokenizers import Tokenizer as HFTokenizer
    except ImportError as exc:
        raise ImportError(
            "nllbprop requires the optional 'nllb-baseline' extra (huggingface_hub, "
            'tokenizers): run `uv pip install -e ".[nllb-baseline]"`, fetch the NLLB '
            "tokenizer files, and run train_unigram_ablation.py -- see "
            "experiments/expanded_morphology_v4/README.md."
        ) from exc
    return HFTokenizer


def _nllb_word_spans(normalized_text: str) -> list[tuple[int, int]]:
    _, pretokens = pretokenize(normalized_text)
    return [(pretoken.start, pretoken.end) for pretoken in pretokens if pretoken.kind == "word"]


def _spans_overlap(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    start, end = span
    return any(start < w_end and end > w_start for w_start, w_end in spans)


def _nllb_token_rows(tokenizer: Any, normalized_text: str) -> list[dict[str, object]]:
    encoding = tokenizer.encode(normalized_text)
    word_spans = _nllb_word_spans(normalized_text)
    rows: list[dict[str, object]] = []
    for token, offset, identifier in zip(
        encoding.tokens, encoding.offsets, encoding.ids, strict=True
    ):
        start, end = offset
        kind = "word" if end > start and _spans_overlap((start, end), word_spans) else "other"
        rows.append(
            {
                "token": token,
                "id": identifier,
                "start": start,
                "end": end,
                "pretoken_kind": kind,
                "vocabulary_kind": "learned",
            }
        )
    return rows


def _unigram_ablation_token_rows(tokenizer: Any, text: str) -> tuple[str, list[dict[str, object]]]:
    # This tokenizer's pre_tokenizer was disabled at training time (see
    # train_unigram_ablation.py), so it must be driven the same way here:
    # pretokenize first, then encode each segment independently, exactly
    # like _morphbpe_encoding_output never merges across a pretoken boundary.
    normalized, pretokens = pretokenize(text)
    rows: list[dict[str, object]] = []
    for pretoken in pretokens:
        segment_encoding = tokenizer.encode(pretoken.surface)
        for token, offset, identifier in zip(
            segment_encoding.tokens, segment_encoding.offsets, segment_encoding.ids, strict=True
        ):
            local_start, local_end = offset
            rows.append(
                {
                    "token": token,
                    "id": identifier,
                    "start": pretoken.start + local_start,
                    "end": pretoken.start + local_end,
                    "pretoken_kind": pretoken.kind,
                    "vocabulary_kind": "learned",
                }
            )
    return normalized, rows


def _compare_nllb_baseline(
    repository_root: Path,
    size: str,
    crossing_penalty: int,
    text: str,
) -> dict[str, object]:
    hf_tokenizer_class = _load_hf_tokenizer_class()
    nllb_tokenizer_path, unigram_ablation_path = _nllb_paths(repository_root, size)
    plain_artifact, morph_artifact = _v4_paths(repository_root, size, crossing_penalty)
    missing = [
        path
        for path in (nllb_tokenizer_path, unigram_ablation_path, plain_artifact, morph_artifact)
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "nllbprop comparison input missing: "
            + ", ".join(map(str, missing))
            + " -- fetch the NLLB tokenizer files and run train_unigram_ablation.py "
            "(see experiments/expanded_morphology_v4/README.md)."
        )

    nllb_tokenizer = hf_tokenizer_class.from_file(str(nllb_tokenizer_path))
    nllb_tokenizer.post_processor = None
    unigram_tokenizer = hf_tokenizer_class.from_file(str(unigram_ablation_path))

    plain_tokenizer = load_runtime_tokenizer(plain_artifact)
    morph_tokenizer = load_runtime_tokenizer(morph_artifact)
    if plain_tokenizer.vocabulary_size != morph_tokenizer.vocabulary_size:
        raise ValueError("plain BPE and MorphBPE vocabulary sizes differ; use matched artifacts")
    if unigram_tokenizer.get_vocab_size() != plain_tokenizer.vocabulary_size:
        raise ValueError("unigram ablation vocabulary size does not match the local vocabulary")

    plain = _encoding_output(plain_tokenizer.encode(text))
    morph = _encoding_output(morph_tokenizer.encode(text))
    normalized_text = cast(str, plain["normalized_text"])
    if morph["normalized_text"] != normalized_text:
        raise AssertionError("plain BPE and MorphBPE normalization outputs differ")

    unigram_normalized, unigram_rows = _unigram_ablation_token_rows(unigram_tokenizer, text)
    if unigram_normalized != normalized_text:
        raise AssertionError("unigram ablation normalization output differs")
    unigram = _token_rows_output(unigram_normalized, unigram_rows)

    nllb = _token_rows_output(normalized_text, _nllb_token_rows(nllb_tokenizer, normalized_text))

    return {
        "comparison_mode": "nllb200_pretrained_tokenizer_vs_local_encode_time_only",
        "nllb_retrained_on_corpus": False,
        "unigram_ablation_is_nllb_tokenizer": False,
        "lexicon_used_at_runtime": False,
        "morphology_boundaries_enforced_at_runtime": False,
        "vocabulary_size": plain_tokenizer.vocabulary_size,
        "crossing_penalty": crossing_penalty,
        "normalized_text": normalized_text,
        "nllb": nllb,
        "unigram_ablation": unigram,
        "plain_bpe": plain,
        "morphbpe": morph,
        "note": (
            "NLLB is pretrained and not retrained on this corpus; its vocabulary "
            "(256,204) is over 30x the local vocabulary here, which confounds any "
            "fertility comparison against it. 'unigram_ablation' is NOT NLLB's "
            "tokenizer -- a fresh Unigram-LM model trained on this project's own "
            "corpus at the matched local vocabulary size, to isolate the algorithm "
            "effect from that confound. See "
            "experiments/expanded_morphology_v4/reports/nllb-baseline-comparison.md."
        ),
    }


def _print_nllb_comparison(value: dict[str, object]) -> None:
    normalized_text = cast(str, value["normalized_text"])
    penalty = value["crossing_penalty"]
    conditions: list[tuple[str, dict[str, object]]] = [
        ("NLLB-200", cast(dict[str, object], value["nllb"])),
        ("Unigram-abl.", cast(dict[str, object], value["unigram_ablation"])),
        ("Plain BPE", cast(dict[str, object], value["plain_bpe"])),
        (f"MorphBPE p{penalty}", cast(dict[str, object], value["morphbpe"])),
    ]
    _, pretokens = pretokenize(normalized_text)
    word_count = sum(pretoken.kind == "word" for pretoken in pretokens)
    label_width = max(len(label) for label, _ in conditions)
    count_width = max(len(str(side["word_token_count"])) for _, side in conditions)
    continuation_width = 2 + label_width + 1 + count_width

    print(normalized_text)
    for label, side in conditions:
        count = cast(int, side["word_token_count"])
        print(f"  {label:<{label_width}} {count:>{count_width}} | {_word_piece_display(side)}")
    fertility_text = "  ".join(
        f"{label} {(cast(int, side['word_token_count']) / word_count if word_count else 0.0):.2f}"
        for label, side in conditions
    )
    print(f"{'':<{continuation_width}} | fertility {fertility_text}")
    print(
        "  Encode-time only: NLLB is not retrained on this corpus and its vocabulary "
        "is ~30x larger than the local vocabulary above, which confounds fertility "
        "against it directly. 'Unigram-abl.' is NOT NLLB's tokenizer -- a fresh "
        "Unigram-LM model trained on this project's own corpus at the matched "
        "vocabulary size, isolating the algorithm effect from that confound."
    )


def _comparison_repository_root(explicit_root: Path | None) -> Path:
    if explicit_root is not None:
        return explicit_root.resolve()
    current = Path.cwd().resolve()
    source_checkout = Path(__file__).resolve().parents[2]
    for candidate in (current, *current.parents, source_checkout):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "artifacts/selected-tokenizer"
        ).is_dir():
            return candidate
    raise FileNotFoundError(
        "Kapampangan MorphBPE repository not found; run inside the repository or pass --root PATH"
    )


def build_compare_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="comp",
        description="Compare a matched Plain-BPE and MorphBPE tokenizer pair.",
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("condition", choices=("original", "experimental"))
    parser.add_argument(
        "text",
        nargs="?",
        default="kabukasan",
        help="quoted word or sentence to compare (default: kabukasan)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def build_prop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prop",
        description=(
            "Paper-aligned comparison of Plain BPE runtime with standard runtime "
            "from MorphBPE-constrained training."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("condition", choices=("original", "experimental"))
    parser.add_argument(
        "text",
        nargs="?",
        default="kabukasan",
        help="quoted word or sentence to compare (default: kabukasan)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def build_prop2_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prop2",
        description=(
            "Compare Plain BPE with the boundary-safe MorphBPE training extension; "
            "both use standard lexicon-free runtime."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument(
        "text",
        nargs="?",
        default="kabukasan",
        help="quoted word or sentence to compare (default: kabukasan)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def _build_v2_parser(program: str, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=program, description=description)
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument(
        "text",
        nargs="?",
        default="sinulat",
        help="quoted word or sentence to compare (default: sinulat)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def build_v3prop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="v3prop",
        description=(
            "Compare Plain BPE with weighted MorphBPE using standard lexicon-free runtime."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("crossing_penalty", type=int, choices=(1, 2, 4, 8))
    parser.add_argument(
        "text",
        nargs="?",
        default="sumulat",
        help="quoted word or sentence to compare (default: sumulat)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def build_v4prop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="v4prop",
        description=(
            "Compare Plain BPE with the expanded-morphology v4 weighted MorphBPE "
            "training extension using standard lexicon-free runtime."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("crossing_penalty", type=int, choices=(1, 2, 4, 8))
    parser.add_argument(
        "text",
        nargs="?",
        default="misamban",
        help="quoted word or sentence to compare (default: misamban)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def compare_main(argv: list[str] | None = None) -> int:
    args = build_compare_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    plain_artifact, morph_artifact, morph_lexicon = _comparison_paths(
        repository_root, cast(str, args.size), cast(str, args.condition)
    )
    missing = [
        path for path in (plain_artifact, morph_artifact, morph_lexicon) if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "comparison input missing: " + ", ".join(str(path) for path in missing)
        )
    _print_comparison(
        _compare_tokenizers(
            plain_artifact,
            morph_artifact,
            morph_lexicon,
            cast(str, args.text),
        )
    )
    return 0


def prop_main(argv: list[str] | None = None) -> int:
    args = build_prop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    plain_artifact, morph_artifact, _morph_lexicon = _comparison_paths(
        repository_root, cast(str, args.size), cast(str, args.condition)
    )
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "comparison input missing: " + ", ".join(str(path) for path in missing)
        )
    _print_comparison(
        _compare_standard_bpe_runtime(
            plain_artifact,
            morph_artifact,
            cast(str, args.text),
        )
    )
    return 0


def prop2_main(argv: list[str] | None = None) -> int:
    args = build_prop2_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    plain_artifact, morph_artifact = _prop2_paths(
        repository_root,
        cast(str, args.size),
    )
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "prop2 comparison input missing: " + ", ".join(str(path) for path in missing)
        )
    _print_comparison(
        _compare_boundary_safe_standard_runtime(
            plain_artifact,
            morph_artifact,
            cast(str, args.text),
        )
    )
    return 0


def v2prop_main(argv: list[str] | None = None) -> int:
    args = _build_v2_parser(
        "v2prop",
        "Compare Plain BPE with source-adjudicated v2 paper-runtime MorphBPE.",
    ).parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    plain_artifact, morph_artifact = _v2_paths(repository_root, cast(str, args.size), "morphbpe")
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError("v2prop comparison input missing: " + ", ".join(map(str, missing)))
    _print_comparison(
        _compare_standard_bpe_runtime(plain_artifact, morph_artifact, cast(str, args.text))
    )
    return 0


def v2prop2_main(argv: list[str] | None = None) -> int:
    args = _build_v2_parser(
        "v2prop2",
        "Compare Plain BPE with the source-adjudicated v2 boundary-safe extension.",
    ).parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    plain_artifact, morph_artifact = _v2_paths(
        repository_root, cast(str, args.size), "boundary-safe"
    )
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError("v2prop2 comparison input missing: " + ", ".join(map(str, missing)))
    _print_comparison(
        _compare_v2_boundary_safe_standard_runtime(
            plain_artifact, morph_artifact, cast(str, args.text)
        )
    )
    return 0


def v3prop_main(argv: list[str] | None = None) -> int:
    args = build_v3prop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    penalty = cast(int, args.crossing_penalty)
    plain_artifact, morph_artifact = _weighted_v3_paths(
        repository_root,
        cast(str, args.size),
        penalty,
    )
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError("v3prop comparison input missing: " + ", ".join(map(str, missing)))
    _print_comparison(
        _compare_weighted_standard_runtime(
            plain_artifact,
            morph_artifact,
            cast(str, args.text),
            penalty,
        )
    )
    return 0


def _v4_runtime_report(repository_root: Path) -> dict[str, Any] | None:
    report_path = (
        repository_root / "experiments/expanded_morphology_v4/reports/runtime-evaluation.json"
    )
    if not report_path.is_file():
        return None
    raw = read_json(report_path)
    if not isinstance(raw, dict):
        return None
    return cast(dict[str, Any], raw)


def _v4_cached_metrics(
    repository_root: Path, size: str, crossing_penalty: int
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Looks up the corpus-wide silver diagnostics that
    `run_experiment.py validate` already computed and cached in
    `reports/runtime-evaluation.json`, for the plain and weighted-penalty
    conditions at the requested vocabulary size. Returns None (rather than
    raising) when the report or this size/penalty pair is unavailable, since
    `v4prop`'s primary token comparison must keep working even before
    `validate` has been run.
    """
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    report = _v4_runtime_report(repository_root)
    if report is None:
        return None
    targets = report.get("targets")
    if not isinstance(targets, dict):
        return None
    conditions = targets.get(vocabulary)
    if not isinstance(conditions, dict):
        return None
    plain = conditions.get("plain_bpe")
    morph = conditions.get(f"penalty_{crossing_penalty}")
    if not isinstance(plain, dict) or not isinstance(morph, dict):
        return None
    return cast(dict[str, Any], plain), cast(dict[str, Any], morph)


def _print_v4_delta_line(
    label_width: int, label: str, value: float, precision: float, recall: float
) -> None:
    print(f"      {label:<{label_width}} {value:.4f}  (P {precision:.4f} R {recall:.4f})")


def _print_v4_boundary_f1(
    crossing_penalty: int, plain: dict[str, Any], morph: dict[str, Any]
) -> None:
    if "boundary_f1" not in plain or "boundary_f1" not in morph:
        return
    plain_f1 = cast(float, plain["boundary_f1"])
    morph_f1 = cast(float, morph["boundary_f1"])
    delta = morph_f1 - plain_f1
    relative_display = f"{(delta / plain_f1 * 100.0):+.1f}%" if plain_f1 else "n/a"
    morph_label = f"MorphBPE p{crossing_penalty}"
    label_width = max(len("Plain BPE"), len(morph_label))
    print(
        "    morpheme boundary F1 -- precision/recall of the tokenizer's "
        "predicted merge boundaries against this experiment's own "
        "rule-derived boundaries (the resegmentation audit). Those "
        "'gold' boundaries come from the same morphological segmenter that "
        "also biases training, so this is a silver self-consistency check, "
        "not independent/human-annotated gold, and it does not evaluate the "
        "sentence you typed -- only the fixed audit word list:"
    )
    _print_v4_delta_line(
        label_width,
        "Plain BPE",
        plain_f1,
        cast(float, plain["boundary_precision"]),
        cast(float, plain["boundary_recall"]),
    )
    _print_v4_delta_line(
        label_width,
        morph_label,
        morph_f1,
        cast(float, morph["boundary_precision"]),
        cast(float, morph["boundary_recall"]),
    )
    print(f"      {'':<{label_width}} delta {delta:+.4f} ({relative_display})")


def _print_v4_morphological_consistency(
    crossing_penalty: int, plain: dict[str, Any], morph: dict[str, Any]
) -> None:
    if "morphological_consistency_f1" not in plain or "morphological_consistency_f1" not in morph:
        return
    plain_f1 = cast(float, plain["morphological_consistency_f1"])
    morph_f1 = cast(float, morph["morphological_consistency_f1"])
    delta = morph_f1 - plain_f1
    relative_display = f"{(delta / plain_f1 * 100.0):+.1f}%" if plain_f1 else "n/a"
    morph_label = f"MorphBPE p{crossing_penalty}"
    label_width = max(len("Plain BPE"), len(morph_label))
    print(
        "    morphological consistency F1 (MCF1) -- whether words sharing a "
        "morpheme get shared tokens, and shared tokens correspond to shared "
        "morphemes, measured as word-pair precision/recall over this "
        "experiment's own morpheme labels (very large morpheme/token groups "
        "are capped to a deterministic sample). Not independent gold, and "
        "not specific to the sentence you typed -- it summarizes every "
        "analyzed word in the corpus:"
    )
    _print_v4_delta_line(
        label_width,
        "Plain BPE",
        plain_f1,
        cast(float, plain["morphological_consistency_precision"]),
        cast(float, plain["morphological_consistency_recall"]),
    )
    _print_v4_delta_line(
        label_width,
        morph_label,
        morph_f1,
        cast(float, morph["morphological_consistency_precision"]),
        cast(float, morph["morphological_consistency_recall"]),
    )
    print(f"      {'':<{label_width}} delta {delta:+.4f} ({relative_display})")


def v4prop_main(argv: list[str] | None = None) -> int:
    args = build_v4prop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    penalty = cast(int, args.crossing_penalty)
    size = cast(str, args.size)
    plain_artifact, morph_artifact = _v4_paths(repository_root, size, penalty)
    missing = [path for path in (plain_artifact, morph_artifact) if not path.exists()]
    if missing:
        raise FileNotFoundError("v4prop comparison input missing: " + ", ".join(map(str, missing)))
    _print_comparison(
        _compare_v4_standard_runtime(plain_artifact, morph_artifact, cast(str, args.text), penalty)
    )
    cached = _v4_cached_metrics(repository_root, size, penalty)
    if cached is not None:
        plain_metrics, morph_metrics = cached
        print(
            f"  corpus-wide silver diagnostics (vocab {size}; computed once by "
            "`validate`, cached in reports/runtime-evaluation.json, not "
            "recomputed for this call):"
        )
        _print_v4_boundary_f1(penalty, plain_metrics, morph_metrics)
        _print_v4_morphological_consistency(penalty, plain_metrics, morph_metrics)
    return 0


def _nllb_ablation_report(repository_root: Path) -> dict[str, Any] | None:
    report_path = (
        repository_root
        / "experiments/expanded_morphology_v4/reports/unigram-ablation-boundary-metrics.json"
    )
    if not report_path.is_file():
        return None
    raw = read_json(report_path)
    if not isinstance(raw, dict):
        return None
    return cast(dict[str, Any], raw)


def _nllb_cached_metrics(
    repository_root: Path, size: str, crossing_penalty: int
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    """Looks up the corpus-wide silver diagnostics that
    `evaluate_unigram_ablation.py` already computed and cached in
    `reports/unigram-ablation-boundary-metrics.json`, for the plain,
    weighted-penalty, and Unigram-ablation conditions at the requested
    vocabulary size. Returns None (rather than raising) when the report or
    this size/penalty pair is unavailable, since `nllbprop`'s primary token
    comparison must keep working even before that script has been run.
    """
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    report = _nllb_ablation_report(repository_root)
    if report is None:
        return None
    targets = report.get("targets")
    if not isinstance(targets, dict):
        return None
    conditions = targets.get(vocabulary)
    if not isinstance(conditions, dict):
        return None
    plain = conditions.get("plain_bpe")
    morph = conditions.get(f"penalty_{crossing_penalty}")
    unigram = conditions.get("unigram_ablation")
    if not isinstance(plain, dict) or not isinstance(morph, dict) or not isinstance(unigram, dict):
        return None
    return cast(dict[str, Any], plain), cast(dict[str, Any], morph), cast(dict[str, Any], unigram)


def _print_nllb_cached_metrics(
    size: str,
    crossing_penalty: int,
    plain: dict[str, Any],
    morph: dict[str, Any],
    unigram: dict[str, Any],
) -> None:
    if "boundary_f1" not in plain or "boundary_f1" not in morph or "boundary_f1" not in unigram:
        return
    morph_label = f"MorphBPE p{crossing_penalty}"
    label_width = max(len("Plain BPE"), len(morph_label), len("Unigram-abl."))
    rows = (("Plain BPE", plain), (morph_label, morph), ("Unigram-abl.", unigram))
    print(
        f"  corpus-wide silver diagnostics (vocab {size}; computed once by "
        "evaluate_unigram_ablation.py, cached in "
        "reports/unigram-ablation-boundary-metrics.json, not recomputed for "
        "this call). Unigram-abl. is NOT NLLB's tokenizer; NLLB itself has no "
        "cached corpus-wide diagnostic here since it is pretrained, not "
        "trained against this experiment's audit:"
    )
    print(
        "    morpheme boundary F1 -- precision/recall of each tokenizer's "
        "predicted merge boundaries against this experiment's own "
        "rule-derived boundaries (the resegmentation audit); silver "
        "self-consistency, not independent/human-annotated gold, and it does "
        "not evaluate the sentence you typed -- only the fixed audit word "
        "list:"
    )
    for label, metrics in rows:
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["boundary_f1"]),
            cast(float, metrics["boundary_precision"]),
            cast(float, metrics["boundary_recall"]),
        )
    print(
        "    morphological consistency F1 (MCF1) -- whether words sharing a "
        "morpheme get shared tokens, and shared tokens correspond to shared "
        "morphemes; same silver caveats as above:"
    )
    for label, metrics in rows:
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["morphological_consistency_f1"]),
            cast(float, metrics["morphological_consistency_precision"]),
            cast(float, metrics["morphological_consistency_recall"]),
        )


_STOCHASTIC_CROSSING_PENALTY = 4
_STOCHASTIC_DROPOUT_RATES = (0.1, 0.2)


def _stochastic_condition_name(dropout_rate: float) -> str:
    return f"stochastic-p{_STOCHASTIC_CROSSING_PENALTY}-d{dropout_rate:g}"


def _stochastic_paths(
    repository_root: Path, size: str, dropout_rate: float
) -> tuple[Path, Path, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported stochprop size: {size}")
    if dropout_rate not in _STOCHASTIC_DROPOUT_RATES:
        raise ValueError(f"unsupported stochprop dropout_rate: {dropout_rate}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    experiment = repository_root / "experiments/expanded_morphology_v4/artifacts"
    plain_artifact = experiment / "plain" / "candidates" / f"vocab-{vocabulary}"
    morph_artifact = (
        experiment
        / f"penalty-{_STOCHASTIC_CROSSING_PENALTY}"
        / "candidates"
        / f"vocab-{vocabulary}"
    )
    stochastic_artifact = (
        experiment / _stochastic_condition_name(dropout_rate) / "candidates" / f"vocab-{vocabulary}"
    )
    return plain_artifact, morph_artifact, stochastic_artifact


def _compare_stochastic_morphbpe(
    repository_root: Path,
    size: str,
    dropout_rate: float,
    text: str,
) -> dict[str, object]:
    plain_artifact, morph_artifact, stochastic_artifact = _stochastic_paths(
        repository_root, size, dropout_rate
    )
    missing = [
        path for path in (plain_artifact, morph_artifact, stochastic_artifact) if not path.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "stochprop comparison input missing: "
            + ", ".join(map(str, missing))
            + " -- run train_stochastic_morphbpe.py first (see "
            "experiments/expanded_morphology_v4/README.md)."
        )

    plain_manifest = _artifact_manifest(plain_artifact, "kapampangan_plain_bpe")
    morph_manifest = _artifact_manifest(morph_artifact, "kapampangan_morphbpe")
    stochastic_manifest = _artifact_manifest(stochastic_artifact, "kapampangan_morphbpe")
    plain_tokenizer = load_runtime_tokenizer(plain_artifact)
    morph_tokenizer = load_runtime_tokenizer(morph_artifact)
    stochastic_tokenizer = load_runtime_tokenizer(stochastic_artifact)
    if not (
        plain_tokenizer.vocabulary_size
        == morph_tokenizer.vocabulary_size
        == stochastic_tokenizer.vocabulary_size
    ):
        raise ValueError("plain/morphbpe/stochastic vocabulary sizes differ; use matched artifacts")

    plain = _encoding_output(plain_tokenizer.encode(text))
    morph = _encoding_output(morph_tokenizer.encode(text))
    stochastic = _encoding_output(stochastic_tokenizer.encode(text))
    normalized_text = cast(str, plain["normalized_text"])
    if morph["normalized_text"] != normalized_text or stochastic["normalized_text"] != (
        normalized_text
    ):
        raise AssertionError("plain/morphbpe/stochastic normalization outputs differ")

    return {
        "comparison_mode": "expanded_morphology_v4_stochastic_standard_runtime",
        "paper_replication_training": False,
        "lexicon_used_at_runtime": False,
        "morphology_boundaries_enforced_at_runtime": False,
        "vocabulary_size": plain_tokenizer.vocabulary_size,
        "crossing_penalty": _STOCHASTIC_CROSSING_PENALTY,
        "dropout_rate": dropout_rate,
        "normalized_text": normalized_text,
        "plain_bpe": {"artifact_fingerprint": plain_manifest.get("artifact_fingerprint"), **plain},
        "morphbpe": {"artifact_fingerprint": morph_manifest.get("artifact_fingerprint"), **morph},
        "stochastic": {
            "artifact_fingerprint": stochastic_manifest.get("artifact_fingerprint"),
            **stochastic,
        },
        "note": (
            "Stochastic MorphBPE thesis extension: WeightedMorphBPETrainer's own "
            "penalty score plus train-time-only dropout of intra-morpheme merge "
            "applications. Standard runtime is ordinary, fully deterministic, "
            "lexicon-free BPE, identical in kind to the plain/morphbpe conditions "
            "here -- only how the stochastic condition's merge table was learned "
            "differs. NOT Asgari et al. (2025)'s unmodified algorithm, nor a "
            "literal reproduction of BPE-dropout/Unigram sampling."
        ),
    }


def _print_stochastic_comparison(value: dict[str, object]) -> None:
    normalized_text = cast(str, value["normalized_text"])
    dropout_rate = cast(float, value["dropout_rate"])
    penalty = value["crossing_penalty"]
    conditions: list[tuple[str, dict[str, object]]] = [
        ("Plain BPE", cast(dict[str, object], value["plain_bpe"])),
        (f"MorphBPE p{penalty}", cast(dict[str, object], value["morphbpe"])),
        (f"Stochastic d{dropout_rate:g}", cast(dict[str, object], value["stochastic"])),
    ]
    _, pretokens = pretokenize(normalized_text)
    word_count = sum(pretoken.kind == "word" for pretoken in pretokens)
    label_width = max(len(label) for label, _ in conditions)
    count_width = max(len(str(side["word_token_count"])) for _, side in conditions)
    continuation_width = 2 + label_width + 1 + count_width

    print(normalized_text)
    for label, side in conditions:
        count = cast(int, side["word_token_count"])
        print(f"  {label:<{label_width}} {count:>{count_width}} | {_word_piece_display(side)}")
    fertility_text = "  ".join(
        f"{label} {(cast(int, side['word_token_count']) / word_count if word_count else 0.0):.2f}"
        for label, side in conditions
    )
    print(f"{'':<{continuation_width}} | fertility {fertility_text}")


def _stochastic_ablation_report(repository_root: Path) -> dict[str, Any] | None:
    report_path = (
        repository_root
        / "experiments/expanded_morphology_v4/reports/stochastic-morphbpe-runtime-evaluation.json"
    )
    if not report_path.is_file():
        return None
    raw = read_json(report_path)
    if not isinstance(raw, dict):
        return None
    return cast(dict[str, Any], raw)


def _stochastic_cached_metrics(
    repository_root: Path, size: str, dropout_rate: float
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    """Looks up cached corpus-wide silver diagnostics: plain/penalty-4 from
    `reports/runtime-evaluation.json` (already computed by `run_experiment.py
    validate`) and the stochastic condition from
    `reports/stochastic-morphbpe-runtime-evaluation.json` (computed by
    `train_stochastic_morphbpe.py`). Returns None if either report or this
    size/dropout_rate pair is unavailable, since `stochprop`'s primary token
    comparison must keep working before either has been run.
    """
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    v4_report = _v4_runtime_report(repository_root)
    stochastic_report = _stochastic_ablation_report(repository_root)
    if v4_report is None or stochastic_report is None:
        return None
    v4_targets = v4_report.get("targets")
    stochastic_targets = stochastic_report.get("targets")
    if not isinstance(v4_targets, dict) or not isinstance(stochastic_targets, dict):
        return None
    v4_conditions = v4_targets.get(vocabulary)
    stochastic_conditions = stochastic_targets.get(vocabulary)
    if not isinstance(v4_conditions, dict) or not isinstance(stochastic_conditions, dict):
        return None
    plain = v4_conditions.get("plain_bpe")
    morph = v4_conditions.get(f"penalty_{_STOCHASTIC_CROSSING_PENALTY}")
    stochastic = stochastic_conditions.get(_stochastic_condition_name(dropout_rate))
    if (
        not isinstance(plain, dict)
        or not isinstance(morph, dict)
        or not isinstance(stochastic, dict)
    ):
        return None
    return (
        cast(dict[str, Any], plain),
        cast(dict[str, Any], morph),
        cast(dict[str, Any], stochastic),
    )


def _print_stochastic_cached_metrics(
    dropout_rate: float,
    plain: dict[str, Any],
    morph: dict[str, Any],
    stochastic: dict[str, Any],
) -> None:
    if "boundary_f1" not in plain or "boundary_f1" not in morph or "boundary_f1" not in stochastic:
        return
    morph_label = f"MorphBPE p{_STOCHASTIC_CROSSING_PENALTY}"
    stochastic_label = f"Stochastic d{dropout_rate:g}"
    label_width = max(len("Plain BPE"), len(morph_label), len(stochastic_label))
    rows = (("Plain BPE", plain), (morph_label, morph), (stochastic_label, stochastic))
    print(
        "  corpus-wide silver diagnostics (computed once by "
        "train_stochastic_morphbpe.py, cached in "
        "reports/stochastic-morphbpe-runtime-evaluation.json, not recomputed "
        "for this call):"
    )
    print(
        "    morpheme boundary F1 -- precision/recall of each tokenizer's "
        "predicted merge boundaries against this experiment's own "
        "rule-derived boundaries (the resegmentation audit); silver "
        "self-consistency, not independent/human-annotated gold, and it does "
        "not evaluate the sentence you typed -- only the fixed audit word "
        "list:"
    )
    for label, metrics in rows:
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["boundary_f1"]),
            cast(float, metrics["boundary_precision"]),
            cast(float, metrics["boundary_recall"]),
        )
    print(
        "    morphological consistency F1 (MCF1) -- whether words sharing a "
        "morpheme get shared tokens, and shared tokens correspond to shared "
        "morphemes; same silver caveats as above:"
    )
    for label, metrics in rows:
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["morphological_consistency_f1"]),
            cast(float, metrics["morphological_consistency_precision"]),
            cast(float, metrics["morphological_consistency_recall"]),
        )


def _all_conditions_paths(repository_root: Path, size: str) -> dict[str, Path]:
    if size not in {"6k", "8k", "16k"}:
        raise ValueError(f"unsupported allprop size: {size}")
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    v4_experiment = repository_root / "experiments/expanded_morphology_v4"
    artifacts = v4_experiment / "artifacts"
    return {
        "nllb": v4_experiment / "resources/nllb-tokenizer/tokenizer.json",
        "unigram_ablation": artifacts / f"unigram-ablation/vocab-{vocabulary}/tokenizer.json",
        "plain": artifacts / "plain/candidates" / f"vocab-{vocabulary}",
        "morphbpe": (
            artifacts / f"penalty-{_STOCHASTIC_CROSSING_PENALTY}/candidates/vocab-{vocabulary}"
        ),
        "stochastic_d0.1": (
            artifacts / f"{_stochastic_condition_name(0.1)}/candidates/vocab-{vocabulary}"
        ),
        "stochastic_d0.2": (
            artifacts / f"{_stochastic_condition_name(0.2)}/candidates/vocab-{vocabulary}"
        ),
    }


def _compare_all_conditions(repository_root: Path, size: str, text: str) -> dict[str, object]:
    hf_tokenizer_class = _load_hf_tokenizer_class()
    paths = _all_conditions_paths(repository_root, size)
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "allprop comparison input missing: "
            + ", ".join(missing)
            + " -- fetch the NLLB tokenizer files, and run train_unigram_ablation.py "
            "and train_stochastic_morphbpe.py first (see "
            "experiments/expanded_morphology_v4/README.md)."
        )

    nllb_tokenizer = hf_tokenizer_class.from_file(str(paths["nllb"]))
    nllb_tokenizer.post_processor = None
    unigram_tokenizer = hf_tokenizer_class.from_file(str(paths["unigram_ablation"]))

    plain_tokenizer = load_runtime_tokenizer(paths["plain"])
    morph_tokenizer = load_runtime_tokenizer(paths["morphbpe"])
    stochastic_d01_tokenizer = load_runtime_tokenizer(paths["stochastic_d0.1"])
    stochastic_d02_tokenizer = load_runtime_tokenizer(paths["stochastic_d0.2"])
    local_sizes = {
        plain_tokenizer.vocabulary_size,
        morph_tokenizer.vocabulary_size,
        stochastic_d01_tokenizer.vocabulary_size,
        stochastic_d02_tokenizer.vocabulary_size,
    }
    if len(local_sizes) != 1:
        raise ValueError("local artifact vocabulary sizes differ; use matched artifacts")
    if unigram_tokenizer.get_vocab_size() != next(iter(local_sizes)):
        raise ValueError("unigram ablation vocabulary size does not match the local vocabulary")

    plain = _encoding_output(plain_tokenizer.encode(text))
    normalized_text = cast(str, plain["normalized_text"])
    morph = _encoding_output(morph_tokenizer.encode(text))
    stochastic_d01 = _encoding_output(stochastic_d01_tokenizer.encode(text))
    stochastic_d02 = _encoding_output(stochastic_d02_tokenizer.encode(text))
    for label, side in (
        ("morphbpe", morph),
        ("stochastic_d0.1", stochastic_d01),
        ("stochastic_d0.2", stochastic_d02),
    ):
        if side["normalized_text"] != normalized_text:
            raise AssertionError(f"{label} normalization output differs from plain_bpe")

    unigram_normalized, unigram_rows = _unigram_ablation_token_rows(unigram_tokenizer, text)
    if unigram_normalized != normalized_text:
        raise AssertionError("unigram ablation normalization output differs")
    unigram = _token_rows_output(unigram_normalized, unigram_rows)

    nllb = _token_rows_output(normalized_text, _nllb_token_rows(nllb_tokenizer, normalized_text))

    return {
        "comparison_mode": "expanded_morphology_v4_all_conditions_encode_time",
        "lexicon_used_at_runtime": False,
        "morphology_boundaries_enforced_at_runtime": False,
        "vocabulary_size": next(iter(local_sizes)),
        "crossing_penalty": _STOCHASTIC_CROSSING_PENALTY,
        "normalized_text": normalized_text,
        "nllb": nllb,
        "unigram_ablation": unigram,
        "plain_bpe": plain,
        "morphbpe": morph,
        "stochastic_d0.1": stochastic_d01,
        "stochastic_d0.2": stochastic_d02,
        "note": (
            "NLLB is pretrained, encode-time only, never retrained on this corpus; "
            "its vocabulary is ~30x the local vocabulary, which confounds any "
            "fertility comparison against it directly. 'unigram_ablation' is NOT "
            "NLLB's tokenizer -- a fresh Unigram-LM model trained on this corpus at "
            "the matched local vocabulary size. 'morphbpe' is the weighted-penalty "
            "condition at penalty 4; 'stochastic_d0.1'/'stochastic_d0.2' add "
            "train-time-only dropout on top of it. All local conditions use "
            "standard, fully deterministic, lexicon-free BPE inference."
        ),
    }


def _print_all_conditions_comparison(value: dict[str, object]) -> None:
    normalized_text = cast(str, value["normalized_text"])
    penalty = value["crossing_penalty"]
    conditions: list[tuple[str, dict[str, object]]] = [
        ("NLLB-200", cast(dict[str, object], value["nllb"])),
        ("Unigram-abl.", cast(dict[str, object], value["unigram_ablation"])),
        ("Plain BPE", cast(dict[str, object], value["plain_bpe"])),
        (f"MorphBPE p{penalty}", cast(dict[str, object], value["morphbpe"])),
        ("Stochastic d0.1", cast(dict[str, object], value["stochastic_d0.1"])),
        ("Stochastic d0.2", cast(dict[str, object], value["stochastic_d0.2"])),
    ]
    _, pretokens = pretokenize(normalized_text)
    word_count = sum(pretoken.kind == "word" for pretoken in pretokens)
    label_width = max(len(label) for label, _ in conditions)
    count_width = max(len(str(side["word_token_count"])) for _, side in conditions)
    continuation_width = 2 + label_width + 1 + count_width

    print(normalized_text)
    for label, side in conditions:
        count = cast(int, side["word_token_count"])
        print(f"  {label:<{label_width}} {count:>{count_width}} | {_word_piece_display(side)}")
    fertility_text = "  ".join(
        f"{label} {(cast(int, side['word_token_count']) / word_count if word_count else 0.0):.2f}"
        for label, side in conditions
    )
    print(f"{'':<{continuation_width}} | fertility {fertility_text}")


def _all_conditions_cached_metrics(
    repository_root: Path, size: str
) -> dict[str, dict[str, Any]] | None:
    """Pulls cached corpus-wide silver diagnostics for every local condition
    from the two reports that already contain them:
    `unigram-ablation-boundary-metrics.json` (plain_bpe, penalty_4,
    unigram_ablation -- see evaluate_unigram_ablation.py) and
    `stochastic-morphbpe-runtime-evaluation.json` (the two stochastic
    conditions -- see train_stochastic_morphbpe.py). NLLB has no cached
    metrics here: it is not trained on this corpus, so there is no
    meaningful way to score it against this experiment's own resegmentation
    audit. Returns None if either report or this size is unavailable.
    """
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    unigram_report = _nllb_ablation_report(repository_root)
    stochastic_report = _stochastic_ablation_report(repository_root)
    if unigram_report is None or stochastic_report is None:
        return None
    unigram_targets = unigram_report.get("targets")
    stochastic_targets = stochastic_report.get("targets")
    if not isinstance(unigram_targets, dict) or not isinstance(stochastic_targets, dict):
        return None
    unigram_conditions = unigram_targets.get(vocabulary)
    stochastic_conditions = stochastic_targets.get(vocabulary)
    if not isinstance(unigram_conditions, dict) or not isinstance(stochastic_conditions, dict):
        return None

    result: dict[str, dict[str, Any]] = {}
    for key, label in (
        ("plain_bpe", "Plain BPE"),
        (f"penalty_{_STOCHASTIC_CROSSING_PENALTY}", f"MorphBPE p{_STOCHASTIC_CROSSING_PENALTY}"),
        ("unigram_ablation", "Unigram-abl."),
    ):
        metrics = unigram_conditions.get(key)
        if isinstance(metrics, dict):
            result[label] = cast(dict[str, Any], metrics)
    for rate in (0.1, 0.2):
        metrics = stochastic_conditions.get(_stochastic_condition_name(rate))
        if isinstance(metrics, dict):
            result[f"Stochastic d{rate:g}"] = cast(dict[str, Any], metrics)
    return result or None


def _print_all_conditions_cached_metrics(metrics_by_label: dict[str, dict[str, Any]]) -> None:
    if not metrics_by_label or any(
        "boundary_f1" not in metrics for metrics in metrics_by_label.values()
    ):
        return
    label_width = max(len(label) for label in metrics_by_label)
    print(
        "  corpus-wide silver diagnostics (computed once by "
        "evaluate_unigram_ablation.py / train_stochastic_morphbpe.py, not "
        "recomputed for this call; NLLB has none -- not trained on this "
        "corpus):"
    )
    print(
        "    morpheme boundary F1 -- predicted merge boundaries vs. this "
        "experiment's own resegmentation audit; silver self-consistency, "
        "not independent/human-annotated gold, and it does not evaluate "
        "the sentence you typed -- only the fixed audit word list:"
    )
    for label, metrics in metrics_by_label.items():
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["boundary_f1"]),
            cast(float, metrics["boundary_precision"]),
            cast(float, metrics["boundary_recall"]),
        )
    print(
        "    morphological consistency F1 (MCF1) -- whether words sharing a "
        "morpheme get shared tokens, and shared tokens correspond to shared "
        "morphemes; same silver caveats as above:"
    )
    for label, metrics in metrics_by_label.items():
        _print_v4_delta_line(
            label_width,
            label,
            cast(float, metrics["morphological_consistency_f1"]),
            cast(float, metrics["morphological_consistency_precision"]),
            cast(float, metrics["morphological_consistency_recall"]),
        )


def build_allprop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="allprop",
        description=(
            "Compare NLLB-200, the Unigram-LM ablation, Plain BPE, weighted "
            "MorphBPE (penalty 4), and both stochastic-dropout MorphBPE "
            "conditions in one call, all at the same local vocabulary size."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument(
        "text",
        nargs="?",
        default="misamban",
        help="quoted word or sentence to compare (default: misamban)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def allprop_main(argv: list[str] | None = None) -> int:
    args = build_allprop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    size = cast(str, args.size)
    comparison = _compare_all_conditions(repository_root, size, cast(str, args.text))
    _print_all_conditions_comparison(comparison)
    cached = _all_conditions_cached_metrics(repository_root, size)
    if cached is not None:
        _print_all_conditions_cached_metrics(cached)
    return 0


def build_stochprop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="stochprop",
        description=(
            "Compare Plain BPE, weighted MorphBPE (penalty 4), and the "
            "stochastic-dropout MorphBPE extension using standard "
            "lexicon-free runtime."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("dropout_rate", type=float, choices=_STOCHASTIC_DROPOUT_RATES)
    parser.add_argument(
        "text",
        nargs="?",
        default="misamban",
        help="quoted word or sentence to compare (default: misamban)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def stochprop_main(argv: list[str] | None = None) -> int:
    args = build_stochprop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    dropout_rate = cast(float, args.dropout_rate)
    size = cast(str, args.size)
    comparison = _compare_stochastic_morphbpe(
        repository_root, size, dropout_rate, cast(str, args.text)
    )
    _print_stochastic_comparison(comparison)
    cached = _stochastic_cached_metrics(repository_root, size, dropout_rate)
    if cached is not None:
        plain_metrics, morph_metrics, stochastic_metrics = cached
        _print_stochastic_cached_metrics(
            dropout_rate, plain_metrics, morph_metrics, stochastic_metrics
        )
    return 0


def build_nllbprop_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nllbprop",
        description=(
            "Compare the real pretrained NLLB-200 tokenizer and a matched-vocabulary "
            "Unigram-LM ablation (NOT NLLB's tokenizer -- trained fresh on this "
            "project's own corpus) against local Plain BPE and expanded-morphology v4 "
            "weighted MorphBPE, all at the same vocabulary size. Encode-time only: "
            "NLLB is never retrained on this corpus."
        ),
    )
    parser.add_argument("size", choices=("6k", "8k", "16k"))
    parser.add_argument("crossing_penalty", type=int, choices=(1, 2, 4, 8))
    parser.add_argument(
        "text",
        nargs="?",
        default="misamban",
        help="quoted word or sentence to compare (default: misamban)",
    )
    parser.add_argument("--root", type=_path, help="repository root when run elsewhere")
    return parser


def nllbprop_main(argv: list[str] | None = None) -> int:
    args = build_nllbprop_parser().parse_args(argv)
    repository_root = _comparison_repository_root(args.root)
    penalty = cast(int, args.crossing_penalty)
    size = cast(str, args.size)
    comparison = _compare_nllb_baseline(repository_root, size, penalty, cast(str, args.text))
    _print_nllb_comparison(comparison)
    cached = _nllb_cached_metrics(repository_root, size, penalty)
    if cached is not None:
        plain_metrics, morph_metrics, unigram_metrics = cached
        _print_nllb_cached_metrics(size, penalty, plain_metrics, morph_metrics, unigram_metrics)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kapampangan-morphbpe")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify-dataset")
    verify.add_argument("--dataset-root", type=_path, required=True)
    verify.add_argument("--output", type=_path)

    lexicon = subparsers.add_parser("build-lexicon")
    lexicon.add_argument("--dataset-root", type=_path, required=True)
    lexicon.add_argument("--output-dir", type=_path, required=True)

    segment = subparsers.add_parser("segment")
    segment.add_argument("--lexicon", type=_path, required=True)
    segment.add_argument("--text", required=True)

    prepare = subparsers.add_parser("prepare-training")
    prepare.add_argument("--dataset-root", type=_path, required=True)
    prepare.add_argument("--lexicon", type=_path, required=True)
    prepare.add_argument("--output-dir", type=_path, required=True)
    prepare.add_argument("--engine", choices=("rust", "python"), default="rust")

    freeze = subparsers.add_parser("freeze-candidates")
    freeze.add_argument("--prepared-manifest", type=_path, required=True)
    freeze.add_argument("--output", type=_path, required=True)

    parity = subparsers.add_parser("verify-segmentation-parity")
    parity.add_argument("--dataset-root", type=_path, required=True)
    parity.add_argument("--lexicon", type=_path, required=True)
    parity.add_argument("--output", type=_path, required=True)

    train = subparsers.add_parser("train-candidates")
    train.add_argument("--prepared-stream", type=_path, required=True)
    train.add_argument("--prepared-manifest", type=_path, required=True)
    train.add_argument("--grid", type=_path, required=True)
    train.add_argument("--lexicon-manifest", type=_path, required=True)
    train.add_argument("--output-dir", type=_path, required=True)

    evaluate = subparsers.add_parser("evaluate-validation")
    evaluate.add_argument("--dataset-root", type=_path, required=True)
    evaluate.add_argument("--lexicon", type=_path, required=True)
    evaluate.add_argument("--candidates-dir", type=_path, required=True)
    evaluate.add_argument("--grid", type=_path, required=True)
    evaluate.add_argument("--reports-dir", type=_path, required=True)

    select = subparsers.add_parser("select-candidate")
    select.add_argument("--grid", type=_path, required=True)
    select.add_argument("--validation-report", type=_path, required=True)
    select.add_argument("--output", type=_path, required=True)

    finalize = subparsers.add_parser("finalize-tokenizer")
    finalize.add_argument("--prepared-stream", type=_path, required=True)
    finalize.add_argument("--selection", type=_path, required=True)
    finalize.add_argument("--lexicon-manifest", type=_path, required=True)
    finalize.add_argument("--prepared-manifest", type=_path, required=True)
    finalize.add_argument("--output-dir", type=_path, required=True)
    finalize.add_argument("--rebuild-dir", type=_path, required=True)

    tokenize = subparsers.add_parser("tokenize")
    tokenize.add_argument("--artifact", type=_path, required=True)
    tokenize.add_argument("--text", required=True)
    tokenize.add_argument("--add-special-tokens", action="store_true")

    compare = subparsers.add_parser("compare-tokenizers")
    compare.add_argument("--plain-artifact", type=_path, required=True)
    compare.add_argument("--morph-artifact", type=_path, required=True)
    compare.add_argument("--morph-lexicon", type=_path, required=True)
    compare.add_argument("--text", required=True)

    decode = subparsers.add_parser("decode")
    decode.add_argument("--artifact", type=_path, required=True)
    decode.add_argument("--ids", required=True, help="JSON list of integer token IDs")

    inspect = subparsers.add_parser("inspect-artifact")
    inspect.add_argument("--artifact", type=_path, required=True)

    validate = subparsers.add_parser("validate-artifact")
    validate.add_argument("--artifact", type=_path, required=True)

    runtime = subparsers.add_parser("verify-runtime-independence")
    runtime.add_argument("--artifact", type=_path, required=True)
    runtime.add_argument("--runtime-root", type=_path, required=True)
    runtime.add_argument("--output", type=_path, required=True)

    nllb = subparsers.add_parser("export-nllb-contract")
    nllb.add_argument("--artifact", type=_path, required=True)
    nllb.add_argument("--output-dir", type=_path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = cast(str, args.command)
    if command == "verify-dataset":
        result = verify_dataset(args.dataset_root)
        if args.output is not None:
            write_json(args.output, result)
        _print(result)
    elif command == "build-lexicon":
        _print(build_lexicon(args.dataset_root, args.output_dir))
    elif command == "segment":
        segmenter = MorphologicalSegmenter(load_lexicon(args.lexicon))
        _print(_segment_output(segmenter, args.text))
    elif command == "prepare-training":
        _print(
            prepare_training_stream(
                args.dataset_root, args.lexicon, args.output_dir, engine=args.engine
            )
        )
    elif command == "freeze-candidates":
        _print(freeze_candidate_grid(args.prepared_manifest, args.output))
    elif command == "verify-segmentation-parity":
        _print(verify_python_rust_parity(args.dataset_root, args.lexicon, args.output))
    elif command == "train-candidates":
        models, report = train_candidate_models(
            args.prepared_stream,
            args.prepared_manifest,
            args.grid,
            args.output_dir,
        )
        summary = export_candidate_models(
            models,
            args.output_dir,
            training_report_path=args.output_dir / "candidate-training-report.json",
            grid_path=args.grid,
            lexicon_manifest_path=args.lexicon_manifest,
            prepared_manifest_path=args.prepared_manifest,
        )
        _print({"training": report, "artifacts": summary})
    elif command == "evaluate-validation":
        _print(
            evaluate_candidates(
                args.dataset_root,
                args.lexicon,
                args.candidates_dir,
                _targets(args.grid),
                args.reports_dir,
            )
        )
    elif command == "select-candidate":
        _print(select_candidate(args.grid, args.validation_report, args.output))
    elif command == "finalize-tokenizer":
        _print(
            finalize_selected_tokenizer(
                args.prepared_stream,
                args.selection,
                args.output_dir,
                args.rebuild_dir,
                lexicon_manifest_path=args.lexicon_manifest,
                prepared_manifest_path=args.prepared_manifest,
            )
        )
    elif command == "tokenize":
        encoding = load_runtime_tokenizer(args.artifact).encode(
            args.text, add_special_tokens=args.add_special_tokens
        )
        _print(_encoding_output(encoding))
    elif command == "compare-tokenizers":
        _print(
            _compare_tokenizers(
                args.plain_artifact,
                args.morph_artifact,
                args.morph_lexicon,
                args.text,
            )
        )
    elif command == "decode":
        identifiers = json.loads(args.ids)
        if not isinstance(identifiers, list) or not all(
            isinstance(item, int) for item in identifiers
        ):
            raise ValueError("--ids must be a JSON list of integers")
        _print({"text": load_runtime_tokenizer(args.artifact).decode(identifiers)})
    elif command == "inspect-artifact":
        _print(read_json(args.artifact / "tokenizer-manifest.json"))
    elif command == "validate-artifact":
        result = validate_artifact_files(args.artifact)
        tokenizer = load_runtime_tokenizer(args.artifact)
        result["vocabulary_size"] = tokenizer.vocabulary_size
        result["reload_succeeded"] = True
        _print(result)
    elif command == "verify-runtime-independence":
        _print(verify_clean_runtime(args.artifact, args.runtime_root, args.output))
    elif command == "export-nllb-contract":
        _print(export_nllb_contract(args.artifact, args.output_dir))
    else:
        raise AssertionError(f"unhandled command: {command}")
    return 0
