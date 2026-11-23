# AAMAS 2027 Author Rebuttal (English — Ready for OpenReview)

> **Character limit verified:** Every individual block below is strictly **≤ 2,480 characters** (even counting Windows `\r\n` newlines). Use **Parts 1–4** if OpenReview provides separate reply boxes per reviewer, or **Part 5** if OpenReview provides one single 2,500-character rebuttal box.

---

## 1. General Response (Common to All Reviewers)

<!-- BEGIN:GENERAL -->
We thank all three reviewers for their detailed, constructive critiques. Rather than defending overbroad claims, we ran targeted rebuttal experiments (matched undefended LLM controls, availability-rule ablation, fixed-placement collusion, propagation sensitivity, cluster-aware CIs, and a CoRB bug fix) and prepared a full revision plan.

**Summary of new results & reconciliations:**
1. **Availability-rule ablation (pE9X, Xdct):** Disabling the hard star/tree hub rule removes trivial 1.000 saturation while keeping substantial k-quorum failure: on N=5, M=30 (0% compliance), colluding ASR_sys moves from 1.000 to **0.300** [0.167, 0.479] on star/tree (chain 0.000, mesh 0.433). On synthetic degradation (M=738, star), removing the hub rule cleanly separates defenses (colluding: no-defense 0.657, fixed-threshold 0.539, guardrail 0.424).
2. **Matched undefended controls (pE9X):** At identical N=5, M=30 seeds (1,075 decisions, 0 parse failures), Llama-3.2-1B complies 1,075/1,075 undefended (matching defended: ceiling effect). Because AWS Bedrock deprecated mistral-7b-instruct-v0:2 to Legacy during review, we ran a matched none-vs-delimiting pair on its active successor Ministral-3-8B-Instruct: **0/1,075** compliance in both arms (floor effect), with +26.3% token overhead (213->269 tokens/call). We will retract causal wording ("drives compliance to 0/1,075") and state floor/ceiling scope explicitly.
3. **Controlled collusion (pE9X):** We rename Thm 9.7 to Seed Placement Advantage and isolate pure coordination with fixed count (s=2) and fixed placement across all 4 topologies (M=738): coordinated action raises ASR_act by +0.270..+0.428 and split-payload collusion by +0.104..+0.232 (all Holm p=0.0016).
4. **Cluster-aware CIs & reconciliation (pE9X):** Treating 360 episodes (2.986 dec/ep) as clusters under worst-case greedy ICC=1 yields a 95% upper bound of **0.0106** (Bonf-12: **0.0223**) vs 0.0036. We relabel 41.6%->31.8%->27.6% as **ASR_act**, align two-sided cell CIs ([0,0.114], [0.274,0.608], [0.886,1]), and state cross-context shrinkage is unresolved at M=738.
5. **Reorganization & self-containment (Go5y, Xdct):** We will move Overview + worked task to Sec. 2, cut supplement refs (21-> <=5), define all terms on first use, separate trusted harness (TCB) from compromisable Orchestrator, and bundle `make_defense_table.py`.
<!-- END:GENERAL -->

---

## 2. Response to Reviewer Go5y

<!-- BEGIN:GO5Y -->
Thank you for the clear, actionable feedback on organization and readability. We agree that the current layout forces readers to jump forward and back and hides the researcher workflow behind formal machinery.

**1. Leading with MASGym Overview & Concrete Workflow (Concerns 1 & 4):**
In the revision, we will move the overall architecture and user workflow from Section 7 up to a new **Section 2 (MASGym Overview & Researcher Workflow)** immediately after the Introduction:
- **End-to-end architecture figure** paired with a 5-step researcher loop: (i) select a forced-coordination task and registered deterministic predicates (Psi, Phi), (ii) pick topology (star/chain/tree/mesh) and agent count N, (iii) set adversary vector c_adv = (beta, coll, adapt, orch, tool, syb, mem) and blue defense, (iv) execute seeded episodes via LLMBackboneAdapter or the synthetic emulator, and (v) inspect trace-level metrics (ASR_act, ASR_avail, ASR_sys, NRP_sys) with episode-level cluster-aware CIs.
- **Concrete task scenario in the main text:** We will promote our worked 3-forced "travel-booking" scenario (currently buried in the Supplement, App. A.7) directly into Section 2. Three distinct workers handle itinerary lookup (calendar tool), budget-constrained flight booking (booking tool), and payment execution (payment tool). We show step-by-step how a malicious tool note attempts payment-payee redirection, how Phi reads only recorded state transitions (ignoring natural-language messages), and how a compromised worker/orchestrator can alternatively trigger availability failure by withholding a required subtask.

