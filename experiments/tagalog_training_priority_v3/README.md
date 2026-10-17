# Training-only infix and other-affix priority

The user requires all morphology resources to be used during training only.
The previously suggested runtime-boundary method was abandoned before any
implementation. This experiment instead changes only the training priority
schedule. Both new variants use byte-identical installed ordinary BPE inference,
with no dictionary lookup, morphology analysis, boundary enforcement or per-word
exception during runtime.

## Fixed experiment

- Same v2 input package, 34,148 records, 3,311 original roots and 993 additions.
- Identical raw corpus and morphology boundary annotations.
- Existing infix role spans retained exactly.
- Other-affix roles require an accepted analysis matching the frozen boundaries.
  Shared surface/boundary keys retain only roles supported by both language
  analyses. Root, ambiguous, unknown and separator spans get no affix priority.
- Training order: infixes, other affixes, then ordinary weighted selection.
- Infix budget32, other-affix budget256, root budget0, crossing penalty48.
- Vocabulary targets6,080 and8,192, one deterministic trajectory with snapshots.
- All settings fixed before reading DEV in this run.

The audit identifies11,993 other-affix spans /95,357 weighted occurrences and
retains1,026 infix spans /10,063 occurrences. Support exhausts after6 infix merges
and229 other-affix merges, before the remaining weighted phase.

## Result

| Vocab | Installed v1 DEV F1 | Revised v2 DEV F1 | New DEV F1 | Installed v1 TEST F1 | New TEST F1 |
|---|---:|---:|---:|---:|---:|
| 6,080 | 59.334% | 58.960% | 56.805% | 58.006% | 53.673% |
| 8,192 | 58.399% | 57.903% | 55.340% | 53.910% | 50.582% |

Both new variants produce `nag | aral` for `nagaral`, `nag | - | aral` for
`nag-aral` and `basa | hin` for `basahin`, without runtime morphology. However,
their full DEV/TEST boundary scores and DEV consistency scores are lower. Keep
the installed infix-first48/6,080 candidate. These examples do not establish
overall or Tagalog morphological superiority.

Reports compare12 conditions: the two new variants, v1/v2 infix-first48, revised
weighted32, Plain BPE and Unigram at matched sizes. Existing controls are
reencoded and their previous DEV/TEST/corpus scores reproduced. DEV selection
precedes historical TEST reading in this run; TEST has been evaluated before.
Labels are mixed silver/user-derived and most reference words occur in training.
Tagalog corpus evaluation has no independent reviewed morphological gold.

## Reproduce from the repository

Copy the complete verified v2 `inputs` and `evaluation_inputs` folders into a new
result directory. Create a `reports/protected_before.json` file mapping the
absolute paths of files to protect to their pre-edit SHA-256 hashes, as in this
completed run. Then use the project Python environment:

```powershell
python experiments/tagalog_training_priority_v3/train.py --inputs RESULTS/inputs --output RESULTS
.venv-translation/Scripts/python.exe experiments/tagalog_training_priority_v3/evaluate.py --results RESULTS --v1 ORIGINAL_COMPARISON --v2 REVISED_V2_COMPARISON
python -I experiments/tagalog_training_priority_v3/runtime_only_check.py --results RESULTS
.venv-translation/Scripts/python.exe experiments/tagalog_training_priority_v3/verify.py --results RESULTS --v2 REVISED_V2_COMPARISON
python -m unittest discover -s experiments/tagalog_training_priority_v3 -p 'test_*.py' -v
```

Training and the exported runtime need only the standard library. Unigram
comparison uses tokenizers0.21.0 already in the project environment. The verifier
independently checks6,408 reference encodings, metric arithmetic, unchanged
inputs/infix roles, nested snapshots and961 protected files. An isolated runtime
check covers1,090 reference/edge cases without importing morphology modules.

## Installed state

No webapp tokenizer, translator or neural checkpoint was changed. This experiment
does not train source embeddings or evaluate translation quality. Any later
translation condition must use the matching tokenizer and source embeddings.
