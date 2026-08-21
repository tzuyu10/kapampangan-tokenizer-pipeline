# Expanded morphology v4 - resegmentation audit

Status: local-test, source-supported, provisional. Not independent gold.
Root inventory reused byte-for-byte from `source_adjudicated_v2`; only new
affix/morphophonology rules were added. See `EVIDENCE.md` for full citations.

- Word types resegmented: **143,529**
- Types newly analyzed vs. v2 (boundaries changed): **5,897** (42,393 occurrences)
- Ambiguous types (preserved, not resolved): **890**

## Rule counts (occurrences)

| Rule ID | Occurrences | Types |
|---|---:|---:|
| `PROTECT_ROOT` | 533,463 | 4,565 |
| `REDUP_CV_REDUPLICATION` | 8,336 | 994 |
| `PREFIX_KA` | 8,031 | 418 |
| `SUFFIX_AN` | 7,771 | 745 |
| `INFIX_IN` | 7,505 | 506 |
| `PREFIX_MA` | 6,350 | 597 |
| `PROTECT_COMPOUND` | 5,781 | 24 |
| `PREFIX_PA` | 5,204 | 330 |
| `PREFIX_MI` | 4,712 | 407 |
| `CIRCUMFIX_KA_AN` | 4,402 | 295 |
| `PREFIX_PAN_PAM_LABIAL_M_SUBSTITUTION` | 3,275 | 652 |
| `PREFIX_I` | 3,037 | 338 |
| `PREFIX_MAKA` | 2,840 | 404 |
| `PREFIX_MAG` | 2,232 | 278 |
| `PREFIX_ME` | 2,045 | 309 |
| `CLITIC_LA` | 1,948 | 62 |
| `CIRCUMFIX_PANG_PAN_AN` | 1,613 | 47 |
| `PREFIX_M_BARE` | 1,406 | 132 |
| `INFIX_UM` | 1,139 | 208 |
| `PREFIX_MEG` | 1,049 | 39 |
| `CLITIC_MU` | 965 | 42 |
| `CLITIC_KU` | 889 | 39 |
| `PREFIX_PEKA` | 889 | 84 |
| `SUFFIX_ANAN` | 846 | 50 |
| `CIRCUMFIX_PA_AN` | 785 | 158 |
| `SUFFIX_EN` | 709 | 17 |
| `PREFIX_PAN_PAN_DENTAL_N_SUBSTITUTION` | 668 | 103 |
| `PREFIX_MIG` | 657 | 138 |
| `CLITIC_NA` | 576 | 75 |
| `PREFIX_MAN_MAM_LABIAL_M_SUBSTITUTION` | 504 | 70 |
| `CIRCUMFIX_PI_AN` | 477 | 103 |
| `PREFIX_PAN_PANG_VELAR_NG_SUBSTITUTION` | 453 | 21 |
| `PREFIX_MAN_MAN_UNCHANGED` | 446 | 83 |
| `CLITIC_RA` | 443 | 36 |
| `PREFIX_MAKI` | 430 | 75 |
| `CIRCUMFIX_MI_AN` | 404 | 87 |
| `CLITIC_YA` | 365 | 43 |
| `PREFIX_MAN_MAN_DENTAL_N_SUBSTITUTION` | 346 | 61 |
| `PREFIX_MAN_MEN_UNCHANGED` | 322 | 42 |
| `CIRCUMFIX_PAG_AN` | 317 | 59 |
| `CLITIC_NE` | 261 | 31 |
| `CLITIC_PA` | 215 | 40 |
| `PREFIX_PAN_PANG_UNCHANGED` | 208 | 75 |
| `PREFIX_IPA` | 185 | 52 |
| `PREFIX_MAN_MANG_VELAR_NG_SUBSTITUTION` | 173 | 42 |
| `PREFIX_MANG` | 163 | 48 |
| `PREFIX_MAGPA` | 153 | 61 |
| `PREFIX_MAN_MEM_LABIAL_M_SUBSTITUTION` | 148 | 44 |
| `PREFIX_MEKA` | 148 | 68 |
| `CIRCUMFIX_PANG_AN` | 131 | 20 |
| `PREFIX_MEKI` | 130 | 31 |
| `PREFIX_MAN_MANY_DENTAL_Y_SUBSTITUTION` | 125 | 32 |
| `PREFIX_MAGKA` | 122 | 17 |
| `PREFIX_PAKI` | 112 | 33 |
| `PREFIX_MENG` | 111 | 17 |
| `PREFIX_MAKAPAG` | 106 | 17 |
| `PREFIX_MAN_MEN_DENTAL_N_SUBSTITUTION` | 88 | 31 |
| `CLITIC_NO` | 80 | 28 |
| `CIRCUMFIX_PANG_PAM_AN` | 62 | 19 |
| `PREFIX_MIGPA` | 59 | 28 |
| `PREFIX_MAN_MENG_VELAR_NG_SUBSTITUTION` | 33 | 17 |
| `CIRCUMFIX_PANG_PANGA_AN` | 32 | 9 |
| `PREFIX_MAGPAKA` | 29 | 18 |
| `REDUP_V_REDUPLICATION` | 29 | 23 |
| `PREFIX_MIGKA` | 28 | 9 |
| `PREFIX_PAN_PANGA_LITERAL` | 25 | 18 |
| `PREFIX_MAKIPAG` | 24 | 13 |
| `PREFIX_KA_FULL_REDUPLICATION` | 23 | 10 |
| `PREFIX_MEKAPAG` | 11 | 8 |
| `PREFIX_MAN_MENY_DENTAL_Y_SUBSTITUTION` | 10 | 7 |
| `PREFIX_MIGPAKA` | 8 | 6 |
| `PREFIX_MEGPA` | 6 | 6 |
| `PREFIX_MEGKA` | 1 | 1 |

