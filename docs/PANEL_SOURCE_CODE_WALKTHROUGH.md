# Panel source-code walkthrough and manuscript alignment

Reviewed 2026-10-06 against `Morphologically-Aware Byte-Pair Encoding Tokenizer for the Kapampangan Language .pdf` (78 PDF pages). References below use PDF page numbers; printed page numbers are three lower. This is a review of the current deployment, not a change to experiments or the manuscript. The older TOOL_PAPER_ARCHITECTURE_AUDIT.md describes an earlier 15-epoch deployment.

## What you can accurately claim

The application implements Kapampangan-to-Filipino translation with two independently adapted source embedding tables on a shared frozen NLLB-200 distilled 600M base. The current Plain BPE and hard-constrained Morph-BPE bundles both completed 30 epochs and selected epoch 30. The architecture and comparison conditions substantially match the SOP, but the deployed Morph-BPE is NOT the weighted crossing-penalty extension proposed in this manuscript.

Do not say the whole paper is already implemented and validated. Functioning translation, matching training controls, translation quality, and statistical significance are separate claims.

## Explain three separate processes

1. **Tokenizer training:** source corpus -> normalization/pre-tokenization -> lexicon-guided morphology -> protected boundaries -> learn vocabulary and merge rules -> export tokenizer artifact.
2. **Translation adaptation:** paired source/target sentences -> condition-specific source IDs and native target IDs -> train only the new source embeddings against target labels -> save best checkpoint. Repeat independently for Plain BPE and Morph-BPE with matched controls.
3. **Live translation:** input -> saved tokenizer -> ID conversion -> trained source embedding -> frozen NLLB encoder and decoder -> native Filipino target IDs -> decoded text. No lexicon lookup or training happens during this request.

The tokenizer creates units and IDs; it does not translate words by dictionary lookup. The NLLB network generates the translation.

## Files to open, in presentation order

All paths below are relative to the repository root. Use VS Code Ctrl+P to open the path and Ctrl+G for the line number. Line numbers describe this review snapshot.

