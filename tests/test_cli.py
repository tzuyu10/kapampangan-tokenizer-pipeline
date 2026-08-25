from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest

from kapampangan_morphbpe import cli
from kapampangan_morphbpe.artifact import export_tokenizer_artifact
from kapampangan_morphbpe.bpe import BPEModel
from kapampangan_morphbpe.cli import (
    compare_main,
    main,
    nllbprop_main,
    prop2_main,
    prop_main,
    stochprop_main,
    v2prop2_main,
    v2prop_main,
    v3prop_main,
    v4prop_main,
)
from kapampangan_morphbpe.lexicon import TrainingLexicon
from kapampangan_morphbpe.pretokenizer import pretokenize


def _synthetic_comparison(text: str) -> dict[str, object]:
    normalized, pretokens = pretokenize(text)
    tokens = [
        {
            "end": pretoken.end,
            "pretoken_kind": pretoken.kind,
            "start": pretoken.start,
            "token": pretoken.surface,
        }
        for pretoken in pretokens
    ]
    side: dict[str, object] = {
        "tokens": tokens,
        "word_token_count": sum(pretoken.kind == "word" for pretoken in pretokens),
    }
    return {
        "normalized_text": normalized,
        "plain_bpe": side,
        "morphbpe": side,
    }


def test_compact_comparison_display_groups_words_and_calculates_fertility(
    capsys: object,
) -> None:
    cli._print_comparison(
        {
            "normalized_text": "ab cd",
            "morphbpe": {
                "word_token_count": 4,
                "tokens": [
                    {"token": "a", "start": 0, "end": 1, "pretoken_kind": "word"},
                    {"token": "b", "start": 1, "end": 2, "pretoken_kind": "word"},
                    {"token": " ", "start": 2, "end": 3, "pretoken_kind": "whitespace"},
                    {"token": "c", "start": 3, "end": 4, "pretoken_kind": "word"},
                    {"token": "d", "start": 4, "end": 5, "pretoken_kind": "word"},
                ],
            },
            "plain_bpe": {
                "word_token_count": 2,
                "tokens": [
                    {"token": "ab", "start": 0, "end": 2, "pretoken_kind": "word"},
                    {"token": " ", "start": 2, "end": 3, "pretoken_kind": "whitespace"},
                    {"token": "cd", "start": 3, "end": 5, "pretoken_kind": "word"},
                ],
            },
        }
    )
    assert capsys.readouterr().out == (  # type: ignore[attr-defined]
        "ab cd\n"
        "  MorphBPE  4 | a + b | c + d\n"
        "  Plain BPE 2 | ab | cd\n"
        "              | fertility morph 2.00 plain 1.00\n"
    )


def test_validate_and_tokenize_cli(toy_artifact: Path, capsys: object) -> None:
    assert main(["validate-artifact", "--artifact", str(toy_artifact)]) == 0
    validate_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert validate_output["reload_succeeded"] is True

    assert (
        main(
            [
                "tokenize",
                "--artifact",
                str(toy_artifact),
                "--text",
                "ab  ñ!",
            ]
        )
        == 0
    )
    tokenize_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert tokenize_output["normalized_text"] == "ab  ñ!"
    ids = tokenize_output["ids"]

    assert (
        main(
            [
                "decode",
                "--artifact",
                str(toy_artifact),
                "--ids",
                json.dumps(ids),
            ]
        )
        == 0
    )
    decode_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert decode_output["text"] == "ab  ñ!"


