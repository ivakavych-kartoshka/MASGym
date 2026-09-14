# Implementation Notes

How the MASGym paper (`../main.pdf`) is translated into code. See
`audits/paper_to_code_traceability.csv` for the per-object mapping and
`audits/math_to_code_audit.md` for the mathematical audit.

## Topic fidelity
MASGym is a **benchmark environment + evaluation methodology** for multi-agent LLM security,
**not** a new attack, defense, or a conformal-prediction method. The task template mentioned
conformal-prediction files; those are intentionally out of scope (recorded as
`intentionally_out_of_scope` in the traceability CSV). The code implements MASGym's actual
objects: topologies, the parameterized adversary, the deterministic checker, compromise
propagation, system-level metrics, and the CoRB co-evolving protocol.

## Layered design (mirrors paper Section 7)
- **`masgym.data`** — schemas (Section 3-6), topology builders (Section 4.2), the synthetic
  episode generator (the Section 10 smoke-test substitute for real LLM backbones), and external
  adapters.
- **`masgym.env`** — the three layers: `emulation` (ToolEmu-style; synthetic + adapter),
  `checker` (deterministic, Thm 9.4), `judge` (hijackable contrast, Prop 9.5), `propagation`
  (independent-cascade + threshold, Assumption A4), and `orchestration` (runs an episode).
- **`masgym.methods`** — `aggregators` (Eq. 1/5, Thm 9.2), `scoring` (Algorithm 1 ScoreConfig),
  `red_policies`/`blue_policies`, and `corb` (Algorithm 2).
- **`masgym.theory`** — closed forms for Props 9.7-9.11, Thm 9.13, Thm 9.17, Cor 9.18, and the
  metric-axiom checks. These are verified numerically against Monte-Carlo in the tests.
- **`masgym.metrics`** — the full metric suite (Eqs. 3-6, Appendix B) with Hoeffding/Wilson CIs.
- **`masgym.baselines`** — synthetic-effect-model defenses (no-defense, fixed-threshold, lifted)
  and adapter stubs for external systems (ASB, AgentDojo, real guardrails, MA defenses).

## The synthetic agent model (why it is honest)
Running real MASGym needs LLM backbones + the ToolEmu emulator, which are external. For local
smoke tests we implement a **transparent synthetic model** that realizes the paper's own
compromise dynamics (Assumption A4: independent-cascade / threshold) and the k-forced-coordination
/ transversal success condition (Prop 9.15). This model is *faithful to the paper's definitions*
and its expected behaviour matches the proven closed forms (the tests check this). It is **not** a
measurement of any real agent or defense. Every batch of synthetic episodes and every output file
carries the banner "synthetic smoke-test output, not a paper result", and defense effect-parameters
are labelled `SYNTHETIC_EFFECT_MODEL`. The paper's headline degradation claim remains an unproduced
`(hypothesis)`; the code never asserts it.

## Deterministic scoring (the load-bearing property)
`env.checker.DeterministicChecker` reads only `Trace.recorded_transitions` (and
`Trace.witness_completed`), never `Trace.messages`. This is the code embodiment of Theorem 9.4:
an injection that changes messages but not the recorded state cannot change the verdict.
`env.judge.HijackableDummyJudge` reads messages and can be flipped by a trigger phrase, embodying
Proposition 9.5. The `run_ablation` experiment measures the gap (RQ2).

## Reproducibility
All randomness flows through `utils.seeding.SeededRNG`. `score_config`/`generate_episodes` are
deterministic given a seed (tested). Every result file gets a provenance header
(`utils.io.run_metadata`) with the seed, config hash, version, and the synthetic flag.

## Known simplifications (documented)
- Sybils are modelled as extra adversarial seed identities (a synthetic influence proxy).
- Defense effect-models reduce the effective per-edge `p` uniformly and provide fixed
  detect/recover rates; they do **not** encode any orchestrator/topology-specific effect, so the
  pipeline never manufactures the degradation hypothesis.
- Mesh *fixation* (`CPR -> 1`) is kept at remark level in the paper and is **not** implemented as a
  numeric bound; only the exact one-round mesh bound is implemented.
