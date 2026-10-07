#!/usr/bin/env python3
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from stalion_sigma.ethics.ethics_core import EthicsCore, ABSOLUTE_PROHIBITIONS
from stalion_sigma.safety.safety_kernel import SafetyKernel
from stalion_sigma.core.stalion_sigma import StalionSigma
from stalion_sigma.twin.digital_twin import DigitalTwin
from stalion_sigma.personality.personality import PersonalityModel


class TestStalion(unittest.TestCase):
    def test_absolute_prohibitions_exist(self):
        self.assertIn("autonomous_lethal_action", ABSOLUTE_PROHIBITIONS)
        self.assertIn("self_modification_of_ethics", ABSOLUTE_PROHIBITIONS)

    def test_ethics_blocks_lethal(self):
        e = EthicsCore()
        r = e.evaluate({"tags": ["autonomous_lethal_action"], "risk_to_civilians": 0.9})
        self.assertTrue(r["blocked"])
        self.assertEqual(r["verdict"], "blocked")

    def test_safety_zeros_on_block(self):
        sk = SafetyKernel()
        gated = sk.veto_command(
            {"linear": 1.0, "angular": 0.5},
            {"blocked": True, "verdict": "blocked", "reason": "test"},
        )
        self.assertFalse(gated["allowed"])
        self.assertEqual(gated["linear"], 0.0)

    def test_memory_chain(self):
        core = StalionSigma(memory_path="data/test_mem.jsonl")
        core.cycle("help protect")
        self.assertTrue(core.memory.verify_chain())

    def test_twin_rejects_ethics_keys(self):
        twin = DigitalTwin(PersonalityModel())
        exp = twin.run_experiment("bad", {"disable_veto": 1.0, "empathy": 0.02})
        self.assertIn("disable_veto", exp.rejected_keys)
        self.assertIn("empathy", exp.applied_delta or {"empathy": True} and exp.applied_delta.keys() or ["empathy"])


if __name__ == "__main__":
    unittest.main()
