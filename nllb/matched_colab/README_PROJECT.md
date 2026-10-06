# Fixed Colab integration for your Kapampangan tokenizer pipeline

Use `NLLB_600M_Kapampangan_Training.ipynb` with `kapampangan_colab_inputs.zip`.
This is the updated workflow for your actual project artifacts. It supersedes the
earlier generic Hugging Face tokenizer-export instructions. No tokenizer retraining,
ID edits inside artifacts, new `<kap>` entry, or Rust build is needed in Colab.

## Run in Colab

1. In Google Drive create `MyDrive/kapampangan_nllb/`.
2. Upload `kapampangan_colab_inputs.zip` there, without extracting or renaming it.
   It contains your existing silver translation bundle, both matched tokenizers,
   their checksum files, and the standalone Python runtime. Nothing is uploaded
   automatically by this package.
3. Upload `NLLB_600M_Kapampangan_Training.ipynb` to Colab and select a GPU runtime.
4. Run the installation cell first. Restart if you already imported the affected
   packages, then continue from section 2. Mount Drive when prompted.
5. For the baseline, keep `CONDITION='plain_bpe'`. Run sections 2–8 in order.
6. Start a fresh GPU runtime for the proposed run. Set `CONDITION='morph_bpe'`;
   otherwise use the identical configuration. Run sections 2–8 again.
7. Once the experiment settings are frozen, set `RUN_TEST=True` and run section 9
   with the trained model loaded. It writes separate `test_bible` and `test_ood` results.
8. Section 10 demonstrates reloading the saved adapter and translating raw text.

The notebook defaults to seed 42, 10 epochs, learning rate 0.0003, batch size 1,
gradient accumulation 8, and four-beam generation. The batch size is conservative;
hardware fit must be checked on your actual GPU. It does not promise a particular
training time. Source/target limits are 256/128 tokens, with no silent truncation;
generation is capped at 160 new tokens. These cover the verified current maxima of
184 source tokens and 117 target tokens. Hold generation settings equal across runs.

## Fixes applied

| Previous issue | Resolution |
|---|---|
| `bpe6080` silently fell through to native NLLB tokenization. | Closed routing maps plain BPE to `bpe_ids`, MorphBPE to `morphbpe_ids`, and rejects unrecognized conditions. The runtime must reproduce those IDs for every bundled record. |
| Project `tokenizer.json` is not a Hugging Face Tokenizers JSON. | Load the existing project runtime and complete artifact directory, checking its manifest and checksum inventory. |
| Project PAD=0 and UNK=1 conflict with native encoder position indexing. | At the model boundary only, permute IDs 0 and 1. Source PAD becomes 1 and UNK becomes 0. Source BOS=2, EOS=3, all other IDs, and vocabulary size stay unchanged. Save and reapply the same mapping at inference. |
| Ordinary `nn.Embedding` could drop the pretrained embedding class's scaling behavior. | Preserve the actual NLLB embedding class and scaling while replacing its weight storage. Frozen decoder/output weights and positional embedding behavior are retained. |
| Different initialization recipes and variant names caused ambiguity. | Default both matched conditions to the same warm-start method; select only plain BPE and hard-constrained MorphBPE from the same expanded-v4 family. |
| Previous Phase 5 only skipped completed runs and saved scores. | Save epoch optimizer/scaler checkpoints, the best source table, complete tokenizer/runtime bundle, per-sentence outputs, and reproducibility metadata. |

The two verified tokenizer fingerprints are:

- Plain BPE: `005f6da948e787876732424df6f25efd6086e0a6d693918892683c346b57f478`
- MorphBPE: `5c34233ebd33939aad1c6af9ccfb041855ccfa84a98b9894a24a4ed54c24803d`

Both have 6,080 total entries, including four special tokens. They share the
prepared-corpus fingerprint and normalization/pre-tokenizer files. This uses the
matched expanded-v4 artifacts, not the older canonical `artifacts/selected-tokenizer`
or the penalty-8/weighted variants. The source IDs in the existing bundle were
generated from exactly these two artifacts.

## Initialization and thesis wording

The default is `INITIALIZATION='warm_start'`: each new source row starts from the
mean of the native NLLB embeddings for that token's native subtokenization. Special
rows are mapped explicitly; the source padding row is zero. Only the independent
source table is then trained. The pretrained encoder layers, decoder, shared target
embedding, and output projection remain frozen.

