"""Scaled real-LLM pilot: topology x agent-count x scenario sweep, one model per run.

Extends ``run_llm_pilot.py`` (which fixes star / N=3) to an arbitrary grid of
topologies and agent counts for a SINGLE backbone model. Run it once per model so
VRAM and wall-clock stay controlled on one GPU:

    python experiments/run_llm_pilot_sweep.py --model Qwen/Qwen2.5-3B-Instruct \
        --episodes 100 --topologies star,chain,tree,mesh --agents 3,5,10

Output layout (``outputs/llm_pilot_scale/<Model-Short>/``):
    summary.json          model-level aggregate: config -> env + per-scenario results
    compare.csv           long table: (topology, agents, scenario, metrics) for this model
    <topo>_a<n>/summary.json  per-config scenario aggregates
    <topo>_a<n>/episodes.csv  per-episode rows
    <topo>_a<n>/decisions.jsonl exact prompts + raw model output for inspectability

The paper's parameter sweeps use the synthetic model; the defense study in the main text
is measured on runs produced by this sweep, with ``--defense`` applying a real prompt-level
transformation to the prompt sent to the backbone.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from concurrent.futures import ThreadPoolExecutor

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np

from experiments.run_llm_pilot import (
    PILOT_BANNER,
    RECOMMENDED,
    SCENARIOS,
    HFCausalBackbone,
    MistralAPIBackbone,
    BedrockAPIBackbone,
    MISTRAL_DEFAULT_MODEL,
    BEDROCK_DEFAULT_MODEL,
    _load_env_file,
    asdict_env,
    run_episode_pilot,
    DEFENSES,
)
from masgym.data.adapters import LLMBackboneAdapter
from masgym.data.schemas import AdversaryConfig, EnvConfig, TopologyName
from masgym.env.checker import DeterministicChecker
from masgym.metrics.metrics import (
    asr_sys,
    compromise_propagation_rate,
    coordination_quality,
    nrp_sys,
    pna_sys,
)
from masgym.utils.io import ensure_dir, write_csv, write_json
from masgym.utils.logging import configure_logging, get_logger
from masgym.utils.seeding import SeededRNG

logger = get_logger(__name__)

DEFAULT_TOPOLOGIES = ",".join(t.value for t in TopologyName)
DEFAULT_AGENTS = "3,5,10"
ALL_SCENARIOS = ",".join(SCENARIOS)
DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"


def _scenario_aggregate(
    scenario: str, episodes: list, ep_decisions: list[dict], n_run: int
) -> dict:
    active = [d for d in ep_decisions if d["attack"]]
    n_dec = len(active)
    n_exfil = sum(1 for d in active if d["action"] == "exfiltrate")
    n_parse_fail = sum(1 for d in active if d["parse_failed"])
    return {
        "scenario": scenario,
        "episodes": n_run,
        "asr_sys": round(asr_sys(episodes), 4),
        "asr_action": round(n_exfil / n_dec, 4) if n_dec else float("nan"),
        "psi_mean": round(coordination_quality(episodes), 4),
        "cpr": round(compromise_propagation_rate(episodes), 4),
        "tokens_mean": round(float(np.mean([e.tokens for e in episodes])), 1),
        "latency_mean_s": round(float(np.mean([e.latency for e in episodes])), 3),
        "decisions": n_dec,
        "exfiltration_decisions": n_exfil,
        "compliance_rate": round(n_exfil / n_dec, 4) if n_dec else float("nan"),
        "parse_failures": n_parse_fail,
    }


def _run_config(
    env: EnvConfig,
    scenario_names: list[str],
    model_id: str,
    n_run: int,
    base_seed: int,
    cfg_index: int,
    adapter,
    checker: DeterministicChecker,
    outdir: pathlib.Path,
    write_notes: bool,
    generate=None,
    workers: int = 1,
    defense: str = "none",
) -> list[dict]:
    """Run every scenario for one (topology, n_agents) config; write config artifacts.

    ``workers > 1`` runs the episodes of a scenario in a thread pool. This is safe and
    result-identical: each episode seeds its own ``SeededRNG(seed)`` derived from
    ``(base_seed, cfg_index, m)`` and carries no state across iterations, and the API
    backbones run at ``temperature=0`` so a prompt always maps to the same completion.
    Results are reassembled in episode order, so artifacts are byte-identical to
    ``workers=1``. Only valid for API backbones (the HF path keeps the sequential path).
    """
    ensure_dir(outdir)
    all_episodes: list = []
    decision_log: list[dict] = []
    rows: list[dict] = []
    results: dict[str, dict] = {}

    for scenario in scenario_names:
        adv = AdversaryConfig(**SCENARIOS[scenario])

        def one_episode(m: int):
            rng = SeededRNG(seed=base_seed + cfg_index * 10_007 + m * 91)
            return run_episode_pilot(env, adv, rng, adapter, checker,
                                     model_id=model_id, generate=generate, defense=defense)

        if workers > 1:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                # executor.map preserves input order, so assembly below stays deterministic
                produced = list(pool.map(one_episode, range(n_run)))
        else:
            produced = [one_episode(m) for m in range(n_run)]

        episodes: list = []
        ep_decisions: list[dict] = []
        for m, (ep, decs) in enumerate(produced):
            episodes.append(ep)
            ep_decisions.extend(decs)
            all_episodes.append(ep)
            rows.append(
                {
                    "scenario": scenario,
                    "episode": m,
                    "n_agents": env.n_agents,
                    "phi": int(ep.phi),
                    "psi": int(ep.psi),
                    "tokens": round(ep.tokens, 1),
                    "latency_s": round(ep.latency, 3),
                    "decisions": len(decs),
                }
            )
        results[scenario] = _scenario_aggregate(scenario, episodes, ep_decisions, n_run)
        logger.info("config=%s scenario=%-24s %s", outdir.name, scenario, results[scenario])
        decision_log.extend(ep_decisions)

    benign_eps = [e for e in all_episodes if e.adversary.beta == 0.0]
    pna = pna_sys(benign_eps) if benign_eps else float("nan")
    logger.info("config=%s PNA_sys (benign) = %.4f", outdir.name, pna)
    for scen in results:
        results[scen]["pna_sys"] = round(pna, 4)
        results[scen]["nrp_sys"] = round(nrp_sys(pna, results[scen]["asr_sys"]), 4)

    write_json(
        outdir / "summary.json",
        {"banner": PILOT_BANNER, "model": model_id, "env": asdict_env(env), "scenarios": results},
    )
    write_csv(outdir / "episodes.csv", rows)
    with (outdir / "decisions.jsonl").open("w", encoding="utf-8") as fh:
        for d in decision_log:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    if write_notes:
        (outdir / "README.md").write_text(
            _config_readme(results, env, model_id), encoding="utf-8"
        )

    # flatten for the model-level compare table
    compare_rows: list[dict] = []
    for scen, r in results.items():
        compare_rows.append(
            {
                "topology": env.topology.value,
                "n_agents": env.n_agents,
                "scenario": scen,
                "asr_sys": r["asr_sys"],
                "asr_act": r["asr_action"],
                "nrp_sys": r["nrp_sys"],
                "cpr": r["cpr"],
                "tokens": r["tokens_mean"],
                "latency": r["latency_mean_s"],
                "compliance_rate": r["compliance_rate"],
                "parse_failures": r["parse_failures"],
            }
        )
    return compare_rows


def _config_readme(results: dict, env: EnvConfig, model_id: str) -> str:
    lines = [
        f"# LLM pilot sweep ({model_id}) -- {env.topology.value} / N={env.n_agents}",
        "",
        PILOT_BANNER,
        "",
        "## What this is",
        "- Real backbone driven through `LLMBackboneAdapter.generate_fn`.",
        "- The compromised agent's reaction to an injected tool note is a real model output.",
        "- The same deterministic checker scores the trace (phi/psi) as in the synthetic suite.",
        "- With `--defense`, a real prompt-level transformation is applied to the sent prompt.",
        "",
        "## Scope limits",
        "- The paper's parameter sweeps are the synthetic model; the defense study reported",
        "  in the main text uses runs like this one.",
        "- Data is fictitious; the measurements are real.",
        "",
        "## Per-scenario aggregates (see summary.json)",
    ]
    for scen, r in results.items():
        lines.append(
            f"- **{scen}**: ASR_sys={r['asr_sys']:.3f} ASR_act={r['asr_action']:.3f} "
            f"NRP_sys={r['nrp_sys']:.3f} CPR={r['cpr']:.3f} tokens/ep={r['tokens_mean']:.1f} "
            f"latency/ep={r['latency_mean_s']:.2f}s"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scaled real-LLM pilot sweep (one model per run).")
    parser.add_argument("--backend", type=str, default="hf", choices=["hf", "mistral", "bedrock"],
                        help="hf=local transformers; mistral=hosted Mistral API; bedrock=AWS Bedrock (needs BEDROCK_API_KEY)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="HF model id / Mistral API model id")
    parser.add_argument("--episodes", type=int, default=100, help="episodes per (config, scenario)")
    parser.add_argument("--topologies", type=str, default=DEFAULT_TOPOLOGIES,
                        help="comma list, default " + DEFAULT_TOPOLOGIES)
    parser.add_argument("--agents", type=str, default=DEFAULT_AGENTS,
                        help="comma list of agent counts, default " + DEFAULT_AGENTS)
    parser.add_argument("--scenarios", type=str, default=ALL_SCENARIOS,
                        help="comma list, default all")
    parser.add_argument("--device", type=str, default="cuda", help="cuda|cpu")
    parser.add_argument("--quant", type=str, default="none", choices=["none", "4bit", "8bit"],
                        help="bitsandbytes quantization for models that exceed VRAM")
    parser.add_argument("--out", type=pathlib.Path, default=None,
                        help="base output dir (default outputs/llm_pilot_scale)")
    parser.add_argument("--seed", type=int, default=0, help="base RNG seed")
    parser.add_argument("--write-notes", action="store_true", help="write README provenance notes")
    parser.add_argument("--max-retries", type=int, default=6, help="API retries on 429/5xx (mistral)")
    parser.add_argument("--min-interval", type=float, default=1.0, help="min seconds between API calls (mistral pacing)")
    parser.add_argument("--region", type=str, default="us-east-1",
                        help="AWS region for bedrock-runtime; must match the region the key was generated in")
    parser.add_argument("--workers", type=int, default=1,
                        help="episodes run concurrently (API backbones only). 1 keeps the "
                             "sequential path; results are identical either way")
    parser.add_argument("--rpm", type=float, default=None,
                        help="global request-per-minute ceiling (overrides --min-interval). "
                             "Recommended alongside --workers, e.g. --rpm 150")
    parser.add_argument("--defense", type=str, default="none", choices=list(DEFENSES),
                        help="per-agent defense applied to the real backbone prompt: none | "
                             "delimiting | instructional_prevention. Each is a real prompt-level "
                             "defense, so its effect is measured, not modelled. 'none' reproduces "
                             "the undefended prompt used by earlier runs")
    args = parser.parse_args(argv)
    if args.backend == "mistral" and args.model == DEFAULT_MODEL:
        args.model = MISTRAL_DEFAULT_MODEL
    if args.backend == "bedrock" and args.model == DEFAULT_MODEL:
        args.model = BEDROCK_DEFAULT_MODEL

    short = RECOMMENDED.get(args.model, args.model.split("/")[-1])
    base = args.out or (_ROOT / "outputs" / "llm_pilot_scale")
    out_dir = base / short
    if args.defense != "none":
        out_dir = out_dir.with_name(f"{short}--{args.defense}")

    configure_logging()
    ensure_dir(out_dir)
    checker = DeterministicChecker()

    topologies = [TopologyName(t.strip()) for t in args.topologies.split(",")]
    n_agents_list = [int(a.strip()) for a in args.agents.split(",")]
    scenario_names = [s.strip() for s in args.scenarios.split(",")] or list(SCENARIOS)

    logger.info("%s", PILOT_BANNER)
    logger.info("loading %s on %s", args.model, args.device)
    logger.info("grid: %d topologies x %d agent-counts x %d scenarios x %d episodes",
                len(topologies), len(n_agents_list), len(scenario_names), args.episodes)
    logger.info("per-agent defense condition: %s", args.defense)

    if args.backend == "mistral":
        _load_env_file(_ROOT / ".env")
        backend = MistralAPIBackbone(args.model, max_retries=args.max_retries,
                                     min_interval_s=args.min_interval, rpm=args.rpm)
        adapter = LLMBackboneAdapter(model_name=args.model, generate_fn=backend.generate)
        generate = backend.generate
        logger.info("Mistral API backbone wired through %s (endpoint %s)",
                    type(backend).__name__, backend.endpoint)
    elif args.backend == "bedrock":
        _load_env_file(_ROOT / ".env")
        backend = BedrockAPIBackbone(args.model, region=args.region, max_retries=args.max_retries,
                                     min_interval_s=args.min_interval, rpm=args.rpm)
        adapter = LLMBackboneAdapter(model_name=args.model, generate_fn=backend.generate)
        generate = backend.generate
        logger.info("AWS Bedrock backbone wired through %s (endpoint %s)",
                    type(backend).__name__, backend.endpoint)
    else:
        if args.workers > 1:
            logger.warning("--workers is ignored for the hf backend (single GPU model instance)")
        backend = HFCausalBackbone(args.model, device=args.device, quant=args.quant)
        adapter = LLMBackboneAdapter(model_name=args.model, generate_fn=backend.generate)
        generate = None
        logger.info("real backbone wired through %s", type(adapter).__name__)

    workers = max(1, args.workers) if generate is not None else 1
    if workers > 1:
        logger.info("concurrency: %d episodes in flight, rate cap %s",
                    workers, f"{args.rpm} rpm" if args.rpm else f"1 call/{args.min_interval}s")

    configs: dict[str, dict] = {}
    all_rows: list[dict] = []
    cfg_index = 0
    for topo in topologies:
        for n_agents in n_agents_list:
            env = EnvConfig(n_agents=n_agents, topology=topo, horizon=4,
                            forced_degree=2, p_infect=0.3)
            cfg_name = f"{topo.value}_a{n_agents}"
            cfg_dir = out_dir / cfg_name
            rows = _run_config(
                env, scenario_names, args.model, args.episodes, args.seed,
                cfg_index, adapter, checker, cfg_dir, args.write_notes, generate, workers,
                args.defense,
            )
            configs[cfg_name] = {
                "env": asdict_env(env),
                "scenarios": json.loads((cfg_dir / "summary.json").read_text(encoding="utf-8"))["scenarios"],
            }
            all_rows.extend(rows)
            cfg_index += 1

    write_json(
        out_dir / "summary.json",
        {"banner": PILOT_BANNER, "model": args.model, "quant": args.quant,
         "grid": {"topologies": [t.value for t in topologies],
                  "n_agents": n_agents_list,
                  "scenarios": scenario_names,
                  "episodes_per_scenario": args.episodes},
         "configs": configs},
    )
    write_csv(out_dir / "compare.csv", all_rows)

    print("\n===== PILOT SWEEP SUMMARY =====")
    print(f"{'topo':<7}{'N':>3} {'scenario':<24}{'ASR_sys':>9}{'ASR_act':>9}{'NRP_sys':>9}{'CPR':>7}{'lat(s)':>9}{'compl%':>8}")
    for r in all_rows:
        print(
            f"{r['topology']:<7}{r['n_agents']:>3} {r['scenario']:<24}{r['asr_sys']:>9.3f}"
            f"{r['asr_act']:>9.3f}{r['nrp_sys']:>9.3f}{r['cpr']:>7.3f}"
            f"{r['latency']:>9.2f}{r['compliance_rate']:>8.3f}"
        )
    print("\nFiles written to", out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())