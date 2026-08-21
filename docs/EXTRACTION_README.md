# Dictionary extraction — what was produced and how to check it

Stage 20 converts the source PDFs into JSONL lexical entries.
**Extraction only.** No morphological analysis, no guessed roots or affixes, no
translation, no silent spelling correction. Morphological annotation is a
separate, later stage.

```bash
python scripts/20_extract_dictionaries.py --pdf-dir "C:/Users/Gabo/Downloads/DATASET/UNANNOTATED"
python scripts/21_verify_extraction.py    --pdf-dir "C:/Users/Gabo/Downloads/DATASET/UNANNOTATED"
```

Runtime: about 3 minutes, mostly the 835-page Samson dictionary.

---

## What came out

| Source | Entries | Unique headwords | With definition | Flagged | Sorted |
|---|---|---|---|---|---|
| Samson, *Kapampangan Dictionary* (835 pp) | **9,751** | 9,018 | 9,751 | 82.3% | 94.1% |
| Kapampangan–English–Pilipino wordlist (56 pp) | **3,056** | 2,950 | 2,944 | 97.9% | 94.5% |
| *Speaking Kapampangan*, Kapampangan→English glossary | **1,322** | 1,304 | 679 | 100% | 71.6% |
| *Speaking Kapampangan*, English→Kapampangan vocabulary | **919** | 908 | 295 | 100% | 84.3% |
| *Mga Salita sa Iba't Ibang Dayalekto* | **68** | 67 | 68 | 0% | 52.2% |
| **Total** | **15,116** | **12,929** | | | |

"Sorted" = share of consecutive headword pairs in alphabetical order. It is a
sanity check, not a target: a dictionary is sorted, so a low figure means the
parser picked up text that is not a headword. Samson at 94% is healthy (the
remainder is homograph runs and OCR-damaged headwords). The Mirikitani
glossaries are lower because their scan interleaves entries.

### Files

```
data/extracted/
  samson.jsonl                 9,751
  trilingual.jsonl             3,056
  mirikitani_pam_eng.jsonl     1,322
  mirikitani_eng_pam.jsonl       919
  dayalekto.jsonl                 68
  all_entries.jsonl           15,116   (everything, in source order)
  extraction_report.json               per-source counts
```

---

## Not extracted, on purpose

Three PDFs contain no lexical entries. Mining example words out of running
prose would break the rule that words appearing only inside explanations must
never become headwords.

| File | Why |
|---|---|
| `SL-030-forman-kapampangan-grammar-notes.pdf` | Forman's grammar. **Use this later for the affix inventory** — it is the authoritative source for the `pang-` → `pam-`/`pan-`/`panga-` allomorphs your `prefixes.tsv` is missing. |
| `ilide.info-an-introduction-to-the-kapampangan-langu-*.pdf` | Lecture notes, prose with scattered examples. |
| `ilide.info-paghahambing-ng-wikang-kapampangan-*.pdf` | Comparative paper in Filipino. Cite it for the orthography and phonology rules. |

---

## Record format

One JSON object per line:

```json
{
  "entry_id": "samson:p0050:010:ano",
  "headword": "Ano",
  "definition": "a forest palm tree (Livisiona rotundifolia) whose leaves are used for roofing, hats, rain gears...",
  "part_of_speech": ["noun"],
  "pronunciation": "",
  "syllables": [],
  "examples": [],
  "derived_forms": [],
  "spelling_variants": ["Anaw"],
  "cross_references": [],
  "source": {
    "dictionary": "Samson, Kapampangan Dictionary",
    "page": 50,
    "original_text": "Ano. or Anaw. n. a forest palm tree ( Livisiona rotundifolia) ..."
  },
  "ocr_status": "needs_review",
  "notes": "Layout artefact: column-separator bars retained in the text."
}
```

`source.page` is the **PDF page number**, so you can open the PDF at that page
and see the entry. `source.original_text` reproduces the entry as printed,
headword included — every field can be traced back to it.

Empty means the source did not provide it. Nothing is filled in by inference.
`syllables` stays empty for all of these sources because none of them
syllabify; when a source does, syllables go there and are **never** reread as
prefix/suffix.

---

## How entries were found

### Samson (the hard one)

The PDF's text layer loses indentation, so "this line starts a new entry" has
to be inferred. Three signals are combined:

1. the line begins `headword.` or `headword,`
2. what follows is a part-of-speech abbreviation, a verb-class marker
   (`Active verb`, `P. 1.`), a cross-reference (`See`, `Syn.`) or a language tag
   (`(Sp.)`)
3. **the candidate falls inside the page's alphabetical band**