| Step | File and location | What to show and explain |
| --- | --- | --- |
| 1. Surface preparation | `src/kapampangan_morphbpe/normalization.py:6`; `src/kapampangan_morphbpe/pretokenizer.py:19` | NFC normalization and separation of word, whitespace and punctuation units. NFC is not comprehensive spelling correction. |
| 2. Lexicon and morphology | `experiments/expanded_morphology_v4/run_experiment.py:211`; `experiments/expanded_morphology_v4/expanded_morphology.py:317` | `prepare()` loads the training lexicon, calls the expanded segmenter and records protected offsets for accepted analyses. `_analyze()` at line 747 checks known forms and rule candidates; unsupported/ambiguous cases are not arbitrarily forced into roots. Lexicon input: `experiments/source_adjudicated_v2/resources/training-lexicon.json`. |
| 3. Deployed tokenizer learning | `src/kapampangan_morphbpe/bpe.py:71`, `:82`, `:108`; `experiments/expanded_morphology_v4/train_constrained_morphbpe.py:119` | `_sequence_pairs` skips protected joins; `_apply_pair` prevents crossing them; `ConstrainedBPETrainer` learns frequency-ranked merges. This is the hard-constrained algorithm used by the deployed Morph-BPE artifact. |
| 4. Plain BPE control | `experiments/expanded_morphology_v4/run_experiment.py:211` and `:568` | The plain stream preserves the same surfaces and frequencies but supplies empty boundary lists. The same trainer therefore performs ordinary BPE without morphological protection. |
| 5. Paper's weighted extension | `src/kapampangan_morphbpe/weighted_bpe.py:36`, `:82`, `:126` | Allowed and crossing counts are separate; `_score` implements A(p) - lambda*C(p). Weighted code exists, but its artifacts are not the installed translation Morph-BPE. |
| 6. Exported evidence | `nllb/checkpoints/morph_bpe/source_artifact/tokenizer-manifest.json`; corresponding Plain BPE file | Show vocabulary size, hashes, `weighted_penalty_used: false`, `merge_constraint`, and `lexicon_used_at_runtime: false`. These identify the actual artifact more reliably than a UI label. |
| 7. Runtime tokenization | `nllb/checkpoints/morph_bpe/runtime/kapampangan_morphbpe_runtime/tokenizer.py:247` and `:324` | `encode` pre-tokenizes; `_encode_pretoken` uses whole-surface vocabulary lookup, otherwise character units and lowest-rank learned merges; unsupported characters become UNK. No morphology dictionary is loaded. The root `runtime/.../tokenizer.py` is byte-identical to this deployed copy. |
| 8. NLLB ID compatibility | `nllb/checkpoints/morph_bpe/nllb_source_adapter.py:65` | `SourceTokenizer` verifies artifacts, swaps native PAD/UNK IDs 0 and 1 at the model boundary, and surrounds content with BOS/EOS. This keeps NLLB padding behavior correct without changing the source segmentation. |
| 9. What was trained | Same adapter, `install_source_embedding` at 203, `warm_start` at 241, `train` at 299 | All pretrained parameters are frozen. Only the independent 6080 x 1024 encoder embedding is trainable: 6,225,920 parameters. Warm start averages native subtoken embeddings using the same recipe for both conditions. The native decoder vocabulary remains unchanged. |
| 10. Training loop/checkpoint | Same adapter, `prepare` at 173, `collate` at 192, `train` at 299 | Source IDs and native target labels are batched; ignored target padding is -100. Model loss drives backpropagation into source embeddings; AdamW updates those weights. Validation loss selects `best_source.safetensors`; `last.pt` stores resume state. Read `manifest.json` and `history.json` in each bundle for actual settings and epochs. |
| 11. UI and local API | `webapp/frontend/ui/src/pages/TranslatorPage.jsx:26`; `webapp/frontend/ui/src/api.js:58`; `webapp/backend/server.py:106` | The browser sends text and condition to the local Python backend. This API is communication between app components, not a paid external translator. |
| 12. Actual translation | `webapp/backend/translation_service.py:127` | `translate()` loads the matching tokenizer/weights, builds source IDs and attention mask, and calls `model.generate`. Native target decoding produces Filipino text. `compare()` at 191 repeats this for both conditions. `tokenize_adapted()` at 205 powers Show tokens. |
| 13. Evaluation | `notebooks/NLLB_600M_Kaggle_Paired_Evaluation.ipynb`, section 5 | Both models translate identical held-out rows with matched decoding; references are used to compute corpus BLEU and chrF++. Evaluation does not update weights. Intrinsic metric code is in `experiments/tokenizer_selection_v1/run_selection.py`, especially `_score` and `_mcf1`. |

For encoder/decoder internals, show `.venv-translation/Lib/site-packages/transformers/models/m2m_100/modeling_m2m_100.py`: M2M100EncoderLayer line 578, M2M100DecoderLayer 656, M2M100Encoder 920, M2M100Decoder 1107, and M2M100ForConditionalGeneration 1519. These are installed Hugging Face implementations used by NLLB, not original project code. The conditional-generation forward computes cross-entropy at line 1604. Do not edit library code for the demo.

## Alignment findings and solutions

