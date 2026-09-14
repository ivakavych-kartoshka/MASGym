# Idea Fidelity Report — MASGym

Source of truth: `idea.pdf` (= `idea.tex`), *"MASGym: A Co-Evolving Red/Blue Security Gym
for Multi-Agent LLM Systems"* (Secure Multi-Agent Systems — Research Idea Repository;
concept note, not a paper). This report extracts the canonical specification and locks it.
Every manuscript section must remain consistent with the **LOCKED PAPER SPECIFICATION**
below. If any draft section diverges, the draft is discarded and rewritten.

---

## 1. Extraction from `idea.pdf`

**(1) Exact / working title.**
"MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems."

**(2) Core research field.**
Security evaluation (benchmarks / measurement instruments) for **multi-agent LLM systems** —
i.e., orchestrated collectives of tool-using LLM agents. Cross-cuts AI safety, LLM-agent
security, and multi-agent systems. It is an *environment / methodology* contribution, **not**
an attack paper and **not** a defense paper.

**(3) Core technical keywords.**
Multi-agent LLM security; benchmark/environment ("gym"); co-evolving red/blue; forced
coordination; heterogeneous roles; partial observability; colluding agents; compromised
orchestrator; malicious tools; Sybil identities; poisoned shared memory; system-level metrics;
system-level Non-Refusal-Performance (NRP); LM-emulated tools (ToolEmu-style); deterministic
state-based security checks (AgentDojo-style); communication topologies (star, chain, tree,
mesh); compromise propagation; group-level emergence.

**(4) System-model entities.**
Heterogeneous roles: an **orchestrator** (planner), **workers**, **tool-executors**, and a
**shared-memory store**; 3–50 agents; partial observability (agents see only local context and
permitted messages); communication topologies star / chain / tree / mesh; per-agent trust
boundaries; optional human-approval hooks; emulated tools; a deterministic state checker; an
orchestration layer that instantiates topology, roles, observability, and adversary parameters.

**(5) Main mathematical objects.**
- ASB's metric  NRP = PNA · (1 − ASR)  (utility × (1 − attack success)).
- The proposed **system-level generalization**  NRP_sys = PNA_sys · (1 − ASR_sys),
  where ASR_sys is measured against **system-level security predicates** over the **global
  state trace**, and PNA_sys is benign coordinated-task performance.
- A **parameterized adversary** vector: adversary fraction over agents; collusion on/off;
  static/adaptive; orchestrator compromised on/off; malicious tools; Sybils; poisoned memory.
- The **co-evolving red/blue** trajectory of (attack, defense) pairs and their system-NRP.
- System-level measured quantities: system-ASR, collusion success rate, compromise-propagation
  rate, coordination quality, time-to-detection, recovery rate, cost, scalability.
- Emulation-fidelity caveat quantified by ToolEmu's reported human agreement κ ≈ 0.48.

**(6) Proposed algorithm name (if present).**
No formal algorithm name is given. The named *procedure* is the **co-evolving red/blue
protocol**: alternate a **red policy** (proposes attack configurations from the parameter
space) and a **blue policy** (proposes defenses), logging (attack, defense, system-NRP)
trajectories. The manuscript names this procedure **CoRB** (Co-evolving Red/Blue) for
reference; the name is a label, not a new mechanism, and preserves the idea's wording.

**(7) Theorem names / directions (if present).**
None stated (it is a concept note). The idea, however, *demands* two theoretical obligations
that the manuscript discharges honestly:
  (a) "the exact aggregation is a design contribution to be validated, not assumed" and
      "the system-NRP aggregation must be justified, not asserted" → an **axiomatic
      characterization** of the NRP_sys aggregator (construct validity).
  (b) "deterministic state-based checks … so a successful injection cannot hijack the judge"
      → an **evaluator-integrity** statement (the deterministic checker's verdict is
      independent of adversarial message content except through TCB-recorded state).
Additional in-scope, faithful theory the environment's own quantities motivate:
  (c) **compromise-propagation** bounds across the four topologies (supports the
      "compromise-propagation rate" metric and the topology sweep);
  (d) a **forced-coordination** lower bound (supports "no single agent can complete alone");
  (e) **estimator concentration / sample complexity** for system-ASR and NRP_sys (supports
      "how many episodes are needed" and the cost analysis).
All are stated under explicit assumptions; empirical claims stay `(hypothesis)`.

**(8) Experiment plan.**
Validate the instrument and demonstrate the headline finding. **Models:** open (Llama-3,
Qwen2.5, Mistral) + proprietary (GPT-4o, Claude-3.5). **Scale/topology:** 3–50 agents; star,
chain, tree, mesh. **Adversary sweeps:** adversary fraction; independent vs. colluding; static
vs. adaptive; orchestrator on/off; malicious tools; Sybils; poisoned memory. **Metrics:**
system-ASR, collusion success rate, compromise-propagation rate, coordination quality,
system-NRP, time-to-detection, recovery rate, token/API + latency cost, scalability.
**Baselines:** ASB re-run single-agent; AgentDojo; no-defense; per-agent defenses lifted into
the multi-agent setting. **Ablations:** collusion on/off; orchestrator trusted vs. compromised;
emulated vs. real tools; deterministic vs. LLM-judge evaluation (to quantify evaluator-hijack
risk).

**(9) Baseline methods.**
ASB (single-agent mode); AgentDojo (single-agent); no-defense; per-agent defenses lifted into
the multi-agent setting (e.g., delimiting/sandwich, paraphrase, PI detector, instructional
prevention, guardrails) — used as *lifted baselines* to test whether they survive.

