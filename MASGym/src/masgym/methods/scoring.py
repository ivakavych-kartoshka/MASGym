"""Algorithm 1 -- ScoreConfig: deterministic system-level scoring of one configuration.

Runs ``n_episodes`` adversarial episodes and ``n_episodes`` benign-counterpart episodes,
then computes the full system-level metric bundle. All scoring is deterministic given the
trace (the LLM is never on the scoring critical path; Theorem 9.4).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from ..data.schemas import AdversaryConfig, EnvConfig
from ..data.synthetic import generate_benign_episodes, generate_episodes
from ..env.orchestration import DefenseLike
from ..metrics.metrics import SystemMetrics, compute_system_metrics

Aggregator = Callable[[float, float], float]


@dataclass
class ScoreConfigResult:
    """Result of :func:`score_config`."""

    env: EnvConfig
    adversary: AdversaryConfig
    defense_name: str
    n_episodes: int
    seed: int
    metrics: SystemMetrics

    def row(self) -> dict[str, object]:
        """Flat dict row for CSV/JSON logging (used by CoRB and experiment runners)."""
        d: dict[str, object] = {
            "topology": self.env.topology.value,
            "n_agents": self.env.n_agents,
            "defense": self.defense_name,
            "n_episodes": self.n_episodes,
            "seed": self.seed,
        }
        d.update(self.adversary.as_dict())
        d.update(self.metrics.to_dict())
        return d


def score_config(
    env: EnvConfig,
    adv: AdversaryConfig,
    n_episodes: int = 200,
    seed: int = 0,
    defense: Optional[DefenseLike] = None,
    aggregator: Optional[Aggregator] = None,
) -> ScoreConfigResult:
    """Algorithm 1: score one ``(env, adv, defense)`` configuration over ``n_episodes``."""
    adv_eps = generate_episodes(env, adv, n_episodes, seed=seed, defense=defense)
    benign_eps = generate_benign_episodes(env, n_episodes, seed=seed + 1, defense=defense)
    metrics = compute_system_metrics(adv_eps, benign_eps, aggregator=aggregator)
    return ScoreConfigResult(
        env=env,
        adversary=adv,
        defense_name=getattr(defense, "name", "no_defense"),
        n_episodes=n_episodes,
        seed=seed,
        metrics=metrics,
    )
