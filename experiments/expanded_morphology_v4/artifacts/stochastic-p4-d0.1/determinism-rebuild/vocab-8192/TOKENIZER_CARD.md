# Expanded morphology v4 tokenizer (stochastic-p4-d0.1; 8,192)

Artifact fingerprint: `ebafd9f2ee1dfd3ef1b816c734c27981ddf6d8ab64875aa482d3df263a80c3b3`

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
