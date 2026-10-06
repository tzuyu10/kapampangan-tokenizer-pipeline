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

## Phase 4 verification (2026-08-31) — done

That independence property was verified on the real
`facebook/nllb-200-distilled-600M` weights (Colab, Tesla T4). Result:
**sound, with one operational caveat** — `model.tie_weights()` re-points the
encoder embedding back to the shared matrix, so Phase 5 must apply the
encoder-only swap after model load and re-apply it around any checkpoint
round-trip. 7 of 8 mechanical checks pass; the 8th is that expected re-tie
behaviour.

- `phase4-architecture-verification.json` — raw notebook output.
- `phase4-architecture-verification.md` — readable verdict + the exact
  Phase 5 requirements.
- `phase4-provenance-manifest.json` — SHA-256, source path, Colab environment.
- `notebooks/phase4-nllb-architecture-verification.ipynb` — the notebook.

