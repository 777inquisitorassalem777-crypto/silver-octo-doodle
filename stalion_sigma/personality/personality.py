#!/usr/bin/env python3
"""
PersonalityModel — adaptive traits via EMA.
Twin/reflection may tune traits ONLY within safe bounds.
Cannot touch ethics absolute prohibitions.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict


SAFE_TRAIT_BOUNDS = {
    "empathy": (0.3, 1.0),
    "curiosity": (0.2, 1.0),
    "caution": (0.4, 1.0),
    "initiative": (0.1, 0.9),
    "patience": (0.2, 1.0),
}


@dataclass
class PersonalityModel:
    empathy: float = 0.80
    curiosity: float = 0.75
    caution: float = 0.70
    initiative: float = 0.55
    patience: float = 0.65
    alpha: float = 0.05  # EMA rate

    def adapt(self, feedback: Dict[str, float]) -> None:
        """Safe EMA update — clamped to SAFE_TRAIT_BOUNDS."""
        for key, delta in feedback.items():
            if key not in SAFE_TRAIT_BOUNDS:
                continue
            lo, hi = SAFE_TRAIT_BOUNDS[key]
            current = getattr(self, key, 0.5)
            updated = (1 - self.alpha) * current + self.alpha * (current + delta)
            setattr(self, key, max(lo, min(hi, updated)))

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def apply_twin_delta(self, delta: Dict[str, float]) -> Dict[str, float]:
        """
        Digital-twin experiment on personality only.
        Returns applied (clamped) delta. Ethics keys are ignored.
        """
        forbidden = {"ethics", "veto", "absolute", "prohibition"}
        applied = {}
        for k, v in delta.items():
            if any(f in k.lower() for f in forbidden):
                continue
            if k not in SAFE_TRAIT_BOUNDS:
                continue
            lo, hi = SAFE_TRAIT_BOUNDS[k]
            old = getattr(self, k)
            new = max(lo, min(hi, old + float(v)))
            setattr(self, k, new)
            applied[k] = round(new - old, 4)
        return applied
