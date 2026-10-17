from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def _runner():
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "root_priority_experiment",
        root / "experiments/root_first_morphbpe_v1/run_experiment.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_role_offsets_use_actual_segments_despite_restoration_or_stale_unit_surface():
    runner = _runner()
    analysis = SimpleNamespace(
        token="mamasa",
        segments=("mam", "asa"),
        underlying_units=(
            SimpleNamespace(kind="prefix", surface="mam", underlying="maN-"),
            SimpleNamespace(kind="root", surface="basa", underlying="basa"),
        ),
    )
    lexicon = SimpleNamespace(valid_hosts=frozenset({"basa"}), compounds=frozenset())
    spans = runner.analysis_spans(analysis, lexicon)
    assert [(span["start"], span["end"], span["role"], span["surface"]) for span in spans] == [
        (0, 3, "affix", "mam"),
        (3, 6, "root", "asa"),
    ]
    assert spans[1]["underlying"] == "basa"


def test_uncertain_hosts_and_compounds_are_excluded_without_losing_known_root_host():
    runner = _runner()
    analysis = SimpleNamespace(
        token="abcxyzpq",
        segments=("ab", "cx", "yz", "pq"),
        underlying_units=tuple(
            SimpleNamespace(kind="root_or_compound", surface=surface, underlying=surface)
            for surface in ("ab", "cx", "yz", "pq")
        ),
    )
    lexicon = SimpleNamespace(
        valid_hosts=frozenset({"ab", "yz"}),
        compounds=frozenset({"cx", "yz"}),
    )
    spans = runner.analysis_spans(analysis, lexicon)
    assert [(span["start"], span["end"], span["surface"]) for span in spans] == [(0, 2, "ab")]


def test_infix_order_separates_only_infix_spans_and_preserves_split_root_offsets():
    runner = _runner()
    analysis = SimpleNamespace(
        token="suminulatan",
        segments=("s", "um", "in", "ulat", "an"),
        underlying_units=tuple(
            SimpleNamespace(kind=kind, surface=surface, underlying=underlying)
            for kind, surface, underlying in (
                ("root_fragment", "s", "sulat"),
                ("infix", "um", "-um-"),
                ("infix", "in", "-in-"),
                ("root_fragment", "ulat", "sulat"),
                ("suffix", "an", "-an"),
            )
        ),
    )
    lexicon = SimpleNamespace(valid_hosts=frozenset({"sulat"}), compounds=frozenset())
    old = runner.analysis_spans(analysis, lexicon)
    new = runner.analysis_spans(analysis, lexicon, separate_infixes=True)
    assert [(span["start"], span["end"], span["role"]) for span in new] == [
        (0, 1, "root"), (1, 3, "infix"), (3, 5, "infix"),
        (5, 9, "root"), (9, 11, "affix"),
    ]
    assert [span["role"] for span in old] == ["root", "affix", "affix", "root", "affix"]
    assert [{k: v for k, v in span.items() if k != "role"} for span in old] == [
        {k: v for k, v in span.items() if k != "role"} for span in new
    ]
