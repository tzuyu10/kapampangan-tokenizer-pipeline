# Initial UI performance metrics

The Translation Metrics & Process tab shows installed-model training diagnostics and generation observations from the Translator A/B input. The Tokenization Comparison & Metrics tab shows initial tokenizer diagnostics and live comparison scores from the Tokenization input. Existing fertility charts remain available.

## Four-tab workflow

1. **Translator A/B:** enter Kapampangan text and generate both Plain BPE and Morph-BPE translations.
2. **Translation Metrics & Process:** inspect saved epoch/loss diagnostics, current input token counts/timing, and select either model's existing translation process. This tab uses the exact result from tab 1 and does not launch another translation.
3. **Tokenization:** enter text, inspect output pieces/IDs and the segmentation process.
4. **Tokenization Comparison & Metrics:** inspect the three-way splits, initial diagnostic metrics, colored fertility/F1 charts and calculation disclosures for the input from tab 3.

Switching tabs preserves inputs, results and in-progress requests during the current browser session. Editing or clearing translation input invalidates the previous result and process. Reloading the page starts a new session; inputs are not persisted to disk. Arrow keys, Home and End navigate the tab bar, which scrolls horizontally on small screens.

Restart the Python backend after updating the code, then refresh the frontend. The new endpoint is `GET /api/performance/initial`. No model loading, GPU or training is required to read these metrics.

## Tokenizer diagnostic

The server scores the exact deployed tokenizer artifacts against `reference_data.py`'s fixed `SENTENCES` and `FAMILIES`: 25 word occurrences, 21 unique words. It reuses the existing boundary/consistency scoring code. These are project demonstration references, not an independent held-out evaluation set, and must not be reported as final thesis evaluation results.

| Condition | Fertility | Boundary F1 | Consistency F1 |
| --- | ---: | ---: | ---: |
| MorphBPE penalty-32 | 1.920 | 0.889 | 0.870 |
| Plain BPE | 1.160 | 0.077 | 0.345 |
| Matched Unigram-LM | 1.240 | 0.357 | 0.400 |

Scores are computed at request time, not hardcoded. The source disclosure includes the actual tokenizer SHA-256 and reference splits. F1 ranges from 0 to 1. Fertility is pieces per word; fewer pieces alone do not establish better morphology or translation. The installed weighted penalty32 Morph-BPE translation model uses the same source tokenizer artifact as the Tokenization tab.

## Translation diagnostics

The server reads each installed bundle's `manifest.json` and `history.json`. It respects `KAPAMPANGAN_MODEL_DIR`. Missing or invalid histories display an unavailable message. Both losses come from the epoch with minimum saved validation loss, rather than mixing the best validation epoch with the final training epoch.

| Local condition | Completed epochs | Best validation epoch | Training loss | Validation loss |
| --- | ---: | ---: | ---: | ---: |
| Plain BPE | 30 | 30 | 1.371 | 1.233 |
| Weighted Morph-BPE, penalty32 | 30 | 30 | 1.395 | 1.238 |

Loss is not accuracy. Saved evaluation reports are read from `reports/translation/paired_evaluation_v2`. The endpoint verifies report checksums and matches actual installed weight, source tokenizer, runtime, helper and target tokenizer hashes, dataset identity, ordered test IDs and decoding settings before exposing scores. Model replacement cannot silently inherit previous scores. No NLLB loading or SacreBLEU installation is needed to serve the imported, verified reports.

The supplied `paired_evaluation_v2_backup.zip` contains complete predictions for 1,659 test rows. Both corpus scores were independently reproduced with SacreBLEU 2.5.1 and references matched the current CSV exactly. Plain BPE matches the active Plain30 checkpoint and displays **45.802 BLEU**, **65.397 chrF++**. The archive's Morph-BPE has **46.008 BLEU**, **65.314 chrF++**, but its identities match `morph_bpe_hard30_backup_20261008`, not the active weighted penalty32 checkpoint. Its training diagnostics also declare `weighted_penalty_used: false`. The active Morph-BPE row therefore displays **Checkpoint mismatch**, with an explanation. These are test corpus scores on a 0-100 scale, not accuracy percentages or scores for the current UI input.

Evaluate the exact current weighted model before replacing that report. Preserve the old report as historical evidence and reproduce/verify the new metrics and identities. Neither existing score difference establishes significance or weighted penalty32 superiority.

## Verification of evaluation display (2026-10-08)

- Archive CRC, ordered row/source/reference correspondence, text export consistency and both metric signatures/scores checked.
- Six metrics tests passed, including rejection of changed weights, changed tokenizer, tampered reports and changed evaluation rows.
- Frontend production build passed; temporary local backend/browser preview showed Plain scores and Morph checkpoint mismatch.
- No model weights changed and no model generation or training was run. Only saved translations were rescored locally.

## Original diagnostic verification

- Three new metrics tests passed: deployed tokenizer/reference score agreement, best-epoch loss selection, and missing/invalid history handling.
- Frontend production build passed.
- Fresh local backend and browser preview verified tokenizer scores, both epoch-30 histories, and unavailable BLEU/chrF++ labels.
- No training, weight changes or full NLLB inference performed for this UI change.
