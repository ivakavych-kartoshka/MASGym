"""Command-line interface for MASGym.

    python -m masgym.cli --help
    python -m masgym.cli version
    python -m masgym.cli demo --out outputs/synthetic_demo
    python -m masgym.cli sweep    --config configs/synthetic_demo.yaml --out outputs/sweep
    python -m masgym.cli ablation --config configs/synthetic_demo.yaml --out outputs/ablation
    python -m masgym.cli theory   --out outputs/theory
    python -m masgym.cli corb     --config configs/synthetic_demo.yaml --out outputs/corb
    python -m masgym.cli plot     --input outputs/sweep/sweep_metrics.csv --output outputs/sweep

Real experiments (real LLM backbones / ToolEmu / ASB / AgentDojo) are run on EC2 via the same
config with real adapters wired in; see docs/ec2_experiment_guide.md. This CLI runs only the
synthetic pipeline locally.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .utils.io import load_yaml
from .utils.logging import configure_logging, get_logger

logger = get_logger("masgym.cli")


def _experiments():
    """Import the top-level ``experiments`` package (source checkout)."""
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    import experiments  # noqa: F401

    return repo_root


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="masgym", description="MASGym: multi-agent LLM security gym (synthetic pipeline).")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="print version")

    d = sub.add_parser("demo", help="run the full synthetic smoke-test demo")
    d.add_argument("--out", default="outputs/synthetic_demo")
    d.add_argument("--seed", type=int, default=0)

    for name, helptext in [("sweep", "adversary sweep"), ("ablation", "ablations"), ("corb", "CoRB co-evolving loop")]:
        s = sub.add_parser(name, help=helptext)
        s.add_argument("--config", required=True)
        s.add_argument("--out", required=True)
        s.add_argument("--seed", type=int, default=None)

    t = sub.add_parser("theory", help="numerical verification of the paper's closed-form theory")
    t.add_argument("--out", default="outputs/theory")
    t.add_argument("--seed", type=int, default=0)
    t.add_argument("--trials", type=int, default=8000)

    pl = sub.add_parser("plot", help="plot results from a result CSV")
    pl.add_argument("--input", required=True)
    pl.add_argument("--output", required=True)
    pl.add_argument("--kind", choices=["sweep", "corb"], default="sweep")
    return p


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    args = build_parser().parse_args(argv)

    if args.command == "version":
        print(f"masgym {__version__}")
        return 0

    if args.command == "demo":
        from .demo import run_demo

        run_demo(args.out, seed=args.seed)
        return 0

    _experiments()
    if args.command == "sweep":
        from experiments.run_evaluation import run_sweep

        run_sweep(load_yaml(args.config), args.out, seed=args.seed)
    elif args.command == "ablation":
        from experiments.run_ablation import run_ablation

        run_ablation(load_yaml(args.config), args.out, seed=args.seed)
    elif args.command == "corb":
        from experiments.run_corb import run_corb_experiment

        run_corb_experiment(load_yaml(args.config), args.out, seed=args.seed)
    elif args.command == "theory":
        from experiments.run_theory_check import run_theory_check

        run_theory_check(args.out, trials=args.trials, seed=args.seed)
    elif args.command == "plot":
        from experiments.plot_results import plot_corb_pareto, plot_sweep

        if args.kind == "corb":
            plot_corb_pareto(args.input, args.output)
        else:
            plot_sweep(args.input, args.output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
