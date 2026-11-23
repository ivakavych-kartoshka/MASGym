# TODO Before Submission — MASGym

Ordered by importance. Items are grouped by category as required.

## A. Placeholder results to replace with measured data (BLOCKING)
- [ ] Run the full evaluation (RQ1–RQ6) and replace **all** placeholder cells:
  - Table 2 (`tab:degradation`) — headline single-agent → MA degradation study.
  - Table 3 (`tab:topology`) — $\CPR$/$\ASRs$ by topology.
  - Table 4 (`tab:sybil`), Table 5 (`tab:adaptive`), Table 6 (`tab:cost`) in App. B.
  - Figure 6 (`fig:results`) — replace conceptual curves with measured data (remove "conceptual"
    labels only once real data is in).
- [ ] Convert every `(hypothesis)` tag to a measured result **or** reframe as a negative result if
  defenses do not degrade (Abstract, Intro contribution 5, RQ3, Limitations, Conclusion).
- [ ] Build the real-tool subset needed for the emulated-vs-real-tools fidelity ablation.

## B. Unverified / upgrade-needed citations
- [ ] Independently re-fetch and re-verify the ~59 corpus-pool "abstract-only verified" references
  (inherited from the sibling `Idea_11` claim map) against their arXiv abstract pages, so this folder
  is self-contained. Priority: closest-competing attacks/defenses (see `citation_todo.md`).
- [ ] Confirm AgentDojo NeurIPS 2024 D&B DOI `10.52202/079017-2636` on the official proceedings page.
- [ ] Confirm final published venues for currently-arXiv-only entries at camera-ready.
- [ ] Confirm `he2025emerged` ACM CSUR DOI `10.1145/3773080` + pages.
- [ ] Fix the exact author-of-record convention for model cards (`dubey2024llama3` Grattafiori-first;
  `qwen2025qwen25`, `jiang2023mistral7b`, `openai2024gpt4o` org vs. lead author) per journal style.

## C. Incomplete proofs / theory
- [ ] None are incomplete. Thm 9.13 is proved in full in App. A (body labels it "Proof sketch");
  optionally relabel the body pointer to "(full proof in Appendix A)". 
- [ ] Optional: state the $s>1$ collusion generalization as its own corollary if space allows
  (currently a cited remark using Kempe's greedy bound).

## D. Missing experiments / validation of assumptions
- [ ] Validate the propagation model (Assumption 4): measure whether observed compromise dynamics
  resemble independent-cascade/threshold, and report the gap (this is what `\CPR` is for).
- [ ] Validate Assumption 2 (i.i.d. episodes) empirically or bound the dependence.
- [ ] Fix and report the concrete $M, R, G, H, \epsilon, \alpha$ used, and the actual reachable region
  of the parameter space.

## E. Author metadata to confirm
- [ ] Confirm author list, affiliations, corresponding-author email, ORCID, and acknowledgements/
  funding. (Current front matter is a single-author placeholder.)
- [ ] Confirm the exact Claude-3.5 variant used as an agent backbone (and add a citation/system card
  once fixed).

## F. Journal-specific formatting
- [ ] Replace the local `elsarticle.cls` **compatibility shim** with the official Elsevier class
  (`tlmgr install elsarticle` / `texlive-publishers`); `main.tex` compiles unchanged. Delete the shim.
- [ ] Switch `\bibliographystyle{plainnat}` to `elsarticle-num` (ships with the official class) or the
  target journal's required style; regenerate `.bbl`.
- [ ] Choose the target venue and reformat: NeurIPS D&B / ICLR (primary), or Computers & Security /
  IEEE TDSC / TIFS if journal. Adjust page limits, abstract length, and highlights accordingly.
- [ ] Provide the artifact/data-availability statement and the reproducibility appendix release URL.

## G. Unresolved LaTeX warnings
- [ ] 9 overfull `\hbox`es (worst ≈46 pt), mostly long bib URLs/titles and a couple of wide lines;
  tidy with `\sloppy`/rewrapping or `\url` breaking before camera-ready.
- [ ] Benign font warning `T1/lmr/bx/sc undefined` (bold small-caps substitution); harmless, but a
  submission font package (e.g., avoiding bold `\textsc`) removes it.

## H. Figure readability items
- [ ] All six figures PASS the audit. Optional polish: rename the emulator macro to remove the
  cosmetic $\mathcal{E}$ overlap with graph edges (see `notation_consistency_check.md`); optionally
  soften "depends sharply" → "strongly" (see `claim_strength_audit.md`).
- [ ] Regenerate high-DPI figure exports (or standalone PDFs) if the venue requires vector figures
  separate from the main file.

## I. Assumptions needing validation before claims harden
- [ ] A1 (trusted harness/checker) and predicate correctness — add a predicate-review procedure and
  report inter-author agreement on predicate specifications.
- [ ] A4 (propagation model realism) — as in D above.

## Status summary
Compiles (41 pp, 0 undefined refs). Theory complete. Figures pass. Citations verified (with the
re-verification upgrade in B). **The one blocking item for a real submission is Section A: run the
experiments and replace placeholders.**
