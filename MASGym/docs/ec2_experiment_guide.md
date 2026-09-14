# EC2 Experiment Guide (real, paper-scale runs)

> This repository never downloads datasets or runs paper-level experiments automatically. The
> steps below are performed manually on an EC2 (or similar) machine after you provision data,
> models, and credentials.

## 0. Prerequisites to provision manually
- **LLM backbones**: API access (GPT-4o, Claude-3.5) and/or local weights (Llama-3, Qwen2.5,
  Mistral). Store keys in environment variables; never commit them.
- **ToolEmu emulator**: install the real ToolEmu emulator / an LLM backend for tool emulation.
- **Benchmark task pools**: AgentBench, GAIA, WebArena, SWE-bench (some require registration /
  license / GitHub access), and MMLU, GSM8K. Place under `<data.root>/<benchmark>/`
  (see `docs/data_format.md`).
- **External baselines** (optional): ASB (github.com/agiresearch/ASB), AgentDojo, Llama Guard,
  NeMo Guardrails, AutoDefense, G-Safeguard.

## 1. Install
```bash
pip install -e .            # or: pip install -r requirements.txt && export PYTHONPATH=src:.
pytest -q                   # sanity check on synthetic data
```

## 2. Wire real adapters (replace synthetic components)
- Backbones: implement `generate_fn` for `masgym.data.adapters.LLMBackboneAdapter`.
- Emulator: implement `emulate_fn` for `masgym.env.emulation.ToolEmuAdapter`.
- Real LLM judge (RQ2): implement `judge_fn` for `masgym.env.judge.LLMJudgeAdapter`.
- External baselines: implement `run(config)` in `masgym.baselines.external_wrappers.*`.
- Benchmark tasks: implement parsing in `masgym.data.adapters.BenchmarkTaskAdapter.load_tasks`.
Then replace the synthetic `Orchestrator` agent behaviour with real agent rollouts that populate
the same `Trace` schema (so the deterministic checker and metrics are unchanged).

## 3. Choose the episode budget
```python
from masgym.theory.sample_complexity import hoeffding_min_samples, sweep_budget
hoeffding_min_samples(eps=0.05, alpha=0.05)   # -> 738 episodes per config
sweep_budget(G=50, delta=0.1, alpha=0.05)     # -> per-config M across a 50-config sweep
```

## 4. Run the sweeps (per topology and agent count)
```bash
python scripts/run_experiment.py --config configs/experiment_template.yaml --stage sweep     --out outputs/sweep
python scripts/run_experiment.py --config configs/experiment_template.yaml --stage ablation  --out outputs/ablation
python scripts/run_experiment.py --config configs/experiment_template.yaml --stage corb      --out outputs/corb
python scripts/make_plots.py --input outputs/sweep/sweep_metrics.csv --output outputs/sweep --kind sweep
```
Set `data.root`, `env.topology` (run once per topology), and `env.n_agents` (sweep 3..50) per run.

## 5. Record provenance
Every output carries a provenance header. For real runs, set `synthetic=False` in the runner call
(or wire real adapters so the generator marks runs accordingly) and archive the exact configs,
seeds, model/version identifiers, and the CoRB trajectory logs alongside the results.

## Cost warning
Cost grows as `Theta(R * M * N * H)` agent invocations (Section 8.1 / Cor 9.18). Budget the
reachable region of the parameter space explicitly; the mesh topology is the costliest
(`|E| = Theta(N^2)`).
