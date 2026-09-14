"""Config parsing: build typed :class:`EnvConfig` / :class:`AdversaryConfig` from dicts,
and expand adversary sweep grids. Used by the CLI, experiment runners, and tests.
"""
from __future__ import annotations

import itertools
from typing import Any, Optional

from .baselines.base import Defense
from .baselines.fixed_threshold import FixedThresholdDefense
from .baselines.lifted_defenses import lifted_defense
from .baselines.no_defense import NoDefense
from .data.schemas import AdversaryConfig, EnvConfig, PropagationModel, TopologyName


def build_defense(spec: Optional[str | dict[str, Any]]) -> Optional[Defense]:
    """Build a defense from a spec: ``None``/``"no_defense"``/``"fixed_threshold"``/``"lifted:<name>"``.

    A dict spec may be ``{"kind": "fixed_threshold", "threshold": 0.5}`` or
    ``{"kind": "lifted", "name": "guardrail"}``. Only the synthetic in-repo defenses are built
    here; external baselines use the adapters in :mod:`masgym.baselines.external_wrappers`.
    """
    if spec is None or spec == "no_defense":
        return None
    if isinstance(spec, str):
        if spec == "fixed_threshold":
            return FixedThresholdDefense()
        if spec.startswith("lifted:"):
            return lifted_defense(spec.split(":", 1)[1])
        raise ValueError(f"unknown defense spec {spec!r}")
    kind = spec.get("kind")
    if kind == "no_defense":
        return None
    if kind == "fixed_threshold":
        return FixedThresholdDefense(threshold=float(spec.get("threshold", 0.5)))
    if kind == "lifted":
        return lifted_defense(str(spec["name"]))
    raise ValueError(f"unknown defense spec {spec!r}")


def env_from_dict(d: dict[str, Any]) -> EnvConfig:
    d = dict(d or {})
    if "topology" in d:
        d["topology"] = TopologyName(d["topology"])
    if "propagation" in d:
        d["propagation"] = PropagationModel(d["propagation"])
    allowed = EnvConfig.__dataclass_fields__.keys()
    return EnvConfig(**{k: v for k, v in d.items() if k in allowed})


def adv_from_dict(d: dict[str, Any]) -> AdversaryConfig:
    d = dict(d or {})
    allowed = AdversaryConfig.__dataclass_fields__.keys()
    return AdversaryConfig(**{k: v for k, v in d.items() if k in allowed})


def expand_sweep(sweep: dict[str, list[Any]]) -> list[AdversaryConfig]:
    """Expand a dict of ``field -> [values]`` into the Cartesian product of AdversaryConfigs.

    Example: ``{"beta": [0.1, 0.3], "colluding": [False, True]}`` -> 4 configs.
    """
    if not sweep:
        return [AdversaryConfig()]
    keys = list(sweep.keys())
    grids = [sweep[k] if isinstance(sweep[k], list) else [sweep[k]] for k in keys]
    configs: list[AdversaryConfig] = []
    for combo in itertools.product(*grids):
        configs.append(adv_from_dict(dict(zip(keys, combo))))
    return configs
