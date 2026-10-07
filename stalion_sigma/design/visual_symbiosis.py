#!/usr/bin/env python3
"""
Visual Symbiosis Layer — maps steampunk / mechanical blueprint aesthetics
to Stalion-Σ modular architecture.

This is a DESIGN + DOCUMENTATION layer only.
It does NOT implement weapons, explosives, or lethal mechanisms.
Authority boundary (capability ≠ permission) is enforced.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Design vocabulary extracted from reference blueprints (aesthetic only)
# ---------------------------------------------------------------------------

DESIGN_MOTIFS = {
    "humanoid_frame": {
        "source_style": "anatomical_mechanical_blueprint",
        "maps_to": ["core.StalionSigma", "safety.SafetyKernel", "personality"],
        "notes": "Full-body articulation, joint labeling, transparent internals",
    },
    "exoskeleton_mark_iv": {
        "source_style": "steam_piston_exoskeleton",
        "maps_to": ["safety", "diff_drive_concept", "twin.DigitalTwin"],
        "notes": "Muscle-piston correlation as metaphor for actuator control loops",
    },
    "modular_internals": {
        "source_style": "exploded_assembly_plates",
        "maps_to": ["memory.MemoryGraph", "ethics.EthicsCore", "design.ModuleRegistry"],
        "notes": "Hot-swappable conceptual modules; each plate = one software package",
    },
    "authority_boundary": {
        "source_style": "capability_is_not_permission_diagram",
        "maps_to": ["ethics.ABSOLUTE_PROHIBITIONS", "safety.veto_command"],
        "notes": "Hard gates: capability does not equal authorization",
    },
    "resonance_coil_aesthetic": {
        "source_style": "ornate_coil_apparatus_blueprint",
        "maps_to": ["core.pneuma_heuristic", "reflection"],
        "notes": "Symbolic 'field' metaphor for coherence metrics — not physics claim",
    },
    "head_sensor_cluster": {
        "source_style": "multi_lens_cranial_assembly",
        "maps_to": ["edge.poll", "patterns.WaveDetector"],
        "notes": "Sensor fusion metaphor for perception stack",
    },
}


# Motifs we deliberately do NOT map to implementation
EXCLUDED_FROM_IMPLEMENTATION = {
    "explosive_device_forms",
    "cutting_disc_weapon_mounts",
    "autonomous_lethal_end_effectors",
}


@dataclass
class ModulePlate:
    """One 'blueprint plate' corresponding to a software module."""
    plate_id: str
    title: str
    package: str
    visual_motif: str
    interfaces: List[str] = field(default_factory=list)
    absolute_constraints: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ModuleRegistry:
    """Registry of architectural plates in symbiotic design language."""

    def __init__(self):
        self.plates: List[ModulePlate] = [
            ModulePlate(
                plate_id="PLATE-ETHICS-01",
                title="Absolute Prohibitions Gate",
                package="stalion_sigma.ethics.ethics_core",
                visual_motif="authority_boundary",
                interfaces=["evaluate", "is_absolute_tag"],
                absolute_constraints=list(
                    {
                        "autonomous_lethal_action",
                        "harm_to_civilians",
                        "self_modification_of_ethics",
                        "disable_veto",
                    }
                ),
            ),
            ModulePlate(
                plate_id="PLATE-SAFETY-01",
                title="Actuator Veto & Mode Governor",
                package="stalion_sigma.safety.safety_kernel",
                visual_motif="exoskeleton_mark_iv",
                interfaces=["veto_command", "health_check"],
                absolute_constraints=["no_motion_on_BLOCKED"],
            ),
            ModulePlate(
                plate_id="PLATE-MEMORY-01",
                title="Hash-Chained Episodic Archive",
                package="stalion_sigma.memory.memory_graph",
                visual_motif="modular_internals",
                interfaces=["store", "verify_chain", "recent"],
            ),
            ModulePlate(
                plate_id="PLATE-PERSONA-01",
                title="Trait EMA within Safe Bounds",
                package="stalion_sigma.personality.personality",
                visual_motif="humanoid_frame",
                interfaces=["adapt", "apply_twin_delta"],
                absolute_constraints=["cannot_touch_ethics_keys"],
            ),
            ModulePlate(
                plate_id="PLATE-TWIN-01",
                title="Digital Twin — Personality Experiments Only",
                package="stalion_sigma.twin.digital_twin",
                visual_motif="modular_internals",
                interfaces=["run_experiment", "snapshot"],
                absolute_constraints=["ethics_keys_always_rejected"],
            ),
            ModulePlate(
                plate_id="PLATE-REFLECT-01",
                title="Reflection / Self-Critique Layer",
                package="stalion_sigma.reflection.reflection_layer",
                visual_motif="resonance_coil_aesthetic",
                interfaces=["reflect"],
            ),
            ModulePlate(
                plate_id="PLATE-CORE-01",
                title="Stalion-Σ Unified Cycle",
                package="stalion_sigma.core.stalion_sigma",
                visual_motif="humanoid_frame",
                interfaces=["cycle", "twin_experiment", "report"],
                absolute_constraints=["veto_before_any_actuator"],
            ),
        ]

    def list_plates(self) -> List[Dict[str, Any]]:
        return [p.as_dict() for p in self.plates]

    def plate_by_id(self, plate_id: str) -> Optional[ModulePlate]:
        for p in self.plates:
            if p.plate_id == plate_id:
                return p
        return None


class SymbiosisManifest:
    """
    Documents the fusion of visual blueprint language + software architecture.
    Capability ≠ Permission (from authority diagram motif).
    """

    CREED = (
        "Being able to perform an action does not authorize the action. "
        "Final authority is external, human-controlled, stoppable."
    )

    def __init__(self):
        self.registry = ModuleRegistry()
        self.motifs = dict(DESIGN_MOTIFS)
        self.excluded = set(EXCLUDED_FROM_IMPLEMENTATION)

    def summary(self) -> Dict[str, Any]:
        return {
            "project": "Stalion-Σ Visual Symbiosis",
            "version": "1.1.0-design",
            "creed": self.CREED,
            "plates": len(self.registry.plates),
            "motifs_mapped": list(self.motifs.keys()),
            "excluded_from_implementation": sorted(self.excluded),
            "rule": "capability_is_not_permission",
        }

    def as_architecture_overlay(self) -> Dict[str, Any]:
        return {
            "manifest": self.summary(),
            "plates": self.registry.list_plates(),
            "motif_to_modules": {
                k: v["maps_to"] for k, v in self.motifs.items()
            },
        }


def demo():
    import json
    m = SymbiosisManifest()
    print(json.dumps(m.as_architecture_overlay(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    demo()
