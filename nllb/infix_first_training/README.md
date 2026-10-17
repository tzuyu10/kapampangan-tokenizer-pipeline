# Infix-first penalty48 and penalty16 training on Kaggle

These notebooks train two new source embedding tables for the already trained
infix-first tokenizers. They use the same translation data, NLLB base revision
and training settings as the installed weighted penalty32 model.

No penalty16 or penalty48 translation weights have been trained by preparing
these files. The tokenizer results are separate from translation quality.
Training and optional translation evaluation happen when you run the notebooks
on Kaggle.

## 1. Choose the matching notebook and input package

Extract `release-assets/infix_first_training/ALL_FILES.zip` on your computer.
Use one row below for each separate Kaggle notebook.

| Condition | Notebook | Private training input |
|---|---|---|
| Infix-first penalty48 | `NLLB_600M_InfixFirst_Penalty48_Source_Embedding_Training.ipynb` | `infix_first_penalty48_training_inputs.zip` |
| Infix-first penalty16 | `NLLB_600M_InfixFirst_Penalty16_Source_Embedding_Training.ipynb` | `infix_first_penalty16_training_inputs.zip` |

The training input contains the checksum-verified translation CSV, exact
candidate source tokenizer, tokenizer runtime, training and data helpers,
native Filipino target tokenizer, and recorded baseline provenance. It contains
no trained candidate source weights or optimizer checkpoint. The notebooks
download the pinned NLLB base separately.

`current_weighted32_reference.zip` is optional. It contains the installed
weighted penalty32 inference bundle for a fresh comparison in the same Kaggle
environment. It contains its selected source weights, tokenizer and helper,
but no optimizer checkpoint or complete NLLB base model.

Keep `ALL_FILES.zip` as the local delivery archive. Upload the selected training
input ZIP to Kaggle, rather than uploading the complete delivery archive.

## 2. Add private Kaggle inputs

1. Create a Kaggle dataset and upload the training input ZIP for the condition
   you will run. Keep the dataset private because it includes the project data.
2. If you want a fresh current32 comparison, also upload
   `current_weighted32_reference.zip`. It can be in the same private dataset or
   a separate attached dataset.
3. Import the matching `.ipynb` file as a Kaggle notebook.
4. Attach the private dataset to that notebook using Kaggle's input controls.

Kaggle may expose the ZIP itself or unpack it into folders. Both forms are
supported. Input discovery checks the package identity and hashes, so the
penalty48 notebook accepts the penalty48 package and the penalty16 notebook
accepts the penalty16 package. If both training packages are attached, each
notebook should select its matching package.

If discovery reports multiple matching copies, set `INPUT_PATH` to the exact
ZIP path or extracted package root shown under `/kaggle/input`. For an extracted
package, use the folder that directly contains `package_manifest.json`.
Do not point it only at `source_artifact/`.

