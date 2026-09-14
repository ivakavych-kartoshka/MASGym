"""Closed-form compromise-propagation expectations (paper Props 9.7-9.10, Thm 9.13).

Each function returns the *expected number of additionally compromised agents* (reach beyond
the seed) under the independent-cascade model with per-edge probability ``p``. The Monte-Carlo
simulator in :mod:`masgym.env.propagation` is validated against these forms in
``tests/test_propagation.py``.
"""
from __future__ import annotations

from ..utils.validation import require_probability


def chain_expected_reach(n: int, p: float) -> float:
    """Prop 9.7: chain reach ``sum_{j=1}^{n-1} p^j`` (<= p/(1-p) for p<1)."""
    require_probability(p, "p")
    if n < 2:
        return 0.0
    return float(sum(p ** j for j in range(1, n)))


def star_centre_expected_reach(n: int, p: float) -> float:
    """Prop 9.8: star, centre seed -> ``p(n-1)`` (each leaf independently w.p. p)."""
    require_probability(p, "p")
    return float(p * max(0, n - 1))


def star_leaf_expected_reach(n: int, p: float) -> float:
    """Prop 9.8: star, leaf seed -> ``p + p^2 (n-2)`` (centre then the other leaves)."""
    require_probability(p, "p")
    if n < 2:
        return 0.0
    return float(p + (p ** 2) * max(0, n - 2))


def cpr_star_centre(p: float) -> float:
    """Prop 9.8: compromise-propagation rate on a star with a compromised centre = ``p``."""
    return require_probability(p, "p")


def tree_expected_reach(b: int, p: float, d: int) -> float:
    """Prop 9.9: rooted tree reach ``sum_{l=1}^{d} (bp)^l`` (transition at bp=1)."""
    require_probability(p, "p")
    if b < 1 or d < 1:
        return 0.0
    bp = b * p
    return float(sum(bp ** ell for ell in range(1, d + 1)))


def mesh_one_round_expected(n: int, s: int, p: float) -> float:
    """Prop 9.10: complete-graph one-round reach ``(n-s)(1-(1-p)^s)`` (additional beyond s seeds)."""
    require_probability(p, "p")
    if s >= n:
        return 0.0
    return float((n - s) * (1.0 - (1.0 - p) ** s))


def collusion_gap_star(n: int, p: float) -> float:
    """Thm 9.13: exact single-seed collusion advantage on a star.

    ``Delta_coll = p(1-p)(n-1)(n-2)/n`` (colluding centre-seed minus independent random-seed).
    """
    require_probability(p, "p")
    if n < 3:
        return 0.0
    return float(p * (1.0 - p) * (n - 1) * (n - 2) / n)
