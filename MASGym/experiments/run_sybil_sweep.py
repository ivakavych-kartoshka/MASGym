"""Sybil sweep (paper RQ5 / Appendix tab:sybil).

Star, N=5, beta=0.1 (witness usually survives, so ASR is not trivially saturated),
sybil count in {0,1,2,4}: an adversary controlling one policy gains extra seeded
identities via ``n_adv = ceil(beta*N) + sybils``. Measured with the single-agent
predicate (``asr_action``) alongside the full system predicate (``asr_sys``).

NOTE: the harness does not (yet) instrument per-selection / per-vote influence
shares, so ``tab:sybil`` is restated over system metrics rather than the selection
arguments in the placeholder sketch. All numbers are synthetic -- provenance-stamped.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from masgym.config import adv_from_dict, build_defense, env_from_dict
from masgym.methods.scoring import score_config
from masgym.theory.sample_complexity import hoeffding_min_samples
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import configure_logging, get_logger

logger = get_logger(__name__)

DEFENSES = {"none": None, "per_agent": "lifted:guardrail", "system_level": "fixed_threshold"}
SYBIL_COUNTS = (0, 1, 2, 4)


def run_sybil_sweep(out_dir: str | pathlib.Path, n_episodes: int, seed: int = 0) -> list[dict]:
    out = ensure_dir(out_dir)
    env = env_from_dict(
        {"topology": "star", "n_agents": 5, "forced_degree": 2, "p_infect": 0.3,
         "base_unsafe_action_prob": 0.1}
    )
    rows: list[dict] = []
    idx = 0
    for n_syb in SYBIL_COUNTS:
        adv = adv_from_dict({"beta": 0.1, "colluding": False, "sybils": n_syb})
        for dname in DEFENSES:
            res = score_config(env, adv, n_episodes, seed=seed + idx, defense=build_defense(DEFENSES[dname]))
            rows.append({"sybils": n_syb, "defense_kind": dname, **res.row()})
            idx += 1

    write_csv(out / "sybil_sweep.csv", rows)
    write_json(out / "sybil_summary.json",
               {"note": "synthetic; ASR_sys saturated near 1 when witness lost; ASR_action = "
                        "single-agent predicate (unsafe/exfil)",
                "table": {n: {r["defense_kind"]: {"asr_sys": r["asr_sys"], "asr_action": r["asr_action"],
                                                 "nrp_action": r["pna_sys"] * (1 - r["asr_action"]),
                                                 "cpr": r["cpr"]} for r in rows if r["sybils"] == n}
                          for n in SYBIL_COUNTS},
                "provenance": run_metadata({"grid": "sybil x defense, beta=0.1"}, seed)})
    _write_notes(out, n_episodes)
    logger.info("wrote %d sybil rows -> %s (SYNTHETIC)", len(rows), out)
    return rows


def _write_notes(out: pathlib.Path, m: int) -> None:
    (out / "README.md").write_text(
        f"# Sybil sweep (synthetic, M={m})\n"
        "- star N=5, beta=0.1, sybils in {{0,1,2,4}}. sybils adds seeded identities.\n"
        "- ASR_action = single-agent predicate (unsafe/exfil); NRP_action = PNA*(1-ASR_action).\n",
        encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/sybil")
    ap.add_argument("--m", type=int, default=None)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    configure_logging()
    m = args.m or hoeffding_min_samples(0.05, 0.05)
    run_sybil_sweep(args.out, m, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())