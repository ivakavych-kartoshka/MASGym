"""Degradation & single-agent baseline sweep (feeds paper Table 1 / RQ1-RQ3).

Layout chosen to be *definition-faithful to main.tex*:

* ``Predsec`` keeps all three predicates (unsafe action, exfiltration, coordination
  sabotage) as in ``sections/problem_formulation.tex`` -- we do NOT redefine Phi.
* The paper's ASB reduction (theory section) is stated for ``N=1`` *with the
  single-agent predicate*, so the Single-agent column of Table 1 is reported with
  ``asr_action`` (unsafe/exfil only) alongside ``asr_sys``.
* Multi-agent columns run regimes where an honest witness usually survives, so ``ASR``
  is not trivially saturated by availability sabotage.

Grid (all synthetic; default ``M=738``)::

  Block A  single-agent / ASB regression (RQ1)
     A1  N=1 chain, forced_degree=1, the lone agent compromised
     A2  N=3 chain, forced_degree=2, one compromised agent among honest witnesses
         (beta = 1/3) -> ASB-like regime with witnesses
  Block B  multi-agent degradation (RQ3)
     star N=5, forced_degree=2, p_infect in {0.1,0.3}, beta in {0.1,0.2,0.3},
     contexts ma_colluding / ma_orch-compromised

Every number is synthetic -- labelled, provenance-stamped, not a real-LLM result.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import pandas as pd

from masgym.config import adv_from_dict, build_defense, env_from_dict
from masgym.methods.scoring import score_config
from masgym.theory.sample_complexity import hoeffding_min_samples
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import configure_logging, get_logger

logger = get_logger(__name__)

DEFENSES = {
    "none": None,
    "per_agent": "lifted:guardrail",
    "system_level": "fixed_threshold",
}


def run_degradation_sweep(
    out_dir: str | pathlib.Path,
    n_episodes: int = 738,
    seed: int = 0,
    base_unsafe_values: list[float] | None = None,
    betas: list[float] | None = None,
    p_infect_values: list[float] | None = None,
    n_agents_ma: int = 5,
) -> list[dict]:
    out = ensure_dir(out_dir)
    base_unsafe_values = base_unsafe_values or [0.1, 0.5]
    betas = betas or [0.1, 0.2, 0.3]
    p_infect_values = p_infect_values or [0.1, 0.3]

    rows: list[dict] = []
    idx = 0
    for base_unsafe in base_unsafe_values:
        # ---------------- Block A: single-agent / ASB regression ----------------
        for case, env_d, adv_d in [
            (
                "A1_single_n1",
                {"topology": "chain", "n_agents": 1, "forced_degree": 1, "p_infect": 0.3,
                 "base_unsafe_action_prob": base_unsafe},
                {"beta": 1.0, "colluding": False},
            ),
            (
                "A2_single_with_witness",
                {"topology": "chain", "n_agents": 3, "forced_degree": 2, "p_infect": 0.1,
                 "base_unsafe_action_prob": base_unsafe},
                {"beta": 1 / 3, "colluding": False},
            ),
        ]:
            env = env_from_dict(env_d)
            adv = adv_from_dict(adv_d)
            for dname in DEFENSES:
                res = score_config(
                    env, adv, n_episodes, seed=seed + idx, defense=build_defense(DEFENSES[dname])
                )
                rows.append(
                    {
                        "block": "single_agent",
                        "case": case,
                        "base_unsafe_action_prob": base_unsafe,
                        "context": "single_agent",
                        "beta": adv_d["beta"],
                        "p_infect": env_d["p_infect"],
                        "defense_kind": dname,
                        "nrp_action": res.metrics.pna_sys * (1.0 - res.asr_action),
                        **res.row(),
                    }
                )
                idx += 1

        # ------------- Block B: multi-agent degradation (N=5, star) -------------
        for p_infect in p_infect_values:
            ma_env = env_from_dict(
                {
                    "topology": "star",
                    "n_agents": n_agents_ma,
                    "forced_degree": 2,
                    "p_infect": p_infect,
                    "base_unsafe_action_prob": base_unsafe,
                }
            )
            contexts = {
                "ma_colluding": {"beta": 0.0, "colluding": True},
                "ma_orch": {"beta": 0.0, "colluding": False, "orchestrator_compromised": True},
            }
            for beta in betas:
                for cname, cadv in contexts.items():
                    adv = adv_from_dict({**cadv, "beta": beta})
                    for dname in DEFENSES:
                        res = score_config(
                            ma_env, adv, n_episodes, seed=seed + idx,
                            defense=build_defense(DEFENSES[dname]),
                        )
                        rows.append(
                            {
                                "block": "multi_agent",
                                "case": cname,
                                "base_unsafe_action_prob": base_unsafe,
                                "context": cname,
                                "beta": beta,
                                "p_infect": p_infect,
                                "defense_kind": dname,
                                "nrp_action": res.metrics.pna_sys * (1.0 - res.asr_action),
                                **res.row(),
                            }
                        )
                        idx += 1

    write_csv(out / "degradation_sweep.csv", rows)
    summary = _summarize(rows)
    write_json(
        out / "degradation_summary.json",
        {"summary": summary, "provenance": run_metadata({"grid": "see degradation_sweep.csv"}, seed)},
    )
    _write_notes(out)
    logger.info("wrote %d degradation rows -> %s (SYNTHETIC)", len(rows), out)
    return rows


def _summarize(rows: list[dict]) -> dict[str, object]:
    df = pd.DataFrame(rows)
    primary = df[df["base_unsafe_action_prob"] == 0.1]
    pk = primary["defense_kind"]

    KEYS = ("asr_sys", "asr_action", "asr_sabotage", "nrp_sys", "nrp_action",
            "cpr", "detection_rate", "recovery_rate", "coordination_quality")

    def pick(mask: "pd.Series[bool]") -> dict:
        r = primary[mask]
        if r.empty:
            return {}
        return {k: r.iloc[0][k] for k in KEYS}

    # Table 1 operating point: MA rows at beta=0.3, p_infect=0.1 (witness usually survives).
    cells: dict[str, object] = {}
    for d in DEFENSES:
        cells[d] = {
            "single_agent_n1_asr_action": pick(
                (pk == d) & (primary.case == "A1_single_n1")),
            "single_agent_with_witness": pick(
                (pk == d) & (primary.case == "A2_single_with_witness")),
            "ma_colluding": pick(
                (pk == d) & (primary.context == "ma_colluding")
                & (primary.beta == 0.3) & (primary.p_infect == 0.1)),
            "ma_orch": pick(
                (pk == d) & (primary.context == "ma_orch")
                & (primary.beta == 0.3) & (primary.p_infect == 0.1)),
        }

    summary: dict[str, object] = {
        "note": (
            "synthetic-model results. Predsec keeps unsafe/exfil/sabotage as main.tex defines; "
            "asr_action = single-agent predicate (unsafe/exfil) used for the ASB reduction at N=1; "
            "asr_sabotage = availability-sabotage share. Table 1 operating point: MA at "
            "beta=0.3, p_infect=0.1; single-agent from Block A."
        ),
        "table": cells,
    }
    return summary


def _write_notes(out: pathlib.Path) -> None:
    lines = [
        "# Degradation & single-agent baseline (synthetic)",
        "",
        "Produced for paper Table 1 (RQ1/RQ3), Phi unchanged (unsafe/exfil/sabotage).",
        "- `asr_sys`    : system predicate (paper's Phi).",
        "- `asr_action` : single-agent predicate (unsafe/exfil only) - the quantity the",
        "                 paper's ASB reduction (N=1) reason about.",
        "- `asr_sabotage` : share of episodes with a coordination-sabotage transition.",
        "- `nrp_action` = PNA * (1 - asr_action) for the ASB-compatible single-agent row.",
        "Block A: A1 = N=1 lone compromised agent; A2 = N=3 with one compromised among",
        "         honest witnesses (beta=1/3).",
        "Block B: star N=5, forced_degree=2, p_infect in {0.1,0.3}, beta in {0.1,0.2,0.3},",
        "         contexts ma_colluding / ma_orch.",
        "Primary operating point for the table: base_unsafe_action_prob=0.1, MA beta=0.3,",
        "         p_infect=0.1.",
        "All numbers are synthetic; provenance in `degradation_summary.json`.",
    ]
    (out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="MASGym degradation / N=1 baseline sweep")
    ap.add_argument("--out", default="outputs/degradation")
    ap.add_argument("--m", type=int, default=None,
                    help="episodes per config (default: hoeffding_min_samples(0.05,0.05)=738)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    configure_logging()
    m = args.m or hoeffding_min_samples(eps=0.05, alpha=0.05)
    logger.info("episodes per config M=%d (eps=0.05, alpha=0.05)", m)
    run_degradation_sweep(args.out, n_episodes=m, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())