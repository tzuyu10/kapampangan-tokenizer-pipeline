"""Lexicon Dictionary (thesis p. 41-42).

A *training-time only* linguistic resource holding validated Kapampangan
roots, prefixes, infixes, suffixes, circumfixes, clitics, compounds and
spelling variants.  It is consumed by :mod:`kapampangan_mt.segmenter` and
indirectly by :mod:`kapampangan_mt.morph_bpe`; it is **never** loaded at
inference time (thesis p. 42: "After the tokenizer has been trained, the
dictionary is no longer used during actual input").

File format
-----------
All files are UTF-8 TSV with a header row.  ``#`` starts a comment line.

  roots.tsv         root, gloss_fil, pos, source
  prefixes.tsv      prefix, gloss, allomorphs(|-sep), source
  infixes.tsv       infix, gloss, source
  suffixes.tsv      suffix, gloss, allomorphs(|-sep), source
  circumfixes.tsv   prefix, suffix, gloss, source
  clitics.tsv       clitic, type(enclitic|proclitic|ligature), gloss, source
  compounds.tsv     compound, parts(|-sep), gloss, source
  variants.tsv      variant, canonical, note, source

``source`` is a free-text provenance field (e.g. "Del Corro 1980 p.44",
"validator: J. Santos 2026-02-11").  Keep it filled — the panel will ask.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_FILES = {
    "roots": "roots.tsv",
    "prefixes": "prefixes.tsv",
    "infixes": "infixes.tsv",
    "suffixes": "suffixes.tsv",
    "circumfixes": "circumfixes.tsv",
    "clitics": "clitics.tsv",
    "compounds": "compounds.tsv",
    "variants": "variants.tsv",
}


def _affix(s: str) -> str:
    """Strip the citation hyphens linguists write (``ma-``, ``-an``, ``-um-``)."""
    return s.strip().strip("-").strip()


def _read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as fh:
        lines = [ln for ln in fh if not ln.lstrip().startswith("#") and ln.strip()]
    if not lines:
        return []
    reader = csv.DictReader(lines, delimiter="\t")
    for row in reader:
        rows.append({(k or "").strip(): (v or "").strip() for k, v in row.items()})
    return rows


@dataclass
class Lexicon:
    """In-memory Lexicon Dictionary."""

    roots: set[str] = field(default_factory=set)
    prefixes: list[str] = field(default_factory=list)
    infixes: list[str] = field(default_factory=list)
    suffixes: list[str] = field(default_factory=list)
    circumfixes: list[tuple[str, str]] = field(default_factory=list)
    clitics: list[str] = field(default_factory=list)
    compounds: dict[str, list[str]] = field(default_factory=dict)
    variants: dict[str, str] = field(default_factory=dict)  # variant -> canonical

    #: surface allomorph -> canonical morpheme  (e.g. "pam" -> "pang")
    prefix_allomorphs: dict[str, str] = field(default_factory=dict)
    suffix_allomorphs: dict[str, str] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    @classmethod
    def load(cls, directory: str | Path) -> "Lexicon":
        d = Path(directory)
        lex = cls()

        for r in _read_tsv(d / REQUIRED_FILES["roots"]):
            if r.get("root"):
                lex.roots.add(r["root"])

        for r in _read_tsv(d / REQUIRED_FILES["prefixes"]):
            p = _affix(r.get("prefix", ""))
            if not p:
                continue
            lex.prefixes.append(p)
            lex.prefix_allomorphs[p] = p
            for allo in filter(None, map(_affix, (r.get("allomorphs") or "").split("|"))):
                lex.prefixes.append(allo)
                lex.prefix_allomorphs[allo] = p

        for r in _read_tsv(d / REQUIRED_FILES["infixes"]):
            if _affix(r.get("infix", "")):
                lex.infixes.append(_affix(r["infix"]))

        for r in _read_tsv(d / REQUIRED_FILES["suffixes"]):
            s = _affix(r.get("suffix", ""))
            if not s:
                continue
            lex.suffixes.append(s)
            lex.suffix_allomorphs[s] = s
            for allo in filter(None, map(_affix, (r.get("allomorphs") or "").split("|"))):
                lex.suffixes.append(allo)
                lex.suffix_allomorphs[allo] = s

        for r in _read_tsv(d / REQUIRED_FILES["circumfixes"]):
            pre, suf = _affix(r.get("prefix", "")), _affix(r.get("suffix", ""))
            if pre and suf:
                lex.circumfixes.append((pre, suf))

        for r in _read_tsv(d / REQUIRED_FILES["clitics"]):
            if _affix(r.get("clitic", "")):
                lex.clitics.append(_affix(r["clitic"]))

        for r in _read_tsv(d / REQUIRED_FILES["compounds"]):
            c = r.get("compound", "")
            if c:
                lex.compounds[c] = [p for p in (r.get("parts") or "").split("|") if p]

        for r in _read_tsv(d / REQUIRED_FILES["variants"]):
            if r.get("variant") and r.get("canonical"):
                lex.variants[r["variant"]] = r["canonical"]

        lex.finalize()
        return lex

    # ------------------------------------------------------------------ #
    def finalize(self) -> None:
        """De-duplicate and sort affixes **longest-first**.

        Longest-first ordering is a deliberate deviation from the thesis
        pseudocode (Figure 7), which iterates ``for each prefix in
        LEXICON.PREFIXES`` in unspecified order.  With arbitrary order,
        ``ma-`` fires before ``maka-`` and ``mag-``, silently producing the
        wrong analysis for a large share of verbs.  See docs/THESIS_ISSUES.md
        (Issue T-1).
        """
        # Expand circumfixes over prefix allomorphs: a circumfix declared as
        # (pang, an) must also fire on pam-/pan-/panga-...-an, otherwise the
        # morphophonemic alternation named in Chapter 1 defeats the analyser.
        canon_to_allos: dict[str, set[str]] = {}
        for allo, canon in self.prefix_allomorphs.items():
            canon_to_allos.setdefault(canon, set()).add(allo)
        expanded = set(self.circumfixes)
        for pre, suf in list(self.circumfixes):
            canon = self.prefix_allomorphs.get(pre, pre)
            for allo in canon_to_allos.get(canon, {pre}):
                expanded.add((allo, suf))
                self.prefix_allomorphs.setdefault(allo, canon)
        self.circumfixes = list(expanded)

        self.prefixes = sorted(set(self.prefixes), key=lambda s: (-len(s), s))
        self.infixes = sorted(set(self.infixes), key=lambda s: (-len(s), s))
        self.suffixes = sorted(set(self.suffixes), key=lambda s: (-len(s), s))
        self.clitics = sorted(set(self.clitics), key=lambda s: (-len(s), s))
        self.circumfixes = sorted(
            set(self.circumfixes), key=lambda ps: (-(len(ps[0]) + len(ps[1])), ps)
        )

    # -------------------------- lookups ------------------------------- #
    def is_root(self, form: str) -> bool:
        """True if *form* is a root or a spelling variant of one."""
        return form in self.roots or self.variants.get(form, "") in self.roots

    def canonical_root(self, form: str) -> str:
        return self.variants.get(form, form)

    def canonical_morpheme(self, surface: str, kind: str) -> str:
        """Map an allomorph to its canonical morpheme label.

        ``pam``/``pan``/``panga`` -> ``pang``.  Used by Morphological
        Consistency F1 so that phonologically conditioned variants of the same
        morpheme are not counted as different morphemes.
        """
        if kind == "prefix":
            return self.prefix_allomorphs.get(surface, surface)
        if kind == "suffix":
            return self.suffix_allomorphs.get(surface, surface)
        return surface

    def stats(self) -> dict[str, int]:
        return {
            "roots": len(self.roots),
            "prefixes": len(self.prefixes),
            "infixes": len(self.infixes),
            "suffixes": len(self.suffixes),
            "circumfixes": len(self.circumfixes),
            "clitics": len(self.clitics),
            "compounds": len(self.compounds),
            "variants": len(self.variants),
        }

    def validate(self) -> list[str]:
        """Cheap sanity checks; returns a list of human-readable warnings."""
        warn: list[str] = []
        if not self.roots:
            warn.append("roots.tsv is empty — segmentation will fall back to whole words.")
        if len(self.roots) < 1000:
            warn.append(
                f"only {len(self.roots)} roots. The segmenter can only analyse a word "
                "whose stripped remainder is a known root, so root coverage directly "
                "caps Morpheme Boundary F1. Target >= 3,000 roots."
            )
        for v, c in self.variants.items():
            if c not in self.roots and c not in self.variants:
                warn.append(f"variant '{v}' maps to unknown canonical '{c}'")
        for c, parts in self.compounds.items():
            if "".join(parts) != c.replace("-", "").replace(" ", ""):
                warn.append(f"compound '{c}' parts {parts} do not concatenate back")
        return warn
