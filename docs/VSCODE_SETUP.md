# Running the project in Visual Studio Code — step by step

Written for Windows (the proposal's ASUS TUF A15). macOS/Linux differences are
noted inline. Follow in order; each step says how to tell it worked.

---

## Step 0 — Install the prerequisites

| Tool | Version | Where |
|---|---|---|
| Python | **3.11** (3.10–3.12 fine; avoid 3.13) | python.org — tick **"Add python.exe to PATH"** |
| Visual Studio Code | latest | code.visualstudio.com |
| Git | latest | git-scm.com |
| NVIDIA driver | supports CUDA 12.1+ | GeForce Experience / nvidia.com |

Check in a **new** terminal:

```powershell
python --version      # Python 3.11.x
git --version
nvidia-smi            # should list your RTX 4050 and a CUDA version
```

If `python` opens the Microsoft Store, disable the aliases:
Settings → Apps → Advanced app settings → App execution aliases → turn off
`python.exe` and `python3.exe`.

---

## Step 1 — Open the project

```powershell
cd C:\Users\<you>\Documents
git clone <your-repo-url> kapampangan-morphbpe   # or unzip the folder here
cd kapampangan-morphbpe
code .
```

VS Code will offer to install the recommended extensions
(`.vscode/extensions.json`) — accept. You want at minimum:

- **Python** (ms-python.python)
- **Pylance**
- **Python Debugger** (debugpy)
- **Ruff** — linting
- **Rainbow CSV** — makes the lexicon TSVs readable
- **YAML** — for `config/pipeline.yaml`

---

## Step 2 — Create the virtual environment

In the VS Code terminal (`` Ctrl+` ``):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux: `source .venv/bin/activate`

If PowerShell blocks the script:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Your prompt should now start with `(.venv)`.

Then tell VS Code to use it: `Ctrl+Shift+P` → **Python: Select Interpreter** →
pick the one ending in `.venv\Scripts\python.exe`. Bottom-right of the status
bar should show `.venv`.

---

## Step 3 — Install dependencies

**PyTorch first, on its own**, because the CUDA build does not come from PyPI:

```powershell
python -m pip install --upgrade pip

# NVIDIA GPU (RTX 4050, CUDA 12.x):
pip install torch --index-url https://download.pytorch.org/whl/cu121

# No GPU:
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Then everything else:

```powershell
pip install -r requirements-dev.txt
```

`requirements-dev.txt` includes `requirements.txt`, so this installs both the
pipeline and the test/lint tools.

Verify:

```powershell
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# expect e.g.  2.5.1+cu121 True
python -c "import transformers, sacrebleu, scipy, numpy; print('deps ok')"
```

`torch.cuda.is_available()` printing `False` on a machine with an NVIDIA GPU
almost always means you installed the CPU wheel. Uninstall and redo:
`pip uninstall torch -y` then reinstall with the `cu121` index URL.

### The full dependency list

**Core** (`requirements.txt`)

```
torch          >=2.2      installed separately, see above
numpy          >=1.26,<3  arrays, MCF1 incidence matrices
pandas         >=2.1      corpus inspection
PyYAML         >=6.0      config/pipeline.yaml
regex          >=2023.12  Unicode-aware pre-tokenisation
tqdm           >=4.66     progress bars
scipy          >=1.11     paired t-test, Wilcoxon, Shapiro-Wilk
sacrebleu      >=2.4.0    BLEU (eq. 8) and chrF++ (eq. 9)
transformers   >=4.41,<5  NLLB-200 loading and generation
sentencepiece  >=0.2.0    required by NllbTokenizer
tokenizers     >=0.19     transformers backend
safetensors    >=0.4      model weights format
accelerate     >=0.30     device placement
huggingface-hub>=0.23     model download
datasets       >=2.19     optional
matplotlib     >=3.8      plots for Chapter 4
```

**Dev** (`requirements-dev.txt`): `pytest`, `pytest-cov`, `ruff`, `mypy`,
`ipykernel`, `jupyter`.

**Web scraping only** (`requirements-scraping.txt`): `requests`,
`beautifulsoup4`, `lxml`, `trafilatura`, `langdetect`. Install only if you are
collecting the news-domain samples.

---

## Step 4 — Prove the install works

```powershell
python -m pytest tests -q
```

Expect `27 passed`. If you get `ModuleNotFoundError: kapampangan_mt`, the
`PYTHONPATH` is not set — `.vscode/settings.json` sets it for VS Code terminals,
so open a **new** terminal, or run `$env:PYTHONPATH="src"` once.

---

## Step 5 — Smoke-test the whole pipeline on synthetic data

This proves the code runs before you have real data. Roughly 60 seconds.

```powershell
python scripts/make_toy_data.py --n 600
python scripts/00_prepare_data.py
python scripts/01_validate_lexicon.py
python scripts/02_build_gold_template.py --n 200
Copy-Item data/gold/morpheme_gold.TEMPLATE.tsv data/gold/morpheme_gold.tsv
python scripts/03_train_tokenizer.py
python scripts/03_train_tokenizer.py --plain-bpe
python scripts/04_eval_tokenizer.py --allow-auto-gold --no-nllb
python scripts/07_report.py
```

macOS/Linux: replace `Copy-Item` with `cp`.

You should see, from stage 03:

```
sample: ['▁k', 'in', 'an', '▁ne', '▁ing', '▁pamangan', '▁king', '▁bale', '.']
```

`kinan` split as `k | in | an` — root, infix, root. Plain BPE leaves it as one
blob. That contrast is the thesis in one line.

Or use the VS Code task: `Ctrl+Shift+P` → **Tasks: Run Task** →
**Full tokenizer pipeline (toy data)**.

> **Delete `data/raw/parallel.tsv` and `data/gold/morpheme_gold.tsv` before doing
> real work.** They are synthetic. Nothing produced from them may go in Chapter 4.

---

## Step 6 — Switch to real data

1. Put your real corpus at `data/raw/parallel.tsv` (see
   [DATA_REQUIREMENTS.md](DATA_REQUIREMENTS.md)).
2. Replace `data/lexicon/*.tsv` with your validated lexicon.
3. Re-run stages 00 and 01. Read the coverage number from stage 01 — if it is
   under ~70%, add roots before going further.
4. Regenerate the gold template (stage 02), have **two people** annotate it,
   report Cohen's kappa, save as `morpheme_gold.tsv` with `provenance=human`.
5. Re-run stages 03 and 04 **without** `--allow-auto-gold` and **without**
   `--no-nllb`. The first NLLB run downloads ~2.5 GB.

---

## Step 7 — The translation experiments

```powershell
python scripts/05_train_nmt.py --arm baseline
python scripts/05_train_nmt.py --arm adapted
python scripts/05_train_nmt.py --arm control

python scripts/06_translate_eval.py --arms baseline adapted control
python scripts/07_report.py
```

Watch VRAM with `nvidia-smi` in a second terminal. On out-of-memory:

```powershell
python scripts/05_train_nmt.py --arm adapted --set train.batch_size=4 train.grad_accum=8
```

Effective batch stays 32, so the arms remain comparable.

Final tables land in `artifacts/results/REPORT.md`, formatted as Tables 2–5 of
Chapter 4.

---

## Debugging inside VS Code

`.vscode/launch.json` has one entry per stage. Press `F5`, pick a configuration
from the dropdown, set breakpoints by clicking left of a line number. Useful
places to break:

| Want to understand | Break at |
|---|---|
| why a word is not analysed | `segmenter.py` → `_segment`, first line |
| what pairs Morph-BPE is merging | `morph_bpe.py` → inside the `while` loop |
| why fertility looks wrong | `tokenizer.py` → `_base_symbols` |
| how the graft changes the model | `nllb/graft.py` → after `model.model.encoder.embed_tokens = new_emb` |

---

## Changing settings without editing files

Every script accepts `--set key=value` using dotted paths from
`config/pipeline.yaml`:

```powershell
python scripts/03_train_tokenizer.py --set tokenizer.candidates="[4000,8000,16000]"
python scripts/03_train_tokenizer.py --set segmenter.strict_thesis_mode=True
python scripts/05_train_nmt.py --arm adapted --set train.epochs=20 nllb.init=random
```

`segmenter.strict_thesis_mode=True` runs the literal Figure 7 pseudocode with no
repairs — useful for an ablation paragraph showing what each repair buys.

---

## Common problems

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: kapampangan_mt` | `PYTHONPATH` not set | open a new VS Code terminal, or `$env:PYTHONPATH="src"` |
| `torch.cuda.is_available()` is `False` | CPU wheel installed | reinstall torch with the `cu121` index URL |
| `ValueError: … rows are tagged provenance=auto` | using machine-generated gold data | annotate it properly, or pass `--allow-auto-gold` for smoke tests only |
| `vocab_size … is too small` | vocabulary smaller than specials + bytes + alphabet | raise `tokenizer.candidates` |
| Fertility around 5.0, tokens look like `<0xE2>` | word-start marker mismatch | you are on an old build — `_base_symbols` must fuse `▁` with the first character |
| CUDA out of memory | batch too large for 6 GB | `--set train.batch_size=4 train.grad_accum=8` |
| Very slow first NLLB run | 2.5 GB model download | one-off; then set `HF_HUB_OFFLINE=1` |
| `charmap` / `UnicodeDecodeError` on Windows | non-UTF-8 default encoding | `$env:PYTHONUTF8="1"`, and save all TSVs as UTF-8 |

---

## Quick reference

| Stage | Command | Needs GPU |
|---|---|---|
| toy data | `python scripts/make_toy_data.py` | no |
| 00 prepare | `python scripts/00_prepare_data.py` | no |
| 01 lexicon | `python scripts/01_validate_lexicon.py` | no |
| 02 gold template | `python scripts/02_build_gold_template.py --n 1500` | no |
| 03 tokenizer | `python scripts/03_train_tokenizer.py [--plain-bpe]` | no |
| 04 tokenizer eval | `python scripts/04_eval_tokenizer.py` | no |
| 05 NMT train | `python scripts/05_train_nmt.py --arm {baseline,adapted,control}` | **yes** |
| 06 decode + eval | `python scripts/06_translate_eval.py --arms …` | **yes** |
| 07 report | `python scripts/07_report.py` | no |
