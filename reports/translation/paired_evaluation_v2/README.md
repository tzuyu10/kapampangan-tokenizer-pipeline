# Verified saved translation evaluation

Imported from the user-supplied `paired_evaluation_v2_backup.zip` on 2026-10-08. `verification.json` records its SHA-256, original report-file hashes and independently reproduced scores.

Both conditions contain 1,659 ordered predictions matching the full test split of CSV SHA-256 `69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b`. Every saved ID, source and target matches the CSV. Hypotheses/reference exports match prediction JSONL. Both reported output-limit counts are zero. Archive CRC passed. SacreBLEU 2.5.1 reproduced corpus BLEU with 13a tokenization and chrF++ with word_order=2, including signatures.

| Evaluated checkpoint | BLEU | chrF++ | Active model match |
| --- | ---: | ---: | --- |
| Plain BPE 30 | 45.80158515598869 | 65.39727705338743 | Yes |
| Hard-constrained Morph-BPE 30 | 46.00762043052671 | 65.31353458952087 | No, matches preserved hard30 backup |

The Morph report's source-weight hash is `399a4f2edea35c3e7bcf13119aad3146997d67c84b8899a7206df392dc3b3b91`, source-tokenizer hash `b034e67b0c6e53db63230e418870ab5e3a8414435236ab75d3d6971443381c01`. Both match `nllb/checkpoints/morph_bpe_hard30_backup_20261008`. Its saved training diagnostics explicitly record weighted_penalty_used=false.

The active weighted penalty32 model has weight hash `6d7721111fa35f7b11e97b5e832e32fa81f28f58d23fdfdfd60fbdcdf60f67fc` and tokenizer hash `3021219634a9f510489405526fca3e8d60823089f95673bcf9c0f9a4e4c7e972`. The UI rejects attribution of the old report to this model. Retain these original results for historical comparison; a new evaluation of the current weighted model is required.

Verification checks saved prediction/reference arithmetic and recorded checkpoint identities. It does not rerun cloud generation, establish bilingual human correctness or statistical significance. `ui-preview.jpg` shows the verified local preview after integration.
