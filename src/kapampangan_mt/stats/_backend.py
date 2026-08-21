"""SciPy-backed statistics with pure-NumPy fallbacks.

SciPy is the tool named in the thesis and is what you should install.  The
fallbacks exist so the pipeline still runs (and unit tests still pass) in a
stripped environment; they are numerically equivalent for the paired t-test and
use the normal approximation for Wilcoxon.
"""
from __future__ import annotations

import math

import numpy as np

try:  # pragma: no cover
    from scipy import stats as _sp

    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    _sp = None
    HAVE_SCIPY = False


def ttest_rel(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if HAVE_SCIPY:
        t, p = _sp.ttest_rel(a, b)
        return float(t), float(p)
    d = a - b
    n = len(d)
    sd = d.std(ddof=1)
    if sd == 0 or n < 2:
        return float("nan"), 1.0
    t = float(d.mean() / (sd / math.sqrt(n)))
    # two-sided p from Student's t via the regularised incomplete beta function
    df = n - 1
    x = df / (df + t * t)
    p = _betainc(df / 2.0, 0.5, x)
    return t, float(min(1.0, max(0.0, p)))


def wilcoxon(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    if HAVE_SCIPY:
        try:
            w, p = _sp.wilcoxon(a, b, zero_method="wilcox")
            return float(w), float(p)
        except ValueError:
            return float("nan"), 1.0
    d = (a - b)[a != b]
    n = len(d)
    if n == 0:
        return float("nan"), 1.0
    order = np.argsort(np.abs(d))
    ranks = np.empty(n, dtype=float)
    ranks[order] = np.arange(1, n + 1)
    w_plus = ranks[d > 0].sum()
    w_minus = ranks[d < 0].sum()
    W = min(w_plus, w_minus)
    mu = n * (n + 1) / 4.0
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    if sigma == 0:
        return float(W), 1.0
    z = (W - mu + 0.5) / sigma
    p = 2 * (1 - _norm_cdf(abs(z)))
    return float(W), float(min(1.0, max(0.0, p)))


def shapiro(d: np.ndarray) -> tuple[float, float]:
    if HAVE_SCIPY and 3 <= len(d) <= 5000:
        s, p = _sp.shapiro(d)
        return float(s), float(p)
    return float("nan"), float("nan")


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b) via continued fraction."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(math.log(x) * a + math.log(1 - x) * b - lbeta) / a
    if x > (a + 1) / (a + b + 2):
        return 1.0 - _betainc(b, a, 1 - x)
    f, c, d = 1.0, 1.0, 0.0
    for i in range(200):
        m = i // 2
        if i == 0:
            num = 1.0
        elif i % 2 == 0:
            num = (m * (b - m) * x) / ((a + 2 * m - 1) * (a + 2 * m))
        else:
            num = -((a + m) * (a + b + m) * x) / ((a + 2 * m) * (a + 2 * m + 1))
        d = 1.0 + num * d
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        c = 1.0 + num / c
        c = 1e-30 if abs(c) < 1e-30 else c
        f *= c * d
        if abs(1.0 - c * d) < 1e-12:
            break
    return front * (f - 1.0)
