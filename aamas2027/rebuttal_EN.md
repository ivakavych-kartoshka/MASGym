# AAMAS 2027 Author Rebuttal (English — Ready for OpenReview)

> **OpenReview format:** Markdown formatting and LaTeX formulas (`$...$`), verified strictly **≤ 2,500 characters** per response (including spaces and `\r\n` newlines).

---

## 1. Response to Reviewer Go5y

<!-- BEGIN:GO5Y -->
Thank you for the feedback on organization. We agree that the current version makes readers jump between sections, and the way researchers actually use MASGym is buried under the formal definitions.

**1. Moving the overview and researcher workflow to Section 2 (Concerns 1 & 4):**
In the revision, the system overview and workflow (now in Section 7) will move to Section 2, right after the Introduction. This section will present an end-to-end architecture figure alongside the researcher's five steps: (i) choose a forced-coordination task with its deterministic predicates $(\Psi, \Phi)$; (ii) select a topology (`star`, `chain`, `tree`, or `mesh`) and the number of agents $N$; (iii) configure the adversary vector $c_{adv} = (\beta, \text{coll}, \text{adapt}, \text{orch}, \text{tool}, \text{syb}, \text{mem})$ together with the blue-side defense; (iv) run seeded episodes through `LLMBackboneAdapter` or the synthetic emulator; and (v) read a trace-level report with $ASR_{act}$, $ASR_{avail}$, $ASR_{sys}$, and $NRP_{sys}$, plus episode-level cluster-aware CIs.

The 3-forced "travel-booking" example, currently in the Supplement (Appendix F.7), will also move into the main text. Three workers handle itinerary lookup, budget-constrained booking, and payment. The example walks through three concrete situations: a malicious tool injects an instruction to change the payee; $\Phi$ reads only recorded state transitions and ignores conversational text; and a compromised worker or orchestrator causes an availability failure by withholding a required subtask.

**2. Removing redundancy and clarifying Related Work (Concerns 2 & 3):**
We will cut the passages repeated across the Abstract, Introduction, and Related Work, and shorten the discussions of "what MASGym is not." The vague summaries will be replaced by a compact table comparing ASB, AgentDojo, InjecAgent, ToolEmu, and MASGym on five criteria: multi-agent interaction, forced coordination, communication topology, a parameterized adversary model (collusion/orchestrator/Sybil), and deterministic trace checking. Every notation will be introduced before it is used, with a compact notation table in Section 2, so the main paper can be read without opening the Supplement.
<!-- END:GO5Y -->

---

## 2. Response to Reviewer Xdct

<!-- BEGIN:XDCT -->
Thank you for the careful reading. We address each point below with new experiments run during the rebuttal.

**1. Do the results just reflect predefined topology rules? (Concern 1):**
You are right: the hard hub rule forces $ASR_{sys} = 1.000$ on `star` and `tree` whenever the hub is compromised. We ran an ablation separating action failure, quorum exhaustion, and the hub rule. At $N=5, M=30$ ($0\%$ compliance), removing the hard hub rule drops colluding $ASR_{sys}$ from $1.000$ to **$0.300$** $[0.167, 0.479]$ on `star` and `tree` ($0.233$ and $0.167$ with a compromised orchestrator), while `chain` stays at $0.000$ and `mesh` is $0.433$. System failure from $k$-quorum exhaustion thus remains substantial without saturation. On synthetic degradation ($M=738$, `star`, $\beta=0.3$), removing the hub rule also eliminates saturation and separates defenses (colluding: no-defense $0.657$, fixed-threshold $0.539$, guardrail $0.424$). We will report both modes alongside $ASR_{act}$.

**2. Threshold propagation and sensitivity to $\theta$ (Concern 2):**
We agree that the threshold rule is a stylized model, not a claim about how compromise spreads between real LLMs. We ran a sensitivity study ($N \in \{5,10\}$, $\beta=0.3$, $M=738$) comparing `ThresholdCascade` ($\theta \in \{1,2,3\}$) with `IndependentCascade` ($p \in \{0.1,0.3,0.5\}$) and a stochastic `LinearThreshold` ($U(0,1)$). For $\theta \ge 2$, sparse graphs (`chain`, `tree`, max in-degree $1$) stop spreading ($CPR=0.000$), while dense `mesh` still reaches the full network ($CPR=1.000$, even at $\theta=3, N=10$). Under the stochastic models (IC $p=0.3$ and LT), the vulnerability ordering $\text{mesh} > \text{star} > \text{tree/chain}$ still holds. We will state clearly that these are stylized analytical models.

