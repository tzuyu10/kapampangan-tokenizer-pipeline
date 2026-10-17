# Kapampangan tokenizer inputs with bounded Tagalog additions

This separate research package preserves the exact Kapampangan inputs used by
the current weighted penalty32 and infix-first experiments. It adds existing
Tagalog text and dictionary entries. No sentences or translations were generated.

| Resource | Original Kapampangan | Tagalog addition | Combined |
| --- | ---: | ---: | ---: |
| Unique operational root entries | 3,311 | 993 | 4,304 |
| Tokenizer training text records | 26,268 | 7,880 | 34,148 |

The counts use `floor(original_count * 0.30)`, separately. The root denominator
excludes the original compound inventory and spelling-variant mapping, which are
preserved. A corpus record can contain multiple sentences. These are record
counts, not word/token counts. Tagalog makes up about 23.08% of combined records;
the manifest also records actual word occurrence counts.

## Use in Colab

1. Open `Retrain_PAM_TL_30pct_Tokenizer_Colab.ipynb` in Google Colab.
2. Run the upload cell and select `tagalog_30pct_tokenizer_inputs.zip`.
3. Keep the defaults to train weighted Morph-BPE, penalty32, vocabulary6,080.
   To train the separate infix-first48 condition, set `ALGORITHM='infix-first'`
   and `PENALTY=48`. To train a matched Plain BPE control, use `ALGORITHM='plain'`.
4. Run training, then download the new tokenizer artifact using the last cell.

The tokenizer uses CPU and the Python standard library. A GPU is unnecessary.
Training time has not been benchmarked. Each output needs a new directory.
The notebook verifies every packaged file before training. The prepared streams
already incorporate the selected lexicons and language-specific morphology.

## Use locally

Extract the input ZIP. In the extracted folder, run:

```powershell
python train_tokenizer.py --inputs . --output ..\pam_tl_weighted32 --algorithm weighted --penalty 32 --vocab-size 6080
```

Optional matched conditions, each in its own output folder:

```powershell
python train_tokenizer.py --inputs . --output ..\pam_tl_infix_first48 --algorithm infix-first --penalty 48 --vocab-size 6080
python train_tokenizer.py --inputs . --output ..\pam_tl_plain --algorithm plain --vocab-size 6080
```

## Files that matter

- `data/train.csv`: combined `id,text` training records; original order/text first.
- `data/kapampangan_train.csv`: exact original training CSV bytes.
- `data/tagalog_train.csv` and `.txt`: only the 7,880 selected Tagalog records.
- `data/tagalog_train.jsonl`: original and cleaned text, original dataset row
  index, document title/start row, revision, hashes and review status per record.
- `lexicons/tagalog_roots.json`: 993 selected unique Tagalog words, definitions,
  original dictionary row indices, source links and sample frequencies.
- `lexicons/kapampangan-training-lexicon.json`: exact original Kapampangan lexicon.
- `lexicons/lexicon-pam-tl.json`: language-partitioned inventory linking both.
- `prepared/training-stream.jsonl`: combined morphology-aware BPE input.
- `prepared/plain-training-stream.jsonl`: same surface counts without boundaries.
- `prepared/role-spans.jsonl`: conservative infix roles for the infix-first option.
- `manifest.json`, `checksums.json`, `verification.json`: counts, provenance,
  filtering/selection policy, identity and verification evidence.
- `provenance/`: source citations, licenses, original manifests and builder.
- `source/`, `runtime/`, `vendor/`: frozen Python code used by this experiment.

Use the supplied training script. Do not feed the language-partitioned lexicon
container into an older Kapampangan-only preprocessing command. Kapampangan
preprocessing remains exactly frozen; Tagalog is processed with separate Tagalog
rules and only its 993 selected roots. Shared strings retain their observed
source-language analyses during preparation. Runtime remains ordinary BPE
without a language classifier or dictionary lookup.

The upstream Tagalog segmenter returns underlying `um,kain` for `kumain`.
The adapter converts this into lossless surface spans `k|um|ain`, preserves case,
and falls back to an intact word for unsupported surface analyses. These are
automatic provisional analyses, not human-validated morphology annotations.

## Selection and source provenance

The original inputs come from the user's preserved
`morphbpe-penalty32-dataset-bundle.zip`. Their verified dictionary has 3,311 root
keys, unlike the older 1,478-root lexicon still present in the repository's
top-level resources folder. The original training stream SHA256 starts
`fc520e0e3359` and the lexicon SHA256 starts `5219e018bcd9`; full hashes are saved.

Tagalog text comes from [linkanjarad/Wikitext-TL39](https://huggingface.co/datasets/linkanjarad/Wikitext-TL39),
revision `7c1a76c2c1864abf434453e312f034d0cf211fff`, `data/train.parquet`.
The full download is only a local source cache. The delivery contains the selected
7,880 records. Each selected record has its original zero-based Parquet row index.
The source dataset is already distributed as train only; the added subset is
assigned to tokenizer training, with no new validation/test split invented.

Selection scans the complete 1,524,071-row source, rejects headings, URLs/markup,
control characters and non-Latin-heavy text, requires5-80 word strings and at
least two common Tagalog marker occurrences, and removes normalized duplicates.
WikiText `@-@`, `@,@` and `@.@` artifacts are repaired; NFC and whitespace are
normalized. Other spelling and punctuation are preserved. Qualifying rows are
sampled by seeded SHA256 ranking, with at most three rows per source document.
These heuristics cannot certify that every word is Tagalog or every webpage was
human-authored. No new synthetic examples were generated here.

New text excludes punctuation/case/whitespace-normalized matches to original
Kapampangan training, validation and test text, plus both sides of the current
translation validation/test rows. Held-out text is used only for exclusion and
is not included in this delivery or used for scoring/parameter selection.
This check does not establish that the older Kapampangan tokenizer corpus is
free of all translation-evaluation overlap or that paraphrases never overlap.

The dictionary is from the local `filipino-tokenizer` repository, originally
maintained at [JpCurada/filipino-tokenizer](https://github.com/JpCurada/filipino-tokenizer).
Rows retain their `tagalog.pinoydictionary.com` source links. Filtering requires
one lexical word of at least four characters, a nonempty definition and a word
matching its URL headword. Empty/malformed/truncated entries and duplicates are
excluded. Existing Kapampangan root/variant/compound keys are excluded from the
new root inventory. Eligible roots are ranked by exact-word frequency in the
selected Tagalog training sample, with seeded hash tie-breaking.

The MIT notice for copied Filipino tokenizer code is retained. Original corpus
citations and source rights caveats are preserved. Use remains local experimental
research; this package does not establish new public redistribution rights.

## After retraining

This prepares source tokenizer training inputs, not additional Kapampangan to
Filipino translation pairs. Keep the native Filipino NLLB target tokenizer.
A new source tokenizer needs a fresh compatible source embedding table and
source-embedding adaptation before translation use. Existing source embeddings
must stay paired with their original token IDs. Compare conditions using the
same augmented training text and matched settings. Translation improvements and
human linguistic quality remain unverified.

New exports use the augmented dataset fingerprint in both tokenizer metadata
and artifact manifests, with refreshed fingerprints and checksums. The original
base dataset identifier and input-package manifest hash remain recorded in
metadata. Keep these artifacts separate from the unaugmented condition.
