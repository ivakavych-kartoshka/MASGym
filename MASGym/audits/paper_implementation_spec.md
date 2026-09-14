# Paper Implementation Specification — MASGym

**Source paper:** `../main.pdf` (this repository's parent folder).
**Title:** *MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems with
Parameterized Collusion, Orchestrator Compromise, and System-Level Metrics.*

> Note on the task template. The generic task template referenced conformal-prediction files
> (`calibration.py`, `mondrian.py`, weighted conformal, trajectory certification). **This paper is
> not about conformal prediction.** Per the paper-fidelity rule, the structure below is adapted to
> MASGym's actual objects (environment, deterministic checker, compromise propagation, system-level
> metrics, co-evolving red/blue protocol). The conformal branch is `intentionally_out_of_scope`.

## 1. Central task
MASGym is a **benchmark environment + evaluation methodology** for the *security of multi-agent
LLM systems*. It is explicitly **not** a new attack or defense. Its scientific object is the
controlled variation of coordination, collusion, and orchestrator variables and the **system-level
metrics** that quantify their effect. The environment is an *instrument, not a verdict*: a low
system-level attack-success rate is never equated with "secure."

## 2. Method / system name
**MASGym** with three layers: (i) an **emulation layer** (ToolEmu-style LM tool emulation, plus an
adversarial-emulator mode); (ii) a **deterministic checking layer** that scores system-level
security predicates over the global state trace (never an LLM judge on the critical path); (iii) an
**orchestration layer** that instantiates topology, roles, partial observability, and the
parameterized adversary. The evaluation procedure is **CoRB** (Co-evolving Red/Blue).

## 3. Algorithms (must implement)
- **Algorithm 1 — `ScoreConfig`**: deterministic system-level scoring of one configuration. Runs
  `M` episodes; each episode runs `N` agents for `H` steps under a topology and an adversary config,
  records a global trace, updates the compromise set under propagation rule `P`, and the deterministic
  checker computes `(Ψ, Φ)`. Returns estimates `ASR_sys, PNA_sys, NRP_sys, CPR` + detection/recovery.
- **Algorithm 2 — `CoRB`**: co-evolving red/blue loop. For `R` rounds: red proposes an attack config
  `c_adv` (static or adaptive best-response); score `(c_adv, blue^{r-1})`; blue proposes/upgrades a
  defense; re-score `(c_adv, blue^r)`; append to trajectory `L`; return `L` + Pareto frontier.

## 4. Equations (must implement as explicit functions)
- **Eq (1):** `NRP = PNA · (1 − ASR)` (ASB baseline metric).
- **Eq (2):** `c_adv = (β, coll, adapt, orch, tool, syb, mem)` (adversary configuration vector).
- **Eq (3):** `ASR_sys(c) = P_{τ∼D(c)}[Φ(τ) = 1]`.
- **Eq (4):** `PNA_sys(c) = P_{τ∼D(c°)}[Ψ(τ) = 1]` (benign counterpart `c°`).
- **Eq (5):** `NRP_sys(c) = PNA_sys(c) · (1 − ASR_sys(c))`.
- **Eq (6):** `CPR(c) = E[(|B_∞| − |B_0|) / (N − |B_0|)]` (compromise-propagation rate).

## 5. Theory objects to implement + numerically verify (closed forms)
- **Thm 9.2 metric axioms:** product aggregator `g(u,σ)=u·σ` is unique under D2/D4a/D4b; alternatives
  `min(u,σ)`, weighted geometric mean `u^w σ^{1−w}`. **Prop 9.1:** reduces to Eq (1) at `N=1`.
- **Thm 9.4 evaluator integrity / Prop 9.5 judge hijackable:** deterministic checker verdict is a
  function of the recorded trace only; an LLM judge can be flipped by message content with the trace
  unchanged.
- **Props 9.7–9.10 propagation (independent-cascade with `p`):**
  chain reach `Σ_{j=1}^{n−1} p^j ≤ p/(1−p)`; star centre-seed reach `p(n−1)` (`CPR=p`), leaf-seed
  `p + p²(n−2)`; tree reach `Σ_{ℓ=1}^{d}(bp)^ℓ` (transition at `bp=1`); mesh (`K_n`) one round
  `s + (n−s)(1 − (1−p)^s)`.
- **Cor 9.11 threshold confinement:** in-degree `< θ` ⇒ never compromised; chain with `θ≥2` ⇒ `CPR=0`.
- **Thm 9.13 collusion advantage (star, one seed):** `Δ_coll = p(1−p)(N−1)(N−2)/N = Θ(p(1−p)N) > 0`.
- **Prop 9.15 forced coordination:** `k`-forced ⇒ no set `<k` completes; adversary transversal of
  witnesses ⇒ can force `Ψ=0`.
- **Thm 9.17 concentration / sample complexity:** Hoeffding `P[|ASR_hat−ASR|≥ε] ≤ 2e^{−2Mε²}` ⇒
  `M ≥ ln(2/α)/(2ε²)`; NRP bound `|NRP_hat−NRP| ≤ |PNA_hat−PNA| + |ASR_hat−ASR|` (`4e^{−2Mε²}`).
