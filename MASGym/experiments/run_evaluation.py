"""Adversary-sweep evaluation (paper RQ3-RQ6): score a grid of adversary configs.

Writes ``sweep_metrics.csv`` (one row per configuration) and a provenance JSON. On the
built-in synthetic generator every row is a "synthetic smoke-test output, not a paper result".
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from masgym.config import adv_from_dict, build_defense, env_from_dict, expand_sweep
from masgym.methods.scoring import score_config
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import get_logger

logger = get_logger(__name__)


def run_sweep(cfg: dict[str, Any], out_dir: str | Path, seed: Optional[int] = None) -> list[dict]:
    """Run the adversary sweep defined by ``cfg`` and persist metrics."""
    out = ensure_dir(out_dir)
    env = env_from_dict(cfg.get("env", {}))
    ev = cfg.get("eval", {})
    n_ep = int(ev.get("n_episodes", 100))
    base_seed = int(seed if seed is not None else ev.get("seed", 0))
    defense = build_defense(cfg.get("defense"))
    advs = expand_sweep(cfg.get("sweep", {})) or [adv_from_dict(cfg.get("adversary", {}))]

    rows: list[dict] = []
    for i, adv in enumerate(advs):
        res = score_config(env, adv, n_ep, seed=base_seed + i, defense=defense)
        rows.append(res.row())
    write_csv(out / "sweep_metrics.csv", rows)
    write_json(out / "sweep_metadata.json", run_metadata(cfg, base_seed, synthetic=True))
    logger.info("wrote %d sweep rows to %s (SYNTHETIC)", len(rows), out / "sweep_metrics.csv")
    return rows
