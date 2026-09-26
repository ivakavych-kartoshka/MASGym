"""Tests for the defense release bundle builder.

The decision log does not record which scenario produced a record, so
assign_scenarios recovers the mapping from the order scenarios were appended
in. A wrong mapping would silently attribute exfiltration to the wrong
adversary, so the checks below pin down both the happy path and the failure
modes that must abort rather than guess.
"""
from __future__ import annotations

import pytest

from experiments.make_defense_release import EXFIL_ACTION, assign_scenarios


def _rec(episode: int, action: str = "benign") -> dict:
    return {"episode": episode, "action": action}


def _metrics(decisions: int, exfil: int) -> dict:
    return {"decisions": decisions, "exfiltration_decisions": exfil}


def test_assigns_scenarios_in_append_order() -> None:
    records = [
        _rec(0, EXFIL_ACTION), _rec(1, EXFIL_ACTION),
        _rec(2),
        _rec(3, EXFIL_ACTION),
    ]
    scen = [("single_attacker", _metrics(2, 2)), ("colluding", _metrics(1, 0)),
            ("compromised_orchestrator", _metrics(1, 1))]
    out = assign_scenarios(records, scen, "test")
    assert [r["_scenario"] for r in out] == [
        "single_attacker", "single_attacker",
        "colluding",
        "compromised_orchestrator",
    ]


def test_benign_records_are_absent_by_construction() -> None:
    records = [_rec(0, EXFIL_ACTION)]
    scen = [("single_attacker", _metrics(1, 1))]
    out = assign_scenarios(records, scen, "test")
    assert out[0]["_scenario"] == "single_attacker"


def test_aborts_when_exfiltration_count_disagrees() -> None:
    records = [_rec(0, EXFIL_ACTION), _rec(1)]
    scen = [("single_attacker", _metrics(2, 2))]
    with pytest.raises(SystemExit, match="exfiltration count"):
        assign_scenarios(records, scen, "test")


def test_aborts_when_record_count_disagrees() -> None:
    records = [_rec(0, EXFIL_ACTION)]
    scen = [("single_attacker", _metrics(2, 2))]
    with pytest.raises(SystemExit, match="expected 2 decisions"):
        assign_scenarios(records, scen, "test")


def test_aborts_on_leftover_records() -> None:
    records = [_rec(0, EXFIL_ACTION), _rec(1, EXFIL_ACTION)]
    scen = [("single_attacker", _metrics(1, 1))]
    with pytest.raises(SystemExit, match="left over"):
        assign_scenarios(records, scen, "test")
