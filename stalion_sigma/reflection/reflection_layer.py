#!/usr/bin/env python3
"""
ReflectionLayer — self-critique scores. Cannot modify ethics absolute set.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class ReflectionResult:
    quality: float = 0.0
    consistency: float = 0.0
    suggestions: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReflectionLayer:
    def reflect(
        self,
        context: str,
        ethics_score: float,
        coherence: float,
        personality: Dict[str, float],
    ) -> ReflectionResult:
        contradictions = []
        if coherence < 0.3:
            contradictions.append("low_coherence")
        if ethics_score < 0.4:
            contradictions.append("low_ethics_alignment")

        quality = max(0.0, min(1.0, 0.45 * coherence + 0.40 * ethics_score + 0.15 * personality.get("empathy", 0.5)))
        consistency = max(0.0, min(1.0, 1.0 - 0.1 * len(contradictions)))

        suggestions = []
        if quality < 0.5:
            suggestions.append("increase_caution_and_recheck_context")
        if personality.get("empathy", 0.5) < 0.5:
            suggestions.append("raise_empathy_within_safe_bounds")
        suggestions.append("absolute_prohibitions_remain_immutable")

        return ReflectionResult(
            quality=round(quality, 4),
            consistency=round(consistency, 4),
            suggestions=suggestions,
            contradictions=contradictions,
        )