def test_compare_plain_bpe_and_morphbpe_cli(
    tmp_path: Path,
    toy_model: BPEModel,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain_artifact = tmp_path / "plain"
    morph_artifact = tmp_path / "morph"
    export_tokenizer_artifact(
        toy_model,
        plain_artifact,
        artifact_type="kapampangan_plain_bpe",
        metadata={"tokenizer_condition": "plain_bpe"},
    )
    export_tokenizer_artifact(
        toy_model,
        morph_artifact,
        metadata={"tokenizer_condition": "morphbpe"},
    )
    lexicon = TrainingLexicon(
        roots=frozenset({"b"}),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic",
    )
    monkeypatch.setattr("kapampangan_morphbpe.cli.load_lexicon", lambda _path: lexicon)

    assert (
        main(
            [
                "compare-tokenizers",
                "--plain-artifact",
                str(plain_artifact),
                "--morph-artifact",
                str(morph_artifact),
                "--morph-lexicon",
                str(tmp_path / "synthetic-lexicon.json"),
                "--text",
                "kab!",
            ]
        )
        == 0
    )
    output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert output["vocabulary_size"] == len(toy_model.vocabulary)
    assert output["vocabulary_sizes_match"] is True
    assert output["plain_bpe"]["pieces"] == ["k", "ab", "!"]
    assert output["morphbpe"]["pieces"] == ["k", "a", "b", "!"]
    assert output["morphbpe"]["morphology"][0]["segments"] == ["ka", "b"]
    assert output["morphbpe"]["morphology"][0]["protected_boundaries"] == [2]
    assert output["morphology_boundaries_enforced_at_runtime"] is True
    assert output["pieces_differ"] is True
    assert output["word_token_count_delta_morphbpe_minus_plain"] == 1
    assert output["comparison_mode"] == "runtime_constrained_morphology_extension"
    assert output["paper_aligned_standard_runtime"] is False
    assert output["lexicon_used_at_runtime"] is True


def test_paper_aligned_comparison_uses_standard_runtime_only(
    tmp_path: Path,
    toy_model: BPEModel,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plain_artifact = tmp_path / "plain"
    morph_artifact = tmp_path / "morph"
    export_tokenizer_artifact(
        toy_model,
        plain_artifact,
        artifact_type="kapampangan_plain_bpe",
        metadata={"tokenizer_condition": "plain_bpe"},
    )
    export_tokenizer_artifact(
        toy_model,
        morph_artifact,
        metadata={"tokenizer_condition": "morphbpe"},
    )
    monkeypatch.setattr(
        cli,
        "load_lexicon",
        lambda _path: pytest.fail("paper-aligned runtime must not load a lexicon"),
    )

    output = cli._compare_standard_bpe_runtime(plain_artifact, morph_artifact, "kab!")
    assert output["comparison_mode"] == "paper_aligned_standard_bpe_runtime"
    assert output["paper_aligned_standard_runtime"] is True
    assert output["lexicon_used_at_runtime"] is False
    assert output["morphology_boundaries_enforced_at_runtime"] is False
    assert output["plain_bpe"]["pieces"] == ["k", "ab", "!"]  # type: ignore[index]
    assert output["morphbpe"]["pieces"] == ["k", "ab", "!"]  # type: ignore[index]


def test_boundary_safe_comparison_uses_standard_runtime_only(
    tmp_path: Path,
    toy_model: BPEModel,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plain_artifact = tmp_path / "plain"
    morph_artifact = tmp_path / "morph"
    export_tokenizer_artifact(
        toy_model,
        plain_artifact,
        artifact_type="kapampangan_plain_bpe",
        metadata={"tokenizer_condition": "plain_bpe"},
    )
    export_tokenizer_artifact(
        toy_model,
        morph_artifact,
        metadata={"tokenizer_condition": "global_boundary_safe_morphbpe_extension"},
    )
    monkeypatch.setattr(
        cli,
        "load_lexicon",
        lambda _path: pytest.fail("prop2 runtime must not load a lexicon"),
    )

    output = cli._compare_boundary_safe_standard_runtime(
        plain_artifact,
        morph_artifact,
        "kab!",
    )
    assert output["comparison_mode"] == "boundary_safe_training_standard_bpe_runtime"
    assert output["paper_aligned_standard_runtime"] is True
    assert output["paper_replication_training"] is False
    assert output["lexicon_used_at_runtime"] is False
    assert output["morphology_boundaries_enforced_at_runtime"] is False
    assert output["boundary_guarantee_scope"] == "source_adjudicated_boundary_changes"


def test_weighted_comparison_uses_standard_runtime_without_word_guarantees(
    tmp_path: Path,
    toy_model: BPEModel,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plain_artifact = tmp_path / "plain"
    morph_artifact = tmp_path / "morph"
    export_tokenizer_artifact(
        toy_model,
        plain_artifact,
        artifact_type="kapampangan_plain_bpe",
        metadata={"tokenizer_condition": "plain_bpe"},
    )
    export_tokenizer_artifact(
        toy_model,
        morph_artifact,
        metadata={"tokenizer_condition": "weighted_morphbpe"},
    )
    monkeypatch.setattr(
        cli,
        "load_lexicon",
        lambda _path: pytest.fail("weighted runtime must not load a lexicon"),
    )

    output = cli._compare_weighted_standard_runtime(
        plain_artifact,
        morph_artifact,
        "kab!",
        4,
    )
    assert output["comparison_mode"] == "weighted_morphbpe_standard_runtime"
    assert output["lexicon_used_at_runtime"] is False
    assert output["morphology_boundaries_enforced_at_runtime"] is False
    assert output["crossing_penalty"] == 4
    assert output["boundary_guarantee_scope"] == "none"
    assert output["surface_specific_runtime_guarantees"] == []


@pytest.mark.parametrize(
    ("size", "condition", "plain_relative", "morph_relative", "lexicon_relative"),
    [
        (
            "6k",
            "original",
            "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer",
            "artifacts/selected-tokenizer",
            "resources/training-lexicon.json",
        ),
        (
            "6k",
            "experimental",
            "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer",
            "experiments/source_adjudicated_v1/artifacts/selected-tokenizer",
            "experiments/source_adjudicated_v1/resources/training-lexicon.json",
        ),
        (
            "8k",
            "original",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
            "experiments/vocab_ablation_v1/artifacts/original/candidates/vocab-8192",
            "resources/training-lexicon.json",
        ),
        (
            "8k",
            "experimental",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
            "experiments/vocab_ablation_v1/artifacts/source-adjudicated/candidates/vocab-8192",
            "experiments/source_adjudicated_v1/resources/training-lexicon.json",
        ),
        (
            "16k",
            "original",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
            "experiments/vocab_ablation_v1/artifacts/original/candidates/vocab-16384",
            "resources/training-lexicon.json",
        ),
        (
            "16k",
            "experimental",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
            "experiments/vocab_ablation_v1/artifacts/source-adjudicated/candidates/vocab-16384",
            "experiments/source_adjudicated_v1/resources/training-lexicon.json",
        ),
    ],
)
def test_short_compare_resolves_all_six_pairs(
    tmp_path: Path,
    size: str,
    condition: str,
    plain_relative: str,
    morph_relative: str,
    lexicon_relative: str,
) -> None:
    assert cli._comparison_paths(tmp_path, size, condition) == (
        tmp_path / plain_relative,
        tmp_path / morph_relative,
        tmp_path / lexicon_relative,
    )


def test_short_compare_supports_default_and_explicit_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph, lexicon = cli._comparison_paths(tmp_path, "8k", "experimental")
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    lexicon.parent.mkdir(parents=True, exist_ok=True)
    lexicon.write_text("{}", encoding="utf-8")
    calls: list[tuple[Path, Path, Path, str]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        morph_lexicon: Path,
        text: str,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, morph_lexicon, text))
        return _synthetic_comparison(text)

    monkeypatch.setattr(cli, "_compare_tokenizers", fake_compare)
    assert compare_main(["8k", "experimental", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("kabukasan\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, lexicon, "kabukasan")

    assert compare_main(["8k", "experimental", "Masanting ya.", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("Masanting ya.\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, lexicon, "Masanting ya.")


def test_prop_supports_default_and_sentence_text_without_lexicon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph, lexicon = cli._comparison_paths(tmp_path, "8k", "experimental")
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    assert not lexicon.exists()
    calls: list[tuple[Path, Path, str]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, text))
        return _synthetic_comparison(text)

    monkeypatch.setattr(cli, "_compare_standard_bpe_runtime", fake_compare)
    assert prop_main(["8k", "experimental", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("kabukasan\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, "kabukasan")

    sentence = "Bukas na datang ing pangulo."
    assert prop_main(["8k", "experimental", sentence, "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith(sentence + "\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, sentence)


@pytest.mark.parametrize(
    ("size", "plain_relative", "morph_relative"),
    [
        (
            "6k",
            "experiments/source_adjudicated_v1/artifacts/plain-bpe-tokenizer",
            "experiments/boundary_safe_v1/artifacts/candidates/vocab-6080",
        ),
        (
            "8k",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-8192",
            "experiments/boundary_safe_v1/artifacts/candidates/vocab-8192",
        ),
        (
            "16k",
            "experiments/vocab_ablation_v1/artifacts/plain/candidates/vocab-16384",
            "experiments/boundary_safe_v1/artifacts/candidates/vocab-16384",
        ),
    ],
)
def test_prop2_resolves_all_sizes(
    tmp_path: Path,
    size: str,
    plain_relative: str,
    morph_relative: str,
) -> None:
    assert cli._prop2_paths(tmp_path, size) == (
        tmp_path / plain_relative,
        tmp_path / morph_relative,
    )


def test_prop2_supports_default_and_sentence_text_without_lexicon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph = cli._prop2_paths(tmp_path, "8k")
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    calls: list[tuple[Path, Path, str]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, text))
        return _synthetic_comparison(text)

    monkeypatch.setattr(cli, "_compare_boundary_safe_standard_runtime", fake_compare)
    assert prop2_main(["8k", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("kabukasan\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, "kabukasan")

    sentence = "Bukas na datang ing pangulo."
    assert prop2_main(["8k", sentence, "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith(sentence + "\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, sentence)


@pytest.mark.parametrize("size", ["6k", "8k", "16k"])
@pytest.mark.parametrize("condition", ["morphbpe", "boundary-safe"])
def test_v2_comparison_paths(tmp_path: Path, size: str, condition: str) -> None:
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    assert cli._v2_paths(tmp_path, size, condition) == (
        tmp_path
        / "experiments/source_adjudicated_v2/artifacts/plain/candidates"
        / f"vocab-{vocabulary}",
        tmp_path
        / "experiments/source_adjudicated_v2/artifacts"
        / condition
        / "candidates"
        / f"vocab-{vocabulary}",
    )


@pytest.mark.parametrize(
    ("entry_point", "condition", "comparison_name"),
    [
        (v2prop_main, "morphbpe", "_compare_standard_bpe_runtime"),
        (v2prop2_main, "boundary-safe", "_compare_v2_boundary_safe_standard_runtime"),
    ],
)
def test_v2_commands_support_default_and_sentence_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
    entry_point: object,
    condition: str,
    comparison_name: str,
) -> None:
    plain, morph = cli._v2_paths(tmp_path, "8k", condition)
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    calls: list[tuple[Path, Path, str]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, text))
        return _synthetic_comparison(text)

    monkeypatch.setattr(cli, comparison_name, fake_compare)
    command = cast(Callable[[list[str] | None], int], entry_point)
    assert command(["8k", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("sinulat\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, "sinulat")

    sentence = "Bukas na datang ing pangulo."
    assert command(["8k", sentence, "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith(sentence + "\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, sentence)


@pytest.mark.parametrize("size", ["6k", "8k", "16k"])
@pytest.mark.parametrize("penalty", [1, 2, 4, 8])
def test_v3_comparison_paths(
    tmp_path: Path,
    size: str,
    penalty: int,
) -> None:
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    assert cli._weighted_v3_paths(tmp_path, size, penalty) == (
        tmp_path
        / "experiments/source_adjudicated_v2/artifacts/plain/candidates"
        / f"vocab-{vocabulary}",
        tmp_path
        / "experiments/weighted_morphbpe_v3/artifacts"
        / f"penalty-{penalty}"
        / "candidates"
        / f"vocab-{vocabulary}",
    )


def test_v3_command_has_no_surface_specific_guarantee(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph = cli._weighted_v3_paths(tmp_path, "8k", 4)
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    calls: list[tuple[Path, Path, str, int]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
        crossing_penalty: int,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, text, crossing_penalty))
        output = _synthetic_comparison(text)
        output["surface_specific_runtime_guarantees"] = []
        return output

    monkeypatch.setattr(cli, "_compare_weighted_standard_runtime", fake_compare)
    assert v3prop_main(["8k", "4", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("sumulat\n")  # type: ignore[attr-defined]
    assert calls == [(plain, morph, "sumulat", 4)]


@pytest.mark.parametrize("size", ["6k", "8k", "16k"])
@pytest.mark.parametrize("penalty", [1, 2, 4, 8])
def test_v4_comparison_paths(
    tmp_path: Path,
    size: str,
    penalty: int,
) -> None:
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    assert cli._v4_paths(tmp_path, size, penalty) == (
        tmp_path
        / "experiments/expanded_morphology_v4/artifacts/plain/candidates"
        / f"vocab-{vocabulary}",
        tmp_path
        / "experiments/expanded_morphology_v4/artifacts"
        / f"penalty-{penalty}"
        / "candidates"
        / f"vocab-{vocabulary}",
    )


def test_v4_command_has_no_surface_specific_guarantee(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph = cli._v4_paths(tmp_path, "8k", 4)
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    calls: list[tuple[Path, Path, str, int]] = []

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
        crossing_penalty: int,
    ) -> dict[str, object]:
        calls.append((plain_artifact, morph_artifact, text, crossing_penalty))
        output = _synthetic_comparison(text)
        output["surface_specific_runtime_guarantees"] = []
        return output

    monkeypatch.setattr(cli, "_compare_v4_standard_runtime", fake_compare)
    assert v4prop_main(["8k", "4", "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith("misamban\n")  # type: ignore[attr-defined]
    assert calls == [(plain, morph, "misamban", 4)]

    sentence = "Misamban la ing tau."
    assert v4prop_main(["8k", "4", sentence, "--root", str(tmp_path)]) == 0
    assert capsys.readouterr().out.startswith(sentence + "\n")  # type: ignore[attr-defined]
    assert calls[-1] == (plain, morph, sentence, 4)


@pytest.mark.parametrize("size", ["6k", "8k", "16k"])
def test_nllb_paths(tmp_path: Path, size: str) -> None:
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    assert cli._nllb_paths(tmp_path, size) == (
        tmp_path / "experiments/expanded_morphology_v4/resources/nllb-tokenizer/tokenizer.json",
        tmp_path
        / "experiments/expanded_morphology_v4/artifacts/unigram-ablation"
        / f"vocab-{vocabulary}"
        / "tokenizer.json",
    )


def _synthetic_nllb_comparison(text: str) -> dict[str, object]:
    normalized, pretokens = pretokenize(text)
    tokens = [
        {
            "end": pretoken.end,
            "pretoken_kind": pretoken.kind,
            "start": pretoken.start,
            "token": pretoken.surface,
        }
        for pretoken in pretokens
    ]
    side: dict[str, object] = {
        "tokens": tokens,
        "word_token_count": sum(pretoken.kind == "word" for pretoken in pretokens),
    }
    return {
        "normalized_text": normalized,
        "crossing_penalty": 4,
        "nllb": side,
        "unigram_ablation": side,
        "plain_bpe": side,
        "morphbpe": side,
    }


def test_nllbprop_labels_every_condition_and_flags_the_ablation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    calls: list[tuple[Path, str, int, str]] = []

    def fake_compare(
        repository_root: Path,
        size: str,
        crossing_penalty: int,
        text: str,
    ) -> dict[str, object]:
        calls.append((repository_root, size, crossing_penalty, text))
        return _synthetic_nllb_comparison(text)

    monkeypatch.setattr(cli, "_compare_nllb_baseline", fake_compare)
    assert nllbprop_main(["8k", "4", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert out.startswith("misamban\n")
    assert "NLLB-200" in out
    assert "Unigram-abl." in out
    assert "Plain BPE" in out
    assert "MorphBPE p4" in out
    assert "NOT NLLB's tokenizer" in out
    assert calls == [(tmp_path, "8k", 4, "misamban")]

    sentence = "Sumulat ako ng tula."
    assert nllbprop_main(["16k", "8", sentence, "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert out.startswith(sentence + "\n")
    assert calls[-1] == (tmp_path, "16k", 8, sentence)


def test_nllb_cached_metrics_returns_none_when_report_missing(tmp_path: Path) -> None:
    assert cli._nllb_cached_metrics(tmp_path, "8k", 4) is None


def _write_unigram_ablation_report(root: Path) -> None:
    report_dir = root / "experiments/expanded_morphology_v4/reports"
    report_dir.mkdir(parents=True)
    report = {
        "targets": {
            "8192": {
                "plain_bpe": {
                    "boundary_f1": 0.2325,
                    "boundary_precision": 0.3029,
                    "boundary_recall": 0.1887,
                    "morphological_consistency_f1": 0.1414,
                    "morphological_consistency_precision": 0.1481,
                    "morphological_consistency_recall": 0.1352,
                },
                "penalty_4": {
                    "boundary_f1": 0.5867,
                    "boundary_precision": 0.5591,
                    "boundary_recall": 0.6172,
                    "morphological_consistency_f1": 0.2168,
                    "morphological_consistency_precision": 0.2006,
                    "morphological_consistency_recall": 0.2358,
                },
                "unigram_ablation": {
                    "boundary_f1": 0.4363,
                    "boundary_precision": 0.5539,
                    "boundary_recall": 0.3599,
                    "morphological_consistency_f1": 0.2199,
                    "morphological_consistency_precision": 0.1968,
                    "morphological_consistency_recall": 0.2489,
                },
            }
        }
    }
    (report_dir / "unigram-ablation-boundary-metrics.json").write_text(
        json.dumps(report), encoding="utf-8"
    )


def test_nllb_cached_metrics_reads_cached_report(tmp_path: Path) -> None:
    _write_unigram_ablation_report(tmp_path)
    result = cli._nllb_cached_metrics(tmp_path, "8k", 4)
    assert result is not None
    plain, morph, unigram = result
    assert plain["boundary_f1"] == 0.2325
    assert morph["boundary_f1"] == 0.5867
    assert unigram["boundary_f1"] == 0.4363
    assert unigram["morphological_consistency_f1"] == 0.2199
    # A penalty not present in the cached report degrades gracefully to None.
    assert cli._nllb_cached_metrics(tmp_path, "8k", 8) is None


def test_nllbprop_prints_cached_metrics_when_report_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    _write_unigram_ablation_report(tmp_path)

    def fake_compare(
        repository_root: Path,
        size: str,
        crossing_penalty: int,
        text: str,
    ) -> dict[str, object]:
        return _synthetic_nllb_comparison(text)

    monkeypatch.setattr(cli, "_compare_nllb_baseline", fake_compare)
    assert nllbprop_main(["8k", "4", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "corpus-wide silver diagnostics" in out
    assert "morpheme boundary F1" in out
    assert "0.2325" in out
    assert "0.5867" in out
    assert "0.4363" in out
    assert "morphological consistency F1 (MCF1)" in out
    assert "0.1414" in out
    assert "0.2168" in out
    assert "0.2199" in out


@pytest.mark.parametrize("size", ["6k", "8k", "16k"])
@pytest.mark.parametrize("dropout_rate", [0.1, 0.2])
def test_stochastic_paths(tmp_path: Path, size: str, dropout_rate: float) -> None:
    vocabulary = {"6k": "6080", "8k": "8192", "16k": "16384"}[size]
    assert cli._stochastic_paths(tmp_path, size, dropout_rate) == (
        tmp_path / "experiments/expanded_morphology_v4/artifacts/plain/candidates"
        f"/vocab-{vocabulary}",
        tmp_path / "experiments/expanded_morphology_v4/artifacts/penalty-4/candidates"
        f"/vocab-{vocabulary}",
        tmp_path
        / "experiments/expanded_morphology_v4/artifacts"
        / f"stochastic-p4-d{dropout_rate:g}"
        / "candidates"
        / f"vocab-{vocabulary}",
    )


def _synthetic_stochastic_comparison(text: str) -> dict[str, object]:
    normalized, pretokens = pretokenize(text)
    tokens = [
        {
            "end": pretoken.end,
            "pretoken_kind": pretoken.kind,
            "start": pretoken.start,
            "token": pretoken.surface,
        }
        for pretoken in pretokens
    ]
    side: dict[str, object] = {
        "tokens": tokens,
        "word_token_count": sum(pretoken.kind == "word" for pretoken in pretokens),
    }
    return {
        "normalized_text": normalized,
        "crossing_penalty": 4,
        "dropout_rate": 0.2,
        "plain_bpe": side,
        "morphbpe": side,
        "stochastic": side,
    }


def test_stochprop_labels_every_condition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    calls: list[tuple[Path, str, float, str]] = []

    def fake_compare(
        repository_root: Path,
        size: str,
        dropout_rate: float,
        text: str,
    ) -> dict[str, object]:
        calls.append((repository_root, size, dropout_rate, text))
        return _synthetic_stochastic_comparison(text)

    monkeypatch.setattr(cli, "_compare_stochastic_morphbpe", fake_compare)
    assert stochprop_main(["8k", "0.2", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert out.startswith("misamban\n")
    assert "Plain BPE" in out
    assert "MorphBPE p4" in out
    assert "Stochastic d0.2" in out
    assert calls == [(tmp_path, "8k", 0.2, "misamban")]

    sentence = "Sumulat ako ng tula."
    assert stochprop_main(["6k", "0.1", sentence, "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert out.startswith(sentence + "\n")
    assert calls[-1] == (tmp_path, "6k", 0.1, sentence)


def test_stochastic_cached_metrics_returns_none_when_report_missing(tmp_path: Path) -> None:
    assert cli._stochastic_cached_metrics(tmp_path, "8k", 0.2) is None


def _write_stochastic_reports(root: Path) -> None:
    report_dir = root / "experiments/expanded_morphology_v4/reports"
    report_dir.mkdir(parents=True)
    v4_report = {
        "targets": {
            "8192": {
                "plain_bpe": {
                    "boundary_f1": 0.2325,
                    "boundary_precision": 0.3029,
                    "boundary_recall": 0.1887,
                    "morphological_consistency_f1": 0.1414,
                    "morphological_consistency_precision": 0.1481,
                    "morphological_consistency_recall": 0.1352,
                },
                "penalty_4": {
                    "boundary_f1": 0.5867,
                    "boundary_precision": 0.5591,
                    "boundary_recall": 0.6172,
                    "morphological_consistency_f1": 0.2168,
                    "morphological_consistency_precision": 0.2006,
                    "morphological_consistency_recall": 0.2358,
                },
            }
        }
    }
    (report_dir / "runtime-evaluation.json").write_text(json.dumps(v4_report), encoding="utf-8")
    stochastic_report = {
        "targets": {
            "8192": {
                "stochastic-p4-d0.2": {
                    "boundary_f1": 0.6395,
                    "boundary_precision": 0.5900,
                    "boundary_recall": 0.6982,
                    "morphological_consistency_f1": 0.2308,
                    "morphological_consistency_precision": 0.1937,
                    "morphological_consistency_recall": 0.2856,
                },
            }
        }
    }
    (report_dir / "stochastic-morphbpe-runtime-evaluation.json").write_text(
        json.dumps(stochastic_report), encoding="utf-8"
    )


def test_stochastic_cached_metrics_reads_cached_reports(tmp_path: Path) -> None:
    _write_stochastic_reports(tmp_path)
    result = cli._stochastic_cached_metrics(tmp_path, "8k", 0.2)
    assert result is not None
    plain, morph, stochastic = result
    assert plain["boundary_f1"] == 0.2325
    assert morph["boundary_f1"] == 0.5867
    assert stochastic["boundary_f1"] == 0.6395
    # A dropout rate not present in the cached report degrades gracefully to None.
    assert cli._stochastic_cached_metrics(tmp_path, "8k", 0.1) is None


def test_stochprop_prints_cached_metrics_when_report_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    _write_stochastic_reports(tmp_path)

    def fake_compare(
        repository_root: Path,
        size: str,
        dropout_rate: float,
        text: str,
    ) -> dict[str, object]:
        return _synthetic_stochastic_comparison(text)

    monkeypatch.setattr(cli, "_compare_stochastic_morphbpe", fake_compare)
    assert stochprop_main(["8k", "0.2", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "corpus-wide silver diagnostics" in out
    assert "morpheme boundary F1" in out
    assert "0.2325" in out
    assert "0.5867" in out
    assert "0.6395" in out
    assert "morphological consistency F1 (MCF1)" in out
    assert "0.1414" in out
    assert "0.2168" in out
    assert "0.2308" in out


def test_v4_cached_metrics_returns_none_when_report_missing(tmp_path: Path) -> None:
    assert cli._v4_cached_metrics(tmp_path, "8k", 4) is None


def _write_v4_runtime_report(root: Path) -> None:
    report_dir = root / "experiments/expanded_morphology_v4/reports"
    report_dir.mkdir(parents=True)
    report = {
        "targets": {
            "8192": {
                "plain_bpe": {
                    "boundary_f1": 0.2325,
                    "boundary_precision": 0.3029,
                    "boundary_recall": 0.1887,
                    "morphological_consistency_f1": 0.1414,
                    "morphological_consistency_precision": 0.1481,
                    "morphological_consistency_recall": 0.1352,
                },
                "penalty_4": {
                    "boundary_f1": 0.5867,
                    "boundary_precision": 0.5591,
                    "boundary_recall": 0.6172,
                    "morphological_consistency_f1": 0.2168,
                    "morphological_consistency_precision": 0.2006,
                    "morphological_consistency_recall": 0.2358,
                },
            }
        }
    }
    (report_dir / "runtime-evaluation.json").write_text(json.dumps(report), encoding="utf-8")


def test_v4_cached_metrics_reads_cached_report(tmp_path: Path) -> None:
    _write_v4_runtime_report(tmp_path)
    result = cli._v4_cached_metrics(tmp_path, "8k", 4)
    assert result is not None
    plain, morph = result
    assert plain["boundary_f1"] == 0.2325
    assert plain["morphological_consistency_f1"] == 0.1414
    assert morph["boundary_f1"] == 0.5867
    assert morph["morphological_consistency_f1"] == 0.2168
    # A penalty not present in the cached report degrades gracefully to None.
    assert cli._v4_cached_metrics(tmp_path, "8k", 8) is None


def test_v4prop_prints_boundary_f1_and_morphological_consistency_when_report_present(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: object,
) -> None:
    plain, morph = cli._v4_paths(tmp_path, "8k", 4)
    plain.mkdir(parents=True)
    morph.mkdir(parents=True)
    _write_v4_runtime_report(tmp_path)

    def fake_compare(
        plain_artifact: Path,
        morph_artifact: Path,
        text: str,
        crossing_penalty: int,
    ) -> dict[str, object]:
        return _synthetic_comparison(text)

    monkeypatch.setattr(cli, "_compare_v4_standard_runtime", fake_compare)
    assert v4prop_main(["8k", "4", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out  # type: ignore[attr-defined]
    assert "corpus-wide silver diagnostics" in out
    assert "morpheme boundary F1" in out
    assert "not independent/human-annotated gold" in out
    assert "0.2325" in out
    assert "0.5867" in out
    assert "morphological consistency F1 (MCF1)" in out
    assert "0.1414" in out
    assert "0.2168" in out


def test_segment_cli_accepts_words_and_sentences(
    monkeypatch: pytest.MonkeyPatch, capsys: object
) -> None:
    lexicon = TrainingLexicon(
        roots=frozenset({"sulat", "ya"}),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic",
    )
    monkeypatch.setattr("kapampangan_morphbpe.cli.load_lexicon", lambda _path: lexicon)
    lexicon_path = Path("unused-lexicon.json")

    assert (
        main(
            [
                "segment",
                "--lexicon",
                str(lexicon_path),
                "--text",
                "kasulatan",
            ]
        )
        == 0
    )
    word_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert word_output["display"] == "ka || sulat || an"
    assert word_output["status"] == "accepted"
    assert "normalized_text" not in word_output

    assert (
        main(
            [
                "segment",
                "--lexicon",
                str(lexicon_path),
                "--text",
                "Kasulatan ya.",
            ]
        )
        == 0
    )
    sentence_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert sentence_output["normalized_text"] == "Kasulatan ya."
    assert sentence_output["display"] == "Ka || sulat || an ya."
    assert [item["surface"] for item in sentence_output["pretokens"]] == [
        "Kasulatan",
        " ",
        "ya",
        ".",
    ]
    assert sentence_output["pretokens"][0]["analysis"]["status"] == "accepted"
    assert sentence_output["pretokens"][1]["analysis"] is None
    assert sentence_output["pretokens"][2]["analysis"]["status"] == "protected_root"
    assert sentence_output["pretokens"][3] == {
        "analysis": None,
        "display": ".",
        "end": 13,
        "kind": "punctuation",
        "start": 12,
        "surface": ".",
    }
