# Translation metric variable results

P, R and p_n use a 0-1 scale; BLEU and chrF++ use a 0-100 scale. BLEU p_n includes the configured exponential smoothing. Corpus lengths/counts are aggregated within sentences, without joining sentence boundaries.

| Condition | BP | w_n (each) | p1 | p2 | p3 | p4 | BLEU |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| plain_bpe | 1.000000 | 0.250000 | 0.720782 | 0.517696 | 0.391723 | 0.301068 | 45.801585 |
| morph_bpe | 1.000000 | 0.250000 | 0.720478 | 0.519624 | 0.394198 | 0.303595 | 46.007620 |

| Condition | beta | P | R | chrF++ |
| --- | ---: | ---: | ---: | ---: |
| plain_bpe | 2.000000 | 0.654372 | 0.653873 | 65.397277 |
| morph_bpe | 2.000000 | 0.653602 | 0.653019 | 65.313535 |

Split: test; examples: 1659; full split: True.
Results are reference agreement, not a statistical significance or human correctness judgment.
