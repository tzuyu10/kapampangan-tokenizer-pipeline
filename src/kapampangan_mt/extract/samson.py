"""Parser for *Kapampangan Dictionary* (Fr. Venancio Q. Samson), 835 pp.

Layout
------
Single reading flow, two printed columns that the PDF's text layer already
serialises correctly. Each page opens with a running head naming the first and
last headword on that page (``abono absic``); everything after it is entry text
wrapped across lines with no preserved indentation.

Entry detection
---------------
Indentation is lost, so a new entry is recognised by three signals together:

1. the line begins ``headword.`` or ``headword,``
2. what follows is a part-of-speech abbreviation, a verb-class marker, or a
   cross-reference — the shapes Samson actually uses
3. the candidate headword is alphabetically at or after the previous one

Signal 3 is what makes this reliable: a dictionary is sorted, so an
out-of-order candidate is almost always a sentence-initial word inside a
definition rather than a real headword. Candidates that fail it are left
attached to the running entry instead of being invented as new ones.

The parser records the raw text it consumed for every entry, so any decision it
made can be checked against the page.
"""
from __future__ import annotations

import re

from .pdf_text import n_pages, page_lines
from .schema import Entry, Source, assess_ocr, make_id, sort_key

DICTIONARY = "Samson, Kapampangan Dictionary"

# Samson's own abbreviations, as printed. 'ft.' is included because the scan
# renders 'n.' that way on a large share of pages — it is flagged, not fixed.
POS_TOKENS = {
    "n": "noun", "ft": "noun (OCR: printed as 'ft.')", "adj": "adjective",
    "adv": "adverb", "v": "verb", "vt": "transitive verb", "vi": "intransitive verb",
    "nv": "noun-verb", "vn": "verb-noun", "pron": "pronoun", "prep": "preposition",
    "conj": "conjunction", "interj": "interjection", "num": "numeral",
    "art": "article", "part": "particle", "abbr": "abbreviation",
}
_POS_RE = re.compile(
    r"^\(?(?:Sp\.|Eng\.|Tag\.|Ch\.)?\)?\s*"
    r"(" + "|".join(sorted(POS_TOKENS, key=len, reverse=True)) + r")\.\s",
    re.IGNORECASE,
)
_VERB_START = re.compile(r"^(Active verb|Verb|Passive|Infinitive|P\.\s*\d)", re.I)
_XREF_START = re.compile(r"^S\s?ee\b|^See\b|^Syn\.|^Cf\.|^cf\.", re.I)
_ORIGIN = re.compile(r"^\((Sp|Eng|Tag|Ch|Lat|Fr)\.\)")

#: English words that open definition sentences. The brief is explicit: words
#: appearing only inside definitions must never become lexical entries. The
#: alphabetical band catches most of them; this catches the rest.
ENGLISH_STOPWORDS = {
    "with", "without", "the", "and", "but", "for", "from", "that", "this",
    "these", "those", "when", "where", "which", "while", "there", "their",
    "then", "than", "also", "such", "some", "one", "two", "into", "onto",
    "upon", "over", "under", "after", "before", "about", "because", "being",
    "been", "have", "has", "had", "was", "were", "are", "not", "any", "all",
    "each", "very", "more", "most", "less", "used", "using", "usually",
    "said", "says", "thus", "here", "what", "who", "whom", "whose",
    "someone", "something", "anyone", "anything", "everyone", "everything",
    "reprieve", "responsibility", "worshipping", "verses",
}

_HEAD = re.compile(
    r"^([a-zA-ZñÑğĞáéíóúàèìòùâêîôûäëïöüÁÉÍÓÚÂÊÎÔÛ'’\-]{2,28})\s*[.,]\s+(\S.*)$"
)
_RUNNING_HEAD = re.compile(r"^[A-Za-zñÑğáéíóúâêîôû'’\-]+\s+[A-Za-zñÑğáéíóúâêîôû'’\-]+\s*$")

