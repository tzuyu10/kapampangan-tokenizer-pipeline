# Architecture — what changed, what didn't, and how the pieces connect

This doc is the detailed answer to "what did you change, and how are the
pieces wired together." Read `README.md` first if you just want to run it.

## 1. What is byte-for-byte unchanged

- `backend/tokenizer/kapampangan_morphbpe_runtime/tokenizer.py` and
  `__init__.py` — copied directly from your `demo/kapampangan_morphbpe_runtime/`
  folder. Not one character edited. This is the file that actually decides
  how a word gets split — the `Tokenizer` class, `_pretokenize()`, and the
  merge loop inside `_encode_pretoken()`.
- `backend/tokenizer/artifacts/morphbpe-penalty32/*`, `plain-bpe/*`, and
  `unigram-lm-6080/*` — the exact artifact files. `plain-bpe` and
  `unigram-lm-6080` are still the original files copied from your
  `demo/plain-bpe/` and `demo/unigram-lm-6080/`. `morphbpe-penalty32` is
  **not** from `demo/` — it went through two swaps on 2026-09-13: first
  `morphbpe-penalty8` -> a canonical-lexicon-trained `penalty-64` (based on
  the silver-lexicon `data/validation.csv` method alone), then that ->
  this `penalty-32`, trained on the richer `expanded_morphology_v4` lexicon
  (3,311 roots, verified byte-identical to the stream that produced the
  real official `penalty-1/2/4/8` artifacts) after scoring the full
  1..256 sweep against BOTH the silver-lexicon method AND the authoritative,
  partially-human-verified `tokenizer_selection_v1` DEV/TEST reference --
  the same reference that originally established `penalty-8` as the "Phase
  3" winner. Penalty=32 beats that established winner on both DEV (0.5422
  vs 0.4639) and TEST (0.4977 vs 0.4093) F1, and also beat the intermediate
  canonical-lexicon `penalty-64` the first swap had put in (0.4052 DEV /
  0.4000 TEST) -- that first swap was a regression by this more rigorous
  standard, corrected here. See
  `experiments/expanded_morphology_v4_penalty_extension_v1/README.md` and
  `reports/selection-v1-extended-scores.json` for full numbers.
  It's an exact, unmodified copy of that experiment's exported
  `penalty-32/candidates/vocab-6080/` artifact — same export path
  (`export_tokenizer_artifact`), same checksum format, nothing hand-edited.
  All three BPE-family artifacts get the same `checksums.sha256` re-hash on
  load (existing `tokenizer.py` code) — so if any were ever altered, the
  backend refuses to start rather than silently serving a different
  tokenizer than the one on disk. `unigram-lm-6080` has no
  `checksums.sha256` of its own (it never did, in your original folder) —
  its `tokenizer.json` is read directly by `unigram_lm.py`.
- `backend/tokenizer/unigram_lm.py` — the `UnigramLM` class (the Viterbi
  best-path decoder), copied verbatim out of your `demo.py`. Moved into its
  own module rather than imported from `demo.py` directly, because your
  `demo.py` also *instantiates* its tokenizers at import time using paths
  relative to its own file location (`HERE / "morphbpe-penalty8"` etc., from
  when that was still the active artifact) — importing it as-is from a
  different directory would have tried to load artifacts from the wrong
  place. The class itself is untouched.
- `backend/tokenizer/reference_data.py` — the scoring functions (`score`,
  `mcf1`, `rows_for`, `_f1`, `_capped_pairs`, `_pieces_from_boundaries`) and
  the gold data (`SENTENCES`, `FAMILIES`, `WORDS`) are copied verbatim from
  your `demo.py`. I did not rewrite the F1 math — it's the same functions
  your own CLI demo uses, just imported instead of re-typed, so a Boundary
  F1 number from this web app is the same number `demo.py` would print for
  the same input.

## 2. What is new, and why

### `backend/tokenizer/trace_service.py`

This is the one piece of real "new logic," and it does two things:

