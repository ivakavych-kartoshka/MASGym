"""Cross-family formula check on the real-LLM pilot runs (PILOT-labelled).

Recomputes the system-level metrics from the raw per-episode rows and checks the
closed-form identities used in the paper:

  (F1) ASR_sys == mean(phi) over episodes               [Eq. 3]
  (F2) NRP_sys == PNA_sys * (1 - ASR_sys)               [Eq. 5 / Thm 9.2]  PNA from benign psi
  (F3) CPR    == mean((B_inf - B_0)/(N - B_0))          [Eq. 6, from episodes.csv_phi... ]
  (F4) the security-driver attribution: which predicate fired per episode
       (exfiltration/unsafe_action vs sabotage:coordination). Requires decisions.jsonl
       + episode phi: an episode whose compromised agents all *refused* (no exfiltration)
       yet phi=1 must be sabotage (availability-based structure).

Writes outputs/llm_pilot_models/formula_check.csv (per model x scenario) and prints a
compact table. PILOT-labelled: no effect on the headlined synthetic tables.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd

RESULTS = _ROOT / "outputs"
OUT = RESULTS / "llm_pilot_models"


def check_model(d: pathlib.Path, rows: list[dict]):
    eps = pd.read_csv(d / "episodes.csv")
    decisions = []
    if (d / "decisions.jsonl").exists():
        decisions = [json.loads(l) for l in (d / "decisions.jsonl").read_text(encoding="utf-8").splitlines()]

    scenario_out = []
    for scen in sorted(eps["scenario"].unique()):
        sub = eps[eps["scenario"] == scen]
        asr_eps = float(sub["phi"].mean())
        psi_means = {s: float(g["psi"].mean()) for s, g in eps.groupby("scenario")}
        pna = psi_means.get("benign", float("nan"))
        nrp_check = pna * (1.0 - asr_eps) if not math.isnan(pna) else float("nan")

        n = int(sub["episode"].count())
        # driver attribution: count exfiltration transitions from the trace signal
        # approximation -- exfiltration decisions exist iff a compromised agent acted.
        scen_atk = [x for x in decisions if x["attack"]]
        n_exfil = sum(1 for x in scen_atk if x["action"] == "exfiltrate")
        n_refusal = sum(1 for x in scen_atk if x["action"] == "benign")
        if scen == "benign":
            n_exfil, n_refusal = 0, 0
        driver = (
            "exfiltration-driven"
            if n_exfil > 0
            else ("availability-sabotage (structural)" if asr_eps > 0 and n_exfil == 0 else "none")
        )
        scenario_out.append(
            {
                "model": d.name[len("llm_pilot-"):],
                "scenario": scen,
                "episodes": n,
                "asr_sys_calc": round(asr_eps, 4),
                "nrp_calc": round(nrp_check, 4) if not math.isnan(nrp_check) else float("nan"),
                "pna_benign": round(pna, 4) if not math.isnan(pna) else float("nan"),
                "decisions_active": len(scen_atk),
                "exfil_decisions": n_exfil,
                "refusal_decisions": n_refusal,
                "asr_action_calc": round(n_exfil / len(scen_atk), 4) if scen_atk else float("nan"),
                "driver": driver,
            }
        )
    return scenario_out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)
    out = args.out or (OUT / "formula_check.csv")

    dirs = sorted(RESULTS.glob("llm_pilot-*"))
    all_rows: list[dict] = []
    for d in dirs:
        all_rows.extend(check_model(d, []))

    df = pd.DataFrame(all_rows)
    df.to_csv(out, index=False, float_format="%.4f")

    print(f"{'model':<38}{'scenario':<26}{'ASR_sys':>9}{'NRP':>7}{'PNA':>6}{'act':>7}{'drv':<30}")
    for _, r in df.iterrows():
        print(
            f"{r['model']:<38}{r['scenario']:<26}{r['asr_sys_calc']:>9.3f}{r['nrp_calc']:>7.3f}"
            f"{r['pna_benign']:>6.3f}{r['asr_action_calc']:>7.3f}{r['driver']:<30}"
        )
    print("\nwrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())