_XREF_FIND = re.compile(r"(?:S\s?ee|See also|Syn\.|Cf\.|cf\.)\s+([A-Za-zñÑğáéíóúâêîôû'’\- ,]+)")
_VARIANT_FIND = re.compile(
    r"(?:also (?:written|spelled)|or,? better|variant of|same as)\s+"
    r"([A-Za-zñÑğáéíóúâêîôû'’\-]+)", re.IGNORECASE)
_EXAMPLE_FIND = re.compile(r"(?:v\.\s?g\.|e\.\s?g\.|Idiom:)\s*,?\s*([^.]{6,180}\.)")


def _looks_like_entry_start(rest: str) -> bool:
    return bool(_POS_RE.match(rest) or _VERB_START.match(rest)
                or _XREF_START.match(rest) or _ORIGIN.match(rest))


def _running_head(lines: list[str]) -> tuple[str, str] | None:
    """The first/last headword printed at the top of each page.

    This is the strongest signal available: a page's entries must all sort
    between its two running-head words. It rules out sentence-initial words
    inside definitions far more reliably than any part-of-speech heuristic.
    Returns ``None`` when the head is missing or itself OCR-damaged.
    """
    for line in lines:
        line = line.strip()
        if not line:
            continue
        toks = line.split()
        if not (1 <= len(toks) <= 2):
            return None
        if not all(re.fullmatch(r"[A-Za-zñÑğĞçÇńŃáéíóúàèìòùâêîôûäëïöüÁÉÍÓÚ'’\-]{2,28}", t)
               for t in toks):
            return None
        lo = sort_key(toks[0])
        hi = sort_key(toks[-1])
        if not lo or not hi:
            return None
        return (lo, hi)
    return None


def _page_bands(path: str, first_page: int, last_page: int) -> dict[int, tuple[str, str]]:
    """Alphabetical band each page must fall inside.

    Lower bound = this page's own running head. Upper bound = the running head
    of the NEXT page that has one, because a printed dictionary page ends where
    the following page begins. Using the neighbour rather than the page's own
    second head-word also survives the pages whose head is a single word or is
    itself OCR-damaged.
    """
    heads: dict[int, str] = {}
    for pg in range(first_page, last_page + 1):
        h = _running_head(page_lines(path, pg))
        if h:
            heads[pg] = h[0]
    bands: dict[int, tuple[str, str]] = {}
    pages = sorted(heads)
    for i, pg in enumerate(pages):
        lo = heads[pg]
        hi = heads[pages[i + 1]] if i + 1 < len(pages) else lo[:1] + "zzzz"
        if hi[:2] < lo[:2]:                      # letter rolled over, or bad head
            hi = lo[:1] + "zzzz"
        bands[pg] = (lo, hi)
    return bands


def _in_band(key: str, band: tuple[str, str] | None, width: int = 4) -> bool:
    if band is None:
        return False
    lo, hi = band
    return lo[:width] <= key[:width] <= hi[:width]


def find_body_range(path: str) -> tuple[int, int]:
    """First and last page index that carry dictionary entries."""
    total = n_pages(path)
    first = last = None
    for i in range(total):
        lines = [l.strip() for l in page_lines(path, i) if l.strip()]
        if len(lines) < 5:
            continue
        hits = sum(1 for l in lines
                   if (m := _HEAD.match(l)) and _looks_like_entry_start(m.group(2)))
        if hits >= 3:
            first = i if first is None else first
            last = i
    return (first or 0), (last or total - 1)


