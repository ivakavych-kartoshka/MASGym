# MASGym — A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems

Reference implementation of the paper *MASGym: A Co-Evolving Red/Blue Security Gym for
Multi-Agent LLM Systems with Parameterized Collusion, Orchestrator Compromise, and System-Level
Metrics* (`../main.pdf`). MASGym is a **benchmark environment + evaluation methodology** for the
security of multi-agent LLM systems — not a new attack or defense.

> ⚠️ **No paper-level experimental results are claimed by this repository unless real benchmark
> outputs are generated and their provenance is recorded.** The built-in generator is
> **synthetic**; every demo/experiment output it produces is labelled
> "synthetic smoke-test output, not a paper result".
>
> ⚠️ **This repository does not automatically download datasets or run paper-level experiments.**
> Real experiments are intended to be executed on EC2 after the required datasets, benchmarks,
> models, and credentials are manually provisioned (see `docs/ec2_experiment_guide.md`).

## What is implemented
This repo implements the **runnable core** of MASGym on a transparent synthetic agent model, plus
**numerical verification of the paper's closed-form theory**:

- Communication **topologies** (star, chain, tree, mesh) and the **parameterized adversary**
  `c_adv = (β, coll, adapt, orch, tool, syb, mem)` (Eq. 2).
- The **deterministic checker** that scores system-level predicates over the recorded trace and is
  provably invariant to injected messages (Thm 9.4), contrasted with a **hijackable LLM-judge**
  stand-in (Prop 9.5).
- **Compromise-propagation** models: independent-cascade and threshold (Assumption A4).
- The **system-level metric suite**: `ASR_sys, PNA_sys, NRP_sys, CPR, CSR/Δ_coll`, coordination
  quality, time-to-detection, recovery, cost, human-intervention rate (Eqs. 3–6, App. B), with
  Hoeffding/Wilson confidence intervals.
- **Aggregators** (product Eq. 1/5 + `min` + weighted geometric mean) and axiom checks (Thm 9.2).
- **Algorithm 1 (ScoreConfig)** and **Algorithm 2 (CoRB)** with pluggable red/blue policies.
- **Closed-form theory** (Props 9.7–9.11, Thm 9.13, Thm 9.17, Cor 9.18) verified against
  Monte-Carlo in the tests.

External systems (real LLM backbones, ToolEmu, ASB, AgentDojo, real guardrails) are **adapter
interfaces with TODOs**; they are never faked.

## Paper → code map (summary)
| Paper object | Code |
|---|---|
| Eq. 1/5 NRP | `methods/aggregators.py::product_nrp` |
| Eq. 2 adversary | `data/schemas.py::AdversaryConfig` |
| Eqs. 3–6 metrics | `metrics/metrics.py` |
| Alg. 1 ScoreConfig | `methods/scoring.py::score_config` |
| Alg. 2 CoRB | `methods/corb.py::run_corb` |
| Thm 9.4 / Prop 9.5 | `env/checker.py`, `env/judge.py` |
| Props 9.7–9.11 | `theory/propagation_bounds.py`, `env/propagation.py` |
| Thm 9.13 collusion | `theory/propagation_bounds.py::collusion_gap_star` |
| Thm 9.2 axioms | `theory/metric_axioms.py` |
| Thm 9.17 / Cor 9.18 | `theory/sample_complexity.py`, `metrics/confidence_intervals.py` |

Full mapping: `audits/paper_to_code_traceability.csv`.

## Installation
```bash
cd MASGym
python -m venv .venv && source .venv/bin/activate      # optional
pip install -e .            # or: pip install -r requirements.txt && export PYTHONPATH=src:.
```
Python ≥ 3.10 (3.11+ recommended). CPU-only; no GPU or network required.

## Quick start — synthetic demo
```bash
python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml --out outputs/synthetic_demo
# or:
python -m masgym.cli demo --out outputs/synthetic_demo
```
Produces (all **synthetic**, labelled): `sweep_metrics.csv`, `ablation.csv`, `theory_check.json`,
`corb_trajectory.csv`, and stamped `*.png` plots in `outputs/synthetic_demo/`.

