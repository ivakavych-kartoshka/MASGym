# MASGym developer tasks. Uses the src/ layout via PYTHONPATH so no install is required.
PYTHONPATH := src:.
export PYTHONPATH

.PHONY: help install test demo theory lint typecheck clean

help:
	@echo "make install    - pip install -e .[dev]"
	@echo "make test       - run the pytest suite (synthetic only)"
	@echo "make demo       - run the synthetic smoke-test demo -> outputs/synthetic_demo/"
	@echo "make theory     - run closed-form theory verification -> outputs/theory/"
	@echo "make lint       - ruff check (if installed)"
	@echo "make typecheck  - mypy src (if installed)"
	@echo "make clean      - remove outputs/ artifacts and caches"

install:
	pip install -e .[dev]

test:
	pytest -q

demo:
	python scripts/run_synthetic_demo.py --config configs/synthetic_demo.yaml --out outputs/synthetic_demo

theory:
	python -m masgym.cli theory --out outputs/theory --trials 8000

lint:
	ruff check . || echo "ruff not installed; skipping"

typecheck:
	mypy src || echo "mypy not installed; skipping"

clean:
	rm -rf outputs/synthetic_demo outputs/theory outputs/sweep outputs/ablation outputs/corb
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