Signal 3 does the real work. Every page prints a running head naming its first
and last headword (`abono absic`), so a page's entries must sort between its own
head and the next page's. That rules out definition sentences far better than
any part-of-speech rule.

It also matters that the band **resets** at each page rather than accumulating.
An early version took the running maximum; one bad accept on a page whose
running head was OCR-damaged raised the bound permanently and silenced every
page after it — extraction stopped dead at 125 entries out of 9,751. The band
is authoritative per page, so a single bad page can no longer poison the rest.

### The tabular glossaries

Reading them in natural order interleaves the columns and pairs the wrong
headword with the wrong gloss — that would *fabricate* definitions. Instead the
text chunks' x/y coordinates are used: assign to columns by x, estimate one
vertical offset per column per page, then pair only within a tight window.

**When no pairing falls inside the window, the field is left empty and the entry
is flagged.** It is never filled with the nearest guess. That is why 679 of
1,322 Kapampangan→English entries have no definition: the scan did not let us
determine one with confidence.

---

## OCR flags

82% of Samson entries carry `ocr_status: "needs_review"`. That sounds alarming;
here is the actual breakdown:

| Reason | Count | Severity |
|---|---|---|
| words split by spurious spaces (`as awa`, `pis amb an`) | 8,022 | cosmetic — text is readable |
| column-separator bars `\|` retained | 3,173 | cosmetic |
| source marks it a loanword `(Sp.)` | 2,425 | **not an error** — informational |
| two-column glossary alignment risk | 2,241 | **real** — verify before use |
| `ft.` where `n.` was printed | 489 | real but systematic and known |
| unexpected symbol characters | 273 | real |
| gloss could not be aligned | 693 | **real** — field left empty |

The scan renders `n.` as `ft.` on a large share of pages. This is **flagged, not
corrected** — the part of speech is recorded as `noun (OCR: printed as 'ft.')`
and the raw text keeps `ft.` so you can check.

Sort by `notes` when reviewing. The alignment warnings are the ones that matter;
the spurious-space and pipe-bar flags are noise you can filter out.

---

## Verification

`scripts/21_verify_extraction.py` runs twelve checks:

```
schema keys exact on every record             PASS
no morphological fields present               PASS
no empty headwords                            PASS
no page numbers as headwords                  PASS
no column headers as headwords                PASS
every entry carries a page number             PASS
every entry carries original text             PASS
every entry names its dictionary              PASS
entry_ids unique                              PASS
flagged entries all carry a note              PASS
no 'clear' entry hides an OCR note            PASS
headword traceable in its original_text       PASS   (2 of 15,116)
```

It also opens the PDF and confirms sampled headwords really appear on their
recorded page — 15/15 on the last run.

Two items are reported for human review rather than failed automatically:
`are` and `all` look like English words but sit in Kapampangan sources. `are`
is a genuine Kapampangan word ('hay, straw'; Filipino *dayami*) — a homograph,
not an extraction error. `all` in the Mirikitani glossary is unresolved.

Note also that `Pilipino` on Samson p555 is a **real headword**
("*Pilipino.* (Sp. Filipino), n. any native or citizen of the Philippines"),
not a column header. The verifier scopes that check to the glossaries so it
does not delete a valid entry.

---

## What this does and does not give your thesis

**Gives you:** 12,929 unique headwords with definitions and page-level
provenance — roughly **4× the 3,109 roots** you had. This is the raw material
for the Lexicon Dictionary.

**Does not give you:** roots, affixes, segmentations, or gold morpheme
boundaries. That is deliberate — it is the next stage, and it needs a
Kapampangan speaker.

**Two things to know before you use it:**

1. **Samson is written in the Spanish-era orthography** — `acu`, `cacu`,
   `manğacû`, `quing`. Your running corpus uses `aku`, `kaku`, `king`. The
   `orthography_rules.tsv` in `data/lexicon/` handles the main mappings, but
   this dictionary will need the rules applied before its headwords match your
   corpus.
2. **Samson defines in English, not Filipino.** For Kapampangan→Filipino glosses
   the trilingual wordlist is your source (2,944 entries with a Pilipino
   column), and its Pilipino column is the one that drifts — check the flags.

---

## Next

1. Review the alignment-flagged entries (the `Pilipino gloss not confidently
   aligned` and `Two-column glossary` notes). Everything else can wait.
2. Merge Samson headwords into `data/lexicon/roots.tsv` after applying the
   orthography rules — expect segmenter coverage to rise well past the current
   73%.
3. Take the affix inventory from the Forman grammar, which was deliberately not
   auto-extracted.
