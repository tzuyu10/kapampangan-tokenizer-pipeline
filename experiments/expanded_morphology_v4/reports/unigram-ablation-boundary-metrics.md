# Unigram ablation vs. Plain BPE / MorphBPE: boundary F1 and MCF1

Silver diagnostics against this experiment's own resegmentation audit and morphology index (not independent/human-annotated gold), computed identically across every condition below.

| vocab | condition | boundary F1 | boundary P | boundary R | MCF1 | MCF1 P | MCF1 R |
|---|---|---|---|---|---|---|---|
| 6080 | plain_bpe | 0.2454 | 0.2846 | 0.2156 | 0.1375 | 0.1263 | 0.1507 |
| 6080 | penalty_1 | 0.4367 | 0.4135 | 0.4627 | 0.1685 | 0.1445 | 0.2019 |
| 6080 | penalty_2 | 0.4957 | 0.4633 | 0.5330 | 0.1853 | 0.1574 | 0.2251 |
| 6080 | penalty_4 | 0.5722 | 0.5291 | 0.6230 | 0.2049 | 0.1756 | 0.2461 |
| 6080 | penalty_8 | 0.6882 | 0.6366 | 0.7488 | 0.2391 | 0.2005 | 0.2962 |
| 6080 | unigram_ablation | 0.4520 | 0.5264 | 0.3961 | 0.2192 | 0.1829 | 0.2734 |
| 8192 | plain_bpe | 0.2325 | 0.3029 | 0.1887 | 0.1414 | 0.1481 | 0.1352 |
| 8192 | penalty_1 | 0.4470 | 0.4371 | 0.4575 | 0.1788 | 0.1682 | 0.1908 |
| 8192 | penalty_2 | 0.5065 | 0.4873 | 0.5273 | 0.1989 | 0.1836 | 0.2169 |
| 8192 | penalty_4 | 0.5867 | 0.5591 | 0.6172 | 0.2168 | 0.2006 | 0.2358 |
| 8192 | penalty_8 | 0.7023 | 0.6657 | 0.7432 | 0.2600 | 0.2327 | 0.2945 |
| 8192 | unigram_ablation | 0.4363 | 0.5539 | 0.3599 | 0.2199 | 0.1968 | 0.2489 |
| 16384 | plain_bpe | 0.1694 | 0.3195 | 0.1153 | 0.1324 | 0.2034 | 0.0982 |
| 16384 | penalty_1 | 0.4621 | 0.4793 | 0.4460 | 0.1911 | 0.2149 | 0.1720 |
| 16384 | penalty_2 | 0.5246 | 0.5338 | 0.5156 | 0.2146 | 0.2295 | 0.2015 |
| 16384 | penalty_4 | 0.6092 | 0.6164 | 0.6023 | 0.2332 | 0.2464 | 0.2214 |
| 16384 | penalty_8 | 0.7372 | 0.7404 | 0.7341 | 0.2915 | 0.2939 | 0.2891 |
| 16384 | unigram_ablation | 0.3720 | 0.5654 | 0.2771 | 0.2145 | 0.2253 | 0.2048 |

'unigram_ablation' is NOT NLLB's tokenizer -- a fresh Unigram-LM model trained on this project's own corpus at the matched local vocabulary size (see train_unigram_ablation.py / nllb_baseline_report.py).
