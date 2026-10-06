# Gemini batch -- mechanical word-attestation check

Coverage signal only (see module docstring in `verify_gemini_batch.py` for exactly what this does and does not verify).

- Total sentences checked: 500
- Total PAM content tokens: 5207
- Overall token attestation: 4518 / 5207 (86.8%)
- Sentences with every content word attested: 90 (18.0%)
- Sentences with zero attested content words: 0

## A concrete, checkable pattern in the unattested tokens

Two of the most frequent unattested tokens are objectively verifiable as
**untranslated Tagalog left in the "Kapampangan" column**, not gaps in this
project's dictionary coverage -- the same batch uses genuine Kapampangan
vocabulary for the identical meaning elsewhere, so this is a same-batch
internal inconsistency, not a dictionary-coverage question:

- **`Bagaman`** ("although") appears untranslated in **8** sentences (e.g.
  #233, #334, #366) while **14** other sentences (6 with `Maski`, 8 with
  `Agyang`) correctly use genuine Kapampangan concessive markers for the
  same meaning.
- **`sasakyan`** (the full Tagalog spelling of "vehicle") appears in **8**
  sentences, actually *more often* than the Kapampangan-contracted
  `saskyan` (4 sentences) used elsewhere in the same batch for the same
  word.

This suggests a meaningful fraction of the batch mixes in un-adapted
Tagalog rather than consistently applying Kapampangan vocabulary/phonology,
which the overall 86.8% token-attestation rate alone does not surface.

## Most frequent unattested tokens (top 30)

| Token | Occurrences |
| --- | --- |
| pagsusulit | 9 |
| maaga | 9 |
| sasakyan | 8 |
| bagaman | 8 |
| maghintay | 7 |
| lalewan | 7 |
| lumub | 6 |
| pagka-yari | 6 |
| aplikasyon | 5 |
| panying | 5 |
| dumatang | 5 |
| kadagting | 5 |
| sumakay | 5 |
| mag-ayos | 5 |
| manalon | 5 |
| sumakai | 5 |
| inabili | 5 |
| kwarto | 5 |
| saskyan | 4 |
| trapiko | 4 |
| maiwasan | 4 |
| magluto | 4 |
| tanghali | 4 |
| sapatos | 4 |
| makapasa | 4 |
| meg-wan | 4 |
| mekit | 4 |
| natanggap | 3 |
| gripo | 3 |
| huling | 3 |
