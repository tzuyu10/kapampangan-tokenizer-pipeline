> **Current setup for new devices:** follow [RUNNING.md](RUNNING.md). It includes model installation, Windows/macOS/Linux commands, and local-network access.

# Plain BPE translation integration

Installed bundle: `nllb/checkpoints/plain_bpe`. Best validation checkpoint: epoch 15, loss 1.342994. Source embeddings only; the pinned NLLB base is loaded separately. No evaluation scores are claimed.

## Start on this computer

1. Stop an older backend using port 8000, if one is running.
2. Once, run `webapp\setup-translation.cmd` (requires installed Python 3.12 or 3.11 and Internet). Then run `webapp\start-translation-backend.cmd`.
3. In a second CMD window, change directory to `webapp\frontend\ui` and run `npm run dev`.
4. Open the URL printed by Vite. The Translator page runs Plain BPE. The comparison page can show Plain BPE alone while Morph-BPE is unavailable.

The launcher resolves the pipeline root relative to its own file. It uses only `.venv-translation` for dependencies, `.cache/huggingface` for model downloads, and `nllb/checkpoints` for trained bundles within that root. Setup uses the installed Windows Python launcher to create the local virtual environment and caches packages under `.cache/pip`. There is no dependency on the Thesis Time workspace. First inference downloads the pinned NLLB base if missing. CPU inference works but is slower; CUDA is selected automatically if available. Do not start another copy while the original still owns port 8000.

## Other computers

Create a dedicated Python environment and install `webapp/backend/requirements-translation.txt`, then run `python webapp/backend/server.py`. Install a CUDA-compatible PyTorch build if GPU inference is desired. Preserve the entire bundle; never load its directory directly with AutoModel.from_pretrained.

POST `/api/translate` accepts `{"text":"Masanting ya ing abak.","condition":"plain_bpe"}`. POST `/api/translate/compare` returns the installed conditions. GET `/api/translation/status` distinguishes installed and loaded models; the first request can fail if base download or memory allocation fails. Requests are serialized to protect model inference. Inputs over 500 characters or the trained token limit are rejected instead of truncated.

The complete Morph-BPE bundle can later be placed at `nllb/checkpoints/morph_bpe`; its manifest must declare morph_bpe. Restart the backend after installing or replacing bundles. A full scientific comparison still requires matched settings and held-out evaluation.


## Inference performance

The backend shares a single frozen NLLB base between compatible conditions, and swaps only their separate source-embedding modules under the inference lock. Beam count (4), output limit (160), FP32 precision, and trained weights are unchanged. Tokenizers and validated manifests are cached for the process lifetime; restart the backend after replacing a bundle. Up to 128 exact condition/text results are cached in memory; the UI labels cache hits. This cache is for interactive use, not measuring model latency in thesis evaluation.

CPU inference defaults to four threads, capped by available logical cores. To override in PowerShell before startup, set `$env:KAPAMPANGAN_CPU_THREADS = "6"`. CPU thread count is hardware-dependent; a short local test measured about 4.8 seconds at four threads versus 8.7 seconds at six threads, with identical output. This is not a corpus-wide benchmark. Cached requests avoid model generation. Initial loading still takes time. GPU is used automatically when a CUDA-enabled PyTorch environment and compatible GPU are available.
