from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

_REPO_ROOT = Path(__file__).resolve().parents[1]
_V4_ROOT = _REPO_ROOT / "experiments/expanded_morphology_v4"
if str(_V4_ROOT) not in sys.path:
    sys.path.insert(0, str(_V4_ROOT))

import run_experiment as v4run  # noqa: E402


@dataclass(frozen=True, slots=True)
class _FakeToken:
    token: str
    identifier: int = 0
    start: int = 0
    end: int = 0
    pretoken_kind: str = "word"
    vocabulary_kind: str = "merge"


@dataclass(frozen=True, slots=True)
class _FakeEncoding:
    tokens: tuple[_FakeToken, ...]


class _FakeTokenizer:
    """Minimal stand-in for RuntimeTokenizer: returns pre-scripted pieces per
    surface so the metric's own pair logic can be tested independently of any
    trained artifact."""

    def __init__(self, pieces: dict[str, tuple[str, ...]]) -> None:
        self._pieces = pieces

    def encode(self, text: str, *, add_special_tokens: bool = False) -> _FakeEncoding:
        del add_special_tokens
        return _FakeEncoding(tuple(_FakeToken(token=piece) for piece in self._pieces[text]))

    def decode(
        self, identifiers: list[int] | tuple[int, ...], *, skip_special_tokens: bool = True
    ) -> str:
        raise NotImplementedError

    @property
    def vocabulary_size(self) -> int:
        return 0


def _row(surface: str, morphemes: list[tuple[str, str]]) -> dict[str, object]:
    return {
        "surface": surface,
        "morphemes": [{"kind": kind, "underlying": label} for kind, label in morphemes],
    }


def test_morphological_consistency_f1_hand_computed_example() -> None:
    """Five words, hand-traced expected TP/FP/FN:

    - misamban/pisamban/sasamba all share the root morpheme "samba" AND the
      tokenizer represents it with the identical token "samba" in every one
      -> 3 true-positive pairs.
    - misamban/pisamban/kabukasan all share the "-an" suffix morpheme, but
      the tokenizer only emits a bare 1-character "n" for misamban/pisamban
      (excluded by the length>=2 filter) versus a 2-character "an" for
      kabukasan, so the shared morpheme is never token-shared
      -> 2 false-negative pairs (misamban-kabukasan, pisamban-kabukasan).
    - "another" shares no morpheme with kabukasan (different roots) but the
      tokenizer coincidentally emits the same "an" piece for both
      -> 1 false-positive pair.
    """
    index_rows = [
        _row(
            "misamban",
            [("circumfix_prefix", "mi-"), ("root", "samba"), ("circumfix_suffix", "-an")],
        ),
        _row(
            "pisamban",
            [("circumfix_prefix", "pi-"), ("root", "samba"), ("circumfix_suffix", "-an")],
        ),
        _row("sasamba", [("reduplicant", "REDUP(samba)"), ("root", "samba")]),
        _row(
            "kabukasan",
            [("circumfix_prefix", "ka-"), ("root", "bukas"), ("circumfix_suffix", "-an")],
        ),
        _row("another", [("root", "other")]),
    ]
    tokenizer = _FakeTokenizer(
        {
            "misamban": ("mi", "samba", "n"),
            "pisamban": ("pi", "samba", "n"),
            "sasamba": ("sa", "samba"),
            "kabukasan": ("ka", "bukas", "an"),
            "another": ("an", "other"),
        }
    )
    result = v4run._morphological_consistency_f1(tokenizer, index_rows)
    assert result["true_positive_pairs"] == 3
    assert result["false_positive_pairs"] == 1
    assert result["false_negative_pairs"] == 2
    assert result["morphological_consistency_precision"] == 0.75
    assert result["morphological_consistency_recall"] == 0.6
    assert abs(cast(float, result["morphological_consistency_f1"]) - (2 * 0.75 * 0.6 / 1.35)) < 1e-9


def test_morphological_consistency_f1_empty_index_is_zero() -> None:
    tokenizer = _FakeTokenizer({})
    result = v4run._morphological_consistency_f1(tokenizer, [])
    assert result["true_positive_pairs"] == 0
    assert result["morphological_consistency_precision"] == 0.0
    assert result["morphological_consistency_recall"] == 0.0
    assert result["morphological_consistency_f1"] == 0.0


def test_morphological_consistency_f1_ignores_single_character_pieces() -> None:
    """A shared single-character morpheme/token must not create a pair: both
    the minimum morpheme length and minimum token length filters are 2."""
    index_rows = [
        _row("a1", [("clitic", "a")]),
        _row("a2", [("clitic", "a")]),
    ]
    tokenizer = _FakeTokenizer({"a1": ("a", "1"), "a2": ("a", "2")})
    result = v4run._morphological_consistency_f1(tokenizer, index_rows)
    assert result["morpheme_groups"] == 0
    assert result["token_groups"] == 0
    assert result["true_positive_pairs"] == 0


def test_capped_pairs_respects_cap_and_is_deterministic() -> None:
    members = list(range(10))
    pairs = v4run._capped_pairs(members, cap=4)
    assert len(pairs) == 6  # C(4, 2)
    assert pairs == v4run._capped_pairs(members, cap=4)
    for left, right in pairs:
        assert left < 4
        assert right < 4
