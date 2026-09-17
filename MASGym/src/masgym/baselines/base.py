"""Defense interface and a synthetic effect-model base.

A defense conforms to :class:`~masgym.env.orchestration.DefenseLike`: it may reduce the
effective per-edge propagation probability and provide detection / recovery probabilities.

SYNTHETIC EFFECT-MODEL NOTICE. The numeric ``p_reduction``, ``detect``, and ``recover``
values below are *chosen model parameters*, not measured efficacies of any real defense.
They exist to exercise the pipeline. No degradation conclusion (the paper's headline
hypothesis) is drawn from them; every output that uses them is a synthetic smoke-test.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..data.schemas import AdversaryConfig, EnvConfig
from ..utils.validation import clamp_unit, require_probability

SYNTHETIC_EFFECT_MODEL = True


class Defense(ABC):
    """Abstract blue-team defense."""

    name: str

    @abstractmethod
    def effective_p_infect(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...

    @abstractmethod
    def detect_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...

    @abstractmethod
    def recover_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...


@dataclass
class SyntheticDefense(Defense):
    """A defense modelled by a uniform per-edge ``p`` reduction plus detect/recover rates.

    The reduction is applied uniformly and does NOT encode any orchestrator- or
    topology-specific effect, so the pipeline never manufactures the paper's degradation
    hypothesis; any pattern that appears is a property of the transparent synthetic model.

    The same ``p_reduction`` fraction is also applied by the orchestrator to the
    per-step unsafe-action probability (a compromised agent is less likely to turn an
    injection into a recorded action), which is what lets the single-agent N=1 baseline
    move ``ASR_sys`` at all.
    """

    name: str
    p_reduction: float = 0.0  # fraction by which effective p is reduced
    detect: float = 0.0
    recover: float = 0.0
    synthetic_effect_model: bool = True

    def __post_init__(self) -> None:
        require_probability(self.p_reduction, "p_reduction")
        require_probability(self.detect, "detect")
        require_probability(self.recover, "recover")

    def effective_p_infect(self, env: EnvConfig, adv: AdversaryConfig) -> float:
        return clamp_unit(env.p_infect * (1.0 - self.p_reduction))

    def detect_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float:
        return self.detect

    def recover_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float:
        return self.recover
