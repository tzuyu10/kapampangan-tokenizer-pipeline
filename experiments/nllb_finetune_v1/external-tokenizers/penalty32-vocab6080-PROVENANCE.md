# External tokenizer: morphbpe-penalty32 @ vocab 6,080

Copied from a teammate's branch, not produced by this repo's own
`experiments/expanded_morphology_v4` grid script. Extracted via
`git show`, never merged/pulled — that branch
(`Draft/TrainedOnly-Tokenizer-V1`) deletes most of this repo and is not a
feature branch.

- Source: `origin/Draft/TrainedOnly-Tokenizer-V1`,
  `webapp/backend/tokenizer/artifacts/morphbpe-penalty32/`, commit `8be05d3`.
- `artifact_fingerprint`: `2dc38cb89b2b3545c134b43c932a1f343453372bdbaeea090900d5566d759ad1`
- Byte-verified against the checksums recorded in its own
  `tokenizer-manifest.json` after extraction (matches).
- Training provenance (per its own manifest/card, verified by the
  teammate): `training_stream_sha256 fc520e0e3359c3...` — the same
  `experiments/expanded_morphology_v4/runs/prepared/training-stream.jsonl`
  that produced the official `penalty-1/2/4/8` grid; `dataset_fingerprint`
  matches the official grid. Extends the crossing-penalty sweep to 32
  (score = `allowed_frequency(p) - 32 * crossing_frequency(p)`). Not
  selected, not a frozen thesis artifact (its own card says so).
- Vocab 6,080 -- NOT the 16k retraining that was requested; the teammate
  appears to have iterated on the penalty value at the original vocab
  size first.
