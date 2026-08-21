# AI-assisted candidate morphological lexicon

> **This is a CANDIDATE lexicon.** Every record carries
> `"validation_status": "unvalidated"`. It has not been reviewed by a native
> Kapampangan speaker or a linguist and must not be used as a validated
> linguistic resource until it has been.

```bash
python scripts/22_build_candidate_lexicon.py
python scripts/23_qc_candidate_lexicon.py --pdf-dir "C:/Users/Gabo/Downloads/DATASET/UNANNOTATED"
```

Output: `data/lexicon_candidate/candidate_lexicon.jsonl` — **14,209 entries**.

---

## What is in it

| Morphological status | Entries | Share |
|---|---|---|
| `unknown` | 10,257 | 72.2% |
| `simple` | 2,805 | 19.8% |
| `derived` | 579 | 4.1% |
| `variant` | 542 | 3.8% |
| `compound` | 26 | 0.2% |
| `inflected` | 0 | — |

| Annotation source | Entries | Confidence |
|---|---|---|
| `dictionary_explicit` | 3,485 | high |
| `AI_proposed` | 467 | 242 medium, 225 low |
| `unknown` | 10,257 | low |

3,384 entries have a proposed root. 3,304 have a segmentation.
**Zero** entries have a root silently copied from the headword outside
`status: simple`.

**72% `unknown` is the intended result, not a shortfall.** The brief says an
incomplete but defensible annotation beats an incorrect one. Two thirds of these
entries are cases where the dictionary says nothing about structure and no
dictionary-attested affix strips to a form the dictionary also lists. Guessing
there would have produced exactly the kind of invented morphology the brief
forbids.

---

## How an analysis is licensed

No external knowledge of Kapampangan is used as evidence. That constraint has
teeth, and it is worth showing why.

### Why plain string matching was rejected

The obvious approach is to scan the 9,030 Samson headwords for
`long = affix + short` where both are headwords. Run it and the "top prefixes"
come out as:

```
p-    94 hits    e.g. plato   = p- + lato
t-    87 hits    e.g. tapis   = t- + apis
s-    79 hits    e.g. silo    = s- + ilo
-s   122 hits
-c    95 hits
```

These are string coincidences. A lexicon built on them would be worthless, and
it would look plausible enough to survive casual review — which is worse.

### What was used instead

Samson prints paradigms *inside its own entries*:

```
abut.  Active verb, mamabut, minabut, mabut, and its infinitive, manabut,
       to uproot, or pull out ...
```

The dictionary is asserting here that *mamabut*, *minabut*, *mabut* and
*manabut* belong to the headword *abut*. That is a fact stated by the source,
not an inference. 2,011 entries carry such statements, yielding **6,806
explicit (headword → form) observations**.

Counting the string operations across those 6,806 observations gives an affix
inventory that looks like Kapampangan rather than like noise:

| Kind | Licensed affixes (count of explicit statements supporting each) |
|---|---|
| prefix | `i-` (186), `man-` (138), `min-` (60), `m-` (53), `mag-` (46), `in-` (40), `mum-` (35) |
| infix | `-in-` (306), `-um-` (73), `-ar-` (31) |
| suffix | `-an` (103), `-n` (11), `-nan` (8), `-anan` (5) |
| circumfix | `pa-…-an` (20), `in-…-an` (19), `pi-…-an` (14), `pag-…-an` (10), `pig-…-an` (6) … |
| reduplication | `ta~` (98), `la~` (57), `tu~` (54), `pa~` (33), `ca~` (30) … |

Frequency floors: prefix/infix ≥ 20, suffix ≥ 5, circumfix ≥ 5,
reduplication ≥ 3. Below the floor an affix may not license anything.

Two implementation details that mattered:

**Reduplication is tested before prefixation.** `tabac → tatabac` is a copy of
the root's own opening syllable, not a `ta-` prefix. Testing prefixes first
would have filled the inventory with dozens of phantom CV prefixes — and
`ta~`, `la~`, `tu~` are precisely the ones that would have appeared.

**4,660 of the 6,806 explicit pairs (68%) are not plain concatenation.**
`abono → abonuan`, `acû → inacûan`, `bala → belan`. These are morphophonemic
alternations. The dictionary still tells us the root, so the root is recorded —
but `segmentation` is left empty, because the morpheme boundaries genuinely
cannot be placed from the string alone.

### The three levels of claim

| `annotation_source` | When | Confidence |
|---|---|---|
| `dictionary_explicit` | Samson prints the relationship | high |
| `AI_proposed` | Stripping a licensed affix leaves a form that is itself a headword | medium, or low for short/rare affixes or cross-source matches |
| `unknown` | Neither | low, `root: null`, `segmentation: ""` |

Order of evaluation per entry:

1. Is this headword printed in another headword's paradigm? → `derived`, root =
   that headword, **dictionary_explicit**
2. Does this headword print a paradigm of its own? → `simple` (the dictionary
   treats it as a base), **dictionary_explicit**
3. Does the dictionary give an explicit alternative spelling? → `variant`,
   **dictionary_explicit**
