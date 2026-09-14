"""Blue (defense) policies for the CoRB loop (paper Section 8).

A blue policy proposes or upgrades a defense. The defenses are the synthetic effect-models
of :mod:`masgym.baselines`; the policy decides *which* to deploy each round.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from ..baselines.base import Defense, SyntheticDefense
from ..baselines.no_defense import NoDefense
from ..data.schemas import AdversaryConfig


class BluePolicy(Protocol):
    def propose(self, history: list[dict], adv: AdversaryConfig) -> Defense: ...


@dataclass
class StaticBluePolicy:
    """Deploy a single fixed defense every round (the "static blue" setting)."""

    defense: Defense

    def propose(self, history: list[dict], adv: AdversaryConfig) -> Defense:
        return self.defense


@dataclass
class EscalatingBluePolicy:
    """Upgrade defense strength when the previous round's ASR was high (co-adapting blue)."""

    start_reduction: float = 0.2
    step: float = 0.1
    max_reduction: float = 0.8
    _reduction: float = -1.0

    def propose(self, history: list[dict], adv: AdversaryConfig) -> Defense:
        if self._reduction < 0.0:
            self._reduction = self.start_reduction
            return self._make()
        last_asr = 0.0
        if history:
            v = history[-1].get("asr_sys")
            last_asr = float(v) if v == v else 0.0  # nan-safe
        if last_asr > 0.4:
            self._reduction = round(min(self.max_reduction, self._reduction + self.step), 3)
        return self._make()

    def _make(self) -> SyntheticDefense:
        if self._reduction <= 0.0:
            return NoDefense()
        return SyntheticDefense(
            name=f"escalating_blue(p_red={self._reduction:.2f})",
            p_reduction=self._reduction,
            detect=min(0.9, self._reduction),
            recover=0.3,
        )
