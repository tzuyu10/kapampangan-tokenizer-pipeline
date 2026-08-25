# Expanded morphology v4

This isolated local experiment adds linguistically evidenced Kapampangan
affixes and morphophonological processes that are missing from the Table 1
baseline (`src/kapampangan_morphbpe/constants.py`,
`src/kapampangan_morphbpe/morphology.py`), without touching that baseline or
any existing artifact. It does **not** add new roots: the root/host inventory
is reused byte-for-byte from
`experiments/source_adjudicated_v2/resources/training-lexicon.json`. Only the
rule set changes.

See `EVIDENCE.md` for the full page-level provenance behind every accepted
rule and for the list of rejected/deferred items (`paki-...-an`, `-in`, the
`-ng` linker, Tagalog `pinaka-`, and several documented-but-not-productive
tense/vowel alternations). See `reports/audit.md` for the measured rule
counts, newly analyzed forms, and ambiguous forms from resegmenting the
complete 143,529-word-type preserved training inventory.

## What changed vs. Table 1

New prefixes: `m-`, the `maN-` actor prefix with nasal place assimilation
(`man-`/`mam-`/`mang-`, plus their `men-`/`mem-`/`meng-` aspect twins, plus
the dental `-y-` irregular subclass `many-`/`meny-`), `maki-`/`meki-`,
`makipag-`, `paki-`, `peka-`, `mi-`, `magpa-`/`migpa-`/`megpa-`,
`magka-`/`migka-`/`megka-`, `magpaka-`/`migpaka-`/`megpaka-`, and the `paN-`
nominalizer (`pan-`/`pam-`/`pang-`/`panga-` used standalone, not only inside
the existing `pang-...-an` circumfix -- and, uniquely, **compositional**: it
can attach over an already `mag-`/`ma-`-prefixed stem, e.g.
`pam- + (mag- + aral)` = `pamagaral`).

New circumfixes: `mi-...-an` (stative), `pi-...-an` (locative), `pag-...-an`
(goal focus, no nasal assimilation).

New suffixes: `-en` and `-anan`, plus a general vowel-hiatus/`w`-insertion
allomorphy rule shared by `-an`/`-en`/`-anan` (a vowel-final root drops the
suffix's own leading vowel, surfacing as a bare `-n`/`-nan`; an `i`/`u`-final
root inserts `w`).

New morphophonology: CV-/V-reduplication for the continuing/progressive
aspect (with the documented medial `d->r` alternation), and `ka-` + full-root
reduplication for the recent-completive aspect.

Analysis is recursive/compositional for exactly the two rule families where
the evidence shows it (the `paN-` nominalizer, and reduplication wrapping an
already-affixed stem); every other rule keeps the original one-level
exact-root validation. Every accepted analysis carries both the lossless
surface segments (used for BPE training boundaries) and the underlying
morpheme labels (for diagnostics), so
`misamban` -> surface `mi + samba + n`, underlying `mi- + samba + -an`.

## Reproduce

```powershell
.\.venv\Scripts\python.exe .\experiments\expanded_morphology_v4\run_experiment.py prepare
.\.venv\Scripts\python.exe .\experiments\expanded_morphology_v4\run_experiment.py train
.\.venv\Scripts\python.exe .\experiments\expanded_morphology_v4\run_experiment.py validate
```

or all three in one call: `... run_experiment.py all`.

`prepare` verifies the reused v2 lexicon/prepared-stream hashes, resegments
every one of the 143,529 preserved word types with the expanded analyzer,
asserts exact surface/kind/frequency parity with the v2 stream (only
boundaries may change), and writes `runs/prepared/training-stream.jsonl`
(morphology-protected) and `runs/prepared/plain-training-stream.jsonl` (all
boundaries cleared) plus `reports/audit.json`/`reports/audit.md`.

