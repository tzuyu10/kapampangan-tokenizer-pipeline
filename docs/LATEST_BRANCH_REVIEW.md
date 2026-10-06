# Latest/WebAppFull review

Reviewed 2026-10-06, HEAD d15df33. Local tip matches the recorded origin/Latest/WebAppFull tip; no network fetch performed. Branch includes 1,047 tracked files, compared with the earlier app-only branch. Only pre-review untracked file: webapp/backend/tokenizer/morphology_display.json. Checkpoints and local environments remain ignored.

## Findings

1. **Incorrect root/affix coloring:** SegmentationProcess.jsx lines 7-19 calls the longest token root and all others affixes. For sinulat, the initial s and final ulat are root parts; longest-piece coloring misclassifies s. The morphology sidecar is untracked and not loaded by current trace_service.py. Retain reference-based span annotation rather than a length heuristic.
2. **A/B lacks matched-control gate:** translation_service.py status can_compare checks only readiness, and compare invokes conditions without dataset/config/target-tokenizer/split equivalence verification. Future mismatched bundles could appear to be a controlled experiment. Restore the saved-control audit and block incompatible comparisons.
3. **Unigram input contamination:** comparison_service.py groups_by_tokenizer reconstructs source surfaces from MorphBPE output. Unsupported characters become literal <unk> text, so Unigram does not receive the same original input. Preserve normalized original source units for all conditions.
4. **Preprocessing regression:** translation_service.py uses text.strip() while earlier training/serving normalization collapses internal whitespace. Show tokens also encodes unnormalized text. Repeated spaces, tabs and newlines can change IDs and split cache entries. Apply one shared normalization recipe for token display, translation and caching, matched to training.

## Checks

- Vite production build passed.
- Four current backend regression tests passed. These check process behavior and do not cover all findings above.
- GenerationTrace adds hooks and beam-search observations. Its version-specific model execution was not exercised with actual NLLB weights in this review.
- Fertility charts remain visible in Comparison.
- No new real-model inference, scientific evaluation or quality certification performed.

Review only: no application fixes, staging, commit or push performed. Project context updated as required. The full-source branch improves distribution scope, but is not equivalent to retaining every recent runtime/UI correction. Human-reference quality and manuscript weighted-versus-hard-constrained alignment remain separate unresolved scientific issues.