## CLI
```bash
python -m masgym.cli --help
python -m masgym.cli version
python -m masgym.cli sweep    --config configs/synthetic_demo.yaml --out outputs/sweep
python -m masgym.cli ablation --config configs/synthetic_demo.yaml --out outputs/ablation
python -m masgym.cli theory   --out outputs/theory --trials 8000
python -m masgym.cli corb     --config configs/synthetic_demo.yaml --out outputs/corb
python -m masgym.cli plot     --input outputs/sweep/sweep_metrics.csv --output outputs/sweep --kind sweep
```
Stage mapping (MASGym is a benchmark, not a conformal method): the generic template's
`calibrate`/`evaluate` map to `sweep`/`ablation` here.

## Real-data usage (EC2)
Wire the adapters (`masgym.data.adapters`, `masgym.env.emulation.ToolEmuAdapter`,
`masgym.env.judge.LLMJudgeAdapter`, `masgym.baselines.external_wrappers`) to your provisioned
datasets/models, set `data.root` in a config, then run `scripts/run_experiment.py`. Full steps in
`docs/ec2_experiment_guide.md`. Nothing is downloaded automatically.

## Folder structure
```
MASGym/
  configs/            default / synthetic_demo / experiment_template YAMLs
  src/masgym/         data · env · methods · theory · metrics · baselines · utils · cli · demo
  experiments/        run_evaluation · run_ablation · run_theory_check · run_corb · plot_results
  scripts/            run_synthetic_demo · run_experiment · make_plots
  tests/              13 pytest modules (synthetic only)
  examples/           example config + a tiny synthetic episodes file
  docs/               implementation_notes · data_format · baseline_adapters · reproducibility · ec2_experiment_guide
  audits/             spec · traceability · math/result-integrity/gaps audits
  outputs/            generated artifacts (git-ignored)
```

## Implemented algorithms
ScoreConfig (Alg. 1), CoRB co-evolving red/blue loop (Alg. 2), independent-cascade & threshold
propagation, red policies (grid/random/adaptive), blue policies (static/escalating), deterministic
checker, hijackable-judge contrast.

## Metrics
`ASR_sys`, `PNA_sys`, `NRP_sys`, `CPR`, collusion success rate & advantage, coordination quality,
time-to-detection, recovery rate, token/latency cost, human-intervention rate; Hoeffding & Wilson CIs.

## Baselines
In-repo (synthetic effect-models): no-defense, fixed-threshold, lifted per-agent defenses
(delimiting, paraphrase, PI-detector, instructional-prevention, guardrail). Adapter stubs (external):
ASB, AgentDojo, Llama Guard / NeMo / TrustAgent, AutoDefense, G-Safeguard. See
`docs/baseline_adapters.md`.

## Configuration guide
Edit `configs/*.yaml`: `env.*` (topology, agents, horizon, `p_infect`, `forced_degree`,
propagation), `eval.*` (`n_episodes`, `seed`), `defense` (`null|fixed_threshold|lifted:<name>`),
`sweep.*` (lists → Cartesian product), `corb.*` (rounds, red, blue). See `configs/default.yaml`.

## Reproducibility
Deterministic under a fixed seed; provenance headers on every output; episode budget via
`hoeffding_min_samples`. See `docs/reproducibility.md`.

## Limitations & known gaps
- The synthetic agent model is a transparent stand-in for real LLM agents; its numbers are **not**
  measurements. The paper's degradation finding remains an unproduced `(hypothesis)`.
- Real LLM backbones, ToolEmu emulation, and ASB/AgentDojo runs require external provisioning
  (adapters + TODOs). See `audits/implementation_gaps.md` and `TODO_IMPLEMENTATION.md`.
- Sybils and defense efficacy are synthetic effect-models (documented).

## Tests
```bash
pytest -q          # 81 tests, synthetic only, no network
```
Optional (if installed): `ruff check .`, `mypy src`.

## Reproduce demo outputs
```bash
python -m masgym.cli demo --out outputs/synthetic_demo   # regenerates all synthetic demo files
```

## License
MIT (see `pyproject.toml`).
