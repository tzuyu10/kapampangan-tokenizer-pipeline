# Lexicon Dictionary — SEED FILES

The TSVs in this folder are a **starter seed**, not a validated resource.
They exist so the pipeline runs end-to-end on day one. Every row is marked
`source=SEED`. Before any result goes into Chapter 4:

1. Replace/extend each file from the Kapampangan Dictionary Embeddings dataset
   and from Del Corro (1980), Forman (1971), Fajardo & Lee (2025).
2. Have a native speaker or Kapampangan linguist sign off each entry and put
   their name + date in the `source` column.
3. Run `python scripts/01_validate_lexicon.py` — it fails the build on
   structural errors and warns on low coverage.

Target size for a defensible study: >= 3,000 roots, >= 60 prefixes (with
allomorphs), all documented affixes from the grammars above.