**2. Eliminating Redundancy & Clarifying Related Work (Concerns 2 & 3):**
- We will remove duplicated framing across the Abstract, Introduction, and Related Work, and trim the "what MASGym is not" prose.
- We will replace vague related-work summaries with a compact **comparison table** contrasting ASB, AgentDojo, InjecAgent, ToolEmu, and MASGym along five concrete axes: multi-agent interaction, forced coordination, communication topology, parameterized adversary (collusion/orchestrator/Sybils), and deterministic trace checker.
- Every section will introduce notation sequentially before use, with a compact notation table in Section 2, so the main paper reads linearly and self-contained without flipping to the Supplement.
<!-- END:GO5Y -->

---

## 3. Response to Reviewer Xdct

<!-- BEGIN:XDCT -->
Thank you for the thorough critique. We address each technical and presentation concern directly with new ablations and concrete revisions.

**1. Predefined topology rules & saturation (Concern 1):**
You are right that our hub-critical availability rule forced ASR_sys=1.000 on star/tree whenever the hub was compromised. We ran an ablation separating action failure, quorum exhaustion, and hub-rule failure:
- On N=5, M=30 (0% compliance), **removing the hard hub rule** drops colluding ASR_sys from 1.000 to **0.300** [0.167, 0.479] on star/tree (comp. orch.: 0.233/0.167), while chain stays 0.000 and mesh 0.433—showing non-trivial k-quorum failure remains without saturation.
- On synthetic degradation (M=738, star, beta=0.3), removing the hub rule eliminates 1.000 saturation and cleanly distinguishes defenses: colluding ASR_sys is 0.657 (no-defense), 0.539 (fixed-threshold), and 0.424 (guardrail). We will report both full and no-hub decompositions alongside ASR_act.

**2. Threshold propagation & theta sensitivity (Concern 2):**
We agree the threshold rule ("compromised once >=theta in-neighbors are") is a stylized model, not a claim about real-world LLM infection. We ran a sensitivity study (N in {5,10}, beta=0.3, M=738) comparing ThresholdCascade (theta=1,2,3) vs IndependentCascade (p=0.1,0.3,0.5) and stochastic Linear Threshold (U(0,1)):
- At theta>=2, sparse topologies (chain, tree; max in-degree 1) halt completely (CPR=0.000), while dense mesh still percolates (CPR=1.000, even at theta=3, N=10).
- Across stochastic models (IC p=0.3, LT), dense-vs-sparse vulnerability ordering (mesh > star > tree/chain in CPR) persists qualitatively. We will state explicitly that propagation models are stylized analytical abstractions.

**3. Self-containment, script, notation, & TCB vs Orchestrator (Concerns 3–10):**
- **Self-containment & theory:** We will cut Supplement refs from 21 to <=5, keep 3–4 core theorems in plain language with brief proof sketches and explicit assumptions, and move secondary corollaries to the Appendix.
- **Script:** `make_defense_table.py` (in the repo) and `run_rebuttal_studies.py` will be included in the supplementary archive.
- **Notation & TCB:** We will drop subscripted/undefined acronyms from the Abstract, define NRP, PNA, ASR, Phi, Psi, and TCB on first use, and separate the **trusted runtime harness (TCB)** (trace logger + checker) from the **LLM Orchestrator agent** (untrusted, subject to compromise).
<!-- END:XDCT -->

---

## 4. Response to Reviewer pE9X

<!-- BEGIN:PE9X -->
Thank you for this insightful review. Every concern identified a real methodological weakness; we ran targeted experiments to resolve each honestly.

**1. Availability saturation (Con 1):**
Disabling the hard star/tree hub rule on N=5, M=30 (0% compliance) drops colluding ASR_sys from 1.000 to **0.300** [0.167,0.479] on star/tree (comp. orch.: 0.233/0.167; chain 0.000; mesh 0.433), isolating k-quorum exhaustion. On synthetic degradation (M=738, star), removing it resolves defenses (colluding: none 0.657, fixed-threshold 0.539, guardrail 0.424). We will report ASR_act, ASR_sys(no-hub), and ASR_sys(full).

**2. Matched undefended controls (Con 2):**
At exact N=5, M=30 seeds (1,075 decisions, 0 parse fails):
- **Llama-3.2-1B (none):** 1,075/1,075 compliance (matches defended: ceiling effect).
- **Ministral-3-8B-Instruct (Bedrock):** Since AWS deprecated mistral-7b-instruct-v0:2 to Legacy, we ran a matched none-vs-delimiting pair on its active successor: **0/1,075** compliance in both arms (floor effect, matching Qwen pilots) with **+26.3%** token overhead (213->269/call).
We retract "drives compliance to 0/1,075" and frame Table 1 as zero- vs full-compliance regimes.

