from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

_EXPERIMENT_ROOT = Path(__file__).resolve().parent
_REPOSITORY_ROOT = _EXPERIMENT_ROOT.parents[1]
for _extra in (_REPOSITORY_ROOT / "src", _REPOSITORY_ROOT / "runtime"):
    if str(_extra) not in sys.path:
        sys.path.insert(0, str(_extra))

from kapampangan_morphbpe.lexicon import TrainingLexicon  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key, normalize_text  # noqa: E402

"""Isolated, source-enriched Kapampangan morphological analyzer (v4).

This module is entirely separate from ``src/kapampangan_morphbpe/morphology.py``
(the frozen Table 1 baseline) and from ``src/kapampangan_morphbpe/constants.py``.
Neither file is imported for its affix inventory; both are left byte-identical.

Scope and evidence live in ``EVIDENCE.md`` next to this file. Every new rule
below carries a short citation comment pointing at that table. The root/host
inventory is reused unmodified from
``experiments/source_adjudicated_v2/resources/training-lexicon.json`` -- this
module adds affixes and morphophonological processes only, never new roots.

Design summary
---------------

* Every accepted analysis is *lossless*: concatenating ``segments`` always
  reconstructs the normalized input exactly (enforced in
  ``ExpandedSegmentation.__post_init__``).
* Every accepted analysis also carries ``underlying_units``: a parallel list of
  :class:`MorphUnit` values naming the *underlying* morpheme even when it is
  not literally present in the surface (for example the ``-an`` suffix
  surfacing as bare ``-n`` after an ``a``/``e``-final root, or a nasal-final
  consonant deleted by ``maN-``/``paN-`` place assimilation).
* Analysis is recursive/compositional for exactly the two rule families where
  the evidence shows it (the ``paN-`` nominalizer stacking over ``mag-``/``ma-``
  stems, and reduplication wrapping an already-affixed actor stem). Every other
  rule keeps the original architecture's stricter one-level exact-root
  validation.
* Ambiguity is preserved, never silently resolved: when a stage yields more
  than one distinct ``(segments, underlying, rule_id)`` reading, the token is
  marked ``ambiguous`` and left as a single unsplit token, exactly like the
  Table 1 baseline.
"""

MAX_RECURSION_DEPTH = 4

# ---------------------------------------------------------------------------
# New literal (non-reconstructive) affixes. Each entry cites EVIDENCE.md.
# ---------------------------------------------------------------------------

# Evidence: EVIDENCE.md #6 (paki-), #7 (peka-), #8/#9 (maki-/meki-), #10 (makipag-),
# #11 (mi- standalone), #12-#17 (magpa-/magka-/magpaka- and their mig-/meg- aspect twins).
NEW_LITERAL_PREFIXES: tuple[str, ...] = (
    "paki",
    "peka",
    "maki",
    "meki",
    "makipag",
    "mi",
    "magpa",
    "migpa",
    "megpa",
    "magka",
    "migka",
    "megka",
    "magpaka",
    "migpaka",
    "megpaka",
)

# Evidence: EVIDENCE.md #18 (mi-...-an), #19 (pi-...-an), #20 (pag-...-an).
NEW_CIRCUMFIX_PREFIXES: tuple[str, ...] = ("mi", "pi", "pag")

# Evidence: EVIDENCE.md #21 (-en), #22 (-anan).
NEW_SUFFIX_FAMILIES: tuple[str, ...] = ("en", "anan")

# Evidence: EVIDENCE.md #1-#5 (maN- actor prefix, nasal place assimilation).
_DENTAL_ALVEOLAR = "tdns"
_DENTAL_ALVEOLAR_Y = "ds"
_LABIAL = "pbm"
_VELAR = "kgq"


@dataclass(frozen=True, slots=True)
class NasalFamily:
    surface_prefix: str
    restore_classes: str
    rule_tag: str


