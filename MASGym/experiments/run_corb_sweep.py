"""CoRB static-vs-adaptive red study (paper Appendix tab:adaptive).

Runs the co-evolving red/blue protocol (Algorithm 2) with a random (``static``) red and
with an ``adaptive`` red, both against the escalating blue policy, for R=20 rounds,
star N=5. Emits combined per-round metrics for rounds {1,5,10,20} so the appendix table
reports a maintained or eroded NRP over rounds. All numbers are synthetic.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from masgym.config import env_from_dict
from masgym.methods.blue_policies import EscalatingBluePolicy
from masgym.methods.corb import run_corb
from masgym.methods.red_policies import AdaptiveRedPolicy, RandomRedPolicy
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import configure_logging, get_logger
from masgym.utils.seeding import SeededRNG

logger = get_logger(__name__)
ROUNDS_TO_REPORT = (1, 5, 10, 20)


def run_corb_sweep(out_dir: str | pathlib.Path, rounds: int, n_episodes: int, seed: int = 0) -> dict[str, object]:
    out = ensure_dir(out_dir)
    env = env_from_dict(
        {"topology": "star", "n_agents": 5, "forced_degree": 2, "p_infect": 0.3,
         "base_unsafe_action_prob": 0.1}
    )
    blue = EscalatingBluePolicy()
    datasets: dict[str, object] = {}
    for red_name, red in (
        ("static", RandomRedPolicy(SeededRNG(seed))),
        ("adaptive", AdaptiveRedPolicy()),
    ):
        res = run_corb(env, red, blue, rounds=rounds, n_episodes=n_episodes, seed=seed)
        write_csv(out / f"corb_trajectory_{red_name}.csv", res.rows)
        # report the blue (post-defense) row of each selected round
        by_round: list[dict] = []
        for r in ROUNDS_TO_REPORT:
            hits = [row for row in res.rows if row["round"] == r and row["phase"] == "blue"]
            if hits:
                row = hits[0]
                by_round.append({"round": r, "asr_sys": round(row["asr_sys"], 4),
                                 "nrp_sys": round(row["nrp_sys"], 4),
                                 "asr_action": round(row["asr_action"], 4),
                                 "defense": row["defense"]})
        datasets[red_name] = by_round

    write_json(out / "corb_summary.json",
               {"note": "synthetic; CoRB loop blue-phase rows; ASR_sys saturated near 1 via "
                        "availability sabotage, so NRP_action is the discriminating column",
                "table": datasets,
                "provenance": run_metadata({"rounds": rounds, "n_episodes": n_episodes}, seed)})
    _write_notes(out, rounds, n_episodes)
    logger.info("CoRB static/adaptive study -> %s (SYNTHETIC)", out)
    return datasets


def _write_notes(out: pathlib.Path, rounds: int, m: int) -> None:
    (out / "README.md").write_text(
        f"# CoRB static-vs-adaptive red (synthetic, rounds={rounds}, M={m})\n"
        "Blue = EscalatingBluePolicy. tab:adaptive reports blue-phase rows at rounds "
        "{1,5,10,20}. NRP_action = PNA*(1-ASR_action).\n",
        encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/corb_study")
    ap.add_argument("--rounds", type=int, default=20)
    ap.add_argument("--m", type=int, default=60)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    configure_logging()
    run_corb_sweep(args.out, args.rounds, args.m, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())