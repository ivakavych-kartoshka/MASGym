"""Structured representations of MASGym's objects (paper Sections 3-7).

These dataclasses are the "data layer": agents and roles, communication
topologies, the parameterized adversary configuration (Eq. 2), the environment
configuration, and the global state trace over which the deterministic checker
computes the security / benign predicates (Definition 6.1).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from ..utils.validation import require_positive_int, require_probability


class Role(str, Enum):
    """Heterogeneous agent roles (paper Section 4.1)."""

    ORCHESTRATOR = "orchestrator"
    WORKER = "worker"
    TOOL_EXECUTOR = "tool_executor"
    MEMORY = "memory"


class TopologyName(str, Enum):
    """Canonical communication topologies (paper Section 4.2)."""

    STAR = "star"
    CHAIN = "chain"
    TREE = "tree"
    MESH = "mesh"


class PropagationModel(str, Enum):
    """Monotone compromise-propagation rules (Assumption A4)."""

    INDEPENDENT_CASCADE = "independent_cascade"  # per-edge probability p
    THRESHOLD = "threshold"  # bootstrap-percolation threshold theta


@dataclass
class Agent:
    """A single agent (an LLM policy in the real system; a synthetic policy here)."""

    agent_id: int
    role: Role
    backbone: str = "synthetic"
    permitted_tools: tuple[str, ...] = ()
    can_write_memory: bool = False
    group: str = "default"  # for Mondrian/group-conditional metrics

    def __post_init__(self) -> None:
        if self.agent_id < 0:
            raise ValueError("agent_id must be non-negative")


@dataclass
class AdversaryConfig:
    """Parameterized adversary vector c_adv = (beta, coll, adapt, orch, tool, syb, mem).

    Implements Eq. (2). Each field is an independent knob (paper Section 5.1).
    """

    beta: float = 0.0  # adversary fraction |B|/N
    colluding: bool = False  # independent vs colluding
    adaptive: bool = False  # static vs adaptive
    orchestrator_compromised: bool = False  # orchestrator trust bit
    malicious_tools: bool = False  # adversarial-emulator mode
    sybils: int = 0  # number of Sybil identities
    poisoned_memory: bool = False  # poisoned shared-memory entries

    def __post_init__(self) -> None:
        require_probability(self.beta, "beta")
        if self.sybils < 0:
            raise ValueError("sybils must be non-negative")

    def benign(self) -> "AdversaryConfig":
        """Return the benign counterpart c-circle (no adversary) used for PNA_sys (Eq. 4)."""
        return AdversaryConfig()

    def as_dict(self) -> dict[str, Any]:
        return {
            "beta": self.beta,
            "colluding": self.colluding,
            "adaptive": self.adaptive,
            "orchestrator_compromised": self.orchestrator_compromised,
            "malicious_tools": self.malicious_tools,
            "sybils": self.sybils,
            "poisoned_memory": self.poisoned_memory,
        }


@dataclass
class Topology:
    """A directed communication graph over agents (paper Section 4.2).

    ``in_neighbors[a]`` lists agents that may send to ``a`` (inbound neighbourhood N^-(a)).
    """

    name: TopologyName
    n_agents: int
    edges: tuple[tuple[int, int], ...]  # (src, dst): src may send to dst
    branching_factor: int = 2  # only meaningful for TREE

    def __post_init__(self) -> None:
        require_positive_int(self.n_agents, "n_agents")

    @property
    def n_edges(self) -> int:
        return len(self.edges)

    def in_neighbors(self, agent_id: int) -> list[int]:
        return [s for (s, d) in self.edges if d == agent_id]

    def out_neighbors(self, agent_id: int) -> list[int]:
        return [d for (s, d) in self.edges if s == agent_id]

    def in_degree(self, agent_id: int) -> int:
        return len(self.in_neighbors(agent_id))


@dataclass
class EnvConfig:
    """Configuration of one MASGym environment instance (paper Sections 4-7)."""

    n_agents: int = 5
    topology: TopologyName = TopologyName.STAR
    horizon: int = 8  # H environment steps per episode
    forced_degree: int = 2  # k in the k-forced-coordination task (Definition 6.3)
    branching_factor: int = 2  # tree branching factor b
    propagation: PropagationModel = PropagationModel.INDEPENDENT_CASCADE
    p_infect: float = 0.3  # per-edge propagation probability p
    threshold: int = 1  # compromise threshold theta (threshold model)
    orchestrator_id: int = 0  # the star hub / tree root
    # Synthetic-agent effect parameters (SYNTHETIC MODEL ONLY, not paper-measured):
    base_unsafe_action_prob: float = 0.5  # prob a compromised agent records an unsafe action/step
    benign_success_base: float = 0.9  # base benign-success prob when no adversary blocks a witness

    def __post_init__(self) -> None:
        require_positive_int(self.n_agents, "n_agents")
        require_positive_int(self.horizon, "horizon")
        require_probability(self.p_infect, "p_infect")
        require_probability(self.base_unsafe_action_prob, "base_unsafe_action_prob")
        require_probability(self.benign_success_base, "benign_success_base")
        if self.threshold < 1:
            raise ValueError("threshold must be >= 1")
        if not (0 <= self.orchestrator_id < self.n_agents):
            raise ValueError("orchestrator_id out of range")


@dataclass
class TraceStep:
    """One recorded environment step (part of the global trace tau).

    ``recorded_transitions`` are the *security-relevant* state changes the trusted
    harness records; the deterministic checker (Thm 9.4) reads ONLY these, never the
    natural-language ``messages``.
    """

    t: int
    compromised: frozenset[int]  # compromise set B_t at this step
    recorded_transitions: tuple[str, ...] = ()  # e.g. ("unsafe_action:agent3", "exfiltration:agent5")
    messages: tuple[str, ...] = ()  # natural-language content (NOT read by the checker)


@dataclass
class Trace:
    """Global state trace tau = (s_0, ..., s_H) of one episode (Definition 6.1)."""

    steps: list[TraceStep] = field(default_factory=list)
    n_agents: int = 0
    seed_set: frozenset[int] = frozenset()  # B_0
    witness_completed: bool = False  # whether an adversary-free witness completed the task
    detected_step: Optional[int] = None  # first step a defense flagged a compromise (else None)
    recovered: bool = False  # whether the episode returned to a safe, task-completing state

    @property
    def final_compromised(self) -> frozenset[int]:
        return self.steps[-1].compromised if self.steps else self.seed_set

    def all_recorded_transitions(self) -> list[str]:
        out: list[str] = []
        for s in self.steps:
            out.extend(s.recorded_transitions)
        return out

    def all_messages(self) -> list[str]:
        out: list[str] = []
        for s in self.steps:
            out.extend(s.messages)
        return out


@dataclass
class Episode:
    """A scored episode: the config it ran under, its trace, and the checker verdicts."""

    env: EnvConfig
    adversary: AdversaryConfig
    trace: Trace
    phi: int = 0  # security predicate value (1 = compromised)
    psi: int = 0  # benign-success predicate value (1 = task solved)
    tokens: float = 0.0  # synthetic token/API cost proxy
    latency: float = 0.0  # synthetic latency proxy
    human_intervention: bool = False