MAN_FAMILIES: tuple[NasalFamily, ...] = (
    NasalFamily("man", "", "UNCHANGED"),
    NasalFamily("man", _DENTAL_ALVEOLAR, "DENTAL_N_SUBSTITUTION"),
    NasalFamily("many", _DENTAL_ALVEOLAR_Y, "DENTAL_Y_SUBSTITUTION"),
    NasalFamily("mam", _LABIAL, "LABIAL_M_SUBSTITUTION"),
    NasalFamily("mang", _VELAR, "VELAR_NG_SUBSTITUTION"),
    NasalFamily("men", "", "UNCHANGED"),
    NasalFamily("men", _DENTAL_ALVEOLAR, "DENTAL_N_SUBSTITUTION"),
    NasalFamily("meny", _DENTAL_ALVEOLAR_Y, "DENTAL_Y_SUBSTITUTION"),
    NasalFamily("mem", _LABIAL, "LABIAL_M_SUBSTITUTION"),
    NasalFamily("meng", _VELAR, "VELAR_NG_SUBSTITUTION"),
)

# Evidence: EVIDENCE.md #23 (paN- nominalizer, standalone pang-/pam-/pan-/panga-).
PAN_FAMILIES: tuple[NasalFamily, ...] = (
    NasalFamily("pan", _DENTAL_ALVEOLAR, "DENTAL_N_SUBSTITUTION"),
    NasalFamily("pam", _LABIAL, "LABIAL_M_SUBSTITUTION"),
    NasalFamily("pang", _VELAR, "VELAR_NG_SUBSTITUTION"),
    NasalFamily("pang", "", "UNCHANGED"),
    NasalFamily("panga", "", "LITERAL"),
)


@dataclass(frozen=True, slots=True)
class MorphUnit:
    surface: str
    underlying: str
    kind: str

    def to_dict(self) -> dict[str, object]:
        return {"surface": self.surface, "underlying": self.underlying, "kind": self.kind}


@dataclass(frozen=True, slots=True)
class Candidate:
    segments: tuple[str, ...]
    underlying_units: tuple[MorphUnit, ...]
    rule_id: str
    kind: str


@dataclass(frozen=True, slots=True)
class ExpandedSegmentation:
    token: str
    segments: tuple[str, ...]
    protected_boundaries: tuple[int, ...]
    underlying_units: tuple[MorphUnit, ...]
    rule_id: str | None
    kind: str | None
    status: str
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
        if self.underlying_units and len(self.underlying_units) != len(self.segments):
            raise ValueError("underlying units must align with surface segments")

    @property
    def display(self) -> str:
        return " || ".join(self.segments)

    @property
    def underlying_display(self) -> str:
        if not self.underlying_units:
            return self.token
        return " + ".join(unit.underlying for unit in self.underlying_units)

    def to_dict(self) -> dict[str, object]:
        return {
            "token": self.token,
            "segments": list(self.segments),
            "protected_boundaries": list(self.protected_boundaries),
            "underlying_units": [unit.to_dict() for unit in self.underlying_units],
            "underlying_display": self.underlying_display,
            "rule_id": self.rule_id,
            "kind": self.kind,
            "status": self.status,
            "trace": list(self.trace),
            "display": self.display,
        }


def _mark_boundaries(segments: tuple[str, ...]) -> tuple[int, ...]:
    boundaries: list[int] = []
    position = 0
    for segment in segments[:-1]:
        position += len(segment)
        boundaries.append(position)
    return tuple(boundaries)


def _ordered(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values), key=lambda value: (-len(value), value)))


def _rule_fragment(value: str) -> str:
    return value.upper().replace("-", "_")


def _drop_leading_chars_with_units(
    segments: tuple[str, ...], units: tuple[MorphUnit, ...], count: int
) -> tuple[tuple[str, ...], tuple[MorphUnit, ...]] | None:
    """Drop ``count`` leading surface characters from ``segments``, dropping the
    matching whole leading :class:`MorphUnit` entries from ``units`` in lockstep
    whenever a whole segment is fully consumed, so the two stay aligned (a
    nasal-substitution restoration can delete an entire one-character segment,
    e.g. the reduplicant "p" in "p" + "pang" -> "pang" when "pam-" restores a
    deleted "p")."""
    if count == 0:
        return segments, units
    remaining = count
    seg_list = list(segments)
    unit_list = list(units)
    while remaining > 0:
        if not seg_list:
            return None
        if len(seg_list[0]) <= remaining:
            remaining -= len(seg_list[0])
            seg_list.pop(0)
            if unit_list:
                unit_list.pop(0)
        else:
            seg_list[0] = seg_list[0][remaining:]
            remaining = 0
    if not seg_list:
        return None
    return tuple(seg_list), tuple(unit_list)


