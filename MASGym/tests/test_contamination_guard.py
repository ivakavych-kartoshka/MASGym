"""Contamination guards on the two scripts that build paper-facing tables.

A failed backbone call is recorded as a benign decision with parse_failed set, so
a run whose credential died still reports a plausible compliance rate. Both the
table builder and the release builder therefore refuse to consume any cell that
carries parse failures. These tests drive the guards with a contaminated fixture
so the refusal is proven, not assumed.
"""
from __future__ import annotations

import json

import pytest

from experiments import make_defense_release, make_defense_table


def _write_run(root, parse_failures: int) -> None:
    cell = root / "star_a5"
    cell.mkdir(parents=True)
    (cell / "summary.json").write_text(
        json.dumps({
            "env": {"n_agents": 5, "topology": "star"},
            "scenarios": {
                "benign": {"episodes": 30, "decisions": 0},
                "single_attacker": {
                    "episodes": 30,
                    "decisions": 100,
                    "exfiltration_decisions": 0,
                    "asr_sys": 0.0,
                    "asr_action": 0.0,
                    "compliance_rate": 0.0,
                    "parse_failures": parse_failures,
                },
            },
        }),
        encoding="utf-8",
    )
    (cell / "decisions.jsonl").write_text(
        json.dumps({
            "episode": 1, "t": 0, "agent": 0, "attack": True,
            "defense": "delimiting", "action": "benign", "parse_failed": True,
            "parse_rule": "empty", "system_prompt": "s", "user_prompt": "u",
            "raw_model_output": "", "latency_s": 0.0, "approx_tokens": 0,
        }) + "\n",
        encoding="utf-8",
    )


def test_table_builder_rejects_parse_failures(tmp_path, monkeypatch) -> None:
    _write_run(tmp_path, parse_failures=4)
    monkeypatch.setattr(make_defense_table, "SOURCES", [("Fake", str(tmp_path))])
    with pytest.raises(SystemExit, match="parse failures"):
        make_defense_table.collect(30)


def test_table_builder_accepts_clean_cell(tmp_path, monkeypatch) -> None:
    _write_run(tmp_path, parse_failures=0)
    monkeypatch.setattr(make_defense_table, "SOURCES", [("Fake", str(tmp_path))])
    df = make_defense_table.collect(30)
    assert len(df) == 1
    assert int(df.iloc[0]["parse_failures"]) == 0


def test_release_builder_rejects_parse_failures(tmp_path, monkeypatch) -> None:
    _write_run(tmp_path, parse_failures=4)
    monkeypatch.setattr(make_defense_release, "SOURCES", [("Fake", str(tmp_path), True)])
    monkeypatch.setattr(make_defense_release, "_ROOT", tmp_path.parent)
    monkeypatch.setattr("sys.argv", ["make_defense_release.py"])
    with pytest.raises(SystemExit, match="parse failures"):
        make_defense_release.main()