- **Cor 9.18 sweep budget:** `M = O(Δ^{−2} ln(G/α))`; total `Θ(G·N·H·Δ^{−2} ln(G/α))`.
- **§8.1 complexity table:** per-episode `Θ(NH)` invocations, `Θ((N+|E|)H)` trace; per-sweep totals.

## 6. Data structures
`Agent` (id, role, backbone, permitted tools, memory perms, compromised flag); `Role` ∈ {orchestrator,
worker, tool_executor, memory}; `Topology` (name ∈ {star, chain, tree, mesh}, directed graph, edges,
inbound neighbourhoods); `AdversaryConfig` (Eq 2 fields); `EnvConfig` (N, topology, roles, observability,
horizon H, propagation params p/θ, k-forced degree); `TraceStep` (t, per-agent action/message record,
recorded state transitions); `Trace` (list of steps, compromise sets over time, terminal state);
`Episode` (config, trace, `(Ψ, Φ)` verdicts); `SecurityPredicate`/`BenignPredicate` (callables over trace).

## 7. Inputs and outputs
**Input:** an `EnvConfig` + `AdversaryConfig` + choice of backbone/emulator/checker/defense.
**Output:** per-config metric estimates and a CoRB trajectory (rows = `(c_adv, blue, NRP_sys, ASR_sys,
cost)`) with a Pareto frontier. All persisted as JSON/CSV under `outputs/`.

## 8. Metrics (§7.6, App. B)
`ASR_sys`, `PNA_sys`, `NRP_sys`, collusion success rate `CSR` + advantage `Δ_coll`, compromise-
propagation rate `CPR`, coordination quality, time-to-detection, recovery rate, token/API + latency
cost, scalability, human-intervention rate; Hoeffding confidence intervals.

## 9. Baselines (§10)
Implementable directly (synthetic effect-models, clearly labelled): **no-defense**, **fixed-threshold**,
and **lifted per-agent defenses** (delimiting/sandwich, paraphrase, PI-detector, instructional
prevention, guardrail). Require external systems (adapters + TODO): **ASB single-agent**, **AgentDojo**,
real **Llama Guard / NeMo / TrustAgent**, and reference MA defenses **AutoDefense / G-Safeguard**.
Deterministic-checker vs **LLM-judge** is an ablation (judge is an external LLM → adapter + a dummy
hijackable judge for tests).

## 10. Datasets / simulation settings (§10)
Backbones: Llama-3, Qwen2.5, Mistral, GPT-4o, Claude-3.5 (external → adapter). Benign task pools:
AgentBench, GAIA, WebArena, SWE-bench, MMLU, GSM8K (external → adapter). Scale/topology: 3–50 agents ×
{star, chain, tree, mesh}. Adversary sweeps over `c_adv`. **For local smoke tests, a fully synthetic
episode generator** realizes the paper's propagation model (Assumption 4) and predicates — **no LLM**.

## 11. Experimental protocol (§10)
RQ1 construct validity; RQ2 evaluator integrity (deterministic vs judge); RQ3 defense degradation
(headline **hypothesis**); RQ4 topology/propagation; RQ5 collusion/Sybils; RQ6 scalability/cost.
`M` episodes per config chosen by Thm 9.17; Benjamini–Hochberg across the sweep grid; ablations:
collusion on/off, orchestrator trusted/compromised, emulated/real tools, deterministic/judge.

## 12. Assumptions
A1 trusted harness/checker (TCB); A2 i.i.d. episodes; A3 bounded {0,1} indicators; A4 monotone
propagation (independent-cascade `p` / threshold `θ`); A5 continuous aggregator.

## 13. Limitations (paper)
Emulation fidelity `κ≈0.48`; headline finding is a **hypothesis**; metric construct validity relative
to axioms; propagation model is a model; TCB + predicate specification are assumptions; cost grows as
`Θ(RMNH)`; scope excludes real-world tool side effects, physical actuation, model-weight attacks.

## 14. Conceptual-only components (in the paper, placeholders here)
All numerical results (Tables 2–6, Figure 6) are **placeholders / `(hypothesis)`**. The headline
degradation claim is unproduced. Real backbones, real ToolEmu emulation, and real ASB/AgentDojo runs
are not executed in this repository.

## 15. Components requiring real external data / systems
Real LLM backbones & API keys; ToolEmu emulator; ASB and AgentDojo harnesses; benign benchmark task
pools; real per-agent guardrails. All are provided as **adapter interfaces with TODOs** (see
`docs/baseline_adapters.md`, `docs/data_format.md`, `TODO_IMPLEMENTATION.md`).

## 16. What this repository DOES implement and run locally (synthetic, honest)
The orchestration layer, topologies, adversary parameterization, the **deterministic checker**, the
**propagation models** (independent-cascade + threshold), the **synthetic episode generator**, **all
system-level metrics** + Hoeffding CIs, the **aggregators** (product/min/weighted-geometric), the
**CoRB** loop with simple red/blue policies, and **numerical verification of every closed-form theory
result** against Monte-Carlo — all on synthetic data, with outputs labelled
"synthetic smoke-test output, not a paper result."
