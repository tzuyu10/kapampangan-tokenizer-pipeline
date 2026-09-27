# expanded_morphology_v4 penalty-64 extension

Trains the genuinely new `crossing_penalty=64` configuration on the exact
prepared training stream that produced the *real* `penalty-1/2/4/8`
artifacts already committed under `experiments/expanded_morphology_v4/`
(rule-refined on top of `source_adjudicated_v2`'s adjudicated lexicon,
3,311 operational root keys) -- not the smaller canonical
`resources/training-lexicon.json` (1,478 roots) that
`weighted_morphbpe_penalty_extension_v1` had to fall back to, since that
lexicon's own build chain needs external reference dictionaries not
present on this machine.

## Provenance

Inputs in `inputs/` were handed off as `penalty64-training-inputs.zip` and
verified before use:

- sha256 of every file matched the handoff's own manifest.
- `training-lexicon-manifest.json` shows `operational_root_keys: 3311`,
  `dataset_fingerprint` matching the official corpus.
- Decisive check: `experiments/expanded_morphology_v4/artifacts/penalty-8/candidates/vocab-6080/tokenizer-manifest.json`'s
  `artifact_fingerprint` (`f2ea195a970c387f5e5e3ba7fe5675bae9103853950d46d1072fd2685d151258`)
  is byte-identical to the tokenizer actually deployed in the webapp
  (pulled from the `Draft/Tool` branch). This confirms `inputs/training-stream.jsonl`
  really is the stream that produced the real, already-shipped-in-the-webapp
  artifacts, not an unverified or mismatched hand-off.

No re-derivation from raw text was needed or performed -- `inputs/training-stream.jsonl`
is used exactly as handed off, per the handoff's own guidance (byte-identical
preprocessing to the official artifacts).

## What this adds

`crossing_penalty=64` at vocab 6,080 / 8,192 / 16,384 -- the same trainer
(`WeightedMorphBPETrainer`) and vocab targets as the existing
`expanded_morphology_v4` `penalty-1/2/4/8` artifacts, just one more point on
the sweep. Does not touch or overwrite any existing artifact.

## Evaluation

Scored with `evaluate_candidate()` against the real `data/validation.csv`,
using `resources/training-lexicon.json` as the gold-segmentation lexicon --
the same evaluation lexicon used for the officially shipped candidate and
every other comparison in this session, so results are directly comparable
across experiments even though the *training* lexicons differ.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\expanded_morphology_v4_penalty_extension_v1\run_extension.py --dataset-root "C:\DevTools\KapampanganTokenizer\kapampangan-general-corpus-v1"
```
