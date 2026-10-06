# Paired translation evaluation on Kaggle

## Required files

- `NLLB_600M_Kaggle_Paired_Evaluation.ipynb`
- `plain_bpe_kpm_tgl_cleaned_earlystop_seed42_v2_backup.zip`
- `morph_bpe_kpm_tgl_cleaned_15epochs_seed42_v1_backup.zip`
- `kpm_tgl_cleaned.csv`

No tokenizer input ZIP is needed: both trained bundles contain their exact tokenizers. Preserve all files within each bundle.

## Run

1. Create a Kaggle notebook and import the evaluation notebook.
2. Upload each model ZIP as its own private Kaggle dataset, then attach both datasets through Add Input. Keep their extracted files separate if Kaggle expands the ZIPs. Attach the CSV too. Do not merge the contents of the two model archives into a single directory.
3. Enable GPU and Internet in Session options. This notebook uses one GPU.
4. Run the installation cell once, restart the session, then continue from section 2.
5. Leave `SPLIT = 'test'` for final thesis evaluation. To evaluate validation instead, set `SPLIT = 'validation'` and use a fresh output directory/session. Do not use test scores to tune settings.
6. Run sections 2 through 5 in order. Both trained models are loaded and evaluated sequentially on the same rows. No training occurs. The first model load downloads the pinned NLLB base weights, reused by the second.
7. Run section 6 and download `/kaggle/working/paired_evaluation_backup.zip` from Output.

## Output

`comparison.csv` compares corpus BLEU (13a) and chrF++ scores. Each condition folder contains `metrics.json` with metric signatures, aligned `predictions.jsonl`, `hypotheses.txt`, `references.txt`, and `evaluation_identity.json`. These are translation metrics, not morphological boundary F1 or hypothesis-significance tests. Saved training validation loss is shown for context; evaluation does not recompute cross-entropy.

## Resume before the runtime limit

Interrupt evaluation, then run section 6 to archive all completed predictions. Download that ZIP before ending the session. In a new notebook session, attach it alongside the original inputs, run setup, then sections 2 onward. Section 4 restores it. Identity checks reject changed model weights, dataset, split, decoder settings, helper, or software versions. Partial progress in working storage is not permanent unless saved/downloaded. An incomplete final JSONL line is discarded on resume.

## Comparison constraints

These bundles both completed 15 epochs and selected epoch 15 by lowest validation loss. Plain BPE was configured for maximum 30 epochs; Morph-BPE for 15, with patience 3 still present in its saved configuration. Both histories kept improving and did not stop early. Report the actual procedure, rather than claiming identical configured stopping limits. The notebook checks matching learning rate, seed, batch settings, initialization, data, base revision and target tokenizer. The unresolved tokenizer-training-corpus overlap audit still applies. No quality results are invented.

## Frontend after installation

From the pipeline root in VS Code PowerShell, stop the old backend and run:

```powershell
.\webapp\start-translation-backend.cmd
```

In a second terminal:

```powershell
Set-Location .\webapp\frontend\ui
npm.cmd run dev
```

On Translator select Plain BPE or Morph-BPE. Translate calls the selected trained bundle; Show tokens uses its exact native tokenizer without loading NLLB. Translator A/B generates both outputs. The older Tokenizer tab is explicitly labeled as the penalty-32 training visualization, not the translation artifact. First translation requires the base model download. Local frontend compilation and both tokenizers have been checked; full local generation and Kaggle execution still require runtime validation.
