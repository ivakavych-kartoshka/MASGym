# Reviewer-Style Self-Audit — MASGym

Written as an adversarial reviewer from NeurIPS D&B / ICLR / USENIX Security / IEEE S&P / AAMAS.

## Locked topic
A benchmark/environment + evaluation methodology for the security of multi-agent LLM systems,
with parameterized collusion, orchestrator/tool compromise, Sybils, and poisoned memory, and
system-level metrics (generalizing ASB's NRP), scored by a deterministic checker; ships a
degradation `(hypothesis)`. (See `idea_fidelity_report.md`, `topic_signature.json`.)

## Does the manuscript match `idea.pdf`?
Yes. See `topic_alignment_check.md`: title, abstract, contributions, system/threat model,
theorem directions, algorithm (CoRB), experiment plan, figures, and seed references all align.
It is an **environment/methodology** paper, not a new attack or defense — consistent with the idea.

## Final contribution list
1. An environment + forced-coordination task suite for multi-agent LLM security (roles, partial
   observability, star/chain/tree/mesh, 3–50 agents).
2. A natively parameterized adversary model (fraction, collusion, adaptivity, orchestrator
   compromise, malicious tools, Sybils, poisoned memory).
3. A system-level metric suite incl. $\NRPs=\PNAs(1-\ASRs)$, deterministically scored.
4. The CoRB co-evolving red/blue protocol.
5. Instrument-supporting theory (metric characterization, evaluator integrity, propagation +
   collusion separation, forced-coordination bound, estimator concentration).
6. A headline degradation **hypothesis** with a protocol to test it.

## Main novelty claims & supporting evidence
| Claim | Evidence | Boundary set by |
|---|---|---|
| First environment purpose-built for MA LLM security (to our knowledge, within verified lit.) | MASEC §4.7 states none exists | `schroederdewitt2025masec`; single-agent scope of `zhang2025asb`,`debenedetti2024agentdojo`,`ruan2024toolemu` |
| System-level NRP is justified, not asserted | Thm 9.2 + Remark 9.3 (uniqueness relative to axioms; alternatives shown) | generalizes `zhang2025asb` NRP |
| Deterministic checker not hijackable by messages | Thm 9.4 + Prop 9.5 (existence of judge hijack) | `debenedetti2024agentdojo`; judge bias `zheng2023judging`,`wang2023fair` |
| Collusion/topology shape measured compromise | Props 9.7–9.10, Cor 9.11, Thm 9.13 | cascade/percolation `kempe2003maximizing`,`watts2002simple`,`chalupa1979bootstrap` |

## Likely reviewer objections & responses
1. **"A benchmark without measured results."** — Acknowledged; the paper is explicit that all
   numbers are placeholders/`(hypothesis)` and ships the theory + protocol. **Before submission the
   sweeps must be run** (see `TODO_before_submission.md`); this is the single biggest gap.
2. **"Emulation fidelity (κ≈0.48) undermines validity."** — Addressed: scoring is routed through the
   deterministic checker (not the emulator's verdict), and an emulated-vs-real-tools ablation is
   specified. Absolute numbers are framed as comparative.
3. **"The metric is arbitrary."** — Addressed by Thm 9.2 (axiomatic) + Remark 9.3 (alternatives) +
   RQ1 aggregator-sensitivity ablation.
4. **"The propagation theorems are about a toy model, not LLM agents."** — Explicitly conceded
   (Remark 9.14, Limitations): they characterize the environment's dynamics and predict where to
   look; measured $\CPR$ adjudicates realism.
5. **"Is this just ASB×N / AgentDojo-at-scale?"** — Rebutted in §2.7 with the concrete distinctions
   (no collusion/orchestrator-trust/topology in ASB; single-agent checker in AgentDojo).
6. **"Compute cost."** — Quantified (§8.1 complexity, Cor 9.18); the reachable region is reported
   rather than implied to be exhaustive.

## Theorem / proof risks
- Thm 9.13 body says "Proof sketch" while the full proof is in App. A — ensure the appendix pointer is
  obvious to reviewers (it is boxed). Low risk.
- The mesh fixation ($\CPR\to1$) is a remark-level extrapolation, not a theorem — correctly labelled.
- All other results have complete in-paper proofs. No result depends on an unavailable "Idea N" lemma.

## Experiment gaps
- No real measurements yet (all placeholder). Claude-3.5 exact variant, per-model decoding, and the
  final $M,R,G$ budgets must be fixed. Real-tool subset for the fidelity ablation must be built.

## Overclaiming risks
- Only one "first" claim, guarded and citation-grounded (see `claim_strength_audit.md`). No
  "optimal/sharp/matching/SOTA/superior." Headline finding marked `(hypothesis)` throughout.

## Figure readability status
All six figures rendered and inspected; Fig. 4 and Fig. 5 revised for overlaps; all PASS
(`figure_quality_audit.md`).

## LaTeX compilation status
Compiles with `pdflatex`+`bibtex` (local `elsarticle` shim). 41 pages. 0 undefined
references/citations. 9 minor overfull hboxes (worst ≈46 pt), no fatal errors. One benign font
substitution (`T1/lmr/bx/sc`).

## Citation verification status
83 verified references, all cited, none dangling. 4 full-text; ~59 abstract-only (arXiv abs page);
~20 metadata-only (DOI/publisher). Seed refs + 17 anchors verified against primary pages this
session; corpus-pool entries inherit the sibling project's verification and are flagged for an
independent re-check (`citation_todo.md`). No fabricated entries.

## Bottom line
The manuscript is a coherent, faithfully-expanded, rigorously-hedged benchmark paper with a real
theoretical core and journal-quality figures. Its acceptance-critical dependency is running the
sweeps to convert the `(hypothesis)` results into measured findings.
