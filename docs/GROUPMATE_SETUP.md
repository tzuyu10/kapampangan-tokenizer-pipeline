# Run the revised app on a groupmate's device

This guide targets the proposed branch **`codex/tokenizer-team-revision`**. The maintainer must first complete [PUBLISH_FULL_REPOSITORY.md](PUBLISH_FULL_REPOSITORY.md). Until that push happens, this branch is not available remotely.

## Install these once

| Install | Use |
| --- | --- |
| [Git](https://git-scm.com/downloads/) | Clone and pull source |
| [Standard 64-bit Python 3.12 or 3.13](https://www.python.org/downloads/) | Backend and translation dependencies; enable the Windows Python launcher |
| [Node.js 22 with npm](https://nodejs.org/en/download) | React/Vite frontend; select the 22.x installer |
| Browser | Open the app |

The setup script also supports standard Python 3.11. Use the listed Python versions for this pinned dependency set; do not assume a newer Python release is compatible. Do not choose free-threaded Python. VS Code is optional. CPU inference works without a GPU, but the first translation and longer sentences may be slow. 16 GB RAM is a practical target, not a measured minimum. Allow several GB of free storage and Internet for dependencies and the initial NLLB base download, approximately 2.5 GB.

No Rust build, database, Docker installation, retraining, copied virtual environment or copied `node_modules` is needed to run the webapp. The backend dependencies, including PyTorch and the pinned Transformers/tokenizer libraries, are installed by the provided script.

## 1. Clone the published branch

In PowerShell, navigate to the parent folder where you want the project:

```powershell
git clone --branch codex/tokenizer-team-revision --single-branch https://github.com/tzuyu10/kapampangan-tokenizer-pipeline.git
Set-Location kapampangan-tokenizer-pipeline
git branch --show-current
```

For an existing clone, first save or commit your own edits. Then, from its repository root:

```powershell
git fetch origin codex/tokenizer-team-revision:refs/remotes/origin/codex/tokenizer-team-revision
git switch --track origin/codex/tokenizer-team-revision
```

If you already created this local branch, use `git switch codex/tokenizer-team-revision` instead of `--track`, followed by `git pull --ff-only`. Stop and resolve your own pending edits if Git refuses a switch. Do not reset or delete your work.

## 2. Install the backend dependencies

All remaining commands start at the repository root unless stated otherwise:

```powershell
.\webapp\setup-translation.cmd
```

Wait for `Setup complete`. The script selects available Python 3.13, then 3.12, then 3.11 for a new `.venv-translation`. An existing environment is reused. No environment activation is required for the commands in this guide.

## 3. Download and verify the trained models

Get the maintainer's model ZIPs and matching `share-manifest.json` and `SHA256SUMS.txt`. They are separate from Git. For the current three translation choices, download:

- `plain_bpe_inference.zip`
- `morph_bpe_inference.zip`
- `morph_bpe_infix_first_penalty48_inference.zip`

The optional three historical bundles in the publishing guide reproduce the full six-bundle menu. You do not need them to run the current models. Keep each ZIP intact; do not extract and combine files from different bundles. These packages include Python helper code, so use the project's trusted exports.

Put downloaded files together, for example in `Downloads\team-models-20261017-all6`, then verify each downloaded ZIP against the supplied manifest before installation:

```powershell
$bundleDownloads = Join-Path $HOME 'Downloads\team-models-20261017-all6'
$shareManifest = Get-Content (Join-Path $bundleDownloads 'share-manifest.json') -Raw | ConvertFrom-Json
foreach ($bundleRecord in $shareManifest.bundles) {
    $archivePath = Join-Path $bundleDownloads $bundleRecord.archive
    if (Test-Path -LiteralPath $archivePath) {
        $actualHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash
        if ($actualHash -ne $bundleRecord.sha256) { throw "Checksum mismatch: $archivePath" }
        Write-Host "Verified $($bundleRecord.archive)"
    }
}
```

Check that all three required files are present. Then install them:

```powershell
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'plain_bpe_inference.zip') --name plain_bpe
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'morph_bpe_inference.zip') --name morph_bpe
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'morph_bpe_infix_first_penalty48_inference.zip') --name morph_bpe_infix_first_penalty48
.\webapp\start-translation-backend.cmd --list-models
```

The installer validates inventories and identities, and creates the matching folders under `nllb/checkpoints/`. It refuses an existing folder. If already installed and unchanged, skip reinstalling. For a genuinely new trained export, install it with a new unique `--name`, retain the previous bundle, and select the new name at startup. Never mix an old embedding table with a new tokenizer.

For an optional historical ZIP, pass its corresponding folder name with `--name`, such as `plain_bpe_15`. Omitting `--name` on historical archives would target the original Plain/Morph slot and is not the intended installation here.

To install the three historical choices too, use unique names so they appear as separate choices in the startup menu:

```powershell
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'plain_bpe_15_inference.zip') --name plain_bpe_15
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'morph_bpe_15_inference.zip') --name morph_bpe_15
.\.venv-translation\Scripts\python.exe .\webapp\install-model-bundle.py (Join-Path $bundleDownloads 'morph_bpe_hard30_backup_20261008_inference.zip') --name morph_bpe_hard30_backup_20261008
```

## 4. Start the backend, terminal 1

```powershell
.\webapp\start-translation-backend.cmd
```

Choose one Plain BPE and one Morph-BPE bundle in the numbered startup menu. To run a repeatable Plain30 versus trained infix48 comparison:

```powershell
.\webapp\start-translation-backend.cmd --plain-bundle plain_bpe --morph-bundle morph_bpe_infix_first_penalty48
```

Use one startup command at a time. For the current weighted penalty32 Morph model, replace the final name with `morph_bpe`, or use `--defaults`. Keep this terminal running. Stop it with Ctrl+C before changing selections. The backend normally listens at `http://127.0.0.1:8000`.

## 5. Start the frontend, terminal 2

Open another PowerShell at the repository root:

```powershell
Set-Location webapp/frontend/ui
npm.cmd ci
npm.cmd run dev
```

Open **http://localhost:5173**. Keep both terminals running. Run `npm.cmd ci` again when pulling a changed `package-lock.json`.

## 6. Check the tokenizer and translator separately

In **Tokenization**, choose either:

- **Infix + affix priority Morph-BPE, penalty 48, 6,080 tokens (Kapampangan + Tagalog)**
- **Infix + affix priority Morph-BPE, penalty 48, 8,192 tokens (Kapampangan + Tagalog)**

Enter `nagaral`, then click **Tokenize**. Both should display `nag | aral`. These exports use morphology during training only. Runtime uses their ordinary learned BPE merges, with no morphology lookup or word-specific overrides. The previous infix-first48/6,080 default remains selected initially because the new targeted splits did not improve overall evaluation. **Tokenization Comparison & Metrics** uses the selected Morph tokenizer and matching 6k/8k Plain BPE and Unigram controls.

The six earlier Kapampangan + Tagalog family/size options, historical weighted32 and older infix-priority packs are included in source too. Installed trained bundles add their own tokenizer options. Therefore a device with fewer installed model bundles can show fewer `trained:` options while still having all shipped standalone tokenizers.

In **Translator A/B**, compare a short Kapampangan sentence. The first translation downloads and loads the pinned frozen NLLB base if absent. Watch the backend terminal and wait. Later requests reuse it. The Tokenization dropdown does not change translation model weights. The new Tagalog-augmented tokenizers still need their own matching source-embedding training before future translation use.

## Later runs and updates

From the repository root, stop running servers, then:

```powershell
git switch codex/tokenizer-team-revision
git pull --ff-only
.\webapp\setup-translation.cmd
.\webapp\start-translation-backend.cmd
```

Start the frontend again in a second terminal. Re-run `npm.cmd ci` there if dependencies changed. Pulling code does not download or replace trained bundles. Obtain new model ZIPs separately when the maintainer supplies a new trained version. Existing valid local bundles are retained by Git updates.

If only testing tokenizer tabs, model ZIPs and NLLB downloads are unnecessary: start the backend using `py -3.13 .\webapp\backend\server.py` (use your installed supported Python version), then start the frontend normally. Translation remains unavailable without the trained bundles and translation dependencies.

## macOS/Linux

Use the same published branch, model ZIPs and folder names. Replace the Windows dependency setup with:

```bash
python3.12 -m venv .venv-translation
.venv-translation/bin/python -m pip install --upgrade pip
.venv-translation/bin/python -m pip install -r webapp/backend/requirements-translation.txt
.venv-translation/bin/python -m pip check
.venv-translation/bin/python webapp/install-model-bundle.py ~/Downloads/team-models-20261017/plain_bpe_inference.zip --name plain_bpe
.venv-translation/bin/python webapp/install-model-bundle.py ~/Downloads/team-models-20261017/morph_bpe_inference.zip --name morph_bpe
.venv-translation/bin/python webapp/install-model-bundle.py ~/Downloads/team-models-20261017/morph_bpe_infix_first_penalty48_inference.zip --name morph_bpe_infix_first_penalty48
.venv-translation/bin/python webapp/run-backend.py --plain-bundle plain_bpe --morph-bundle morph_bpe_infix_first_penalty48
```

In a second terminal: `cd webapp/frontend/ui`, `npm ci`, then `npm run dev`. Use `python3.13` instead if that is the installed supported interpreter. CUDA is used when available; otherwise the current backend uses CPU. These macOS/Linux commands are provided for portability and have not been run on those operating systems in this task.

## Common problems

- Branch not found: the maintainer must push the named branch first, and private-repository members need repository access.
- Python not found: install standard supported 64-bit Python with the Windows launcher, reopen PowerShell, then run setup again.
- Model missing: install the separate ZIP. `git pull` only supplies source/tokenizer files.
- Checksum or package validation fails: download the original complete ZIP again; preserve `.gitattributes` and all exported tokenizer files.
- Port already in use: stop an earlier server. Frontend defaults to 5173, backend to 8000. See [RUNNING.md](../webapp/RUNNING.md) for alternate ports and LAN hosting.
- First translation fails: check the backend error, Internet access and available RAM/storage. A bundle can validate while the frozen base download is still unavailable.
- Backend dependency error after pulling: rerun setup; do not install arbitrary newer versions over the pinned requirements.

The documented local checks validate exports, model identities, tokenizer behavior and the app build. They do not prove that a new device has completed its first NLLB download or that a tokenizer has better translation quality.
