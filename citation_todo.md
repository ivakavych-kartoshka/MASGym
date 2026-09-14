# Citation TODO — MASGym

Claims still needing a citation, or citations needing an upgrade in verification level, before
submission. There are **no** `\textcolor{red}{[Citation needed]}` markers left in the
manuscript body; the items below are quality upgrades, not gaps.

## Claims that are intentionally self-supported (no external citation needed)
- All theorem/proposition/corollary statements in `sections/theory.tex` and `appendix/proofs.tex`
  are proved in-paper under stated assumptions; external results are cited where invoked
  (Hoeffding `hoeffding1963probability`, influence-maximization greedy bound `kempe2003maximizing`,
  FDR `benjamini1995controlling`). No theorem relies on an unavailable "Idea N" result, so no
  `% TODO: import/restate` placeholder was required.
- `NRP_sys = PNA_sys(1-ASR_sys)` is a contribution of this paper generalizing ASB's metric
  (`zhang2025asb`); the generalization is justified by Theorem (axiomatic characterization),
  not asserted, so no external citation is claimed for it.

## Verification-level upgrades to perform before submission
1. Re-verify the ~59 "abstract-only verified" corpus-pool references against their arXiv
   abstract pages independently in this project (they are currently inherited from the vetted
   sibling `Idea_11` claim map; re-fetch to make this folder self-contained). Priority order:
   the closest-competing attacks/defenses (`lee2024promptinfection`, `zhou2025corba`,
   `gu2024agentsmith`, `he2025redteaming`, `yu2024netsafe`, `zhang2024psysafe`, `cohen2024aiworm`,
   `yang2024watchout`, `yu2025gsafeguard`), then the frameworks and PI primitives.
2. Confirm the AgentDojo NeurIPS 2024 D&B DOI `10.52202/079017-2636` on the official proceedings
   page (currently from proceedings-page fetch; keep arXiv:2406.13352 as backup identifier).
3. Confirm final published venues (if any) for currently-arXiv-only entries before camera-ready:
   `lee2024promptinfection`, `zhou2025corba`, `yu2024netsafe`, `yu2025gsafeguard`,
   `zeng2024autodefense`, `cohen2024aiworm`, `tian2023evilgeniuses`, `fourney2024magenticone`,
   `wang2024mixture`.
4. `he2025emerged` (ACM CSUR) — confirm the assigned DOI `10.1145/3773080` and page range on the
   ACM DL landing page at camera-ready.
5. Model cards (`dubey2024llama3`, `qwen2025qwen25`, `jiang2023mistral7b`, `openai2024gpt4o`) —
   confirm author-of-record convention (org vs. lead author) per the target journal's style.

## No missing-citation claims
Every substantive empirical or prior-work claim in the manuscript is either (a) cited to a
verified reference, or (b) explicitly marked `(hypothesis)` / "placeholder" as an unproduced
result. There are no unsupported factual claims awaiting a citation.
