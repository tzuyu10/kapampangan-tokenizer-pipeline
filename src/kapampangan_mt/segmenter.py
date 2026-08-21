"""Morphological Segmentation component (thesis p. 38-41, Figure 7).

Two modes:

``strict_thesis_mode=True``
    A literal transcription of the Figure 7 pseudocode: one affix layer,
    remainder must be a lexicon root/variant, no allomorph resolution, no
    reduplication.  Use this to reproduce exactly what the proposal describes.

``strict_thesis_mode=False``  (default, recommended)
    The same rule order, plus four documented repairs:
      R1  affixes tried longest-first (Lexicon.finalize)
      R2  allomorph table (pang- ~ pam- ~ pan- ~ panga-) so a surface prefix
          that is not literally in the lexicon still resolves
      R3  recursive peeling up to ``max_depth`` so stacked affixation
          (mag-pa-ROOT-an) is analysable
      R4  optional CV/CVC reduplication
    Every repair is justified in docs/THESIS_ISSUES.md.

The output is a list of :class:`Morph` whose ``surface`` fields concatenate
back to the input token, so boundary offsets are always well defined.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from .lexicon import Lexicon
from .normalize import Normalizer

VOWELS = set("aeiou")
BOUNDARY_MARK = " || "  # MARK_BOUNDARIES, Figure 7


@dataclass(frozen=True)
class Morph:
    surface: str
    label: str
    kind: str  # root|prefix|infix|suffix|clitic|redup|unknown


@dataclass
class Segmentation:
    token: str
    morphs: list[Morph]
    analyzed: bool
    rule: str = "fallback"

    @property
    def surfaces(self) -> list[str]:
        return [m.surface for m in self.morphs]

    @property
    def labels(self) -> list[str]:
        """Canonical morpheme labels — the unit used by Morphological Consistency F1."""
        return [m.label for m in self.morphs]

    @property
    def boundaries(self) -> set[int]:
        """Internal character offsets where a morpheme boundary falls.

        Word-initial (0) and word-final (len) positions are excluded because
        they are not predictions — every tokenizer gets them for free.
        """
        out, pos = set(), 0
        for m in self.morphs[:-1]:
            pos += len(m.surface)
            out.add(pos)
        return out

    def marked(self, sep: str = BOUNDARY_MARK) -> str:
        """MARK_BOUNDARIES(segments) from Figure 7."""
        return sep.join(self.surfaces) if len(self.morphs) > 1 else self.token

    def __str__(self) -> str:  # pragma: no cover
        return "+".join(f"{m.surface}[{m.kind}]" for m in self.morphs)


@dataclass
class SegmenterConfig:
    strict_thesis_mode: bool = False
    max_depth: int = 3
    enable_clitics: bool = True
    enable_reduplication: bool = True
    clitic_match: str = "suffix"      # "suffix" | "contains" (thesis literal)
    min_remainder_len: int = 2
    max_infix_onset: int = 2          # infix may sit after 1 or 2 onset consonants
    enable_vowel_restoration: bool = True  # basa + -an -> basan (stem-final vowel elides)


class MorphologicalSegmenter:
    """SEGMENT_TRAINING_TOKEN(token, LEXICON)."""

    def __init__(
        self,
        lexicon: Lexicon,
        normalizer: Normalizer | None = None,
        config: SegmenterConfig | None = None,
    ) -> None:
        self.lex = lexicon
        self.norm = normalizer or Normalizer()
        self.cfg = config or SegmenterConfig()
        self._cache: dict[str, Segmentation] = {}

    # ================================================================== #
    # public API
    # ================================================================== #
    def segment(self, token: str) -> Segmentation:
        token = self.norm.normalize_token(token)
        if not token:
            return Segmentation("", [], False, "empty")
        if token in self._cache:
            return self._cache[token]
        seg = self._segment(token, depth=0)
        self._cache[token] = seg
        return seg

    def segment_sentence(self, sentence: str) -> list[Segmentation]:
        from .pretokenize import pre_tokenize

        out = []
        for pt in pre_tokenize(self.norm.normalize_text(sentence)):
            if pt.kind == "word":
                out.append(self.segment(pt.surface))
            else:
                out.append(
                    Segmentation(pt.surface, [Morph(pt.surface, pt.surface, "unknown")],
                                 False, pt.kind)
                )
        return out

    def coverage(self, tokens: list[str]) -> float:
        """Fraction of word types the segmenter can actually analyse.

        Report this in Chapter 4: it is the ceiling on Morpheme Boundary F1
        for the proposed tokenizer, and it is entirely determined by lexicon
        coverage, not by the algorithm.
        """
        if not tokens:
            return 0.0
        return sum(self.segment(t).analyzed for t in set(tokens)) / len(set(tokens))

    # ================================================================== #
    # internals — Figure 7 order
    # ================================================================== #
    def _segment(self, token: str, depth: int) -> Segmentation:
        # 1. compounds
        if token in self.lex.compounds:
            parts = self.lex.compounds[token]
            return Segmentation(
                token, [Morph(p, self.lex.canonical_root(p), "root") for p in parts],
                True, "compound",
            )
        # 2. bare root (or known spelling variant of one)
        if self.lex.is_root(token):
            return Segmentation(
                token, [Morph(token, self.lex.canonical_root(token), "root")],
                True, "root",
            )

        for name, fn in (
            ("circumfix", self._try_circumfix),
            ("prefix", self._try_prefix),
            ("infix", self._try_infix),
            ("suffix", self._try_suffix),
            ("reduplication", self._try_reduplication),
            ("clitic", self._try_clitic),
        ):
            if name == "reduplication" and not self.cfg.enable_reduplication:
                continue
            if name == "reduplication" and self.cfg.strict_thesis_mode:
                continue
            if name == "clitic" and not self.cfg.enable_clitics:
                continue
            cand = fn(token, depth)
            if cand is not None:
                cand.rule = name
                return cand

        # 3. fallback: return the token unanalysed
        return Segmentation(token, [Morph(token, token, "unknown")], False, "fallback")

    # ------------------------------------------------------------------ #
    def _resolve_stem(self, stem: str, depth: int) -> list[Morph] | None:
        """Validity test for what remains after stripping an affix.

        Strict mode  : stem must literally be in ROOTS or VARIANTS (Figure 7).
        Default mode : stem may itself be analysable (recursive peeling, R3).
        """
        if len(stem) < self.cfg.min_remainder_len:
            return None
        if self.lex.is_root(stem):
            return [Morph(stem, self.lex.canonical_root(stem), "root")]
        if self.cfg.strict_thesis_mode:
            return None
        # R5: stem-final vowel elision before a vowel-initial suffix
        # (basa + -an -> basan). Surface stays "bas" so offsets still line up;
        # the *label* is restored to the canonical root so MCF1 links basan to basa.
        if self.cfg.enable_vowel_restoration:
            for v in "aeiou":
                if self.lex.is_root(stem + v):
                    return [Morph(stem, self.lex.canonical_root(stem + v), "root")]
        if depth + 1 >= self.cfg.max_depth:
            return None
        inner = self._segment(stem, depth + 1)
        return inner.morphs if inner.analyzed else None

    def _affix_label(self, surface: str, kind: str) -> str:
        if self.cfg.strict_thesis_mode:
            return surface
        return self.lex.canonical_morpheme(surface, kind)

    # ------------------------- TRY_CIRCUMFIX --------------------------- #
    def _try_circumfix(self, token: str, depth: int) -> Segmentation | None:
        for pre, suf in self.lex.circumfixes:
            if len(token) <= len(pre) + len(suf):
                continue
            if token.startswith(pre) and token.endswith(suf):
                core = token[len(pre) : len(token) - len(suf)]
                stem = self._resolve_stem(core, depth)
                if stem is not None:
                    return Segmentation(
                        token,
                        [Morph(pre, self._affix_label(pre, "prefix"), "prefix"), *stem,
                         Morph(suf, self._affix_label(suf, "suffix"), "suffix")],
                        True,
                    )
        return None

    # --------------------------- TRY_PREFIX ---------------------------- #
    def _try_prefix(self, token: str, depth: int) -> Segmentation | None:
        for pre in self.lex.prefixes:
            if not token.startswith(pre) or len(token) <= len(pre):
                continue
            stem = self._resolve_stem(token[len(pre) :], depth)
            if stem is not None:
                return Segmentation(
                    token,
                    [Morph(pre, self._affix_label(pre, "prefix"), "prefix"), *stem],
                    True,
                )
        return None

    # ---------------------------- TRY_INFIX ---------------------------- #
    def _try_infix(self, token: str, depth: int) -> Segmentation | None:
        """Kapampangan infixes -in-/-um- sit after the root-initial consonant.

        ``kan`` ('eat') -> ``k-in-an`` (perfective), ``k-um-an`` (actor focus).
        We only allow onsets of 1-2 characters (``k``, ``ky``, ``ng``) rather
        than every position, because "each valid infix position" in Figure 7 is
        undefined and an unconstrained scan invents boundaries inside roots.
        """
        for infix in self.lex.infixes:
            for onset in range(1, self.cfg.max_infix_onset + 1):
                if len(token) <= onset + len(infix):
                    continue
                left = token[:onset]
                if token[onset : onset + len(infix)] != infix:
                    continue
                if any(c in VOWELS for c in left):
                    continue  # onset must be consonantal
                right = token[onset + len(infix) :]
                reconstructed = left + right
                stem = self._resolve_stem(reconstructed, depth)
                if stem is None:
                    continue
                # Split the reconstructed-root analysis back around the infix.
                root_label = stem[0].label if stem else reconstructed
                return Segmentation(
                    token,
                    [
                        Morph(left, root_label, "root"),
                        Morph(infix, self._affix_label(infix, "infix"), "infix"),
                        Morph(right, root_label, "root"),
                    ],
                    True,
                )
        return None

    # --------------------------- TRY_SUFFIX ---------------------------- #
    def _try_suffix(self, token: str, depth: int) -> Segmentation | None:
        for suf in self.lex.suffixes:
            if not token.endswith(suf) or len(token) <= len(suf):
                continue
            stem = self._resolve_stem(token[: len(token) - len(suf)], depth)
            if stem is not None:
                return Segmentation(
                    token,
                    [*stem, Morph(suf, self._affix_label(suf, "suffix"), "suffix")],
                    True,
                )
        return None

    # ------------------------ reduplication (R4) ----------------------- #
    def _try_reduplication(self, token: str, depth: int) -> Segmentation | None:
        """CV- / CVC- reduplication, e.g. ``mamangan`` -> ``ma~mangan``.

        Not in the thesis scope statement (p. 12) but productive in
        Kapampangan aspect marking; leaving it out lowers MBF1 on real text.
        """
        for n in (3, 2):
            if len(token) <= 2 * n:
                continue
            head, rest = token[:n], token[n:]
            if not rest.startswith(head):
                continue
            stem = self._resolve_stem(rest, depth)
            if stem is not None:
                return Segmentation(
                    token, [Morph(head, "RED", "redup"), *stem], True,
                )
        return None

    # --------------------------- TRY_CLITIC ---------------------------- #
    def _try_clitic(self, token: str, depth: int) -> Segmentation | None:
        for clitic in self.lex.clitics:
            if len(token) <= len(clitic):
                continue
            if self.cfg.clitic_match == "suffix":
                if not token.endswith(clitic):
                    continue
                host = token[: len(token) - len(clitic)]
                positions = [host]
            else:  # literal "contains" reading of Figure 7 — see Issue T-2
                idx = token.find(clitic)
                if idx <= 0:
                    continue
                positions = [token[:idx]]
            for host in positions:
                stem = self._resolve_stem(host, depth)
                if stem is not None:
                    return Segmentation(
                        token,
                        [*stem, Morph(clitic, clitic, "clitic")],
                        True,
                    )
        return None
