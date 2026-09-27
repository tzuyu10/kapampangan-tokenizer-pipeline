# Project integration validation — 2026-09-18

The updated notebook uses the exact matched plain-BPE and hard-constrained MorphBPE
artifacts from `experiments/expanded_morphology_v4/artifacts/`.

Passed software checks:

- All tokenizer checksum inventories and all four frozen bundle hashes/row counts.
- Runtime output equals pre-tokenized bundle IDs for **all 4,227 records in both conditions**.
- The model-boundary 0/1 ID permutation is reversible and leaves segmentation unchanged.
- Explicit plain-BPE routing and rejection of unknown conditions; no native-ID fallback.
- Correct attention masks and position handling for source UNK=0 and PAD=1.
- Original scaled-embedding class retained; warm-start control rows match native rows.
- Real tiny-M2M100 forward/backward; source gradients are nonzero and all frozen weights
  remain unchanged.
- Generic adapter training, checkpoint resumption, and save/reload regression tests.
- Project runtime/artifact + source-weight export reload preserves token IDs and logits.
- Notebook schema, code-cell syntax, and embedded-helper consistency.
- Real native NLLB tokenizer on the complete bundle: longest source 184 tokens,
  longest target 117 tokens, and zero source unknown tokens under both artifacts.

Environment: Python 3.12, PyTorch 2.6.0 CPU, Transformers 4.48.3,
Tokenizers 0.21.0, SacreBLEU 2.5.1. Tests use the actual M2M100 architecture at tiny
dimensions, not a simulated model. Full 600M weights and Colab GPU training were
not executed. The notebook includes the real GPU preflight.

Data audit: zero cross-split identical normalized/case-folded sources; 22 repeated
normalized source occurrences within training. The original split manifest identifies
24 partially aligned training rows. No records were changed or silently removed.

Original tokenizer-training corpus and prepared streams were not present at their
recorded paths. Tokenizer-training versus translation-test overlap remains unaudited.
This is an unresolved research-data limitation, not a software integration check that
can be declared passed without the source corpus.
