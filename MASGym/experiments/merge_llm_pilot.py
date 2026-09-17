"""Rebuild outputs/llm_pilot_models/ from the per-model pilot runs.

Globs outputs/llm_pilot-*/summary.json, flattens the per-scenario aggregates into
summary.json (modell -> resa -> scenario) and compare.csv (long table). The short
model label is the directory suffix (e.g. "Llama-3.2-1B-Instruct").
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

OUT_DIR = _ROOT / "outputs" / "llm_pilot_models"
RESULTS = _ROOT / "outputs"


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Merge per-model LLM pilot summaries.")
    parser.add_argument("--out", type=pathlib.Path, default=OUT_DIR)
    args = parser.parse_args(argv)

    model_dirs = sorted(RESULTS.glob("llm_pilot-*"))
    if not model_dirs:
        print("no outputs/llm_pilot-* dirs found")
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    models: dict[str, dict[str, dict]] = {}
    for d in model_dirs:
        summary = json.loads((d / "summary.json").read_text(encoding="utf-8"))
        short = d.name[len("llm_pilot-"):]
        models[short] = summary["scenarios"]

    rows: list[dict] = []
    for short in sorted(models):
        for scen, r in models[short].items():
            rows.append(
                {
                    "model": short,
                    "scenario": scen,
                    "asr_sys": r.get("asr_sys", float("nan")),
                    "asr_act": r.get("asr_action", float("nan")),
                    "nrp_sys": r.get("nrp_sys", float("nan")),
                    "cpr": r.get("cpr", float("nan")),
                    "tokens": r.get("tokens_mean", float("nan")),
                    "latency": r.get("latency_mean_s", float("nan")),
                    "parse_failures": r.get("parse_failures", 0),
                }
            )

    with (args.out / "compare.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json.dump(
        {
            "banner": "PILOT multi-model comparison (open instruct families)",
            "models": models,
            "source_dirs": [d.name for d in model_dirs],
        },
        open(args.out / "summary.json", "w", encoding="utf-8"),
        indent=1,
        allow_nan=True,
    )
    print(f"wrote {args.out / 'summary.json'} and compare.csv ({len(rows)} rows, {len(models)} models)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())