**3. Self-containment, scripts, notation, and TCB (Concerns 3–10):**
Supplement references will drop from $21$ to at most $5$. We will keep 3–4 core theorems stated in plain language with proof sketches and explicit assumptions, moving secondary corollaries to the Supplement. `make_defense_table.py` and `run_rebuttal_studies.py` will be included in the supplementary archive. The Abstract will drop undefined and subscripted acronyms; NRP, PNA, ASR, $\Phi$, $\Psi$, and TCB will each be defined at first use. Finally, we will separate the **trusted runtime harness (TCB)** (trace logger and checker) from the untrusted **LLM Orchestrator agent**, which can be compromised.
<!-- END:XDCT -->

---

## 3. Response to Reviewer pE9X

<!-- BEGIN:PE9X -->
Thank you for the feedback; we ran targeted experiments to address each point.

**1. Availability saturation (Con 1):** Disabling the hard hub rule on `star` and `tree` at $N=5, M=30$ ($0\%$ compliance) dropped colluding $ASR_{sys}$ from $1.000$ to **$0.300$** $[0.167, 0.479]$ on both ($0.233$ and $0.167$ under a compromised orchestrator), while `chain` stayed $0.000$ and `mesh` $0.433$, isolating $k$-quorum failure. On synthetic degradation ($M=738$, `star`), removing it separated colluding defenses ($0.657$ none, $0.539$ fixed-threshold, $0.424$ guardrail). We will report $ASR_{act}$ with both $ASR_{sys}$ modes.

**2. Matched controls (Con 2):** Running `--defense none` at $N=5, M=30$ on all four backbones ($0$ parse fails) showed floor effects on `Qwen2.5-3B` (**$1/1093$**, $0.09\%$) and `Qwen2.5-7B-4bit` (**$0/1093$**, $0\%$) vs $0/1075$ defended, and a ceiling effect on `Llama-3.2-1B` (**$1075/1075$** in both). Since AWS moved `mistral-7b-instruct-v0:2` to Legacy, we ran a `none` vs `delimiting` pair on `Ministral-3-8B-Instruct`: **$0/1075$** compliance in both arms with **$+26.3\%$** token cost ($213 \to 269$/call). We will drop "drives compliance to $0/1075$" and frame Table 1 as zero- vs full-compliance.

**3. Collusion vs placement (Con 3):** We will rename Thm 9.7 *Seed Placement Advantage* ($s=1$ central vs random CPR: $+0.134$ `tree`, $+0.122$ `star`, $+0.033$ `chain`, $-0.032$ not significant on `mesh`). Fixing attacker count ($s=2$), placement (random/central), and propagation across 4 topologies ($M=738$), coordination raised $ASR_{act}$ by **$+0.270$ to $+0.428$** (effort) and **$+0.104$ to $+0.232$** (split-payload), all $p_{Holm}=0.0016$.

**4. Theory, CoRB, & CIs (Cons 4–7):** We fixed blue-policy reuse in `run_corb_sweep.py` ($M=200$: `chain_adaptive` $ASR_{sys}=0.310, NRP=0.635$; `star_adaptive` $0.415, 0.521$). We will state homogeneity, determinism, and $\pi(\tau)$ assumptions, note checker integrity $\neq$ predicate correctness, and frame CoRB as a proposed protocol with synthetic validation (cost omits defense overhead). Grouping $1075$ decisions into $360$ episodes ($2.986$/ep; $ICC=1 \Rightarrow N_{eff}=360$) gave a $95\%$ upper bound on the zero-compliance rate of **$0.0106$** (vs $0.0036$ if independent; Bonferroni-12: **$0.0223$**). We will align cell CIs ($[0,0.114], [0.274,0.608], [0.886,1]$), relabel $41.6\% \to 31.8\% \to 27.6\%$ as $ASR_{act}$, and note shrinkage is unresolved at $M=738$ ($p=0.083, 0.292$).
<!-- END:PE9X -->
