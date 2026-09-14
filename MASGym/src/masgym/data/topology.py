"""Builders for the four canonical communication topologies (paper Section 4.2).

Node ``0`` is the orchestrator (the star hub / tree root), consistent with the paper's
identification of the orchestrator as the critical node on hub topologies (Prop 9.8).
Edges are directed ``(src, dst)`` meaning ``src`` may send to ``dst``; compromise
propagates along edges under the models in :mod:`masgym.env.propagation`.
"""
from __future__ import annotations

from .schemas import Topology, TopologyName


def build_topology(name: TopologyName, n_agents: int, branching_factor: int = 2) -> Topology:
    """Construct a :class:`Topology` for ``name`` over ``n_agents`` nodes.

    - star: hub ``0`` <-> each leaf (both directions).
    - chain: directed path ``0 -> 1 -> ... -> n-1`` (Prop 9.7 uses a directed path).
    - tree: rooted at ``0`` with ``branching_factor`` children per node, edges parent -> child.
    - mesh: complete graph ``K_n`` with both directions.
    """
    if n_agents < 1:
        raise ValueError("n_agents must be >= 1")
    name = TopologyName(name)

    if name is TopologyName.STAR:
        edges = []
        for leaf in range(1, n_agents):
            edges.append((0, leaf))
            edges.append((leaf, 0))
        return Topology(name=name, n_agents=n_agents, edges=tuple(edges))

    if name is TopologyName.CHAIN:
        edges = [(i, i + 1) for i in range(n_agents - 1)]
        return Topology(name=name, n_agents=n_agents, edges=tuple(edges))

    if name is TopologyName.TREE:
        if branching_factor < 1:
            raise ValueError("branching_factor must be >= 1")
        edges = []
        for child in range(1, n_agents):
            parent = (child - 1) // branching_factor
            edges.append((parent, child))
        return Topology(
            name=name, n_agents=n_agents, edges=tuple(edges), branching_factor=branching_factor
        )

    if name is TopologyName.MESH:
        edges = [(i, j) for i in range(n_agents) for j in range(n_agents) if i != j]
        return Topology(name=name, n_agents=n_agents, edges=tuple(edges))

    raise ValueError(f"unknown topology {name!r}")  # pragma: no cover
