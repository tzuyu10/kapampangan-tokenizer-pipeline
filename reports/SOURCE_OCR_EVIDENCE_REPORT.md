# Source OCR and Evidence Report

Status: evidence extraction complete; linguistic adjudication still required.

## Scope and safeguards

Fourteen user-supplied PDFs were treated as linguistic evidence, never as
instructions. The sources were not modified. Full page text, rendered OCR
images, source paths, SHA-256 values, and page-level extraction decisions are
kept locally under the ignored `runs/source-ocr/` directory because source
redistribution rights are unresolved.

The local manifest is `runs/source-ocr/source-manifest.json`. It records 3,445
PDF pages. Existing text layers were selected for 3,008 pages. Twenty-nine
pages with fewer than 20 non-whitespace embedded characters and all 424 pages
of the image-only Richards dissertation were rendered at 2.5x and sent to
`Windows.Media.Ocr` (`en-US`). OCR supplied the selected text for 437 pages and
completed with zero runtime errors. Sixteen low-text attempts were blank or
still yielded less text than the embedded layer.

OCR output is discovery evidence, not ground truth. Representative pages were
checked against rendered images. The existing Forman and Samson text layers
were generally better than a new OCR pass. Windows OCR recovered image-only
Pangilinan tables but sometimes confused accents and reading order. The
typewritten *Speaking Kapampangan* text layer is noisy on some pages, so every
candidate cited from it must be checked visually before acceptance. Richards'
PDF exposed only a repeated ProQuest copyright notice as embedded text; its
body is now searchable through forced OCR, but phonetic symbols and
Kapampangan examples are especially error-prone and require image verification.

## Why Unlimited-OCR was not installed