`train` trains a `plain` `ConstrainedBPETrainer` control plus a **weighted
MorphBPE penalty grid** (1/2/4/8, reusing `WeightedMorphBPETrainer` from
`weighted_morphbpe_v3` unmodified, just pointed at v4's own resegmented
stream instead of v2's) at 6,080/8,192/16,384 -- the same targets, special
tokens, and BPE tie-breaking as every other experiment in this repository.
Each condition is built twice in memory and re-exported to prove
byte-identical determinism, with zero protected-boundary merge violations,
and every existing artifact (canonical, v1, v2, boundary-safe-v1,
weighted-v3, vocab-ablation-v1) is asserted hash-identical before and after.

This replaced an earlier flat, unweighted `morphbpe` condition
(`ConstrainedBPETrainer` respecting boundaries but not penalizing them). That
approach only rejects a crossing merge for the one occurrence where it
crosses a boundary -- a pair that straddles a boundary in one word can still
be learned wholesale from every *other* unprotected occurrence elsewhere in
the corpus, and standard runtime (which has no memory of which occurrence
was protected during training) will then reapply it inside the protected
word too. The weighted score instead demotes a pair's *global* rank by its
total crossing frequency across the whole corpus, the same mechanism
`weighted_morphbpe_v3` already validated for `v2`'s boundary set.

`validate` reloads every artifact, checksums it, round-trips diagnostic words
(`misamban`, `kabukasan`, `sinulat`) through standard runtime, and scores
boundary precision/recall/F1, fertility, and **Morphological Consistency
F1-Score (MCF1)** against the resegmentation audit / morphology index as a
**training-derived silver diagnostic**, not independent gold.

### Morphological Consistency F1-Score (MCF1)

The thesis proposal (Data Analysis, adapted from the MorphBPE evaluation
framework of Asgari et al. 2025) defines a third tokenizer-level metric
alongside Fertility Rate and Morpheme Boundary F1: "whether words that share
morphemes are assigned shared tokens and whether shared tokens correspond to
shared morphemes." Neither source gives an exact algorithm, so
`_morphological_consistency_f1` in `run_experiment.py` is one explicit,
documented operationalization over the accepted words in
`runs/segmentations/morphology-index.jsonl` (every accepted/protected word's
structured `(kind, underlying-label)` morphemes, written by `prepare`):

- Two words *share a morpheme* if their analyses contain the same
  `(kind, underlying-label)` pair (a protected root/compound counts as its
  own single morpheme, so standalone `samba` matches the `samba` morpheme
  inside `misamban`).
- Two words *share a token* if their standard-runtime encodings contain at
  least one identical piece of length >= 2 (single characters are excluded
  as trivially frequent noise).
- TP = pairs that share both a morpheme and a token; FN = morpheme-sharing
  pairs with no shared token (inconsistent representation); FP =
  token-sharing pairs with no shared morpheme (a spurious/accidental match).
  `precision = TP/(TP+FP)`, `recall = TP/(TP+FN)`, `F1` the harmonic mean.
- Very large morpheme/token groups are capped to a deterministic prefix
  (300 members) to keep pairwise enumeration tractable; this under-counts
  rather than over-counts, so treat the score as an estimate.

At every trained vocabulary size MCF1 rises monotonically with the crossing
penalty, tracking boundary F1's own trend (see `AGENT_CONTEXT.md` for the
full table), e.g. at 8,192: plain 0.1414 -> penalty 1 0.1788 -> penalty 2
0.1989 -> penalty 4 0.2168 -> penalty 8 0.2600.

## Compare

Activate the project virtual environment, then supply vocabulary size,
crossing penalty (1, 2, 4, or 8), and optional quoted text -- same shape as
`v3prop`:

```powershell
v4prop 8k 1 "misamban"
v4prop 8k 4 "Sumulat ako ng tula"
v4prop 16k 8 "Misamban la ing tau."
v4prop 8k 4 "pekamaragul"
```

Both sides use ordinary lexicon-free BPE inference; `v4prop`'s
`lexicon_used_at_runtime` is always `false`. Morphology only biases which
merges get learned during training -- it does **not** guarantee an exact
boundary at inference time for an unseen or already-merged word. Higher
penalties more strongly suppress corpus-wide merges that conflict with a
protected boundary anywhere in the corpus, which can (not always -- this is
an empirical, per-word, per-penalty, per-size question, not a guarantee)
flip a word from the Plain-BPE-identical split to the morphologically
aligned one. See `reports/runtime-evaluation.json` for the measured effect
across the full penalty grid.

