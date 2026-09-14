"""Confidence intervals for the metric estimators (Theorem 9.17).

``hoeffding_ci`` is the distribution-free interval the paper uses (Theorem 9.17a). A Wilson
interval is also provided for tighter reporting; it uses the stdlib normal quantile, so no
scipy dependency is required.
"""
from __future__ import annotations

import math
from statistics import NormalDist

from ..utils.validation import require_positive_int, require_probability


def hoeffding_halfwidth(n: int, alpha: float = 0.05) -> float:
    """Half-width ``sqrt(ln(2/alpha) / (2n))`` of the two-sided Hoeffding interval (Thm 9.17a)."""
    require_positive_int(n, "n")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * n))


def hoeffding_ci(p_hat: float, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Two-sided Hoeffding CI for a mean of ``n`` bounded {0,1} indicators (Thm 9.17a).

    Returns ``(lo, hi)`` clamped to [0, 1].
    """
    require_probability(p_hat, "p_hat")
    h = hoeffding_halfwidth(n, alpha)
    return max(0.0, p_hat - h), min(1.0, p_hat + h)


def wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wilson score interval for ``k`` successes in ``n`` trials (tighter than Hoeffding)."""
    require_positive_int(n, "n")
    if k < 0 or k > n:
        raise ValueError("k must be in [0, n]")
    z = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    phat = k / n
    denom = 1.0 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = (z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))) / denom
    return max(0.0, center - margin), min(1.0, center + margin)
