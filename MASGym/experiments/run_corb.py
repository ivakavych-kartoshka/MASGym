"""Run the CoRB co-evolving red/blue protocol (paper Algorithm 2) and log its trajectory.

Writes ``corb_trajectory.csv`` (all rounds) and ``corb_pareto.json`` (the (ASR, cost)
frontier). Synthetic smoke-test output, not a paper result.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from masgym.config import env_from_dict
from masgym.methods.blue_policies import EscalatingBluePolicy, StaticBluePolicy
from masgym.methods.corb import run_corb
from masgym.methods.red_policies import AdaptiveRedPolicy, RandomRedPolicy
from masgym.baselines.no_defense import NoDefense
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import get_logger
from masgym.utils.seeding import SeededRNG

logger = get_logger(__name__)


def _make_red(cfg: dict[str, Any], seed: int):
    kind = cfg.get("corb", {}).get("red", "random")
    if kind == "adaptive":
        return AdaptiveRedPolicy()
    return RandomRedPolicy(SeededRNG(seed))


def _make_blue(cfg: dict[str, Any]):
    kind = cfg.get("corb", {}).get("blue", "escalating")
    if kind == "static":
        return StaticBluePolicy(NoDefense())
    return EscalatingBluePolicy()


def run_corb_experiment(cfg: dict[str, Any], out_dir: str | Path, seed: Optional[int] = None) -> dict[str, Any]:
    out = ensure_dir(out_dir)
    env = env_from_dict(cfg.get("env", {}))
    corb_cfg = cfg.get("corb", {})
    rounds = int(corb_cfg.get("rounds", 8))
    n_ep = int(cfg.get("eval", {}).get("n_episodes", 60))
    base_seed = int(seed if seed is not None else cfg.get("eval", {}).get("seed", 0))

    result = run_corb(env, _make_red(cfg, base_seed), _make_blue(cfg), rounds=rounds, n_episodes=n_ep, seed=base_seed)
    write_csv(out / "corb_trajectory.csv", result.rows)
    write_json(out / "corb_pareto.json", {"pareto": result.pareto, "provenance": run_metadata(cfg, base_seed)})
    logger.info("CoRB: %d rows, %d Pareto-optimal points (SYNTHETIC)", len(result.rows), len(result.pareto))
    return {"n_rows": len(result.rows), "n_pareto": len(result.pareto)}
