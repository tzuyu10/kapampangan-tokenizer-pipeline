"""Statistical Treatment (thesis eqs. 10-13) plus two additions the design needs.

Implemented as specified:
  * mean / SD                       (10), (11)
  * paired differences d_i          (12)
  * paired-samples t-test           (13)
  * Wilcoxon signed-rank as sensitivity analysis
  * Cohen's d_z effect size

Added:
  * Shapiro-Wilk on the paired differences, so "we assumed normality by CLT"
    becomes a reported check rather than an assertion.
  * Holm-Bonferroni correction.  The study runs five hypothesis tests
    (FR, MBF1, MCF1, BLEU, chrF++) at alpha = .05.  Uncorrected, the chance of
    at least one false positive is ~23%, and a panel member who knows this will
    ask.  Holm is uniformly more powerful than Bonferroni and needs no
    independence assumption.  See Issue S-2.
"""
from __future__ import annotations

import math


def paired_report(
    proposed: list[float],
    baseline: list[float],
    label: str = "",
    alpha: float = 0.05,
    higher_is_better: bool = True,
) -> dict:
    import numpy as np

    from ._backend import shapiro, ttest_rel, wilcoxon

    a = np.asarray(proposed, dtype=float)
    b = np.asarray(baseline, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"{label}: unequal lengths {a.shape} vs {b.shape}")
    d = a - b
    n = len(d)
    sd_d = float(d.std(ddof=1)) if n > 1 else 0.0

    if sd_d == 0:
        t_stat, p_t = float("nan"), 1.0
    else:
        t_stat, p_t = ttest_rel(a, b)

    w_stat, p_w = wilcoxon(a, b)
    sh_stat, p_shapiro = shapiro(d) if sd_d > 0 else (float("nan"), float("nan"))

    d_z = float(d.mean() / sd_d) if sd_d else 0.0
    normal_ok = not (p_shapiro == p_shapiro) or p_shapiro > alpha
    primary_p = float(p_t) if normal_ok else float(p_w)

    return {
        "metric": label,
        "n": n,
        "mean_proposed": float(a.mean()),
        "sd_proposed": float(a.std(ddof=1)) if n > 1 else 0.0,
        "mean_baseline": float(b.mean()),
        "sd_baseline": float(b.std(ddof=1)) if n > 1 else 0.0,
        "mean_diff": float(d.mean()),
        "sd_diff": sd_d,
        "t": float(t_stat),
        "p_ttest": float(p_t),
        "wilcoxon_W": float(w_stat),
        "p_wilcoxon": float(p_w),
        "shapiro_W": float(sh_stat),
        "p_shapiro": float(p_shapiro),
        "normality_ok": bool(normal_ok),
        "test_used": "paired t-test" if normal_ok else "Wilcoxon signed-rank",
        "p_value": primary_p,
        "cohens_dz": d_z,
        "effect_label": _effect_label(abs(d_z)),
        "favours": ("proposed" if (d.mean() > 0) == higher_is_better else "baseline")
        if d.mean() != 0 else "tie",
        "decision_uncorrected": "reject H0" if primary_p < alpha else "fail to reject H0",
    }


def _effect_label(dz: float) -> str:
    if dz < 0.2:
        return "negligible"
    if dz < 0.5:
        return "small"
    if dz < 0.8:
        return "medium"
    return "large"


def holm_bonferroni(reports: list[dict], alpha: float = 0.05) -> list[dict]:
    """Add family-wise corrected decisions to a list of ``paired_report`` dicts."""
    order = sorted(range(len(reports)), key=lambda i: reports[i]["p_value"])
    m = len(reports)
    out = [dict(r) for r in reports]
    prev_reject = True
    for rank, i in enumerate(order):
        thresh = alpha / (m - rank)
        reject = prev_reject and out[i]["p_value"] < thresh
        prev_reject = reject
        out[i]["holm_threshold"] = thresh
        out[i]["holm_rank"] = rank + 1
        out[i]["decision_holm"] = "reject H0" if reject else "fail to reject H0"
    return out


def describe(values: list[float]) -> dict:
    n = len(values)
    if n == 0:
        return {"n": 0, "mean": 0.0, "sd": 0.0}
    mean = sum(values) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1)) if n > 1 else 0.0
    return {"n": n, "mean": mean, "sd": sd}
