# UI and thesis architecture verification

Reviewed 2026-10-06 on `Latest/WebAppFull`, HEAD `d15df33`.

## Verdict

The translation UI follows the main adapted NLLB architecture. It is not yet a fully faithful presentation of the entire thesis experiment. Source inspection establishes the mappings below; the generation observer has small-model parity tests, not a full NLLB quality evaluation.

Reference: *Morphologically-Aware Byte-Pair Encoding Tokenizer for the Kapampangan Language*, Figure 8 on PDF page 51 (printed page 48), and explanations on PDF pages 52–53. Tokenizer training/runtime descriptions are on PDF pages 48–50.

| Thesis stage | Current UI | Execution evidence | Assessment |
| --- | --- | --- | --- |
| Kapampangan input | Prepare the input | translation_service.py trims input; installed runtime applies Unicode normalization | Present; internal whitespace is not collapsed as it was during training. |
| Source tokenization and IDs | Tokenize Kapampangan | Selected bundle runtime supplies pieces and vocabulary IDs; adapter adds BOS/EOS and swaps PAD/UNK IDs | Correct translation-bundle path. |
| Source embeddings | Look up source embeddings | generation_trace.py observes encoder.embed_tokens output | Actual vectors; only four dimensions are displayed, not the entire vector. |
| Encoder | Encode the sentence | Hook observes last_hidden_state | Actual final contextual vectors; individual attention, residual and feed-forward stages are not visualized. |
| Decoder | Generate with the decoder | Actual model.generate invocation and beam-search observations | Real candidate/prefix and retained-beam data. |
| Output projection and softmax | Included within decoder trace | Native model generation computes target scores; observer runs after generation constraints/processors | No distinct UI stage. Displayed processed log scores must not be called raw probabilities. |
| Target token selection | Decoder trace and finalists | Four beams, cumulative scores and length penalty | Accurate beam-search explanation; manuscript's highest-probability wording should clarify sequence search rather than greedy selection. |
| Target decoding | Decode with the target tokenizer | Native target.decode and cumulative prefix decoding | Correct; source tokenizer does not decode Filipino. |
| Translated output | Display the Filipino output | Returned decoded text | Correct; no manual post-editing. |
| Held-out evaluation | Separate evaluation notebook | Paired BLEU/chrF++ workflow | Not computed by translating an arbitrary sentence in the UI. |

`TranslationProcess.jsx` supplies the presentation. `translation_service.py` supplies the exact IDs and generation response. `generation_trace.py` observes embeddings, final encoder vectors and beam-search decisions without an additional model pass. Observer cleanup and identical outputs are covered by the tiny-model tests.

## Material gaps and solutions

1. **Tokenizer tabs and translation use different Morph-BPE artifacts.** `tokenizer/trace_service.py` loads `artifacts/morphbpe-penalty32`; translation loads each installed bundle's source artifact. The translation Morph-BPE manifest says `weighted_penalty_used: false` and `no_merge_across_protected_boundary`. Therefore the legacy tokenizer demonstration is not proof that its weighted tokenizer produced the translation. Provide an explicit choice between a research tokenizer demonstration and the exact installed translation tokenizer; use the latter for an end-to-end trace.
2. **Weighted proposal versus hard-constrained translation condition.** The manuscript includes global allowed/crossing pair counts and a weighted crossing penalty; the installed translation tokenizer does not use that penalty. Either train source embeddings for the proposed weighted artifact under matched settings, or amend the methodology to describe the implemented hard-constrained condition. Relabeling the UI cannot resolve this experimental mismatch.
3. **Root/affix colors are not morphological evidence.** `SegmentationProcess.jsx` uses the longest piece as root and every other piece as affix. Replace this with reference spans and an unclassified state. Root and affix labels may be display annotations; do not imply a runtime dictionary is used, because the paper explicitly excludes runtime dictionary lookup.
4. **Preprocessing differs from training.** The saved adapter's normalize function applies NFC and collapses whitespace; serving currently only trims before the tokenizer applies NFC. Use a shared training-compatible normalization recipe for serving, token display and cache identity.
5. **A/B readiness does not certify experimental controls.** Current status checks installation readiness, not equivalence of saved data, split, seed, training schedule or native target artifacts. Add a saved-control audit before presenting a pair as a controlled comparison.
6. **Projection/softmax is visually implicit.** Add an explicit explanation between decoder states and beam selection, preserving the distinction between raw logits, normalized scores, processed log scores and cumulative beam scores. Do not present the four shown candidates as the full target vocabulary distribution.

## Model and verification limits

Verification rerun: all four current backend regression tests passed, including tiny-model generation parity, actual tensor/score observations, hook cleanup, invalid-input handling and process-cache behavior.

Both locally installed conditions completed 30 epochs and selected epoch 30. Only their 6,080 × 1,024 source embedding tables were adapted; pretrained encoder, decoder and native target vocabulary remain frozen. This matches the paper's source-only adaptation approach. Weights remain ignored by Git and must be supplied separately to other devices.

This verification does not certify translation accuracy, reference quality, BLEU/chrF++ superiority, statistical significance, or full model-level parity on NLLB weights. No application code or model weights were changed for this review.
