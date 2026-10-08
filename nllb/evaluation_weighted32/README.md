# Evaluate the current weighted penalty32 model

Use `notebooks/NLLB_600M_Kaggle_BLEU_CHRF_30Epochs_Weighted32.ipynb` with `release-assets/evaluation_weighted32/kaggle_bleu_chrf_inputs_30epochs_weighted32.zip`.

The 55-file package contains current Plain BPE and weighted penalty32 Morph-BPE inference bundles, their exact tokenizers/runtimes/helpers, training histories and split manifests, and the matching `kpm_tgl_cleaned.csv`. Both completed and selected epoch 30. The Morph source artifact matches all nine files of the UI penalty32 tokenizer byte-for-byte. Trained source tables remain 6,080 by 1,024. CSV SHA-256 is `69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b`.

The ZIP is 57,950,219 bytes with SHA-256 `c095abbcfb6464f9996b775550bd5a08766ae55713bd374aa6fab564c2854dff`. Its `_package_info.json` records each file checksum and the checkpoint identities. Source-weight hashes are Plain `7de78e7e02f01b481b3e94328218782610b283e6a701aa09246c2836601bda02`, weighted Morph `6d7721111fa35f7b11e97b5e832e32fa81f28f58d23fdfdfd60fbdcdf60f67fc`. It contains no old checkpoints, optimizer states or prior evaluation predictions. The frozen NLLB base is downloaded on the first Kaggle model load.

## Kaggle steps

1. Import the revised notebook into a new Kaggle notebook.
2. Upload the single input ZIP as a private dataset and attach it once. No extra model ZIP, tokenizer training package or CSV is required.
3. Enable a GPU accelerator and Internet.
4. Run section 1, restart the session, then run sections 2 onward in order. Keep `SPLIT='test'`, `MAX_EXAMPLES=None`, and `OUTPUT_NAME='bleu_chrf_weighted32_full_test'`.
5. On the first run, attach no evaluation progress backup. Section 5 prints an empty resume list and proceeds.
6. Run section 6 for full evaluation, section 6B for metric-variable tables, then section 7. Download `/kaggle/working/paired_evaluation_v2_backup.zip` into a new weighted32-results folder to distinguish it from the old report with the same name.

Output filenames and table formats match the previous evaluation: comparison CSV/JSON, paired prediction CSV, condition metrics/identities/predictions/hypotheses/references, training diagnostics, BLEU/chrF++ variable tables and n-gram counts. Identity and training diagnostics now explicitly identify weighted penalty32. Corpus settings remain case-sensitive BLEU-4 with 13a/exponential smoothing and chrF++ character6/word2/beta2; generation is FP32, 4 beams, maximum 160 new tokens. Both conditions evaluate the same 1,659 test rows. Numerical scores must be measured and can differ from the old hard-constrained results.

## Resume

Each completed prediction is flushed immediately; the progress archive refreshes every 100 predictions, at condition completion and on ordinary interruption. Before ending a session, interrupt section 6, run section 7 and save the latest backup. In the next session attach that backup alongside the same input ZIP and run setup plus sections 2 onward. Use only a backup from this revised notebook with these exact inputs. The previous hard-constrained backup is incompatible and deliberately rejected. Working storage alone is not a durable backup.

## Verification and notebook corrections

The original user-supplied notebook is preserved. Its cross-condition runtime-hash equality would reject the current weighted tokenizer's valid separate runtime. The revised copy removes that equality while preserving each runtime's individual checksum validation. It also reads the weighted flag from the trained manifest, corrects historical descriptions, and checks exact current checkpoint/tokenizer hashes, contiguous 30-epoch histories and matched data/settings. This prevents accidental reuse of the old Morph model.

Local checks passed notebook Python syntax, ZIP CRC and all 54 payload checksums, actual zipped/expanded input discovery and CPU validation of both finite embedding tables and all test IDs. Old checkpoint and old resume rejection checks passed. An independent audit reproduced the previous scores/signatures using the unchanged variable exporter, confirming output compatibility. No new NLLB generation, evaluation scores or training were performed locally. Kaggle execution remains to be run.

To rebuild against the same installed checkpoints after deliberately removing or renaming the existing generated ZIP, run from the repository root:

```powershell
.\.venv-translation\Scripts\python.exe -B .\nllb\evaluation_weighted32\build_inputs.py "C:\Users\Gabo\Downloads\kpm_tgl_cleaned.csv"
```

Generated private distribution files stay under ignored `release-assets/`; the builder refuses to overwrite an existing package.
