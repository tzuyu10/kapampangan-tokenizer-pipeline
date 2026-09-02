# Parallel extraction v1 (Phase 2, initial pass)

This isolated experiment builds a real PAM-FIL sentence-pair alignment from
the raw Philippine Languages Database (PLD) archive
(`D:\Coding\thesis\1773845964108-up-dsp-pld.tar.gz`, 48GB, not extracted --
see below), replacing the naive same-elicitation-domain-position cross-
matching that `translation_gold_v1` already found to be mostly wrong.

## What the archive actually is (corrects an assumption in the original
## Phase 2 mandate)

The archive is **not** parsed text -- it is raw per-speaker WAV recordings
(10 languages: `BIK CEB ENG FIL HIL ILO PAG PAM TSG WAR`, confirmed by a
full `tar -tzv` listing) plus one `.log` session file per speaker listing
which elicitation prompt each recording answers. No other file types exist
in the archive. A prior session (per
`curated_research_dataset/README_pld_kapampangan_datasets.md`) already
streamed the whole archive once without extracting it and parsed every
`.log` file's prompt text into two CSVs this experiment copies byte-for-byte
into `resources/`:

- `pld_prompt_entries_pam_fil.csv` (114,438 rows: 63,418 PAM + 51,020 FIL) --
  one row per individual speaker recording.
- `pld_prompt_inventory_pam_fil.csv` (1,924 rows) -- deduplicated
  **canonical prompt slots**: one row per `(lang, source_name_normalized,
  prompt_ordinal)`, with `canonical_text` (the most common transcription
  variant) and an `observed_variants` count.

Since this covers every piece of text the archive contains, **no extraction
of the 48GB archive was necessary or performed.** Disk space is a non-issue
for this pass.

## Why ordinal-position matching fails, precisely

`prompt_ordinal` is an elicitation **slot number**, not a stable per-item
index -- many different speakers each answer the same slot with their own
phrasing (hence `observed_variants` of 40-60+ per slot). Worse, even at the
canonical (deduplicated) level, the PAM and FIL elicitation sessions
numbered their slots **independently**: e.g. slot 5 of `Utt_Greetings.txt`
is "Merry Christmas" on the PAM side and "I apologize for my mistake" on the
FIL side. Slot *counts* per shared-named domain match exactly (e.g.
`Utt_Medical.txt`: 22 PAM slots = 22 FIL slots), which is why order-guess
matching looked plausible, but slot *content* is independently ordered.

## Methodology used here

Direct close reading, the same manual method `translation_gold_v1` used for
its MT-pair triage -- no automated similarity model. For every candidate
domain (a `source_name_normalized` file appearing on both the PAM and FIL
side, or a set of files covering the same narrative), every canonical slot
on both sides was read in full and matched by meaning, not position. Every
matched pair is recorded as a `(pam_domain, pam_ordinal, fil_domain,
fil_ordinal)` reference into the copied canonical inventory -- **the actual
Kapampangan/Filipino text is never hand-retyped**, only looked up
programmatically by `build_matched_pairs.py`, to eliminate any risk of
corrupting accented characters through manual transcription.

See `reports/parallel-extraction-summary.md` for the full domain-by-domain
methodology, results, and an honest accounting of which domains were
confirmed parallel, confirmed non-parallel, or not yet attempted.

## Current result (every identified candidate domain processed, user-reviewed)

**38 pairs** (33 high-confidence, 5 medium-confidence) from 13 domains read
and matched: the 6 sentence-level domains (`Utt_Greetings.txt`,
`Utt_Salawikain.txt` proverbs, `Utt_Essay.txt`, five PAM story files vs.
FIL's interleaved `Utt_Story.txt`, `Utt_CommonExpressions.txt`,
`Utt_Interrogatives.txt`) plus 6 word-level Iso domains and the numeric
`Iso_Ordinal.txt`. `Utt_Letter.txt` (same rhetorical register on both sides
but no overlapping excerpted sentences) and `Iso_MinPairs.txt`
(structurally not translatable -- within-language phonetic contrast pairs)
were fully read and contributed zero pairs, for principled reasons. This is
substantially smaller than the ~13,000-pair thesis-level target from the
original mandate -- see the summary report's honest scope discussion. It is
also a categorically different quality tier than any PAM-FIL data this
project has found before (previous best: 8 distinct correct pairs out of
250 candidate rows in `translation_gold_v1`).

**User spot-check (2026-08-26)** reviewed all 28 sentence-level pairs and
found the methodology sound: one pair (a proposed proverb match) was
rejected as two genuinely different proverbs with different morals sharing
only a surface "deep/shallow" vehicle, not a paraphrase of the same lesson
-- removed rather than kept at reduced confidence. Three further pairs were
confirmed as valid translations but annotated with real grammatical
caveats a linguist would want visible (a politeness-register mismatch, a
declarative/interrogative mood shift, and a verb-aspect shift) -- see each
pair's `note` field in `reports/matched-pairs.csv`. The word-level Iso
pairs (11, after the correction below) have not yet been reviewed by the
user.

