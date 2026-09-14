"""Propagation Monte-Carlo vs closed-form tests (Props 9.7-9.11, Thm 9.13)."""
from __future__ import annotations

import numpy as np

from masgym.data.schemas import TopologyName
from masgym.data.topology import build_topology
from masgym.env.propagation import IndependentCascade, ThresholdCascade
from masgym.theory.propagation_bounds import (
    chain_expected_reach,
    collusion_gap_star,
    mesh_one_round_expected,
    star_centre_expected_reach,
    tree_expected_reach,
)
from masgym.utils.seeding import SeededRNG

P = 0.3
TRIALS = 4000


def _mc(topo, seed_nodes, p, rng, max_waves=None):
    ic = IndependentCascade(p)
    r = [len(ic.waves(seed_nodes, topo, rng, max_waves=max_waves)[-1]) - len(set(seed_nodes)) for _ in range(TRIALS)]
    return float(np.mean(r))


def test_chain_matches_closed_form() -> None:
    rng = SeededRNG(1)
    topo = build_topology(TopologyName.CHAIN, 12)
    assert abs(_mc(topo, [0], P, rng) - chain_expected_reach(12, P)) < 0.1


def test_star_centre_matches_closed_form() -> None:
    rng = SeededRNG(2)
    topo = build_topology(TopologyName.STAR, 12)
    assert abs(_mc(topo, [0], P, rng) - star_centre_expected_reach(12, P)) < 0.3


def test_tree_matches_closed_form() -> None:
    rng = SeededRNG(3)
    topo = build_topology(TopologyName.TREE, 15, branching_factor=2)  # perfect depth-3 binary tree
    assert abs(_mc(topo, [0], P, rng) - tree_expected_reach(2, P, 3)) < 0.25


def test_mesh_one_round_matches_closed_form() -> None:
    rng = SeededRNG(4)
    topo = build_topology(TopologyName.MESH, 12)
    assert abs(_mc(topo, [0, 1], P, rng, max_waves=1) - mesh_one_round_expected(12, 2, P)) < 0.4


def test_collusion_gap_star() -> None:
    rng = SeededRNG(5)
    n = 12
    topo = build_topology(TopologyName.STAR, n)
    ic = IndependentCascade(P)
    coll = np.mean([len(ic.waves([0], topo, rng)[-1]) - 1 for _ in range(TRIALS)])
    g = rng.generator
    ind = np.mean([len(ic.waves([int(g.integers(0, n))], topo, rng)[-1]) - 1 for _ in range(TRIALS)])
    assert abs((coll - ind) - collusion_gap_star(n, P)) < 0.35
    assert collusion_gap_star(n, P) > 0  # strict advantage (Thm 9.13)


def test_threshold_confinement_on_chain() -> None:
    # Cor 9.11: chain in-degree 1 < theta=2 -> no propagation beyond the seed.
    rng = SeededRNG(6)
    topo = build_topology(TopologyName.CHAIN, 10)
    tc = ThresholdCascade(theta=2)
    final = tc.waves([0], topo, rng)[-1]
    assert final == frozenset({0})
