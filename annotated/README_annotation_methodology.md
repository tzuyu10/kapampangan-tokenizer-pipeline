# Kapampangan Dictionary — Cleaned & Annotated Data

## What's in `kapampangan_annotated.json`
3,138 dictionary entries (the front-matter/OCR noise from the first ~196 scraped
"entries" — title page, copyright text, introduction — was removed; the real
alphabetical dictionary body starts at "a’bak").

Each entry looks like this:

```json
{
  "headword": "bangal",
  "root": "bangal",
  "syllables": ["ban", "gal"],
  "pos_blocks": [
    {
      "pos": "V.",
      "senses": ["divide, split. babangal, binangal"],
      "affix_forms": [
        {
          "form": "binangal",
          "segmentation": "b-in-angal",
          "affix_type": "Infix",
          "affix": "-in-",
          "confidence": "heuristic"
        }
      ],
      "derived_forms_in_definition": [
        {
          "form": "pabangal",
          "segmentation": "pa-bangal",
          "affix_type": "Prefix",
          "affix": "pa-",
          "confidence": "heuristic",
          "source": "mined_from_definition"
        }
      ]
    }
  ]
}
```

- **affix_forms**: word forms the original dictionary explicitly listed as a form of the entry.
- **derived_forms_in_definition**: additional inflected forms automatically pulled out of the
  gloss/definition text (the source scrape mostly failed to populate `affix_forms`, so most
  of the real morphological data lives here instead).
- **segmentation**: e.g. `k-um-an`, `ma-kalat`, `pa-...-an` style breakdown, per your example.
- **affix_type / affix**: classified against Table 1 (Prefix, Infix, Suffix, Circumfix,
  Reduplication). Clitics (na, pa, mu, ku, ya, la, ra, ne, no) weren't attached to any headwords
  in this dictionary (they attach to phrases, not lexicon entries), so they're documented here
  for reference but not tagged per-word.
- **confidence**: `"high"` = form equals the root exactly (no affix). `"heuristic"` = matched a
  known affix pattern algorithmically. Entries marked `"Unsegmented" / "low - needs manual
  review"` didn't cleanly match any Table 1 pattern — usually because the source text was noisy
  (English glosses mixed in) or the word involves irregular sound changes not covered by the
  simple rules below.

## How segmentation was done (rule-based, per Table 1)

1. **Circumfix** — `ka-...-an`, `pa-...-an`, `pang-/pam-/pan-/panga-...-an`
2. **CV- reduplication** (progressive/contemplative forms, e.g. *babangal*)
3. **Infix** `-um-`/`-in-` — inserted after the root's first consonant (e.g. *bangal* → *b-in-angal*)
4. **Prefix** — longest match from: *ma-, me-, pa-, maka-, ka-, mag-, meg-, mang-, meng-, i-,
   ipa-, makapag-, mig-, meka-, mekapag-*
5. **Suffix** `-an`
6. Anything left unmatched → flagged `Unsegmented` for manual review.

**Syllable breakdown** uses a maximal-onset heuristic (single consonant between vowels goes
with the following syllable; consonant clusters split one/one), e.g. *kuman → ku.man*,
*a'bak → a'.bak*. This is a good first pass but Kapampangan has some vowel-length and glottal
patterns worth a human once-over, especially on shorter/irregular words.

## Honest limitations — this was automated, not hand-annotated
Given 3,138 entries, I built a rule-based tagger against Table 1 rather than segmenting each
word by hand — that's the only way to cover the whole dictionary in this session. It gets
common patterns right (as shown above) but:
- ~58% of mined "derived forms" didn't match a clean pattern and are marked `Unsegmented` —
  many are just scrape noise (stray English words), but some are real words with irregular
  morphophonology (assimilation, glide insertion, etc.) that the simple rules don't model.
- Root identification for affixed forms is a best-effort string match, not a linguistic parse.

I'd recommend spot-checking a sample against the PDF, and I'm happy to re-run the tagger on
just the flagged/uncertain entries, or refine the rules (e.g. add glide-insertion handling for
vowel-initial roots like *a'bak → mayabak*) if you want higher precision on a specific affix type.
