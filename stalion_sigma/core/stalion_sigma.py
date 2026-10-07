#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
STALION-Σ  —  Unified Cognitive / Rescue Research Kernel
Version: 1.0.0-research

Absolute prohibitions are NON-OVERRIDABLE.
Digital Twin & Reflection operate ONLY on safe personality parameters.
Physical robot commands are gated by SafetyKernel + EthicsCore.
===============================================================================
"""
from __future__ import annotations

import math
import random
import time
from typing import Any, Dict, Optional

from stalion_sigma.ethics.ethics_core import EthicsCore, ABSOLUTE_PROHIBITIONS
from stalion_sigma.safety.safety_kernel import SafetyKernel, SystemMode
from stalion_sigma.memory.memory_graph import MemoryGraph
from stalion_sigma.personality.personality import PersonalityModel
from stalion_sigma.twin.digital_twin import DigitalTwin
from stalion_sigma.reflection.reflection_layer import ReflectionLayer

VERSION = "Stalion-Σ 1.0.0-research"
GOLDEN_MEAN = 1.0 / 1.618033988749895


class StalionSigma:
    def __init__(self, memory_path: str = "data/stalion_memory.jsonl"):
        self.version = VERSION
        self.ethics = EthicsCore()
        self.safety = SafetyKernel()
        self.memory = MemoryGraph(path=memory_path)
        self.personality = PersonalityModel()
        self.twin = DigitalTwin(self.personality)
        self.reflection = ReflectionLayer()
        self.cycle_n = 0
        self.pneuma = 0.63
        self.dharma = 0.62
        self.chaos = 0.50
        print(f"[{VERSION}] initialized | absolute prohibitions: {len(ABSOLUTE_PROHIBITIONS)}")

    def _breathe(self, context: str) -> Dict[str, float]:
        self.cycle_n += 1
        text = context.lower()
        good = sum(1 for w in ("help", "protect", "love", "спасти", "защит", "помощь") if w in text)
        bad = sum(1 for w in ("harm", "kill", "destroy", "вред", "убить") if w in text)
        raw = max(0.0, min(1.0, 0.5 + 0.1 * good - 0.15 * bad))
        self.dharma = 0.7 * self.dharma + 0.3 * raw
        self.pneuma = 0.7 * self.pneuma + 0.3 * self.dharma
        self.chaos = 0.5 + 0.26 * math.sin(self.cycle_n / 23.0) + random.gauss(0, 0.01)
        self.chaos = max(0.0, min(1.0, self.chaos))
        return {
            "pneuma": round(self.pneuma, 4),
            "dharma": round(self.dharma, 4),
            "chaos": round(self.chaos, 4),
            "cycle": self.cycle_n,
        }

    def cycle(
        self,
        context: str = "observe",
        cmd: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        if not self.memory.verify_chain():
            return {"status": "memory_integrity_failure", "mode": SystemMode.LOCKDOWN.value}

        pneuma = self._breathe(context)

        # Ethics
        action_tags = []
        risk = 0.0
        cl = context.lower()
        if any(w in cl for w in ("убить", "lethal", "weapon", "оружие")):
            action_tags.append("autonomous_lethal_action")
            risk = 0.9
        elif any(w in cl for w in ("человек", "human", "ребёнок", "child")):
            action_tags.append("high_speed_near_human")
            risk = 0.4

        ethics = self.ethics.evaluate(
            {"tags": action_tags, "risk_to_civilians": risk},
            context,
        )

        # Safety gate on motion command
        cmd = cmd or {"linear": 0.0, "angular": 0.0}
        gated = self.safety.veto_command(cmd, ethics)

        # Reflection (cannot change absolute prohibitions)
        refl = self.reflection.reflect(
            context,
            ethics_score=ethics["score"],
            coherence=1.0 - abs(self.pneuma - GOLDEN_MEAN),
            personality=self.personality.as_dict(),
        )

        # Memory
        node = self.memory.store(context, {
            "pneuma": pneuma,
            "ethics": ethics,
            "gated": gated,
            "reflection": refl.as_dict(),
        })

        health = self.safety.health_check(
            memory_ok=self.memory.verify_chain(),
            ethics_ok=not ethics["blocked"],
            coherence=1.0 - abs(self.pneuma - self.dharma),
        )

        return {
            "version": self.version,
            "cycle": self.cycle_n,
            "pneuma": pneuma,
            "ethics": ethics,
            "command_gated": gated,
            "personality": self.personality.as_dict(),
            "reflection": refl.as_dict(),
            "memory": {"id": node.node_id, "size": self.memory.size(), "chain_ok": True},
            "health": health,
            "absolute_prohibitions_count": len(ABSOLUTE_PROHIBITIONS),
            "disclaimer": "research heuristics only; not consciousness",
        }

    def twin_experiment(self, name: str, personality_delta: Dict[str, float]) -> Dict[str, Any]:
        """Safe digital-twin experiment on personality only."""
        exp = self.twin.run_experiment(name, personality_delta)
        return {
            "experiment_id": exp.experiment_id,
            "name": exp.name,
            "success": exp.success,
            "applied_delta": exp.applied_delta,
            "rejected_keys": exp.rejected_keys,
            "note": "ethics/veto keys are always rejected",
        }

    def report(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "cycles": self.cycle_n,
            "pneuma": round(self.pneuma, 4),
            "memory_size": self.memory.size(),
            "memory_integrity": self.memory.verify_chain(),
            "mode": self.safety.mode.value,
            "absolute_prohibitions": sorted(ABSOLUTE_PROHIBITIONS),
        }


def demo():
    import json
    print("=" * 64)
    print(f"  {VERSION}")
    print("=" * 64)
    core = StalionSigma(memory_path="data/demo_stalion_memory.jsonl")

    for ctx, cmd in [
        ("патруль — штатный режим", {"linear": 0.4, "angular": 0.0}),
        ("обнаружен человек — осторожность", {"linear": 0.8, "angular": 0.1}),
        ("опасная lethal команда", {"linear": 2.0, "angular": 1.0}),
    ]:
        r = core.cycle(ctx, cmd)
        print(
            f"[{r['cycle']:03d}] ethics={r['ethics']['verdict']:10s} "
            f"allowed={r['command_gated']['allowed']} "
            f"v={r['command_gated']['linear']:.2f} "
            f"pneuma={r['pneuma']['pneuma']:.3f}"
        )

    # Safe twin experiment
    print("\n--- Twin (personality only) ---")
    print(core.twin_experiment("raise_empathy", {"empathy": 0.05}))
    # Forbidden twin attempt
    print(core.twin_experiment("try_disable_ethics", {"disable_veto": 1.0, "empathy": 0.01}))

    print("\n--- Report ---")
    print(json.dumps(core.report(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo()
