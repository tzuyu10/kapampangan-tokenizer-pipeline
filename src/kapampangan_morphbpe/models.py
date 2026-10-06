from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PretokenKind = Literal["word", "whitespace", "punctuation", "symbol"]
SegmentationStatus = Literal[
    "empty",
    "protected_compound",
    "protected_root",
    "accepted",
    "ambiguous",
    "unchanged",
]


@dataclass(frozen=True, slots=True)
class Pretoken:
    surface: str
    start: int
    end: int
    kind: PretokenKind

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < self.start:
            raise ValueError("invalid pretoken offsets")
        if self.end - self.start != len(self.surface):
            raise ValueError("pretoken offsets must use normalized code-point indices")


@dataclass(frozen=True, slots=True)
class Segmentation:
    token: str
    segments: tuple[str, ...]
    protected_boundaries: tuple[int, ...]
    rule_id: str | None
    kind: str | None
    status: SegmentationStatus
    trace: tuple[str, ...]

    def __post_init__(self) -> None:
        if "" in self.segments:
            raise ValueError("segmentation may not contain an empty segment")
        if "".join(self.segments) != self.token:
            raise ValueError("segmentation must reconstruct its token")
        expected: list[int] = []
        position = 0
        for segment in self.segments[:-1]:
            position += len(segment)
            expected.append(position)
        if tuple(expected) != self.protected_boundaries:
            raise ValueError("protected boundaries do not match segments")

    @property
    def display(self) -> str:
        return " || ".join(self.segments)

    def to_dict(self) -> dict[str, object]:
        return {
            "token": self.token,
            "segments": list(self.segments),
            "protected_boundaries": list(self.protected_boundaries),
            "rule_id": self.rule_id,
            "kind": self.kind,
            "status": self.status,
            "trace": list(self.trace),
            "display": self.display,
        }


@dataclass(frozen=True, slots=True)
class PreparedSequence:
    surface: str
    protected_boundaries: tuple[int, ...]
    kind: PretokenKind
    frequency: int

    def __post_init__(self) -> None:
        if not self.surface:
            raise ValueError("prepared sequence surface may not be empty")
        if self.frequency <= 0:
            raise ValueError("prepared sequence frequency must be positive")
        if any(value <= 0 or value >= len(self.surface) for value in self.protected_boundaries):
            raise ValueError("protected boundary outside sequence")
        if tuple(sorted(set(self.protected_boundaries))) != self.protected_boundaries:
            raise ValueError("protected boundaries must be sorted and unique")


@dataclass(frozen=True, slots=True)
class CorpusRecord:
    identifier: str
    text: str


@dataclass(frozen=True, slots=True)
class ReferenceRecord:
    identifier: str
    form: str
    kind: str
    description: str
    example: str
    source: str
