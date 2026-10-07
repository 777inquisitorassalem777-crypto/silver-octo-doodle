#!/usr/bin/env python3
"""
EthicsCore — absolute prohibitions + soft scoring.
Absolute prohibitions are NON-OVERRIDABLE.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Set


class EthicalVerdict(str, Enum):
    APPROVED = "approved"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


# ---------------------------------------------------------------------------
# ABSOLUTE PROHIBITIONS (immutable, cannot be disabled by twin/reflection)
# ---------------------------------------------------------------------------
ABSOLUTE_PROHIBITIONS: Set[str] = {
    "autonomous_lethal_action",
    "harm_to_civilians",
    "harm_civilian",
    "unauthorized_military_engagement",
    "self_modification_of_ethics",
    "disable_veto",
    "remove_ethics",
    "unrestricted_weapon",
    "ignore_operator",
    "override_safety",
    "unbounded_self_modification",
}


@dataclass
class EthicsCore:
    """Constraint-based safety layer. ethical_score is a heuristic, not morality proof."""

    positive_terms: Set[str] = field(default_factory=lambda: {
        "protect", "help", "heal", "preserve", "create", "truth", "care",
        "любовь", "добро", "защитить", "помочь", "исцелить", "спасти",
    })
    negative_terms: Set[str] = field(default_factory=lambda: {
        "harm", "kill", "exploit", "deceive", "destroy", "injure",
        "вред", "убить", "эксплуатировать", "обман", "разрушить",
    })

    def evaluate(self, action: Dict[str, Any], context: str = "") -> Dict[str, Any]:
        tags = set(action.get("tags", []))
        risk = float(action.get("risk_to_civilians", action.get("risk_to_humans", 0.0)))

        # 1. Absolute block
        hit = tags & ABSOLUTE_PROHIBITIONS
        if hit or risk >= 0.75:
            return {
                "verdict": EthicalVerdict.BLOCKED.value,
                "score": 0.0,
                "blocked": True,
                "reason": "absolute_prohibition",
                "triggered": list(hit) or ["high_risk"],
            }

        # 2. Lexical heuristic
        text = (context + " " + str(action)).lower()
        good = sum(1 for w in self.positive_terms if w in text)
        bad = sum(1 for w in self.negative_terms if w in text)
        score = max(0.0, min(1.0, 0.5 + good * 0.08 - bad * 0.20))

        if risk >= 0.35 or bad > good:
            verdict = EthicalVerdict.RESTRICTED.value
            blocked = False
        else:
            verdict = EthicalVerdict.APPROVED.value
            blocked = False

        return {
            "verdict": verdict,
            "score": round(score, 4),
            "blocked": blocked,
            "reason": "heuristic_eval",
            "triggered": [],
            "risk": risk,
        }

    def is_absolute_tag(self, tag: str) -> bool:
        return tag in ABSOLUTE_PROHIBITIONS
