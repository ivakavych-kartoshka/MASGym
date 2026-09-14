"""Deterministic seeding utilities.

All stochasticity in MASGym flows through an explicit :class:`numpy.random.Generator`
so that runs are reproducible under a fixed seed (paper Assumption A2: i.i.d. episodes;
reproducibility requirement of the evaluation protocol).
"""
from __future__ import annotations

import os
import random
from dataclasses import dataclass

import numpy as np


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy, and the ``PYTHONHASHSEED`` environment for determinism.

    This affects any incidental use of the global RNGs. Prefer :class:`SeededRNG`
    for all sampling in library code so that determinism does not rely on global state.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


@dataclass
class SeededRNG:
    """A thin, explicit wrapper around a NumPy Generator.

    Parameters
    ----------
    seed:
        Non-negative integer seed. The same seed yields identical draws.
    """

    seed: int

    def __post_init__(self) -> None:
        if self.seed < 0:
            raise ValueError(f"seed must be non-negative, got {self.seed}")
        self._gen = np.random.default_rng(self.seed)

    @property
    def generator(self) -> np.random.Generator:
        return self._gen

    def spawn(self, offset: int) -> "SeededRNG":
        """Return a child RNG deterministically derived from this one."""
        return SeededRNG(seed=int((self.seed + 1) * 1_000_003 + offset) % (2**31 - 1))
