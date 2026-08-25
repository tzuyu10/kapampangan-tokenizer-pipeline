# Morphology candidate triage (Phase 1)

Status: silver / AI-triaged, not independent gold.

Source: `D:\Coding\thesis\datasets\kapampangan_morph_annotated_dataset.csv`
(650 rows), copied byte-for-byte into `resources/` (see
`resources/provenance-manifest.json` for SHA-256/source path). The original
file at its external path was never modified.

## Why this dataset needed triage, not direct use

Every row already carries this project's own prior `confidence` field
(74 `high` / 576 `medium`, see `AGENT_CONTEXT.md`'s 2026-08-25 dataset-audit
entry) — but `medium confidence... review against native-speaker
judgment... for gold training` is an explicit self-disclosed caveat on 576 of
650 rows, not a usable development/test split on its own. The goal here is
to add independent, mechanical, defensible checks on top of that existing
field, so that what eventually becomes Phase 3's development/test morphology
data rests on more than one dataset's self-reported confidence tag.

## Method

Four signals, computed per row by `triage_morphology.py`:

1. **`reconstruction_ok`** — do the segmented pieces in `morph_segments`
   (stripped of `+`/`~` markers) losslessly reconstruct `normalized`? This is
   the same lossless-reconstruction invariant this project already requires
   of every accepted v2/v4 morphology analysis (see `AGENT_CONTEXT.md` Scope
   section). A failure here is a structural defect in the row itself, not a
   judgment call.
2. **`root_in_v2_lexicon` / `root_in_secondary_lexicon` /
   `reconciliation_root_tier`** — is the claimed root independently attested?
   Checked against
   `experiments/source_adjudicated_v2/resources/training-lexicon.json`
   (this project's own most-vetted local lexicon), the external
   `kapampangan_lexicon_local_curated.csv` /
   `kapampangan_lexicon_polytranslator_curated.csv`, and, added after the
   2026-08-25 user spot-check below,
   `experiments/internet_root_reconciliation_v1/reports/word-evidence.csv`
   — this project's own prior page-cited reconciliation of the *entire*
   143,529-word-type training inventory against Forman (1971), Bergaño/Samson's
   1732 translation, Samson (2011), the ACD, and Kaikki/Wiktionary. A root is
   `strong` if any of the first four (page-cited, dictionary-grade) sources
   support it, `weak` if only the community-maintained Kaikki/Wiktionary
   export does.
3. **`affix_recognized`** — does the row's claimed affix marker appear in
   this project's own already-modeled affix inventory (Table 1's
   `src/kapampangan_morphbpe/constants.py` union v4's documented additions,
   `experiments/expanded_morphology_v4/README.md` "What changed vs. Table
   1")? Reduplication markers are checked structurally (is the marker a
   prefix of, or equal to, the claimed root) rather than against a fixed
   list, since a reduplication marker is a copy of the root, not a fixed
   morpheme string.
