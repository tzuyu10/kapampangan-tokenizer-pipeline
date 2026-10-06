from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import CLITICS, INFIXES, PANG_VARIANTS, PREFIXES, SUFFIXES
from .lexicon import TrainingLexicon, load_lexicon
from .models import Segmentation
from .normalization import comparison_key, normalize_text


@dataclass(frozen=True, slots=True)
class Candidate:
    segments: tuple[str, ...]
    rule_id: str
    kind: str


def _ordered(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(values, key=lambda value: (-len(value), value)))


def _rule_fragment(value: str) -> str:
    return value.upper().replace("-", "_")


def _valid_host(segmenter: MorphologicalSegmenter, surface: str) -> bool:
    return bool(surface) and comparison_key(surface) in segmenter.lexicon.valid_hosts


def try_circumfix(segmenter: MorphologicalSegmenter, token: str) -> tuple[Candidate, ...]:
    lower = comparison_key(token)
    pairs = [
        ("ka", "an", "KA"),
        ("pa", "an", "PA"),
        ("pang", "an", "PANG"),
        *((variant, "an", f"PANG_{_rule_fragment(variant)}") for variant in PANG_VARIANTS),
    ]
    pairs.sort(key=lambda item: (-len(item[0]), item[0], item[2]))
    candidates: list[Candidate] = []
    for prefix, suffix, rule_name in pairs:
        if not lower.startswith(prefix) or not lower.endswith(suffix):
            continue
        if len(token) <= len(prefix) + len(suffix):
            continue
        core = token[len(prefix) : len(token) - len(suffix)]
        if _valid_host(segmenter, core):
            candidates.append(
                Candidate(
                    (token[: len(prefix)], core, token[len(token) - len(suffix) :]),
                    f"CIRCUMFIX_{rule_name}_AN",
                    "circumfix",
                )
            )
    return tuple(candidates)


def try_prefix(segmenter: MorphologicalSegmenter, token: str) -> tuple[Candidate, ...]:
    lower = comparison_key(token)
    candidates: list[Candidate] = []
    for prefix in _ordered(PREFIXES):
        if not lower.startswith(prefix) or len(token) <= len(prefix):
            continue
        remainder = token[len(prefix) :]
        if _valid_host(segmenter, remainder):
            candidates.append(
                Candidate(
                    (token[: len(prefix)], remainder),
                    f"PREFIX_{_rule_fragment(prefix)}",
                    "prefix",
                )
            )
    return tuple(candidates)


def try_infix(segmenter: MorphologicalSegmenter, token: str) -> tuple[Candidate, ...]:
    lower = comparison_key(token)
    candidates: list[Candidate] = []
    for infix in _ordered(INFIXES):
        position = 1
        if len(token) <= position + len(infix) or lower[position : position + len(infix)] != infix:
            continue
        reconstructed = token[:position] + token[position + len(infix) :]
        if _valid_host(segmenter, reconstructed):
            candidates.append(
                Candidate(
                    (
                        token[:position],
                        token[position : position + len(infix)],
                        token[position + len(infix) :],
                    ),
                    f"INFIX_{_rule_fragment(infix)}",
                    "infix",
                )
            )
    return tuple(candidates)


def try_suffix(segmenter: MorphologicalSegmenter, token: str) -> tuple[Candidate, ...]:
    lower = comparison_key(token)
    candidates: list[Candidate] = []
    for suffix in _ordered(SUFFIXES):
        if not lower.endswith(suffix) or len(token) <= len(suffix):
            continue
        remainder = token[: len(token) - len(suffix)]
        if _valid_host(segmenter, remainder):
            candidates.append(
                Candidate(
                    (remainder, token[len(token) - len(suffix) :]),
                    f"SUFFIX_{_rule_fragment(suffix)}",
                    "suffix",
                )
            )
    return tuple(candidates)


def try_clitic(segmenter: MorphologicalSegmenter, token: str) -> tuple[Candidate, ...]:
    lower = comparison_key(token)
    candidates: list[Candidate] = []
    valid_clitic_hosts = segmenter.lexicon.valid_hosts | segmenter.lexicon.compounds
    for clitic in _ordered(CLITICS):
        if not lower.endswith(clitic) or len(token) <= len(clitic):
            continue
        host = token[: len(token) - len(clitic)]
        if comparison_key(host) in valid_clitic_hosts:
            candidates.append(
                Candidate(
                    (host, token[len(token) - len(clitic) :]),
                    f"CLITIC_{_rule_fragment(clitic)}",
                    "clitic",
                )
            )
    return tuple(candidates)


def mark_boundaries(segments: tuple[str, ...]) -> tuple[int, ...]:
    boundaries: list[int] = []
    position = 0
    for segment in segments[:-1]:
        position += len(segment)
        boundaries.append(position)
    return tuple(boundaries)


class MorphologicalSegmenter:
    def __init__(self, lexicon: TrainingLexicon) -> None:
        self.lexicon = lexicon

    @classmethod
    def from_path(cls, path: Path) -> MorphologicalSegmenter:
        return cls(load_lexicon(path))

    def _resolve(
        self, token: str, stage: str, candidates: tuple[Candidate, ...]
    ) -> Segmentation | None:
        if not candidates:
            return None
        distinct = sorted(
            {(candidate.segments, candidate.rule_id, candidate.kind) for candidate in candidates},
            key=lambda value: (value[0], value[1], value[2]),
        )
        if len(distinct) > 1:
            rule_ids = "|".join(value[1] for value in distinct)
            return Segmentation(
                token,
                (token,),
                (),
                None,
                stage,
                "ambiguous",
                ("normalize:nfc", f"stage:{stage}", f"ambiguous:{rule_ids}"),
            )
        segments, rule_id, kind = distinct[0]
        return Segmentation(
            token,
            segments,
            mark_boundaries(segments),
            rule_id,
            kind,
            "accepted",
            ("normalize:nfc", f"stage:{stage}", f"accept:{rule_id}"),
        )

    def segment(self, token: str) -> Segmentation:
        normalized = normalize_text(token)
        if not normalized:
            return Segmentation("", (), (), None, None, "empty", ("normalize:nfc", "empty"))
        key = comparison_key(normalized)
        if key in self.lexicon.compounds:
            return Segmentation(
                normalized,
                (normalized,),
                (),
                "PROTECT_COMPOUND",
                "compound",
                "protected_compound",
                ("normalize:nfc", "protect:compound"),
            )
        if key in self.lexicon.valid_hosts:
            return Segmentation(
                normalized,
                (normalized,),
                (),
                "PROTECT_ROOT",
                "root",
                "protected_root",
                ("normalize:nfc", "protect:root"),
            )
        for stage, function in (
            ("circumfix", try_circumfix),
            ("prefix", try_prefix),
            ("infix", try_infix),
            ("suffix", try_suffix),
            ("clitic", try_clitic),
        ):
            result = self._resolve(normalized, stage, function(self, normalized))
            if result is not None:
                return result
        return Segmentation(
            normalized,
            (normalized,),
            (),
            None,
            None,
            "unchanged",
            ("normalize:nfc", "unchanged:no_valid_analysis"),
        )

    def segment_many(self, tokens: list[str]) -> list[Segmentation]:
        return [self.segment(token) for token in tokens]
