"""Adapters for external baselines / harnesses (paper Section 10).

These are *real-baseline wrappers*: they define the expected input/output schema for systems
that MASGym compares against but that require external code, models, or data. None of them is
implemented locally; each raises ``NotImplementedError`` with a pointer to the EC2 setup docs.
A wrapper must never be confused with the synthetic defenses in this package.

Baselines covered:
* ASB (single-agent mode) -- github.com/agiresearch/ASB
* AgentDojo (single-agent) -- deterministic security() checks
* Real per-agent guardrails -- Llama Guard, NeMo Guardrails, TrustAgent
* Reference multi-agent defenses -- AutoDefense, G-Safeguard
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_TODO = (
    "External baseline not available locally. Provision it on EC2 and implement this adapter. "
    "See docs/baseline_adapters.md, docs/ec2_experiment_guide.md, and TODO_IMPLEMENTATION.md."
)


@dataclass
class ExternalBaselineAdapter:
    """Base adapter defining the expected run interface for an external baseline.

    Expected ``run(config) -> dict`` output schema (once implemented):
        {"asr_sys": float, "pna_sys": float, "nrp_sys": float, "cpr": float, "cost": {...},
         "provenance": {"baseline": str, "version": str, "command": str}}
    """

    name: str
    repo_or_source: str = ""

    def run(self, config: dict[str, Any]) -> dict[str, Any]:  # pragma: no cover - external
        raise NotImplementedError(f"[{self.name}] {_TODO}")


class ASBSingleAgentAdapter(ExternalBaselineAdapter):
    """ASB re-run in single-agent mode (arXiv:2410.02644)."""

    def __init__(self) -> None:
        super().__init__(name="ASB_single_agent", repo_or_source="github.com/agiresearch/ASB")


class AgentDojoAdapter(ExternalBaselineAdapter):
    """AgentDojo single-agent deterministic-check baseline (arXiv:2406.13352)."""

    def __init__(self) -> None:
        super().__init__(name="AgentDojo", repo_or_source="AgentDojo (NeurIPS 2024 D&B)")


class RealGuardrailAdapter(ExternalBaselineAdapter):
    """A real per-agent guardrail (Llama Guard / NeMo Guardrails / TrustAgent)."""

    def __init__(self, guardrail: str) -> None:
        super().__init__(name=f"guardrail:{guardrail}", repo_or_source=guardrail)


class MADefenseAdapter(ExternalBaselineAdapter):
    """A reference multi-agent defense (AutoDefense / G-Safeguard)."""

    def __init__(self, defense: str) -> None:
        super().__init__(name=f"ma_defense:{defense}", repo_or_source=defense)
