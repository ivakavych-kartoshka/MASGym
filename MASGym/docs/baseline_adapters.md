# Baselines and Adapters

MASGym compares defenses under a common, deterministically-scored metric. This repo distinguishes
three kinds of baseline; the code never presents one as another.

## 1. Real (in-repo) baselines — synthetic effect-models
Fully implemented and runnable locally, but with **chosen effect parameters** (labelled
`SYNTHETIC_EFFECT_MODEL`), not measured efficacies:
- `masgym.baselines.no_defense.NoDefense`
- `masgym.baselines.fixed_threshold.FixedThresholdDefense` (tie -> flag/defer, conservative)
- `masgym.baselines.lifted_defenses.lifted_defense(name)` for
  `{delimiting, paraphrase, pi_detector, instructional_prevention, guardrail}`

Each conforms to the `DefenseLike` interface:
```python
effective_p_infect(env, adv) -> float   # reduced per-edge probability
detect_prob(env, adv) -> float
recover_prob(env, adv) -> float
```

## 2. Dummy test baseline
`masgym.data.adapters.DummyBackbone` and `masgym.env.judge.HijackableDummyJudge` are deterministic
stand-ins used **only in tests/ablations**. They are never real agents/judges.

## 3. External baselines — adapter stubs (require EC2 provisioning)
`masgym.baselines.external_wrappers` defines the run interface for systems that are NOT bundled:
- `ASBSingleAgentAdapter` — ASB re-run single-agent (github.com/agiresearch/ASB)
- `AgentDojoAdapter` — AgentDojo single-agent deterministic checks
- `RealGuardrailAdapter(guardrail)` — Llama Guard / NeMo Guardrails / TrustAgent
- `MADefenseAdapter(defense)` — AutoDefense / G-Safeguard

Each `run(config) -> dict` raises `NotImplementedError` with a pointer to setup docs until
implemented on EC2. Expected output schema:
```json
{"asr_sys": float, "pna_sys": float, "nrp_sys": float, "cpr": float,
 "cost": {"tokens": float, "latency": float},
 "provenance": {"baseline": str, "version": str, "command": str}}
```

## LLM-judge ablation (RQ2)
`masgym.env.judge.LLMJudgeAdapter(judge_fn)` wraps a real LLM judge; provide `judge_fn` on EC2.
`HijackableDummyJudge` demonstrates the hijack (Prop 9.5) for tests. The deterministic checker
(`DeterministicChecker`) is always on the critical path.

## Wiring a real backbone
`masgym.data.adapters.LLMBackboneAdapter(model_name, generate_fn)` — supply `generate_fn` that
calls your model (Llama-3, Qwen2.5, Mistral, GPT-4o, Claude-3.5). Keys/models are never bundled.