Every `v4prop` call also prints all three of the thesis's tokenizer-level
metrics for Plain BPE vs. the selected penalty at that vocabulary size:
Fertility Rate is computed live from the sentence you typed (the
`fertility morph X plain Y` line); Morpheme Boundary F1 and MCF1 are
corpus-wide aggregates read from `reports/runtime-evaluation.json` (cached by
`validate`, not recomputed per call), each printed with an explicit
disclaimer that they describe the corpus, not your specific input, and that
their "gold" is this experiment's own rule-derived audit, not
independent/human-annotated gold. Example:

```
Sumulat ako ng tula.
  MorphBPE  6 | S + um + ulat | ako | ng | tula
  Plain BPE 5 | Sum + ulat | ako | ng | tula
              | fertility morph 1.50 plain 1.25
  corpus-wide silver diagnostics (vocab 8k; computed once by `validate`, cached in reports/runtime-evaluation.json, not recomputed for this call):
    morpheme boundary F1 -- precision/recall of the tokenizer's predicted merge boundaries against this experiment's own rule-derived boundaries (the resegmentation audit). Those 'gold' boundaries come from the same morphological segmenter that also biases training, so this is a silver self-consistency check, not independent/human-annotated gold, and it does not evaluate the sentence you typed -- only the fixed audit word list:
      Plain BPE   0.2325  (P 0.3029 R 0.1887)
      MorphBPE p4 0.5867  (P 0.5591 R 0.6172)
                  delta +0.3542 (+152.3%)
    morphological consistency F1 (MCF1) -- whether words sharing a morpheme get shared tokens, and shared tokens correspond to shared morphemes, measured as word-pair precision/recall over this experiment's own morpheme labels (very large morpheme/token groups are capped to a deterministic sample). Not independent gold, and not specific to the sentence you typed -- it summarizes every analyzed word in the corpus:
      Plain BPE   0.1414  (P 0.1481 R 0.1352)
      MorphBPE p4 0.2168  (P 0.2006 R 0.2358)
                  delta +0.0754 (+53.4%)
```

If `validate` has not been run yet (no cached report), this whole block is
silently omitted rather than failing the primary token comparison.

## All conditions in one call: the `allprop` command

For checking a word or sentence against every condition at once -- NLLB-200,
the Unigram ablation, Plain BPE, MorphBPE penalty-4, and both stochastic-
dropout conditions -- `allprop` is an installed console command:

```powershell
allprop 8k "Sumulat ako ng tula."
allprop 6k "misamban"
```

`allprop <6k|8k|16k> ["text or sentence"]` (omitted text defaults to
`misamban`). No retraining happens when you run it -- it only loads
artifacts that already exist on disk (fetched/trained by the scripts
described above) and encodes your text with each. Requires everything
`nllbprop` and `stochprop` each need (the `nllb-baseline` extra, the NLLB
tokenizer files, the trained Unigram ablation, and the trained stochastic
conditions); fails with a clear message listing exactly which artifact is
missing if any aren't present yet.

## Stochastic MorphBPE: train-time-only regularization

A new, explicitly-labeled MorphBPE extension --
`StochasticWeightedMorphBPETrainer`
(`src/kapampangan_morphbpe/stochastic_bpe.py`) -- adds train-time-only
stochastic dropout on top of `WeightedMorphBPETrainer`'s existing penalty
score: at merge-application time, each individual *allowed* (never
boundary-crossing -- that stays strictly forbidden, unchanged) occurrence
of the selected pair is independently skipped with probability
`dropout_rate`, so training is exposed to more than one greedy segmentation
path per word instead of committing to a single one -- similar in spirit
to BPE-dropout (Provilkov et al., 2020) and Unigram's own subword sampling,
but scoped to *this trainer's own vocabulary-construction process only*.
**The exported artifact is unaffected**: standard, fully deterministic,
lexicon-free greedy BPE inference, identical in kind to every other
condition here (`lexicon_used_at_runtime: false`). Only how the merge
table was learned differs. This is **not** the unmodified MorphBPE
algorithm from Asgari et al. (2025), nor a literal reproduction of
BPE-dropout or Unigram sampling -- it is a new thesis extension, same
spirit as `weighted_morphbpe_v3`/this experiment's own `penalty-*`.

