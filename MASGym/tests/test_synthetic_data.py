"""Synthetic episode generator tests."""
from __future__ import annotations

import pytest

from masgym.data.schemas import AdversaryConfig, EnvConfig, TopologyName
from masgym.data.synthetic import generate_benign_episodes, generate_episodes


def test_generate_episodes_shape_and_validity() -> None:
    env = EnvConfig(n_agents=6, topology=TopologyName.STAR, horizon=4)
    eps = generate_episodes(env, AdversaryConfig(beta=0.3, colluding=True), 20, seed=0)
    assert len(eps) == 20
    for ep in eps:
        assert ep.phi in (0, 1) and ep.psi in (0, 1)
        assert len(ep.trace.steps) == env.horizon
        assert ep.trace.final_compromised.issubset(set(range(env.n_agents)))


def test_benign_counterpart_has_no_compromise() -> None:
    env = EnvConfig(n_agents=6, topology=TopologyName.STAR, horizon=4)
    eps = generate_benign_episodes(env, 30, seed=1)
    # no adversary -> no seed set -> no compromise transitions -> phi == 0
    assert all(ep.phi == 0 for ep in eps)
    assert all(len(ep.trace.seed_set) == 0 for ep in eps)


def test_generate_requires_positive_episodes() -> None:
    env = EnvConfig()
    with pytest.raises(ValueError):
        generate_episodes(env, AdversaryConfig(), 0)
