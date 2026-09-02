# External vocabulary verification (user-supplied AI-generated reference)

## Source and why it needed verification, not direct use

`resources/filipino_kapampangan_parallel_corpus.md` was supplied by the
user on 2026-08-26. Direct comparison against this experiment's own
PLD-derived `reports/matched-pairs.csv` found extensive, precise, verbatim
overlap -- 20 of the document's 214 numbered items reproduce this
experiment's own sentence pairs exactly, including specific analytical
choices (a cross-domain pairing that took manual PLD analysis to discover)
and exact accented-character transcriptions. The user confirmed the
document is AI-generated. That overlap is therefore not independent
evidence -- it is very likely this session's own prior output reflected
back -- and per user decision, only non-overlapping items were treated as
candidates, with every one individually verified against this project's
existing evidence before acceptance.

## Method

`build_external_vocab_pairs.py` classifies every one of the document's 214
items as accepted, excluded, or duplicate-of-an-existing-pair; the script
asserts every item falls into exactly one bucket (`missing` list), so
nothing can silently fall through unclassified. Acceptance requires at
least one of:

- **`dictionary_attested`**: the PAM word/root appears in this project's
  own existing attestation evidence (`word-evidence.csv` and/or
  `training-lexicon.json`'s roots list), checked programmatically via
  `verify_external_vocab.py`.
- **`transparent_compound`**: not attested as a whole surface form, but a
  fully regular, standard-pattern morphological compound of attested parts
  (numeral compounding, `apu` + gender particle for grandparent terms).
- **`pld_corroborated`**: independently confirmed by this session's own
  direct reading of the raw PLD archive text in Phase 2 -- the strongest
  practical tier available, since it is this project's own primary-source
  reading, not a third-party claim.
- **`project_established`**: directly confirmed by this project's own
  prior adjudicated findings (the 2026-08-25 Phase 1 morphology
  adjudication, or established discussion elsewhere in this repo, e.g. the
  `-um-` infix work on "Sumulat").

Where a document cell offers multiple alternates (e.g. `Kambal / Cacambal`)
and only one is verified, the accepted pair uses only that alternate --
enforced by an `apply_override` check that the selected text is an exact
substring of the original cell, so an override can only *select* existing
text, never introduce new text. PAM/FIL text is otherwise never hand-typed:
every pair is referenced by its `source_item_num` and looked up
programmatically from the parsed table.

## Result

**182 pairs accepted** (85 high-confidence, 97 medium-confidence) out of
214 document items; 14 rows in `reports/external-vocab-excluded.csv`,
each with a stated reason (13 genuine exclusions; the 14th, item 87, is
kept as an explanatory note pointing to its own now-accepted entry rather
than removed, so the audit trail of both alternates -- `Bunsso` accepted,
`Anaktian` still unattested -- stays visible); 20 identified as exact or
near-exact duplicates of existing PLD-derived pairs (silently dropped, no
new information).

Verification-basis breakdown: 110 dictionary-attested, 58 PLD-corroborated
(independently confirmed via this session's own direct archive reading --
notably stronger than plain dictionary lookup), 10 project-established
(directly confirmed by prior adjudicated findings elsewhere in this repo),
4 transparent compounds.

**Correction (2026-08-28)**: item 87 (`Bunso`/`Bunsso`, "youngest child")
was originally excluded as uncorroborated. A direct full-text search of
Forman (1971), Bergaño (1732/Samson translation), and Samson (2011) --
tooling gained in a later session, not available when this document was
first verified -- found it confirmed correct (Bergaño p.124: "BUNGSO.
Strictly speaking, the youngest child, or the youngest among siblings...").
Moved from excluded to accepted (181 -> 182). The same pass re-checked the
other three uncorroborated exclusions and the item 118 conflict below;
all three (`Gipang`, `Binti`, `Mahina`) held up as correctly excluded,
`Binti` now with a definitive citation (Bergaño p.111: "BINTI. Noun,
Courage, manliness" -- confirmed wrong, not merely unattested). See
`AGENT_CONTEXT.md`'s 2026-08-28 Decisions entries for the full pass.

## Concrete errors caught in the source document

Verification is not a formality here -- it caught real problems in the
AI-generated source:

- **Item 118** claims PAM `Palakingkingan` = "pinky finger" (pairing it
  with FIL `Kalingkingan`), against this experiment's own PLD-derived
  `pldpair_036`, which claims `palakingkingan` = ring finger (an inference
  from the FIL synonym `palasingsingan`, "singsing" = ring, not a
  dictionary citation). **Update (2026-08-28)**: direct full-text search
  of Forman, Bergaño, and Samson (2011) found zero hits for
  `palakingking`/`palasingsing` in any of them -- neither claim is
  attested by any primary source. (The originally-cited "corroboration,"
  `pldpair_037`'s `malingmingan` = pinky, was itself found wrong in the
  same pass -- Bergaño glosses `Malingmingan` as "temples," not a finger --
  and has been removed from `build_matched_pairs.py`.) Genuinely
  unresolved on both sides, not a settled conflict; still excluded here,
  logged in `reports/external-vocab-excluded.csv`.
- **Item 109** claims PAM `Lupa` = "face," directly contradicted by the
  same document's own **item 145**, which uses `Lupa` for "earth/ground" --
  a far more linguistically plausible cognate meaning, and internally
  inconsistent with item 109's own claim. Excluded.
- **Item 167** offers `Magsali` as an alternate for "to sell," which
  contradicts the same document's own **item 166**, using `Sali`/`Sumali`
  for "to buy" -- a likely buy/sell mix-up. The attested, uncontradicted
  alternate `Magtinda` was kept instead.
- **Item 66** offers `Labing-addua` as an alternate for "twenty" -- but
  that literally means "twelve" per the document's own **item 65** (a
  clear copy-paste error). The correct alternate `Adduang pulu` (two-tens)
  was kept instead.
- **Item 108** offers `Tuli` as an alternate for "ear," which most
  plausibly means "circumcision" in Kapampangan/Tagalog, not "ear" --
  excluded as a likely error; the attested `Balugbug` was kept.

Two items (**121**, **207**) turned out to fill genuine gaps this
session's own earlier PLD close-reading left unmatched -- e.g. item 207
supplies a FIL translation for a PAM sentence
(`Nucarin ya ing seli cung lapis nandin?`) seen in the raw
`Utt_Interrogatives.txt` data but never matched during Phase 2's first
pass, and its verb root (`seli`/`sali`, "bought"/"buy") is independently
confirmed by this project's own 2026-08-25 Phase 1 adjudication.

## Status

Silver, not gold: even `high`-confidence pairs here reflect attested word
forms plus this reviewer's own linguistic judgment and cross-referencing
against this project's existing evidence -- not independent
native-speaker/linguist review, and not (except for the `pld_corroborated`
and `project_established` tiers, and now item 87 specifically, which
carries a direct Bergaño page citation from the 2026-08-28 pass) primary-
source page citation the way `internet_root_reconciliation_v1` achieved
for the training lexicon. That 2026-08-28 pass did add direct
dictionary-page verification for a handful of specific disputed/excluded
items (87, 106, 112, 118, 198 -- see above), but the bulk of the 182
accepted pairs still rest on the `dictionary_attested`/`pld_corroborated`
form-level checks described earlier in this report, not a page-by-page
citation for every entry. Not yet spot-checked by the user, unlike the
PLD-derived sentence pairs.
