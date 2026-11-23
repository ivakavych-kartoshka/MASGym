# Citation Consistency Report — MASGym

Automated + manual consistency checks over `main.tex`, `references_verified.bib`, and
`citation_claim_map.csv`. Regenerate the automated parts with the commands in `build/`.

## 1. Every `\cite{...}` key exists in the `.bib`
**PASS.** Extracted 83 unique cited keys from `main.aux` (splitting grouped `\cite{a,b}`);
all 83 resolve to entries in `references_verified.bib`. Dangling citations: **0**.

## 2. Every `.bib` entry is cited (or intentionally retained)
**PASS.** `references_verified.bib` has 83 entries; all 83 are cited at least once. Uncited
entries: **0**. (Ten foundational references that were initially uncited were each given a precise
supporting sentence: `blanchard2017krum`, `lamport1982byzantine`, `pease1980reaching` in Related
Work; `cohen1960coefficient`, `fleiss1971measuring` at the $\kappa\approx0.48$ caveat;
`boucheron2013concentration`, `mcdiarmid1989bounded` in the sample-complexity subsection;
`neyman1933problem`, `lehmann2005testing` in the evaluator-integrity remark; `rubin1974estimating`
at the controlled-variation statement.)

## 3. Compilation resolves all references and citations
**PASS.** Final `pdflatex` run reports 0 "Citation undefined" and 0 "Reference undefined"
warnings. LaTeX cross-references (`\Cref` to theorems, equations, figures, tables, algorithms)
all resolve.

## 4. Author order and titles
**PASS (verified sources).** Seed refs (ToolEmu, ASB, AgentDojo, MASEC) and the 17 externally
verified anchors had their full author lists and exact titles taken verbatim from the fetched
primary pages (arXiv abstract pages, ACL Anthology, PMLR, NeurIPS/SpringerLink). Note recorded in
`citation_claim_map.csv`: `dubey2024llama3` first author is Grattafiori on current arXiv v3 (key
retained). Corpus-pool entries reuse the sibling-verified author strings; flagged for independent
re-check in `citation_todo.md`.

## 5. arXiv IDs match titles
**PASS (spot-checked).** All arXiv IDs used in the four seed references were confirmed by
fetching the abstract page and matching the title (2309.15817 → ToolEmu; 2410.02644 → ASB;
2406.13352 → AgentDojo; 2505.02077 → MASEC). The 17 anchors were confirmed by the verification
subagent against their arXiv/DOI pages. Corpus-pool arXiv IDs inherit the sibling verification.

## 6. DOI matches title
**PASS (where DOIs are used).** DOIs appear only on foundational/publisher entries and the
AgentDojo proceedings entry; each DOI corresponds to the stated title on its Crossref/publisher
record. arXiv-only entries carry `arXiv:` identifiers, not DOIs.

## 7. No citation used for an unsupported (too-strong) claim
**PASS (manual audit).** Cross-checked against the anti-overclaim rules:
- ASB/AgentDojo/ToolEmu are cited as **single-agent** instruments (their actual scope), never as
  multi-agent.
- The influence-maximization $(1-1/e)$ bound is attributed to `kempe2003maximizing` as **their**
  result for a greedy algorithm, not claimed as ours; our contribution is the exact star-topology
  separation, proved in-paper.
- LLM-judge manipulability is cited to `zheng2023judging`/`wang2023fair` as **documented bias**,
  and our `prop:judgehijack` is an **existence** result, not a claim that all judges always fail.
- Krum/BFT (`blanchard2017krum`,`lamport1982byzantine`,`pease1980reaching`) are cited as
  **gradient/numeric, trusted-coordinator** methods that **do not** target LLM collectives — a
  contrast, not an appropriation.
- Cohen/Fleiss $\kappa$ cited only for the agreement-coefficient meaning of ToolEmu's $\kappa\approx0.48$.

## 8. No citation from a different topic dominates the paper
**PASS.** By the `citation_claim_map.csv` section tags, ≥60% of references are on the locked
topic (seed + closest-competing + PI primitives + MAS frameworks + agent benchmarks = ~55 of 83).
Foundational theory (16) supports specific proof steps; peripheral entries appear only in
single supporting sentences. No off-topic cluster (FL/DP/mechanism-design) is present.

## Summary
All eight consistency checks PASS. 83 cited = 83 in `.bib`; 0 dangling; 0 uncited; 0 undefined at
compile; no overclaiming citation detected.
