"""MASGym: a co-evolving red/blue security gym for multi-agent LLM systems.

This package implements the *runnable, synthetic* core of the MASGym paper
(``../main.pdf``): the orchestration layer, communication topologies, the
parameterized adversary, the deterministic checker, compromise-propagation
models, the full system-level metric suite, the CoRB co-evolving red/blue
protocol, and numerical verification of the paper's closed-form theory.

Components that require real LLM backbones, the ToolEmu emulator, or the
ASB/AgentDojo harnesses are provided as adapter interfaces (see
:mod:`masgym.data.adapters` and :mod:`masgym.baselines.external_wrappers`).

IMPORTANT: no output produced by this package is a paper-level result. Every
demo/experiment run on the built-in synthetic generator is a
"synthetic smoke-test output, not a paper result".
"""
from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
