from __future__ import annotations

from collections.abc import Callable
from importlib import import_module
from typing import Protocol, cast

from .lexicon import TrainingLexicon
from .models import Segmentation, SegmentationStatus
from .normalization import normalize_text

RustOutput = tuple[
    str,
    list[str],
    list[int],
    str | None,
    str | None,
    str,
    list[str],
]


class RustBackend(Protocol):
    def segment(self, token: str) -> RustOutput: ...

    def segment_batch(self, tokens: list[str]) -> list[RustOutput]: ...


class RustMorphologicalSegmenter:
    def __init__(self, lexicon: TrainingLexicon) -> None:
        module = import_module("kapampangan_morphbpe._rust_segmenter")
        factory = cast(Callable[[list[str], list[str], list[str]], RustBackend], module.Segmenter)
        self._backend = factory(
            sorted(lexicon.roots),
            sorted(lexicon.compounds),
            sorted(lexicon.variants),
        )

    @staticmethod
    def _convert(output: RustOutput) -> Segmentation:
        token, segments, boundaries, rule_id, kind, status, trace = output
        valid_statuses: set[str] = {
            "empty",
            "protected_compound",
            "protected_root",
            "accepted",
            "ambiguous",
            "unchanged",
        }
        if status not in valid_statuses:
            raise ValueError(f"Rust segmenter returned invalid status: {status}")
        return Segmentation(
            token=token,
            segments=tuple(segments),
            protected_boundaries=tuple(boundaries),
            rule_id=rule_id,
            kind=kind,
            status=cast(SegmentationStatus, status),
            trace=tuple(trace),
        )

    def segment(self, token: str) -> Segmentation:
        return self._convert(self._backend.segment(normalize_text(token)))

    def segment_many(self, tokens: list[str]) -> list[Segmentation]:
        normalized = [normalize_text(token) for token in tokens]
        outputs = self._backend.segment_batch(normalized)
        if len(outputs) != len(normalized):
            raise RuntimeError("Rust segmenter changed batch cardinality")
        return [self._convert(output) for output in outputs]