4. **`reconciliation_conflict`** — added after the user spot-check, and the
   single strongest signal in this triage, overriding all of the above. It
   checks the row's exact surface form (not just its claimed root) against
   `word-evidence.csv` and flags a conflict when either:
   - this project's **own existing v2/v4 system already has an accepted
     analysis of that exact surface with a *different* root** than this row
     claims (e.g. `mamangan`: v2/v4 already accepts `ma + mangan`, root
     `mangan`; this dataset's row instead claims `ma~mang+an`, root `mang`)
     — a direct internal contradiction, not just an absence of evidence; or
   - the reconciliation experiment explicitly recommends **against**
     decomposing that exact surface at all
     (`decision: lexically_attested_unresolved`, `proposed_action:
     do_not_promote_without_root_evidence`) — meaning the whole word is
     independently attested as its own dictionary headword with no source
     evidence supporting further decomposition (e.g. `tatang`, `pasbul`,
     `parang`: all attested standalone in Forman/Bergaño/Samson).

Tier is a deterministic function of these signals plus the row's own
pre-existing `confidence` field (used only as a secondary signal, never
overriding a mechanical failure); `reconciliation_conflict` overrides
everything else:

| Tier | Meaning |
| --- | --- |
| `A_strong_silver` | Reconstructs losslessly, root strongly attested (v2 lexicon or a page-cited reconciliation source), every affix marker recognized, and no reconciliation conflict. |
| `B_moderate_silver` | Reconstructs losslessly, at least one weaker corroboration signal holds, no reconciliation conflict. |
| `C_weak_needs_review` | Reconstructs losslessly, but no corroboration signal succeeded and no reconciliation conflict was found either — genuinely unverified either way. |
| `D_reject_structural_failure` | Fails the lossless-reconstruction check outright — a defect in the row itself. |
| `F_conflicts_with_reconciliation_evidence` | This project's own existing analysis or prior reconciliation evidence actively contradicts this row's claimed decomposition. |

Function-word/clitic rows (no morphological decomposition to check) are
scored separately: tier depends only on reconstruction (trivial, since there
is no segmentation) and whether the surface is in a small closed-class
list (Table 1's own `CLITICS` tuple plus common Kapampangan
prepositions/particles observed in the set), combined with the row's
existing `high`/`medium` confidence tag.

## Result

| Tier | Rows |
| --- | ---: |
| A (strong silver) | 220 |
| B (moderate silver) | 306 |
| C (needs review) | 26 |
| D (reject, structural) | 1 |
| F (conflicts with reconciliation evidence) | 97 |

(Updated 2026-08-25 after a user spot-check added the `reconciliation_conflict`
signal — see below. Before that signal existed, 621/650 rows landed in A/B;
97 of those 621 (15.6%) are now known to conflict with independently sourced
evidence already present in this repository.) Full per-row detail:
`reports/morphology-triage.csv`; machine-readable counts:
`reports/morphology-triage-stats.json`.

### The one structural failure

`kap-morph-0435`: surface `kapamisanan`, but `morph_segments` is
`ka+pampamis+an`, which concatenates to `kapampamisan` (13 characters) —
not `kapamisanan` (11 characters), and the reconciliation evidence shows
zero source match for `kapamisanan` as a whole word either. The user's
spot-check independently suggested the likely true root is `pisan`
("cousin"/togetherness, cf. `kapisanan`), consistent with `pisan` being a
Forman/Bergaño-attested root in `word-evidence.csv` — but this is not
self-evident from the row alone, so it stays excluded rather than
silently corrected.

## User spot-check corrections (2026-08-25)

The user reviewed a stratified sample against their own knowledge and
pointed to `D:\Coding\thesis\pdf-dls\ilide.info-kapampangandictionaryamongsamson-1-pr_8a0f2e64d024628a4ab7b876563dc425.pdf`
(the Samson 2011 Kapampangan dictionary) as a reference. That PDF turns out
to already be a cited source in this repository: it is the exact file this
project's earlier `internet_root_reconciliation_v1` experiment used as
`samson2011` (see its `source-registry.json` and `README.md`), which had
already run page-cited lookups for every word in the training inventory
against it plus Forman (1971), Bergaño/Samson's 1732 translation, the ACD,
and Kaikki/Wiktionary. Every one of the user's corrections below is
independently confirmed by that existing evidence, which this triage had
not cross-referenced until now:

| Row (surface, claimed root) | User's correction | Independent evidence in this repo |
| --- | --- | --- |
| `mamangan`, root `mang` | Over-truncation: the stem is `mangan` (or `pangan`/`kangan`); `mang` is an artificial split. | `word-evidence.csv`: this project's **own existing v2/v4 system already accepts `ma + mangan`** (root `mangan`) for this exact surface — a direct internal contradiction, not just missing evidence. `mangan` and `pangan` are both independently attested (Samson 2011 p.463; Kaikki). |
| `tatang`, root `tang` | Monomorphemic nursery word for "father"; `ta~` is not a real reduplicative prefix here. | `word-evidence.csv`: `tatang` itself is attested as its own headword (Samson 2011 p.740), with `decision: lexically_attested_unresolved` / `do_not_promote_without_root_evidence` — reconciliation already recommended against decomposing it. |
| `pasbul`, root `sbul` | Monomorphemic root meaning "door/gate"; `sbul` is not a valid Kapampangan stem. | `word-evidence.csv`: `pasbul` is Forman-labeled `root_or_stem_headword` (p.178) plus a Bergaño citation — explicitly a root, not a prefixed form. |
| `parang`, root `rang` | Monomorphemic root meaning "field/meadow"; `rang` is not a valid root. | `word-evidence.csv`: `parang` is attested standalone in both Bergaño (p.293) and Samson 2011 (p.537), `decision: lexically_attested_unresolved`. |
| `pamanalastas`, root `nalastas` | Root should be `talastas` (nasal assimilation absorbed the `t`); `nalastas` is not a real root. | `word-evidence.csv`: `talastas` is Forman/Bergaño-attested (`new_exact_root_matched_hypothesis`); `nalastas` does not appear anywhere in the 143,529-word-type reconciliation at all. |
| `pekapun`, root `kapun` | The dataset's implicit gloss ("castrated") looks wrong; real readings are either `peka-` + `pun` (chief/leader) or a form related to `napun`. | `word-evidence.csv`: `pekapun` itself has **zero source match** anywhere (`decision: unresolved_no_source_match`) despite appearing 171 times in the training corpus — genuinely unresolved either way, consistent with flagging it for review rather than accepting it. `napun` (Forman p.158, Samson p.494) and `pun` (five independent sources) are both real, so a `pe-` + `kapun`, or `napun`-related, reading remains plausible but unconfirmed. |
| `makapatulug`, root `tulug` via `makapa-` | Correctly identified: composite `maka-` + `pa-` + `tulug`, both already-modeled Table 1 prefixes stacked. | Confirmed — no reconciliation conflict for this row; the earlier `C_weak_needs_review` placement was a heuristic limitation (this triage's affix check required an exact match to the concatenated string `makapa-`, not a decomposition into known sub-markers `maka-` + `pa-`). Left in `C` rather than silently promoted, since automatically decomposing multi-morpheme marker strings is a real methodology gap, not something to paper over here. |
| `kapamisanan`, root `pamis` | Likely true root is `pisan` ("cousin"), with the source string corrupting it via an erroneous `pampamis` insertion. | `word-evidence.csv`: `pisan` is Forman/Bergaño-attested (`already_analyzed`, protected root); `kapamisanan` and `pamis` in this exact form/context are not attested anywhere. Consistent with, and more specific than, this triage's own structural-failure flag on the row. |
| `Bucung-bucung`/`galáng-galangán` (MT pair, not morphology) | `galáng-galangán` means wrist in Filipino, not ankle (Filipino for ankle is `bukung-bukong`). | Not a Kapampangan-lexicon question — a correction to this session's own (wrong) claim about Filipino vocabulary; recorded in `experiments/translation_gold_v1/reports/mt-pair-triage-summary.md`. |
| `seli` misread as "key" in an MT pair | `seli` means "bought" (root `sali`), not a cognate of `susi` ("key"). | `word-evidence.csv`: `seli` cross-references to `sali` in Forman (p.210); `sali` is independently Bergaño/Forman-attested. Consistent with the user's reading. Recorded in the MT triage summary. |

**Net effect**: adding the `reconciliation_conflict` signal (described
above) moved 97/650 rows (14.9%) — mostly rows that had reused an
independently-attested-but-*wrong* root string, exactly the `mamangan`
pattern — out of A/B and into a new `F` tier. This is a real, measurable
correction to this triage's own accuracy, not a cosmetic addition: it was
only found because the user checked a small sample by hand and because this
project already had page-cited lookup evidence sitting in a different
experiment folder that this triage had not consulted.

## What this triage does not establish

- **Not gold, even now.** Tier A is "corroborated by this project's own
  existing silver lexicon, rule inventory, and reconciliation evidence," not
  independent native-speaker verification. The `F` tier catches the specific
  failure mode the user found (a genuinely attested root reused for the
  wrong word), but a wrong analysis that reuses an attested root *for the
  right word* and a recognized affix marker can still land in A undetected.
- **`root_unattested` (325 rows, mostly B/C tier)** means the root is not in
  any lexicon or reconciliation source checked here — not that it is wrong.
  Many are plausible Kapampangan roots simply absent from all sources
  checked so far.
- The affix-recognition check is a marker-string heuristic, not a grammar
  checker: `makapatulug` above shows it can under-recognize a valid
  composite marker; it can equally be fooled by a string that happens to
  match a known marker but is applied to the wrong root.
- The 26 remaining needs-review rows still mostly share the coverage-gap
  pattern first identified in this triage's initial pass: a prefix (`pe-`,
  `pama-`, `pami-`) plausibly real in Kapampangan but not yet in v4's rule
  inventory — see "Elaborating on a future rule-expansion pass" in
  `AGENT_CONTEXT.md`'s 2026-08-25 entry for what operationalizing these
  would actually require.

## Second-round user adjudication of the `F` tier -- complete (2026-08-25)

The user reviewed **all 97** `F_conflicts_with_reconciliation_evidence`
rows (19/19 `existing_mismatch`, 78/78 `do_not_decompose`) across two
passes and gave a specific verdict on every one. Full detail:
`reports/user-adjudication-2026-08-25.csv`. This is a third, higher-quality
judgment layered on top of the two automated ones (the candidate dataset's
claim vs. this project's existing v2/v4 analysis) -- recorded additively,
not merged into the mechanical tiers, so all three views stay visible for
whoever consumes this data next.

**Calibration finding: the `F` tier reliably flags "this needs a human
look," but must never be read as "the existing v2/v4 analysis is right" or
as "the word is monomorphemic."** Final counts across all 97 rows:

`existing_mismatch` (19 rows, one -- `pasbulan` -- has an unresolved
categorization ambiguity, see the CSV):

| Verdict | Rows |
| --- | ---: |
| Candidate correct, existing wrong | 6 |
| Existing correct (or close), candidate wrong | 7 |
| Both wrong -- a third, deeper root exists | 4 |
| Candidate correct (or close) | 1 |
| Unclear (see `pasbulan` note) | 1 |

Roughly an even split, confirming this is not a one-directional signal.

`do_not_decompose` (78 rows):

| Verdict | Rows | % |
| --- | ---: | ---: |
| Candidate's original decomposition was actually correct (flag false positive) | 36 | 46% |
| Candidate wrong, but a *different* root than "leave it atomic" implies | 19 | 24% |
| Flag correctly caught a genuinely monomorphemic word or loanword | 18 | 23% |
| Candidate partially correct / deeper-derivation nuance | 3 | 4% |
| Both candidate and the "leave atomic" default wrong | 2 | 3% |

**This is the single most important number from this whole triage round**:
the reconciliation experiment's own "do not decompose" recommendation,
taken at face value, would have been wrong 77% of the time (60/78) as a
verdict on whether to accept the *candidate's specific* decomposition --
it is a real, useful "found this exact surface in a dictionary, be careful"
signal, but it is not evidence of monomorphemic status on its own. Treat
every `F`-tier row (or any future row this signal flags) as "known
contested, needs a specific look," never as auto-resolved in either
direction.

### Four systemic patterns behind the wrong analyses (user-identified)

Across the full review, the user identified four recurring *mechanisms*
behind the errors -- useful beyond this one dataset, since both this
triage's candidate root and this project's own existing v2/v4 system make
the same kinds of mistakes:

1. **Intervocalic `/d/` -> `/r/` not reversed.** Roots ending in `d` shift
   to `r` before a vowel-initial suffix like `-an`, but nothing undoes this
   when recovering the root: `tulid` -> `katuliran` (not root `tulir`),
   `palad` -> `kapalaran` (not root `palar`), `dusa` -> `parusa` (not root
   `rusa`).
2. **Nasal assimilation not reversed.** A `paN-`-family prefix assimilates
   to the following consonant, but the assimilated form gets treated as the
   root instead of recovering the underlying one: `damdam`/`ramdam` (feel)
   surfaces as `namdam`/`amdam` in `panamdaman`/`panamdam`, and as
   `nalastas`/`manalastas` (both wrong) instead of `talastas` in
   `pamanalastas`.
3. **Invalid phonotactic clusters created by over-truncation.** Cutting a
   claimed affix off too aggressively leaves a residual "root" that
   contains a consonant cluster this language doesn't allow word-initially:
   `stul` (from `pastul`), `lbe` (from `lumbe`), `ntas` (from `pantas`),
   `nimanm` (from `panimanman`) are all phonotactically impossible as roots
   -- their presence alone is a red flag independent of any dictionary
   lookup.
4. **Loanwords and monomorphemic words over-segmented as if native and
   affixed.** Spanish loans (`capitan`, `pastul`/pastor, `maestro`) and
   native monomorphemic roots (`tutung`, `tatang`, `tatas`, `kawan`) were
   both falsely split into a fictitious root plus a recognized affix
   marker -- a reminder that "the affix marker string is real" is never
   sufficient evidence on its own (see "What this triage does not
   establish" above).

Patterns 1-3 are concrete, checkable rules a future automated pass could
add (e.g. reject any candidate root containing a phonotactically invalid
cluster; try a `d`<->`r` and a de-assimilated nasal variant before giving
up on root attestation) -- noted here as candidates for a future session,
not implemented in this pass.

## Next step

Phase 1 spot-check is now complete for the morphology triage's `F` tier --
every flagged row has a recorded human verdict. One thing intentionally
left open: whether to run the same reconciliation cross-check retroactively
against the MT-pair triage (it currently only checks morphology). Both
triages carry clear silver/AI-triaged labeling and full per-row provenance
for whoever consumes them in Phase 3.