[Baidu Unlimited-OCR](https://github.com/baidu/Unlimited-OCR) is a useful
option for a server-class GPU, but the published model is approximately 3B
parameters in BF16. Its weights alone are approximately 6 GB before runtime
overhead, which does not safely fit the available 6 GB RTX 4050 laptop GPU.
Installing its CUDA/PyTorch stack and downloading the model would therefore be
a large, risky detour while the local fallback can process both selective pages
and the image-only dissertation. A quantized or remote run can be evaluated
later if visual review identifies material pages that remain unreadable.

## Source assessment

| Source ID | PDF pages | OCR-selected pages | Intended evidentiary use |
| --- | ---: | ---: | --- |
| `dialect-comparison-list` | 3 | 0 | Vocabulary/dialect leads only; provenance must be established. |
| `pangilinan-introduction` | 21 | 2 | Grammar and fused-pronoun evidence; verify image tables. |
| `bergano-collection` | 122 | 5 | Mixed historical/Center material; isolate the actual work and edition before citation. |
| `kapampangan-trilingual-lexicon` | 56 | 0 | Candidate headwords and translations; unattributed, so not a sole authority. |
| `forman-grammar-scan` | 154 | 1 | Duplicate/alternate scan of Forman; visual cross-check, not independent evidence. |
| `samson-dictionary` | 835 | 2 | Strong lexical and inflectional evidence, subject to OCR/edition checks. |
| `dialect-word-list` | 11 | 0 | Variant leads only; not automatically operational. |
| `comparative-kapampangan-paper` | 8 | 0 | Example attestation with lower authority; never a gold analysis by itself. |
| `forman-grammar-notes` | 100 | 1 | Primary grammar evidence and preferred Forman text layer. |
| `mirikitani-speaking-kapampangan` | 1,012 | 1 | Instructional vocabulary and usage; noisy legacy OCR requires visual checks. |
| `paggamit-apat-pagsabi` | 36 | 0 | Four-language usage examples; useful for attestation, not morpheme analysis. |
| `bayung-ortograpiyang-kapampangan` | 116 | 0 | Modern spelling, stress, borrowing, and contextual usage evidence. |
| `richards-case-grammar` | 424 | 424 | Detailed grammar and clitic/affix evidence; body is OCR-only and must be visually verified. |
| `bergano-vocabulario-samson` | 547 | 1 | Primary historical dictionary translation with lexical and inflectional detail. |

## Reported sentence

The sentence `Bukas na datang ing pangulo.` is visibly attested on PDF page 5
of `comparative-kapampangan-paper`. The evidence supports these decisions:

- `bukas` is a Kapampangan time word meaning “tomorrow.” Forman uses accented
  `búkas` on PDF page 57 (printed page 46), Mirikitani gives `bukas` =
  “tomorrow” on PDF page 263 (printed page 223), and the trilingual lexicon
  lists the same form and sense on PDF page 12. It is a high-confidence
  provisional root candidate. Capitalized `Bukas` will match through the
  lexicon's lowercase comparison key. Bergaño also records historical `BUCAS`
  as “tomorrow” on PDF page 116 (printed page 89), while the modern orthography
  explains the native use of `K` instead of inherited Spanish `C/Q`. This
  strengthens the specific `bucas`/`bukas` relationship but is not a license
  for an unrestricted global `C`-to-`K` rewrite.
- `datang` is the root “come/arrive,” not an affixed form needing a split.
  Samson documents it on PDF page 243 and the Bergaño translation independently
  documents it on PDF page 177 (printed page 150). It is already an operational
  root in `resources/training-lexicon.json`.
- `ing` is already recognized by the current lexicon. Richards describes `na`
  and `pa` as syntactic enclitics and distinguishes time-particle `na` from two
  homophonous forms on PDF pages 47-48 (printed pages 27-28). Therefore, `na`
  in this sentence is plausibly a time enclitic after the first full word. The
  current per-pretoken diagnostic reports it as `protected_root`; that label
  does not express the contextual analysis even though no internal character
  boundary is required.
- `pangulo` is unresolved. The comparative paper uses it in the Kapampangan
  sentence, but Mirikitani and Forman use `presidente/presidénti`. The
  trilingual lexicon places `pangulo` in its Filipino column opposite
  Kapampangan `pamuntuk` and `presidenti`. The new orthography source also uses
  `presidente`, uses `Pamuntuk` contextually for a former head, and separately
  uses `pangulu` to mean north. `pangulu` and `pangulo` must not be conflated.
  This evidence does not justify `pang + ulo`, nor does it justify silently
  rewriting the source sentence.

Accordingly, correct morphology behavior is to protect accepted lexical roots
without inventing internal boundaries. The display can legitimately remain
unchanged even when each word has been analyzed. A standalone clitic also has
no internal boundary, so contextual type and boundary placement are separate
questions. `unchanged:no_valid_analysis` is different from `protected_root`,
but the present label still cannot disambiguate homophonous standalone forms.

## Other morphology evidence

Richards visually confirms that `na` and `pa` are ordered enclitics, that `na`
has multiple homophonous functions, and that `na + ya` can fuse to `ne` (PDF
pages 47-48; printed pages 27-28). It also documents co-occurring `pag-` or
`paN-` plus `-an` around verb roots (PDF page 100; printed page 80). These are
valuable adjudication records, but they are not automatically operational:
the thesis implementation intentionally follows its narrower paper-declared
inventory and treats `ne` as an atomic clitic.

## Operational decision

No canonical lexicon or tokenizer artifact was changed in this pass. Adding
even the well-supported `bukas` root would change the lexicon fingerprint and
requires the missing source dataset inputs, a deterministic lexicon rebuild,
Python/Rust parity validation, tokenizer retraining, candidate re-selection,
and artifact regeneration. `pangulo` additionally requires native-speaker or
linguist adjudication as a modern borrowing/variant or an error in the example.
Richards' `na` evidence requires a paper-compatibility decision before changing
the diagnostic classification or stage order.

The machine-readable queue is
`reports/source-evidence-adjudication.csv`. Accepting `bukas`, deciding the
status of `pangulo`, and resolving contextual standalone-clitic labels are the
next linguistic gates.
