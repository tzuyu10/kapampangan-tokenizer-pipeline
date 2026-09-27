# Run the translation and tokenization app

This app supports **Kapampangan to Filipino**, with separately trained Plain BPE and Morph-BPE source embeddings on NLLB-200 distilled 600M. It does not support the reverse direction. Translator lets you select a model and inspect its exact tokens. Translator A/B compares both outputs. The older Tokenizer tab is labeled as a penalty-32 training visualization.

## Requirements

- Git, Python **3.11 or 3.12**, and Node.js **22 LTS** with npm.
- Internet for dependency installation and the initial NLLB base download (approximately 2.5 GB). Allow additional space for environments and caches. 16 GB RAM is a practical target for CPU testing.
- One or both trusted trained model ZIPs supplied by the project maintainer. A fresh Git clone does not contain them.

All commands below start in the cloned repository root. Clone this repository using its actual GitHub URL, then open that folder in VS Code. Do not copy another device's virtual environment or node_modules.

## 1. Obtain the model bundles

Download `plain_bpe_inference.zip` and `morph_bpe_inference.zip` from this repository's Releases **after the maintainer uploads them**, or request them directly. They are not automatically available just because the source was pushed. The original Kaggle backup ZIPs are also accepted.

These bundles contain source weights, tokenizers, inference helper and provenance. They do not contain the frozen NLLB base. Inference ZIPs omit the optimizer checkpoint and cannot resume training; keep original Kaggle backups separately. Install trusted project bundles only, since their inference helper is Python code.

## 2. Windows: VS Code PowerShell

Run once:

```powershell
.\webapp\setup-translation.cmd
```

Wait for `Setup complete`. Install the two downloaded ZIPs (replace the example paths):

```powershell
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py "$HOME\Downloads\plain_bpe_inference.zip"
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py "$HOME\Downloads\morph_bpe_inference.zip"
```

The installer validates checksums and places them in `nllb/checkpoints/plain_bpe` and `nllb/checkpoints/morph_bpe`. It refuses to overwrite an existing bundle. Existing users with these bundles installed should skip these commands.

Start the backend:

```powershell
.\webapp\start-translation-backend.cmd
```

Keep it running. In a second terminal:

```powershell
Set-Location .\webapp\frontend\ui
npm.cmd ci
npm.cmd run dev
```

Open `http://localhost:5173`. Later starts only require the backend command and `npm.cmd run dev`; do not reinstall dependencies every time.

## 3. macOS / Linux

Use an installed Python 3.11 or 3.12 executable (substitute python3.11 if appropriate):

```bash
python3.12 -m venv .venv-translation
.venv-translation/bin/python -m pip install -r webapp/backend/requirements-translation.txt
.venv-translation/bin/python webapp/install-model-bundle.py ~/Downloads/plain_bpe_inference.zip
.venv-translation/bin/python webapp/install-model-bundle.py ~/Downloads/morph_bpe_inference.zip
.venv-translation/bin/python webapp/run-backend.py
```

In a second terminal from the repository root:

```bash
cd webapp/frontend/ui
npm ci
npm run dev
```

Open `http://localhost:5173`. These commands are provided for portability; local verification was performed on Windows, not macOS/Linux. CPU is the fallback. CUDA is selected automatically only with a compatible GPU and CUDA-enabled PyTorch installation. Apple MPS is not automatically selected.

## 4. Test from a phone or another computer on the same network

Run both services on the host computer as above, but start the frontend with:

```powershell
npm.cmd run dev -- --host 0.0.0.0
```

Use `npm run dev -- --host 0.0.0.0` on macOS/Linux. Open the **Network** URL printed by Vite on the other device, for example `http://192.168.1.10:5173`. Allow port 5173 through the host firewall on your private network if prompted. Both devices must be on a network that permits communication.

The browser calls `/api` on the frontend host. Vite proxies those requests to the backend on the same host, so you do not need to expose port 8000 or edit localhost in source files. Other devices do not need Python or model downloads for this mode. This is a development server for trusted local-network testing, not a public authenticated deployment.

If the backend runs elsewhere, set `BACKEND_URL` before starting Vite. A direct API deployment can set `VITE_API_BASE_URL`, which is a build-time public setting, not a secret. Backend host/port are configurable with `KAPAMPANGAN_HOST` and `KAPAMPANGAN_PORT`.

## 5. Check it works

- Select Plain BPE or Morph-BPE on Translator.
- Click Show tokens: this uses the exact installed artifact and does not need NLLB weights.
- Click Translate: the first request downloads/loads NLLB. Watch the backend terminal and wait; later requests reuse the base.
- Try Translator A/B once both bundles are installed.
- `/api/health` through the frontend checks connectivity. `/api/translation/status` distinguishes installed checkpoints from loaded models. Checkpoint availability does not guarantee that a first download will succeed.

The server shares frozen base weights, keeps separate source embeddings, uses four beams, and caches up to 128 repeated condition/text requests. Cache hits are labeled. Restart after changing any model bundle. CPU defaults to four threads; override with `KAPAMPANGAN_CPU_THREADS` if needed. Input is limited to 500 characters and the trained source-token limit.

## Evaluation

See `notebooks/NLLB_600M_Kaggle_Paired_Evaluation.ipynb` and `notebooks/README_PAIRED_EVALUATION.md`. Those instructions use original full Kaggle backups, not the inference-only ZIPs. The local web app does not calculate BLEU without references and should not be used for uncached timing benchmarks. Training and evaluation data are not required to serve translations.

## Troubleshooting

- **Python launcher missing:** install Python 3.11/3.12 with the Windows launcher, then reopen the terminal.
- **Setup failed:** read the pip error above the failure message; do not start the backend until installation succeeds.
- **Checkpoint unavailable:** obtain and install the model ZIP. Source code alone is not a trained model.
- **Backend unreachable:** keep its terminal running and check for startup errors. Avoid running two backends on port 8000.
- **Port 5173 occupied:** stop the old frontend or choose another port with `npm run dev -- --port 5174`. Vite uses strict ports so it does not silently move.
- **Download failure:** verify Internet access and restart the backend to retry. The base model cache lives under `.cache/huggingface` in the repository.
- **Another device cannot connect:** use Vite's Network URL, not localhost; check private-network firewall and Wi-Fi isolation.
- **Copy unavailable over LAN HTTP:** manually select the translation. Browsers can restrict clipboard access outside secure contexts.

## Maintainer: preparing the GitHub push

1. Review `git status` and `git diff`; this working tree contains thesis work in addition to web app changes. Do not discard unrelated changes or blindly stage everything.
2. Include `webapp` source, its existing UI package-lock.json, `.gitignore`, `.gitattributes`, this guide, and the root README update. Keep tokenizer artifact checksums together with the exact corresponding files. `.gitattributes` protects their bytes from line-ending conversion.
3. Keep `.venv*`, `node_modules`, `.cache`, `dist`, `nllb/checkpoints`, and `release-assets` out of Git. Never commit account tokens or local .env files.
4. Review and stage intended paths, for example `git add webapp README.md .gitignore .gitattributes`, then inspect `git diff --cached` before committing. Add evaluation notebooks separately if desired.
5. Commit and push to your chosen branch. No commit, push, or public release was performed by the setup work.
6. Upload the two inference ZIPs from the local ignored `release-assets` directory as GitHub Release assets, or distribute them privately. Only publish model/data assets you are authorized to share. Keep the pretrained NLLB base as an upstream download rather than including it in Git.
7. Test a fresh clone using these instructions. Do not rely on files that exist only in your original checkout.
