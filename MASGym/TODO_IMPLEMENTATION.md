# TODO — Implementation (to run real paper-scale experiments)

Everything below is intentionally deferred to EC2. The local repo is complete, tested, and
EC2-ready; it does not download data or run real experiments. See `docs/ec2_experiment_guide.md`.

## A. Wire real models / emulators (adapter stubs today)
- [ ] `data/adapters.py::LLMBackboneAdapter` — implement `generate_fn` for Llama-3, Qwen2.5,
      Mistral, GPT-4o, Claude-3.5 (API keys / weights, never committed).
- [ ] `env/emulation.py::ToolEmuAdapter` — implement `emulate_fn` against the real ToolEmu
      emulator / an LLM backend (surface the κ≈0.48 fidelity caveat in reports).
- [ ] `env/judge.py::LLMJudgeAdapter` — implement `judge_fn` for the RQ2 deterministic-vs-judge
      ablation with a real LLM judge.
- [ ] Replace the synthetic `Orchestrator.run_episode` agent behaviour with real agent rollouts
      that populate the same `Trace` schema (checker + metrics stay unchanged).

## B. Provision benchmark datasets (manual; some require registration/license)
- [ ] AgentBench, GAIA, WebArena, SWE-bench — download and place under `<data.root>/<benchmark>/`.
- [ ] MMLU, GSM8K — public; for worker subtasks.
- [ ] Implement `data/adapters.py::BenchmarkTaskAdapter.load_tasks` parsing (schema in
      `docs/data_format.md`), including the per-task `success_spec`/`security_spec` that map to
      the deterministic `Psi`/`Phi` predicates.

## C. Implement external baselines (adapter stubs today)
- [ ] `baselines/external_wrappers.py::ASBSingleAgentAdapter.run` (github.com/agiresearch/ASB).
- [ ] `AgentDojoAdapter.run` (AgentDojo single-agent).
- [ ] `RealGuardrailAdapter.run` (Llama Guard / NeMo Guardrails / TrustAgent).
- [ ] `MADefenseAdapter.run` (AutoDefense / G-Safeguard).
      Return the documented output schema; never fake a dummy as the real baseline.

## D. Run experiments + produce real results (currently placeholders)
- [ ] Choose `M` per config via `theory.sample_complexity.hoeffding_min_samples` (Thm 9.17) and
      `sweep_budget` (Cor 9.18).
- [ ] Run sweeps per topology × agent count (3–50) and the ablations; set `synthetic=False` in the
      runner provenance once real adapters drive the episodes.
- [ ] Only then may Tables 2–6 / Figure 6 be populated with measured numbers, with provenance.

## E. Verification / confirmation
- [ ] Validate the propagation model (Assumption A4) empirically: does measured `CPR` resemble
      independent-cascade/threshold? Report the gap.
- [ ] Confirm the `success_spec`/`security_spec` predicates with task authors (predicate review).
- [ ] Author confirmation: none required for math (no inconsistencies detected), but confirm the
      exact Claude-3.5 variant and any dataset versions used.

## F. Optional engineering
- [ ] Add `ruff`/`mypy` to CI (configs present in `pyproject.toml`); run `ruff check .`, `mypy src`.
- [ ] Parallelize episode generation for large sweeps (per-config RNG spawning is already supported).

## Not needed
- Conformal-prediction components (out of scope for this paper).
- Any fabricated numbers, benchmarks, or baseline APIs (explicitly prohibited and not present).