## Newly analyzed examples (first 40, alphabetical)

| Surface | v4 segments | Underlying | Rule | Frequency |
|---|---|---|---|---:|
| `AGKATAN` | `AGKAT || AN` | AGKAT + -an | `SUFFIX_AN` | 1 |
| `ALALAYAN` | `AL || ALAYA || N` | REDUP(ALAYA) + ALAYA + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `AUSAN` | `AUS || AN` | AUS + -an | `SUFFIX_AN` | 2 |
| `Aalma` | `A || alma` | REDUP(alma) + alma | `REDUP_V_REDUPLICATION` | 1 |
| `Agkatan` | `Agkat || an` | Agkat + -an | `SUFFIX_AN` | 9 |
| `Agusan` | `Agus || an` | Agus + -an | `SUFFIX_AN` | 44 |
| `Akakit` | `Ak || akit` | REDUP(akit) + akit | `REDUP_CV_REDUPLICATION` | 22 |
| `Akitan` | `Akit || an` | Akit + -an | `SUFFIX_AN` | 1 |
| `Alacan` | `Alac || an` | Alac + -an | `SUFFIX_AN` | 2 |
| `Alala` | `Al || ala` | REDUP(ala) + ala | `REDUP_CV_REDUPLICATION` | 1 |
| `Alalaya` | `Al || alaya` | REDUP(alaya) + alaya | `REDUP_CV_REDUPLICATION` | 1 |
| `Alalayan` | `Al || alaya || n` | REDUP(alaya) + alaya + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `Alan` | `Ala || n` | Ala + -an | `SUFFIX_AN` | 22 |
| `Albuganan` | `Albuganan` | Albuganan | `None` | 1 |
| `Aminan` | `Amin || an` | Amin + -an | `SUFFIX_AN` | 2 |
| `Ananang` | `An || anang` | REDUP(anang) + anang | `REDUP_CV_REDUPLICATION` | 2 |
| `Ananta` | `An || anta` | REDUP(anta) + anta | `REDUP_CV_REDUPLICATION` | 8 |
| `Aninagan` | `Aninag || an` | Aninag + -an | `SUFFIX_AN` | 1 |
| `Apaya` | `Apa || ya` | Apa + =ya | `CLITIC_YA` | 2 |
| `Arena` | `Are || na` | Are + =na | `CLITIC_NA` | 2 |
| `Arian` | `Ari || an` | Ari + -an | `SUFFIX_AN` | 2 |
| `Arwan` | `Ar || wan` | Ari + -an | `SUFFIX_AN` | 1 |
| `Aswan` | `As || wan` | Asu + -an | `SUFFIX_AN` | 1 |
| `Atan` | `Atan` | Atan | `None` | 1 |
| `Atate` | `At || ate` | REDUP(ate) + ate | `REDUP_CV_REDUPLICATION` | 1 |
| `Ausan` | `Aus || an` | Aus + -an | `SUFFIX_AN` | 54 |
| `Babalag` | `Ba || balag` | REDUP(balag) + balag | `REDUP_CV_REDUPLICATION` | 2 |
| `Babalasan` | `Ba || balas || an` | REDUP(balas) + balas + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `Babalik` | `Ba || balik` | REDUP(balik) + balik | `REDUP_CV_REDUPLICATION` | 4 |
| `Babaltang` | `Ba || baltang` | REDUP(baltang) + baltang | `REDUP_CV_REDUPLICATION` | 1 |
| `Babalut` | `Ba || balut` | REDUP(balut) + balut | `REDUP_CV_REDUPLICATION` | 1 |
| `Babandila` | `Ba || bandi || la` | REDUP(bandi) + bandi + =la | `REDUP_CV_REDUPLICATION` | 1 |
| `Babangalan` | `Ba || bangal || an` | REDUP(bangal) + bangal + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `Babasa` | `Ba || basa` | REDUP(basa) + basa | `REDUP_CV_REDUPLICATION` | 1 |
| `Babasan` | `Ba || basan` | REDUP(basan) + basan | `REDUP_CV_REDUPLICATION` | 1 |
| `Babatan` | `Ba || bata || n` | REDUP(bata) + bata + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `Babau` | `Ba || bau` | REDUP(bau) + bau | `REDUP_CV_REDUPLICATION` | 2 |
| `Babawalan` | `Ba || bawal || an` | REDUP(bawal) + bawal + -an | `REDUP_CV_REDUPLICATION` | 1 |
| `Babayat` | `Ba || bayat` | REDUP(bayat) + bayat | `REDUP_CV_REDUPLICATION` | 2 |
| `Babayo` | `Ba || bayo` | REDUP(bayo) + bayo | `REDUP_CV_REDUPLICATION` | 1 |

