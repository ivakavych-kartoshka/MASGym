"""CLI smoke tests + result-integrity checks (runs only on synthetic data)."""
from __future__ import annotations

import json
from pathlib import Path

from masgym.cli import main

_ROOT = Path(__file__).resolve().parents[1]
_DEMO_CFG = str(_ROOT / "configs" / "synthetic_demo.yaml")


def test_cli_version() -> None:
    assert main(["version"]) == 0


def test_cli_theory(tmp_path: Path) -> None:
    assert main(["theory", "--out", str(tmp_path), "--trials", "400", "--seed", "0"]) == 0
    data = json.loads((tmp_path / "theory_check.json").read_text())
    # product aggregator satisfies all axioms; alternatives do not
    assert all(data["axioms"]["product"].values())
    assert data["axioms"]["product_reduces_to_asb"] is True


def test_cli_sweep_provenance_is_synthetic(tmp_path: Path) -> None:
    assert main(["sweep", "--config", _DEMO_CFG, "--out", str(tmp_path)]) == 0
    meta = json.loads((tmp_path / "sweep_metadata.json").read_text())
    # every generated result file must be flagged synthetic (no fake paper results)
    assert meta["synthetic"] is True
    assert "not a paper result" in meta["provenance_note"]


def test_cli_corb(tmp_path: Path) -> None:
    assert main(["corb", "--config", _DEMO_CFG, "--out", str(tmp_path)]) == 0
    assert (tmp_path / "corb_trajectory.csv").exists()
