# Boundary-safe MorphBPE training extension

This isolated local-test experiment strengthens MorphBPE merge learning while
retaining ordinary, artifact-only BPE inference. It never loads a morphology
lexicon or segmentation list at runtime.

The source-adjudicated segmenter deterministically exports 4,914 accepted word
types as a provisional/silver measurement list. Only the five word types whose
boundaries changed relative to the canonical implementation are hard training
audits (`Bucasan`, `Kabukasan`, `kabukas`, `kabukasan`, and `pabukas`). Applying
all 2,634 automatic multi-morpheme analyses as simultaneous hard constraints
blocked common internal merges and degraded toward character tokenization, so
the broader list is not misrepresented as mutually consistent adjudicated gold.

For each proposed merge, the trainer simulates the learned merge order on the
five frozen forms. It defers a candidate when applying it at that rank would
cross an accepted boundary. The candidate may become eligible later after
earlier safe merges change the runtime symbolization. No synthetic morpheme
sequences or changed corpus frequencies are introduced.

This is a training extension, not an unmodified replication of the MorphBPE
paper. Its hard guarantee is limited to the frozen source-adjudicated boundary
changes and does not imply correct morphology for unseen words.

## Rebuild

From the repository root:

```powershell
& .\.venv\Scripts\python.exe `
  .\experiments\boundary_safe_v1\run_experiment.py all
```

Individual resumable stages are `freeze`, `train`, and `validate`. Generated
lists, reports, and artifacts remain ignored below this experiment directory.

## Completed artifacts

| Vocabulary | Merges | Artifact fingerprint | Exact accepted types | Exact accepted occurrences | Hard-audit crossings |
|---:|---:|---|---:|---:|---:|
| 6,080 | 4,488 | `b531b199f71d04d867b1143830fc8e4da921897647865a21b4218eeb5247ff5f` | 1,153 / 4,914 | 487,817 / 536,972 | 0 / 5 |
| 8,192 | 6,600 | `51251b5e637459561d1d3f731ab9effe3303589852734b6030cd13ef9c344fc2` | 1,336 / 4,914 | 494,180 / 536,972 | 0 / 5 |
| 16,384 | 14,792 | `b7a2768e0a6b2f20f6bde9316264dc66b6d0ad2d0b25c8b6134b0a616167c29c` | 1,776 / 4,914 | 501,765 / 536,972 | 0 / 5 |

All three sizes produce `ka + bukas + an` for lowercase `kabukasan` and
`Ka + bukas + an` for title-case `Kabukasan` under standard runtime. Both
independent builds were byte-identical, artifact checksums passed, and existing
canonical, source-adjudicated, and Plain-BPE artifacts remained separate.

The exact-type columns measure one-token-per-segment agreement over the complete
rule-derived silver list. They are diagnostics, not independent evaluation
scores. Additional held-out human-adjudicated data is still required for thesis
evaluation and model selection.

## Compare with `prop2`

Activate the repository virtual environment, then run:

```powershell
prop2 6k "kabukasan"
prop2 8k "kabukasan"
prop2 16k "kabukasan"
```

The text argument is optional and defaults to `kabukasan`. A quoted sentence is
also accepted:

```powershell
prop2 8k "Bukas na datang ing pangulo."
```

`prop2` compares against the matched Plain-BPE artifact and reports that both
sides use standard lexicon-free runtime. Use `prop` for the unmodified
paper-training comparison and `comp` only for the runtime-constrained diagnostic.
All three shortcuts use the compact token-count, word-piece, and fertility
display. The explicit `kapampangan-morphbpe compare-tokenizers` interface keeps
the full JSON diagnostics for programmatic or reproducibility workflows.
