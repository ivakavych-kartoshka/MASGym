"""Closed-form theory (paper Section 9) and its numerical checks."""
from __future__ import annotations

from .metric_axioms import check_axioms, reduces_to_asb
from .propagation_bounds import (
    chain_expected_reach,
    collusion_gap_star,
    cpr_star_centre,
    mesh_one_round_expected,
    star_centre_expected_reach,
    star_leaf_expected_reach,
    tree_expected_reach,
)
from .sample_complexity import (
    asr_confidence_delta,
    episode_cost,
    hoeffding_min_samples,
    nrp_confidence_delta,
    sweep_budget,
    sweep_cost,
)

__all__ = [
    "chain_expected_reach",
    "star_centre_expected_reach",
    "star_leaf_expected_reach",
    "tree_expected_reach",
    "mesh_one_round_expected",
    "collusion_gap_star",
    "cpr_star_centre",
    "hoeffding_min_samples",
    "asr_confidence_delta",
    "nrp_confidence_delta",
    "sweep_budget",
    "episode_cost",
    "sweep_cost",
    "check_axioms",
    "reduces_to_asb",
]