Determinism is preserved by construction: dropout decisions come from a
seeded `random.Random(seed)`, consumed in a fixed, deterministic traversal
order (sorted sequence IDs, left-to-right within each sequence), so two
independent training runs with the same inputs/seed/dropout_rate produce
byte-identical results -- verified the same way every other trainer here
is (two in-memory builds compared for equality, plus a real
determinism-rebuild artifact comparison).

```powershell
python experiments/expanded_morphology_v4/train_stochastic_morphbpe.py
```

Trains at `crossing_penalty=4` (this experiment's own established
representative mid-grid choice) crossed with `dropout_rate` in `{0.1,
0.2}`, seed `20260822`, at all three vocabulary sizes, on the exact same
morphology-resegmented stream `penalty-*` already trains on. Artifacts land
at `artifacts/stochastic-p4-d<rate>/candidates/vocab-<size>` (same shape as
every other condition here); reports at
`reports/stochastic-morphbpe-training-report.json` and
`reports/stochastic-morphbpe-runtime-evaluation.json` (boundary F1/MCF1,
computed by reusing `run_experiment.py`'s own metric functions directly --
this trainer produces a real artifact through the same
`export_tokenizer_artifact`/`RuntimeTokenizer` pipeline as `plain`/
`penalty-*`, unlike the Unigram ablation, which needed its own parallel
implementation).

