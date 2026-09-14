#!/usr/bin/env python3
"""Run the MASGym synthetic smoke-test demo.

    python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml --out outputs/synthetic_demo

Outputs are clearly labelled "synthetic smoke-test output, not a paper result".
"""
from __future__ import annotations

import argparse

import _bootstrap  # noqa: F401  (adds src + repo root to sys.path)

from masgym.demo import run_demo
from masgym.utils.io import load_yaml


def main() -> int:
    ap = argparse.ArgumentParser(description="MASGym synthetic demo")
    ap.add_argument("--config", default=None, help="optional YAML config; falls back to the built-in demo config")
    ap.add_argument("--out", default="outputs/synthetic_demo")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    cfg = load_yaml(args.config) if args.config else None
    summary = run_demo(args.out, seed=args.seed, cfg=cfg)
    print("Demo summary (SYNTHETIC, not a paper result):")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
