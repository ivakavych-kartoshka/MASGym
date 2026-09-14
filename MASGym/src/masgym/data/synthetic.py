"""Synthetic episode generator (paper Section 10 smoke-test substitute).

Runs ``M`` i.i.d. synthetic episodes (Assumption A2) for a given environment and adversary
configuration through the :class:`~masgym.env.orchestration.Orchestrator`. This replaces the
real LLM backbones + ToolEmu emulator for local, dependency-free testing. Every batch of
episodes produced here is a "synthetic smoke-test output, not a paper result".
"""
from __future__ import annotations

from typing import Optional

from ..env.checker import DeterministicChecker
from ..env.emulation import SyntheticToolEmulator, ToolEmulator
from ..env.orchestration import DefenseLike, Orchestrator
from ..utils.seeding import SeededRNG
from .schemas import AdversaryConfig, EnvConfig, Episode


def generate_episodes(
    env: EnvConfig,
    adv: AdversaryConfig,
    n_episodes: int,
    seed: int = 0,
    defense: Optional[DefenseLike] = None,
    checker: Optional[DeterministicChecker] = None,
    emulator: Optional[ToolEmulator] = None,
) -> list[Episode]:
    """Generate ``n_episodes`` synthetic episodes for ``(env, adv)`` under an optional defense."""
    if n_episodes <= 0:
        raise ValueError("n_episodes must be positive")
    orch = Orchestrator(
        checker=checker or DeterministicChecker(),
        emulator=emulator or SyntheticToolEmulator(),
    )
    rng = SeededRNG(seed)
    return [orch.run_episode(env, adv, rng, defense=defense) for _ in range(n_episodes)]


def generate_benign_episodes(
    env: EnvConfig, n_episodes: int, seed: int = 0, defense: Optional[DefenseLike] = None
) -> list[Episode]:
    """Generate episodes under the benign counterpart c-circle (for PNA_sys, Eq. 4)."""
    return generate_episodes(env, AdversaryConfig(), n_episodes, seed=seed, defense=defense)
