"""Small, reusable input validators with clear error messages."""
from __future__ import annotations

from typing import Iterable

import numpy as np


def require_probability(value: float, name: str = "value") -> float:
    """Validate that ``value`` is a probability in [0, 1]."""
    v = float(value)
    if not (0.0 <= v <= 1.0) or np.isnan(v):
        raise ValueError(f"{name} must be a probability in [0, 1], got {value!r}")
    return v


def require_positive_int(value: int, name: str = "value") -> int:
    """Validate that ``value`` is a strictly positive integer."""
    if not isinstance(value, (int, np.integer)) or int(value) <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    return int(value)


def require_nonneg_int(value: int, name: str = "value") -> int:
    if not isinstance(value, (int, np.integer)) or int(value) < 0:
        raise ValueError(f"{name} must be a non-negative integer, got {value!r}")
    return int(value)


def clamp_unit(value: float) -> float:
    """Clamp a float into [0, 1] (used defensively before aggregation)."""
    return float(min(1.0, max(0.0, value)))


def validate_risk_values(values: Iterable[float], name: str = "risk") -> np.ndarray:
    """Validate that all values lie in [0, 1]; return them as a float array.

    Mirrors the paper's requirement that per-agent/step risk signals are in [0, 1].
    """
    arr = np.asarray(list(values), dtype=float)
    if arr.size and (np.any(arr < 0.0) or np.any(arr > 1.0) or np.any(np.isnan(arr))):
        raise ValueError(f"all {name} values must lie in [0, 1]")
    return arr
