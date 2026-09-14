"""Package import tests."""
from __future__ import annotations

import importlib

import pytest

MODULES = [
    "masgym", "masgym.cli", "masgym.config", "masgym.demo",
    "masgym.data.schemas", "masgym.data.topology", "masgym.data.synthetic", "masgym.data.adapters",
    "masgym.env.propagation", "masgym.env.checker", "masgym.env.judge", "masgym.env.emulation",
    "masgym.env.orchestration",
    "masgym.methods.aggregators", "masgym.methods.scoring", "masgym.methods.corb",
    "masgym.methods.red_policies", "masgym.methods.blue_policies",
    "masgym.theory.propagation_bounds", "masgym.theory.sample_complexity", "masgym.theory.metric_axioms",
    "masgym.metrics.metrics", "masgym.metrics.confidence_intervals",
    "masgym.baselines.base", "masgym.baselines.no_defense", "masgym.baselines.fixed_threshold",
    "masgym.baselines.lifted_defenses", "masgym.baselines.external_wrappers",
    "experiments.run_evaluation", "experiments.run_ablation", "experiments.run_theory_check",
    "experiments.run_corb", "experiments.plot_results",
]


@pytest.mark.parametrize("module", MODULES)
def test_import(module: str) -> None:
    importlib.import_module(module)


def test_version() -> None:
    import masgym

    assert isinstance(masgym.__version__, str)
