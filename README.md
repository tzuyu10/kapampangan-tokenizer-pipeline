# Kapampangan Tokenizer — Web App (trained-tokenizer-only branch)

This branch contains only what's needed to run the web app: the backend,
frontend, and the trained tokenizer artifacts it serves. No training code,
experiments, or research history — see the `Draft/Tool-V2` branch (or
`main`) for the full pipeline.

**To run it, see [webapp/README.md](webapp/README.md).**

Quick start:

```bash
python webapp/backend/server.py
```

```bash
cd webapp/frontend/ui
npm install
npm run dev
```

The live tokenizer is `morphbpe-penalty32` (`webapp/backend/tokenizer/artifacts/morphbpe-penalty32/`) —
see `webapp/ARCHITECTURE.md` for what it is and how it was chosen.