def _swap_leading_char(segments: tuple[str, ...], new_char: str) -> tuple[str, ...] | None:
    if not segments or not segments[0]:
        return None
    updated = new_char + segments[0][1:]
    return (updated, *segments[1:])


# Minimum reconstructed-root length for every hypothesis-generating mechanism
# this module adds beyond the literal, paper-mandated "-an" match (vowel-hiatus
# collapse, w-insertion, "-en"/"-anan", nasal-place-assimilation restoration,
# and reduplication bases). Stripping only a single trailing "-n" (hiatus) or a
# single leading consonant (nasal substitution) is far more permissive than
# matching a full affix, so it is far more likely to accidentally validate a
# short, low-quality lexicon entry (the corpus-scraped v2 lexicon still
# contains some 1-2 letter "root" rows). This mirrors source_adjudicated_v2's
# own adjudication policy, which explicitly holds "roots shorter than three
# letters" as accident-prone (see its README). The literal "-an" match is left
# unguarded to stay byte-for-byte faithful to the paper-mandated Table 1 rule.
_MIN_RECONSTRUCTED_ROOT_LENGTH = 3


def _an_family_hypotheses(remainder: str, family: str) -> tuple[tuple[str, str, str], ...]:
    """Reconstruct root/suffix hypotheses for the ``-an``/``-en``/``-anan`` family.

    Returns ``(core_surface, surface_suffix, candidate_root)`` triples. Evidence
    for the three allomorphy patterns (literal, vowel-hiatus collapse to a bare
    ``-n``, and ``w``-insertion before ``-i``/``-u``-final roots) is
    EVIDENCE.md #24.
    """
    hypotheses: list[tuple[str, str, str]] = []
    if family in ("an", "en"):
        full = family
        if remainder.endswith(full) and len(remainder) > len(full):
            core = remainder[: -len(full)]
            if core:
                hypotheses.append((core, full, core))
        # Vowel-hiatus collapse: a vowel-final root drops the suffix's own
        # leading vowel, so the surface shows only a bare "-n". Mirikitani
        # pp.569-570 attests "-an" collapsing after BOTH a-final ("basa" ->
        # "basan") and e-final ("albe" -> "alben") roots, so "-an" checks both
        # vowels; "-en" is only ever attested after an e-final root ("lawe" ->
        # "lawen"), so it checks only "e". This can syntactically overlap with
        # the literal "-an"/"-en" match above (e.g. "samban" ends in both "an"
        # and "n"), so both hypotheses are always tried; the lexicon gate keeps
        # only whichever reconstructs a real root. When a root ends in "e",
        # both "-an" and "-en" collapse identically to a bare "-n": that is a
        # genuine, irreducible surface ambiguity this engine preserves rather
        # than silently resolving (see EVIDENCE.md and
        # test_an_en_hiatus_collision_is_preserved_as_ambiguous).
        allowed_hiatus_vowels = ("a", "e") if family == "an" else ("e",)
        if remainder.endswith("n") and len(remainder) > 1:
            core = remainder[:-1]
            if (
                core
                and len(core) >= _MIN_RECONSTRUCTED_ROOT_LENGTH
                and core[-1] in allowed_hiatus_vowels
            ):
                hypotheses.append((core, "n", core))
        wsuffix = "w" + full
        if remainder.endswith(wsuffix) and len(remainder) > len(wsuffix):
            core_surface = remainder[: -len(wsuffix)]
            if core_surface and len(core_surface) + 1 >= _MIN_RECONSTRUCTED_ROOT_LENGTH:
                for final_vowel in ("i", "u"):
                    hypotheses.append((core_surface, wsuffix, core_surface + final_vowel))
    elif family == "anan":
        if (
            remainder.endswith("anan")
            and len(remainder) > 4
            and len(remainder) - 4 >= _MIN_RECONSTRUCTED_ROOT_LENGTH
        ):
            core = remainder[:-4]
            hypotheses.append((core, "anan", core))
        # Same hiatus-collapse reasoning as above, applied to "-anan" -> "-nan".
        if remainder.endswith("nan") and len(remainder) > 3:
            core = remainder[:-3]
            if core and len(core) >= _MIN_RECONSTRUCTED_ROOT_LENGTH and core[-1] in ("a", "e"):
                hypotheses.append((core, "nan", core))
    else:  # pragma: no cover - defensive
        raise ValueError(f"unsupported suffix family: {family}")
    return tuple(hypotheses)