**a) `trace_word()`** — re-runs the *same* merge-selection rule
`Tokenizer._encode_pretoken()` uses ("of all adjacent pairs that have a
learned merge rule, apply the one with the lowest rank"), but records every
intermediate state, because the real `encode()` only returns the *final*
tokens — it doesn't expose what happened at each step along the way (there
was nothing to change there; the real function was simply never built to
narrate itself, which makes sense for a production tokenizer). Since this is
necessarily a second implementation of that loop, it comes with a built-in
safety net:

**b) `verify_fidelity()`** — runs at server startup (you'll see
`trace/encode parity check: 30/30 words passed` in the terminal). It takes
every word from your own `demo.py` reference data plus a few edge cases
(`kumain`, `Kumain`, capital-letter and single-character words) and asserts
that `trace_word()`'s final tokens exactly equal `tokenizer.encode()`'s real
output for every one of them. If the two ever disagreed, the server would
crash on startup naming the exact word — the step-by-step display can never
silently drift from what the tokenizer actually does.

`trace_service.py` also holds `analyze()`, which is the function
`backend/server.py` calls for every `/api/tokenize` request. It:

1. Splits the raw input on whitespace and strips `|` characters, recording
   which words had them (the gold-annotation convention lifted from
   `demo.py`'s own `custom_section()` — nothing new, just moved from a CLI
   flag into an HTTP request).
2. Feeds the *clean* (pipe-free) text to the real, unmodified
   `tokenizer.encode()` — exactly what `demo.py` does.
3. Also runs `_pretokenize()` (the real one, imported from `tokenizer.py`,
   not reimplemented) to find each word's boundaries, and calls
   `trace_word()` on each one for display.
4. If any word had `|` marks, builds `rows` with `reference_data.rows_for()`
   and scores them with `reference_data.score()` — same functions, same
   math as `demo.py`. If no word had a `|`, this step is skipped entirely.

### `backend/tokenizer/comparison_service.py`

Powers the Comparison tab. `_bpe_groups`, `groups_by_tokenizer`, and
`split_word` are direct ports of the same-named functions in your `demo.py`
— restructured to *return* data instead of `print`-ing to a terminal, but
computing exactly the same thing, on the same three loaded tokenizers
(`MORPH`, `PLAIN`, `UNI`). `custom_compare(raw_text)` is the single entry
point: same `|`-marking convention as `trace_service.analyze()`, generalized
to score all three tokenizers instead of one, using the same verbatim
`reference_data.score()`/`mcf1()` for the headline numbers plus
`scoring_explain.py` (below) for the "how it's computed" breakdown.

An earlier version of this module also reproduced `demo.py`'s own static
showcase (`word_examples`, `family_examples`, `sentence_examples`,
`full_comparison`, and a hardcoded `PHASE3_HEADER`) as a fourth "Comparison"
view. That's been removed — the Comparison tab now always compares whatever
text you last tokenized on the Tokenizer tab instead, which is what powers
a live defense better than a fixed set of examples. (Before removing it, I
verified that module's numbers against your pasted `python demo.py` run
number-for-number — every word split, every family's consistency F1, and
the pooled row (MorphBPE 1.632/0.85/0.96, Plain BPE 1.105/0.00/0.56,
Unigram-LM 1.158/0.35/0.56) matched exactly — so the scoring underneath is
the same code, just no longer wired to a fixed example set.)

### `backend/tokenizer/scoring_explain.py`

