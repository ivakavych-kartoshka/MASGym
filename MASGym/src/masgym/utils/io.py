"""IO helpers: config loading, result persistence, and run provenance.

Every result file written by MASGym carries a provenance header
(:func:`run_metadata`) recording the seed, config hash, package version, and a
``synthetic`` flag so that synthetic smoke-test outputs are never mistaken for
paper results.
"""
from __future__ import annotations

import hashlib
import json
import platform
import time
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from .. import __version__

SYNTHETIC_BANNER = "synthetic smoke-test output, not a paper result"


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_yaml(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data or {}


def _to_jsonable(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    return obj


def config_hash(config: dict[str, Any]) -> str:
    """Stable short hash of a config dict for provenance."""
    blob = json.dumps(config, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:12]


def run_metadata(config: dict[str, Any], seed: int, synthetic: bool = True) -> dict[str, Any]:
    """Provenance header attached to every result file."""
    return {
        "masgym_version": __version__,
        "seed": seed,
        "config_hash": config_hash(config),
        "python": platform.python_version(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "synthetic": synthetic,
        "provenance_note": SYNTHETIC_BANNER if synthetic else "real-data run",
    }


def write_json(path: str | Path, payload: Any) -> Path:
    p = Path(path)
    ensure_dir(p.parent)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(_to_jsonable(payload), fh, indent=2)
    return p


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> Path:
    """Write a list of dict rows to CSV. Tables are always generated, never hard-coded."""
    p = Path(path)
    ensure_dir(p.parent)
    pd.DataFrame(rows).to_csv(p, index=False)
    return p
