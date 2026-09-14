"""Baselines / defenses (paper Section 10).

Implementable directly as *synthetic effect-models* (clearly labelled): no-defense,
fixed-threshold, and the lifted per-agent defenses. External systems (ASB, AgentDojo, real
guardrails, MA defenses) are adapter stubs in :mod:`masgym.baselines.external_wrappers`.
"""
from __future__ import annotations

from .base import Defense, SyntheticDefense
from .fixed_threshold import FixedThresholdDefense
from .lifted_defenses import LIFTED_DEFENSES, lifted_defense
from .no_defense import NoDefense

__all__ = [
    "Defense",
    "SyntheticDefense",
    "NoDefense",
    "FixedThresholdDefense",
    "lifted_defense",
    "LIFTED_DEFENSES",
]
