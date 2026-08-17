# Future NLLB-200 Integration Plan

Status: `future_phase`; no model was downloaded or trained in this goal.

## Fixed experimental conditions

The paper's adapted condition uses NLLB-200 Distilled 600M. Kapampangan source
text uses this 6,080-unit MorphBPE artifact; Filipino target text retains the
native NLLB tokenizer, target vocabulary, decoder embeddings, and output
projection. A new source embedding matrix has 6,080 rows and the model's
required hidden width. Only that new source embedding may be updated. All
remaining pretrained parameters must stay frozen.

Baseline and adapted runs must use identical reviewed PAM-Filipino pairs,
train/validation/test assignment, batch size, optimizer, learning-rate
schedule, update/epoch budget, random seeds, checkpoint rule, maximum lengths,
and decoding configuration. Tokenizer condition must remain the primary
experimental variable.

## Source adapter

`kapampangan_morphbpe.nllb_adapter.SourceTokenizerAdapter` is a
framework-neutral implementation. `encode_batch` produces:

- source token strings and IDs;
- right-padded attention masks;
- vocabulary size and special-token mapping;
- artifact fingerprint;
- NFC-normalized source strings and normalized code-point offsets; and
- explicit per-row truncation flags.

Padding is opt-in/right-sided with `<pad>` ID 0. Truncation is disabled by
default and requires an explicit positive `max_length`. The future integration
must convert these plain Python rows to the selected framework's tensors; the
adapter deliberately does not import or download NLLB/Transformers.

## Mandatory feasibility gate

Before fine-tuning, inspect the exact future NLLB implementation and prove that
it supports an independently replaceable **encoder source embedding** without
altering or retying the target embedding or decoder output projection. Do not
assume this from a library API. Add assertions that:

1. the source embedding has 6,080 rows;
2. all source IDs are in range;
3. gradients exist only for the new source embedding;
4. every other parameter is frozen and unchanged after a probe update;
5. Filipino language-token and generation behavior remain native; and
6. baseline/adapted decoding settings are byte-for-byte equivalent.

If the library exposes only a single tied source/target embedding whose
replacement changes target behavior, stop. That violates the experimental
contract and requires a reviewed architecture adapter, not an implicit
workaround.

## Language tokens

This project does not assume NLLB has a native Kapampangan language token.
Source language-token handling must be specified and held constant after the
future library/model is inspected. Filipino target language-token handling must
remain native and unchanged. These are unresolved integration properties, not
completed claims.

## Required inputs before execution

- a rights-reviewed, human-validated PAM-Filipino corpus at the paper's scale;
- leakage-safe aligned splits, including a sealed 1,300-sentence test set;
- linguist-adjudicated tokenizer boundary references;
- the selected artifact and verified fingerprints;
- an approved model-cache/download location and reproducible software lock;
- pre-registered baseline/adapted hyperparameters and decoding; and
- successful feasibility/freeze assertions above.