## Ambiguous forms (first 25, alphabetical)

| Surface | Frequency |
|---|---:|
| `Albuganan` | 1 |
| `Atan` | 1 |
| `BIEN` | 1 |
| `Balanan` | 1 |
| `Banten` | 3 |
| `Bien` | 9 |
| `Bulanan` | 1 |
| `Dalanan` | 1 |
| `Dinen` | 1 |
| `Ipaku` | 6 |
| `Ipangaku` | 2 |
| `Iparas` | 1 |
| `Kabalan` | 1 |
| `Kakamwan` | 1 |
| `Kakanan` | 6 |
| `Kapangan` | 4 |
| `Katasan` | 3 |
| `Kawan` | 1 |
| `Ketan` | 1 |
| `Luan` | 5 |
| `MALAYA` | 1 |
| `MAMALA` | 1 |
| `MAMUN` | 1 |
| `MANAKIT` | 1 |
| `MANGA` | 2 |

## Rejected / deferred items

| Item | Disposition | Reason |
|---|---|---|
| paki-...-an circumfix | rejected | The only -an-suffixed forms near paki- resolve to something else: pakitanan is pa- + kit(a) + -anan (Mirikitani p.635), and pakidinan is paki- + the irregular suppletive stem dinan ('give to', Mirikitani p.570 item 5). Neither is a productive paki-...-an pattern. |
| -in suffix | rejected | Not found in any reviewed Kapampangan source. |
| -ng linker | rejected (out of scope for v4) | User instruction: model only as a linker with exact-host/context safeguards, not as an ordinary derivational suffix; left for a separately scoped experiment. |
| Tagalog pinaka- | rejected | Not Kapampangan. Kapampangan's own superlative peka- is operationalized. |
| 'mi' in misamban treated as an infix | rejected | misamban is analyzed through the mi-...-an circumfix applied to the attested root samba, not through any infix rule. |
| mekipag- (aspect pair of makipag-) | deferred | meki- and makipag- are each directly attested but no source shows mekipag- itself; adding it would be paradigm analogy, not attestation. |
| peN-/piN- as aspect-marked paN- allomorphs | deferred | Mirikitani pp.744, 795, 945 glossary entries are internally inconsistent about whether they mark aspect on pag- or on paN-. |
| Tense-conditioned root vowel alternation (a<->e, u<->i) | documented, not operationalized | Forman: lexically conditioned per root, not a general phonological rule. |
| min- unfolded-tense variant of maN- (vs. operationalized men-) | documented, not operationalized | Same lexical-conditioning problem; no reliable surface trigger. |
| Vowel lengthening for continuing/progressive tense | documented, not operationalized | Not consistently marked in the plain-text training corpus and does not correspond to a segment boundary. |
| Medial d->r alternation as a general standalone rule | partially operationalized | Only accepted as a reduplication hypothesis, exactly where documented. |