New. `reference_data.py`'s `score()` and `mcf1()` compute precision/recall/
F1 but throw away every intermediate value on the way there (which words'
predicted cuts matched the gold cuts, which words got grouped by a shared
morpheme, which pairs counted as a match/miss/extra). This module re-runs
those exact same two loops — `explain_boundary()` mirrors `score()`,
`explain_consistency()` mirrors `mcf1()` — but keeps everything: per-word
gold vs. predicted cut positions, the morpheme/token groups that produced
each shared-pair count, and the literal list of word-pairs behind every
TP/FP/FN. This is what the Comparison tab's "How These Scores Are Computed"
panel renders. Like `trace_service.trace_word()`, this is necessarily a
*second* implementation of the same math, so it carries the same kind of
safety net: `comparison_service.verify_scoring_fidelity()` runs at server
startup and asserts these functions' precision/recall/F1 exactly match
`reference_data.score()`/`mcf1()` on the project's own gold data (pooled
`SENTENCES` for boundary+consistency, `FAMILIES` forms for consistency,
across all three tokenizers) — printed as
`scoring-explain parity check: 6/6 cases passed`. If it ever failed, the
server won't start — the "how it's computed" numbers shown to a panelist
can never drift from the real Boundary F1 / Consistency F1 above them.
`reference_data.py` itself is not touched by any of this.

### `backend/server.py`

A ~110-line HTTP server using only Python's standard library
(`http.server`) — deliberately **not** Flask/FastAPI, so the backend needs
zero `pip install` and can never break from a dependency mismatch before a
defense. It has six routes: `GET /api/health`, `GET /api/examples`
(returns your `WORDS`/`SENTENCES`/`FAMILIES` data as ready-made example
strings), `POST /api/tokenize` (calls `trace_service.analyze(text)`), and
`POST /api/comparison/custom` (calls `comparison_service.custom_compare(text)`),
plus `GET /api/translation/status` and reserved
`POST /api/translate/compare`. `translation_service.py` derives checkpoint
readiness from `nllb/export_manifest.json`; the reserved compare route returns
503 until real model inference exists, preventing the UI from presenting mock
text as research output. CORS headers are added by hand for the same
zero-dependency reason.

### The frontend (`frontend/ui/`)

All new — a Vite + React app matching your provided design (Lexend font,
`#014CA9` main / `#272727` text, the pill-tab header, the two-card layout,
the Segmentation Process panel with the numbered steps and the token table).
The Comparison tab (`pages/ComparisonPage.jsx`) extends the same visual
language — same cards, same pill headers, same font/colors — with tokenizer
name badges (small dots, still within the blue/gray palette: main blue for
MorphBPE, gray for Plain BPE, a lighter blue tint for Unigram-LM) so the
three columns stay easy to scan across every section. It renders: the 3-way
split of your Tokenizer-tab input, a small bar chart per metric (plain CSS
bars, no charting library — consistent with the zero-dependency backend),
and a per-metric `<details>` disclosure with the `scoring_explain.py`
breakdown. Every page contains **no tokenizer logic and no scoring math at
all** — they only render whatever JSON the corresponding endpoint returns.

`pages/TranslatorComparisonPage.jsx` adds a symmetric translator A/B view:
one shared Kapampangan input followed by the MorphBPE source-tokenizer
condition and the original NLLB-200 baseline. It renders live readiness,
model/tokenizer identity, translation output, token counts, and latency. The
action remains disabled while either checkpoint or the inference adapter is
missing.

`App.jsx` owns the state that connects the two tabs: `comparisonInput` /
`comparisonResult` (plus loading/error) live there, `TokenizerPage` calls an
`onTokenized(text)` prop after every successful tokenize (and `onCleared()`
on Clear), and `App.jsx` uses that callback to fire
`compareCustom(text)` and store the result — so by the time you switch to
the Comparison tab, its data is usually already there.

## 3. End-to-end data flow — where every number on screen comes from

