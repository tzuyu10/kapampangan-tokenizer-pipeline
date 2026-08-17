# Limitations

- The lexicon and morphology references are provisional and not
  native-speaker/linguist adjudicated; validation morphology scores are proxies.
- Only 2.84% of training word occurrences receive accepted multi-segment proxy
  analyses; roots/compounds are additionally protected, but coverage is not a
  measure of linguistic completeness.
- The immutable corpus contains substantial multiscript and OCR-derived
  material, producing a 1,588-character base inventory and an unusually high
  1,592-unit initial vocabulary. This materially shaped the smallest candidate.
- NFC is the sole normalization. No safe reviewed spelling-variant map was
  available, so the paper's broader normalization idea remains unsatisfied.
- Validation proxy boundaries can be crossed at runtime on unseen forms because
  runtime correctly has no lexicon. Training-protected boundaries were never
  crossed.
- Runtime offsets address normalized code points, not original pre-NFC indices
  or UTF-8 bytes. Unknown characters decode to U+FFFD.
- The candidate grid contains only three deterministic data-derived sizes; it
  is not an exhaustive hyperparameter search.
- The 45 Tagalog-labeled parallel rows do not satisfy the paper's Filipino data
  requirement and are unsafe for this goal's smoke fixtures.
- No native NLLB tokenizer baseline, held-out tokenizer evaluation, BLEU,
  chrF++, formal hypothesis test, NLLB model download, or fine-tuning occurred.
- Public redistribution rights for all corpus sources and generated artifacts
  have not been established; outputs are local experimental research assets.

These limitations do not block technical tokenizer training and artifact
loading. They block formal linguistic, comparative, translation, and thesis
claims until the requirements in `docs/EVIDENCE_LIMITATIONS.md` and
`docs/NLLB_READINESS_REPORT.md` are satisfied.

