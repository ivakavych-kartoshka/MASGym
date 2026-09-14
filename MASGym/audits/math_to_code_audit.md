# Math-to-Code Audit — MASGym

Audit of every equation / theorem / algorithmic step implemented, its code interpretation, edge
cases, internal consistency, and any correction needed for a mathematically sound implementation.
The paper is internally consistent on all objects implemented here; where the paper leaves a modelling
choice open, the code implements the **explicitly stated** instance and documents it.

Legend for "consistent?": **YES** = definition, theorem, and any algorithm agree.

| Paper loc | Object | Code interpretation | Edge cases handled | Consistent? | Correction / note |
|---|---|---|---|---|---|
| Eq (1) | `NRP = PNA·(1−ASR)` | `aggregators.product_nrp(pna, asr)` | clamp inputs to `[0,1]`; validate | YES | — |
| Eq (2) | `c_adv=(β,coll,adapt,orch,tool,syb,mem)` | `data.schemas.AdversaryConfig` (validated dataclass) | `β∈[0,1]`; enum fields | YES | — |
| Eq (3) | `ASR_sys=P[Φ(τ)=1]` | `metrics.asr_sys(verdicts)` = mean of `Φ` indicators | empty sample → `nan` + warning | YES | — |
| Eq (4) | `PNA_sys=P[Ψ(τ)=1]` on benign `c°` | `metrics.pna_sys(...)`; benign counterpart built by `AdversaryConfig.benign()` | empty sample → `nan` | YES | `c°` = adversary removed (β=0, all knobs off) |
| Eq (5) | `NRP_sys=PNA_sys(1−ASR_sys)` | `metrics.nrp_sys(...)` via `product_nrp` | inherits clamps | YES | — |
| Eq (6) | `CPR=E[(|B∞|−|B0|)/(N−|B0|)]` | `metrics.cpr(...)`; per-episode fraction averaged | `N−|B0|=0` (all seeded) → define `CPR=0`, warn | YES | division-by-zero guarded (no honest agents to compromise) |
| Prop 9.1 | reduction to ASB at `N=1` | `theory.metric_axioms.reduces_to_asb()` unit test | — | YES | product form identical at N=1 |
| Thm 9.2 | product aggregator unique under D2/D4 | `aggregators.{product_nrp,min_agg,weighted_geom}` + `metric_axioms.check_axioms()` | `weighted_geom` `0^0` → 0 by convention | YES | uniqueness *relative to axioms*; alternatives provided, not claimed optimal. Verified numerically: `product` passes D1-D4; `min` fails D4; `weighted_geometric` fails D2 and D4 (it satisfies a *different* log-linearity axiom set, Remark 9.3) — exactly why Thm 9.2 singles out the product |
| Thm 9.4 | evaluator integrity | `env.checker.DeterministicChecker.score(trace)` depends only on `trace.recorded_transitions` | ignores `trace.messages` entirely | YES | integrity ≠ correctness (documented) |
| Prop 9.5 | LLM judge hijackable (existence) | `env.judge.HijackableDummyJudge` flips on trigger phrase, state unchanged | — | YES | dummy for tests only; real judge is an adapter |
| Prop 9.7 | chain reach `Σ p^j ≤ p/(1−p)` | `theory.propagation_bounds.chain_expected_reach(n,p)` | `p=1` → returns `n−1` (limit) | YES | closed form + MC test |
| Prop 9.8 | star centre `p(n−1)`, leaf `p+p²(n−2)` | `star_centre_expected_reach`, `star_leaf_expected_reach` | `n<2` → 0 | YES | — |
| Prop 9.9 | tree `Σ (bp)^ℓ` | `tree_expected_reach(b,p,d)`; subcrit/​supercrit branches | `bp=1` → linear `d` | YES | Galton–Watson mean; documented |
| Prop 9.10 | mesh one round `s+(n−s)(1−(1−p)^s)` | `mesh_one_round_expected(n,s,p)` | `s≥n` → `n` | YES | one-round only; fixation is a remark, NOT implemented as a bound |
| Cor 9.11 | threshold confinement | `env.propagation.ThresholdCascade`; in-degree `<θ` never infects | isolated nodes | YES | chain `θ≥2` ⇒ CPR 0 (unit test) |
| Thm 9.13 | collusion gap `p(1−p)(N−1)(N−2)/N` | `collusion_gap_star(N,p)`; MC of colluding vs independent seeding | `N<3` → 0 | YES | exact single-seed gap; MC test tolerance |
| Prop 9.15 | forced-coordination / hitting set | `env.orchestration` witness model; `is_transversal()` | `k>N` → infeasible flag | YES | success needs an adversary-free witness |
| Thm 9.17 | Hoeffding `M≥ln(2/α)/(2ε²)`; NRP `4e^{−2Mε²}` | `theory.sample_complexity.hoeffding_min_samples`, `nrp_confidence_delta`; `metrics.confidence_intervals.hoeffding_ci` | `ε=0`/`α∈{0,1}` → ValueError | YES | CI is two-sided marginal; documented |
| Cor 9.18 | sweep budget `M=O(Δ⁻²ln(G/α))` | `sample_complexity.sweep_budget(G,delta,alpha)` and `total_invocations` | `Δ=0` → ValueError | YES | uses `ε=Δ/4` per proof |
| §8.1 | complexity `Θ(NH)`, `Θ((N+|E|)H)` | `theory.sample_complexity.episode_cost`, `sweep_cost` (symbolic counters, not timings) | — | YES | returns operation counts, never fake wall-clock |

