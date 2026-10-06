from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from hypothesis import given
from hypothesis import strategies as st

from kapampangan_morphbpe.lexicon import TrainingLexicon
from kapampangan_morphbpe.morphology import MorphologicalSegmenter
from kapampangan_morphbpe.rust_bridge import RustMorphologicalSegmenter


def lexicon() -> TrainingLexicon:
    return TrainingLexicon(
        roots=frozenset({"kan", "sulat", "basa", "pagkan", "main"}),
        compounds=frozenset({"bahay-basa", "makasulat"}),
        variants=frozenset({"súlat"}),
        lexicon_fingerprint="synthetic",
    )


def test_empty_root_compound_and_unknown() -> None:
    segmenter = MorphologicalSegmenter(lexicon())
    assert segmenter.segment("").status == "empty"
    assert segmenter.segment("sulat").status == "protected_root"
    assert segmenter.segment("bahay-basa").status == "protected_compound"
    assert segmenter.segment("xyz").status == "unchanged"


def test_prefix_infix_suffix_circumfix_and_clitic() -> None:
    segmenter = MorphologicalSegmenter(lexicon())
    assert segmenter.segment("masulat").segments == ("ma", "sulat")
    assert segmenter.segment("kuman").segments == ("k", "um", "an")
    assert segmenter.segment("sulatan").segments == ("sulat", "an")
    assert segmenter.segment("kasulatan").segments == ("ka", "sulat", "an")
    assert segmenter.segment("sulatya").segments == ("sulat", "ya")


def test_pang_variants_are_circumfix_only() -> None:
    segmenter = MorphologicalSegmenter(lexicon())
    assert segmenter.segment("pamkanan").segments == ("pam", "kan", "an")
    assert segmenter.segment("pankanan").segments == ("pan", "kan", "an")
    assert segmenter.segment("pangakanan").segments == ("panga", "kan", "an")
    assert segmenter.segment("pamkan").status == "unchanged"


def test_longest_valid_overlap_is_preserved_as_ambiguous() -> None:
    segmenter = MorphologicalSegmenter(lexicon())
    result = segmenter.segment("makapagkan")
    assert result.status == "ambiguous"
    assert result.segments == ("makapagkan",)
    assert result.rule_id is None


def test_known_root_prevents_root_internal_false_split() -> None:
    segmenter = MorphologicalSegmenter(lexicon())
    result = segmenter.segment("main")
    assert result.status == "protected_root"
    assert result.segments == ("main",)


def test_python_rust_exact_outputs_on_rule_inventory() -> None:
    python = MorphologicalSegmenter(lexicon())
    rust = RustMorphologicalSegmenter(lexicon())
    tokens = [
        "",
        "sulat",
        "bahay-basa",
        "masulat",
        "kuman",
        "sulatan",
        "kasulatan",
        "sulatya",
        "pamkanan",
        "makapagkan",
        "xyz",
        "SÚLAT",
    ]
    assert python.segment_many(tokens) == rust.segment_many(tokens)


def test_regression_fixture_python_rust_outputs() -> None:
    fixture_path = Path(__file__).parent / "fixtures/morphology-regressions.json"
    document = cast(dict[str, Any], json.loads(fixture_path.read_text(encoding="utf-8")))
    cases = cast(list[dict[str, Any]], document["cases"])
    python = MorphologicalSegmenter(lexicon())
    rust = RustMorphologicalSegmenter(lexicon())
    for case in cases:
        expected = (
            tuple(cast(list[str], case["segments"])),
            case["status"],
            case["rule_id"],
        )
        python_result = python.segment(cast(str, case["token"]))
        rust_result = rust.segment(cast(str, case["token"]))
        assert (python_result.segments, python_result.status, python_result.rule_id) == expected
        assert rust_result == python_result


@given(st.sampled_from(["kan", "sulat", "basa"]), st.sampled_from(["ma", "mag", "ipa"]))
def test_accepted_prefix_analysis_always_reconstructs(root: str, prefix: str) -> None:
    result = MorphologicalSegmenter(lexicon()).segment(prefix + root)
    assert "".join(result.segments) == result.token
