# Expanded morphology v4 tokenizer (stochastic-p4-d0.1; 6,080)

Artifact fingerprint: `1bb5d4ab58f9920884fce038a501accb2799ac9bf2ae2c5bbdde0d05609a9a18`

Stochastic MorphBPE thesis extension (NOT the unmodified MorphBPE paper
algorithm, and NOT a literal reproduction of BPE-dropout or Unigram subword
sampling). Built on WeightedMorphBPETrainer's own scoring
(`allowed_frequency(p) - 4 * crossing_frequency(p)`,
summed globally across the v4-resegmented training corpus), plus train-time
-only stochastic dropout: each individual allowed (never boundary-crossing)
occurrence of the selected merge pair is skipped with probability
0.1 (seed 20260822), so the trained vocabulary is exposed to
more than one greedy segmentation path per word during training. A merge is
still never applied across a protected boundary. Standard runtime is
ordinary, fully deterministic, lexicon-free BPE -- morphology and dropout
only affect merge learning; nothing about inference changes. Not
independently evaluated on held-out data.
