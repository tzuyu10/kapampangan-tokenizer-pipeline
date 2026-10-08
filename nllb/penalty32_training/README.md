# Penalty-32 source-embedding training on Kaggle

Use these two files:

- `notebooks/NLLB_600M_Penalty32_Source_Embedding_Training.ipynb`
- `nllb/penalty32_training/penalty32_training_inputs.zip`

The private input ZIP includes the verified `kpm_tgl_cleaned.csv`, exact
visualization penalty-32 tokenizer, its runtime, the unchanged installed
30-epoch training helper, native target tokenizer, and baseline provenance.
It contains no trained source embeddings or optimizer checkpoints. The CSV
matches the installed models' data hash and ordered splits.

Use the revised notebook and regenerated input ZIP together. The notebook checks
the package hashes, and the revised data-support checksum is part of the training
identity. The v2 workflow intentionally rejects resume checkpoints from the
earlier v1 package rather than mixing training identities.

1. Import the notebook into Kaggle.
2. Upload the input ZIP as a private Kaggle dataset and attach it to the notebook.
   Kaggle may unpack the ZIP automatically; the notebook accepts either form.
3. Select a GPU and enable Internet for installing the pinned dependencies and
   downloading the pinned NLLB base if not cached.
4. Run the cells in order. Input paths are discovered automatically. If more than
   one matching package is attached, set `INPUT_PATH` in section 2 explicitly.
5. Keep `RESUME=False` for the first run. Outputs go under
   `/kaggle/working/penalty32_training/runs/morph_bpe/penalty32_warm_start_seed42_v2/`.
6. Download/save the full backup before ending the session. Section 10 exports
   both the full resume ZIP and the installable inference ZIP after training.
   If training is interrupted after at least one saved epoch, run section 10 to
   export the full resume backup; inference export is skipped for an unfinished run.

Only the independent source embedding table trains. NLLB encoder layers,
decoder, target embeddings and output projection remain frozen. The tokenizer
is reused as already trained; penalty 32 is reflected in its learned merges.
The training budget is at most 30 epochs, with the same early stopping and
validation selection as the installed baseline. Actual completion and best
epoch are recorded from history.

The updated setup restores the supplied original notebook's GPU memory and
reproducibility controls: gradient checkpointing with `use_reentrant=False`,
disabled training cache, disabled cuDNN benchmarking and TF32, and deterministic
algorithms with warnings enabled. These controls do not make results identical
across different GPUs or PyTorch versions. The installation cell also retains
the original cleanup of conflicting optional packages before installing the
pinned training dependencies; run it before importing those packages and restart
the cloud session if needed.

This remains a fresh weighted penalty32 run. The supplied original notebook's
saved configuration specifies 15 epochs despite its 30-epoch prose, and its
saved execution stops at a Transformers-version assertion. The installed
manifests and histories establish the baseline's completed 30 epochs. The new
notebook uses their 30-epoch maximum rather than the original copy's stale value.

## Resume and evaluation

For the same retained output directory, set `RESUME=True` and run the notebook
with identical inputs/settings. For a new Kaggle session, upload the generated
penalty32 full backup, set `RESUME_BUNDLE` to its ZIP or extracted root, keep the
same run name, and set `RESUME=True`. Hard-constrained/Plain checkpoints are
rejected. Resume is at completed-epoch boundaries.

Validation translation and held-out test generation are optional and off by
default. Freeze experimental settings before enabling test evaluation. The
evaluation cell uses FP32, four beams, raw CSV reference strings, and identities
that protect progress resume. Compare against the existing Plain30 and
hard-constrained Morph30 on identical rows/settings, using FP32 generation for
every scored condition. The original notebook's convenience `predict` helper
uses mixed precision; do not mix those scores with the new FP32 evaluation and
attribute the difference only to tokenization. No quality gain or GPU training
completion is established by preparing this notebook.

The data reader now follows the supplied original notebook's CSV loading cell:
source and target strings remain unchanged, document groups are checked before
filtering, only training sources overlapping evaluation are excluded, and
within-split duplicate excess is reported afterward. Only comparison keys use
NFC, collapsed whitespace and case folding. The reader additionally requires
matching CSV bytes, counts, exclusions, duplicates and ordered baseline split
IDs. The current CSV has no source or target strings changed by normalization,
so this alignment preserves the already verified training text. Original
tokenizer-corpus overlap with translation test text remains unverified.

After completed training, run section 8.1 before optional evaluation or inference
export. It releases the first model, reloads the saved bundle with its helper,
checks the selected source weights, and translates a validation example.
Inference export requires a passing reload report matching the current bundle;
the full resume backup remains available after a completed epoch even when
training was interrupted. This verifies cloud bundle loading and inference when
executed; local preparation does not establish that this GPU check has passed.

The inference ZIP is compatible with `webapp/install-model-bundle.py` after
preserving/moving aside the current `morph_bpe` bundle. Restart the backend after
installation. App descriptions of the installed Morph-BPE variant also need to
identify weighted penalty32 at that time. This preparation does not modify or
install models into the application.

## Rebuild and verify locally

The builder reads the currently installed baseline and exact UI artifact, so it
refuses a different reference dataset or tokenizer fingerprint:

```powershell
.\.venv-translation\Scripts\python.exe -B .\nllb\penalty32_training\build_notebook.py --csv 'C:\Users\Gabo\Downloads\kpm_tgl_cleaned.csv'
.\.venv-translation\Scripts\python.exe -B -m unittest discover -s .\nllb\penalty32_training -p 'test_*.py' -v
```

Local checks cover data preparation, notebook code syntax, exact artifact
inventory and package hashes. They do not execute the full NLLB model or GPU
training. Keep the generated ZIP private: it contains the translation dataset
and native target tokenizer; no release is published by this workflow.
