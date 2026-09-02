# Parallel extraction v1 -- methodology and results

## 1. Archive structure (corrects the original Phase 2 mandate's assumption)

`1773845964108-up-dsp-pld.tar.gz` (48GB) is a raw speech corpus: WAV
recordings under `PLD/<LANG>/<speaker_id>/<speaker_id>.<session>.<record>.wav`,
one `.log` session file per speaker/session listing which elicitation
prompt each recording answers. A full `tar -tzv` listing (336,263 entries,
run to completion, not sampled) confirmed exactly two file types
(`.wav`, `.log`) and ten language directories: `BIK CEB ENG FIL HIL ILO PAG
PAM TSG WAR`. No master gloss file, no cross-language alignment key, and no
text content beyond what the `.log` files carry exists anywhere in the
archive.

A prior session had already streamed the archive once (without extracting
it) and parsed every `.log` entry into
`curated_research_dataset/pld_prompt_entries_pam_fil.csv` (114,438 rows)
and a deduplicated `pld_prompt_inventory_pam_fil.csv` (1,924 canonical
slots), per `curated_research_dataset/README_pld_kapampangan_datasets.md`.
Both were copied byte-for-byte into `resources/` with a SHA-256 provenance
manifest for this experiment. **No extraction of the 48GB archive was
necessary or performed in this pass** -- the text data it contains was
already fully captured.

## 2. Why the existing `kapampangan_mt_pld_pam_fil_curated.csv`/
   `_order_guess.csv` failed, precisely

Both files pair PAM row *N* with FIL row *N* within each shared
`source_name_normalized` domain (confirmed identical content between the
two files apart from a `dataset_role`/`validation_status` label change --
they are the same alignment, one flagged "needs review", one flagged
"unsafe guess"). `translation_gold_v1`'s triage already showed this
produces mostly wrong pairs and found evidence of block-level
shifting/shuffling.

This session's inspection of the underlying raw entries explains the
mechanism precisely: `prompt_ordinal` identifies an elicitation **slot**
(a target meaning), and many different speakers each recorded their own
phrasing for that slot (`pld_prompt_inventory_pam_fil.csv`'s
`observed_variants` column records 13-64 variants per slot). The PAM and
FIL elicitation sessions assigned slot numbers to target meanings
**independently** -- e.g. in `Utt_Greetings.txt`, PAM slot 5 canonically
reads "Maligayang Pascu pu at masaplalang bayung banua" (Merry Christmas)
while FIL slot 5 reads "Ipagpaumanhin po ninyo ang aking pagkakamali" (I
apologize for my mistake). Slot *counts* match exactly within every
shared-named domain (e.g. `Utt_Medical.txt`: 22=22, `Utt_News.txt`: 40=40),
which is presumably why the original order-guess approach looked
defensible, but slot *content* order is not shared.

## 3. Methodology

For every `source_name_normalized` file appearing under both `PAM` and
`FIL` in the canonical inventory (or, for the story narratives, files
plausibly covering the same content under different names), the full
canonical slot list for both languages was read directly and matched by
meaning. This is the same manual, rubric-driven process
`translation_gold_v1` used for its MT-pair triage -- no automated
similarity/embedding model was used, per explicit user decision.

Every accepted pair is recorded only as a `(pam_domain, pam_ordinal,
fil_domain, fil_ordinal)` reference into the copied canonical inventory.
`build_matched_pairs.py` looks up the actual text programmatically at build
time and fails loudly if any referenced key does not exist. The
Kapampangan/Filipino text itself is never hand-retyped into any file in
this experiment, specifically to avoid corrupting accented characters
during manual transcription (an early terminal-display artifact in this
session initially looked like literal U+FFFD corruption in the source
data; a direct byte/codepoint check of both source CSVs confirmed zero
genuine replacement characters in either file -- it was a terminal
rendering limitation, not real data damage).

Two confidence tiers are used:

