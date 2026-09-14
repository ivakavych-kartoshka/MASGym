# Implementation Gaps

Honest inventory of everything that is NOT fully runnable locally and why. Cross-referenced by
`audits/paper_to_code_traceability.csv` (statuses `adapter_stub_waiting_for_external_dependency`,
`not_implemented_requires_manual_data`, `intentionally_out_of_scope`).

## External dependencies (adapter stubs — require EC2 provisioning)
| Gap | Where | What is needed |
|---|---|---|
| Real LLM backbones (Llama-3, Qwen2.5, Mistral, GPT-4o, Claude-3.5) | `data/adapters.py::LLMBackboneAdapter` | model weights / API keys + a `generate_fn` |
| ToolEmu emulator (real, κ≈0.48) | `env/emulation.py::ToolEmuAdapter` | ToolEmu install / LLM backend + `emulate_fn` |
| Real LLM judge (RQ2) | `env/judge.py::LLMJudgeAdapter` | a model + `judge_fn` |
| ASB single-agent baseline | `baselines/external_wrappers.py::ASBSingleAgentAdapter` | github.com/agiresearch/ASB setup |
| AgentDojo baseline | `baselines/external_wrappers.py::AgentDojoAdapter` | AgentDojo harness |
| Real guardrails (Llama Guard, NeMo, TrustAgent) | `RealGuardrailAdapter` | external models/toolkits |
| Reference MA defenses (AutoDefense, G-Safeguard) | `MADefenseAdapter` | external repos |

Each raises `NotImplementedError` with a pointer until implemented on EC2. None is faked.

## Manual-data dependencies
| Gap | Where | What is needed |
|---|---|---|
| Benign task pools (AgentBench, GAIA, WebArena, SWE-bench, MMLU, GSM8K) | `data/adapters.py::BenchmarkTaskAdapter` | download + place under `data.root`; some need registration/license (see `docs/data_format.md`, `docs/ec2_experiment_guide.md`) |

## Intentionally out of scope
- **Paper-level numerical results** (Tables 2–6, Figure 6) are *placeholders/`(hypothesis)`* in the
  paper; this repo produces only clearly-labelled synthetic demo numbers. Reproducing real results
  requires wiring the adapters above and running on EC2.
- **ToolEmu κ≈0.48** is a documented validity caveat, not a computed quantity.
- **Conformal-prediction components** from the generic task template do not apply (MASGym is a
  benchmark environment, not a conformal method).

## Modelling simplifications (documented, not silent)
- **Synthetic agent model**: real agent rollouts are replaced by the paper's compromise-propagation
  dynamics (Assumption A4) + the k-forced/transversal success rule (Prop 9.15). Faithful to the
  paper's definitions; not a measurement. Labelled synthetic everywhere.
- **Defense effect-models** (`SYNTHETIC_EFFECT_MODEL`): reduce effective `p` uniformly with fixed
  detect/recover; chosen parameters, not measured efficacies. Deliberately encode no
  orchestrator/topology-specific effect, so the pipeline cannot manufacture the degradation
  hypothesis.
- **Sybils**: modelled as extra adversarial seed identities (influence proxy).
- **Mesh fixation** (`CPR→1`): kept remark-level in the paper; only the exact one-round bound is coded.

## No inconsistencies detected
The math audit (`audits/math_to_code_audit.md`) found no conflict between the paper's definitions,
theorems, and algorithms for the implemented objects; the numerical tests confirm code matches the
closed forms. If a future discrepancy appears it must be logged here and flagged
`paper_inconsistency_detected` in the traceability CSV.
