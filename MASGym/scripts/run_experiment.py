#!/usr/bin/env python3
"""Run a MASGym experiment stage from a config.

    python scripts/run_experiment.py --config configs/experiment_template.yaml --stage sweep --out outputs/sweep

Stages: ``sweep`` (adversary sweep / RQ3-RQ6), ``ablation`` (RQ2/RQ5),
``theory`` (closed-form verification), ``corb`` (co-evolving loop).

NOTE: MASGym is a benchmark environment, not a conformal method; the template's
``calibrate``/``evaluate`` stages map to ``sweep``/``ablation`` here (see README).
"""
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401

from masgym.utils.io import load_yaml


def main() -> int:
    ap = argparse.ArgumentParser(description="MASGym experiment runner")
    ap.add_argument("--config", required=True)
    ap.add_argument("--stage", required=True, choices=["sweep", "ablation", "theory", "corb"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    cfg = load_yaml(args.config)

    if args.stage == "sweep":
        from experiments.run_evaluation import run_sweep

        run_sweep(cfg, args.out, seed=args.seed)
    elif args.stage == "ablation":
        from experiments.run_ablation import run_ablation

        run_ablation(cfg, args.out, seed=args.seed)
    elif args.stage == "theory":
        from experiments.run_theory_check import run_theory_check

        run_theory_check(args.out, seed=args.seed or 0)
    elif args.stage == "corb":
        from experiments.run_corb import run_corb_experiment

        run_corb_experiment(cfg, args.out, seed=args.seed)
    print(f"stage '{args.stage}' complete -> {args.out} (SYNTHETIC unless real adapters were wired in)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
