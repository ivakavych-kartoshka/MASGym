# Topic Alignment Check — MASGym

Compares `idea.pdf` against the drafted manuscript on the six required axes plus the
`topic_signature.json` required objects. **Overall verdict: ALIGNED.** No section introduces a
central domain, benchmark family, or agenda name absent from `idea.pdf`/`PROJECT_PATH`.

## 1. Idea PDF topic vs final title
- **Idea PDF:** "MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems."
- **Manuscript title:** "MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems
  with Parameterized Collusion, Orchestrator Compromise, and System-Level Metrics."
- **PASS.** Title preserves the working name and every core term; the subtitle expands with objects
  taken directly from the idea (collusion, orchestrator compromise, system-level metrics).

## 2. Idea PDF keywords vs manuscript keywords
- **Idea:** multi-agent LLM security; benchmark/environment/gym; co-evolving red/blue; forced
  coordination; collusion; compromised orchestrator; malicious tools; Sybils; poisoned memory;
  system-level NRP; ToolEmu emulation; AgentDojo deterministic checks; topologies.
- **Manuscript keywords:** multi-agent LLM security; security benchmark and environment; co-evolving
  red/blue evaluation; collusion; compromised orchestrator; Sybil attack; prompt injection; tool
  emulation; deterministic security checking; system-level metrics; compromise propagation.
- **PASS.** Every idea keyword appears; no foreign keyword introduced.

## 3. Idea PDF theorem directions vs manuscript theorem directions
- **Idea (implied obligations):** the system-NRP aggregation "must be justified, not asserted"
  (construct validity); deterministic checks so "a successful injection cannot hijack the judge."
- **Manuscript:** Thm 9.2 (axiomatic characterization of $\NRPs$, reduces to ASB) directly discharges
  the aggregation-justification obligation; Thm 9.4 + Prop 9.5 (evaluator integrity vs judge hijack)
  discharge the checker-integrity obligation. Additional in-scope theory the idea's own metrics
  motivate: Props 9.7–9.10 + Cor 9.11 (compromise propagation across the four topologies), Thm 9.13
  (collusion advantage), Prop 9.15 (forced coordination), Thm 9.17 + Cor 9.18 (estimator concentration
  → cost).
- **PASS.** No theorem imports a foreign theory (no DP/FL/mechanism-design theorem). All are labelled
  with honest proof status; empirical degradation stays a `(hypothesis)`.

## 4. Idea PDF algorithm vs manuscript algorithm
- **Idea:** a co-evolving loop alternating a red policy (attack configs) and a blue policy (defenses),
  logging (attack, defense, system-NRP) trajectories; deterministic checker never on the critical path.
- **Manuscript:** Algorithm 2 (`\corb`) is exactly this loop; Algorithm 1 (`ScoreConfig`) is the
  deterministic rollout+scoring it calls. The name **CoRB** is introduced as a label for the idea's
  unnamed procedure (idea gives no algorithm name), preserving the algorithmic idea.
- **PASS.**

## 5. Idea PDF experiment plan vs manuscript experiment plan
- **Idea:** models {Llama-3, Qwen2.5, Mistral, GPT-4o, Claude-3.5}; 3–50 agents; star/chain/tree/mesh;
  sweeps over adversary fraction, independent/colluding, static/adaptive, orchestrator on/off, malicious
  tools, Sybils, poisoned memory; metrics {system-ASR, collusion success, compromise propagation,
  coordination quality, system-NRP, time-to-detection, recovery, token/API+latency, scalability};
  baselines {ASB single-agent, AgentDojo, no-defense, lifted per-agent defenses}; ablations
  {collusion on/off, orchestrator trusted/compromised, emulated/real tools, deterministic/LLM-judge}.
- **Manuscript §10 + App. B:** reproduces all of the above verbatim (RQ1–RQ6, models, sweeps, metric
  suite, baselines, and the four named ablations). All tables/plots are labelled placeholders.
- **PASS.** No dataset, attack, metric, or baseline from a different topic was substituted.

## 6. Idea PDF seed references vs manuscript related work
- **Idea seeds:** ToolEmu (2309.15817), ASB (2410.02644), AgentDojo (2406.13352), MASEC (2505.02077).
- **Manuscript:** all four are the `[1] Core seed references` in `references_verified.bib`, cited in the
  Introduction, Preliminaries, Related Work, and Theory; MASEC §4.7 grounds the novelty claim; ASB's NRP
  is generalized; AgentDojo's deterministic check and ToolEmu's emulation are preserved and cited.
- **PASS.**

## `topic_signature.json` required-object coverage per major section
| Section | Required objects present? |
|---|---|
| Abstract | multi-agent security, gym/benchmark, co-evolving red/blue, collusion, orchestrator compromise, Sybil, poisoned memory, $\NRPs$, ToolEmu, AgentDojo — **yes** |
| Introduction | same core terms + MASEC gap + contribution list + `(hypothesis)` — **yes** |
| System model | orchestrator/workers/tool-executors/memory, star/chain/tree/mesh, partial observability, TCB — **yes** |
| Threat model | 7-knob $\config_{\mathrm{adv}}$, independent/colluding, static/adaptive — **yes** |
| Problem/Theory | $\ASRs,\PNAs,\NRPs$, propagation, forced coordination, evaluator integrity — **yes** |
| Algorithm | CoRB red/blue loop + deterministic scoring — **yes** |
| Experiments | models, topologies, sweeps, metrics, baselines, ablations — **yes** |
| Figures | architecture, threat, pipeline, theory, expsetup, conceptual results — **yes** |

## Forbidden-drift scan
No section is dominated by, or centrally about, over-the-air/FL, differential privacy, mechanism
design/VCG, ZK/SMPC/TEE, or MARL reward shaping. Gym/PettingZoo/Melting Pot appear only as the
*environment* lineage in Related Work. **PASS.**

## Result
All six axes and all section-level object checks **PASS**. No topic mismatch requiring revision.
