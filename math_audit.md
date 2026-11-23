# Mathematical Audit — MASGym

Audit of every Assumption, Definition, Proposition, Theorem, Corollary in
`sections/theory.tex`, `sections/problem_formulation.tex`, and `appendix/proofs.tex`.
Numbering matches the compiled PDF (theorem environments numbered by Section 9; definitions by
Section 6). Every result is stated under explicit assumptions with an honest proof-status label.

## Assumptions (Section 9.1)
- **A1 (`as:tcb`) trusted checking:** harness records faithful trace $\Trace$; $\Checker$ is a
  function of $\Trace$ only. Used by Thm 9.4.
- **A2 (`as:iid`) i.i.d. episodes;** **A3 (`as:bounded`) bounded $\{0,1\}$ indicators.** Used by Thm 9.17, Cor 9.18.
- **A4 (`as:prop`) monotone propagation** (independent-cascade with $\pinf$; threshold with $\thresh$). Used by Props 9.7–9.10, Cor 9.11, Thm 9.13.
- **A5 (`as:cont`) continuous aggregator.** Used by Thm 9.2.
All assumptions are stated *before* the results that use them. No hidden assumptions
(strong convexity, sub-Gaussianity, spectral gap, channel inversion, etc.) are invoked.

## Definitions (Section 6)
6.1 predicates $\Predsec,\Predutil:\TraceSp\to\{0,1\}$; 6.2 $\ASRs,\PNAs,\NRPs$ (domains $[0,1]$);
6.3 $k$-forced-coordination (witness family); 6.4 compromise relation + $\CPR\in[0,1]$;
6.5 collusion success rate / advantage. **Dimensional check: PASS** — all metrics are
probabilities/fractions in $[0,1]$; $\NRPs=\PNAs(1-\ASRs)\in[0,1]$.

---

## Prop 9.1 (`prop:reduction`) — reduction to ASB
- **Statement:** $N=1$ with single-agent predicates $\Rightarrow \NRPs=\mathrm{NRP}$ of Eq. (1).
- **Assumptions:** Definitions 6.1–6.2. **Proof status: complete.**
- **External theorem used:** none (definitional). **Possible gap:** none.
- **Too strong?** No — it is an identity at $N=1$. **Revision:** none.

## Thm 9.2 (`thm:metric`) — axiomatic characterization of $\NRPs$
- **Statement:** under D2 (consistency), D4a/D4b (utility/security homogeneity), A5, the unique
  aggregator is $g(u,\sigma)=u\sigma$; also bounded and monotone.
- **Proof status: complete** (functional-equation argument; continuity only extends identities to
  irrationals — detail in `appendix/proofs.tex`).
- **External theorem used:** none. **Dimensional check:** $g:[0,1]^2\to[0,1]$. PASS.
- **Too strong?** Guarded by **Remark 9.3**, which states the product is unique *relative to*
  D2/D4 and exhibits alternatives ($\min$, weighted geometric mean). Not claimed "optimal".
- **Revision:** none; wording already relativized.

## Thm 9.4 (`thm:integrity`) — evaluator integrity
- **Statement:** under A1, equal traces $\Rightarrow$ equal verdicts; message-only manipulations
  that leave $\Trace$ unchanged cannot change $\Predsec$ or the estimators.
- **Proof status: complete** (a function of $\Trace$ is invariant to non-arguments).
- **Possible gap / limitation:** integrity $\neq$ correctness; predicate mis-specification and TCB
  compromise are out of scope — **stated explicitly in Remark 9.6.** Not overclaimed.

## Prop 9.5 (`prop:judgehijack`) — an LLM judge is hijackable
- **Statement:** *there exist* a judge $\Judge$ and a message manipulation $\pi$ with
  $\Trace_\pi=\Trace$ flipping the verdict.
- **Proof status: complete (existence/constructive).** **External support:** consistent with
  documented judge bias `zheng2023judging`,`wang2023fair` (cited as evidence, not as proof).
- **Too strong?** No — an *existence* claim, not "all judges always fail". Correctly scoped.

## Props 9.7–9.10 (`prop:chain/star/tree/mesh`) — topology propagation
- **Statements:** chain reach $\le\pinf/(1-\pinf)$; star centre-seed reach $\pinf(n-1)$ vs leaf
  $\pinf+\pinf^2(n-2)$; tree reach $\sum_\ell(b\pinf)^\ell$ with transition at $b\pinf=1$; mesh
  one-round $\ge s+(n-s)(1-(1-\pinf)^s)$.
