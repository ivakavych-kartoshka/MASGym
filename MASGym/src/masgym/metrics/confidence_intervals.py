"""Confidence intervals for the metric estimators (Theorem 9.17).

``hoeffding_ci`` is the distribution-free interval the paper uses (Theorem 9.17a). A Wilson
interval is also provided for tighter reporting; it uses the stdlib normal quantile, so no
scipy dependency is required.
"""
from __future__ import annotations

import math
import random
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


def bootstrap_ci(
    values: list[float] | tuple[float, ...],
    n_bootstrap: int = 2000,
    alpha: float = 0.05,
    seed: int | None = None,
) -> tuple[float, float, float]:
    """Cluster-aware (by episode) percentile bootstrap CI for a mean.

    ``values`` is one observation per episode (or per cluster). Resampling is
    performed at the episode level so that within-episode correlation is
    preserved; this is the cluster-aware interval requested by task T05.
    Returns ``(lo, hi, mean)``.
    """
    if not values:
        raise ValueError("values must be non-empty")
    if n_bootstrap < 1:
        raise ValueError("n_bootstrap must be positive")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    rng = random.Random(seed)
    n = len(values)
    mean = sum(values) / n
    boots = []
    for _ in range(n_bootstrap):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        boots.append(sum(sample) / n)
    boots.sort()
    lo_idx = max(0, int(math.floor((alpha / 2.0) * n_bootstrap)) - 1)
    hi_idx = min(n_bootstrap - 1, int(math.ceil((1.0 - alpha / 2.0) * n_bootstrap)) - 1)
    return float(boots[lo_idx]), float(boots[hi_idx]), float(mean)


def holm_adjust(p_values: list[float] | tuple[float, ...]) -> list[float]:
    """Holm-Bonferroni step-down adjusted p-values (family-wise control)."""
    m = len(p_values)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        raw = p_values[idx]
        val = raw * (m - rank)
        running = max(running, val)
        adjusted[idx] = min(1.0, running)
    return adjusted


def bh_adjust(p_values: list[float] | tuple[float, ...]) -> list[float]:
    """Benjamini-Hochberg (FDR) adjusted p-values."""
    m = len(p_values)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: p_values[i], reverse=True)
    adjusted = [0.0] * m
    running = 1.0
    for rank, idx in enumerate(order):
        raw = p_values[idx]
        val = raw * m / (m - rank)
        running = min(running, val)
        adjusted[idx] = min(1.0, running)
    return adjusted
