# Run the translation and tokenization app

This app supports **Kapampangan to Filipino**, with separately trained Plain BPE and Morph-BPE source embeddings on NLLB-200 distilled 600M. It does not support the reverse direction. Translator lets you select a model and inspect its exact tokens. Translator A/B compares both outputs. The older Tokenizer tab is labeled as a penalty-32 training visualization.

## Presenting the translation process

In **Translator A/B**, enter a sentence in the left Kapampangan card and click **Compare translations**. Both Filipino results and generation statistics appear in the right Results card. Narrow screens stack the cards. Below them, choose **Morph-BPE** or **Plain BPE** to explain that condition's actual translation. The single Translator tab includes the same process panel.

The numbered flow is: prepare input, tokenize Kapampangan, look up source embeddings, encode the sentence, generate target tokens with the decoder, decode using the native NLLB target tokenizer, and display Filipino output. Source pieces and vocabulary IDs, mapped model input IDs, target pieces and generated IDs come from the selected inference result. Embedding and encoder tables show the first four actual vector values per source position, rounded for readability. Embeddings include the model's lookup scaling, before positions are added. Encoder vectors are the last encoder-layer output; they are not new token IDs.

Use **Previous**, **Next**, or **Decoder step** to walk through the real generation. **Incoming beam** selects a prefix and its top four next-token candidates. Four beams means four candidate sequences, not only four possible words. A second table shows the beam slots retained after each step; completed candidates are handled separately. Highlighting identifies prefixes matching the returned output retrospectively. The final candidates table shows actual sequence scores including the length penalty and marks the selected translation. Forced language/EOS constraints can leave fewer than four finite next-token candidates. Scores are log scores, not confidence percentages or translation-quality measures.

The native NLLB target tokenizer table shows generated ID to token piece to growing readable text, with control tokens removed. It formats the model's output and does not translate the source by itself. All displayed vectors and candidate scores are observed during the original generation under the model lock, without changing generation settings or making an extra model pass. `generation_trace.py` observes the pinned Transformers 4.48.3 beam-search implementation and removes its hooks even on failure. Only small vector slices and candidate lists are stored, not full vocabulary score tensors. Reported generation time includes observation overhead and should not be compared directly with timings from uninstrumented runs.

Only source embeddings were trained; pretrained encoder and decoder layers remain frozen. Generation statistics are not quality scores. Editing or clearing the input clears its previous results. Restart an already-running backend after updating the code so translation responses include the new `process` data. Cached translations retain that data and are labeled Cached.

Backend regression checks: run `.venv-translation/Scripts/python.exe -m unittest discover -s webapp/backend -p "test_*.py" -v` on Windows (use `.venv-translation/bin/python` on macOS/Linux). Response tests use a mocked generation result; trace tests use a tiny real encoder-decoder to verify unchanged output, exact vector slices/candidate scores/final scores, beam continuity, and hook cleanup. No pretrained download or translation-quality evaluation is required for these tests.

## Requirements

- Git, standard 64-bit Python **3.11, 3.12 or 3.13**, and Node.js **22 LTS** with npm.
- Internet for dependency installation and the initial NLLB base download (approximately 2.5 GB). Allow additional space for environments and caches. 16 GB RAM is a practical target for CPU testing.
- One or both trusted trained model ZIPs supplied by the project maintainer. A fresh Git clone does not contain them.

Clone the app branch, then open its folder in VS Code:

```powershell
git clone --branch Latest/WebApp --single-branch https://github.com/tzuyu10/kapampangan-tokenizer-pipeline.git
Set-Location kapampangan-tokenizer-pipeline
```

All setup commands below start in the cloned repository root unless stated otherwise. Do not copy another device's virtual environment or node_modules.

## 1. Obtain the model bundles

Obtain `plain_bpe_inference.zip` and `morph_bpe_inference.zip` directly from the project maintainer. Both are needed for the complete Translator A/B comparison. If the maintainer later publishes Release assets, those can be used instead. No public model download is assumed by this guide; pushing the source does not publish the bundles. Original full project backup ZIPs are also accepted.

These bundles contain source weights, tokenizers, inference helper and provenance. They do not contain the frozen NLLB base. Inference ZIPs omit the optimizer checkpoint and cannot resume training; keep original Kaggle backups separately. Install trusted project bundles only, since their inference helper is Python code.

## 2. Windows: VS Code PowerShell

Run once:

```powershell
.\webapp\setup-translation.cmd
```

For a new environment, setup selects Python 3.13 first, then 3.12 or 3.11 if unavailable. It reuses an existing `.venv-translation` and prints its Python version. Installing Python 3.13 does not change an environment already created with Python 3.12.

To switch an existing environment to 3.13, stop the backend, install standard 64-bit Python 3.13 with the Windows launcher, and rename `.venv-translation` to an unused backup name before running setup again. Model bundles in `nllb/checkpoints` do not need reinstalling or retraining. Free-threaded Python 3.13t is not covered by these instructions.

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

Use an installed standard Python 3.11, 3.12 or 3.13 executable (substitute python3.11 or python3.12 if appropriate):

```bash
python3.13 -m venv .venv-translation
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

Research evaluation notebooks and datasets are excluded from this app-only branch and remain on the research branches, including `nllb/translation`. Evaluation uses original full project backups, not the inference-only ZIPs. The local web app does not calculate BLEU without references and should not be used for uncached timing benchmarks. Training and evaluation data are not required to serve translations.

## Troubleshooting

- **Python launcher missing:** install standard 64-bit Python 3.11, 3.12 or 3.13 with the Windows launcher, then reopen the terminal.
- **Python 3.13 dependency installation:** use the repository's current requirements file. It installs SentencePiece 0.2.1 on Python 3.13 and preserves 0.2.0 on Python 3.11/3.12. The other translation dependency constraints remain unchanged.
- **Setup failed:** read the pip error above the failure message; do not start the backend until installation succeeds.
- **Checkpoint unavailable:** obtain and install the model ZIP. Source code alone is not a trained model.
- **Backend unreachable:** keep its terminal running and check for startup errors. Avoid running two backends on port 8000.
- **Port 5173 occupied:** stop the old frontend or choose another port with `npm run dev -- --port 5174`. Vite uses strict ports so it does not silently move.
- **Download failure:** verify Internet access and restart the backend to retry. The base model cache lives under `.cache/huggingface` in the repository.
- **Another device cannot connect:** use Vite's Network URL, not localhost; check private-network firewall and Wi-Fi isolation.
- **Copy unavailable over LAN HTTP:** manually select the translation. Browsers can restrict clipboard access outside secure contexts.

## Maintainer: app-only distribution

- Keep app source, dependency manifests and UI lockfile, complete legacy tokenizer artifacts, setup scripts, this guide, and root project guidance together. Regression tests verify the translation process without downloading the base model.
- Keep the checksum-preserving `.gitattributes` rule. Removing files listed in a tokenizer artifact's checksum inventory prevents backend startup.
- Do not commit environments, node_modules, caches, build outputs, installed checkpoint folders, local distribution ZIPs, or credentials. The root ignore rules intentionally keep research files outside this branch's tracked snapshot.
- Supply both trained model ZIPs to users separately. Keep full training backups for resume; inference-only bundles omit the optimizer checkpoint and do not include the frozen NLLB base.
- Verify a fresh checkout with dependency installation, both installed bundles, tokenizer inspection, Translator, and Translator A/B before reporting a new device as tested.
