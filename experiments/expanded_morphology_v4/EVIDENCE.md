# Expanded morphology v4 — evidence and provenance

Status: local-test, source-supported, provisional. Not independent linguistic
gold. This table records the exact page-level provenance behind every rule in
`expanded_morphology.py`, and explains every item the user's requested
coverage list asked for but that was **rejected or deliberately deferred**.

All cited pages used the PDF's **embedded text layer** (`selected_method:
"embedded_text"` in `runs/source-ocr/source-manifest.json`), not OCR image
recognition, which this project's own policy (`AGENT_CONTEXT.md`) treats as
the more reliable extraction path. Page numbers below are the PDF page
numbers recorded in that manifest (`pdf_page`), which is also how the OCR
text files are named (`text/<source>/page-NNNN.txt`) — they are **not** the
printed page numbers in each book's own running header/footer, which differ
by a fixed per-book offset (Forman: PDF page − 11 ≈ printed page; Mirikitani:
PDF page − 40 ≈ printed page).

Visual page-image rendering was attempted for spot verification but this
environment has no PDF rasterizer (`pdftoppm`/`poppler` and Python `fitz`/
`pypdf` are both unavailable), so verification instead relied on
**independent cross-source triangulation**: every accepted rule is
corroborated by at least one directly-glossed example sentence/word pair
(not just a bare affix mention), and most are corroborated from two
independent books (Forman *Kapampangan Grammar Notes* and Mirikitani
*Speaking Kapampangan*), plus, where noted, the *Kapampangan Trilingual
Lexicon*'s headword list.

Root inventory: unchanged. This experiment reuses
`experiments/source_adjudicated_v2/resources/training-lexicon.json` byte for
byte — no root is added, removed, or edited. Every example below only uses
roots already present in that lexicon (`aral`, `basa`, `datang`, `din`, `kan`,
`sali`, `samba`) or a synthetic in-memory lexicon in `tests/` for rule
families whose only evidenced example word uses a root not present in the
real corpus lexicon (`lawe`, `pandilu`, `albe`).

## Accepted rules

| # | Rule | Surface examples (source) | Source / page(s) |
|---|---|---|---|
| 0 | Baseline Table 1 prefixes/infixes/suffix/circumfixes/clitics | — | Reproduced unmodified from `docs/MORPHOLOGY_SPEC.md`; not new. |
| 1 | Standalone `m-` prefix (actor, vowel/other-initial root, no place assimilation) | `minum` (m+inum) | Mirikitani p.471 ("miminum" continuing-tense discussion; base form `minum`) |
| 2 | `maN-` actor prefix, dental/alveolar class, regular: `man-`/`men-` + root beginning `t,d,n,s` → `n` replaces the root-initial consonant | `mánalíp` (talip), `mánábat` (sábat), `mánúlid` (túlid) | Forman pp.80–81 (explicit prose rule + 5 examples) |
| 3 | `maN-` actor prefix, dental/alveolar class, irregular: `many-`/`meny-` + root beginning `d,s` → surfaces as `y` instead of `n` (lexically flagged subclass, still productive as a hypothesis gated by exact-root match) | `mányátang` (dátang), `mínyalí` (sálí, i.e. "went shopping") | Forman p.81 ("a number of other roots... have the *s* replaced by *y*... roots beginning with *d*... replaced by *y*: dákap: mányakáp, dátang: mányátang, dútung: mányutung") |
| 4 | `maN-` actor prefix, labial class: `mam-`/`mem-` + root beginning `p,b,m` → `m` replaces the root-initial consonant | `mámuát` (buát), `mámalíta`/`mamalíta` (balíta), `mámalís` (palís); `mamasa` (basa, "is reading") | Forman p.80; Mirikitani p.510 ("(b) maN- mamasa 'is reading'") |
| 5 | `maN-` actor prefix, velar class: `mang-`/`meng-` + root beginning `k,g,q` → `ng` replaces the root-initial consonant | `mamangan`/`mangan` (kan, "eat") | Forman p.76 (prose rule); Mirikitani p.471 ("mamangan... The Actor affix is maN- ... Note the change" discussion) |
| 6 | `paki-` prefix (polite/causative request) | `pakisali` "please buy" | Mirikitani pp.744, 795, 945 (three independent glossary/index entries, consistent gloss "please [causative, polite request affix]") |
| 7 | `peka-` prefix (superlative) | "peka- is the most"; "Adjectivals may also be marked as superlatives by the affix peka- 'the most'" | Mirikitani pp.316, 334 |
| 8 | `maki-` prefix (associative/reciprocal request) | `makisaké`, `makidáme` | Forman p.81 |
| 9 | `meki-` aspect pair of `maki-` | `mekiramdam` (makiramdam-mekiramdam) | Mirikitani p.534 |
| 10 | `makipag-` prefix (associative) | `makipámalíta`, `makipagáral`; `makipagsalita` | Forman p.81; Mirikitani p.541 |
| 11 | `mi-` standalone prefix (reciprocal/stative, no `-an`) | `mípaté`, `mípapaté` ("fight each other") | Forman p.90 |
| 12–14 | `magpa-` / `migpa-` / `megpa-` aspect triplet | `mágpalimús`; `magpaynawa`–`migpaynawa` | Forman p.77 ("magpa- (with tenses as for mag-)"); Mirikitani p.534 |
| 15–17 | `magka-` / `migka-` / `megka-` aspect triplet | `Magkasákit`, `Migkasákit`, `Migkámalí` | Forman p.77 (direct examples) + p.76 ("similarly magka- and magpaka-", explicit generalization of the mag-/mág-/mig-/meg- tense paradigm) |
| — | `magpaka-` / `migpaka-` / `megpaka-` aspect triplet | `mágpakatulíng`, `Ót magpakatulíng ká?` | Forman pp.76, 78 (same explicit generalization) |
| 18 | `mi-...-an` circumfix (stative) | `mítakútan`, `mípatánan`, `míbarílan`, `miabuán`, `mísasakítan`, `mialbugán`, `míarálan` | Forman pp.89–90 ("There is a basic stative type construction marked by either mi- or ka- (mi—an, ka—an.)" + 7 example sentences) |
| 19 | `pi-...-an` circumfix (locative) | `pipandiluan` "place for swimming"; `pisamban` "church" (`samba` "worship" + `-an` → `samban`/`pisamban`, dictionary headwords) | Mirikitani pp.491, 497; Kapampangan Trilingual Lexicon pp.44, 48 (headwords `samba`, `samban`, `pisamban`); also referenced in running text at Forman pp.61–62, Bayung Ortograpiyang Kapampangan pp.32, 60, 108 |
| 20 | `pag-...-an` circumfix (goal focus, no nasal assimilation) | `pagaralan` (aral, "to study something") | Mirikitani pp.569, 810 |
| 21 | `-en` suffix (object-focus allomorph of `-an`) | `lawen` `[= lawe + en]` "look at something" | Mirikitani pp.288, 295 (two independent glossary entries) |
| 22 | `-anan` suffix (goal-referent, future) | `sulatanan` "going to write to someone"; `saupan`/`sulatanan` contrast | Mirikitani pp.595, 652 |
| 24 | `-an`/`-en`/`-anan` allomorphy: (a) literal attachment after a consonant-final root; (b) vowel-hiatus collapse to bare `-n`/`-nan` after an `a`/`e`-final root; (c) `w`-insertion + full suffix after an `i`/`u`-final root | `basan` (basa), `alben` (albe), `kuanan` (kua); `salwan` (sali), `lampaswan` (lampasu); `kanan` (kan), `planchan` (plancha) | Mirikitani pp.569–570 (explicit numbered rule list with all three patterns); cross-confirmed by `lawen`(#21) and dictionary `samban`/`pisamban` (#19, root `samba`) |
| 25 | CV-/V-reduplication for continuing/progressive aspect, including documented medial `d→r` alternation | `tuturu`, `sasali`, `susubli`, `kukua`, `susulat`, `miminum`, `mumunta`, `mumuli`; `daratang` (datang, with noted `d→r`) | Forman pp.78–79; Mirikitani pp.510–511 (7 examples + explicit note: "the change of d to r in daratang from datang... occurs quite regularly") |
| 26 | `ka-` + full-root reduplication for recent-completive aspect (with the same `d→r` alternation) | `karatángratáng` (datang), `kaibátibát`, `kapanganákpanganák`, `kapuntápuntá`, `katigtígtigtíg`, `kabáwalbáwal` | Forman p.91 (§4.5, 10 examples) |
| 23 | `paN-` nominalizer, standalone `pang-`/`pam-`/`pan-`/`panga-`, with the same 3-way place assimilation as `maN-`, **compositional**: may attach over an already `mag-`/`ma-`-prefixed stem | `paninda` (tinda), `pamaynawa` (paynawa), `pamangan` (mang-an), `pamagimporta` (mag-importa), `pamagaral` (mag-aral), `pamamialung` (ma-mialung) | Mirikitani p.686 (§6.5, explicit prose rule + 6 worked examples showing the nasal-place-assimilation derivation step by step) |

## Rejected / deliberately deferred items

| Item | Disposition | Reason |
|---|---|---|
| `paki-...-an` circumfix | **Rejected** | The only `-an`-suffixed forms near `paki-` resolve on inspection to something else: `pakitanan` is `pa-` + `kit(a)` + `-anan` ("Combination of pa- plus -an", Mirikitani p.635, listed under a *different* heading than `paki-`), and `pakidinan` is `paki-` + the irregular suppletive `dinan` ("give to", itself an unproductive special form per Mirikitani p.570 item (5)). Neither is a clean, productive `paki-...-an` pattern; both are either a distinct rule already covered (#19/#24) or a one-off suppletive stem. Not operationalized. |
| `-in` suffix | **Rejected** | Not found in any reviewed source. Per the user's explicit instruction, not added without direct Kapampangan textual support. |
| `-ng` linker | **Rejected / out of scope for v4** | User instruction: only model this "separately as a linker with exact-host/context safeguards", not as an ordinary derivational suffix. That is a distinct grammatical subsystem (attributive/predicate linking, not word-formation) and is left for a future, separately-scoped experiment rather than folded into this affix/circumfix engine. |
| Tagalog `pinaka-` | **Rejected** | Not Kapampangan; appears only in a prior informal/generated candidate list, exactly the kind of item the user warned against. Kapampangan's own superlative is `peka-` (#7), which *is* operationalized. |
| `mi` in `misamban` as an infix | **Rejected** | Never modeled as an infix. `misamban` is analyzed through the `mi-...-an` circumfix (#18) applied to the attested root `samba` (Forman dictionary; Trilingual Lexicon), matching the target `mi- + samba + -an` → surface `mi + samba + n`. |
| `mekipag-` (aspect pair of `makipag-`) | **Deferred** | `meki-` (#9) and `makipag-` (#10) are each directly attested, but no source example shows `mekipag-` itself. Adding it would be paradigm analogy, not direct attestation; held out per the user's explicit caution against extrapolating beyond what is textually supported. |
| `peN-`/`piN-` as aspect-marked `paN-` allomorphs | **Deferred** | Mirikitani pp.744, 795, 945 show `peN-`/`piN-`/`Pig-` glossary entries (`pepaglutuan`, `pinyali`, `piglutu`), but the three forms are inconsistent about whether they mark aspect on `pag-` or on `paN-`, and `pepaglutuan` looks like continuing-tense vowel lengthening/reduplication of `pag-...-an` rather than a distinct prefix. Too unclear to operationalize safely. |
| Tense-conditioned root vowel alternation (`a↔e`, `u↔i`: `mako↔meko`, `muntá↔mintá`, `mulai↔milai`) | **Documented, not operationalized** | Forman states this is lexically conditioned per root ("some take a vowel change... others take min-"), not a general phonological rule; representing it correctly would need a per-root tense paradigm table, which is out of scope for a boundary-segmentation engine. |
| `min-` unfolded-tense variant of `maN-` (vs. the operationalized `men-`, #2–#5) | **Documented, not operationalized** | Same lexical-conditioning problem as above (Forman p.76: "some... others take min-"); no reliable surface trigger distinguishes which roots take `min-` vs `men-`. |
| Vowel lengthening for the continuing/progressive tense of `mag-`/`maN-`/`ma-` | **Documented, not operationalized** | Mirikitani p.510 describes this as vowel *length*, which the plain-text training corpus does not consistently mark (no systematic macron/accent encoding), and it does not correspond to a segment boundary in any case. |
| Medial `d→r` alternation as a general standalone rule | **Partially operationalized** | Only accepted as one additional *hypothesis* inside reduplication (#25, #26), gated by exact-root validation, exactly where the sources document it (`daratang`, `karatángratáng`). Not applied outside reduplication contexts, since no non-reduplicated `d→r` evidence was reviewed. |

## Known interaction risk (not a v4 bug — a corpus-lexicon quality finding)

Because circumfix analysis runs before suffix analysis (preserving the
paper-mandated Table 1 stage order), a handful of very short, low-quality
entries already present in the *reused, unmodified* v2 lexicon (e.g. `na`,
`sa` as one- and two-letter `lemma_or_root_candidate` rows sourced from
Wiktionary) can occasionally out-compete the linguistically correct analysis
for an unrelated word (for example `kanan` — root `kan` "eat" + `-an`,
Mirikitani p.569 — can instead resolve through `ka-...-an` circumfix using
the coincidental short root `na`). This is a pre-existing lexicon-quality
issue inherited unmodified from `source_adjudicated_v2`, not something v4
introduces; v4 only makes it newly *visible* because it added more rule
families that can collide with such short roots. It is reported here rather
than patched, since fixing it would mean editing the reused v2 lexicon (out
of scope: this experiment adds rules, not roots) or reordering the
paper-mandated stage precedence (out of scope: would diverge from Table 1).
See `reports/audit.md` for the measured frequency of this interaction across
the full resegmented training inventory.