**A real bug was caught training on the full corpus, not the unit tests**:
an early version of the merge-application code treated *any* protected-
position match of a selected "allowed" pair as a fatal error. That's wrong
-- the same `(left, right)` pair can legitimately occur at one allowed
position and one protected position within the *same* word (e.g. `abcab`
with a boundary at position 4: the pair `(a,b)` is allowed at positions
0-1 but crosses the boundary at positions 3-4), and the correct behavior
(matching `weighted_bpe.py`'s own `_apply_allowed_pair`) is to silently
leave the protected occurrence unmerged, not raise. This never surfaced in
small synthetic test corpora -- only the real ~3.18M-occurrence corpus hit
it. Fixed, and locked in with a permanent regression test
(`test_same_pair_allowed_at_one_position_and_protected_at_another_in_one_word`
in `tests/test_stochastic_bpe.py`).

**Result: a clean, consistent win on both corpus-wide silver metrics, at
every vocabulary size** (bF1 = boundary F1 vs. the resegmentation audit;
MCF1 = Morphological Consistency F1; both against penalty-4, the
condition being extended):

| vocab | condition | boundary F1 | MCF1 | fertility |
|---|---|---|---|---|
| 6,080 | penalty-4 | 0.5722 | 0.2049 | 2.4283 |
| 6,080 | +dropout 0.1 | 0.5989 (+4.7%) | 0.2153 (+5.1%) | 2.5139 |
| 6,080 | +dropout 0.2 | 0.6255 (+9.3%) | 0.2159 (+5.4%) | 2.5255 |
| 8,192 | penalty-4 | 0.5867 | 0.2168 | 2.3392 |
| 8,192 | +dropout 0.1 | 0.6076 (+3.6%) | 0.2302 (+6.2%) | 2.4378 |
| 8,192 | +dropout 0.2 | 0.6395 (+9.0%) | 0.2308 (+6.5%) | 2.4354 |
| 16,384 | penalty-4 | 0.6092 | 0.2332 | 2.1854 |
| 16,384 | +dropout 0.1 | 0.6333 (+4.0%) | 0.2519 (+8.0%) | 2.2628 |
| 16,384 | +dropout 0.2 | 0.6599 (+8.3%) | 0.2536 (+8.8%) | 2.2787 |

**But not a free lunch at the word level -- check individual words, not
just the aggregate**: `misamban` improves at dropout 0.2 (`mi + sam + ban`,
no longer forming the boundary-crossing `mis`, matching the partial
improvement previously only seen at penalty-8 in the plain weighted grid)
and `kabukasan`/`Dumalan` stay stable (`ka + bukas + an`, `D + um + alan`
at every dropout rate) -- but `Sumulat` **regresses** from the
morphologically correct `S + um + ulat` at plain penalty-4 to
`Su + mu + lat` (losing the `-um-` infix) at *both* dropout 0.1 and 0.2.
This is the same kind of word-specific regression already documented for
the plain penalty grid at penalty-8 (see "Verified" section below) --
aggregate improvement across the corpus does not mean every word improves,
and this is an empirical, per-word question, not a guarantee. No
dropout_rate, penalty, or vocabulary size is selected.

### Ad hoc comparisons: the `stochprop` command

For checking an arbitrary word or sentence interactively, `stochprop` is an
installed console command with the same shape as `v4prop`/`v3prop`:

```powershell
stochprop 8k 0.2 "Sumulat ako ng tula."
stochprop 6k 0.1 "misamban"
```

`stochprop <6k|8k|16k> <0.1|0.2> ["text or sentence"]` (omitted text
defaults to `misamban`). Prints Plain BPE, MorphBPE penalty-4, and the
stochastic-dropout condition side by side with word-token counts, grouped
pieces, and fertility, then (once `train_stochastic_morphbpe.py` has been
run) the same corpus-wide boundary-F1/MCF1 diagnostic block `v4prop`/
`nllbprop` already print, degrading silently if that report isn't present
yet. Example:

```
Sumulat ako ng tula.
  Plain BPE       5 | Sum + ulat | ako | ng | tula
  MorphBPE p4     6 | S + um + ulat | ako | ng | tula
  Stochastic d0.2 6 | Su + mu + lat | ako | ng | tula
                    | fertility Plain BPE 1.25  MorphBPE p4 1.50  Stochastic d0.2 1.50
```

This is the concrete word-level illustration from the section above:
MorphBPE p4 gets the `-um-` infix right, the stochastic condition doesn't,
even though the stochastic condition wins on both corpus-wide metrics --
`stochprop`'s own printed diagnostic block makes that tension visible in
one call instead of requiring a separate report lookup.

## NLLB-200 baseline comparison (encode-time only)

Every comparison above (`v4prop`, and every `prop`/`comp`/`v2prop`/`v3prop`
elsewhere in this repository) is against a freshly-trained Plain-BPE control
on this project's own corpus. The thesis proposal's actual specified
baseline (Scope and Limitation, p.15; Statement of the Problem, p.13) is the
**pretrained native NLLB-200 tokenizer** -- a SentencePiece unigram-LM model,
a genuinely different algorithm from BPE, not just a different training
corpus. That comparison had never been built until this pass.

`nllb_baseline_report.py` is a batch report script covering a fixed set of
23 test items (3 sentences + a 20-word audit sample) at vocab 8,192 in one
run, producing a saved Markdown/JSON report. For ad hoc single-sentence
checks at any of the three vocabulary sizes, see the installed `nllbprop`
command further below instead. With the venv activated, to regenerate the
batch report:

```powershell
python experiments/expanded_morphology_v4/nllb_baseline_report.py
```

It fetches nothing itself; run this first (already done once for this
report -- see provenance below) to populate
`resources/nllb-tokenizer/` with **tokenizer files only** from
`facebook/nllb-200-distilled-600M`, restricted via `allow_patterns` so the
~2.4GB model weights are never pulled:

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="facebook/nllb-200-distilled-600M",
    revision="f8d333a098d19b4fd9a8b18f94170487ad3f821d",
    allow_patterns=["tokenizer.json", "tokenizer_config.json",
                    "special_tokens_map.json", "sentencepiece.bpe.model"],
    local_dir="experiments/expanded_morphology_v4/resources/nllb-tokenizer",
)
```

**Provenance:** `facebook/nllb-200-distilled-600M`, pinned to commit
`f8d333a098d19b4fd9a8b18f94170487ad3f821d`, license `CC-BY-NC-4.0`. Fetched
files and SHA-256: `tokenizer.json` (17,331,176 bytes,
`e316b82de11d0f951f370943b3c438311629547285129b0b81dadabd01bca665`),
`sentencepiece.bpe.model` (4,852,054 bytes,
`14bb8dfb35c0ffdea7bc01e56cea38b9e3d5efcdcb9c251d6b40538e1aab555a`),
`special_tokens_map.json` (3,548 bytes) and `tokenizer_config.json` (564
bytes) -- all recorded in `resources/nllb-tokenizer-manifest.json`
(regenerated by the script on every run; hashes are stable across runs
because the source revision is pinned). The raw downloaded tokenizer files
themselves are **not** committed to this repository (see `.gitignore`):
NLLB-200's CC-BY-NC-4.0 license makes redistribution rights the same open
question this project already treats the OCR source books with, so only the
small provenance manifest is tracked, and the files must be re-fetched
locally before re-running the script.

**Method:** the script loads the NLLB tokenizer via the `tokenizers`
library directly (`Tokenizer.from_file`, no `transformers`/`torch`
dependency), with its shipped post-processor disabled (it appends a
generic placeholder for the language-code special token that
`NllbTokenizerFast.src_lang` would normally resolve per-language; disabling
it isolates content subword pieces for a fair comparison). It then encodes
the same 3 fixed test sentences used throughout this project
(`misamban`, `Sumulat ako ng tula`, `Dumalan ka keni.`) plus a deterministic
20-word prefix of `runs/segmentations/resegmentation-audit.jsonl`, against
NLLB and against this experiment's own `plain` and `penalty-4` conditions at
vocab 8,192 (penalty-4 is a representative mid-grid choice for this report,
**not a selected configuration**). Fertility Rate uses this project's own
T/W formula for all three tokenizers; NLLB has no native pretokenizer
concept comparable to this project's word/whitespace/punctuation
pretokens, so its word attribution is approximated by character-offset
overlap against this project's own word-pretoken spans.

Output: `reports/nllb-baseline-comparison.json` (full data) and
`reports/nllb-baseline-comparison.md` (human-readable table).

**Result, and the confound that limits it:** averaged over the 23 test
items, NLLB's fertility (2.1558) is lower than the local conditions'
(Plain BPE 2.5906, MorphBPE penalty-4 2.7029). NLLB's vocabulary (256,204
entries) is over 30x this project's local vocabulary (8,192) -- vocabulary
size alone strongly drives fertility regardless of morphological alignment,
so **this result must not be read as NLLB segmenting Kapampangan "better"**;
the two effects are confounded and this report does not isolate them by
itself (see the Unigram ablation below, which does). Piece strings are
never byte-identical across NLLB and any local condition (0/23), which is
expected and not informative on its own: NLLB draws from a disjoint, much
larger vocabulary with a different whitespace convention (`▁` prefix vs.
this project's literal space pieces), so exact string agreement was never a
meaningful signal here. This is an encode-time-only, tokenizer-level
comparison; NLLB-200's tokenizer is not retrained on this corpus, and this
is not a substitute for the downstream BLEU/chrF++ translation evaluation
against real NLLB-200 inference, which remains a separate, already-tracked,
much larger blocker (parallel-data gap; see `AGENT_CONTEXT.md`).

### Isolating the algorithm effect: matched-vocabulary Unigram-LM ablation

The native-NLLB comparison above confounds two things: NLLB uses a
different subword *algorithm* (Unigram-LM, via SentencePiece) than this
project's Plain-BPE/MorphBPE (BPE), **and** a much larger vocabulary trained
on ~200 other languages, not Kapampangan. `train_unigram_ablation.py`
isolates the first variable: it trains a **fresh** Unigram-LM tokenizer
(via the already-installed `tokenizers` library's `UnigramTrainer`, not the
separate `sentencepiece` package) on this project's own corpus
(`runs/prepared/plain-training-stream.jsonl` -- the exact same stream
Plain-BPE trains on), at the exact same vocabulary size (8,192), with the
same special tokens and character inventory. **This is not NLLB's
tokenizer** -- SentencePiece/Unigram models can't be fine-tuned, only
trained from scratch, so this is a new, separate artifact under
`artifacts/unigram-ablation/vocab-8192/`, clearly labeled as an ablation
everywhere it's referenced. With the venv activated:

```powershell
python experiments/expanded_morphology_v4/train_unigram_ablation.py
python experiments/expanded_morphology_v4/nllb_baseline_report.py
```

`nllb_baseline_report.py` was extended to include this condition as a
fourth column in the same comparison table and JSON report.

**Known limitation, disclosed rather than hidden:** unlike every other
artifact in this repository, this ablation's training is not verified
byte-reproducible. Two independent training runs on identical input --
including single-threaded (`RAYON_NUM_THREADS=1`, to rule out thread
scheduling) -- produced different `tokenizer.json` content. This is a
characteristic of the third-party `tokenizers`-library Unigram/EM trainer,
not of this project's own deterministic BPE trainers (which use explicit,
code-reviewed tie-breaking rules). The frozen artifact here is one specific
trained instance, fingerprinted in
`artifacts/unigram-ablation/vocab-8192/unigram-ablation-manifest.json`;
re-running the training script will very likely produce a similar but not
byte-identical tokenizer. Given this is an illustrative ablation, not a
primary/selected artifact, this is an accepted, disclosed limitation rather
than a blocker.

**Result:** average fertility -- NLLB (native, 256,204 vocab) 2.1558,
**Unigram ablation (matched 8,192 vocab, this corpus) 2.5145**, Plain BPE
(8,192) 2.5906, MorphBPE penalty-4 (8,192) 2.7029. The Unigram ablation
sits close to Plain BPE/MorphBPE and far above NLLB, despite sharing NLLB's
algorithm family. This points to vocabulary size and multilingual corpus
exposure -- not the Unigram-LM algorithm itself -- as the dominant driver
of NLLB's lower fertility in the native comparison above. In other words:
training NLLB's *algorithm* (not NLLB itself) on Kapampangan at a
Kapampangan-appropriate vocabulary size does **not** reproduce NLLB's
fertility advantage, so that advantage should not be attributed to Unigram
being inherently better suited to Kapampangan morphology than BPE.

### Ad hoc comparisons: the `nllbprop` command

For checking an arbitrary word or sentence interactively -- rather than
re-running the fixed 23-item batch report above -- `nllbprop` is an
installed console command with the same shape as `v4prop`/`v3prop`:

```powershell
nllbprop 8k 4 "Sumulat ako ng tula."
nllbprop 6k 1 "misamban"
nllbprop 16k 8 "Dumalan ka keni."
```

`nllbprop <6k|8k|16k> <1|2|4|8> ["text or sentence"]` (omitted text defaults
to `misamban`, matching `v4prop`). It prints all four conditions --
NLLB-200, the Unigram ablation, Plain BPE, and MorphBPE at the given
penalty -- with word-token counts, grouped pieces, and fertility, plus a
one-line reminder that NLLB is encode-time-only and the ablation is not
NLLB's own tokenizer. Example:

```
Sumulat ako ng tula.
  NLLB-200     5 | ▁Sum + ulat + ▁ako + ▁ng + ▁tula
  Unigram-abl. 6 | Sumul + at | a + ko | ng | tula
  Plain BPE    5 | Sum + ulat | ako | ng | tula
  MorphBPE p4  6 | S + um + ulat | ako | ng | tula
               | fertility NLLB-200 1.25  Unigram-abl. 1.50  Plain BPE 1.25  MorphBPE p4 1.50
