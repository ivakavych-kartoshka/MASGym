"""Topology construction tests (paper Section 4.2)."""
from __future__ import annotations

from masgym.data.schemas import TopologyName
from masgym.data.topology import build_topology


def test_star_edges_and_degrees() -> None:
    t = build_topology(TopologyName.STAR, 5)
    # hub (0) reaches all 4 leaves and each leaf reaches the hub
    assert t.n_edges == 2 * 4
    assert set(t.out_neighbors(0)) == {1, 2, 3, 4}
    assert t.in_degree(1) == 1  # only the hub


def test_chain_is_directed_path() -> None:
    t = build_topology(TopologyName.CHAIN, 5)
    assert t.n_edges == 4
    assert t.out_neighbors(0) == [1]
    assert t.in_degree(0) == 0


def test_tree_edges() -> None:
    t = build_topology(TopologyName.TREE, 7, branching_factor=2)
    assert t.n_edges == 6  # n-1 for a tree
    assert set(t.out_neighbors(0)) == {1, 2}


def test_mesh_is_complete() -> None:
    n = 6
    t = build_topology(TopologyName.MESH, n)
    assert t.n_edges == n * (n - 1)
    assert t.in_degree(0) == n - 1
