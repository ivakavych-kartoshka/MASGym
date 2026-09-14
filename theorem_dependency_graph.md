# Theorem Dependency Graph — MASGym

Flow: **Assumptions → Definitions → Results → Corollaries → Experiments (RQs)**.
Numbers match the compiled PDF. There are no lemmas; the chain is
Assumption/Definition → Proposition/Theorem → Corollary → RQ. This is also the structure drawn in
Figure 4 (`fig:theory`).

```
Definitions 6.1 (predicates) 6.2 (ASR/PNA/NRP) ─────────────► Prop 9.1  (reduction to ASB)
A5 continuous aggregator ─────────────────────────────────► Thm 9.2  (unique product metric) ──► Remark 9.3 (alternatives)
                                                                     │
                                                                     └────► RQ1 (construct validity)

A1 trusted checking ──────────────────────────────────────► Thm 9.4  (evaluator integrity)
                                                             Prop 9.5 (LLM judge hijackable, existence)
                                                                     │           │
                                                             Remark 9.6 (integrity ≠ correctness)
                                                                     └────► RQ2 (deterministic vs judge ablation)

A4 monotone propagation ──► Prop 9.7 chain
                            Prop 9.8 star  ──┐
                            Prop 9.9 tree    ├─► (topology ordering) ────► RQ4 (topology / propagation)
                            Prop 9.10 mesh ──┘
                            Cor 9.11 threshold confinement ─────────────► RQ4 (threshold regime)

A4 + Prop 9.8 (star) ─────────────────────────────────────► Thm 9.13 (strict collusion advantage) ──► Remark 9.14 (model, not real defense)
                                                                     └────► RQ5 (collusion / Sybils)

Definition 6.3 (k-forced) ────────────────────────────────► Prop 9.15 (forced-coordination / hitting set) ──► RQ3, RQ5 (group-level unit)

A2 i.i.d. + A3 bounded ───────────────────────────────────► Thm 9.17 (concentration & sample complexity)
                                                             Cor 9.18 (sweep budget) ──► Sec 8.1 complexity table ──► RQ6 (cost / scalability)
```

## Result → Experiment (RQ) map
| Result | Feeds |
|---|---|
| Thm 9.2, Remark 9.3, Prop 9.1 | RQ1 (construct validity; aggregator-sensitivity ablation) |
| Thm 9.4, Prop 9.5, Remark 9.6 | RQ2 (deterministic-vs-LLM-judge ablation) |
| Props 9.7–9.10, Cor 9.11 | RQ4 (compromise-propagation-rate; topology sweep; Table 3) |
| Thm 9.13, Remark 9.14, Def 6.5 | RQ5 (collusion advantage; Sybil study) |
| Prop 9.15 | RQ3/RQ5 (forced-coordination sabotage; degradation headline) |
| Thm 9.17, Cor 9.18 | RQ6 (episode budget → cost; Table 5; scalability) |

## Notes
- No result depends on an unavailable external ("Idea N") lemma; every external result invoked
  (Hoeffding, Kempe greedy bound, Benjamini–Hochberg) is a published, verified reference.
- The only within-results edge is **Prop 9.8 (star) → Thm 9.13 (collusion)**, drawn in Figure 4.
- Empirical claims (defense degradation, measured $\CPR$ ordering, measured $\Delta_{\mathrm{coll}}$)
  are **downstream** of the theory as *hypotheses to test*, not as proven consequences.
