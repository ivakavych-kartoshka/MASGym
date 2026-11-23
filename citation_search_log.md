# Citation Search Log — MASGym

## Objective
Assemble a verified bibliography (~50–80 refs) for a benchmark/environment paper on
multi-agent LLM security, anchored to `idea.pdf` (MASGym). Correctness and topical relevance
prioritized over count.

## Scholarly databases / sources used
- arXiv official abstract pages (primary metadata + abstract verification).
- Official proceedings pages: NeurIPS, ICML (PMLR), ICLR, ACL Anthology, USENIX.
- DOI / Crossref and SpringerLink (Sybil/IPTPS, classical theory).
- DBLP / Semantic Scholar as discovery only (never as sole verification).
- Project corpus: `00_Phase1_Knowledge_Extraction.md` (per-paper verified extraction of the
  four seed papers), and the vetted sibling pools `Idea_11_AdversarialMAST/`,
  `Idea_10_CovertLink/`, `Idea_14_RobustComm/` `references_verified.bib` + `citation_claim_map.csv`
  (same rigorous verification process).

## Seed references (from idea.pdf) and resolved metadata
| Idea PDF mention | Resolved | Venue | Verified via |
|---|---|---|---|
| ToolEmu (arXiv:2309.15817, ICLR 2024) | Ruan et al., *Identifying the Risks of LM Agents with an LM-Emulated Sandbox* | ICLR 2024 | arxiv.org/abs/2309.15817 (fetched) |
| ASB (arXiv:2410.02644, ICLR 2025) | H. Zhang et al., *Agent Security Bench (ASB)* | ICLR 2025 (Comments: "Accepted by ICLR 2025") | arxiv.org/abs/2410.02644 (fetched) |
| AgentDojo (arXiv:2406.13352) | Debenedetti et al., *AgentDojo* | NeurIPS 2024 Datasets & Benchmarks | corpus Phase-1 + NeurIPS proceedings |
| MASEC (arXiv:2505.02077, §4.7) | Schroeder de Witt et al., *Open Challenges in Multi-Agent Security* | arXiv preprint | arxiv.org/abs/2505.02077 + corpus |

No "Anonymous" seed references were present; all four seed papers carry explicit arXiv IDs,
which were resolved to full author lists and venues above.

## Search queries (representative)
- "Agent Security Bench ASB LLM agents ICLR 2025"; "AgentDojo prompt injection deterministic security check NeurIPS 2024"; "ToolEmu LM-emulated sandbox ICLR 2024"; "Open Challenges Multi-Agent Security de Witt".
- "multi-agent LLM prompt injection propagation" (Prompt Infection, CORBA, Agent Smith, Agent-in-the-Middle).
- "multi-agent LLM safety benchmark" (PsySafe, NetSafe, AgentHarm, HarmBench).
- "memory poisoning LLM agent" (AgentPoison); "LLM agent backdoor" (Watch Out, BadAgent).
- "multi-agent LLM defense" (AutoDefense, G-Safeguard); "LLM guardrails" (Llama Guard, NeMo Guardrails, TrustAgent).
- "Sybil attack" (Douceur IPTPS 2002); "Byzantine tolerant gradient descent Krum"; "OpenAI Gym", "PettingZoo", "Melting Pot"; "red teaming language models with language models".
- Model cards: "Llama 3 herd", "Qwen2.5 technical report", "Mistral 7B", "GPT-4o system card".
- Foundational theory: Hoeffding, McDiarmid, Boucheron concentration, influence maximization (Kempe), global cascades (Watts), bootstrap percolation (Chalupa), Byzantine generals (Lamport/Pease), FDR (Benjamini–Hochberg), Cohen/Fleiss kappa.

## Inclusion criteria
1. Directly supports a specific manuscript sentence (positioning, primitive, baseline, model, or theory result).
2. Metadata verified against a primary source (arXiv abs page / DOI / official proceedings).
3. On the locked topic (multi-agent LLM security, its single-agent predecessors, the frameworks/attacks/defenses it instantiates, or the theory it invokes).

## Exclusion criteria
1. Cannot verify existence/metadata against a primary source.
2. Only keyword-related, not claim-supporting.
3. Off-topic (e.g., unrelated FL/DP/mechanism-design papers) — excluded to avoid topic drift.
4. Duplicate/superseded versions when a better verified version exists.

## Major literature clusters (final bib section headers)
1. Core seed references (4): ToolEmu, ASB, AgentDojo, MASEC.
2. Closest competing methods (18): MAST, InjecAgent, AgentHarm, AgentPoison, Prompt Infection, AiTM, CORBA, Agent Smith, PsySafe, Evil Geniuses, NetSafe, AI Worm, Watch Out, G-Safeguard, AutoDefense, HarmBench, DecodingTrust, Multi-Agent Risks.
3. Foundational theory (16): concentration (Hoeffding, McDiarmid, Boucheron), testing (Neyman–Pearson, Lehmann), causal (Rubin), cascades/percolation (Granovetter, Kempe, Watts, Chalupa), BFT (Lamport, Pease, Krum), FDR (Benjamini–Hochberg), agreement (Cohen, Fleiss).
4. System/model background (20): AutoGen, CAMEL, MetaGPT, ChatDev, AgentVerse, Debate, ChatEval, MoA, DyLAN, OpenHands, Magentic-One, ReAct, Reflexion, Generative Agents, Toolformer, survey, Gym, PettingZoo, Melting Pot, Sybil.
5. Security background / PI primitives (13): Greshake, Houyi, Ignore-Previous, Formalizing-PI, GCG, AutoDAN, Jailbroken, TrustAgent, Personal-LLM-Agents survey, Emerged-Security survey, red-teaming-LMs, Llama Guard, NeMo.
6. Experimental baselines/datasets/models (12): AgentBench, SWE-bench, GAIA, WebArena, MT-Bench judge, fair-evaluators, MMLU, GSM8K, Llama-3, Qwen2.5, Mistral, GPT-4o.

## Rejected candidate references
See `references_rejected.md`. No fabricated entries were included; any reference that could not
be verified was excluded rather than guessed.

## Final reference count
83 verified entries (all cited in the manuscript; see `citation_consistency_report.md`).
This is slightly above the 50–80 guideline; all 83 support specific sentences and none was added
for count. Verification levels: 4 full-text; ~59 abstract-only (arXiv abs page); ~20 metadata-only
(DOI/publisher/proceedings). See `citation_claim_map.csv` for per-entry detail.