- **Proof status: complete** for the stated (independent-cascade) model; full proofs in
  `appendix/proofs.tex`. Mesh **fixation** ($\CPR\to1$) is a **remark-level** extrapolation citing
  cascade/percolation literature `kempe2003maximizing`,`watts2002simple` — labelled as such, not
  proved as a theorem.
- **Asymptotic check:** chain $O(1)$; star $\Theta(\pinf n)$; tree $\Theta((b\pinf)^d)$ supercrit.;
  mesh $\to1$. PASS. **Too strong?** No — explicitly "in the environment's model," not an empirical
  law (stated in the surrounding text and Remark 9.14).

## Cor 9.11 (`cor:threshold`) — threshold confinement
- **Statement:** under the threshold model, in-degree $<\thresh$ nodes never compromise; chain with
  $\thresh\ge2$ has $\CPR=0$. **Proof status: complete** (definitional). **Too strong?** No.

## Thm 9.13 (`thm:collusion`) — strict collusion advantage on the star
- **Statement:** single-seed star; colluding (centre) vs independent (uniform) placement; gap
  $\Delta_{\mathrm{coll}}=\pinf(1-\pinf)\frac{(N-1)(N-2)}{N}=\Theta(\pinf(1-\pinf)N)>0$ for
  $\pinf\in(0,1)$, $N\ge3$.
- **Proof status: complete.** Body labels it "Proof sketch"; the **full exact computation is in
  `appendix/proofs.tex`** (boxed result). **External theorem used:** the $s>1$ generalization cites
  the greedy $(1-1/e)$ influence-max bound `kempe2003maximizing` as *their* result; our claim is
  only the exact single-seed gap.
- **Dimensional/asymptotic check:** $(N-1)(N-2)/N>0$ for $N\ge3$; $\Theta(N)$ for fixed $\pinf$. PASS.
- **Too strong?** No — Remark 9.14 states this is a property of the model, **not** a claim that real
  defenses degrade (that is the empirical hypothesis). No "matching/sharp/optimal" language used.

## Prop 9.15 (`prop:forced`) — forced-coordination lower bound + hitting set
- **Statement:** (a) no set $<k$ completes a $k$-forced task; (b) adversary transversal of the
  witness family can force $\Predutil=0$; adversary-free witness $\Rightarrow$ completable.
- **Proof status: complete** (from Definition 6.3). **Too strong?** No — definitional/combinatorial.

## Thm 9.17 (`thm:sample`) — concentration & sample complexity
- **Statement:** (a) Hoeffding $2e^{-2M\epsilon^2}$; (b) product bound $|\widehat{\NRPs}-\NRPs|\le
  |\widehat{\PNAs}-\PNAs|+|\widehat{\ASRs}-\ASRs|$, $4e^{-2M\epsilon^2}$; (c) Bonferroni/BH over $G$.
- **Proof status: complete.** **External theorem used:** Hoeffding `hoeffding1963probability`
  (assumptions — bounded i.i.d. — verified via A2/A3); FDR `benjamini1995controlling`; general
  concentration `boucheron2013concentration`, McDiarmid `mcdiarmid1989bounded` (mentioned as
  alternatives). **Dimensional check:** product Lipschitz bound proved in appendix; all terms in
  $[0,1]$. PASS. **Too strong?** No.

## Cor 9.18 (`cor:budget`) — sweep budget
- **Statement:** $M=O(\Delta^{-2}\ln(G/\alpha))$ per config; total $\Theta(GNH\Delta^{-2}\ln(G/\alpha))$.
- **Proof status: complete** (set $\epsilon=\Delta/4$ in Thm 9.17). Feeds `sec:complexity` cost table.

## Global checks
- **Every theorem has:** explicit assumptions, variable domains, precise statement, constants
  ($\pinf,\thresh,b,N,M,\epsilon,\alpha,\Delta$), a proof or clearly-labelled status, an
  interpretation, and stated limitations. PASS.
- **Overclaim scan:** no use of "sharp", "matching lower bound", "optimal", "tight", or "first"
  in any theorem statement. "To the best of our knowledge, within the verified literature" is used
  once for the environment-novelty claim (Intro), grounded in MASEC §4.7. See `claim_strength_audit.md`.
- **No upper-bound-as-achievability:** propagation upper bounds are not used to assert a matching
  attack; the collusion *separation* is a direct exact computation, not a contrapositive.
- **No misapplied classical theorem:** Hoeffding used with its bounded-i.i.d. assumptions verified;
  Kempe's greedy bound cited, not re-derived or misattributed; no VCG/Myerson/Cheeger/Gaussian-mechanism invoked.
