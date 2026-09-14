"""Per-agent defenses lifted into the multi-agent setting (paper Section 10).

The paper lifts single-agent defenses -- delimiting/sandwiching, paraphrase, a prompt-injection
detector, instructional prevention, and guardrails -- into MASGym as baselines. Here each is a
*synthetic effect-model* (chosen ``p_reduction``/``detect``/``recover``), used only to exercise
the pipeline. Real implementations require external systems (Llama Guard, NeMo, TrustAgent) and
are provided as adapters in :mod:`masgym.baselines.external_wrappers`.
"""
from __future__ import annotations

from .base import SyntheticDefense

# name -> (p_reduction, detect, recover)  [SYNTHETIC parameters, not measured efficacies]
_LIFTED_SPECS: dict[str, tuple[float, float, float]] = {
    "delimiting": (0.30, 0.20, 0.20),
    "paraphrase": (0.25, 0.15, 0.20),
    "pi_detector": (0.40, 0.50, 0.30),
    "instructional_prevention": (0.20, 0.10, 0.15),
    "guardrail": (0.45, 0.55, 0.35),
}

LIFTED_DEFENSES: tuple[str, ...] = tuple(_LIFTED_SPECS.keys())


def lifted_defense(name: str) -> SyntheticDefense:
    """Return the synthetic effect-model for a named lifted per-agent defense."""
    if name not in _LIFTED_SPECS:
        raise KeyError(f"unknown lifted defense {name!r}; choices: {LIFTED_DEFENSES}")
    pr, det, rec = _LIFTED_SPECS[name]
    return SyntheticDefense(name=f"lifted:{name}", p_reduction=pr, detect=det, recover=rec)
