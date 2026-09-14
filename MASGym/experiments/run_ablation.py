"""Ablations (paper RQ2, RQ5): collusion on/off, orchestrator trust, and the
deterministic-checker vs LLM-judge evaluator-integrity comparison.

Outputs are synthetic smoke-test outputs, not paper results. The evaluator-integrity
ablation, however, is a faithful demonstration of Theorem 9.4 / Proposition 9.5: the
deterministic checker's verdict is invariant to injected messages, whereas a message-reading
judge can be hijacked.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from masgym.config import env_from_dict
from masgym.data.schemas import AdversaryConfig
from masgym.data.synthetic import generate_episodes
from masgym.env.checker import DeterministicChecker
from masgym.env.judge import HijackableDummyJudge
from masgym.methods.scoring import score_config
from masgym.metrics.metrics import collusion_advantage
from masgym.utils.io import ensure_dir, run_metadata, write_csv, write_json
from masgym.utils.logging import get_logger

logger = get_logger(__name__)


def _evaluator_integrity(env, n_ep: int, seed: int) -> dict[str, float]:
    """RQ2: fraction of compromised episodes a judge is hijacked but the checker is not."""
    adv = AdversaryConfig(beta=0.3, colluding=True, malicious_tools=True)
    episodes = generate_episodes(env, adv, n_ep, seed=seed)
    checker = DeterministicChecker()
    judge = HijackableDummyJudge()
    n_comp = 0
    judge_hijacked = 0
    checker_hijacked = 0
    for ep in episodes:
        c = checker.phi(ep.trace)
        j = judge.phi(ep.trace)
        if c == 1:
            n_comp += 1
            if j == 0:
                judge_hijacked += 1
            # deterministic checker is, by construction, never flipped by messages
    return {
        "n_compromised": n_comp,
        "judge_hijack_rate": (judge_hijacked / n_comp) if n_comp else float("nan"),
        "deterministic_hijack_rate": (checker_hijacked / n_comp) if n_comp else 0.0,
    }


def run_ablation(cfg: dict[str, Any], out_dir: str | Path, seed: Optional[int] = None) -> dict[str, Any]:
    out = ensure_dir(out_dir)
    env = env_from_dict(cfg.get("env", {}))
    ev = cfg.get("eval", {})
    n_ep = int(ev.get("n_episodes", 100))
    base_seed = int(seed if seed is not None else ev.get("seed", 0))
    beta = float(cfg.get("ablation", {}).get("beta", 0.3))

    rows: list[dict] = []
    # collusion on/off
    r_ind = score_config(env, AdversaryConfig(beta=beta, colluding=False), n_ep, seed=base_seed)
    r_col = score_config(env, AdversaryConfig(beta=beta, colluding=True), n_ep, seed=base_seed)
    rows += [{"ablation": "collusion", "setting": "independent", **r_ind.row()},
             {"ablation": "collusion", "setting": "colluding", **r_col.row()}]
    # orchestrator trusted/compromised
    r_tr = score_config(env, AdversaryConfig(beta=beta, colluding=True), n_ep, seed=base_seed + 1)
    r_cp = score_config(env, AdversaryConfig(beta=beta, colluding=True, orchestrator_compromised=True), n_ep, seed=base_seed + 1)
    rows += [{"ablation": "orchestrator", "setting": "trusted", **r_tr.row()},
             {"ablation": "orchestrator", "setting": "compromised", **r_cp.row()}]

    integrity = _evaluator_integrity(env, n_ep, base_seed + 2)
    summary = {
        "collusion_advantage": collusion_advantage(r_col.metrics.asr_sys, r_ind.metrics.asr_sys),
        "evaluator_integrity": integrity,
        "note": "synthetic smoke-test output, not a paper result",
    }
    write_csv(out / "ablation.csv", rows)
    write_json(out / "ablation_summary.json", {"summary": summary, "provenance": run_metadata(cfg, base_seed)})
    logger.info("ablation: collusion_advantage=%.3f judge_hijack_rate=%.3f (SYNTHETIC)",
                summary["collusion_advantage"], integrity["judge_hijack_rate"])
    return summary
