# penalty-64 @ 16k handoff — the real training inputs

These are the two files that actually produced the official `penalty-8` /
`penalty-4` / `penalty-2` / `penalty-1` / `morphbpe` artifacts in
`experiments/expanded_morphology_v4/artifacts/`. They are **not** the same
as the `kapampangan-general-corpus-v1` zip or its `resources/training-lexicon.json`
(1,478 roots) used for the current webapp demo — those are a different,
smaller lexicon. Training `penalty-64` on these instead is what makes it
comparable to the real Phase 3 grid.

## Files

| file | sha256 | source path in repo |
|---|---|---|
| `training-lexicon.json` | `5219e018bcd9c4aec44e377f0ba37b07dd2ce38485173102b5462501651050d8` | `experiments/source_adjudicated_v2/resources/training-lexicon.json` |
| `training-lexicon-manifest.json` | `de1758f16444cfa45865ccb38f63c034b1779a94b8417a4a6e41a282fcce8f72` | `experiments/source_adjudicated_v2/resources/training-lexicon-manifest.json` |
| `training-stream.jsonl` | `fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7` | `experiments/expanded_morphology_v4/runs/prepared/training-stream.jsonl` |
| `training-stream-manifest.json` | `712eb538bfc48b315971646be1db135f1787df37780872800993ed1160f65d20` | `experiments/expanded_morphology_v4/runs/prepared/training-stream-manifest.json` |
| `plain-training-stream.jsonl` | `c8aeadd8ec64e763caf44d05a4bb17adde055fd9e788235b968077db0cc5a5e5` | `experiments/expanded_morphology_v4/runs/prepared/plain-training-stream.jsonl` |

(`plain-training-stream.jsonl`'s checksum is also recorded inside
`training-stream-manifest.json` as `plain_stream_sha256` — same manifest
covers both streams, no separate manifest file for it.)

Verify byte-for-byte before use (same convention this project already
follows for every external/handed-off dataset):

```
sha256sum training-lexicon.json training-lexicon-manifest.json \
          training-stream.jsonl training-stream-manifest.json \
          plain-training-stream.jsonl
```

- **`training-lexicon.json`** — the real lexicon: 3,311 operational root
  keys, 26 compounds (`operational_root_keys: 3311` in the manifest).
  Defines which morpheme boundaries are "protected" during training.
  `evidence_status: external_source_supported_provisional_silver_not_gold`
  — some entries trace to external reference dictionaries (e.g. Forman
  1971); treat as project-internal, not for further redistribution.
- **`training-stream.jsonl`** — the morphology-resegmented training stream
  (143,529 word types / 1,476,145 occurrences) that
  `train_constrained_morphbpe.py` / the `weighted_morphbpe_v3` trainer
  actually consume. Pre-processed and frozen — use it as-is rather than
  re-deriving from raw text, so preprocessing is byte-identical to the
  official artifacts.

## What to train

**`morphbpe`, `crossing_penalty=64`, `target_vocab=16384`** (the genuinely
new candidate) — using the same `WeightedMorphBPETrainer` /
crossing-penalty-weighted merge rule already used for `penalty-1/2/4/8`
(score = `allowed_frequency(p) - 64 * crossing_frequency(p)`), fed by
`training-stream.jsonl` + `training-lexicon.json` above instead of the
sealed-zip corpus.

Follow the same isolated-experiment pattern already used for
`weighted_morphbpe_penalty_extension_v1/run_extension.py` (new artifact
directory, don't touch or overwrite any existing artifact) — just point its
inputs at these files and set vocab to 16,384 instead of 6,080.

**If you also want to retrain `plain`-BPE and Unigram-LM at 16k yourselves**
(rather than reusing the existing official artifacts below), use
`plain-training-stream.jsonl` — the same input `experiments/expanded_morphology_v4/train_unigram_ablation.py`
and the `plain` condition's own trainer consume; it does not need the
lexicon at all (plain/Unigram have no protected-boundary concept). Match
the target vocab (16,384) and trainer logic exactly.

**Important cross-check:** training on this exact stream is deterministic,
so your retrained `plain`/`unigram` @ 16k should come out **byte-identical**
to the existing official artifacts:

- `experiments/expanded_morphology_v4/artifacts/plain/candidates/vocab-16384/`
- `experiments/expanded_morphology_v4/artifacts/unigram-ablation/vocab-16384/`

Diff your output's `tokenizer.json`/`merges.json`/`vocab.json` against
those (or compare `artifact_fingerprint` in `tokenizer-manifest.json`). If
they match, your pipeline is confirmed identical to the official one and
the new `penalty-64` result is trustworthy for comparison. If they
**don't** match, something in your training script has diverged from the
official pipeline (different vocab-building logic, different trainer
version, etc.) — worth finding before trusting the `penalty-64` number
either, since the same script family produced it.

## Scoring

For a result that's actually comparable to the thesis's real Phase 3
selection, score against the frozen held-out reference in
`experiments/tokenizer_selection_v1/` (root-family-disjoint DEV 272 / TEST
262 rows), the same one `penalty-8` was selected on — not a new ad hoc
validation set. `run_selection.py` already knows how to score fertility,
boundary F1, and MCF1 for any tokenizer artifact at a given vocab size.