| Paper claim | Current evidence | Required explanation or solution |
| --- | --- | --- |
| SOP: Morph-BPE vs matched Unigram for intrinsic evaluation; Morph-BPE vs Plain BPE for translation (PDF 14-16) | Those experimental families exist; translation compares Plain BPE and Morph-BPE. | Keep the two baselines distinct. Do not call Unigram the deployed translation baseline. |
| Weighted score A(p)-lambda*C(p) (PDF 8-9, 48-49, 58-59) | Implemented in weighted_bpe.py, but installed Morph-BPE manifest says false for weighted penalty. | Major mismatch. Either retain current checkpoints as a hard-constrained experiment and obtain approval for revised methods, or select the intended weighted artifact using validation and adapt NLLB again with that exact tokenizer. Preserve current runs as an ablation. Never swap a new tokenizer into old embeddings or relabel the old checkpoint as weighted. Reuse Plain BPE only if all controls and data remain valid and matched. |
| Lexicon only during training; rank-based runtime (PDF 43, 47, 50) | Runtime performs vocabulary lookup and learned merges without lexicon. | Aligned. Training protection does not guarantee all unseen runtime forms have correct morpheme boundaries. |
| Source-embedding-only adaptation, native target vocabulary (PDF 52) | Explicit freezing and independent source table in adapter. | Aligned. Specify warm-start initialization and encoder-only replacement rather than implying global vocabulary resizing or full-network training. |
| Spelling-variant normalization (PDF 43) | NFC normalization, lowercase comparison keys, and translation whitespace normalization are present. | Narrow manuscript wording or implement/test an explicit spelling policy. Lexicon variant recognition is not universal spelling correction. |
| Affixation-limited scope (PDF 16); segmentation pseudocode (44-46) | Expanded segmenter includes reduplication and morphophonemic rules in addition to listed affixes. | Document the actual expanded scope or regenerate an appropriately scoped experimental tokenizer. |
| Rust preprocessing (PDF 56) | Rust bridge exists, but the v4 preparation entry point explicitly uses the Python ExpandedMorphologicalSegmenter. | Describe the actual Python v4 path. Existing Rust code alone is not evidence it generated these artifacts. |
| Vocabulary chosen using morphological distance (PDF 49) | Selection code maximizes DEV boundary F1, then exact match, then lower fertility. | Describe the implemented selection criterion and retain the selection provenance for the chosen artifact. Do not present a candidate flag as proof of final selection. |
| Highest-probability token selection (PDF 53) | Live generation uses four-beam autoregressive search, no sampling, maximum 160 new tokens. | Explain beam search; avoid describing it as independent greedy argmax at every position. |
| Paired sentence-level tests and effect sizes (PDF 68-71) | Paired evaluation notebook currently produces corpus scores and aligned predictions, not the promised t-test/Wilcoxon/Cohen dz results. | Add a separately specified analysis of paired sentence scores and appropriate evaluation units. Do not infer significance from two corpus scores or training losses. |
| Human-validated references and held-out data (PDF 39-40, 66-67) | Saved hashes/split IDs establish consistency, not semantic correctness or tokenizer-corpus isolation. | Supply reviewer provenance and audit corpus overlap. Current model dataset hash is 69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b; do not substitute another CSV because its filename is similar. Intrinsic selection code explicitly says its reference is not independent native-speaker gold. |

The legacy Tokenizer UI uses a penalty-32 artifact. Demonstrate deployed tokenization using **Translator -> select condition -> Show tokens**. Do not use the legacy visualization as proof that the translation checkpoint uses penalty 32.

## Suggested five-minute demonstration

1. State the research comparison and show the two manifests and histories. Both active best checkpoints are epoch 30; this is verified from histories, not inferred from ZIP names.
2. Show preparation and protected boundaries, then the actual hard-constrained trainer. If asked about the weighted equation, open weighted_bpe.py and disclose the deployment mismatch.
3. Show the runtime encoder and source ID adapter. Explain why tokenizer training and runtime tokenization are different.
4. Show install_source_embedding and its requires_grad assertion. Explain that the decoder remains frozen but can generate different output because the source representations change.
5. Enter the same short sentence in Translator A/B; inspect tokens for each condition using Show tokens. Acknowledge translation errors rather than selecting only favorable examples.
6. Show the evaluation notebook as the quantitative evaluation workflow. Present completed result files only if they belong to these exact checkpoints and dataset.

Suggested opening: "Our system first learns a source tokenizer, then independently learns source embeddings for that tokenizer using paired Kapampangan-Filipino sentences. At deployment, its IDs and embeddings feed the frozen NLLB encoder-decoder, which generates Filipino tokens. Our currently installed Morph-BPE is the hard-constrained condition. The manuscript's weighted extension exists in the repository but still needs a matching translation experiment if retained as the proposed method."

## Review limits

This review inspected manuscript text and architecture figures, active bundle metadata/history, tokenizer training and runtime source, adaptation code, frontend/backend calls and evaluation notebook. Installed tokenizer JSONs match the corresponding v4 plain/morphbpe vocab-6080 candidates byte-for-byte. No retraining, new translation benchmark, manuscript edit or hypothesis test was performed. The last integration smoke test established that both models generate output, not that either is accurate.