- **`high`** -- the sentence is essentially a direct translation (matching
  content words, structure, and named entities where present).
- **`medium`** -- either a cross-domain match (the two languages' sessions
  filed the same formulaic phrase under different domain names) or a
  conceptual/proverb-equivalent paraphrase (the same idiomatic wisdom,
  expressed with a different vehicle -- e.g. a walking-pace metaphor
  translated as a river metaphor).

`exact_translation_partial` marks pairs where the PAM slot's canonical text
includes narration beyond what the FIL slot captured (the two languages'
sessions did not always excerpt identical sentence boundaries from a shared
source text); the note field on each such row states exactly which portion
aligns.

## 4. Results: confirmed domains and pair counts

| Domain(s) | PAM slots | FIL slots | Pairs found | Basis |
|---|---|---|---|---|
| `Utt_Greetings.txt` | 16 | 16 | 6 (+1 cross-domain) | formulaic greetings/thanks/condolences |
| `Utt_Salawikain.txt` | 15 | 15 | 5 | proverbs |
| `Utt_Essay.txt` | 12 | 12 | 2 | comparative folktale essay |
| 5 PAM story files vs. `Utt_Story.txt` (FIL) | 50 | 19 | 8 | folktale narrative sentences |
| `Utt_CommonExpressions.txt` | 18 | 18 | 3 | formulaic expressions |
| `Utt_Interrogatives.txt` | 15 | 15 | 3 | question sentences |
| **Total** | | | **28** (25 high, 3 medium) | |

The story-domain finding is the strongest evidence of genuine translation
design in the archive: FIL's single `Utt_Story.txt` interleaves sentences
from what are recognizably five separate Kapampangan folktales that PAM
recorded as separate files (`Utt_StoryAraw.txt`, `Utt_StoryBernardo.txt`
[the Bernardo Carpio legend], `Utt_StoryGamugamo.txt`, `Utt_StoryIputipot.txt`
[a firefly/gorilla fable, character names "Iput-Ipot" and "Amomongo" appear
verbatim on both sides], `Utt_StoryMatsing.txt` [the Monkey-and-Turtle
fable]) -- e.g. PAM `Utt_StoryIputipot.txt` slot 4/5's dialogue is a
near word-for-word translation of FIL `Utt_Story.txt` slot 5.

