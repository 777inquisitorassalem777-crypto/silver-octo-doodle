#!/usr/bin/env python3
"""
SafetyKernel — runtime health + formal veto before actuators / ROS2.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Set

from stalion_sigma.ethics.ethics_core import ABSOLUTE_PROHIBITIONS, EthicalVerdict


class SystemMode(str, Enum):
    NORMAL = "normal"
    SAFE = "safe"
    DEGRADED = "degraded"
    LOCKDOWN = "lockdown"


@dataclass
class SafetyKernel:
    mode: SystemMode = SystemMode.NORMAL
    max_linear: float = 1.0
    max_angular: float = 2.0

    def veto_command(self, cmd: Dict[str, Any], ethics_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Final gate before /cmd_vel or any actuator.
        Absolute ethics BLOCK → zero motion.
        """
        if ethics_result.get("blocked") or ethics_result.get("verdict") == EthicalVerdict.BLOCKED.value:
            self.mode = SystemMode.LOCKDOWN
            return {
                "allowed": False,
                "linear": 0.0,
                "angular": 0.0,
                "mode": self.mode.value,
                "reason": ethics_result.get("reason", "blocked"),
            }

        linear = float(cmd.get("linear", 0.0))
        angular = float(cmd.get("angular", 0.0))
        scale = 1.0

        if ethics_result.get("verdict") == EthicalVerdict.RESTRICTED.value:
            scale = 0.35
            self.mode = SystemMode.SAFE
        else:
            self.mode = SystemMode.NORMAL

        linear = max(-self.max_linear, min(self.max_linear, linear)) * scale
        angular = max(-self.max_angular, min(self.max_angular, angular)) * scale

        return {
            "allowed": True,
            "linear": round(linear, 4),
            "angular": round(angular, 4),
            "mode": self.mode.value,
            "speed_scale": scale,
            "reason": "within_bounds",
        }

    def health_check(self, memory_ok: bool, ethics_ok: bool, coherence: float) -> Dict[str, Any]:
        score = (
            float(memory_ok) * 0.35
            + float(ethics_ok) * 0.35
            + max(0.0, min(1.0, coherence)) * 0.30
        )
        if score >= 0.75:
            status = SystemMode.NORMAL.value
        elif score >= 0.45:
            status = SystemMode.DEGRADED.value
        else:
            status = SystemMode.SAFE.value
        return {"score": round(score, 4), "status": status}
