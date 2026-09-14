"""Aggregator + metric-axiom tests (Eq. 1/5, Thm 9.2, Prop 9.1, Remark 9.3)."""
from __future__ import annotations

import pytest

from masgym.methods.aggregators import min_agg, product_nrp, weighted_geometric
from masgym.theory.metric_axioms import check_axioms, reduces_to_asb


def test_product_equals_eq1() -> None:
    assert product_nrp(0.8, 0.25) == pytest.approx(0.6)
    for pna in (0.0, 0.5, 1.0):
        for asr in (0.0, 0.3, 1.0):
            assert product_nrp(pna, asr) == pytest.approx(pna * (1 - asr))


def test_product_satisfies_all_axioms() -> None:
    ax = check_axioms(product_nrp)
    assert all(ax.values())


def test_reduces_to_asb() -> None:
    assert reduces_to_asb() is True


def test_min_fails_homogeneity() -> None:
    ax = check_axioms(min_agg)
    assert ax["D1_bounded"] and ax["D2_consistency"] and ax["D3_monotone"]
    assert not ax["D4a_homog_u"]  # min is not homogeneous -> Thm 9.2 excludes it


def test_weighted_geometric_boundary() -> None:
    assert weighted_geometric(0.0, 0.2) == 0.0  # 0^w * . = 0 (axiom D2 boundary)
    assert weighted_geometric(0.5, 1.0) == 0.0  # sigma=0 -> 0


def test_invalid_inputs_raise() -> None:
    with pytest.raises(ValueError):
        product_nrp(1.2, 0.5)
    with pytest.raises(ValueError):
        product_nrp(0.5, -0.1)
