# Rejected / Excluded Candidate References — MASGym

No fabricated references were included anywhere. The policy was: if a candidate could not be
verified against a primary source, or did not support a specific manuscript sentence on the
locked topic, it was excluded rather than guessed. This file records the categories of
exclusion and representative decisions.

## Excluded to avoid topic drift (off the locked topic)
The locked topic is a **benchmark/environment for multi-agent LLM security**. The following
neighbouring areas were deliberately kept out of the core bibliography except where a single
sentence needed them, to prevent the paper from drifting (per `topic_signature.json`
`forbidden_topic_drifts`):
- Over-the-air / federated-learning aggregation papers — not this paper's topic; excluded.
- Differential-privacy mechanism-design papers (Gaussian mechanism, privacy accounting) — excluded; MASGym is not a DP paper.
- Auction / VCG / incentive-compatibility (mechanism design) papers — excluded; MASGym has no incentive mechanism.
- ZK-proof / SMPC / TEE construction papers — excluded; not a cryptographic-construction paper.
- MARL reward-shaping papers — excluded; MASGym is not a MARL-training paper (Gym/PettingZoo/Melting Pot are cited only for the *environment* lineage).

## Excluded as duplicate / superseded versions
- Where a paper had an arXiv preprint and a published proceedings version, only the most
  appropriate verified version was kept (e.g., ASB kept as ICLR 2025; AgentDojo kept as
  NeurIPS 2024 D&B; ToolEmu kept as ICLR 2024) with the arXiv id retained in a `note`. No
  duplicate entries were created for the same work.

## Excluded as keyword-only (did not support a specific claim)
- Generic "LLM survey" papers not tied to agent security were not added; only the agent- and
  MAS-security surveys that support specific positioning sentences were kept
  (`he2025emerged`, `li2024personalllmagents`, `guo2024survey`).

## Not rejected but flagged for re-verification level
- No candidate was included at a verification level below "abstract-only verified." Entries
  inherited from the vetted sibling corpus pool were confirmed present in the sibling
  `citation_claim_map.csv` at "abstract-only verified" (arXiv abstract page) and are labelled
  accordingly in `citation_claim_map.csv`; they are additionally listed in
  `TODO_before_submission.md` for an independent full-text re-check before submission.

## Predatory / unreliable venues
- None included. All venues are arXiv, recognized ML/security conferences (NeurIPS, ICML, ICLR,
  ACL/EMNLP, USENIX, ICCV), or established journals/publishers (ACM, Springer, Wiley, IOP,
  Taylor & Francis, Royal Society).

## Summary
0 fabricated references. 0 references included that could not be verified against a primary
source. All 83 final references are cited and support specific sentences.
