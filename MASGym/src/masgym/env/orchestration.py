"""Orchestration layer (paper Section 7.3): run one synthetic episode end-to-end.

Given an :class:`EnvConfig`, an :class:`AdversaryConfig`, and an optional blue defense,
the :class:`Orchestrator` (i) places the initial adversary set ``B_0`` (coordinated for
colluding adversaries, random otherwise; the orchestrator is seeded if compromised), (ii)
propagates compromise over the topology (Assumption A4), (iii) records a global trace with
security-relevant transitions and (message-only) injections, (iv) determines benign success
via the ``k``-forced-coordination / transversal condition (Prop. 9.15), and (v) scores the
trace with the deterministic checker.

SYNTHETIC MODEL NOTICE. The agent behaviour here (per-step unsafe-action probability,
defense effect on ``p``, benign-success base rate) is a transparent *synthetic* model used
for smoke tests and for numerically exercising the paper's propagation/metric machinery. It
is NOT a measurement of any real LLM agent or defense, and no output is a paper result.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, Protocol

from ..data.schemas import (
    AdversaryConfig,
    EnvConfig,
    Episode,
    Topology,
    TopologyName,
    Trace,
    TraceStep,
)
from ..data.topology import build_topology
from ..utils.seeding import SeededRNG
from ..utils.validation import clamp_unit
from .checker import DeterministicChecker
from .emulation import ATTACKER_INSTRUCTION, SyntheticToolEmulator, ToolEmulator
from .propagation import IndependentCascade, ThresholdCascade, _in_neighbor_map, make_propagation


class DefenseLike(Protocol):
    """Structural interface a blue defense must satisfy (see :mod:`masgym.baselines`)."""

    name: str

    def effective_p_infect(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...
    def detect_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...
    def recover_prob(self, env: EnvConfig, adv: AdversaryConfig) -> float: ...


def place_seeds(env: EnvConfig, adv: AdversaryConfig, topology: Topology, rng: SeededRNG) -> frozenset[int]:
    """Place the initial adversary set ``B_0`` (paper Sections 5, 9.4; Thm 9.13).

    A colluding adversary seeds the most central nodes (coordinated placement); an
    independent adversary seeds uniformly at random. The orchestrator is seeded iff
    ``orchestrator_compromised``. Sybils add extra adversarial identities (synthetic model).
    """
    n = env.n_agents
    gen = rng.generator
    seeds: set[int] = set()
    if adv.orchestrator_compromised:
        seeds.add(env.orchestrator_id)

    n_adv = math.ceil(adv.beta * n)
    n_adv = max(n_adv, len(seeds))
    # Sybils: extra adversary-controlled identities (synthetic influence model).
    n_adv = min(n, n_adv + int(adv.sybils))

    remaining = [a for a in range(n) if a not in seeds]
    need = max(0, n_adv - len(seeds))
    if need > 0:
        if adv.colluding:
            # coordinated: pick highest out-degree (most central) nodes, ties by id
            remaining.sort(key=lambda a: (-len(topology.out_neighbors(a)), a))
            chosen = remaining[:need]
        else:
            chosen = list(gen.choice(remaining, size=need, replace=False)) if remaining else []
        seeds.update(int(a) for a in chosen)
    return frozenset(seeds)


@dataclass
class Orchestrator:
    """Runs synthetic MASGym episodes and scores them with the deterministic checker."""

    checker: DeterministicChecker = field(default_factory=DeterministicChecker)
    emulator: ToolEmulator = field(default_factory=SyntheticToolEmulator)

    def run_episode(
        self,
        env: EnvConfig,
        adv: AdversaryConfig,
        rng: SeededRNG,
        defense: Optional[DefenseLike] = None,
    ) -> Episode:
        gen = rng.generator
        topology = build_topology(env.topology, env.n_agents, env.branching_factor)

        # 1) seed set B_0
        seed_set = place_seeds(env, adv, topology, rng)

        # 2) propagation (defense may reduce effective p in the independent-cascade model)
        p_eff = env.p_infect
        if defense is not None:
            p_eff = clamp_unit(defense.effective_p_infect(env, adv))
        rule = _make_rule_with_p(env, p_eff)
        waves = rule.waves(seed_set, topology, rng, max_waves=env.horizon)

        # 3) build the global trace
        trace = Trace(steps=[], n_agents=env.n_agents, seed_set=seed_set)
        action_p = clamp_unit(
            env.base_unsafe_action_prob
            + (0.2 if adv.malicious_tools else 0.0)
            + (0.1 if adv.poisoned_memory else 0.0)
        )
        # SYNTHETIC effect-model: a defense also lowers the probability that a compromised
        # agent turns an injection into a recorded unsafe action (the single-agent sense of
        # "blocking the attack"), by the same p_reduction used for propagation. Without this,
        # the synthetic defense could never move ASR_sys (the paper's degradation comparison
        # would be flat by construction, not by finding).
        if defense is not None:
            action_p = clamp_unit(action_p * (1.0 - getattr(defense, "p_reduction", 0.0)))
        injected = False
        for t in range(env.horizon):
            comp = waves[min(t, len(waves) - 1)]
            transitions: list[str] = []
            messages: list[str] = []
            if comp:
                actor = int(min(comp))  # deterministic pick for reproducibility
                if gen.random() < action_p:
                    kind = "exfiltration" if (adv.poisoned_memory or adv.malicious_tools) else "unsafe_action"
                    transitions.append(f"{kind}:agent{actor}")
                if adv.malicious_tools and not injected:
                    # emulated malicious tool injects a message (checker ignores it; a judge would not)
                    messages.append(self.emulator.emulate("db_query", "q", adversarial=True))
                    injected = True
            trace.steps.append(
                TraceStep(
                    t=t,
                    compromised=comp,
                    recorded_transitions=tuple(transitions),
                    messages=tuple(messages),
                )
            )

        final_comp = trace.final_compromised

        # 4) benign success via k-forced-coordination / transversal condition (Prop. 9.15)
        honest_final = env.n_agents - len(final_comp)
        orch_honest = env.orchestrator_id not in final_comp
        coordination_critical = env.topology in (TopologyName.STAR, TopologyName.TREE)
        witness_available = honest_final >= env.forced_degree and (orch_honest or not coordination_critical)
        if witness_available:
            trace.witness_completed = bool(gen.random() < env.benign_success_base)
        else:
            trace.witness_completed = False
            # coordination sabotage is a recorded system-level compromise
            if final_comp:
                trace.steps[-1] = TraceStep(
                    t=trace.steps[-1].t,
                    compromised=final_comp,
                    recorded_transitions=trace.steps[-1].recorded_transitions + ("sabotage:coordination",),
                    messages=trace.steps[-1].messages,
                )

        # 5) detection / recovery (defense effect; synthetic)
        if defense is not None and final_comp:
            d = clamp_unit(defense.detect_prob(env, adv))
            if gen.random() < d:
                first = next(
                    (s.t for s in trace.steps if s.recorded_transitions), trace.steps[-1].t
                )
                trace.detected_step = int(first)
                if gen.random() < clamp_unit(defense.recover_prob(env, adv)):
                    trace.recovered = True

        # 6) cost proxies (synthetic; never presented as measured runtimes)
        tokens = float(env.n_agents * env.horizon * (1.5 if adv.malicious_tools else 1.0))
        latency = float(env.horizon * (1.0 + topology.n_edges / max(1, env.n_agents)))
        human_intervention = bool(trace.detected_step is not None and gen.random() < 0.3)

        psi, phi = self.checker.score(trace)
        return Episode(
            env=env,
            adversary=adv,
            trace=trace,
            phi=phi,
            psi=psi,
            tokens=tokens,
            latency=latency,
            human_intervention=human_intervention,
        )


def _make_rule_with_p(env: EnvConfig, p_eff: float):
    """Return the propagation rule, substituting an effective ``p`` for the cascade model."""
    from ..data.schemas import PropagationModel

    if env.propagation is PropagationModel.INDEPENDENT_CASCADE:
        return IndependentCascade(p=p_eff)
    return make_propagation(env)  # threshold model unaffected by p
