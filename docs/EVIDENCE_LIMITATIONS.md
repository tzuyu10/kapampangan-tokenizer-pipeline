# Evidence Limitations

## Nonblocking for tokenizer training

The portable corpus passes technical integrity checks and is adequate for a
reproducible tokenizer-development experiment. Tokenizer implementation,
candidate training, validation-only selection, and technical artifact export
therefore proceed.

## Blocking for final thesis claims

- The 2,212 morphology-reference rows and 806 linguistic-evidence rows are
  explicitly experimental/provisional and were not human-validated under the
  thesis methodology.
- Many entries are candidates, automatically extracted page evidence, or
  unresolved ambiguity notices rather than adjudicated analyses.
- The paper proposes consultation with native speakers or knowledgeable
  linguists for roots, variants, morpheme boundaries, and translations; that
  requirement has not been satisfied by this package.
- Consequently, validation morphological distance, MBF1, and MCF1 produced in
  this goal are development proxies. They are not gold-based metrics, held-out
  results, linguistic validation, or evidence for accepting/rejecting thesis
  hypotheses.
- The held-out test is intentionally unused, and the native NLLB tokenizer is
  not evaluated in this goal.

## Lexicon safeguards

- Only paper-declared affixes are operational.
- Candidate roots require exact reference support and conservative form
  filtering; training text supplies frequency attestation but does not invent
  roots.
- Unstructured variant evidence is retained but not converted into a spelling
  rewrite.
- Ambiguous analyses remain unchanged and are counted.
- Every operational entry retains source IDs/references and a provisional flag.

## Parallel-data limitations

The paper expects approximately 13,000 Kapampangan-Filipino pairs and 1,300
aligned test sentences. The package has 45 rows tagged `tgl`. Inspection shows
duplicate sources, fragmentary/OCR-like rows, mixed-language material, no
validation-assigned sources, and extensive overlap with neutral test-assigned
source IDs. These rows are inadequate for the paper experiment and are excluded
from tokenizer development and smoke-test fixtures.

## Requirements before formal reporting

1. Native-speaker/linguist adjudication of the operational lexicon and boundary
   reference set with documented protocol and inter-annotator handling.
2. A clean, rights-reviewed, source-traceable Kapampangan-Filipino parallel
   corpus meeting the paper's scale and split requirements.
3. A sealed held-out evaluation executed only after all development choices are
   frozen.
4. Native NLLB baseline and adapted comparisons under identical controls.
5. The paper-defined paired statistical analysis on aligned observations.