```
 [TokenizerPage.jsx]
   user types "d|in|atang ya at s|in|ulat ne", clicks Tokenize
        |
        v  tokenize(text)  in src/api.js
        |  POST http://127.0.0.1:8000/api/tokenize   body: {"text": "..."}
        v
 [backend/server.py]  do_POST()
        |  reads the JSON body into `text`
        v
 [trace_service.analyze(text)]
        |
        |-- raw_tokens = text.split()
        |-- sentence = [(surface_without_pipes, spec_with_pipes_or_""), ...]
        |-- clean_text = " ".join(surfaces)              <- this is ALL the
        |                                                    real tokenizer
        |                                                    ever sees; it
        |                                                    never sees "|"
        |-- TOKENIZER.encode(clean_text)                  <- the real,
        |     (real Tokenizer.encode, unmodified)             unmodified
        |                                                     algorithm
        |-- _pretokenize(normalized)                       <- real function,
        |     -> one entry per word/space/punctuation          just reused
        |-- for each "word" pretoken: trace_word(...)      <- new tracing
        |     -> steps[], final_tokens[]                      wrapper
        |-- _group_tokens_by_pretoken(...)                 <- groups the
        |     -> group_pieces = [("d","in","atang"), ("ya",), ...]
        |                                                     real encode()
        |                                                     output back
        |                                                     into per-word
        |                                                     groups
        |-- fertility = total tokens / total words          <- plain
        |                                                      arithmetic,
        |                                                      no gold
        |                                                      needed
        |-- IF any word had "|":
        |     rows = reference_data.rows_for(sentence)       <- gold pieces
        |     metrics = reference_data.score(rows, group_pieces)
        |       -> boundary_precision/recall/f1              <- copied
        |       -> mcf1 / mcf1_precision / mcf1_recall           verbatim
        |                                                        from
        |                                                        demo.py
        v
   returns one JSON object: { words: [...], fertility: {...}, gold: {...} }
        |
        v
 [TokenizerPage.jsx]  setResult(data)
        |
        |-- <ResultsPanel result={data}/>            reads data.fertility,
        |                                             data.gold.boundary_f1,
        |                                             data.gold.consistency_f1
        |
        v-- <SegmentationProcess result={data}/>     maps over data.words;
                                                       each WordCard reads
                                                       word.characters,
                                                       word.steps,
                                                       word.final_tokens
```

So concretely, to answer "where did you store the output of process 1 /
where did the F1 scores come from":

- There's no intermediate "storage" beyond one JSON response per request —
  the whole pipeline above runs inside a single call to `analyze()` and
  returns one dict. React holds that dict in one place:
  `const [result, setResult] = useState(null)` in `TokenizerPage.jsx`. Every
  panel just reads a different key off that same `result` object — nothing
  is recomputed on the frontend and nothing is cached beyond that one state
  variable.
- **Fertility Score** = `result.fertility.score`, computed in `analyze()` as
  `total tokens produced ÷ total words` — arithmetic only, real token counts
  from the real `encode()` call, no gold data involved.
- **Boundary F1** and **Consistency F1** = `result.gold.boundary_f1` /
  `result.gold.consistency_f1`, present only when you typed `|` marks. They
  come from `reference_data.score()`, which is your own `demo.py` scoring
  code, called on the real tokenizer's real output for your clean (pipe-free)
  text versus the gold pieces your `|` marks specified. If you don't mark any
  boundaries, `result.gold` is simply `null` and the UI shows "N/A" rather
  than inventing a number.

## 4. Known simplifications worth knowing about before your defense

- **Root/Affix legend colors** in the Segmentation Process panel are a
  **display heuristic**, not something the tokenizer computes: the longest
  final piece is colored "root," the rest "affix." The real tokenizer has no
  concept of root/affix at runtime (this matches your own project's central
  claim — see `kapampangan-pipeline-walkthrough.md` — that the shipped
  tokenizer is lexicon-free). If a panelist asks, the honest answer is "this
  color is just the longest piece, for visual intuition; the tokenizer
  itself doesn't label anything as root or affix."
- **Gold annotation only exists where you type `|`.** There's no automatic
  lookup against a hidden reference file for arbitrary words — that's a
  deliberate choice (see `README.md`) so the app never fabricates a
  Boundary F1 / Consistency F1 number for text with no gold morphology.
- **Case sensitivity is real** (inherited from the actual tokenizer, not
  introduced by this app) — `kumain` and `Kumain` can and do produce
  different splits. Worth remembering if you plan a live typed demo.