## Special checks requested by the task template (conformal-style) — adapted to MASGym
The template asked to check score/calibration independence, coverage-event matching, tie-breaking,
test-dependent thresholds, group-conditional vs pointwise coverage. **MASGym is not a conformal method**,
so those specific checks map as follows:
- **"Calibration class matches the guaranteed error event":** MASGym's analogue is that the
  **deterministic checker's predicate `Φ` matches the compromise event being measured** — verified by
  construction (the checker reads exactly the recorded security-relevant transitions). No coverage
  guarantee is claimed; only a marginal Hoeffding CI on the mean indicator.
- **"Ties require randomized tie-breaking":** MASGym metrics are means of `{0,1}` indicators; there is
  no threshold-on-scores step, so no tie-breaking is needed. (The optional `fixed_threshold` defense
  uses a `≥` comparison on a synthetic risk score; ties resolve deterministically to *defer/flag*, the
  conservative choice, documented in `baselines/fixed_threshold.py`.)
- **"Group-conditional vs pointwise conditional":** MASGym reports **group-conditional** false-
  certification / ASR by topology and by role via `metrics.group_conditional_asr`; the code never
  claims exact pointwise-conditional guarantees.
- **"Weighted / test-dependent thresholds":** not applicable (no weighted-conformal step in the paper).

## Conservative-implementation decisions
1. `CPR` when all agents are seeded (`N=|B0|`) is defined as `0` (no initially-honest agents to
   compromise) rather than `nan`, and a warning is logged. This is the conservative reading of Eq (6).
2. The **synthetic defense effect-models** (how a lifted per-agent defense reduces effective `p`) are
   *chosen parameters*, not measured efficacies. They are labelled `SYNTHETIC_EFFECT_MODEL` in code and
   in every output. No degradation conclusion is drawn from them — the paper's headline finding remains
   an unproduced `(hypothesis)`.
3. Mesh *fixation* (`CPR→1`) is deliberately **not** implemented as a numeric bound (the paper keeps it
   at remark level); only the exact one-round bound (Prop 9.10) is implemented.

## Inconsistencies detected
**None** between the paper's definitions, theorems, and algorithms for the implemented objects. All
closed forms are re-derived in the paper's Appendix A and match the code; the numerical tests in
`tests/test_propagation.py`, `tests/test_aggregators.py`, and `tests/test_sample_complexity.py`
cross-check code against these closed forms. Any future discrepancy is to be recorded here and flagged
`paper_inconsistency_detected` in the traceability CSV.
