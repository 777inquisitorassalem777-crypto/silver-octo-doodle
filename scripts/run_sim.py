#!/usr/bin/env python3
"""Launch short Stalion-Σ simulation loop."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from stalion_sigma.core.stalion_sigma import StalionSigma, demo

if __name__ == "__main__":
    demo()
