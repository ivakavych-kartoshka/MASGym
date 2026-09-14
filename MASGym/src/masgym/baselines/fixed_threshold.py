"""Fixed-threshold defense (paper Section 10 baseline).

A defense that flags/defers when a per-episode synthetic risk score crosses a threshold.
Tie handling: a score exactly equal to the threshold is treated as *flag/defer* (the
conservative choice; see audits/math_to_code_audit.md). The threshold does not depend on
test data, so there is no test-dependent-threshold issue.

SYNTHETIC EFFECT-MODEL: the mapping from ``threshold`` to (p_reduction, detect, recover)
is a chosen model, not a measured efficacy.
"""
from __future__ import annotations

from ..data.schemas import AdversaryConfig, EnvConfig
from ..utils.validation import require_probability
from .base import SyntheticDefense


class FixedThresholdDefense(SyntheticDefense):
    """Flag/defer at a fixed risk threshold; higher threshold => weaker defense."""

    def __init__(self, threshold: float = 0.5) -> None:
        require_probability(threshold, "threshold")
        self.threshold = threshold
        # A lower threshold flags more aggressively -> larger p reduction and detection.
        super().__init__(
            name=f"fixed_threshold@{threshold:.2f}",
            p_reduction=(1.0 - threshold) * 0.5,
            detect=(1.0 - threshold) * 0.7,
            recover=0.3,
        )

    def flags(self, risk_score: float) -> bool:
        """Return True (flag/defer) iff ``risk_score >= threshold`` (ties -> defer)."""
        return float(risk_score) >= self.threshold