**(10) Seed references (from `idea.pdf`).**
- **ToolEmu** — Ruan et al., *Identifying the Risks of LM Agents with an LM-Emulated Sandbox*,
  arXiv:2309.15817, ICLR 2024. (Emulation layer; κ ≈ 0.48 caveat.)
- **ASB (Agent Security Bench)** — H. Zhang et al., arXiv:2410.02644, ICLR 2025. (NRP metric;
  single-agent; shared memory as lone cross-agent vector.)
- **AgentDojo** — Debenedetti et al., arXiv:2406.13352, NeurIPS 2024 Datasets & Benchmarks.
  (Deterministic state-based `security()` checks; single-agent.)
- **MASEC** — Schroeder de Witt et al., *Open Challenges in Multi-Agent Security*,
  arXiv:2505.02077. (§4.7: no multi-agent security benchmark exists; enumerates requirements.)

**(11) Explicit risks / assumptions (stated in `idea.pdf`).**
- Emulation fidelity is the central threat to validity (κ ≈ 0.48); mitigate by routing scoring
  through the deterministic checker + reporting the emulated-vs-real-tools ablation.
- "Benchmark-without-a-finding" critique: ship the degradation finding, but it must replicate;
  if defenses do not degrade, reframe as a (valuable) negative result.
- API/compute cost grows with agent count and the co-evolving loop → constrains reachable
  parameter space.
- Construct-validity risk: the system-NRP aggregation must be justified, not asserted.
- TCB: the deterministic state checker and the environment harness are trusted; emulated tools
  have no real side effects. Out of scope: real-world tool side effects, physical actuation,
  model-weight attacks.

**(12) What the paper is NOT about.**
- NOT a new attack, and NOT a new defense, as its central contribution.
- NOT "ASB applied to many agents" (ASB has no collusion, no compromised orchestrator).
- NOT "AgentDojo at scale" (AgentDojo's deterministic checker is single-agent by design).
- NOT a model-swap or prompt-filter study; NOT mere engineering.
- NOT over-the-air / federated learning, NOT differential-privacy mechanism design, NOT
  auction/mechanism-design incentives, NOT a cryptographic-protocol paper, NOT a MARL
  reward-shaping paper. (These are forbidden drifts.)
- Does NOT equate lower system-ASR / higher system-NRP with "secure": the environment is an
  instrument, not a verdict.

---

## LOCKED PAPER SPECIFICATION

**Locked topic.** A purpose-built **benchmark/environment ("gym") and evaluation methodology
for the security of multi-agent LLM systems**, with native parameterization of collusion,
orchestrator/tool compromise, Sybils, and poisoned shared memory, and **system-level** risk
metrics — headlined by the `(hypothesis)` finding that single-agent defenses degrade under
collusion and compromised-orchestrator conditions.

**Locked problem statement.** Existing agent-security benchmarks (ASB, AgentDojo, InjecAgent,
ToolEmu) are single-agent; they cannot produce or measure the group-level phenomena (collusion,
compromised orchestrator, malicious tools, Sybils, compromise propagation, forced-coordination
emergence) of deployed orchestrated collectives. There is no instrument to test whether
single-agent defenses survive multi-agent deployment. MASGym is that instrument.

**Locked method family.** (i) A **ToolEmu-style LM-emulation layer** (adversarial-emulator
mode); (ii) an **AgentDojo-style deterministic state checker** evaluating system-level security
predicates over the global state trace — never an LLM judge on the critical path; (iii) an
**orchestration layer** instantiating topology, roles, observability, and the parameterized
adversary; (iv) **system-level metrics** including NRP_sys = PNA_sys·(1 − ASR_sys); (v) the
**co-evolving red/blue (CoRB) protocol**.

**Locked theoretical goals** (all under stated assumptions; honest proof-status labels).
(T-Metric) axiomatic characterization / uniqueness of the NRP_sys aggregator and its reduction
to ASB's NRP when N = 1; (T-Integrity) evaluator integrity of the deterministic checker vs.
LLM-judge hijack; (T-Prop) topology-dependent compromise-propagation bounds (star/chain/tree/
mesh) and a collusion-vs-independent separation in the environment's propagation model;
(T-Coord) a forced-coordination lower bound; (T-Sample) concentration / sample-complexity of
the system-ASR and NRP_sys estimators.

**Locked experiment family.** Instrument-validation + adversary sweeps over {agent count
3–50} × {star, chain, tree, mesh} × {adversary fraction} × {independent, colluding} × {static,
adaptive} × {orchestrator trusted, compromised} × {malicious tools} × {Sybils} × {poisoned
memory}, across open + proprietary agent models, with the ablations named above. All numerical
results are `(hypothesis)` / placeholder until produced.

**Locked baseline family.** ASB (single-agent), AgentDojo, no-defense, and per-agent defenses
lifted into the multi-agent setting; deterministic vs. LLM-judge evaluator ablation.

**Terms that MUST appear in title/abstract/introduction.** multi-agent (LLM) security;
benchmark / environment / "gym"; co-evolving red/blue; collusion; compromised orchestrator;
Sybil; malicious tools; poisoned shared memory; system-level metric / system-level NRP; forced
coordination; heterogeneous roles; partial observability; topologies; ToolEmu-style emulation;
AgentDojo-style deterministic checks; degradation of single-agent defenses `(hypothesis)`.

**Terms that MUST NOT dominate** (may appear only in narrow, cited support, never as the
paper's agenda): differential privacy; over-the-air / federated aggregation; mechanism
design / VCG / auctions / incentive compatibility; zero-knowledge / SMPC / TEE as a central
construction; MARL reward shaping; a single named novel attack or novel defense presented as
*the* contribution. The scientific object is the controlled variation of coordination,
collusion, and orchestrator variables and the system-level metrics that quantify their effect.