For Kaggle's account and interface instructions, see the official
[notebooks documentation](https://www.kaggle.com/docs/notebooks) and
[datasets documentation](https://www.kaggle.com/docs/datasets).

## 3. Select GPU and Internet

Select a GPU accelerator in the notebook settings and enable Internet before
running the dependency and model-loading cells. Internet supplies the pinned
Python dependencies and the pinned NLLB base if it is not cached.

The notebook uses one CUDA device. If Kaggle provides two T4 GPUs, this code
still uses one GPU. GPU availability and session limits follow your Kaggle
account; these new runs have no measured training-time estimate.

Run the dependency cell before importing the model libraries. It installs the
recorded package versions and removes conflicting optional packages. If the
notebook asks for a session restart because another Transformers version is
already imported, restart and run the cells from the beginning.

## 4. Keep the first-run settings

The configuration cell starts with:

```python
INPUT_PATH = ''
DATA_CSV = ''
RESUME = False
RESUME_BUNDLE = ''
RUN_VALIDATION_TRANSLATIONS = False
RUN_TEST = False
RUN_CURRENT32_REFERENCE = False
CURRENT32_REFERENCE_PATH = ''
```

Leave the input paths blank for automatic discovery. `DATA_CSV` uses the CSV in
the input package. An override must match the recorded CSV bytes and ordered
splits; this is not a place to substitute another dataset.

Keep the notebook's condition-specific run name:

```text
penalty48: infix_first_penalty48_warm_start_seed42_v1
penalty16: infix_first_penalty16_warm_start_seed42_v1
```

Each run uses a separate output directory. A nonempty existing run requires an
explicit matching resume, or a new run name.

The matched settings are seed 42, learning rate 0.0003, batch size 1, gradient
accumulation 8, warm initialization, maximum 30 epochs, early-stopping patience 3
and minimum improvement 0.001. Source and target limits remain 256 and 128.
Actual completed epochs and the selected checkpoint are recorded from the
training history; an early stop can finish before 30 epochs.

Only the independent 6,080 x 1,024 source embedding table trains. The encoder
layers, decoder, native target embeddings and output projection remain frozen.
Warm initialization uses the native target embedding vectors for each new
source token. The notebook does not retrain the tokenizer or reuse current32's
trained source table.

## 5. Run the cells in order

Run the cells from the beginning using one of these execution modes.

For a background run, use **Save Version > Save & Run All** with the inputs
already attached and GPU/Internet enabled. This executes the notebook from the
beginning and saves the resulting version's outputs. Start this way for a new
run, rather than first completing the same training interactively. If the run's
output folder already exists, use the matching resume settings in section 7.
Kaggle describes version execution in its
[notebooks documentation](https://www.kaggle.com/docs/notebooks).

For interactive training, enable **Files only** persistence before stopping the
session if that option is available. This covers `/kaggle/working`, where the
notebook stores checkpoints. File persistence is best-effort; also download a
full backup before ending the session. See Kaggle's
[session persistence announcement](https://www.kaggle.com/discussions/product-feedback/355440).

The cells perform these steps:

1. Verify the package, exact candidate tokenizer and recorded data provenance.
2. Load the original ordered train/validation/test partitions and preserve
   the recorded duplicate policy.
3. Encode the data with the candidate source tokenizer and unchanged native
   target tokenizer. Sources exceeding the shared length limit fail rather
   than being silently truncated.
4. Load the pinned `facebook/nllb-200-distilled-600M` revision and install a new
   source embedding table. A preflight check confirms that only this table
   receives gradients.
5. Train, save a checkpoint after each completed epoch, and select the lowest
   validation-loss source weights.
6. Release the first model and reload the saved bundle. It verifies weights,
   source IDs and separate source/target embedding storage, then generates one
   validation example.
7. Export the full backup and, after a passing reload check, the inference ZIP.

Keep the source ID mapping in the supplied helper. Native source PAD 0 and UNK 1
map to model PAD 1 and UNK 0; source BOS 2 and EOS 3 remain 2 and 3. Passing the
custom `tokenizer.json` to a generic Hugging Face tokenizer loader, changing
token IDs, or swapping penalty16/48 artifacts into existing weights breaks the bundle.

The tokenizer's penalty is already reflected in its learned merge rules.
It is not a new penalty added to the NLLB translation loss.

## 6. Save the full backup and inference ZIP

The export cell displays download links for the generated files. Download the
full backup before ending a Kaggle session, including when you intend to run
another condition later.

For a completed saved version, open its **Output** files and download the ZIPs
and checksum file from the condition's training folder. If the inline download
links are unavailable, use the output file browser. The export cell prints the
exact paths.

| Export | Purpose |
|---|---|
| `RUN_NAME_full.zip` | Resume training. Includes the epoch-boundary optimizer checkpoint, selected source weights, history, identity and supporting files. |
| `RUN_NAME_inference.zip` | Reload or later deploy the selected trained model. Excludes the optimizer checkpoint. |
| `RUN_NAME_SHA256SUMS.txt` | Verify the generated archive bytes. |

These bundles contain the source adaptation and references to the pinned base;
they are not standalone copies of all NLLB model weights.

If training stops after at least one completed epoch, run the export cell to
save the full backup. An unfinished run does not produce an installable
inference export. Changes within an interrupted epoch are not a resume point;
the next session resumes from the last saved completed epoch.

Preparing or downloading these files does not install them in the local app.
Preserve the current32 model when evaluating the new conditions.

## 7. Resume the same condition

For the same retained Kaggle working directory, set `RESUME=True` and rerun the
notebook with the same run name, inputs and configuration.

For a new Kaggle session:

1. Attach the matching training input again.
2. Upload the saved `RUN_NAME_full.zip` as a private input.
3. Set `RESUME_BUNDLE` to that ZIP or to its extracted root containing
   `manifest.json` and `last.pt`.
4. Keep the same run name and set `RESUME=True`.
5. Run the cells from the beginning.

Resume requires matching configuration, tokenizer, base, dataset and helper
identity, plus `last.pt` and the saved best source weights. A penalty16 backup
cannot resume penalty48, and the current32 inference reference cannot resume
either candidate. Use a fresh run for a different condition.

## 8. Optional validation translation comparison

After training and the bundle reload check pass, enable validation generation:

```python
RUN_VALIDATION_TRANSLATIONS = True
RUN_TEST = False
RUN_CURRENT32_REFERENCE = True
CURRENT32_REFERENCE_PATH = ''
```

Attach `current_weighted32_reference.zip` if you enable its switch. Discovery
accepts the ZIP or its extracted root. If multiple copies are found, set
`CURRENT32_REFERENCE_PATH` explicitly.

In the same live session, rerun the configuration cell so the switches take
effect, rerun section 8.1 to reload the candidate bundle, then run the candidate
evaluation and current32 comparison cells. The comparison releases the candidate
model before loading current32, so section 8.1 is required again before another
candidate evaluation. If starting a new session,
restore the matching full backup as described above and run the notebook in
order with the evaluation switches enabled.

Candidate metrics and predictions are saved under `OUT/evaluation/validation`.
Current32 reference metrics are saved under
`WORK/reference_evaluation/weighted_penalty32/validation`.

Both use the same ordered CSV rows and raw Filipino references, FP32 generation,
four beams, at most 160 new tokens, forced `tgl_Latn`, and no sampling. Metrics
are corpus BLEU with tokenizer `13a` and chrF++ with `word_order=2`; saved
signatures and evaluation identities document the protocol. When the reference
is enabled, `OUT/evaluation/validation_vs_current32.csv` records both conditions'
scores and the candidate minus current32 differences.

Compare penalty48, penalty16 and current32 on the same split and settings.
The supplied helper's convenience `predict` function uses mixed precision;
the notebook's scored comparison uses FP32. Existing scores are comparable
only when rows, references, selected weights, decoding settings and metric
signatures match. Regenerating current32 here matches the evaluation environment.

Validation loss selects the training checkpoint. Translation metrics answer
whether that checkpoint generates better translations; tokenizer boundary F1
alone does not establish that result.

## 9. Optional final test evaluation

Leave `RUN_TEST=False` while changing experimental settings. Once the comparison
protocol is frozen, set:

```python
RUN_TEST = True
RUN_CURRENT32_REFERENCE = True
```

Keep the validation switch on or off according to which splits you intend to
score. After changing the switches, rerun section 8.1 and both evaluation cells.
Candidate test results are under `OUT/evaluation/test`; current32 results are
under `WORK/reference_evaluation/weighted_penalty32/test`. With the reference
enabled, `OUT/evaluation/test_vs_current32.csv` contains the matched score
comparison.

Run the export cell again after scoring to include the saved evaluation files
in newly downloaded backups. Reference scores are copied into
`OUT/evaluation/current_weighted32_reference`; the current32 weights stay in the
separate reference input.

The CSV and ordered split IDs are checked against the installed training
baseline. Original tokenizer-corpus overlap with translation test text remains
unverified. This package does not claim a new independent gold benchmark or a
translation improvement before the cloud runs and matched evaluation finish.
