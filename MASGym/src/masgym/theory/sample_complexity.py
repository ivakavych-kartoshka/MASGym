"""Concentration and cost (paper Theorem 9.17, Corollary 9.18, Section 8.1).

These are exact closed forms; ``episode_cost``/``sweep_cost`` return *operation counts*
(agent invocations, trace size), never fabricated wall-clock timings.
"""
from __future__ import annotations

import math


def hoeffding_min_samples(eps: float, alpha: float = 0.05) -> int:
    """Thm 9.17a: minimal ``M`` for eps-accurate ASR/PNA: ``ceil(ln(2/alpha)/(2 eps^2))``."""
    if not (0.0 < eps < 1.0):
        raise ValueError("eps must be in (0, 1)")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    return int(math.ceil(math.log(2.0 / alpha) / (2.0 * eps * eps)))


def asr_confidence_delta(m: int, eps: float) -> float:
    """Thm 9.17a: failure probability bound ``2 exp(-2 M eps^2)`` for the ASR estimate."""
    if m <= 0:
        raise ValueError("m must be positive")
    return float(2.0 * math.exp(-2.0 * m * eps * eps))


def nrp_confidence_delta(m: int, eps: float) -> float:
    """Thm 9.17b: failure probability bound ``4 exp(-2 M eps^2)`` for NRP at 2*eps accuracy."""
    if m <= 0:
        raise ValueError("m must be positive")
    return float(4.0 * math.exp(-2.0 * m * eps * eps))


def sweep_budget(g: int, delta: float, alpha: float = 0.05) -> int:
    """Cor 9.18: per-config ``M`` to resolve an NRP gap ``delta`` across ``G`` configs.

    Uses eps = delta/4 with a Bonferroni correction alpha -> alpha/G:
    ``M = ceil( ln(2 G / alpha) / (2 (delta/4)^2) )``.
    """
    if g < 1:
        raise ValueError("g must be >= 1")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must be in (0, 1)")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    eps = delta / 4.0
    return int(math.ceil(math.log(2.0 * g / alpha) / (2.0 * eps * eps)))


def episode_cost(n_agents: int, horizon: int, n_edges: int) -> dict[str, int]:
    """Section 8.1: per-episode cost. ``invocations = Theta(N H)``; ``trace = Theta((N+|E|) H)``."""
    return {
        "agent_invocations": int(n_agents * horizon),
        "trace_size": int((n_agents + n_edges) * horizon),
    }


def sweep_cost(g: int, m: int, n_agents: int, horizon: int, n_edges: int) -> dict[str, int]:
    """Section 8.1 / Cor 9.18: total sweep cost = ``Theta(G M N H)`` invocations."""
    per = episode_cost(n_agents, horizon, n_edges)
    return {
        "agent_invocations": int(g * m * per["agent_invocations"]),
        "trace_size": int(g * m * per["trace_size"]),
    }
