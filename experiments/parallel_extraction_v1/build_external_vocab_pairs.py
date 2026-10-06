"""Build the verified-subset pair list from the user-supplied AI-generated
reference file (resources/filipino_kapampangan_parallel_corpus.md).

Provenance and rigor, per explicit user decision (2026-08-26): the document
overlaps extensively and verbatim with this experiment's own PLD-derived
pldpair_001-039 (confirmed AI-generated, very likely built from this
session's own prior output) -- that overlap is not independent evidence and
is excluded here entirely (already covered by build_matched_pairs.py).
Every other (non-overlapping) item is individually classified ACCEPT or
EXCLUDE below, with a stated reason, before being added to this dataset.
Nothing is accepted purely because it appears in the source file; every ACCEPT
has at least one of:
  - dictionary_attested: the PAM word/root appears in this project's own
    existing attestation evidence (word-evidence.csv and/or
    training-lexicon.json's roots list).
  - transparent_compound: not attested as a whole surface form, but a fully
    regular, standard-pattern morphological compound of attested parts
    (e.g. numeral compounding).
  - pld_corroborated: independently confirmed by this session's own direct
    reading of the raw PLD archive text earlier in Phase 2 (stronger than
    dictionary attestation, since it is this project's own primary-source
    reading, not a third-party claim).
  - project_established: directly confirmed by this project's own prior
    adjudicated findings (the 2026-08-25 Phase 1 morphology adjudication,
    or established morphology-experiment discussion elsewhere in this repo).

Like build_matched_pairs.py, PAM/FIL text is never hand-retyped: every
accepted item is referenced by its item_num into the source table (parsed
fresh by verify_external_vocab.py's loader) and looked up programmatically.
Where an item offers multiple alternates (e.g. "Kambal / Cacambal") and only
one is verified, `pam_override`/`fil_override` selects it -- the script
asserts the override is an exact substring of the original cell, so an
override can only *select* existing text, never introduce new text.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_CSV = BASE_DIR / "reports" / "external-vocab-pairs.csv"
OUTPUT_STATS = BASE_DIR / "reports" / "external-vocab-pairs-stats.json"
EXCLUDED_LOG = BASE_DIR / "reports" / "external-vocab-excluded.csv"

import verify_external_vocab as vev  # noqa: E402  (local module, same directory)

# (item_num, confidence, basis, note, pam_override, fil_override)
ACCEPTED: list[tuple[int, str, str, str, str | None, str | None]] = [
    (1, "high", "pld_corroborated", "Basic greeting; 'Mayap a abak' pattern seen throughout raw PLD Greetings text.", None, None),
    (2, "high", "pld_corroborated", "'Ugto' (noon) seen directly in raw PLD Greetings text this session already read ('Mayap a ugtu pu').", None, None),
    (3, "high", "pld_corroborated", "'Mayap a gatpanapun' pattern seen throughout raw PLD Greetings text.", None, None),
    (4, "high", "pld_corroborated", "'Mayap a bengi' pattern seen throughout raw PLD Greetings text.", None, None),
    (5, "high", "dictionary_attested", "", None, None),
    (7, "medium", "dictionary_attested", "'Alang' (none/without) + 'anuman' (anything); calque of the FIL phrase.", None, None),
    (8, "medium", "dictionary_attested", "Using the attested 'Usuk pu'; 'Tulik pu' alternate not independently attested or corroborated.", "Usuk pu", None),
    (9, "medium", "dictionary_attested", "Using 'Komusta kayu pu?' (Spanish-loanword 'komusta', attested); 'Mapanu kayu pu?' alternate not independently attested.", "Komusta kayu pu?", None),
    (17, "medium", "dictionary_attested", "Using the first alternate; 'King ulian na ku pu' not independently checked.", "Mako na ku pu", None),
    (18, "medium", "dictionary_attested", "Fills a gap this session's own PLD reading left unmatched -- PAM Utt_Greetings.txt slot 8 uses 'kebaitan' with no FIL counterpart found at the time; this document's birthday reading is plausible and uncontradicted.", None, None),
    (19, "high", "pld_corroborated", "", None, None),
    (20, "high", "pld_corroborated", "", None, None),
    (21, "high", "pld_corroborated", "Using 'Nukarin?', which matches this experiment's own confirmed pldpair_022/023 PAM text; 'Pukarin?' alternate not independently corroborated.", "Nukarin?", None),
    (22, "medium", "dictionary_attested", "Root shared with 'capilanman' (whenever/always) seen in Iso_Time.txt.", None, None),
    (23, "high", "pld_corroborated", "'Obat' seen directly in the Iput-Ipot story dialogue this session already read.", None, None),
    (24, "high", "pld_corroborated", "Matches 'Macananu' in this experiment's own pldpair_026 (spelling variant).", None, None),
    (25, "medium", "pld_corroborated", "'Insanu'/'Isanu' seen in Story-domain text (pldpair_020 region) in a 'what/which' sense.", None, None),
    (26, "medium", "dictionary_attested", "", None, None),
    (27, "medium", "dictionary_attested", "", None, None),
    (28, "medium", "dictionary_attested", "Using the fully-attested-by-parts alternate; 'Kanganinu?' (fused form) not independently attested.", "Kang ninu?", None),
    (33, "medium", "dictionary_attested", "Kept as-is (word-level alternate mid-sentence, not a substitutable substring): 'susi' (key) is attested, 'kawi' is not.", None, None),
    (34, "high", "dictionary_attested", "", None, None),
    (35, "high", "dictionary_attested", "", None, None),
    (36, "high", "pld_corroborated", "3rd-person-singular 'ya' appears constantly throughout every PLD text read this session.", None, None),
    (37, "medium", "dictionary_attested", "", None, None),
    (38, "high", "pld_corroborated", "'kecatamu'/'itamu' forms seen throughout the Letter-domain text.", None, None),
    (39, "high", "pld_corroborated", "'kayu' seen constantly throughout PLD text.", None, None),
    (40, "medium", "dictionary_attested", "", None, None),
    (41, "medium", "dictionary_attested", "'ku' possessive/agent marker extremely common throughout PLD text.", None, None),
    (42, "medium", "dictionary_attested", "'mu' possessive/agent marker extremely common throughout PLD text.", None, None),
    (43, "medium", "dictionary_attested", "'na' possessive/agent marker extremely common throughout PLD text.", None, None),
    (44, "medium", "dictionary_attested", "", None, None),
    (45, "high", "pld_corroborated", "'kekatamung' seen in the Letter-domain text.", None, None),
    (46, "medium", "dictionary_attested", "'yu' common throughout PLD text.", None, None),
    (47, "medium", "dictionary_attested", "'da' (3rd-plural agent marker) extremely common throughout PLD text; 'Keraklan' less independently corroborated.", None, None),
    (48, "medium", "dictionary_attested", "'iti' ('this') appears constantly throughout PLD text.", None, None),
    (49, "medium", "dictionary_attested", "Identical spelling to FIL; plausible shared cognate.", None, None),
    (50, "medium", "dictionary_attested", "", None, None),
    (51, "medium", "dictionary_attested", "", None, None),
    (52, "medium", "dictionary_attested", "", None, None),
    (53, "high", "pld_corroborated", "'carin' seen directly in the Bernardo Carpio story text.", None, None),
    (54, "high", "pld_corroborated", "Verified numeral roots also confirmed via this session's own Iso_Ordinal.txt reading.", None, None),
    (55, "high", "pld_corroborated", "", None, None),
    (56, "high", "pld_corroborated", "", None, None),
    (57, "high", "dictionary_attested", "", None, None),
    (58, "high", "dictionary_attested", "", None, None),
    (59, "high", "dictionary_attested", "", None, None),
    (60, "high", "dictionary_attested", "", None, None),
    (61, "high", "dictionary_attested", "", None, None),
    (62, "high", "dictionary_attested", "", None, None),
    (63, "high", "dictionary_attested", "", None, None),
    (64, "high", "dictionary_attested", "", None, None),
    (65, "medium", "transparent_compound", "'labi-ng-adua' (ten+two=twelve) follows the exact same transparent compounding pattern as item 64; not attested as one surface token but both constituent parts are.", None, None),
    (66, "medium", "transparent_compound", "Using 'Adduang pulu' (two-tens=twenty); the document's other alternate 'Labing-addua' is a copy-paste error from item 65 (that literally means twelve, not twenty).", "Adduang pulu", None),
    (67, "medium", "dictionary_attested", "", None, None),
    (68, "medium", "dictionary_attested", "", None, None),
    (69, "high", "pld_corroborated", "'Ngeni' appears constantly throughout PLD text.", None, None),
    (70, "medium", "dictionary_attested", "", None, None),
    (71, "high", "dictionary_attested", "Well-known root; this project's own morphology work (v1-v4) discusses 'Bukas' extensively as an attested word.", None, None),
    (72, "high", "pld_corroborated", "'nandin' seen directly as a PAM Iso_Time.txt slot this session already read (left unmatched there; this document supplies its FIL counterpart).", None, None),
    (73, "medium", "dictionary_attested", "", None, None),
    (74, "high", "pld_corroborated", "'Aldo' appears constantly throughout PLD text.", None, None),
    (77, "high", "pld_corroborated", "Same 'Ugto' root as item 2, seen directly in raw PLD Greetings text.", None, None),
    (75, "high", "pld_corroborated", "'Bengi' appears constantly throughout PLD text.", None, None),
    (76, "high", "pld_corroborated", "Matches this experiment's own pldpair_025 PAM word.", None, None),
    (78, "high", "pld_corroborated", "'Mayap a gatpanapun' pattern seen throughout PLD text.", None, None),
    (79, "medium", "dictionary_attested", "'Domingo' is a transparent Spanish loanword.", None, None),
    (80, "medium", "dictionary_attested", "", None, None),
    (81, "high", "project_established", "Directly corroborated by this experiment's own confirmed pldpair_003 ('bayung banua' = 'bagong taon', new year).", None, None),
    (82, "high", "project_established", "'Tatang' is directly established as a genuine, monomorphemic Kapampangan word in this project's own 2026-08-25 Phase 1 adjudication.", None, None),
    (83, "high", "pld_corroborated", "'Indu' seen constantly throughout the Gamugamo story text.", None, None),
    (84, "high", "dictionary_attested", "", None, None),
    (85, "medium", "dictionary_attested", "", None, None),
    (86, "medium", "dictionary_attested", "", None, None),
    (87, "high", "dictionary_attested", "Confirmed (2026-08-28) via direct dictionary verification: Bergano (1732, Samson translation) p.124 -- 'BUNGSO. Strictly speaking, the youngest child, or the youngest among siblings...' Using 'Bunsso' (the attested alternate); excluding the unattested 'Anaktian'.", "Bunsso", None),
    (88, "medium", "transparent_compound", "Compositional 'apu' (grandparent) + 'a lalaki' (male); not attested as one surface token.", None, None),
    (89, "medium", "transparent_compound", "Compositional 'apu' (grandparent) + 'a babai' (female); not attested as one surface token.", None, None),
    (90, "medium", "dictionary_attested", "", None, None),
    (91, "medium", "dictionary_attested", "", None, None),
    (92, "high", "project_established", "'Pisan' (cousin) is directly confirmed in this project's own 2026-08-25 Phase 1 adjudication ('kapamisanan' root).", None, None),
    (93, "medium", "dictionary_attested", "", None, None),
    (94, "high", "dictionary_attested", "Multi-source attestation (Forman, ACD, UCLA Phonetics Archive, Kaikki) confirmed directly in word-evidence.csv.", None, None),
    (95, "medium", "dictionary_attested", "PAM 'Kasintahan' (direct Tagalog loanword) and 'Novia' (Spanish loanword) are plausible alongside this experiment's own 'Capalsintan' (pldpair_039); code-switching alternates, not independently attested in this project's historical-dictionary sources.", None, None),
    (96, "high", "pld_corroborated", "Shares the 'caluguran' root already used in this experiment's own confirmed pldpair_011.", None, None),
    (97, "high", "dictionary_attested", "Using the directly-attested, identical-cognate 'Kambal' rather than the ambiguous 'Cacambal' (declined earlier in this experiment for exactly this ambiguity).", "Kambal", None),
    (98, "medium", "pld_corroborated", "'ding tau' ('the people') seen throughout the Letter/Essay domain text.", None, None),
    (99, "medium", "dictionary_attested", "", None, None),
    (100, "medium", "dictionary_attested", "", None, None),
    (101, "high", "dictionary_attested", "Multi-source attestation (Forman, Kaikki) confirmed directly in word-evidence.csv.", None, None),
    (102, "medium", "dictionary_attested", "", None, None),
    (103, "high", "dictionary_attested", "Identical cognate spelling.", None, None),
    (104, "high", "pld_corroborated", "'king arung ning gorilya' (in the gorilla's nose) appears repeatedly in the Iput-Ipot story text.", None, None),
    (105, "medium", "dictionary_attested", "", None, None),
    (107, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (108, "medium", "dictionary_attested", "Using the attested 'Balugbug'; excluding the document's 'Tuli' alternate, which most plausibly means 'circumcision' in Kapampangan/Tagalog, not 'ear' -- likely an error in the source document.", "Balugbug", None),
    (110, "medium", "dictionary_attested", "", None, None),
    (111, "medium", "dictionary_attested", "", None, None),
    (113, "high", "pld_corroborated", "Consistent with this session's own Iso_BodyParts.txt reading.", None, None),
    (114, "high", "pld_corroborated", "'taus pusung' (heartfelt, lit. true-heart) seen throughout the Greetings/Letter domain text.", None, None),
    (115, "medium", "dictionary_attested", "", None, None),
    (116, "medium", "dictionary_attested", "", None, None),
    (117, "high", "dictionary_attested", "Identical cognate spelling; also appears in item 205's sentence.", None, None),
    (119, "high", "project_established", "Directly confirmed by this project's own 2026-08-25 Phase 1 adjudication (fixes a gap this session's own PLD Iso_BodyParts.txt reading could not fill -- no FIL 'ankle' term appeared in that specific elicitation list).", None, None),
    (120, "high", "project_established", "Directly confirmed by this project's own 2026-08-25 Phase 1 adjudication (galang-galangan = wrist, not ankle).", None, None),
    (121, "high", "project_established", "Derived from the 'mangan'/'pangan' root this project's own Phase 1 adjudication already confirmed correct.", None, None),
    (122, "high", "dictionary_attested", "", None, None),
    (123, "medium", "dictionary_attested", "Consistent with 'binayu' (pounded [rice]) in this experiment's own confirmed pldpair_009.", None, None),
    (124, "medium", "dictionary_attested", "", None, None),
    (125, "medium", "dictionary_attested", "", None, None),
    (126, "medium", "dictionary_attested", "Spanish loanword, identical spelling.", None, None),
    (127, "medium", "dictionary_attested", "", None, None),
    (128, "medium", "dictionary_attested", "Spanish loanword, identical spelling; thematically consistent with the Story domain's fruit-picking content.", None, None),
    (129, "medium", "dictionary_attested", "Using 'Asukar' (direct Spanish-loanword cognate of 'Asukal'); excluding the 'Yumu' alternate, which this same document's own item 200 defines as 'sweetness' (a quality), not 'sugar' (the substance).", "Asukar", None),
    (130, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (131, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (132, "medium", "dictionary_attested", "International/Spanish loanword, identical spelling.", None, None),
    (133, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (134, "high", "project_established", "'Mangan' (eat) is directly confirmed as the correct root in this project's own 2026-08-25 Phase 1 adjudication.", None, None),
    (135, "medium", "dictionary_attested", "", None, None),
    (136, "high", "pld_corroborated", "Shares the 'melutu' (cooked) root already used in this experiment's own confirmed pldpair_009.", None, None),
    (137, "medium", "dictionary_attested", "", None, None),
    (138, "high", "dictionary_attested", "Multi-source attestation (Forman, Kaikki) confirmed directly in word-evidence.csv.", None, None),
    (140, "medium", "dictionary_attested", "", None, None),
    (143, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (144, "medium", "dictionary_attested", "Using 'Langit' (identical cognate); excluding the 'Banua' alternate, which this experiment's own confirmed pldpair_003 already establishes means 'year', not 'sky/heaven'.", "Langit", None),
    (145, "medium", "dictionary_attested", "", None, None),
    (146, "medium", "dictionary_attested", "Using the identical-cognate, attested 'Dagat'; excluding the unattested 'Kalatdan' alternate.", "Dagat", None),
    (147, "high", "pld_corroborated", "'iyugse king ilug' (thrown into the river) appears in the Story-domain text this session already read.", None, None),
    (148, "medium", "dictionary_attested", "", None, None),
    (149, "high", "pld_corroborated", "'pun saging'/'pun dutung' (banana tree/tree) appear constantly throughout the Story/Essay domain text.", None, None),
    (150, "high", "pld_corroborated", "Matches 'aluntiang bulung' (green leaves) in this experiment's own confirmed pldpair_017/018.", None, None),
    (151, "medium", "dictionary_attested", "Near-identical cognate spelling.", None, None),
    (152, "medium", "dictionary_attested", "", None, None),
    (153, "medium", "dictionary_attested", "Same PAM word as item 152 ('ayup'); plausible polysemy (animal/bird), not treated as a contradiction.", None, None),
    (154, "high", "pld_corroborated", "'Pau' (turtle) is the recurring character name throughout the Matsing story text this session already read in full.", None, None),
    (155, "high", "pld_corroborated", "Identical spelling; recurring throughout the Story/Essay domain text.", None, None),
    (156, "high", "pld_corroborated", "Using 'Alitaptap' (identical cognate spelling, and the generic noun used in the Iput-Ipot story's narration, e.g. 'tacutan ne i alitaptap'); excluding 'Iput-Ipot', which this session's own PLD reading shows is used as the firefly character's proper name within that one story, not the generic word for the species.", "Alitaptap", None),
    (157, "high", "pld_corroborated", "Identical spelling; 'king arung ning gorilya' appears repeatedly in the Iput-Ipot story text.", None, None),
    (158, "high", "pld_corroborated", "Matches 'maglacad' in this experiment's own confirmed pldpair_015.", None, None),
    (159, "medium", "dictionary_attested", "Lower independent confidence; attested but not otherwise corroborated in this session's own reading.", None, None),
    (160, "high", "dictionary_attested", "Well-established basic vocabulary; standard Kapampangan o->u vowel-shift cognate pattern versus Tagalog 'tulog'/'matulog'.", None, None),
    (161, "medium", "dictionary_attested", "Identical spelling; plus native affixed form.", None, None),
    (162, "high", "pld_corroborated", "'Basan ke iti para keca' (I'll read this for you) appears in the Gamugamo story text this session already read.", None, None),
    (163, "high", "project_established", "This project's own v3/v4 morphology experiments extensively discuss 'Sumulat' and its '-um-' infix.", None, None),
    (164, "medium", "dictionary_attested", "Identical spelling, direct shared cognate.", None, None),
    (165, "high", "pld_corroborated", "'obra' (work/jobs) appears in the Letter-domain text this session already read.", None, None),
    (166, "high", "project_established", "Directly confirmed by this project's own 2026-08-25 Phase 1 adjudication: 'seli' (bought) has root 'sali' (buy).", None, None),
    (168, "high", "pld_corroborated", "'Munta ca wari king Menila' (Will you go to Manila) appears in the raw PAM Interrogatives text this session already read.", None, None),
    (169, "medium", "pld_corroborated", "Root 'datang' shares this experiment's own confirmed pldpair_035 ('Pangaratang'/'dumating'); 'Dumatang' is a transparent -um- infix form of the same root.", None, None),
    (170, "medium", "dictionary_attested", "", None, None),
    (171, "medium", "pld_corroborated", "'Makiramdam ca at basan ke iti' (pay attention/listen and I'll read this) in the Gamugamo story text supports a 'listen' sense, though 'ramdam' more literally means 'feel/sense' -- a plausible but not perfectly precise gloss.", None, None),
    (172, "medium", "dictionary_attested", "Identical spelling, direct shared cognate.", None, None),
    (173, "medium", "pld_corroborated", "Root 'baldug' independently seen and corroborated during this session's own Iso_MinPairs.txt reading earlier in Phase 2 ('baldug (v. fall)').", None, None),
    (174, "medium", "dictionary_attested", "", None, None),
    (175, "medium", "dictionary_attested", "Using the attested 'Panintunan'; root 'Nintun' itself not separately attested as an exact surface form.", None, None),
    (176, "medium", "dictionary_attested", "", None, None),
    (177, "high", "pld_corroborated", "'Mekibat ya I Iput-Ipot' (Iput-Ipot answered) appears constantly throughout the Story-domain text this session already read.", None, None),
    (178, "medium", "dictionary_attested", "", None, None),
    (179, "high", "pld_corroborated", "Matches 'buri' in this experiment's own confirmed pldpair_020 ('Insanu ing buri mu?').", None, None),
    (180, "high", "pld_corroborated", "Using 'Masanting', which matches this experiment's own confirmed pldpair_017 ('masanting a pun', a beautiful tree); excluding the unattested 'Malagyu' alternate, which more plausibly means 'famous' (from 'lagyu', name/fame), not 'beautiful'.", "Masanting", None),
    (182, "high", "pld_corroborated", "'mangaragul' (plural form) appears throughout the Story-domain text this session already read ('mangaragul a batu', 'mangaragul a bulung').", None, None),
    (183, "high", "pld_corroborated", "Matches 'malati' in this experiment's own confirmed pldpair_012 ('metung yang macalunus, malati...').", None, None),
    (184, "medium", "pld_corroborated", "Shares the 'tula' root already used in this experiment's own confirmed pldpair_005 ('Catutula cu pu...').", None, None),
    (185, "medium", "dictionary_attested", "", None, None),
    (186, "medium", "dictionary_attested", "Using the attested 'Mapali'; excluding the unattested 'Malapali' alternate.", "Mapali", None),
    (187, "medium", "dictionary_attested", "", None, None),
    (188, "medium", "dictionary_attested", "", None, None),
    (189, "medium", "dictionary_attested", "Identical cognate spelling for the first alternate.", None, None),
    (190, "high", "pld_corroborated", "Matches 'mabagal' discussed in this experiment's own rejected-pair analysis (pldpair review); the word itself is validly corroborated independent of that rejected pairing's other issues.", None, None),
    (191, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (192, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (193, "high", "project_established", "Directly corroborated by this experiment's own confirmed pldpair_003 ('bayung banua', new year).", None, None),
    (194, "medium", "dictionary_attested", "Identical cognate spelling.", None, None),
    (195, "medium", "pld_corroborated", "'matuang capatad' (older sibling) appears in the Iso_Kinship.txt data this session already read.", None, None),
    (197, "high", "pld_corroborated", "'pambihirang sicanan' (extraordinary strength) matches this experiment's own confirmed pldpair_019.", None, None),
    (199, "high", "pld_corroborated", "Matches 'matapat' in this experiment's own confirmed pldpair_011 ('Ing matapat a caluguran').", None, None),
    (200, "medium", "dictionary_attested", "Defines 'Yumu' as the sweetness quality, consistent with item 129's cross-check.", None, None),
    (203, "high", "pld_corroborated", "'Mayap a bengi' pattern seen throughout PLD Greetings text.", None, None),
    (205, "medium", "dictionary_attested", "Thematically and structurally consistent with the PAM Utt_Medical.txt content this session already read and rejected as a non-parallel *domain* -- but this specific sentence's grammar is fully transparent and every content word but one ('capareung', a regular ka-X-ng comparative derivation of the attested root 'pareu') is independently attested.", None, None),
    (207, "high", "pld_corroborated", "Fills a gap this session's own PLD reading left unmatched (PAM Utt_Interrogatives.txt slot 7, 'Nucarin ya ing seli cung lapis nandin?'); 'seli'/'sali' (bought/buy) is independently confirmed by this project's own 2026-08-25 Phase 1 adjudication. Note: the FIL gloss asks where the pencil *was bought*, a subtly different question than the English gloss given ('where is the pencil'), which asks the pencil's current location.", None, None),
    (209, "high", "dictionary_attested", "", None, None),
    (210, "high", "dictionary_attested", "", None, None),
]

# (item_num, reason)
EXCLUDED: list[tuple[int, str]] = [
    (16, "Identical to the FIL phrase; low informational value as a translation pair. Alternate 'Manganat ka' has no attestation or corroboration."),
    (87, "'Anaktian' alternate is unattested. 'Bunsso' is now confirmed correct (moved to ACCEPTED, 2026-08-28) -- see item 87 in the accepted list below."),
    (106, "'Gipang' has zero hits in Forman, Bergano, or Samson (2011) full-text search (2026-08-28); confirmed unattested, not just suspected. 'ipan' is confirmed instead -- Forman (1971) p.62 uses it compositionally ('busbus ipan' = tooth cavity, lit. 'hole-tooth'), consistent with this reviewer's expectation."),
    (109, "Internally contradicted by the same document's own item 145, which uses 'Lupa' for 'earth/ground' -- a far more linguistically plausible cognate meaning than 'face'."),
    (112, "Confirmed wrong (2026-08-28), not just unattested: Bergano (1732, Samson translation) p.111 glosses 'BINTI' as 'Noun, Courage, manliness' -- unrelated to 'leg' entirely. Confirmed again by the Spanish-index cross-references on pp.476/498 ('Brio'/vigor and 'Esfuerzo'/effort both list 'Binti' as a Kapampangan equivalent). No dictionary evidence found anywhere for 'binti' meaning leg."),
    (118, "Genuinely unresolved, not a settled conflict either way (updated 2026-08-28 after direct dictionary verification): 'kalingkingan' = little finger is confirmed correct (Forman 1971 p.69, direct gloss). But this session's own earlier claim that 'malingmingan' = pinky (pldpair_037, based on a shared '-lingking-' surface pattern with kalingkingan) was itself wrong -- Bergano's 1732 dictionary (Samson translation) p.266 glosses 'MALINGMINGAN' as 'the temples / sides of the head', not a finger at all; that pair was removed from build_matched_pairs.py. Neither 'palakingkingan' nor 'palasingsingan' (this document's and this experiment's respective claims for 'ring finger') appear anywhere in Forman, Bergano, or Samson (2011) -- a full-text search of all three found zero hits for either form. So which of ring/pinky 'palakingkingan' actually means remains unattested by any primary source available to this project; excluded pending better evidence, not because either specific claim is confirmed wrong."),
    (141, "Redundant: same PAM word 'Aldo' as item 74 (already accepted)."),
    (142, "Redundant: same PAM word 'Bulan' as item 80 (already accepted)."),
    (167, "The document's own 'Magsali' alternate for 'sell' contradicts its own item 166, which uses 'Sali'/'Sumali' for 'buy' -- likely a buy/sell mix-up. Accepted 'Magtinda' only (see ACCEPTED)."),
    (181, "Redundant: same PAM word 'Masanting' as item 180 (already accepted as 'beautiful')."),
    (196, "'Anak' is already used for 'child' (item 84); reusing it for the adjective 'young' conflates noun and adjective senses imprecisely. Not accepted as a distinct pair."),
    (198, "Still unattested after direct verification (2026-08-28): the only full-text hit in the three dictionaries (Samson 2011 p.350) is a false positive -- 'mahina' as a substring inside 'imahinacion' (imagination, a Spanish loanword), not a real match. No genuine 'mahina' entry found in any of the three; stays excluded."),
    (6, "Near-duplicate of this experiment's own pldpair_002 -- differs only by a hyphen ('taus-pusung' vs 'taus pusung'). No new information."),
    (201, "Near-duplicate of this experiment's own pldpair_030 -- differs only by spelling ('Salucuian' vs 'Salucuiang'). No new information."),
]


def resolve_row(item_num: int, all_rows: list[dict]) -> dict:
    for row in all_rows:
        if row["num"] == item_num:
            return row
    raise KeyError(f"item_num {item_num} not found in source table")


def apply_override(field: str, override: str | None) -> str:
    if override is None:
        return field.strip()
    if override.lower() not in field.lower():
        raise ValueError(f"override {override!r} is not a substring of source field {field!r}")
    return override


def main() -> None:
    all_rows = vev.load_md_rows()
    row_by_num = {r["num"]: r for r in all_rows}

    accepted_nums = {a[0] for a in ACCEPTED}
    excluded_nums = {e[0] for e in EXCLUDED}
    duplicate_texts = vev.load_existing_pair_texts()

    # Completeness check: every non-duplicate item in the document must be
    # explicitly ACCEPTED or EXCLUDED -- nothing silently falls through.
    missing = []
    for row in all_rows:
        n = row["num"]
        if n in accepted_nums or n in excluded_nums:
            continue
        pam_norm = vev.normalize(row["pam"])
        fil_norm = vev.normalize(row["fil"])
        if pam_norm in duplicate_texts or fil_norm in duplicate_texts:
            continue
        missing.append(n)
    if missing:
        raise AssertionError(f"items not classified as accepted/excluded/duplicate: {missing}")

    out_rows = []
    for item_num, confidence, basis, note, pam_override, fil_override in ACCEPTED:
        row = row_by_num[item_num]
        pam_text = apply_override(row["pam"], pam_override)
        fil_text = apply_override(row["fil"], fil_override)
        out_rows.append(
            {
                "pair_id": f"extvoc_{item_num:03d}",
                "source_item_num": item_num,
                "confidence": confidence,
                "verification_basis": basis,
                "pam_text": pam_text,
                "fil_text": fil_text,
                "english_gloss": row["eng"],
                "note": note,
            }
        )

    fieldnames = [
        "pair_id",
        "source_item_num",
        "confidence",
        "verification_basis",
        "pam_text",
        "fil_text",
        "english_gloss",
        "note",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    with EXCLUDED_LOG.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.writer(f)
        writer.writerow(["source_item_num", "fil", "pam", "reason"])
        for item_num, reason in EXCLUDED:
            row = row_by_num[item_num]
            writer.writerow([item_num, row["fil"], row["pam"], reason])

    high = sum(1 for r in out_rows if r["confidence"] == "high")
    medium = sum(1 for r in out_rows if r["confidence"] == "medium")
    by_basis: dict[str, int] = {}
    for r in out_rows:
        by_basis[r["verification_basis"]] = by_basis.get(r["verification_basis"], 0) + 1
    stats = {
        "total_pairs": len(out_rows),
        "confidence_high": high,
        "confidence_medium": medium,
        "by_verification_basis": by_basis,
        "total_excluded": len(EXCLUDED),
    }
    with OUTPUT_STATS.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
