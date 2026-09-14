"""Algorithm 2 -- CoRB: co-evolving red/blue evaluation (paper Section 8).

Alternates a red policy proposing an attack configuration and a blue policy proposing a
defense, scoring each pair with the deterministic checker (Algorithm 1) and logging a
trajectory of ``(c_adv, blue, NRP_sys, ASR_sys, cost)`` rows. Reports the ``(ASR_sys, cost)``
Pareto frontier. Because scoring is deterministic and off the LLM critical path, no proposal
can inflate its own evaluation (Theorem 9.4).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from ..baselines.no_defense import NoDefense
from ..data.schemas import EnvConfig
from ..utils.logging import get_logger
from .blue_policies import BluePolicy
from .red_policies import RedPolicy
from .scoring import score_config

logger = get_logger(__name__)
Aggregator = Callable[[float, float], float]


def pareto_frontier(rows: list[dict], x_key: str = "asr_sys", y_key: str = "mean_tokens") -> list[dict]:
    """Non-dominated set minimizing both ``x_key`` (risk) and ``y_key`` (cost)."""
    pts = [r for r in rows if r.get(x_key) == r.get(x_key) and r.get(y_key) == r.get(y_key)]
    frontier: list[dict] = []
    for r in pts:
        dominated = any(
            (o[x_key] <= r[x_key] and o[y_key] <= r[y_key]) and (o[x_key] < r[x_key] or o[y_key] < r[y_key])
            for o in pts
            if o is not r
        )
        if not dominated:
            frontier.append(r)
    return frontier


@dataclass
class CoRBResult:
    """Trajectory L and Pareto frontier from a CoRB run."""

    rows: list[dict] = field(default_factory=list)
    pareto: list[dict] = field(default_factory=list)


def run_corb(
    env: EnvConfig,
    red: RedPolicy,
    blue: BluePolicy,
    rounds: int = 10,
    n_episodes: int = 100,
    seed: int = 0,
    aggregator: Optional[Aggregator] = None,
) -> CoRBResult:
    """Run the CoRB co-evolving loop for ``rounds`` rounds (Algorithm 2)."""
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    rows: list[dict] = []
    blue_prev = NoDefense()
    for r in range(1, rounds + 1):
        # Red step: propose an attack config (adaptive red may best-respond to blue_prev).
        c_adv = red.propose(rows, getattr(blue_prev, "name", None))
        res_red = score_config(env, c_adv, n_episodes, seed=seed + r, defense=blue_prev, aggregator=aggregator)
        row_red = res_red.row()
        row_red.update({"round": r, "phase": "red"})
        rows.append(row_red)

        # Blue step: propose/upgrade a defense against c_adv, then re-score.
        blue_r = blue.propose(rows, c_adv)
        res_blue = score_config(env, c_adv, n_episodes, seed=seed + r, defense=blue_r, aggregator=aggregator)
        row_blue = res_blue.row()
        row_blue.update({"round": r, "phase": "blue"})
        rows.append(row_blue)
        blue_prev = blue_r
        logger.info(
            "round %d | red ASR=%.3f (%s) | blue ASR=%.3f (%s)",
            r, row_red["asr_sys"], row_red["defense"], row_blue["asr_sys"], row_blue["defense"],
        )
    return CoRBResult(rows=rows, pareto=pareto_frontier(rows))
