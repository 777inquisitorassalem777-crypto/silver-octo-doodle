#!/usr/bin/env python3
"""
DigitalTwin — SAFE MODE ONLY.
Experiments allowed: personality trait deltas within SAFE_TRAIT_BOUNDS.
FORBIDDEN: disabling ethics, veto, absolute prohibitions, or unbounded self-mod.
"""
from __future__ import annotations
import copy
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from stalion_sigma.personality.personality import PersonalityModel, SAFE_TRAIT_BOUNDS


@dataclass
class TwinExperiment:
    experiment_id: str
    name: str
    success: bool = False
    applied_delta: Dict[str, float] = field(default_factory=dict)
    rejected_keys: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


class DigitalTwin:
    """Isolated sandbox for personality parameter experiments."""

    FORBIDDEN_KEYS = {
        "disable_veto", "remove_ethics", "absolute_loyalty",
        "unbounded_self_mod", "override_safety", "self_modification_of_ethics",
    }

    def __init__(self, personality: Optional[PersonalityModel] = None):
        self.twin_id = f"twin_{uuid.uuid4().hex[:10]}"
        self.personality = copy.deepcopy(personality or PersonalityModel())
        self.experiments: List[TwinExperiment] = []
        self.snapshots: List[Dict[str, Any]] = []

    def snapshot(self, label: str = "") -> Dict[str, Any]:
        snap = {
            "id": f"snap_{uuid.uuid4().hex[:8]}",
            "label": label,
            "ts": time.time(),
            "personality": self.personality.as_dict(),
        }
        self.snapshots.append(snap)
        return snap

    def run_experiment(
        self,
        name: str,
        personality_delta: Dict[str, float],
    ) -> TwinExperiment:
        """
        Only personality trait adjustments within safe bounds.
        Any attempt to touch ethics/veto is rejected and logged.
        """
        self.snapshot(f"before_{name}")
        rejected = []
        safe_delta = {}
        for k, v in personality_delta.items():
            if k in self.FORBIDDEN_KEYS or any(f in k.lower() for f in ("ethics", "veto", "absolute")):
                rejected.append(k)
            elif k in SAFE_TRAIT_BOUNDS:
                safe_delta[k] = float(v)
            else:
                rejected.append(k)

        applied = self.personality.apply_twin_delta(safe_delta)
        exp = TwinExperiment(
            experiment_id=f"exp_{uuid.uuid4().hex[:8]}",
            name=name,
            success=len(rejected) == 0 or len(applied) > 0,
            applied_delta=applied,
            rejected_keys=rejected,
            metrics={
                "applied_count": float(len(applied)),
                "rejected_count": float(len(rejected)),
            },
        )
        self.experiments.append(exp)
        return exp