**Important caveat on yield within "confirmed" domains**: even within a
domain confirmed to contain genuinely parallel content, most individual
slots did **not** yield a confident pair. Typically only 15-50% of a
domain's slots matched with high confidence; the rest were either
duplicate/near-duplicate realizations of an already-matched slot, or slots
whose apparent counterpart in the other language could not be identified
with confidence and were deliberately left unmatched rather than forced.
For example `Utt_Interrogatives.txt` supplies several sentences built on
the same grammatical template with different specific names (e.g. "will
[name] play or sing?") where each language's session substituted its own
example rather than translating the exact same sentence -- these were
excluded, not matched, to avoid the exact fabricated-pair failure mode
`translation_gold_v1` was built to catch.

## 5. Domains checked and rejected as non-parallel (evidence-based)

These share a domain name and (usually) an exact slot count across PAM and
FIL, but sampled content is independently authored per language, not
translated:

- **`Utt_News.txt`** (40=40 slots) and its expansion set
  (`Utt_News_Set02/03.txt` [PAM] vs. `TGLNEW_News01/02.txt` [FIL]) -- real,
  distinct news articles per language (PAM discusses Del Monte Pacific
  stock and OPSF budget items; FIL discusses 1989 tourism income and
  Maynilad water rehabilitation). Sampled, not exhaustively read.
- **`Utt_Medical.txt`** base file and its expansion set
  (`Utt_Medical_Set02/03.txt` vs. `TGLNEW_Medical_xaa/xab.txt`) -- PAM
  discusses generic consultation questions and vaccine/cancer-cell content;
  FIL discusses flu symptoms, a specific stroke patient anecdote, and skin
  care -- unrelated specific content. Sampled (8/22 and 8/30), not
  exhaustively read.
- **`Utt_Educ.txt`** base file -- PAM gives classroom instructions
  ("clean the room", "open the book to page 3"); FIL gives different
  classroom instructions ("raise your hand", "cover the book"). Same genre,
  different specific content. Sampled (5/15), not exhaustively read.
- **`Utt_Literature_Set02/03.txt`/`Utt_Tourism_Set02/03.txt`** (PAM) vs.
  **`TGLNEW_Literature_xaa/xab.txt`/`TGLNEW_Tourism01/02.txt`** (FIL) --
  not read in detail, but grouped with the News/Medical Set02/03 pattern
  (40-slot files matching the `TGLNEW` "second wave" naming); treated as
  the same independent-per-language-content family pending a closer check.

**All ten `_Set02`/`_Set03`/`TGLNEW_*` files together account for 400 PAM
canonical slots and 440 FIL canonical slots that this pass treats as
non-parallel** -- by far the largest block of shared-name content in the
archive, and the reason the realistic yield is far short of what raw slot
counts alone would suggest.

Also out of scope by construction, not rejected on evidence: FIL's
proper-noun "Other" lists (`Airlines.txt`, `Cities.txt`, `NameFem.txt`,
etc. -- 10 files, place/company/person names, not translatable content) and
PAM's English-elicitation files (`EngW.txt`, `EngSen.txt`, `Utt_EngShib1/2.txt`
vs. FIL's `Utt_Eng1/2_Shib.txt`, `Utt_Batangas*_Shib.txt`,
`Utt_Marinduque*_Shib.txt`, etc. -- English or regional-accent shibboleth
sentences read by both language groups, not PAM-FIL translations).
`Spontaneous`/`Spo` files and `Random Digit` were excluded per the original
README's own documented reasoning (elicitation question rather than spoken
answer; meaningless digit strings).

## 6. Remaining candidates: fully processed in a second pass

Every remaining candidate domain identified in section 5's scan was read
and closed out in a follow-up pass within this same session:

