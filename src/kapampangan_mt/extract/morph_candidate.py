"""Build an AI-assisted CANDIDATE morphological lexicon from the extracted entries.

This is *candidate* data. Every record carries ``validation_status:
"unvalidated"`` and must be reviewed by a native Kapampangan speaker or
linguist before it is used as a linguistic resource.

The evidence rule
-----------------
No external knowledge of Kapampangan is used to license an analysis. Everything
is grounded in what the supplied dictionary itself asserts.

Why that matters here: running a plain substring search over the 8,959 Samson
headwords "discovers" affixes like ``p-`` (94 hits: *plato* = p- + *lato*),
``t-`` (87), ``-s`` (122) and ``-c`` (95). Those are accidental string
coincidences, not morphology, and a lexicon built on them would be worthless.

So the affix inventory is derived from a much narrower source: the paradigms
Samson *prints inside its own entries*.

    abut. Active verb, mamabut, minabut, mabut, and its infinitive, manabut...

Here the dictionary is stating that *mamabut*, *minabut*, *mabut* and *manabut*
belong to the headword *abut*. Each such statement is one explicit
(headword -> form) observation. Six thousand of them, taken together, yield the
affix inventory — and it comes out looking like Kapampangan rather than like
noise: ``i-``, ``man-``, ``mag-``, ``min-``, ``in-``, ``pa-``, ``-an``,
``-in-``, ``-um-``, ``ca-...-an``, ``pa-...-an``.

An affix has to clear a frequency floor in that explicit set before it may be
used to propose an analysis for a headword the dictionary says nothing about.

Three levels of claim
---------------------
``dictionary_explicit``
    Samson prints the relationship. Confidence high.
``AI_proposed``
    Samson does not print it, but the remainder after stripping a licensed
    affix is itself a Samson headword. Confidence medium, or low for short or
    infrequent affixes.
``unknown``
    Neither applies. ``root`` stays null, ``segmentation`` stays empty. Roughly
    two thirds of entries land here, which is the correct outcome — the
    alternative is invention.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field

WORD = r"[A-Za-zñÑğĞáéíóúàèìòùâêîôûçüÜ'’-]+"

#: Places where Samson prints a paradigm belonging to the current headword.
PARADIGM_PATTERNS = [
    re.compile(r"Active verb(?: and its infinitive)?,?\s+((?:" + WORD + r",\s*){1,10})", re.I),
    re.compile(r"\bVerb,\s+((?:" + WORD + r",\s*){1,10})"),
    re.compile(r"Infinitive,?\s+((?:" + WORD + r",\s*){1,8})", re.I),
    re.compile(r"\bv[ti]\.\s+((?:" + WORD + r",\s*){1,10})"),
    re.compile(r"\bP\.\s*\d\.\s+(?:Past,\s*)?((?:" + WORD + r",\s*){1,8})"),
]
_XREF = re.compile(r"(?:S\s?ee|See also|Syn\.)\s+([A-Za-zñÑğáéíóúâêîôû'’-]{2,24})", re.I)

#: Frequency floors in the EXPLICIT pair set. Below these an affix is treated as
#: an artefact and may not license an AI-proposed analysis.
MIN_PREFIX = 20
MIN_INFIX = 20
MIN_SUFFIX = 5
MIN_CIRCUMFIX = 5


@dataclass
class Morphology:
    status: str = "unknown"
    root: str | None = None
    prefixes: list[str] = field(default_factory=list)
    infixes: list[str] = field(default_factory=list)
    suffixes: list[str] = field(default_factory=list)
    circumfixes: list[str] = field(default_factory=list)
    clitics: list[str] = field(default_factory=list)
    compound_parts: list[str] = field(default_factory=list)
    reduplication: str | None = None
    segmentation: str = ""


@dataclass
class CandidateEntry:
    entry_id: str = ""
    headword: str = ""
    definition: object = ""
    part_of_speech: list[str] = field(default_factory=list)
    pronunciation: str = ""
    syllables: list[str] = field(default_factory=list)
    morphology: Morphology = field(default_factory=Morphology)
    spelling_variants: list[str] = field(default_factory=list)
    derived_forms: list[str] = field(default_factory=list)
    inflected_forms: list[str] = field(default_factory=list)
    evidence: str = ""
    annotation_source: str = "unknown"
    confidence: str = "low"
    ocr_status: str = "clear"
    source: dict = field(default_factory=dict)
    validation_status: str = "unvalidated"
    notes: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


# --------------------------------------------------------------------------- #
# 1. what the dictionary explicitly states
# --------------------------------------------------------------------------- #
def explicit_paradigms(rows: list[dict]) -> dict[str, dict]:
    """``headword -> {"forms": [...], "page": n}`` from printed paradigms."""
    out: dict[str, dict] = {}
    for r in rows:
        head = r["headword"].lower()
        if not head.isalpha():
            continue
        text = r["source"]["original_text"]
        forms: set[str] = set()
        for pat in PARADIGM_PATTERNS:
            for m in pat.finditer(text):
                for w in m.group(1).split(","):
                    w = w.strip().lower()
                    if w and w.isalpha() and w != head and 2 < len(w) < 24:
                        forms.add(w)
        if forms:
            rec = out.setdefault(head, {"forms": set(), "page": r["source"]["page"]})
            rec["forms"] |= forms
    for rec in out.values():
        rec["forms"] = sorted(rec["forms"])
    return out


def classify_pair(head: str, form: str) -> tuple[str, object] | None:
    """How does *form* relate to *head*, as a string operation?

    Reduplication is tested first: ``tabac -> tatabac`` is a copy of the root's
    own opening syllable, not a ``ta-`` prefix, and testing prefixes first would
    populate the inventory with dozens of phantom CV prefixes.
    """
    if len(form) <= len(head):
        return None
    for k in (3, 2, 1):
        if form == head[:k] + head:
            return ("redup", head[:k])
    if form.endswith(head):
        return ("prefix", form[: len(form) - len(head)])
    if form.startswith(head):
        return ("suffix", form[len(head):])
    if head[1:] and form[0] == head[0] and form.endswith(head[1:]):
        return ("infix", form[1: len(form) - len(head[1:])])
    for a in range(1, 7):
        for b in range(1, 5):
            if len(form) == len(head) + a + b and form[a: len(form) - b] == head:
                return ("circumfix", (form[:a], form[-b:]))
    return None


def derive_affix_inventory(paradigms: dict[str, dict]) -> dict:
    """The licensed affix set, counted over explicit pairs only."""
    counts: dict[str, Counter] = {k: Counter() for k in
                                  ("prefix", "suffix", "infix", "circumfix", "redup")}
    examples: dict[tuple, list] = defaultdict(list)
    non_concatenative = 0
    total = 0
    for head, rec in paradigms.items():
        for form in rec["forms"]:
            total += 1
            hit = classify_pair(head, form)
            if hit is None:
                non_concatenative += 1
                continue
            kind, aff = hit
            counts[kind][aff] += 1
            if len(examples[(kind, aff)]) < 3:
                examples[(kind, aff)].append((head, form, rec["page"]))
    floors = {"prefix": MIN_PREFIX, "infix": MIN_INFIX, "suffix": MIN_SUFFIX,
              "circumfix": MIN_CIRCUMFIX, "redup": 3}
    licensed = {k: {a: c for a, c in v.items() if c >= floors[k]} for k, v in counts.items()}
    return {
        "licensed": licensed,
        "counts": {k: dict(v.most_common(40)) for k, v in counts.items()},
        "examples": {f"{k}:{a}": examples[(k, a)] for k, v in licensed.items() for a in v},
        "explicit_pairs": total,
        "non_concatenative_pairs": non_concatenative,
    }


# --------------------------------------------------------------------------- #
# 2. annotate one entry
# --------------------------------------------------------------------------- #
def _fmt(kind: str, aff) -> str:
    if kind == "prefix":
        return f"{aff}-"
    if kind == "suffix":
        return f"-{aff}"
    if kind == "infix":
        return f"-{aff}-"
    if kind == "circumfix":
        return f"{aff[0]}-...-{aff[1]}"
    return str(aff)


def _apply(morph: Morphology, kind: str, aff, root: str) -> None:
    morph.root = root
    if kind == "prefix":
        morph.prefixes = [f"{aff}-"]
        morph.segmentation = f"{aff}- + {root}"
    elif kind == "suffix":
        morph.suffixes = [f"-{aff}"]
        morph.segmentation = f"{root} + -{aff}"
    elif kind == "infix":
        morph.infixes = [f"-{aff}-"]
        morph.segmentation = f"{root[0]} + -{aff}- + {root[1:]}"
    elif kind == "circumfix":
        morph.circumfixes = [f"{aff[0]}-...-{aff[1]}"]
        morph.segmentation = f"{aff[0]}- + {root} + -{aff[1]}"
    elif kind == "redup":
        morph.reduplication = f"{aff}~ (copy of the root-initial sequence)"
        morph.segmentation = f"{aff}~ + {root}"


def _is_licensed(kind: str, aff, inventory: dict) -> bool:
    return aff in inventory["licensed"].get(kind, {})


def annotate(row: dict, lemmas: dict[str, dict], paradigms: dict[str, dict],
             form_owner: dict[str, list[tuple[str, int]]], inventory: dict) -> CandidateEntry:
    head = row["headword"]
    low = head.lower()
    e = CandidateEntry(
        entry_id=row["entry_id"],
        headword=head,                       # original spelling, never corrected
        definition=row["definition"],
        part_of_speech=list(row["part_of_speech"]),
        pronunciation=row["pronunciation"],
        syllables=list(row["syllables"]),    # phonological only; never read as morphemes
        spelling_variants=list(row["spelling_variants"]),
        ocr_status=row["ocr_status"],
        source=dict(row["source"]),
        notes=row["notes"],
    )
    m = e.morphology
    page = row["source"]["page"]
    same_source = row["entry_id"].split(":")[0]
    # All morphological evidence comes from Samson, the only source that prints
    # paradigms. When the entry itself came from one of the bare wordlists, the
    # evidence string has to say so — otherwise a validator would look for the
    # cited page in the wrong book. It is also a real caveat: Samson uses the
    # Spanish-era orthography and the wordlists use the modern one, so a
    # cross-source match may be comparing different spelling systems.
    cross = "" if same_source == "samson" else (
        f" NOTE: this entry is from {same_source}; the supporting evidence is "
        f"from Samson, a different dictionary using the Spanish-era "
        f"orthography. Cross-source match — verify the spelling systems agree.")

    # --- forms the dictionary prints under THIS headword ------------------
    own = paradigms.get(low)
    if own:
        e.derived_forms = list(own["forms"])

    # --- (a) this headword is printed under another headword --------------
    owners = [(o, p) for o, p in form_owner.get(low, []) if o != low]
    if owners:
        root, rpage = owners[0]
        hit = classify_pair(root, low)
        e.annotation_source = "dictionary_explicit"
        e.confidence = "high"
        if hit and _is_licensed(hit[0], hit[1], inventory):
            kind, aff = hit
            _apply(m, kind, aff, root)
            m.status = "derived"
            e.evidence = (
                f"Samson prints '{head}' in the paradigm of the headword "
                f"'{root}' (page {rpage}), which establishes the relationship. "
                f"The string difference is {_fmt(kind, aff)}, which is attested "
                f"in {inventory['licensed'][kind][aff]} other explicit "
                f"statements in this dictionary." + cross
            )
        elif hit:
            # The dictionary asserts the RELATIONSHIP, not that the leftover
            # string is a morpheme. Rare leftovers here are parse artefacts
            # ('suyi-', 'pilub-...-an'), so the root is kept and the affix is not
            # claimed.
            kind, aff = hit
            m.status = "derived"
            m.root = root
            e.evidence = (
                f"Samson prints '{head}' in the paradigm of the headword "
                f"'{root}' (page {rpage}), which establishes the relationship. "
                f"The leftover string {_fmt(kind, aff)} is not attested as an "
                f"affix elsewhere in this dictionary, so no affix or "
                f"segmentation is claimed." + cross
            )
            e.notes = (e.notes + " Root is dictionary-stated; the affix analysis "
                       "was withheld for lack of independent attestation.").strip()
        else:
            m.status = "derived"
            m.root = root
            e.evidence = (
                f"Samson prints '{head}' in the paradigm of the headword "
                f"'{root}' (page {rpage}). The two forms are not related by "
                f"simple concatenation, so no segmentation is proposed." + cross
            )
            e.notes = (e.notes + " Root related by a non-concatenative "
                       "alternation; segmentation left empty deliberately.").strip()
        return e

    # --- (b) the dictionary treats this headword as a base ----------------
    if own:
        m.status = "simple"
        m.root = low
        m.segmentation = low
        e.annotation_source = "dictionary_explicit"
        e.confidence = "high"
        e.evidence = (
            f"Samson lists a paradigm under this headword on page {page} "
            f"({', '.join(own['forms'][:4])}{'...' if len(own['forms']) > 4 else ''}), "
            f"so the dictionary treats '{head}' as the base form." + cross
        )
        return e

    # --- (c) the dictionary explicitly gives a variant --------------------
    if e.spelling_variants:
        m.status = "variant"
        e.annotation_source = "dictionary_explicit"
        e.confidence = "high"
        e.evidence = (
            f"Samson prints '{head}' with an explicit alternative spelling "
            f"('{e.spelling_variants[0]}') on page {page}."
        )
        return e

    # --- (d) compound: hyphenated and both halves are headwords -----------
    if "-" in low:
        parts = [p for p in low.split("-") if p]
        if len(parts) > 1 and all(p in lemmas for p in parts):
            m.status = "compound"
            m.compound_parts = parts
            m.segmentation = " + ".join(parts)
            e.annotation_source = "AI_proposed"
            e.confidence = "medium"
            e.evidence = (
                "Heuristic inference: the headword is hyphenated and every part "
                + ", ".join(f"'{p}' (page {lemmas[p]['page']})" for p in parts)
                + " is itself a headword in this dictionary. Not stated by the "
                "dictionary as a compound; requires validation."
            )
            return e

    # --- (e) strip one licensed affix; the remainder must be a headword ---
    lic = inventory["licensed"]
    best = None                                   # (kind, aff, root, count)
    for k in (3, 2, 1):
        if len(low) > 2 * k and low[:k] == low[k: 2 * k] and low[k:] in lemmas:
            c = lic["redup"].get(low[:k])
            if c:
                best = ("redup", low[:k], low[k:], c)
                break
    if best is None:
        for aff, c in sorted(lic["prefix"].items(), key=lambda kv: (-len(kv[0]), -kv[1])):
            if low.startswith(aff) and low[len(aff):] in lemmas:
                best = ("prefix", aff, low[len(aff):], c)
                break
    if best is None:
        for aff, c in sorted(lic["circumfix"].items(), key=lambda kv: -kv[1]):
            a, b = aff
            if low.startswith(a) and low.endswith(b) and low[len(a): len(low) - len(b)] in lemmas:
                best = ("circumfix", aff, low[len(a): len(low) - len(b)], c)
                break
    if best is None:
        for aff, c in sorted(lic["suffix"].items(), key=lambda kv: (-len(kv[0]), -kv[1])):
            if low.endswith(aff) and low[: len(low) - len(aff)] in lemmas:
                best = ("suffix", aff, low[: len(low) - len(aff)], c)
                break
    if best is None:
        for aff, c in sorted(lic["infix"].items(), key=lambda kv: -kv[1]):
            for pos in (1,):
                if low[pos: pos + len(aff)] == aff:
                    cand = low[:pos] + low[pos + len(aff):]
                    if cand in lemmas and len(cand) >= 3:
                        best = ("infix", aff, cand, c)
                        break
            if best:
                break

    if best is not None:
        kind, aff, root, count = best
        _apply(m, kind, aff, root)
        m.status = "derived"
        e.annotation_source = "AI_proposed"
        e.confidence = "medium" if (count >= 40 and len(root) >= 4) else "low"
        e.evidence = (
            f"Heuristic inference, not stated by the dictionary. Removing "
            f"{_fmt(kind, aff)} leaves '{root}', which is itself a headword in "
            f"this dictionary (page {lemmas[root]['page']}). "
            f"{_fmt(kind, aff)} is attested in {count} explicit "
            f"headword-to-form statements elsewhere in the same dictionary. "
            f"Requires validation." + cross
        )
        return e

    # --- (f) nothing defensible -------------------------------------------
    m.status = "unknown"
    m.root = None
    e.annotation_source = "unknown"
    e.confidence = "low"
    e.evidence = (
        "No morphological analysis is proposed. The dictionary states nothing "
        "about this entry's structure, and stripping any dictionary-attested "
        "affix does not leave a form that is itself a headword here."
    )
    if same_source != "samson":
        e.notes = (e.notes + " Source is a bare wordlist with no morphological "
                   "information, so only the headword and gloss are available.").strip()
    return e
