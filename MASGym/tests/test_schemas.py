"""Schema validation tests."""
from __future__ import annotations

import pytest

from masgym.data.schemas import AdversaryConfig, EnvConfig, TopologyName


def test_adversary_beta_bounds() -> None:
    with pytest.raises(ValueError):
        AdversaryConfig(beta=1.5)
    with pytest.raises(ValueError):
        AdversaryConfig(sybils=-1)


def test_adversary_benign_counterpart() -> None:
    adv = AdversaryConfig(beta=0.4, colluding=True, orchestrator_compromised=True, sybils=3)
    benign = adv.benign()
    assert benign.beta == 0.0 and not benign.colluding and benign.sybils == 0


def test_envconfig_validation() -> None:
    with pytest.raises(ValueError):
        EnvConfig(p_infect=2.0)
    with pytest.raises(ValueError):
        EnvConfig(n_agents=5, orchestrator_id=10)
    ok = EnvConfig(n_agents=6, topology=TopologyName.MESH, horizon=4)
    assert ok.n_agents == 6
