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

Scores are computed at request time, not hardcoded. The source disclosure includes the actual tokenizer SHA-256 and reference splits. F1 ranges from 0 to 1. Fertility is pieces per word; fewer pieces alone do not establish better morphology or translation. The penalty-32 tokenizer is a different artifact from the installed hard-constrained Morph-BPE translation tokenizer.

## Translation diagnostics

The server reads each installed bundle's `manifest.json` and `history.json`. It respects `KAPAMPANGAN_MODEL_DIR`. Missing or invalid histories display an unavailable message. Both losses come from the epoch with minimum saved validation loss, rather than mixing the best validation epoch with the final training epoch.

| Local condition | Completed epochs | Best validation epoch | Training loss | Validation loss |
| --- | ---: | ---: | ---: | ---: |
| Plain BPE | 30 | 30 | 1.371 | 1.233 |
| Morph-BPE | 30 | 30 | 1.379 | 1.235 |

Loss is not accuracy. BLEU and chrF++ display **Not evaluated** because no paired held-out quality report is available for these installed bundles. Older experiment scores are not substituted. Run `notebooks/NLLB_600M_Kaggle_Paired_Evaluation.ipynb` with both exact bundles and aligned held-out references to obtain quality scores. Importing that output into the UI is not implemented by this initial diagnostic endpoint.

## Verification

- Three new metrics tests passed: deployed tokenizer/reference score agreement, best-epoch loss selection, and missing/invalid history handling.
- Frontend production build passed.
- Fresh local backend and browser preview verified tokenizer scores, both epoch-30 histories, and unavailable BLEU/chrF++ labels.
- No training, weight changes or full NLLB inference performed for this UI change.