def parse(path: str, first_page: int | None = None, last_page: int | None = None,
          progress: bool = True) -> list[Entry]:
    if first_page is None or last_page is None:
        a, b = find_body_range(path)
        first_page = a if first_page is None else first_page
        last_page = b if last_page is None else last_page

    bands = _page_bands(path, first_page, last_page)
    entries: list[Entry] = []
    buf: list[str] = []
    cur_head: str | None = None
    cur_page: int | None = None
    prev_key = ""
    per_page_index = 0

    def flush() -> None:
        nonlocal buf, cur_head, cur_page
        if cur_head is None:
            buf = []
            return
        entries.append(_build(cur_head, " ".join(buf).strip(), cur_page, per_page_index))
        buf = []
        cur_head = None

    for pg in range(first_page, last_page + 1):
        if progress and pg % 100 == 0:
            print(f"  samson: page {pg + 1}/{last_page + 1}, {len(entries)} entries so far")
        lines = [l for l in page_lines(path, pg)]
        band = bands.get(pg)
        per_page_index = 0
        if band:
            # RESET, not max(). The running head is authoritative for this page.
            # Using max() meant that one bad accept on a band-less page raised
            # prev_key permanently and silenced every page that followed —
            # extraction stopped dead at 125 entries out of ~9,000.
            prev_key = band[0]
        head_skipped = False

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue
            if not head_skipped:
                head_skipped = True
                if band and _RUNNING_HEAD.match(line) or (band and len(line.split()) <= 2):
                    continue
            if line.isdigit():
                continue

            m = _HEAD.match(line)
            if m:
                cand, rest = m.group(1), m.group(2)
                key = sort_key(cand)
                # When a running head is available the band test is REQUIRED.
                # Relaxing it to "or looks like an entry" lets a definition
                # sentence such as "reprieve. Verb, ..." be taken as a headword,
                # which then poisons the monotonicity guard for every page after.
                ok = _in_band(key, band) if band else _looks_like_entry_start(rest)
                if cand.lower() in ENGLISH_STOPWORDS:
                    ok = False
                if key and key[:4] >= prev_key[:4] and ok:
                    flush()
                    cur_head, cur_page, prev_key = cand, pg + 1, key
                    per_page_index += 1
                    buf = [rest]
                    continue
            buf.append(line)
    flush()
    return entries


def _build(headword: str, raw: str, page: int | None, index: int) -> Entry:
    text = re.sub(r"\s+", " ", raw).strip()

    pos: list[str] = []
    definition = text
    explicit_variants: list[str] = []

    # Samson writes alternate spellings as a leading "or Anaw." before the part
    # of speech. The source states these explicitly, so recording them is not
    # inference — but the part of speech has to be looked for AFTER them.
    alt = re.match(r"^or\s+([A-Za-zñÑğáéíóúàèìòùâêîôû'’\-]{2,28})\s*[.,]\s*", text)
    if alt:
        explicit_variants.append(alt.group(1))
        text = text[alt.end():]
        definition = text

    m = _POS_RE.match(text)
    if m:
        tag = m.group(1).lower()
        pos.append(POS_TOKENS.get(tag, tag))
        definition = text[m.end():].strip()
    origin = _ORIGIN.match(text)
    if origin:
        definition = re.sub(r"^\((Sp|Eng|Tag|Ch|Lat|Fr)\.\)\s*", "", definition).strip()

    xrefs: list[str] = []
    for hit in _XREF_FIND.findall(text):
        for part in re.split(r"[,;]", hit):
            part = part.strip(" .")
            # a cross-reference is a single word; longer runs are sentence text
            if part and len(part.split()) == 1 and len(part) > 1:
                xrefs.append(part)

    variants = explicit_variants + [v for v in _VARIANT_FIND.findall(text) if v]
    examples = [e.strip() for e in _EXAMPLE_FIND.findall(text)]

    status, notes = assess_ocr(headword + " " + text)
    if origin:
        notes.append(f"Source marks this as a loanword: ({origin.group(1)}.).")

    return Entry(
        entry_id=make_id("samson", page, index, headword),
        headword=headword,
        definition=definition,
        part_of_speech=pos,
        pronunciation="",
        syllables=[],
        examples=examples[:5],
        derived_forms=[],                 # Samson mixes these into prose; not inferred
        spelling_variants=variants[:5],
        cross_references=sorted(set(xrefs))[:8],
        # The headword is put back so original_text reproduces the entry as
        # printed. Storing only the body made 22% of records untraceable to
        # their own source text.
        source=Source(dictionary=DICTIONARY, page=page,
                      original_text=(f"{headword}. {raw}".strip() if raw else headword)),
        ocr_status=status,
        notes=" ".join(notes),
    )
