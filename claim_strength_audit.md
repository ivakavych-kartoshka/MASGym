# Claim-Strength Audit — MASGym

Every occurrence of a strong word ("first", "optimal", "sharp", "matching", "tight",
"state-of-the-art", "superior", "universal", "guarantee", "unique", "strict") was located and
adjudicated. Verdict for each: **justified**, **weakened**, or **removed**.

## "first"
- **"the first environment purpose-built for the security of multi-agent LLM systems"**
  (Introduction). **JUSTIFIED (guarded).** Prefixed with "to the best of our knowledge and within
  the verified literature," and grounded in MASEC (`schroederdewitt2025masec`, §4.7), which itself
  states no multi-agent security benchmark exists. Not an unqualified "first ever."
- "first-class caveat / first-class variable / first-class threat" (×4) — idiom, not a priority
  claim. **JUSTIFIED.**
- "First, \defname{} is not ASB applied to many agents" — enumeration marker. **JUSTIFIED.**

## "optimal"
- Single occurrence: "it is **not** a claim that the product is 'optimal' in any absolute sense"
  (Remark 9.3). This is an explicit **disavowal**. **JUSTIFIED.** No positive optimality claim exists.

## "sharp" / "sharply"
- "security in multi-agent systems is non-compositional … makes the point sharply" (Intro) —
  rhetorical, paraphrasing MASEC. **JUSTIFIED.**
- "the expected reach of a compromise depends **sharply** on topology" (Theory) — descriptive; the
  *following sentence* provides the **exact** expectations (Props 9.7–9.10) that differ by orders of
  magnitude, so "sharply" is accurate. **JUSTIFIED.** Not a formal "sharp threshold" claim. (Could be
  softened to "strongly"; left as accurate.)

## "matching"
- Single occurrence: "a payment … **matching** the itinerary" (worked example, App. B). Semantic use.
  **JUSTIFIED.** No "matching lower bound" / "matching impossibility" claim anywhere.

## "universal"
- All occurrences refer to the paper *Universal and Transferable Adversarial Attacks*
  (`zou2023universal`) and its "universal triggers." A **proper-noun / cited-method** reference, not
  a claim about \defname{}. **JUSTIFIED.**

## "unique"
- "$g(u,\sigma)=u\sigma$ is the **unique** such aggregator" and "the product is the unique aggregator
  **relative to** D2/D4" (Thm 9.2, Remark 9.3). **JUSTIFIED** — proved, and explicitly relativized to
  the stated axioms (alternatives named). Not "the unique reasonable metric."

## "strict" / "strictly"
- "**strict** collusion advantage," "the coordinated adversary **strictly** dominates" (Thm 9.13).
  **JUSTIFIED** — the gap $\pinf(1-\pinf)(N-1)(N-2)/N$ is proved $>0$ for $\pinf\in(0,1)$, $N\ge3$
  (full computation in `appendix/proofs.tex`).

## "guarantee"
- "concentration **guarantees**" (Thm 9.17) — proved. **JUSTIFIED.**
- "an analogous **guarantee**" (McDiarmid alternative) — attributed to a cited inequality. **JUSTIFIED.**
- "an assumption, not a **guarantee**" (Remark 9.6) and "not a safety **guarantee**" (Ethics) —
  **disavowals.** **JUSTIFIED.**

## Words checked and ABSENT
- "tight", "state-of-the-art", "superior", "no efficiency loss", "novel" (as a bare adjective),
  "matching lower bound", "matching impossibility": **0 occurrences.**

## Empirical-claim guarding
- The headline finding (single-agent defenses degrade under collusion/orchestrator compromise) is
  marked **`(hypothesis)`** at every occurrence (Abstract, Intro contribution 5, RQ3, Limitations,
  Conclusion), and the paper states it reframes as a negative result if it does not replicate.
- All result tables/plots carry "Placeholder / expected trend only; replace with actual experimental
  results before submission" (Tables 2–5; Figure 6 caption). No measured number is asserted.

## Verdict
No claim was found that required weakening or removal beyond the guards already in the text. The
single novelty ("first … multi-agent LLM security environment") is appropriately hedged and
citation-grounded. One optional softening noted ("depends sharply" → "strongly").
