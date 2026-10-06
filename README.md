# Kapampangan Translation Web App

React + Vite frontend and a local Python backend for **Kapampangan to Filipino** translation using matched Plain BPE and Morph-BPE source embeddings on NLLB-200 distilled 600M.

The app has four tabs: Translator A/B, Translation Metrics & Process, Tokenization, and Tokenization Comparison & Metrics. The translation process shows actual token IDs, embedding and encoder vector slices, beam-search candidates, target-token decoding, and the final Filipino output.

## Clone this branch

```powershell
git clone --branch Latest/WebAppFull --single-branch https://github.com/tzuyu10/kapampangan-tokenizer-pipeline.git
Set-Location kapampangan-tokenizer-pipeline
```

If you already have this repository, use `Latest/WebAppFull` for the full source branch. Local UI edits must be committed and published before another device can obtain them through Git.

## Run the app

Follow **[webapp/RUNNING.md](webapp/RUNNING.md)** for prerequisites, Windows and macOS/Linux commands, model installation, troubleshooting, and testing from another device.

1. Install Python 3.11 or 3.12 and Node.js with npm.
2. Obtain both trusted model bundles from the maintainer: `plain_bpe_inference.zip` and `morph_bpe_inference.zip`. Original full project backup ZIPs are also accepted. The Git clone does not include trained models. No hosted download is assumed by these instructions.
3. On Windows, run `webapp\setup-translation.cmd`, install both ZIPs with `webapp/install-model-bundle.py`, then run `webapp\start-translation-backend.cmd`.
4. In a second terminal, open `webapp/frontend/ui`, run `npm.cmd ci`, then `npm.cmd run dev`.
5. Open **http://localhost:5173**. The first translation downloads the frozen NLLB base if it is not cached.

Only the computer running the backend needs Python and model files. Another device on the same network can use the app through the host's Vite Network URL as described in the guide.

## Use the four tabs

1. In **Translator A/B**, enter one Kapampangan sentence and compare Plain BPE with Morph-BPE.
2. Open **Translation Metrics & Process** to view the same run's token counts, timing, model diagnostics and selectable process trace. Switching tabs does not run the model again.
3. In **Tokenization**, enter text to see token output and segmentation steps.
4. Open **Tokenization Comparison & Metrics** for the same tokenization input's splits, fertility and morphology F1 charts, plus initial diagnostics.

Inputs/results persist while switching tabs. Editing translation input clears its previous process. BLEU/chrF++ remain unavailable until paired held-out evaluation is completed. See [initial metrics and scope](docs/INITIAL_UI_METRICS.md).

## Source and models

This full source branch contains app source, tokenizer artifacts, research/training code and notebooks, dependency manifests, setup scripts, regression tests, and project guidance. Trained model weights, environments, caches and build outputs are not supplied by the clone.

The installer creates `nllb/checkpoints/plain_bpe` and `nllb/checkpoints/morph_bpe` locally. Preserve complete tokenizer artifact inventories and their checksums. Keep full training backups separately because inference bundles cannot resume training.

## Verification

Frontend production build:

```powershell
Set-Location webapp/frontend/ui
npm.cmd run build
```

Backend regression tests, from the repository root after setup:

```powershell
.\.venv-translation\Scripts\python.exe -m unittest discover -s webapp/backend -p "test_*.py" -v
```

These checks verify the frontend build and tracing/response behavior. They do not establish translation quality. The app does not support Filipino-to-Kapampangan translation.
