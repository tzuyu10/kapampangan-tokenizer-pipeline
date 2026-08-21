"""Paired bootstrap resampling for corpus-level MT metrics (Koehn, 2004).

Corpus BLEU is not the mean of sentence BLEUs, so a t-test over sentence BLEU
does not test the number reported in Table 3.  The field-standard significance
test for corpus BLEU / chrF++ is the paired bootstrap; report it as primary and
keep the thesis' paired t-test on sentence-level scores as a secondary check.
"""
from __future__ import annotations

import numpy as np


def paired_bootstrap_corpus(
    hyp_a: list[str],
    hyp_b: list[str],
    refs: list[str],
    metric: str = "bleu",
    n_resamples: int = 1000,
    seed: int = 13,
    lowercase: bool = False,
) -> dict:
    from sacrebleu.metrics import BLEU, CHRF

    scorer = (
        BLEU(lowercase=lowercase, tokenize="13a")
        if metric == "bleu"
        else CHRF(char_order=6, word_order=2, beta=2)
    )
    n = len(refs)
    assert len(hyp_a) == len(hyp_b) == n
    rng = np.random.default_rng(seed)

    base_a = scorer.corpus_score(hyp_a, [refs]).score
    base_b = scorer.corpus_score(hyp_b, [refs]).score
    diffs = np.empty(n_resamples)
    for k in range(n_resamples):
        idx = rng.integers(0, n, n)
        ha = [hyp_a[i] for i in idx]
        hb = [hyp_b[i] for i in idx]
        rf = [refs[i] for i in idx]
        diffs[k] = scorer.corpus_score(ha, [rf]).score - scorer.corpus_score(hb, [rf]).score

    p = float(2 * min((diffs <= 0).mean(), (diffs >= 0).mean()))
    return {
        "metric": metric,
        "score_proposed": base_a,
        "score_baseline": base_b,
        "observed_diff": base_a - base_b,
        "mean_bootstrap_diff": float(diffs.mean()),
        "ci_low": float(np.percentile(diffs, 2.5)),
        "ci_high": float(np.percentile(diffs, 97.5)),
        "p_value": p,
        "n_resamples": n_resamples,
        "decision": "reject H0" if p < 0.05 else "fail to reject H0",
    }
