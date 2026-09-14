#!/usr/bin/env python3
"""Generate plots from a MASGym result CSV (never from hard-coded numbers).

    python scripts/make_plots.py --input outputs/sweep/sweep_metrics.csv --output outputs/sweep --kind sweep
"""
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401


def main() -> int:
    ap = argparse.ArgumentParser(description="MASGym plotting")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--kind", choices=["sweep", "corb"], default="sweep")
    args = ap.parse_args()
    from experiments.plot_results import plot_corb_pareto, plot_sweep

    if args.kind == "corb":
        path = plot_corb_pareto(args.input, args.output)
    else:
        path = plot_sweep(args.input, args.output)
    print(f"wrote {path} (SYNTHETIC stamp applied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