```

Requires the `nllb-baseline` optional extra (`uv pip install -e
".[nllb-baseline]"`), the NLLB tokenizer files fetched into
`resources/nllb-tokenizer/`, and the Unigram ablation trained at all three
sizes (`python train_unigram_ablation.py`, which now loops over
6,080/8,192/16,384 -- matching `v4prop`'s size choices exactly). Fails with
a clear message (not a bare traceback) if the `tokenizers`/`huggingface_hub`
packages aren't installed; every other installed command (`prop`, `comp`,
`v4prop`, etc.) is unaffected either way, since the import is local to
`nllbprop` alone, not a package-wide dependency.

If `evaluate_unigram_ablation.py` (below) has already been run, `nllbprop`
also prints its cached corpus-wide boundary-F1/MCF1 block for Plain BPE vs.
the selected penalty vs. the Unigram ablation, exactly like `v4prop` already
does for its own two conditions -- degrading silently if that report isn't
present yet.

### Is the Unigram ablation actually more morphologically accurate? Check, don't eyeball

A few hand-tried sentences can look like the Unigram ablation finds cleaner
morpheme boundaries than MorphBPE (e.g. `Makisamba` -> Unigram correctly
isolates `Maki + samba`; both BPE conditions wrongly split `Mak + is +
amba`, the same "unprotected merge outranks the penalty for this specific
word" failure mode already documented for `misamban` itself). But `Sumulat`/
`Dumalan` show the opposite: MorphBPE correctly isolates the `-um-` infix,
Unigram does not. Three sentences is not a corpus-wide answer either way.

`evaluate_unigram_ablation.py` computes the exact same boundary-F1 and MCF1
silver diagnostics `run_experiment.py validate()` already computes for
Plain BPE/MorphBPE, but for the Unigram ablation too, against the same
resegmentation audit and morphology index (read-only; writes its own
separate report, does not touch `run_experiment.py`'s files):

```powershell
python experiments/expanded_morphology_v4/evaluate_unigram_ablation.py
```

Output: `reports/unigram-ablation-boundary-metrics.json`/`.md`.

**Result:** the two metrics tell different stories. On **boundary F1**
(exact protected-position match), MorphBPE wins decisively and
increasingly with penalty at every vocabulary size -- e.g. at 8,192:
Unigram ablation 0.4363 vs. plain 0.2325, penalty 1/2/4/8 =
0.4470/0.5065/0.5867/0.7023. So the corpus-wide picture does **not**
support "Unigram is generally more accurate than MorphBPE" -- the
`Makisamba`-style examples are best explained by MorphBPE's own documented
failure mode hitting those specific words, not a general Unigram advantage.
(The Unigram ablation's boundary *precision* is actually higher than
MorphBPE's at every penalty except 8 -- it just has much lower *recall*,
consistent with keeping fewer, larger pieces overall.) On **MCF1** (does a
shared morpheme get a shared token, corpus-wide -- arguably a more
generalization-oriented measure than exact boundary position), the Unigram
ablation is genuinely competitive with, and sometimes beats, MorphBPE at
low-to-moderate penalties despite having zero morphological supervision --
e.g. at 8,192: Unigram 0.2199 vs. plain 0.1414, penalty 1/2/4 =
0.1788/0.1989/0.2168 (Unigram beats all three), only losing to penalty 8's
0.2600.

## Verified: why v4 moved from unweighted to weighted training

Before the weighted rebuild, a one-off unweighted `ConstrainedBPETrainer`
condition was trained on v4's own stream to check a specific claim: that
paper-aligned, boundary-*respecting* (not boundary-*penalizing*) training
looks a lot like Plain BPE at standard runtime. At vocab 8,192, against the
resegmentation audit: boundary F1 was 0.3346 (constrained) vs. 0.2962
(plain) -- only a ~13% relative improvement -- and the constrained tokenizer
produced **byte-identical pieces to Plain BPE on 71.7% of audit words**
(4,230 / 5,897). That's the concrete evidence behind moving to the weighted
penalty score instead of only enforcing hard non-crossing during training.

## Known findings worth reading before citing this experiment

- A small number (well under 1%) of newly-introduced hypotheses in the first
  draft of this analyzer accidentally validated 1-2 letter noise entries
  already present in the *reused, unmodified* v2 lexicon (e.g. treating
  "San" as "Sa" + "n"). This is now guarded by a minimum reconstructed-root
  length of 3, matching `source_adjudicated_v2`'s own stated policy of
  holding "roots shorter than three letters" -- see `EVIDENCE.md`'s
  "Known interaction risk" section and
  `test_hiatus_collapse_does_not_validate_short_noisy_roots`.
- Resegmenting the full inventory occasionally changes a v2 boundary that a
  narrower, incrementally-updated v2 stream had not yet revisited (for
  example, a handful of words are now correctly resolved as an exact
  protected root under the *same* v2 lexicon that v2's own stream had not
  re-derived). A larger share of changed rows are new genuine ambiguity: once
  more rule families exist, more than one can validly compete for the same
  word, and this analyzer preserves that ambiguity rather than guessing.
