"""Utility-security aggregators (paper Eq. 1/5; Theorem 9.2; Remark 9.3).

The default aggregator is the product ``g(u, sigma) = u * sigma`` with ``u = PNA_sys`` and
``sigma = 1 - ASR_sys``. Theorem 9.2 shows this is the unique aggregator under axioms
D2/D4a/D4b; Remark 9.3 names alternatives (``min``, weighted geometric mean), which are
provided here so that construct validity is *testable*, not asserted (RQ1).
"""
from __future__ import annotations

from ..utils.validation import clamp_unit, require_probability


def product_nrp(pna: float, asr: float) -> float:
    """NRP_sys = PNA_sys * (1 - ASR_sys)  (Eq. 1 / Eq. 5; the default, Thm 9.2)."""
    require_probability(pna, "pna")
    require_probability(asr, "asr")
    return clamp_unit(pna * (1.0 - asr))


def min_agg(pna: float, asr: float) -> float:
    """Alternative aggregator g(u, sigma) = min(u, sigma) (worst-coordinate; Remark 9.3)."""
    require_probability(pna, "pna")
    require_probability(asr, "asr")
    return clamp_unit(min(pna, 1.0 - asr))


def weighted_geometric(pna: float, asr: float, w: float = 0.5) -> float:
    """Alternative aggregator g(u, sigma) = u^w * sigma^(1-w) (Remark 9.3).

    Uses the convention ``0^0 = 0`` so the boundary ``g(0, .) = 0`` (axiom D2) holds.
    """
    require_probability(pna, "pna")
    require_probability(asr, "asr")
    require_probability(w, "w")
    sigma = 1.0 - asr
    if pna == 0.0 or sigma == 0.0:
        return 0.0
    return clamp_unit((pna ** w) * (sigma ** (1.0 - w)))


# Registry so experiments/tests can iterate over aggregators by name.
AGGREGATORS: dict[str, object] = {
    "product": product_nrp,
    "min": min_agg,
    "weighted_geometric": weighted_geometric,
}