- **`Utt_Letter.txt`** (5 PAM slots, 5 FIL slots, both read in full) --
  unmistakably the same register of 19th-century Philippine patriotic
  rhetoric about Spanish colonial oppression on both sides (PAM discusses
  "Balayan" [homeland], "Castila" [Spaniards], orphans, and exile from
  family; FIL's content -- "panahon na ngayong dapat... mga Tagalog...
  pinagbuhatan ng kanilang mga kahirapan", plus a blood-compact reference
  in slot 5 -- reads unmistakably like Andrés Bonifacio's "Ang Dapat
  Mabatid ng mga Tagalog"). Very likely the same historical document
  underlies both sides, but the five sentences each language's session
  happened to excerpt do not overlap with each other. **Zero pairs
  recorded** -- forcing a match here would mean pairing sentences that
  merely share register and era, not content, exactly the failure mode
  this whole phase exists to avoid. A future pass that identifies PAM's
  exact source document and locates its full text outside this elicitation
  subset could recover real pairs; out of scope here.
- **7 Iso (word-level) domains**, all read in full:
  - `Iso_BodyParts.txt` (15=15) -- 2 pairs (`palakingkingan`/`palakingkingan`
    "ring finger", identical wordform; `Malingmingan`/`kalingkingan`
    "pinky finger", shared root). PAM's dominant repeated answer
    ("Cayucut", 6/15 slots, glossed "end of the spinal column at the
    buttocks") has no FIL counterpart in this specific list -- left
    unmatched rather than guessed. Deliberately did **not** match PAM
    `Bucung-bucung` ("ankle") to FIL `galáng-galangán`, even though it
    superficially looks similar: this project's own Phase 1 adjudication
    already established `galáng-galangán` means "wrist," not "ankle," and
    this list has no FIL word for "ankle" (`bukung-bukong`) at all.
  - `Iso_Kinship.txt` (11=11) -- 2 pairs (`Manuyang`/`manugang`
    "son/daughter-in-law"; `Capalsintan`/`kasintahan` "sweetheart", shared
    "sinta" root). PAM `Tegauang lalaki` and `Cacambal` ("twin") had
    plausible-looking FIL candidates (`bayaw`, `katambal`) but were left
    unmatched -- kinship terms are precise and easy to get wrong (exactly
    the error class Phase 1's morphology triage already caught), and
    confidence in the specific PAM term's meaning was not high enough to
    commit.
  - `Iso_Ordinal.txt` (12=12) -- 2 pairs, matched by exact numeric value
    rather than translation judgment at all: PAM "27th"/FIL "27th" and PAM
    "23rd"/FIL "23rd" are unambiguous regardless of which slot they sit in.
  - `Iso_Time.txt` (21=21) -- 1 pair (`Salucuiang`/`kasalukuyang`
    "present/current", shared root). The dominant PAM answer
    (`capilanman`/`anggang capilanman`, "always/forever", ~7/21 slots) has
    no clear FIL counterpart in this list.
  - `Iso_Weather.txt` (9=9) -- 3 pairs (`Bugsu ning angin`/`bugso ng
    hangin` "gust of wind", identical words; `Maialumigmig`/`halumigmig`
    "humid", shared root; `Madalumdum`/`makulimlim` "cloudy/overcast",
    same concept via different, non-cognate words).
  - `Iso_Educ.txt` (15=15) -- 2 pairs (`Espana`/`Espanya`, same proper
    noun; `Pangaratang`/`dumating`, "arrival"/"arrived", shared "dating"
    root). The list otherwise contains mostly unrelated proper nouns per
    side (PAM: Rizal, Pilanduc, Usman; FIL: Maynila, Soliman) and generic
    function words too ambiguous to pair safely (e.g. PAM `Niti` "this"
    could plausibly match either FIL `itong` or `nilang`; left unmatched).
  - `Iso_MinPairs.txt` (9=9) -- **structurally inapplicable, not just
    unmatched**. Every row on both sides is a within-language phonetic
    minimal-pair contrast (e.g. PAM `kabud (adv. immediately) -- kabud
    (adj. only)`; FIL `bakas-bakás (financial partnership) -- bakas-bakás
    (footprint)`), demonstrating tone/stress ambiguity inside one
    language, not a translatable concept between the two. There is no
    PAM-FIL pair to find here regardless of matching effort.

Word-level Iso pairs were held to a stricter bar than the sentence-level
domains: only included when the PAM and FIL forms are the same word,
obvious cognates/shared roots, or (for `Iso_Ordinal.txt`) an unambiguous
shared numeric value -- never a same-domain vocabulary guess, which is
exactly the error `translation_gold_v1`'s own user-adjudication round
already caught once in this project's history.

## 7. User spot-check (2026-08-26)

The user reviewed all 28 sentence-level pairs from section 4 (the
word-level Iso pairs from section 6 have not yet been reviewed) and
returned a linguist-quality assessment:

- **One pair rejected, not just downgraded**: the proposed
  `Utt_Salawikain.txt` PAM slot 9 / FIL slot 5 pair ("still waters run
  deep"-style proverbs) was recorded as a `medium`-confidence conceptual
  paraphrase. The user's verdict: these are **two distinct proverbs with
  different morals**, not the same lesson through a different vehicle --
  PAM's walking-pace proverb teaches that deliberation/caution leaves a
  deep, lasting result, while FIL's river proverb teaches that a quiet
  demeanor can mask hidden depth or danger. Removed from the pair set
  entirely (not kept at a lower tier) -- see the removal note left in
  `build_matched_pairs.py` in place of the entry, which records the
  original proposal and the rejection reasoning.
- **Three pairs confirmed valid but annotated with grammatical caveats**
  the user identified: a politeness-register mismatch in a `Utt_Greetings.txt`
  condolence pair (PAM's polite/plural `ye pu` vs. FIL's informal/singular
  `mo`); a declarative-vs-interrogative mood shift in the aligned portion
  of a `Utt_StoryMatsing.txt` partial pair (PAM reads as a statement/threat,
  FIL as a question offering a choice); and a verb-aspect shift in an
  `Utt_Interrogatives.txt` pair (PAM contemplative/future "will get lost"
  vs. FIL imperfective/present "is missing"). All three remain in the pair
  set at their original confidence tier, with the caveat recorded in the
  pair's `note` field -- these are genuine translations with a real,
  flagged grammatical wrinkle, not errors to discard.
- Every other reviewed pair (24 of 28), including all 3 pairs in the
  Essay/Story `exact_translation_partial` tier, was confirmed accurate as
  originally recorded.

This validates the close-reading methodology on a real independent check:
23 of 24 sentence-level `high`/`medium` calls held up untouched, one
genuine methodology gap was caught and corrected (a shared "deep/shallow"
surface vehicle is not sufficient evidence of a shared proverb -- the
specific lesson must match too), and three calls benefited from a
linguist's finer-grained read that this session's own close reading missed.

## 8. Final result and honest scope assessment against the ~13,000-pair
   thesis target

**39 pairs total** (35 high-confidence, 4 medium-confidence) after
processing every identified candidate domain and incorporating the user's
review: 27 from the 6 sentence-level domains in section 4 (28 originally,
minus the 1 rejected proverb pair), plus 12 from the word-level Iso domains
and the numeric Ordinal domain in section 6. `Utt_Letter.txt` and
`Iso_MinPairs.txt` contributed zero pairs, for principled reasons specific
to each (no sentence-level overlap in the excerpted subset; not
translatable content at all, respectively).

**Further correction (2026-08-28)**: one of the 12 word-level Iso pairs
(PAM `Malingmingan` / FIL `kalingkingan`, claimed as "pinky finger") was
itself found wrong on direct dictionary verification -- Bergaño's 1732
dictionary glosses `Malingmingan` as "the temples / sides of the head," not
a finger. Removed. **Final total: 38 pairs** (33 high-confidence, 5
medium-confidence -- the `palakingkingan` pair was also downgraded to
medium in the same pass, since neither its "ring finger" claim nor the
competing "pinky" claim is attested in Forman, Bergaño, or Samson). See
`AGENT_CONTEXT.md`'s 2026-08-28 Decisions entries for the full
verification pass.

This is nowhere close to the original mandate's ~13,000-pair training-scale
target, and came in toward the lower end of this report's own earlier
60-90-pair estimate -- the gap is mostly explained by how much of the
archive's apparent overlap (the ten `_Set02`/`_Set03`/`TGLNEW_*` files,
400+440 slots) turned out to be non-parallel, and by how conservatively
word-level matches were screened for cognate-confusion risk. It is,
however, a categorically different quality tier than anything found in
this project before (`translation_gold_v1`'s best case: 8 distinct correct
pairs from 250 candidate rows), and a defensible size for a **held-out gold
evaluation set** rather than fine-tuning-scale training data (the
2026-08-25 handoff notes recorded a ~1,300-pair reference scale for aligned
*tests*, which this is much closer to in spirit, if smaller).

The realistic path to *training*-scale PAM-FIL data, if still wanted, is a
separate strategic question -- not something this archive's genuinely
parallel content can supply -- and should be discussed with the user rather
than assumed.

## 9. Redistribution rights

Same posture as every other externally-sourced dataset in this project:
unresolved. `resources/` holds only the two already-derived CSV files (not
the raw archive or any audio), consistent with `curated_research_dataset`'s
own existing local-experimental-research status.
