"""Compromise-propagation models (Assumption A4; Propositions 9.7-9.11).

Two monotone (absorbing) rules are implemented:

* :class:`IndependentCascade` -- Kempe-style: when a node becomes compromised it gets a
  *single* independent chance (probability ``p``) to compromise each susceptible
  out-neighbour. A susceptible node ``v`` with ``k`` newly-compromised in-neighbours in a
  wave is compromised with probability ``1 - (1-p)^k``. This reproduces the paper's closed
  forms exactly: chain ``sum_j p^j``, star centre ``p(n-1)``, tree ``sum_l (bp)^l``, mesh one
  round ``s + (n-s)(1-(1-p)^s)``.
* :class:`ThresholdCascade` -- bootstrap percolation: ``v`` is compromised once at least
  ``theta`` of its in-neighbours are compromised (Cor. 9.11).

Both are seeded with the initial adversary set ``B_0`` and iterated to fixation (or for a
bounded number of waves), returning the sequence ``B_0, B_1, ...`` used to compute the
compromise-propagation rate (Eq. 6) and to build the global trace.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Optional, Protocol

from ..data.schemas import EnvConfig, PropagationModel, Topology
from ..utils.seeding import SeededRNG
from ..utils.validation import require_probability


def _in_neighbor_map(topology: Topology) -> dict[int, list[int]]:
    m: dict[int, list[int]] = defaultdict(list)
    for (s, d) in topology.edges:
        m[d].append(s)
    return m


class PropagationRule(Protocol):
    """A monotone propagation rule mapping a compromised set to its successor."""

    def waves(
        self, seed: Iterable[int], topology: Topology, rng: SeededRNG, max_waves: Optional[int] = None
    ) -> list[frozenset[int]]:
        ...


@dataclass
class IndependentCascade:
    """Independent-cascade model with per-edge probability ``p`` (Props 9.7-9.10, 9.13)."""

    p: float

    def __post_init__(self) -> None:
        require_probability(self.p, "p")

    def waves(
        self, seed: Iterable[int], topology: Topology, rng: SeededRNG, max_waves: Optional[int] = None
    ) -> list[frozenset[int]]:
        gen = rng.generator
        in_map = _in_neighbor_map(topology)
        active = set(seed)
        newly = set(active)
        history = [frozenset(active)]
        wave = 0
        while newly and (max_waves is None or wave < max_waves):
            candidates = {
                v for u in newly for (_, v) in _out_edges(topology, u) if v not in active
            }
            next_newly: set[int] = set()
            for v in sorted(candidates):
                k = sum(1 for nb in in_map[v] if nb in newly)
                if k == 0:
                    continue
                prob = 1.0 - (1.0 - self.p) ** k
                if gen.random() < prob:
                    next_newly.add(v)
            active |= next_newly
            newly = next_newly
            history.append(frozenset(active))
            wave += 1
        return history


@dataclass
class ThresholdCascade:
    """Bootstrap-percolation model: compromise once ``>= theta`` in-neighbours compromised."""

    theta: int

    def __post_init__(self) -> None:
        if self.theta < 1:
            raise ValueError("theta must be >= 1")

    def waves(
        self, seed: Iterable[int], topology: Topology, rng: SeededRNG, max_waves: Optional[int] = None
    ) -> list[frozenset[int]]:
        in_map = _in_neighbor_map(topology)
        active = set(seed)
        history = [frozenset(active)]
        wave = 0
        while max_waves is None or wave < max_waves:
            newly = {
                v
                for v in range(topology.n_agents)
                if v not in active and sum(1 for nb in in_map[v] if nb in active) >= self.theta
            }
            if not newly:
                break
            active |= newly
            history.append(frozenset(active))
            wave += 1
        return history


def _out_edges(topology: Topology, u: int) -> list[tuple[int, int]]:
    return [(s, d) for (s, d) in topology.edges if s == u]


def make_propagation(env: EnvConfig) -> PropagationRule:
    """Build the propagation rule specified by an :class:`EnvConfig`."""
    if env.propagation is PropagationModel.INDEPENDENT_CASCADE:
        return IndependentCascade(p=env.p_infect)
    if env.propagation is PropagationModel.THRESHOLD:
        return ThresholdCascade(theta=env.threshold)
    raise ValueError(f"unknown propagation model {env.propagation!r}")  # pragma: no cover
