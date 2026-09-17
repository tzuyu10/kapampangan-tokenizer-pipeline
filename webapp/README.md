# Kapampangan Tokenizer — Web App

A React frontend + Python backend that puts your trained MorphBPE tokenizer
(`morphbpe-penalty32`, a weighted-MorphBPE candidate — swapped in
2026-09-13, trained on the richer `expanded_morphology_v4` lexicon
(3,311 roots) after scoring the crossing-penalty sweep against both the
real `data/validation.csv` and the authoritative, partially-human-verified
`tokenizer_selection_v1` DEV/TEST reference; penalty=32 beats the
previously-established `penalty-8` "Phase 3" winner on both — see
`experiments/expanded_morphology_v4_penalty_extension_v1/README.md`)
behind a browser UI, matching the "Translator / Tokenizer" design you
provided, plus a third **Comparison** tab. The **Tokenizer** tab is fully
working and shows the real, live, step‑by‑step segmentation process for
anything you type. The **Comparison** tab is also fully working: it takes
the exact same text you just tokenized on the Tokenizer tab and compares
MorphBPE penalty-32, Plain BPE, and Unigram-LM (NLLB's own algorithm) side
by side — word splits, a
bar-chart score comparison, and a "how these scores are computed" panel that
shows the literal intermediate values (true/false positives, boundary
positions, shared-morpheme groups) the scoring code produced for your input.
The **Translator** tab is a UI shell only. A separate **Translator A/B** tab
now presents the planned controlled comparison between MorphBPE + NLLB-200
and the original NLLB-200 baseline. It reads live checkpoint readiness from
the backend and deliberately displays no generated text while the models are
absent — see [Translator tabs](#translator-tabs-not-functional) below.

The tokenizer algorithm itself is **not modified in any way** — see
`ARCHITECTURE.md` for exactly what this project added versus what was copied
untouched from your research repo.

```
kapampangan-tokenizer-app/
├── README.md              <- you are here
├── ARCHITECTURE.md        <- what changed, what didn't, how data flows end-to-end
├── backend/
│   ├── server.py          <- the HTTP API (stdlib only, no pip install needed)
│   ├── translation_service.py <- truthful NLLB checkpoint/readiness metadata
│   └── tokenizer/
│       ├── kapampangan_morphbpe_runtime/   <- UNCHANGED copy of your runtime
│       │   ├── __init__.py
│       │   └── tokenizer.py
│       ├── artifacts/
│       │   ├── morphbpe-penalty32/         <- copy of the 9 artifact files (penalty=32, see above)
│       │   ├── plain-bpe/                  <- UNCHANGED copy, same runtime class
│       │   └── unigram-lm-6080/            <- UNCHANGED copy (tokenizer.json + manifest)
│       ├── unigram_lm.py                   <- the UnigramLM Viterbi decoder, copied verbatim
│       ├── reference_data.py               <- gold data + scoring fns, copied from demo.py (untouched)
│       ├── scoring_explain.py              <- NEW: "show your work" diagnostic scoring (Comparison tab)
│       ├── trace_service.py                <- NEW: step-tracing + API orchestration (Tokenizer tab)
│       ├── comparison_service.py           <- NEW: 3-way comparison orchestration (Comparison tab)
│       └── _reference_demo_source.py       <- your original demo.py, kept for reference
└── frontend/
    └── ui/                <- Vite + React app
        ├── package.json
        ├── index.html
        └── src/
            ├── main.jsx, App.jsx            <- App.jsx owns the shared Tokenizer↔Comparison state
            ├── api.js                       <- fetch wrapper to the backend
            ├── styles/global.css            <- Lexend font + your color palette
            ├── components/
            │   ├── Header.jsx               <- app navigation tabs
            │   ├── ResultsPanel.jsx         <- Fertility / Boundary F1 / Consistency F1
            │   ├── SegmentationProcess.jsx  <- the step-by-step panel
            │   ├── ExampleChips.jsx         <- one-click known-good demo inputs
            │   └── icons.jsx
            └── pages/
                ├── TokenizerPage.jsx        <- fully functional
                ├── ComparisonPage.jsx       <- fully functional (mirrors the Tokenizer tab's input)
                ├── TranslatorPage.jsx       <- UI shell only, not wired up
                └── TranslatorComparisonPage.jsx <- honest A/B translation interface
```

## Prerequisites

- **Python 3.11 or later** (the runtime uses `dataclass(slots=True)` and
  `itertools.pairwise`, both 3.10+; the artifact's own README asks for 3.11+).
  No `pip install` needed — the backend uses only the standard library.
- **Node.js 18+** and **npm**, for the React frontend.

## 1. Run the backend

```bash
cd backend
python server.py
```

You should see:

```
[startup] trace/encode parity check: 30/30 words passed
[startup] scoring-explain parity check: 6/6 cases passed
[startup] tokenizer artifact loaded: morphbpe-penalty32 (vocab size 6080)
[startup] comparison artifacts loaded: plain-bpe (vocab size 6080), unigram-lm-6080 (vocab size 6080)
[startup] serving on http://127.0.0.1:8000  (Ctrl+C to stop)
```

Both parity checks run automatically every time the server starts — self-
tests that (1) the step-by-step trace this app displays always agrees with
the real tokenizer's own `encode()` output, and (2) the "how it's computed"
breakdown on the Comparison tab always agrees with `reference_data.py`'s own
`score()`/`mcf1()` numbers (see `ARCHITECTURE.md`). If either ever fails,
the server won't start, and the exact mismatch is in the error.

Leave this running. It serves six endpoints on `http://127.0.0.1:8000`:
`GET /api/health`, `GET /api/examples`, `POST /api/tokenize`,
`POST /api/comparison/custom`, `GET /api/translation/status`, and the reserved
`POST /api/translate/compare` route. The reserved route returns HTTP 503 until
real inference is available; it never returns placeholder translations.

## 2. Run the frontend

In a second terminal:

```bash
cd frontend/ui
npm install
npm run dev
```

Open the URL it prints (default `http://localhost:5173`). The Tokenizer tab
is the default view.

> If your network blocks `npm install` from finishing, run it from a
> machine/network that has normal internet access — it only needs to fetch
> `react`, `react-dom`, `vite`, and `@vitejs/plugin-react`.

## 3. Using it

Type or paste Kapampangan text into the left box and press **Tokenize**.

- **Fertility Score** is always computed — it needs no reference data.
- **Boundary F1** and **Consistency F1** need gold morpheme boundaries. Mark
  them yourself using the **same `|` convention your own `demo.py` CLI
  already used**: type `s|in|ulat` instead of `sinulat`, and the app strips
  the `|` before tokenizing but uses it to score the real output against
  that gold split. Type a full sentence the same way, e.g.
  `d|in|atang ya at s|in|ulat ne`. Words without a `|` count as one gold
  morpheme (matches `demo.py`'s own `custom_section` behavior).
- Without any `|` in the input, Boundary F1 / Consistency F1 show **N/A** —
  this is intentional; there is no gold reference for arbitrary text, so the
  app never fabricates a score for it.
- The **example chips** under the input are pulled live from
  `GET /api/examples` (your own `WORDS` / `SENTENCES` lists from `demo.py`)
  so you always have a few one-click, known-good inputs for a live demo —
  useful if you don't want to type Kapampangan text from memory in front of
  a panel.
- The **Segmentation Process** panel shows one card per word: normalize →
  word detection (vocabulary shortcut vs. character split) → raw characters
  → every merge rule applied, in the priority order it was learned during
  training → the final tokens with their vocabulary IDs.

## 4. Using the Comparison tab

The Comparison tab has **no input box of its own** — it always shows the
3-way comparison for whatever text you last tokenized on the **Tokenizer**
tab. Type/pick an example there, press **Tokenize**, then switch to
**Comparison**:

- **Your Input — 3-Way Split** — the exact text you just tokenized, run
  through MorphBPE penalty-32, Plain BPE, and Unigram-LM live.
- **Score Comparison** — a bar chart per metric (Fertility always; Boundary
  F1 and Consistency F1 once you've marked gold boundaries with `|`, e.g.
  `s|in|ulat`, same convention as the Tokenizer tab), one bar per tokenizer,
  color-matched to their dots elsewhere in the app.
- **How These Scores Are Computed** — an expandable, per-tokenizer
  walkthrough of the *actual intermediate values* the scoring code produced
  for your input: for Boundary F1, a table of every word's gold vs.
  predicted cut positions and the resulting TP/FP/FN counts feeding
  precision/recall/F1; for Consistency F1 (MCF1), which words got grouped
  by a shared gold morpheme vs. a shared produced token, and exactly which
  word-pairs counted as a match, a miss, or an extra. These numbers are not
  a re-explanation — `backend/tokenizer/scoring_explain.py` computes them
  with the same loops as `reference_data.py`'s `score()`/`mcf1()`, and a
  startup parity check (see above) guarantees they can never disagree with
  the real Boundary F1 / Consistency F1 shown just above them.

This replaced an earlier version of this tab that reproduced `demo.py`'s
own fixed showcase (hand-picked words/families/sentences) as a static page;
that's gone now in favor of comparing whatever you're actually testing on
the Tokenizer tab, which is more useful for a live defense. The four
official Phase 3 held-out numbers (MorphBPE penalty-8 0.4639 dev / 0.4093
test — selected, Unigram-LM 0.293, MorphBPE hard-constrained 0.268, Plain
BPE 0.198) aren't shown on this tab anymore; cite them from your thesis
directly if asked, since there's no `hard-constrained` artifact in this demo
folder to recompute them from live.

## Translator tabs (not functional)

The Translator page matches your design pixel-for-pixel but doesn't call
anything — there is no trained Kapampangan→Filipino translation model yet.
Per your own project docs (`PAPER_TRACEABILITY.md` / `LIMITATIONS.md`),
NLLB-200 download and fine-tuning are explicitly future work, not done. The
**Translate** button is disabled and the page says so under the two boxes.
The **Clear** button and the **Copy** icon on the Filipino side both work
locally (no backend needed) since they don't require translation.

The **Translator A/B** page is the comparison interface for the future
experiment. It sends one Kapampangan input to two conditions and is designed
to show their Filipino output, tokenizer/model identity, source/output token
counts, and latency side by side:

- **MorphBPE + NLLB-200** — the proposed source-tokenizer and matching
  encoder-embedding condition.
- **Original NLLB-200** — the unchanged pretrained tokenizer/model baseline.

Today both cards show **Checkpoint required**, based on
`nllb/export_manifest.json`. The compare button stays disabled because the
repository explicitly records `nllb_model_downloaded: false` and
`nllb_model_trained: false`. Use **Load demo data** to populate both cards
with visibly labeled dummy translations and metrics for interface testing;
demo values are never sent to or returned by the translation API.

## Troubleshooting

- **"Could not reach the tokenizer backend"** in the UI — `python server.py`
  isn't running, or it's on a different port than `8000`. Check the terminal
  running it.
- **CORS error in the browser console** — the frontend must be served from
  `http://localhost:5173` or `http://127.0.0.1:5173` (Vite's defaults). If
  you changed the Vite port, add it to `ALLOWED_ORIGINS` in `backend/server.py`.
- **Parity check fails at startup** — this would mean the display logic and
  the real tokenizer disagree on some word, which should not happen; if it
  does, please don't ignore it — it means something is inconsistent between
  the artifact files and the runtime code (e.g. artifact files were edited).
