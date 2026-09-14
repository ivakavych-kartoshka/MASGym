# Reproducibility

## Seeds
All stochasticity flows through `masgym.utils.seeding.SeededRNG` (a wrapper around
`numpy.random.default_rng`). The same seed yields identical episodes, metrics, and CoRB
trajectories. `masgym.utils.seeding.set_global_seed` additionally seeds Python/NumPy globals and
`PYTHONHASHSEED` for incidental determinism. Tests `tests/test_reproducibility.py` assert this.

## Configs
Experiments are driven by YAML configs (`configs/*.yaml`). `masgym.config` parses them into typed
`EnvConfig`/`AdversaryConfig` and expands adversary sweep grids. The config is hashed
(`config_hash`) and stored in every result's provenance header.

## Provenance
`masgym.utils.io.run_metadata(config, seed, synthetic)` stamps each output file with:
`masgym_version`, `seed`, `config_hash`, `python`, `timestamp_utc`, and `synthetic` (+ a
`provenance_note`). Synthetic runs are flagged `synthetic: true` with the note
"synthetic smoke-test output, not a paper result".

## Environment
- Python >= 3.10 (3.11+ recommended). CPU-only. No GPU, no network needed for the synthetic
  pipeline or tests.
- Runtime deps: numpy, pandas, matplotlib, pyyaml (`requirements.txt`). Dev: pytest, ruff, mypy.
- Deterministic given `(config, seed)`; number of episodes `M` should be chosen with
  `masgym.theory.sample_complexity.hoeffding_min_samples(eps, alpha)` (Theorem 9.17).

## Reproducing the synthetic demo
```bash
pip install -r requirements.txt
export PYTHONPATH=src:.            # or: pip install -e .
python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml --out outputs/synthetic_demo
```
Outputs (CSV/JSON/PNG) land in `outputs/synthetic_demo/` and are labelled synthetic.

## Reproducing the theory verification
```bash
python -m masgym.cli theory --out outputs/theory --trials 8000
```
This compares Monte-Carlo compromise reach against the closed forms (Props 9.7-9.11, Thm 9.13),
checks the metric axioms (Thm 9.2), and verifies Hoeffding-CI coverage (Thm 9.17). It is a
self-consistency check, not a benchmark result.

## Tests
```bash
pytest -q
```
All tests run on synthetic data with fixed seeds; none require external datasets or network.
