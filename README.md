# MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems

Reference implementation, paper sources, and rebuttal studies for **MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems with Parameterized Collusion, Orchestrator Compromise, and System-Level Metrics** (AAMAS 2027 submission).

## Repository Layout

- [`MASGym/`](MASGym/) — Python package (`src/masgym/`), experiment runners (`experiments/`), CLI & demo scripts (`scripts/`), configs (`configs/`), documentation (`docs/`), and unit test suite (`tests/`).
- [`aamas2027/`](aamas2027/) — LaTeX sources and compiled PDFs for the main paper (`main.pdf`), technical supplement (`main_supplement.pdf`), and author rebuttal (`rebuttal_EN.md`).
- [`results/rebuttal/`](results/rebuttal/) — Reproducible CSV/JSON/Markdown summaries from the rebuttal studies (availability-rule ablation, controlled collusion, propagation sensitivity, cluster-aware CIs, CoRB Pareto analysis, and matched undefended/defended real-LLM sweeps for `Llama-3.2-1B-Instruct` and `Ministral-3-8B-Instruct`).

## Quick Start

```bash
cd MASGym
pip install -r requirements.txt
pytest -q

# Run synthetic demo
python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml --out outputs/synthetic_demo

# Reproduce all 4 CPU rebuttal studies (seed-locked)
python experiments/run_rebuttal_studies.py --m 738 --seed 0
```

See [`MASGym/README.md`](MASGym/README.md) for full CLI usage, real-LLM sweep options, and reproducibility instructions.