**Correction (2026-08-28)**: a direct dictionary check (see
`AGENT_CONTEXT.md`'s 2026-08-28 Decisions entries) found that one of the
word-level Iso pairs from the first pass -- PAM `Malingmingan` paired with
FIL `kalingkingan` as "pinky finger," justified only by a shared
`-lingking-` surface pattern -- was wrong. Bergaño's 1732 dictionary
glosses `MALINGMINGAN` as "the temples / sides of the head," not a finger
at all. Removed (39 -> 38 pairs). A second pair (`palakingkingan` = "ring
finger") was downgraded from high to medium confidence in the same pass:
full-text search of Forman, Bergaño, and Samson (2011) found zero hits for
`palakingking`/`palasingsing` in any of them, so this claim -- like the
external document's competing "pinky" claim for the same word -- remains
unattested by any primary source available to this project.

Everything produced here is silver / close-reading-verified, not
independent linguist/native-speaker gold.

## External vocabulary track (user-supplied AI-generated reference)

On 2026-08-26 the user supplied
`D:\Downloads\filipino_kapampangan_parallel_corpus.md`, a 214-item PAM-FIL
phrasebook/vocabulary reference. Direct comparison found it overlaps
verbatim with 20 of this experiment's own PLD-derived pairs -- the user
confirmed it is AI-generated, so that overlap is not independent evidence.
Per user decision, only the non-overlapping items were treated as
candidates and individually verified against this project's own existing
dictionary/attestation evidence before acceptance (never accepted just for
appearing in the document). Result: **182 pairs accepted** (85
high-confidence, 97 medium), 14 excluded with a stated reason (including
one flagged, unresolved conflict with this experiment's own PLD analysis).
**Correction (2026-08-28)**: one of the four originally-uncorroborated
exclusions (`Bunso`/`Bunsso`, "youngest child") was itself wrong -- direct
dictionary verification confirmed it via Bergaño's 1732 dictionary p.124
("BUNGSO. Strictly speaking, the youngest child...") and it was moved from
excluded to accepted (181 -> 182). See `reports/external-vocab-verification.md`
and `AGENT_CONTEXT.md`'s 2026-08-28 Decisions entries for the full
dictionary-verification pass (also downgraded/reasoned-through: item 118's
`palakingkingan` conflict, above).
See `reports/external-vocab-verification.md` for full methodology,
including concrete errors this verification pass caught in the source
document. This track is kept in separate files from the PLD-derived pairs
above (different provenance, different verification method) -- see
`reports/external-vocab-pairs.csv` and `reports/external-vocab-excluded.csv`.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v1\build_matched_pairs.py
.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v1\verify_external_vocab.py
.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v1\build_external_vocab_pairs.py
```

`build_matched_pairs.py` reads `resources/pld_prompt_inventory_pam_fil.csv`
and the hand-curated `PAIRS` list inside the script; writes
`reports/matched-pairs.csv` and `reports/matched-pairs-stats.json`. It
raises immediately if any referenced `(lang, domain, ordinal)` key is
missing from the inventory, which also serves as a consistency check on
every match recorded.

`verify_external_vocab.py` parses
`resources/filipino_kapampangan_parallel_corpus.md`'s tables and checks
every PAM token against `word-evidence.csv`/`training-lexicon.json`;
writes `reports/external-vocab-candidates.csv` (the raw attestation scan).
`build_external_vocab_pairs.py` applies the actual accept/exclude
decisions on top of that scan; writes `reports/external-vocab-pairs.csv`
and `reports/external-vocab-excluded.csv`. It asserts every one of the
document's 214 items is classified as accepted, excluded, or a duplicate
of an existing pair -- nothing can silently fall through unclassified.

## Gemini-generated 500-sentence batch (mechanical check only)

On 2026-08-26 the user also supplied a 500-sentence Filipino-Kapampangan
batch directly in chat (no file, no citation), confirmed AI-generated
(Google/Gemini), covering negation, tense/aspect, subordination,
comparatives, and everyday/workplace/travel/health registers -- genuinely
new content, not overlapping the PLD-derived pairs. Given the batch's scale
and grammatical complexity, full per-item verification (as done for the
214-item file) isn't feasible; per explicit user decision, only a
mechanical word-level attestation check was run, with no sentence-level
correctness judgment. Saved verbatim to
`resources/gemini_kapampangan_sentence_batch.md` with a provenance note.

**Result**: 86.8% of PAM content tokens (4,518/5,207) are attested in this
project's existing evidence; only 18% of sentences (90/500) have every
content word attested -- expected at this scale, since even a high
per-word rate compounds down across ~10-word sentences. More notably, two
of the most frequent unattested tokens are **objectively untranslated
Tagalog**, verifiable within the batch itself: `Bagaman` ("although")
appears untranslated in 8 sentences while 14 others correctly use genuine
Kapampangan `Maski`/`Agyang` for the same meaning; the full Tagalog
spelling `sasakyan` ("vehicle") appears in 8 sentences, more often than the
Kapampangan-contracted `saskyan` (4 sentences) used elsewhere in the same
batch. See `reports/gemini-batch-word-attestation.md` for the full
breakdown. **No sentences from this batch have been accepted into the pair
dataset** -- this is a coverage signal only, not a verification pass;
treating any sentence here as reliable would need native-speaker/linguist
review this project has consistently deferred elsewhere.

Reproduce: `.\.venv\Scripts\python.exe .\experiments\parallel_extraction_v1\verify_gemini_batch.py`
