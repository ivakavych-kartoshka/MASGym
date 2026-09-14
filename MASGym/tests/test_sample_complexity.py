"""Sample-complexity + confidence-interval tests (Theorem 9.17, Corollary 9.18)."""
from __future__ import annotations

import math

import pytest

from masgym.metrics.confidence_intervals import hoeffding_ci, hoeffding_halfwidth, wilson_ci
from masgym.theory.sample_complexity import (
    hoeffding_min_samples,
    nrp_confidence_delta,
    sweep_budget,
)


def test_hoeffding_min_samples_formula() -> None:
    m = hoeffding_min_samples(0.05, 0.05)
    assert m == math.ceil(math.log(2 / 0.05) / (2 * 0.05 ** 2)) == 738


def test_hoeffding_halfwidth_consistency() -> None:
    m = hoeffding_min_samples(0.05, 0.05)
    assert hoeffding_halfwidth(m, 0.05) <= 0.05 + 1e-9


def test_nrp_delta_bound() -> None:
    assert nrp_confidence_delta(738, 0.05) == pytest.approx(4 * math.exp(-2 * 738 * 0.05 ** 2))


def test_product_triangle_inequality() -> None:
    # |u_hat*s_hat - u*s| <= |u_hat-u| + |s_hat-s|  (proof of Thm 9.17b)
    import numpy as np

    rng = np.random.default_rng(0)
    for _ in range(1000):
        u, s, uh, sh = rng.random(4)
        assert abs(uh * sh - u * s) <= abs(uh - u) + abs(sh - s) + 1e-12


def test_sweep_budget() -> None:
    assert sweep_budget(50, 0.1, 0.05) == 6081


def test_cis_valid() -> None:
    lo, hi = hoeffding_ci(0.4, 738, 0.05)
    assert 0.0 <= lo <= 0.4 <= hi <= 1.0
    wlo, whi = wilson_ci(300, 738, 0.05)
    assert 0.0 <= wlo <= whi <= 1.0
