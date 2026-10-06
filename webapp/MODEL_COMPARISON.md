# Active translation model comparison

Updated 2026-10-06. Both active models are source-embedding adaptations of the same pinned NLLB-200 distilled 600M base. Only Kapampangan to Filipino is supported.

| Attribute | Plain BPE | Morph-BPE |
| --- | --- | --- |
| Completed epochs | 30 | 30 |
| Best validation checkpoint | 30 | 30 |
| Training loss at best checkpoint | 1.370526 | 1.378880 |
| Validation loss | 1.233166 | 1.234986 |
| Source vocabulary | 6,080 | 6,080 |
| Learning rate | 0.0003 | 0.0003 |
| Seed | 42 | 42 |
| Batch size / accumulation | 1 / 8 | 1 / 8 |
| Initialization | Warm start | Warm start |
| Maximum epochs / patience / minimum improvement | 30 / 3 / 0.001 | 30 / 3 / 0.001 |
| Runtime source tokenizer | Plain BPE | Hard-constrained Morph-BPE |

Dataset SHA-256 matches: `69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b`. Saved split memberships also match exactly. Base revision, target tokenizer, helper, source length limits and generation settings pass the backend comparison audit. Both use four beams and at most 160 new tokens.

Plain BPE validation loss is lower by approximately 0.001820. This is not evidence of statistically significant superiority or better generated translation. Matched held-out BLEU/chrF++ evaluation and bilingual assessment remain necessary. Neither model is the older 15-epoch checkpoint. Saved-control compatibility does not resolve dataset quality or tokenizer-corpus leakage.

## Use the comparison

1. Stop the old backend with Ctrl+C and run `webapp/start-translation-backend.cmd` from the repository root.
2. Keep the frontend running or start it using `npm run dev` in `webapp/frontend/ui`.
3. Refresh the browser and open **Translator A/B**. Enter one Kapampangan input and click **Compare translations**.
4. The same text is translated with each model's own source tokenizer and embeddings. Source/output token counts and generation latency are displayed. Cached outputs are labeled and should not be used as benchmark timings.
5. On the main Translator tab, select either model and use **Show tokens** to inspect its exact source segmentation.

Installed directories: `nllb/checkpoints/plain_bpe` and `nllb/checkpoints/morph_bpe`. The original uploaded archive's `morphbpe/` wrapper was removed during installation; its manifest condition remains `morph_bpe`. Old bundles remain archived. Historical release ZIPs have not been updated to these versions.

The backend audit also notes that the translation Morph-BPE artifact uses hard constraints, not the penalty-32 scoring of the legacy visualization; do not conflate these methods in the manuscript.

## Integration verification

Real offline CPU generation through the comparison backend succeeded for both installed models on 2026-10-06:

| Input | Plain BPE output | Morph-BPE output |
| --- | --- | --- |
| Masanting ya ing abak. | Maliwanag ang umaga. | Mabilis ang umaga. |

Both used 11 source tokens and reported zero unknown tokens. This is an integration smoke test, not an endorsement of either translation. Outputs differ and require bilingual review. Single sequential call timings are not a fair speed benchmark. Raw results are saved locally in `nllb/checkpoints/comparison_smoke_20261006.json`.
