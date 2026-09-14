"""Environment layer: propagation, deterministic checker, LLM-judge contrast, emulation, orchestration."""
from __future__ import annotations

from .checker import DeterministicChecker
from .judge import HijackableDummyJudge, LLMJudgeAdapter
from .propagation import IndependentCascade, ThresholdCascade, make_propagation
from .orchestration import Orchestrator

__all__ = [
    "DeterministicChecker",
    "HijackableDummyJudge",
    "LLMJudgeAdapter",
    "IndependentCascade",
    "ThresholdCascade",
    "make_propagation",
    "Orchestrator",
]
