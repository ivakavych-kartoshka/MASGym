"""Numerical verification of the paper's closed-form theory (Section 9).

This is NOT a benchmark result; it is a self-check that the implementation matches the
proven closed forms. It (i) compares Monte-Carlo compromise reach against Props 9.7-9.10 and
the collusion gap (Thm 9.13), (ii) checks the metric axioms (Thm 9.2 / Remark 9.3), and (iii)
verifies Hoeffding-CI coverage and sample-complexity formulas (Thm 9.17 / Cor 9.18).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from masgym.data.schemas import TopologyName
from masgym.data.topology import build_topology
from masgym.env.propagation import IndependentCascade
from masgym.methods.aggregators import min_agg, product_nrp, weighted_geometric
from masgym.metrics.confidence_intervals import hoeffding_ci
from masgym.theory.metric_axioms import check_axioms, reduces_to_asb
from masgym.theory.propagation_bounds import (
    chain_expected_reach,
    collusion_gap_star,
    mesh_one_round_expected,
    star_centre_expected_reach,
    tree_expected_reach,
)
from masgym.theory.sample_complexity import hoeffding_min_samples, sweep_budget
from masgym.utils.io import ensure_dir, run_metadata, write_json
from masgym.utils.logging import get_logger
from masgym.utils.seeding import SeededRNG

logger = get_logger(__name__)


def _mc_reach(topology, seed_nodes, p, rng, trials, max_waves=None) -> float:
    ic = IndependentCascade(p)
    reach = [len(ic.waves(seed_nodes, topology, rng, max_waves=max_waves)[-1]) - len(set(seed_nodes)) for _ in range(trials)]
    return float(np.mean(reach))


def run_theory_check(out_dir: str | Path, trials: int = 8000, seed: int = 0) -> dict[str, Any]:
    out = ensure_dir(out_dir)
    rng = SeededRNG(seed)
    p = 0.3
    results: dict[str, Any] = {"propagation": {}, "collusion": {}, "axioms": {}, "sample_complexity": {}}

    # --- propagation: MC vs closed form ---
    n = 12
    star = build_topology(TopologyName.STAR, n)
    results["propagation"]["star_centre"] = {
        "mc": _mc_reach(star, [0], p, rng, trials),
        "closed": star_centre_expected_reach(n, p),
    }
    chain = build_topology(TopologyName.CHAIN, n)
    results["propagation"]["chain"] = {
        "mc": _mc_reach(chain, [0], p, rng, trials),
        "closed": chain_expected_reach(n, p),
    }
    tree = build_topology(TopologyName.TREE, 15, branching_factor=2)  # perfect binary tree, depth 3
    results["propagation"]["tree"] = {
        "mc": _mc_reach(tree, [0], p, rng, trials),
        "closed": tree_expected_reach(2, p, 3),
    }
    mesh = build_topology(TopologyName.MESH, n)
    results["propagation"]["mesh_one_round"] = {
        "mc": _mc_reach(mesh, [0, 1], p, rng, trials, max_waves=1),
        "closed": mesh_one_round_expected(n, 2, p),
    }

    # --- collusion separation (star): colluding centre-seed vs independent random single seed ---
    ic = IndependentCascade(p)
    coll = [len(ic.waves([0], star, rng)[-1]) - 1 for _ in range(trials)]
    ind = []
    g = rng.generator
    for _ in range(trials):
        s0 = int(g.integers(0, n))
        ind.append(len(ic.waves([s0], star, rng)[-1]) - 1)
    results["collusion"]["star"] = {
        "mc_gap": float(np.mean(coll) - np.mean(ind)),
        "closed_gap": collusion_gap_star(n, p),
    }

    # --- metric axioms ---
    results["axioms"] = {
        "product": check_axioms(product_nrp),
        "min": check_axioms(min_agg),
        "weighted_geometric": check_axioms(lambda u, a: weighted_geometric(u, a, 0.5)),
        "product_reduces_to_asb": reduces_to_asb(),
    }

    # --- sample complexity + empirical Hoeffding coverage ---
    eps, alpha, ptrue = 0.05, 0.05, 0.4
    m = hoeffding_min_samples(eps, alpha)
    covered = 0
    reps = 2000
    for _ in range(reps):
        draws = (g.random(m) < ptrue).mean()
        lo, hi = hoeffding_ci(float(draws), m, alpha)
        if lo <= ptrue <= hi:
            covered += 1
    results["sample_complexity"] = {
        "eps": eps, "alpha": alpha, "M_min": m,
        "empirical_coverage": covered / reps,
        "target_coverage_at_least": 1 - alpha,
        "sweep_budget_G50_delta0.1": sweep_budget(50, 0.1, alpha),
    }

    results["provenance"] = run_metadata({"trials": trials}, seed, synthetic=True)
    results["note"] = "numerical verification of closed forms; not a benchmark result"
    write_json(out / "theory_check.json", results)
    logger.info("theory check written to %s", out / "theory_check.json")
    return results
