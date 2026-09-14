"""Synthetic smoke-test demo: runs the whole MASGym pipeline on a tiny synthetic config.

Produces, under ``out_dir`` (default ``outputs/synthetic_demo/``): a sweep, an ablation, the
theory check, a CoRB trajectory, and two plots -- all clearly labelled
"synthetic smoke-test output, not a paper result".
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .utils.io import SYNTHETIC_BANNER, ensure_dir
from .utils.logging import configure_logging, get_logger

logger = get_logger(__name__)


def _ensure_experiments_on_path() -> None:
    """Make the top-level ``experiments`` package importable from a source checkout."""
    repo_root = Path(__file__).resolve().parents[2]  # src/masgym/demo.py -> repo root
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def demo_config() -> dict[str, Any]:
    """A small synthetic configuration (fast; not a paper setting)."""
    return {
        "env": {"n_agents": 8, "topology": "star", "horizon": 5, "p_infect": 0.3, "forced_degree": 2},
        "eval": {"n_episodes": 80, "seed": 0},
        "sweep": {
            "beta": [0.0, 0.25, 0.5],
            "colluding": [False, True],
            "orchestrator_compromised": [False, True],
        },
        "ablation": {"beta": 0.3},
        "corb": {"rounds": 6, "red": "adaptive", "blue": "escalating"},
    }


def run_demo(
    out_dir: str | Path = "outputs/synthetic_demo", seed: int = 0, cfg: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Run the full synthetic demo and write labelled outputs.

    If ``cfg`` is None, a small built-in :func:`demo_config` is used.
    """
    configure_logging()
    _ensure_experiments_on_path()
    from experiments.plot_results import plot_corb_pareto, plot_sweep
    from experiments.run_ablation import run_ablation
    from experiments.run_corb import run_corb_experiment
    from experiments.run_evaluation import run_sweep
    from experiments.run_theory_check import run_theory_check

    out = ensure_dir(out_dir)
    cfg = cfg or demo_config()
    logger.info("=== MASGym synthetic demo (%s) ===", SYNTHETIC_BANNER)

    sweep_rows = run_sweep(cfg, out, seed=seed)
    ablation = run_ablation(cfg, out, seed=seed)
    theory = run_theory_check(out, trials=3000, seed=seed)
    corb = run_corb_experiment(cfg, out, seed=seed)

    plots = []
    try:
        plots.append(str(plot_sweep(out / "sweep_metrics.csv", out)))
        plots.append(str(plot_corb_pareto(out / "corb_trajectory.csv", out)))
    except Exception as exc:  # pragma: no cover - plotting is best-effort
        logger.warning("plotting skipped: %s", exc)

    (out / "README.md").write_text(
        f"# Synthetic demo outputs\n\n**{SYNTHETIC_BANNER}.**\n\n"
        "Files here are produced by `masgym.demo.run_demo` on a tiny synthetic configuration to\n"
        "exercise the pipeline. They are NOT paper results and contain no real benchmark numbers.\n\n"
        "- `sweep_metrics.csv` - system-level metrics per adversary config\n"
        "- `ablation.csv` / `ablation_summary.json` - collusion, orchestrator, evaluator-integrity\n"
        "- `theory_check.json` - Monte-Carlo vs closed-form verification of Section 9\n"
        "- `corb_trajectory.csv` / `corb_pareto.json` - CoRB co-evolving loop\n"
        "- `*.png` - plots stamped SYNTHETIC\n",
        encoding="utf-8",
    )
    summary = {
        "out_dir": str(out),
        "n_sweep_rows": len(sweep_rows),
        "collusion_advantage_synthetic": ablation["collusion_advantage"],
        "judge_hijack_rate_synthetic": ablation["evaluator_integrity"]["judge_hijack_rate"],
        "n_corb_rows": corb["n_rows"],
        "theory_star_mc": theory["propagation"]["star_centre"]["mc"],
        "theory_star_closed": theory["propagation"]["star_centre"]["closed"],
        "plots": plots,
        "note": SYNTHETIC_BANNER,
    }
    logger.info("demo complete -> %s (%s)", out, SYNTHETIC_BANNER)
    return summary
