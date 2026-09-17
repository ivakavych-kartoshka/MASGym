"""Collusion-advantage sweep (paper RQ5 / Figure 6-c / Delta_coll, Def 6.5).

Star, N=5, no defense, beta in {0,0.1,...,0.5}, colluding on/off. Emits the data for
the collusion-vs-independent ASR curves and the numeric collusion advantage
``Delta_coll = ASR^coll - ASR^ind``. Reports the single-agent predicate (``asr_action``)
next to the system predicate (``asr_sys``), because the latter saturates via
availability sabotage once the star hub is hit. All numbers are synthetic.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from masgym.config import adv_from_dict, env_from_dict
from masgym.methods.scoring import score_config
from masgym.theory.sample_complexity import hoeffding_min_samples
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import configure_logging, get_logger

logger = get_logger(__name__)
BETAS = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)


def run_collusion_sweep(out_dir: str | pathlib.Path, n_episodes: int, seed: int = 0) -> list[dict]:
    out = ensure_dir(out_dir)
    env = env_from_dict(
        {"topology": "star", "n_agents": 5, "forced_degree": 2, "p_infect": 0.3,
         "base_unsafe_action_prob": 0.1}
    )
    rows: list[dict] = []
    idx = 0
    for beta in BETAS:
        for colluding in (False, True):
            adv = adv_from_dict({"beta": beta, "colluding": colluding})
            res = score_config(env, adv, n_episodes, seed=seed + idx)
            rows.append({"beta": beta, "colluding": colluding,
                         "asr_action": res.asr_action,
                         "nrp_action": res.metrics.pna_sys * (1 - res.asr_action),
                         **res.row()})
            idx += 1

    def pick(beta: float, coll: bool) -> dict | None:
        hits = [r for r in rows if r["beta"] == beta and r["colluding"] == coll]
        return hits[0] if hits else None

    deltas = {}
    for beta in (0.1, 0.2, 0.3, 0.4, 0.5):
        i, c = pick(beta, False), pick(beta, True)
        if i and c:
            deltas[str(beta)] = {
                "delta_coll_asr_action": round(c["asr_action"] - i["asr_action"], 4),
                "delta_coll_cpr": round(c["cpr"] - i["cpr"], 4),
            }

    write_csv(out / "collusion_sweep.csv", rows)
    write_json(out / "collusion_summary.json",
               {"note": "synthetic; asr_action = single-agent predicate; asr_sys saturates "
                        "via availability sabotage on the star hub",
                "delta_coll": deltas,
                "provenance": run_metadata({"grid": "beta x colluding, no defense"}, seed)})
    _write_notes(out, n_episodes)
    logger.info("wrote %d collusion rows -> %s (SYNTHETIC)", len(rows), out)
    return rows


def _write_notes(out: pathlib.Path, m: int) -> None:
    (out / "README.md").write_text(
        f"# Collusion-advantage sweep (synthetic, M={m})\n"
        "star N=5, no defense, base_unsafe_action_prob=0.1, beta in {{0,0.1,...,0.5}}.\n"
        "delta_coll_asr_action = ASR_action(coll) - ASR_action(ind); note the sign flip vs the\n"
        "system predicate, which saturates at 1 via availability sabotage.\n",
        encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/collusion")
    ap.add_argument("--m", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    configure_logging()
    m = args.m or hoeffding_min_samples(0.05, 0.05)
    run_collusion_sweep(args.out, m, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())