"""Metric formula tests (Eqs. 3-6, Appendix B)."""
from __future__ import annotations

import math

import pytest

from masgym.data.schemas import AdversaryConfig, EnvConfig, Episode, Trace, TraceStep
from masgym.metrics.metrics import (
    asr_sys,
    collusion_advantage,
    compromise_propagation_rate,
    nrp_sys,
    pna_sys,
)


def _mk(phi: int, psi: int, n: int = 5, seed=frozenset(), final=None) -> Episode:
    final = seed if final is None else final
    tr = Trace(steps=[TraceStep(t=0, compromised=final)], n_agents=n, seed_set=seed)
    return Episode(env=EnvConfig(n_agents=n), adversary=AdversaryConfig(), trace=tr, phi=phi, psi=psi)


def test_asr_and_pna_are_means() -> None:
    eps = [_mk(1, 0), _mk(1, 1), _mk(0, 1), _mk(0, 1)]
    assert asr_sys(eps) == pytest.approx(0.5)
    assert pna_sys(eps) == pytest.approx(0.75)


def test_nrp_product() -> None:
    assert nrp_sys(0.8, 0.25) == pytest.approx(0.6)


def test_empty_sample_is_nan() -> None:
    assert math.isnan(asr_sys([]))
    assert math.isnan(nrp_sys(float("nan"), 0.5))


def test_cpr_all_seeded_is_zero() -> None:
    # N == |B_0| -> no initially-honest agents -> CPR defined as 0 (conservative)
    ep = _mk(1, 0, n=3, seed=frozenset({0, 1, 2}), final=frozenset({0, 1, 2}))
    assert compromise_propagation_rate([ep]) == pytest.approx(0.0)


def test_cpr_fraction() -> None:
    # N=5, seed {0}, final {0,1,2} -> (3-1)/(5-1) = 0.5
    ep = _mk(1, 0, n=5, seed=frozenset({0}), final=frozenset({0, 1, 2}))
    assert compromise_propagation_rate([ep]) == pytest.approx(0.5)


def test_collusion_advantage() -> None:
    assert collusion_advantage(0.9, 0.6) == pytest.approx(0.3)