**3. Controlled collusion vs placement (Con 3):**
We rename Thm 9.7 to *Seed Placement Advantage* (s=1 central vs random CPR: +0.134 tree, +0.122 star, +0.033 chain, -0.032 n.s. mesh). Fixing count (s=2), placement (random/central), and propagation across 4 topologies (M=738), pure coordination raises ASR_act by **+0.270..+0.428** (effort) and **+0.104..+0.232** (split-payload), all Holm p=0.0016.

**4. Theory, CoRB, & scope (Cons 4–5):**
We make homogeneity/determinism/pi(tau) assumptions explicit and clarify checker integrity != predicate correctness. We fixed a blue-policy reuse bug in `run_corb_sweep.py` (fresh blue, M=200: chain_adaptive ASR_sys=0.310/NRP=0.635; star_adaptive 0.415/0.521), note the synthetic cost proxy omits defense overhead (unlike +26.3% on Ministral), and downgrade CoRB to a proposed protocol with synthetic validation.

**5. Cluster CIs & reconciliation (Cons 6–7):**
1,075 decisions cluster in 360 episodes (2.986/ep). Under greedy ICC=1 (N_eff=360), 0-compliance 95% upper bound is **0.0106** (Bonf-12: **0.0223**), not 0.0036. We align cell CIs ([0,0.114], [0.274,0.608], [0.886,1]; Bonf-12: [0,0.215], [0.218,0.678], [0.785,1]), relabel 41.6%->31.8%->27.6% as **ASR_act**, and note shrinkage is unresolved at M=738 (p=0.083, 0.292).
<!-- END:PE9X -->

---

## 5. Single-Box Combined Rebuttal (Use ONLY if OpenReview has ONE 2,500-char box total)

<!-- BEGIN:SINGLE -->
We thank all reviewers for their thorough critiques. During rebuttal we ran targeted experiments and prepared a full revision plan.

**1. Availability ablation (pE9X, Xdct):** Disabling the hard star/tree hub rule removes trivial 1.000 saturation while keeping k-quorum failure: on N=5, M=30 (0% compliance), colluding ASR_sys drops from 1.000 to **0.300** [0.167,0.479] on star/tree (comp. orch.: 0.233/0.167; chain 0.000; mesh 0.433). On synthetic degradation (M=738, star), removing it cleanly separates defenses (colluding: none 0.657, fixed-threshold 0.539, guardrail 0.424). We will report ASR_act, ASR_sys(no-hub), and ASR_sys(full).

**2. Matched undefended controls (pE9X):** On identical N=5, M=30 seeds (1,075 decisions, 0 parse fails): Llama-3.2-1B complies 1,075/1,075 undefended (ceiling effect). Since AWS deprecated mistral-7b-instruct-v0:2 to Legacy, we ran a matched none-vs-delimiting pair on active Ministral-3-8B-Instruct: **0/1,075** compliance in both arms (floor effect, matching Qwen pilots) with +26.3% token cost (213->269/call). We retract "drives compliance to 0/1,075" and frame Table 1 as zero- vs full-compliance regimes.

**3. Controlled collusion & propagation (pE9X, Xdct):** We rename Thm 9.7 to Seed Placement Advantage and isolate coordination with fixed count (s=2) and fixed placement across 4 topologies (M=738): coordinated effort raises ASR_act +0.270..+0.428 and split-payload +0.104..+0.232 (all Holm p=0.0016). Sweeping ThresholdCascade (theta=1..3) vs IndependentCascade (p=0.1..0.5) and LinearThreshold (N=5,10) shows theta>=2 halts chain/tree (CPR=0) while mesh percolates (1.0), and dense>sparse persists across stochastic models; we frame threshold rules as stylized.

**4. Cluster CIs, CoRB, & reconciliation (pE9X):** Clustering 360 episodes (ICC=1) yields 0-compliance 95% upper bound 0.0106 (Bonf-12: 0.0223) vs 0.0036; cell CIs align to [0,0.114]/[0.274,0.608]/[0.886,1]. We relabel 41.6%->31.8%->27.6% as **ASR_act** (shrinkage unresolved at M=738: p=0.083/0.292), fix a blue-policy reuse bug in `run_corb_sweep.py`, and downgrade CoRB to a proposed protocol with synthetic validation.

**5. Structure & clarity (Go5y, Xdct):** We move Overview + workflow + travel-booking task to Sec. 2, add a related-work table, cut supplement refs (21-> <=5), define all acronyms on first use, separate trusted harness (TCB) from compromisable Orchestrator, and bundle `make_defense_table.py`.
<!-- END:SINGLE -->