class ExpandedMorphologicalSegmenter:
    def __init__(self, lexicon: TrainingLexicon) -> None:
        self.lexicon = lexicon
        self._cache: dict[str, ExpandedSegmentation] = {}

    # -- host validation -----------------------------------------------

    def _trivial(self, surface: str, kind: str) -> ExpandedSegmentation:
        rule_id = "PROTECT_COMPOUND" if kind == "compound" else "PROTECT_ROOT"
        status = "protected_compound" if kind == "compound" else "protected_root"
        return ExpandedSegmentation(
            surface,
            (surface,),
            (),
            (MorphUnit(surface, surface, kind),),
            rule_id,
            kind,
            status,
            ("normalize:nfc", f"protect:{kind}"),
        )

    def _valid_host_analysis(
        self, surface: str, depth: int, *, allow_recursive: bool
    ) -> ExpandedSegmentation | None:
        if not surface:
            return None
        key = comparison_key(surface)
        if key in self.lexicon.compounds:
            return self._trivial(surface, "compound")
        if key in self.lexicon.valid_hosts:
            return self._trivial(surface, "root")
        if allow_recursive and depth > 0:
            result = self._analyze(surface, depth - 1)
            if result.status in ("accepted", "protected_root", "protected_compound"):
                return result
        return None

    # -- stage: reduplication -------------------------------------------

    def _try_reduplication(self, token: str, lower: str, depth: int) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        # CV-/V-reduplication for continuing/progressive aspect. Evidence: EVIDENCE.md #25.
        for redup_len in (2, 1):
            if len(token) <= redup_len * 2:
                continue
            redup = token[:redup_len]
            rest = token[redup_len:]
            # Pattern detection uses the lowercase comparison strings so a
            # title-cased word ("Daratang": redup "Da", rest "ratang") still
            # matches even though the reduplicant and the base copy differ in
            # case; the actual hypotheses below keep slicing from `redup`/
            # `rest` so the original casing is preserved in the output.
            redup_lower = lower[:redup_len]
            rest_lower = lower[redup_len:]
            base_hypotheses: list[tuple[str, str]] = []
            if rest_lower.startswith(redup_lower):
                base_hypotheses.append((rest, "identity"))
            if (
                redup_len >= 1
                and redup_lower[0] == "d"
                and rest_lower[:1] == "r"
                and rest_lower[1:redup_len] == redup_lower[1:]
            ):
                base_hypotheses.append((redup[0] + rest[1:], "d_to_r_medial"))
            for base_literal, alternation in base_hypotheses:
                if len(base_literal) < _MIN_RECONSTRUCTED_ROOT_LENGTH:
                    continue
                sub = self._valid_host_analysis(base_literal, depth, allow_recursive=True)
                if sub is None:
                    continue
                if alternation == "identity":
                    rest_segments: tuple[str, ...] | None = sub.segments
                else:
                    rest_segments = _swap_leading_char(sub.segments, rest[0])
                if rest_segments is None or "".join(rest_segments) != rest:
                    continue
                surface_segments = (redup, *rest_segments)
                base_label = (
                    sub.underlying_units[0].underlying if sub.underlying_units else base_literal
                )
                underlying_units = (
                    MorphUnit(redup, f"REDUP({base_label})", "reduplicant"),
                    *sub.underlying_units,
                )
                tag = "CV_REDUPLICATION" if redup_len == 2 else "V_REDUPLICATION"
                candidates.append(
                    Candidate(surface_segments, underlying_units, f"REDUP_{tag}", "reduplication")
                )
        # ka- + full-root reduplication for the recent-completive aspect.
        # Evidence: EVIDENCE.md #26.
        if lower.startswith("ka") and len(token) > 2:
            rest = token[2:]
            if rest and len(rest) % 2 == 0:
                half = len(rest) // 2
                first, second = rest[:half], rest[half:]
                # Recent-completive ka- reduplicates the *whole* root. Forman
                # p.91 shows the medial d->r alternation applying to BOTH
                # copies (karatangratang, not karatangdatang), so the root
                # reconstruction reverts a shared leading "r" back to "d"
                # rather than reading it directly off one copy.
                root_hypotheses: list[str] = []
                if first == second:
                    root_hypotheses.append(first)
                    if first and first[0] == "r":
                        root_hypotheses.append("d" + first[1:])
                for root_literal in dict.fromkeys(root_hypotheses):
                    if len(root_literal) < _MIN_RECONSTRUCTED_ROOT_LENGTH:
                        continue
                    sub = self._valid_host_analysis(root_literal, depth, allow_recursive=False)
                    if sub is None or sub.segments != (root_literal,):
                        continue
                    surface_segments = (token[:2], first, second)
                    underlying_units = (
                        MorphUnit(token[:2], "ka-", "prefix"),
                        MorphUnit(first, root_literal, "root"),
                        MorphUnit(second, f"REDUP({root_literal})", "reduplicant"),
                    )
                    candidates.append(
                        Candidate(
                            surface_segments,
                            underlying_units,
                            "PREFIX_KA_FULL_REDUPLICATION",
                            "reduplication",
                        )
                    )
        return tuple(candidates)

    # -- stage: circumfix -------------------------------------------------

    def _try_circumfix(self, token: str, lower: str, depth: int) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        pairs: list[tuple[str, str, str]] = [
            ("ka", "an", "KA"),
            ("pa", "an", "PA"),
            ("pang", "an", "PANG"),
            ("pam", "an", "PANG_PAM"),
            ("pan", "an", "PANG_PAN"),
            ("panga", "an", "PANG_PANGA"),
            ("mi", "an", "MI"),  # Evidence: EVIDENCE.md #18
            ("pi", "an", "PI"),  # Evidence: EVIDENCE.md #19
            ("pag", "an", "PAG"),  # Evidence: EVIDENCE.md #20
        ]
        for prefix, family, rule_name in pairs:
            if not lower.startswith(prefix):
                continue
            remainder = token[len(prefix) :]
            remainder_lower = lower[len(prefix) :]
            # Hypotheses are discovered against the lowercase comparison string
            # (endswith/startswith on the raw mixed-case token would silently
            # fail to match, e.g. "ARAPAN".endswith("an") is False), then
            # re-sliced from the original-case `remainder` so casing survives.
            for core_lower, _suffix_lower, candidate_root in _an_family_hypotheses(
                remainder_lower, family
            ):
                core = remainder[: len(core_lower)]
                surface_suffix = remainder[len(core_lower) :]
                if not self._is_valid_host(candidate_root):
                    continue
                candidate_root_display = core + candidate_root[len(core_lower) :]
                surface_segments = (token[: len(prefix)], core, surface_suffix)
                underlying_units = (
                    MorphUnit(token[: len(prefix)], f"{prefix}-", "circumfix_prefix"),
                    MorphUnit(core, candidate_root_display, "root"),
                    MorphUnit(surface_suffix, "-an", "circumfix_suffix"),
                )
                candidates.append(
                    Candidate(
                        surface_segments,
                        underlying_units,
                        f"CIRCUMFIX_{rule_name}_AN",
                        "circumfix",
                    )
                )
        return tuple(candidates)

    def _is_valid_host(self, surface: str) -> bool:
        return bool(surface) and comparison_key(surface) in self.lexicon.valid_hosts

    # -- stage: prefix ------------------------------------------------------

    # Evidence: EVIDENCE.md #0 (paper-mandated Table 1 baseline, reproduced here
    # unmodified so the expanded stage list can run in one pass).
    _BASELINE_PREFIXES: tuple[str, ...] = (
        "ma",
        "me",
        "pa",
        "maka",
        "ka",
        "mag",
        "meg",
        "mang",
        "meng",
        "i",
        "ipa",
        "makapag",
        "mig",
        "meka",
        "mekapag",
    )

    def _try_prefix(self, token: str, lower: str, depth: int) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        for prefix in _ordered(self._BASELINE_PREFIXES + NEW_LITERAL_PREFIXES):
            if not lower.startswith(prefix) or len(token) <= len(prefix):
                continue
            remainder = token[len(prefix) :]
            if self._is_valid_host(remainder):
                candidates.append(
                    Candidate(
                        (token[: len(prefix)], remainder),
                        (
                            MorphUnit(token[: len(prefix)], f"{prefix}-", "prefix"),
                            MorphUnit(remainder, remainder, "root"),
                        ),
                        f"PREFIX_{_rule_fragment(prefix)}",
                        "prefix",
                    )
                )
        # standalone "m-" -- Evidence: EVIDENCE.md #1.
        if lower.startswith("m") and len(token) > 1:
            remainder = token[1:]
            if self._is_valid_host(remainder):
                candidates.append(
                    Candidate(
                        (token[:1], remainder),
                        (
                            MorphUnit(token[:1], "m-", "prefix"),
                            MorphUnit(remainder, remainder, "root"),
                        ),
                        "PREFIX_M_BARE",
                        "prefix",
                    )
                )
        candidates.extend(
            self._nasal_family_candidates(
                token, lower, depth, prefix_label="MAN", families=MAN_FAMILIES, recursive=False
            )
        )
        candidates.extend(
            self._nasal_family_candidates(
                token, lower, depth, prefix_label="PAN", families=PAN_FAMILIES, recursive=True
            )
        )
        return tuple(candidates)

    def _nasal_family_candidates(
        self,
        token: str,
        lower: str,
        depth: int,
        *,
        prefix_label: str,
        families: tuple[NasalFamily, ...],
        recursive: bool,
    ) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        underlying_label = {"MAN": "maN-", "PAN": "paN-"}[prefix_label]
        ordered_families = sorted(
            families, key=lambda item: (-len(item.surface_prefix), item.surface_prefix)
        )
        for family in ordered_families:
            if not lower.startswith(family.surface_prefix):
                continue
            remainder = token[len(family.surface_prefix) :]
            if not remainder:
                continue
            restorations = [""] if not family.restore_classes else list(family.restore_classes)
            seen_roots: set[str] = set()
            for restore_char in restorations:
                candidate_root = restore_char + remainder
                if candidate_root in seen_roots:
                    continue
                seen_roots.add(candidate_root)
                if len(candidate_root) < _MIN_RECONSTRUCTED_ROOT_LENGTH:
                    continue
                sub = self._valid_host_analysis(candidate_root, depth, allow_recursive=recursive)
                if sub is None:
                    continue
                trimmed_pair = _drop_leading_chars_with_units(
                    sub.segments, sub.underlying_units, len(restore_char)
                )
                if trimmed_pair is None:
                    continue
                trimmed_segments, trimmed_units = trimmed_pair
                if "".join(trimmed_segments) != remainder:
                    continue
                surface_segments = (token[: len(family.surface_prefix)], *trimmed_segments)
                underlying_units = (
                    MorphUnit(token[: len(family.surface_prefix)], underlying_label, "prefix"),
                    *trimmed_units,
                )
                rule_id = (
                    f"PREFIX_{prefix_label}_{_rule_fragment(family.surface_prefix)}_"
                    f"{family.rule_tag}"
                )
                candidates.append(Candidate(surface_segments, underlying_units, rule_id, "prefix"))
        return tuple(candidates)

    # -- stage: infix (paper-mandated baseline, unmodified) -----------------

    _INFIXES: tuple[str, ...] = ("in", "um")

    def _try_infix(self, token: str, lower: str) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        for infix in _ordered(self._INFIXES):
            position = 1
            if (
                len(token) <= position + len(infix)
                or lower[position : position + len(infix)] != infix
            ):
                continue
            reconstructed = token[:position] + token[position + len(infix) :]
            if self._is_valid_host(reconstructed):
                left, mid, right = (
                    token[:position],
                    token[position : position + len(infix)],
                    token[position + len(infix) :],
                )
                candidates.append(
                    Candidate(
                        (left, mid, right),
                        (
                            MorphUnit(left, left, "root_fragment"),
                            MorphUnit(mid, f"-{infix}-", "infix"),
                            MorphUnit(right, right, "root_fragment"),
                        ),
                        f"INFIX_{_rule_fragment(infix)}",
                        "infix",
                    )
                )
        return tuple(candidates)

    # -- stage: suffix --------------------------------------------------

    def _try_suffix(self, token: str, lower: str) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        for family in ("an", *NEW_SUFFIX_FAMILIES):
            # See the matching comment in _try_circumfix: hypotheses are
            # discovered against `lower`, then re-sliced from `token` so
            # ALL-CAPS/Title-Case surfaces keep their original casing.
            for core_lower, _suffix_lower, candidate_root in _an_family_hypotheses(lower, family):
                core = token[: len(core_lower)]
                surface_suffix = token[len(core_lower) :]
                if not self._is_valid_host(candidate_root):
                    continue
                candidate_root_display = core + candidate_root[len(core_lower) :]
                candidates.append(
                    Candidate(
                        (core, surface_suffix),
                        (
                            MorphUnit(core, candidate_root_display, "root"),
                            MorphUnit(surface_suffix, f"-{family}", "suffix"),
                        ),
                        f"SUFFIX_{_rule_fragment(family)}",
                        "suffix",
                    )
                )
        return tuple(candidates)

    # -- stage: clitic (paper-mandated baseline, unmodified) -----------------

    _CLITICS: tuple[str, ...] = ("na", "pa", "mu", "ku", "ya", "la", "ra", "ne", "no")

    def _try_clitic(self, token: str, lower: str) -> tuple[Candidate, ...]:
        candidates: list[Candidate] = []
        valid_clitic_hosts = self.lexicon.valid_hosts | self.lexicon.compounds
        for clitic in _ordered(self._CLITICS):
            if not lower.endswith(clitic) or len(token) <= len(clitic):
                continue
            host = token[: len(token) - len(clitic)]
            if comparison_key(host) in valid_clitic_hosts:
                candidates.append(
                    Candidate(
                        (host, token[len(token) - len(clitic) :]),
                        (
                            MorphUnit(host, host, "root_or_compound"),
                            MorphUnit(token[len(token) - len(clitic) :], f"={clitic}", "clitic"),
                        ),
                        f"CLITIC_{_rule_fragment(clitic)}",
                        "clitic",
                    )
                )
        return tuple(candidates)

    # -- resolution -------------------------------------------------------

    def _resolve(
        self, token: str, stage: str, candidates: tuple[Candidate, ...]
    ) -> ExpandedSegmentation | None:
        if not candidates:
            return None
        distinct = sorted(
            {
                (
                    candidate.segments,
                    tuple(unit.underlying for unit in candidate.underlying_units),
                    candidate.rule_id,
                    candidate.kind,
                    candidate.underlying_units,
                )
                for candidate in candidates
            },
            key=lambda value: (value[0], value[1], value[2], value[3]),
        )
        if len(distinct) > 1:
            rule_ids = "|".join(sorted({value[2] for value in distinct}))
            return ExpandedSegmentation(
                token,
                (token,),
                (),
                (),
                None,
                stage,
                "ambiguous",
                ("normalize:nfc", f"stage:{stage}", f"ambiguous:{rule_ids}"),
            )
        segments, _underlying_labels, rule_id, kind, underlying_units = distinct[0]
        return ExpandedSegmentation(
            token,
            segments,
            _mark_boundaries(segments),
            underlying_units,
            rule_id,
            kind,
            "accepted",
            ("normalize:nfc", f"stage:{stage}", f"accept:{rule_id}"),
        )

    # -- entry points -------------------------------------------------------

    def _analyze(self, token: str, depth: int) -> ExpandedSegmentation:
        cache_key = f"{depth}:{token}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        key = comparison_key(token)
        if key in self.lexicon.compounds:
            result = self._trivial(token, "compound")
        elif key in self.lexicon.valid_hosts:
            result = self._trivial(token, "root")
        else:
            result = None
            for stage, stage_candidates in (
                ("circumfix", self._try_circumfix(token, key, depth)),
                ("prefix", self._try_prefix(token, key, depth)),
                ("reduplication", self._try_reduplication(token, key, depth)),
                ("infix", self._try_infix(token, key)),
                ("suffix", self._try_suffix(token, key)),
                ("clitic", self._try_clitic(token, key)),
            ):
                resolved = self._resolve(token, stage, stage_candidates)
                if resolved is not None:
                    result = resolved
                    break
            if result is None:
                result = ExpandedSegmentation(
                    token,
                    (token,),
                    (),
                    (MorphUnit(token, token, "unchanged"),),
                    None,
                    None,
                    "unchanged",
                    ("normalize:nfc", "unchanged:no_valid_analysis"),
                )
        assert result is not None
        self._cache[cache_key] = result
        return result

    def segment(self, token: str) -> ExpandedSegmentation:
        normalized = normalize_text(token)
        if not normalized:
            return ExpandedSegmentation(
                "", (), (), (), None, None, "empty", ("normalize:nfc", "empty")
            )
        return self._analyze(normalized, MAX_RECURSION_DEPTH)

    def segment_many(self, tokens: list[str]) -> list[ExpandedSegmentation]:
        return [self.segment(token) for token in tokens]
