"""Turn the project's real DATASET folder into the pipeline's expected inputs.

Handles four files:

``Kapampangan_Religious_Text-1_cleaned.json``  5,464 records, Bible text with
    ``Book <lbl>C:V</lbl>`` reference markers. High quality.
``Kapampangan_Literary_Text-1_cleaned.json``  13,310 records, poetry/prose.
    **Contains binary garbage** — the source was a legacy ``.doc`` read as
    Latin-1, so OLE compound-document streams (``ÐÏà¡±á``, NUL bytes, ``ÿÿÿÿ``)
    leaked into the text. Roughly 10% of records must be discarded.
``kapampangan_annotated.json``  3,138 dictionary headwords with root,
    syllabification and heuristically segmented affixed forms. This is the
    Lexicon Dictionary source.
``dictionary_entries.json``  the same dictionary before enrichment, plus PDF
    boilerplate ("download", "national", page fragments). Superseded — ignored.

Orthography note
----------------
The dictionary is transcribed in PALI/Forman conventions: ``’`` and ``q`` mark
glottal stop, ``:`` marks vowel length (``a’bak``, ``ma:walaq``,
``pa:makiya’be``). The running corpus uses plain orthography (``abak``,
``mawala``). Every lexicon entry is therefore stored twice: the PALI form goes
to ``variants.tsv`` and the stripped form becomes the usable root.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

TAG = re.compile(r"<[^>]+>")
VERSE = re.compile(r"^(.*?)\s*<lbl>(\d+):(\d+)</lbl>\s*(.*)$", re.DOTALL)
CTRL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
WORD = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", re.UNICODE)
PALI_MARKS = str.maketrans({"’": "", "'": "", ":": ""})


# --------------------------------------------------------------------------- #
# corpus text
# --------------------------------------------------------------------------- #
@dataclass
class LineRecord:
    text: str
    domain: str
    ref: str = ""


@dataclass
class IngestReport:
    kept: int = 0
    dropped: Counter = field(default_factory=Counter)

    def as_dict(self) -> dict:
        return {"kept": self.kept, "dropped": dict(self.dropped),
                "total": self.kept + sum(self.dropped.values())}


def is_binary_garbage(text: str) -> tuple[bool, str]:
    """Detect the OLE/`.doc` leakage in the literary file.

    Five independent signals; any one is enough. Tuned to keep poetry (which is
    short, punctuation-heavy and uses accented vowels for stress) while killing
    byte soup.
    """
    if CTRL.search(text):
        return True, "control_bytes"
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return True, "no_letters"
    non_ascii = sum(1 for c in letters if not c.isascii()) / len(letters)
    if non_ascii > 0.25:
        return True, "non_ascii_letters"
    if len(letters) / len(text) < 0.45:
        return True, "low_alpha_ratio"
    vowels = sum(1 for c in text.lower() if c in "aeiou")
    if vowels / len(letters) < 0.18:
        return True, "no_vowels"
    if any(len(w) >= 22 for w in WORD.findall(text)):
        return True, "impossible_word_length"
    return False, ""


def clean_corpus_json(
    path: str | Path, domain: str, strip_verse_ref: bool = True,
    min_words: int = 3,
) -> tuple[list[LineRecord], IngestReport]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    rep = IngestReport()
    out: list[LineRecord] = []
    seen: set[str] = set()

    for row in rows:
        raw = (row.get("text") or "")
        if raw.startswith("Title:"):
            rep.dropped["section_title"] += 1
            continue

        ref = ""
        m = VERSE.match(raw)
        if m:
            ref = f"{m.group(1).strip()} {m.group(2)}:{m.group(3)}"
            if strip_verse_ref:
                raw = m.group(4)

        text = unicodedata.normalize("NFC", TAG.sub(" ", raw))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            rep.dropped["empty"] += 1
            continue

        garbage, why = is_binary_garbage(text)
        if garbage:
            rep.dropped[f"garbage:{why}"] += 1
            continue
        if len(WORD.findall(text)) < min_words:
            rep.dropped["too_short"] += 1
            continue
        key = text.lower()
        if key in seen:
            rep.dropped["duplicate"] += 1
            continue
        seen.add(key)
        out.append(LineRecord(text=text, domain=domain, ref=ref))
        rep.kept += 1
    return out, rep


# --------------------------------------------------------------------------- #
# lexicon
# --------------------------------------------------------------------------- #
def strip_pali(form: str) -> str:
    """``ma:walaq`` -> ``mawala``; ``a’bak`` -> ``abak``."""
    s = unicodedata.normalize("NFC", form).translate(PALI_MARKS)
    s = re.sub(r"q(?=$|[^aeiou])", "", s)     # final/pre-consonantal q = glottal
    return s.strip().lower()


AFFIX_KIND = {
    "Prefix": "prefix", "Suffix": "suffix", "Infix": "infix",
    "Circumfix": "circumfix", "Reduplication": "redup", "Root": "root",
}


def parse_annotated_dictionary(path: str | Path) -> dict:
    """Extract everything the Lexicon Dictionary needs from the annotated JSON."""
    entries = json.loads(Path(path).read_text(encoding="utf-8"))

    roots: dict[str, dict] = {}
    variants: dict[str, str] = {}
    prefixes: Counter[str] = Counter()
    suffixes: Counter[str] = Counter()
    infixes: Counter[str] = Counter()
    circumfixes: Counter[tuple[str, str]] = Counter()
    redup: Counter[str] = Counter()
    segmentations: list[dict] = []
    derived: dict[str, dict] = {}
    stats = Counter()

    for e in entries:
        head = e.get("headword") or ""
        root_raw = e.get("root") or head
        root = strip_pali(root_raw)
        if not root or not root.isascii() or not root.replace("-", "").isalpha():
            stats["root_rejected"] += 1
            continue
        pos = ""
        for b in e.get("pos_blocks", []) or []:
            if b.get("pos"):
                pos = b["pos"].strip().rstrip(".")
                break
        gloss = ""
        for b in e.get("pos_blocks", []) or []:
            for s in b.get("senses", []) or []:
                if s:
                    gloss = s.strip()
                    break
            if gloss:
                break
        roots.setdefault(root, {"pos": pos, "gloss": gloss, "headword": head})
        stats["roots"] += 1
        if strip_pali(head) != root:
            variants[strip_pali(head)] = root
        if root_raw.lower() != root:
            variants[root_raw.lower()] = root

        for b in e.get("pos_blocks", []) or []:
            for key in ("affix_forms", "derived_forms_in_definition"):
                for f in b.get(key, []) or []:
                    kind = AFFIX_KIND.get(f.get("affix_type") or "", "")
                    surface = strip_pali(f.get("form") or f.get("original_form") or "")
                    seg = (f.get("segmentation") or "").strip()
                    if not surface or not surface.isalpha():
                        continue
                    affix = (f.get("affix") or "").strip()
                    if kind == "prefix" and affix:
                        prefixes[affix.strip("-")] += 1
                    elif kind == "suffix" and affix:
                        suffixes[affix.strip("-")] += 1
                    elif kind == "infix" and affix:
                        infixes[affix.strip("-")] += 1
                    elif kind == "circumfix" and "..." in affix:
                        left, _, right = affix.partition("...")
                        left = left.strip("- ")
                        right = re.sub(r"\(.*?\)", "", right).strip("- ")
                        if left and right:
                            circumfixes[(left, right)] += 1
                    elif kind == "redup" and affix:
                        redup[affix.split()[0].strip("~-")] += 1

                    # a segmentation is only usable if its pieces rebuild the word
                    pieces = [p for p in re.split(r"-+", seg) if p and p != "..."]
                    usable = bool(pieces) and "".join(
                        strip_pali(p) for p in pieces) == surface
                    segmentations.append({
                        "form": surface, "segmentation": "|".join(
                            strip_pali(p) for p in pieces) if usable else "",
                        "affix_type": f.get("affix_type"),
                        "affix": affix, "root": root,
                        "confidence": f.get("confidence"),
                        "concatenates": usable,
                    })
                    stats["seg_usable" if usable else "seg_unusable"] += 1
                    # NOTE: derived forms must NOT go into `variants`.
                    # `variants` means "different spelling of the same morpheme"
                    # and Lexicon.is_root() consults it, so putting `sumulat`
                    # there would make Figure 7's rule 2 fire and return the
                    # word unsegmented — destroying the very analysis this
                    # thesis is about. They are collected separately instead.
                    if usable and surface != root:
                        derived[surface] = {"root": root, "segmentation":
                                            "|".join(strip_pali(p) for p in pieces)}

    return {
        "roots": roots, "variants": variants,
        "prefixes": prefixes, "suffixes": suffixes, "infixes": infixes,
        "circumfixes": circumfixes, "redup": redup,
        "segmentations": segmentations, "derived": derived,
        "stats": dict(stats),
    }
