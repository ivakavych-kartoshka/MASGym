"""Determinism / reproducibility tests (paper Assumption A2; reproducibility requirement)."""
from __future__ import annotations

import numpy as np

from masgym.data.schemas import AdversaryConfig, EnvConfig, TopologyName
from masgym.data.synthetic import generate_episodes
from masgym.methods.scoring import score_config
from masgym.utils.seeding import SeededRNG


def test_seeded_rng_determinism() -> None:
    a = SeededRNG(42).generator.random(5)
    b = SeededRNG(42).generator.random(5)
    assert np.allclose(a, b)


def test_score_config_reproducible() -> None:
    env = EnvConfig(n_agents=8, topology=TopologyName.STAR, horizon=5)
    adv = AdversaryConfig(beta=0.25, colluding=True)
    m1 = score_config(env, adv, 100, seed=3).metrics
    m2 = score_config(env, adv, 100, seed=3).metrics
    assert m1.asr_sys == m2.asr_sys and m1.cpr == m2.cpr and m1.nrp_sys == m2.nrp_sys


def test_different_seed_changes_episodes() -> None:
    env = EnvConfig(n_agents=8, topology=TopologyName.MESH, horizon=5)
    adv = AdversaryConfig(beta=0.3)
    e1 = [ep.phi for ep in generate_episodes(env, adv, 50, seed=0)]
    e2 = [ep.phi for ep in generate_episodes(env, adv, 50, seed=1)]
    assert e1 != e2  # extremely unlikely to be identical under different seeds