4. Hyphenated, with every part a headword? → `compound`, **AI_proposed**
5. Does one licensed affix strip to a form that is itself a headword? →
   `derived`, **AI_proposed**
6. Otherwise → `unknown`, root `null`

---

## Reading an entry

```json
{
  "entry_id": "samson:p0018:012:acayan",
  "headword": "acayan",
  "definition": "...",
  "part_of_speech": ["noun"],
  "syllables": [],
  "morphology": {
    "status": "derived",
    "root": "acay",
    "prefixes": [], "infixes": [], "suffixes": ["-an"],
    "circumfixes": [], "clitics": [], "compound_parts": [],
    "reduplication": null,
    "segmentation": "acay + -an"
  },
  "spelling_variants": [],
  "derived_forms": [],
  "inflected_forms": [],
  "evidence": "Heuristic inference, not stated by the dictionary. Removing -an leaves 'acay', which is itself a headword in this dictionary (page 18). -an is attested in 103 explicit headword-to-form statements elsewhere in the same dictionary. Requires validation.",
  "annotation_source": "AI_proposed",
  "confidence": "medium",
  "ocr_status": "needs_review",
  "source": { "dictionary": "Samson, Kapampangan Dictionary", "page": 18,
              "original_text": "acayan. n. ..." },
  "validation_status": "unvalidated",
  "notes": "..."
}
```

Every `evidence` string names the specific headword and page that supports the
claim, so a validator can open the PDF and check it in seconds.

`syllables` is empty throughout: none of these sources syllabify. Where a source
does provide syllables they go in that field and are **never** reread as
morphemes — syllabification and morphological segmentation are different things.

---

## Cross-source caveat

All morphological evidence comes from Samson, the only source that prints
paradigms. Entries from the wordlists (trilingual, Mirikitani) can still be
matched against Samson's lemma list, and when that happens the evidence string
says so explicitly:

> NOTE: this entry is from trilingual; the supporting evidence is from Samson,
> a different dictionary using the Spanish-era orthography. Cross-source
> match — verify the spelling systems agree.

Those entries are capped at `low` confidence. Samson writes `acu`, `quing`,
`cacu`; the wordlists write `aku`, `king`, `kaku`. A cross-source match may be
comparing two spelling systems.

---

## Quality control

`scripts/23_qc_candidate_lexicon.py` runs all 24 checks from the brief.
**24/24 pass**, and 10/10 sampled `dictionary_explicit` analyses were verified
against the original PDF page.

Four of the checks initially failed against correct data, which is worth
recording because the same traps will catch a reviewer:

- **`tubig` is a real Samson headword** (*"tubig. Tubigtubigan. n. pimples which
  are watery"*), not a Filipino definition word that leaked in. Homographs
  across the two languages are expected.
- **Mirikitani prints verb roots in full capitals** (`ALIKABOK`, `DAGDAG`,
  `BATING`) as an editorial convention. All-caps does not mean page header.
- **`Pilipino` on Samson p555 is a real headword**, not a column title.

Two were genuine bugs and are fixed:

- Two entries took an English word from inside a definition as a headword
  (`someone`, `something`). Added to the extractor's stopword list.
- The `dictionary_explicit` branch wrote the raw string difference straight into
  the affix fields, producing artefacts like `suyi-` and `pilub-…-an`. The
  dictionary asserts the *relationship*, not that the leftover string is a
  morpheme — so the root is kept and the affix is now withheld unless it is
  independently attested.

---

## What a validator should do first

Sorted by value per hour:

1. **The 467 `AI_proposed` entries.** These are the ones where the machine made
   a claim the dictionary did not. Every one names its evidence and page. A few
   hours of review either promotes them to validated or removes them.
2. **The 242 `medium`-confidence ones inside that set** — highest yield.
3. **The `derived` entries with an empty `segmentation`** (the 68%
   morphophonemic cases). The root is dictionary-stated and reliable; only the
   boundary placement is missing, and a speaker can supply it quickly.
4. **The reduplication inventory.** `ta~`, `la~`, `tu~`, `ca~` were derived
   mechanically from copy patterns. Confirm they are reduplication and not
   prefixation before the segmenter relies on them.
5. Leave the 10,257 `unknown` entries alone until the rest is done. They are
   correctly marked as carrying no analysis.

Set `validation_status` to `validated` (or `rejected`) as you go, and record the
validator's name and date in `notes`. Nothing in this pipeline will overwrite
those fields.

---

## Not yet merged into the working lexicon

`data/lexicon/*.tsv` is what the segmenter actually loads. This candidate
lexicon is **not** in it. Merging needs two decisions first:

1. **Orthography.** Samson is Spanish-era. The corpus is modern. The rules in
   `data/lexicon/orthography_rules.tsv` have to be approved before Samson
   headwords will match corpus tokens.
2. **Which confidence levels to admit.** Admitting `AI_proposed / low` into the
   lexicon means unvalidated guesses shape Morph-BPE training, and that will be
   asked about at your defence. The defensible default is
   `dictionary_explicit` only, with `AI_proposed` added after validation.
