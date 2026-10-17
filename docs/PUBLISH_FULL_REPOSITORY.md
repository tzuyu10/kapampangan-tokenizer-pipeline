# Publish the revised full repository

Prepared on 2026-10-17. These are commands for the maintainer to run. No new branch, staging, commit or push was performed when this guide was prepared.

## What will be published

Publish the current intended project source: webapp, tokenizer exports and runtimes, research/training code, notebooks, tests, dependency manifests, lockfile and documentation. This includes the earlier pending translator/model-selection changes as well as the new tokenizer options.

The current checkout is `Final/ToolV1` at `f895ed7`. Create the new branch from this checkout so its pending changes come with you. The proposed destination is **`codex/tokenizer-team-revision`**. It does not become downloadable until you push it. If you choose another name, replace it in both this guide and `GROUPMATE_SETUP.md`.

The root ignore rules already allow full project source. Do not replace them with the old app-only ignore file. Installed weights under `nllb/checkpoints/`, `.venv*`, `node_modules`, `.cache`, `release-assets`, builds and credentials stay local. Verified tokenizer-only packs are included explicitly by `webapp/.gitignore`. Keep `.gitattributes`: it prevents line-ending conversion from breaking their SHA-256 checksums on another device.

The trained bundles are shared separately. The six prepared inference ZIPs are about 28 MB each, so they are below GitHub's regular Git 50 MB warning and 100 MB hard per-file limit. They could technically be committed, but this project keeps model binaries outside the source branch so every clone stays focused on code and tokenizer resources. A GitHub release or private file share can distribute them separately. See [GitHub's file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

## 1. Create a branch while retaining the current work

Open PowerShell in the existing project:

```powershell
Set-Location C:\Users\Gabo\kapampangan-tokenizer-pipeline
git status --short
git branch --show-current
git remote -v
git switch -c codex/tokenizer-team-revision
```

`git switch -c` creates a branch at the current commit and keeps current edits. Do not first switch to an older branch or reset the working tree. If the proposed branch name already exists, choose a new unused name rather than deleting it. The expected origin is `https://github.com/tzuyu10/kapampangan-tokenizer-pipeline.git`.

## 2. Check the app

Use the environment already installed on this device:

```powershell
.\.venv-translation\Scripts\python.exe -m unittest discover -s webapp/backend -p "test_*.py" -v
Push-Location webapp/frontend/ui
npm.cmd run build
Pop-Location
```

If Windows test fixtures encounter temporary-directory permission errors, use a local ignored folder for the test session:

```powershell
New-Item -ItemType Directory -Force .cache/test-tmp | Out-Null
$env:TEMP = (Resolve-Path .cache/test-tmp).Path
$env:TMP = $env:TEMP
.\.venv-translation\Scripts\python.exe -m unittest discover -s webapp/backend -p "test_*.py" -v
```

## 3. Stage and review the whole intended source snapshot

```powershell
git add -A
git diff --cached --stat
git diff --cached --check
git diff --cached --name-status
git diff --cached --name-only -- nllb/checkpoints .venv .venv-translation .cache release-assets webapp/frontend/ui/node_modules webapp/frontend/ui/dist
```

The last command should produce no output. Review the complete staged list because this working tree contains changes from several earlier tasks. This is deliberately a full snapshot, including intended removals of obsolete checksum-listed files. Do not restore those obsolete files independently from their new inventories.

Check for oversized staged files without printing file contents:

```powershell
git diff --cached --name-only --diff-filter=ACM | ForEach-Object {
    if (Test-Path -LiteralPath $_ -PathType Leaf) {
        $candidateFile = Get-Item -LiteralPath $_
        if ($candidateFile.Length -ge 50MB) {
            [PSCustomObject]@{ Path = $_; MiB = [math]::Round($candidateFile.Length / 1MB, 2) }
        }
    }
}
```

Also review for private files and credentials. If something unintended was staged, `git restore --staged -- "path/to/file"` removes it from staging while retaining its local contents. Correct its ignore rule if necessary. Do not use `git add -f` to include environments or model files. The existing small `nllb/matched_colab/kapampangan_colab_inputs.zip` is a training-input archive, not a trained model; it was already tracked.

## 4. Commit and push

After the checks and staged review pass:

```powershell
git commit -m "feat(app): add tokenizer variants and team setup"
git push -u origin codex/tokenizer-team-revision
git status --short
git log -1 --oneline
git ls-remote --heads origin codex/tokenizer-team-revision
```

The commit shown locally and by `ls-remote` should match. Authenticate with your GitHub account if Git requests it. Give groupmates the branch name and [GROUPMATE_SETUP.md](GROUPMATE_SETUP.md). No merge into the older branches is required to test this new branch.

## 5. Share the trained bundles separately

Prepared local files are in `release-assets/team-models-20261017-all6/`. That directory is ignored by Git. Share its ZIPs plus `share-manifest.json` and `SHA256SUMS.txt` through your team's private file sharing, or upload trusted release assets yourself.

| Archive | Purpose |
| --- | --- |
| `plain_bpe_inference.zip` | Current 30-epoch Plain BPE translation model |
| `morph_bpe_inference.zip` | Current 30-epoch weighted penalty32 translation model |
| `morph_bpe_infix_first_penalty48_inference.zip` | Additional trained 30-epoch infix48 translation model |
| `plain_bpe_15_inference.zip` | Optional historical Plain15 |
| `morph_bpe_15_inference.zip` | Optional historical Morph15 |
| `morph_bpe_hard30_backup_20261008_inference.zip` | Optional historical hard-constrained Morph30 |

All six were exported and checked for a matching local selection menu. The first three cover the current principal translation choices. Each ZIP keeps its own source weights, source tokenizer, runtime/helper, native target tokenizer, manifest and provenance. ZIPs omit `last.pt` and caches; they cannot resume training. Keep your original full backups separately. The frozen NLLB base is downloaded on each device's first translation, unless already cached.

For a later export, use a new output folder:

```powershell
.\.venv-translation\Scripts\python.exe .\webapp\export-model-bundles.py --output .\release-assets\team-models-next
```

By default the exporter selects the first three bundles. Add `--bundles` followed by exact installed folder names to choose others. Existing output folders are refused, and installed bundles are not changed. Archive hashes change if ZIP metadata changes on a future export, so distribute the matching newly generated checksum files.

**Tokenizer-only and translation versions are independent.** The new Kapampangan + Tagalog infix/affix-priority 6k and 8k options are for the Tokenization tabs. They have no newly trained translation embeddings. Do not replace a trained bundle's tokenizer with one of those exports.
