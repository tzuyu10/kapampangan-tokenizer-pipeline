# Future NLLB Source-tokenizer Contract

No NLLB model is included, downloaded, or trained here.

- `source-tokenizer-contract.json` freezes artifact identity, source outputs,
  special tokens, padding/truncation, language-token cautions, and the intended
  source-only embedding condition.
- `export_manifest.json` hashes the contract, selected artifact manifest, and
  framework-neutral adapter source.
- `kapampangan_morphbpe.nllb_adapter.SourceTokenizerAdapter` implements
  `encode_batch` without Transformers or tensor dependencies.

The future integrator must verify that the exact NLLB library exposes a truly
independent source embedding. Filipino target tokenization, decoder vocabulary,
and output projection must remain unchanged. See
`docs/NLLB_INTEGRATION_PLAN.md` and `docs/NLLB_READINESS_REPORT.md` before any
model download or training.

