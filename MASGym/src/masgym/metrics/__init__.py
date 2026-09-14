"""System-level metric suite (paper Section 7.6, Appendix B) and confidence intervals."""
from __future__ import annotations

from .confidence_intervals import hoeffding_ci, hoeffding_halfwidth, wilson_ci
from .metrics import (
    SystemMetrics,
    asr_sys,
    collusion_advantage,
    compromise_propagation_rate,
    compute_system_metrics,
    coordination_quality,
    group_conditional_asr,
    nrp_sys,
    pna_sys,
    recovery_rate,
    time_to_detection,
)

__all__ = [
    "SystemMetrics",
    "asr_sys",
    "pna_sys",
    "nrp_sys",
    "compromise_propagation_rate",
    "coordination_quality",
    "collusion_advantage",
    "time_to_detection",
    "recovery_rate",
    "group_conditional_asr",
    "compute_system_metrics",
    "hoeffding_ci",
    "hoeffding_halfwidth",
    "wilson_ci",
]
