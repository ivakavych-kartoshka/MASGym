"""CoRB co-evolving loop tests (Algorithm 2)."""
from __future__ import annotations

import logging

from masgym.data.schemas import EnvConfig, TopologyName
from masgym.methods.blue_policies import EscalatingBluePolicy
from masgym.methods.corb import pareto_frontier, run_corb
from masgym.methods.red_policies import RandomRedPolicy
from masgym.utils.seeding import SeededRNG

logging.disable(logging.CRITICAL)


def test_corb_row_count_and_pareto() -> None:
    env = EnvConfig(n_agents=6, topology=TopologyName.STAR, horizon=4)
    res = run_corb(env, RandomRedPolicy(SeededRNG(0)), EscalatingBluePolicy(), rounds=3, n_episodes=30, seed=0)
    assert len(res.rows) == 6  # 2 scorings per round
    assert all(r in res.rows for r in res.pareto)
    assert len(res.pareto) >= 1


def test_corb_deterministic_under_seed() -> None:
    env = EnvConfig(n_agents=6, topology=TopologyName.STAR, horizon=4)
    a = run_corb(env, RandomRedPolicy(SeededRNG(1)), EscalatingBluePolicy(), rounds=2, n_episodes=20, seed=7)
    b = run_corb(env, RandomRedPolicy(SeededRNG(1)), EscalatingBluePolicy(), rounds=2, n_episodes=20, seed=7)
    assert [r["asr_sys"] for r in a.rows] == [r["asr_sys"] for r in b.rows]


def test_pareto_frontier_basic() -> None:
    rows = [
        {"asr_sys": 0.2, "mean_tokens": 100.0},  # non-dominated
        {"asr_sys": 0.5, "mean_tokens": 50.0},   # non-dominated
        {"asr_sys": 0.6, "mean_tokens": 120.0},  # dominated by the first
    ]
    front = pareto_frontier(rows)
    assert rows[0] in front and rows[1] in front and rows[2] not in front
