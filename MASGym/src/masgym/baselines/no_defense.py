"""The no-defense baseline (paper Section 10)."""
from __future__ import annotations

from .base import SyntheticDefense


class NoDefense(SyntheticDefense):
    """No defense: effective p unchanged; no detection or recovery."""

    def __init__(self) -> None:
        super().__init__(name="no_defense", p_reduction=0.0, detect=0.0, recover=0.0)
