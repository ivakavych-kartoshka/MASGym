"""Numerical checks of the metric axioms (paper Theorem 9.2, Prop 9.1, Remark 9.3).

``check_axioms`` verifies which of the axioms D1 (bounded), D2 (consistency), D3 (monotone),
D4a/D4b (homogeneity) an aggregator satisfies over a grid. The product aggregator satisfies
all; ``min`` and the weighted geometric mean satisfy D1-D3 but not D4 -- which is exactly why
Theorem 9.2 singles out the product *relative to* D2/D4 (Remark 9.3).
"""
from __future__ import annotations

from typing import Callable

import numpy as np

Aggregator = Callable[[float, float], float]  # (pna, asr) -> nrp

_TOL = 1e-9


def check_axioms(agg: Aggregator, n_grid: int = 11) -> dict[str, bool]:
    """Return a dict of axiom -> pass/fail for aggregator ``agg`` (pna, asr) -> value."""
    us = np.linspace(0.0, 1.0, n_grid)
    asrs = np.linspace(0.0, 1.0, n_grid)

    d1 = True  # bounded in [0,1]
    d2 = True  # g(u,1)=u [asr=0] and g(0,sigma)=0 [pna=0]
    d3 = True  # monotone non-decreasing in pna and in sigma=(1-asr)
    d4a = True  # homogeneity in u: g(lam*u, asr) = lam*g(u,asr)
    d4b = True  # homogeneity in sigma: g(u, 1-lam*(1-asr)) = lam*g(u,asr)

    for u in us:
        for a in asrs:
            v = agg(float(u), float(a))
            if not (-_TOL <= v <= 1.0 + _TOL) or np.isnan(v):
                d1 = False
        # D2 consistency
        if abs(agg(float(u), 0.0) - float(u)) > 1e-9:
            d2 = False
    for a in asrs:
        if abs(agg(0.0, float(a)) - 0.0) > 1e-9:
            d2 = False

    # D3 monotonicity in u (asr fixed) and in sigma (u fixed)
    for a in asrs:
        col = [agg(float(u), float(a)) for u in us]
        if any(col[i + 1] - col[i] < -1e-9 for i in range(len(col) - 1)):
            d3 = False
    for u in us:
        # increasing sigma == decreasing asr; iterate asr descending
        row = [agg(float(u), float(a)) for a in asrs[::-1]]
        if any(row[i + 1] - row[i] < -1e-9 for i in range(len(row) - 1)):
            d3 = False

    # D4 homogeneity
    for u in us:
        for a in asrs:
            base = agg(float(u), float(a))
            for lam in (0.25, 0.5, 0.75):
                if abs(agg(lam * float(u), float(a)) - lam * base) > 1e-9:
                    d4a = False
                sigma = 1.0 - float(a)
                a2 = 1.0 - lam * sigma  # scale sigma by lam
                if abs(agg(float(u), a2) - lam * base) > 1e-9:
                    d4b = False

    return {"D1_bounded": d1, "D2_consistency": d2, "D3_monotone": d3, "D4a_homog_u": d4a, "D4b_homog_sigma": d4b}


def reduces_to_asb(n_grid: int = 11) -> bool:
    """Prop 9.1: the default (product) NRP_sys reduces to ASB's NRP = PNA(1-ASR) at N=1."""
    from ..methods.aggregators import product_nrp

    us = np.linspace(0.0, 1.0, n_grid)
    asrs = np.linspace(0.0, 1.0, n_grid)
    for u in us:
        for a in asrs:
            if abs(product_nrp(float(u), float(a)) - float(u) * (1.0 - float(a))) > 1e-12:
                return False
    return True