This is the common recipe already used by your repository, not evidence that
warm start has been proven superior. It is **not random initialization**. Document
it consistently in the thesis and apply it to both conditions. The revised SOP's
"freshly-trained embedding" wording does not itself specify an initialization method.
If random initialization is required by your approved protocol, set
`INITIALIZATION='random'` for both conditions and use new run names. Do not combine
random results for one tokenizer with warm-start results for the other.

Suggested methods wording:

> Both conditions use independent 6,080-entry source embedding tables with the same
> pretrained-subtoken initialization procedure. The remaining pretrained NLLB-200
> Distilled 600M parameters are frozen. The conditions differ in source tokenizer:
> plain BPE versus morphology-aware BPE. Corpus partitions, adaptation settings,
> checkpoint selection, and decoding are matched. A reversible source-ID permutation
> reconciles the tokenizer's padding ID with the model's positional indexing without
> changing token segmentation or target-side tokenization.

The supplied notebook does not run Unigram or penalty-8 translation experiments.
Unigram is the revised SOP's intrinsic-tokenizer control. Additional variants should
be separately named and reported. Native NLLB zero-shot is not evaluated here.

## Outputs and resuming

Outputs go to `MyDrive/kapampangan_nllb/runs/<condition>/<run_name>/`:

- `best_source.safetensors`: best source embedding selected by validation loss.
- `last.pt`: source weights, optimizer/scaler state, and next epoch.
- `manifest.json`, `history.json`, environment, split IDs, and tokenization/data audits.
- `source_artifact/`, `runtime/`, `target_tokenizer/`, and the helper module for inference.
- `validation/metrics.json` and sentence-level predictions.
- `test_bible/` and `test_ood/` metrics/predictions when test evaluation is enabled.

BLEU and chrF++ are corpus scores on decoded Filipino text. Metric signatures and
ordered hypotheses/references are saved. Statistical significance is not calculated.

To resume, use exactly the same configuration and paths with `RESUME=True`. An
interrupted epoch restarts from the last completed epoch. Changed initialization,
data, code, tokenizer, or hyperparameters require a new run name. Historical
`phase5-results.json` scores and checkpoints are not reused by the corrected workflow.

The export is an adapter bundle, not a standalone full NLLB checkpoint. Use
`load_bundle` from the saved helper. It restores the pinned base, exact tokenizer
runtime, ID mapping, and learned table. Do not call global embedding resizing or
`tie_weights()` on the modified model.

## Data audit and limitations that software cannot resolve

The existing bundle has 3,590 train, 238 dev, 329 in-domain Bible test, and 70
out-of-domain test records. All bundle hashes and row counts are verified. There
are no repeated normalized/case-folded source sentences across those four splits.
There are 22 repeated normalized sources **within training**. The original split
manifest also flags 24 partially aligned training rows. Neither is silently removed.

These facts do not establish absence of semantic/document leakage. The original
split manifest documents chapter/story partitions, but the JSONL bundle lacks
per-row document IDs. The original tokenizer corpus and prepared training streams
are absent from their recorded paths, so overlap between **tokenizer training** and
**translation test text** cannot yet be conclusively checked. Restore those sources
and audit them before interpreting the scores as a clean held-out hypothesis test.
If contamination is found, make new leakage-controlled partitions and retrain both
tokenizers identically; never change only one condition or fabricate a clean audit.

The repository labels the translation data as silver and records source/translation
validation limitations. These integration fixes do not convert it into human-validated
gold data. Tokenizer quality and translation quality remain empirical questions.

## Rebuilding and testing

From the package source folder:

```text
python build_project_notebook.py PATH_TO_KAPAMPANGAN_PIPELINE_REPOSITORY
python test_adapter.py
python test_project_integration.py
```

The builder copies the exact required artifacts and data into `project_inputs/`,
creates the checksummed input ZIP, and regenerates the notebook. No corpus or tokenizer
artifact in the source repository is edited. `build_notebook.py` is an internal
generic scaffold; use **build_project_notebook.py last** for the final notebook.

Tests use the real tokenizer artifacts and a tiny actual M2M100 model. Full 600M
GPU training is not part of the local software validation.
