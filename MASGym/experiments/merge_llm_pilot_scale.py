"""Merge per-model scaled pilot sweeps into one comparison table.

Combines ``outputs/llm_pilot_scale/<Model>/compare.csv`` into
``outputs/llm_pilot_scale/all_models_compare.csv`` plus a ``_summary.json`` with
model -> config -> scenario aggregates.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

RESULTS = _ROOT / "outputs" / "llm_pilot_scale"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge per-model pilot sweep results.")
    parser.add_argument("--root", type=pathlib.Path, default=RESULTS)
    args = parser.parse_args(argv)

    root: pathlib.Path = args.root
    if not root.is_dir():
        print(f"no {root} dir found (run run_llm_pilot_sweep.py first)")
        return 1

    model_dirs = sorted(d for d in root.iterdir() if d.is_dir())
    all_rows: list[dict] = []
    models: dict[str, dict] = {}
    for d in model_dirs:
        cmp_path = d / "compare.csv"
        summary_path = d / "summary.json"
        if not cmp_path.is_file():
            continue
        with (d / "compare.csv").open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames or [])
            for row in reader:
                row = {k: (float(row[k]) if _is_num(row[k]) else row[k]) for k in row}
                all_rows.append({"model": d.name, **row})
        if summary_path.is_file():
            models[d.name] = json.loads(summary_path.read_text(encoding="utf-8"))

    if not all_rows:
        print("no compare.csv files found")
        return 1

    fieldnames = ["model", *fieldnames]
    with (root / "all_models_compare.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    json.dump(
        {"banner": "PILOT multi-model scaled comparison (open instruct families)",
         "models": models},
        open(root / "_summary.json", "w", encoding="utf-8"),
        indent=1,
        allow_nan=True,
    )
    print(f"wrote {root / 'all_models_compare.csv'} ({len(all_rows)} rows, {len(models)} models)")
    return 0


def _is_num(v: str) -> bool:
    try:
        float(v)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())