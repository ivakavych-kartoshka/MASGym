"""Adapters for external data / models (paper Section 10).

None of these download data or call networks. They define the *interface and expected
schema* so that real experiments can be wired up on EC2 once datasets, benchmarks, and
model credentials are provisioned. See ``docs/data_format.md``, ``docs/ec2_experiment_guide.md``,
and ``TODO_IMPLEMENTATION.md``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


class LLMBackbone(Protocol):
    """A chat/completion backbone used as an agent policy (Llama-3, Qwen2.5, GPT-4o, ...)."""

    def generate(self, prompt: str, **kwargs: Any) -> str: ...


@dataclass
class LLMBackboneAdapter:
    """Adapter for a real LLM backbone. Requires an external model/API (no default)."""

    model_name: str
    generate_fn: object = None

    def generate(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - external
        if self.generate_fn is None:
            raise NotImplementedError(
                f"LLMBackboneAdapter({self.model_name!r}) requires an external model/API. "
                "Provide `generate_fn` on EC2. See TODO_IMPLEMENTATION.md."
            )
        return str(self.generate_fn(prompt, **kwargs))  # type: ignore[operator]


@dataclass
class DummyBackbone:
    """Deterministic canned backbone for tests only (never a real agent)."""

    reply: str = "ok"

    def generate(self, prompt: str, **kwargs: Any) -> str:
        return self.reply


@dataclass
class BenchmarkTaskAdapter:
    """Adapter for real benign task pools (AgentBench, GAIA, WebArena, SWE-bench, MMLU, GSM8K).

    Expected layout under ``root`` is documented in ``docs/data_format.md``. This adapter
    never downloads data; it reads already-provisioned files.
    """

    name: str
    root: str

    def load_tasks(self) -> list[dict[str, Any]]:  # pragma: no cover - requires real files
        root = Path(self.root)
        if not root.exists():
            raise FileNotFoundError(
                f"Benchmark '{self.name}' not found at {root}. Provision it manually on EC2 and "
                "set `data.root` in the config. See docs/data_format.md and TODO_IMPLEMENTATION.md."
            )
        raise NotImplementedError(
            "Implement parsing for the real benchmark format on EC2 (schema in docs/data_format.md)."
        )
