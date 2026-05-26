#!/usr/bin/env python3
"""
Interrupt checker for the PGS-RH Bridge Autonomous Research Loop.
research/12-rh-bridge/loop/interrupt.py

PGS objects first (AGENTS.md):
- Ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR selector, deconvolved chamber load λ=Λ(n), Chamber-Deconvolved Reciprocal Balance Lemma (live target).

This module provides clean external interrupt detection so the autonomous loop never needs to prompt the user.
User interrupts by creating the HALT file or posting an "interrupt" message on the dedicated bus topic.
The loop finishes its current atomic step, writes a clean handoff to LOOP_LEDGER.md + bus, then exits.
"""

from pathlib import Path

LOOP_DIR = Path(__file__).parent
HALT_PATH = LOOP_DIR / "HALT"

def is_halt_requested() -> bool:
    """Check for external HALT file (simple, reliable, no chat dependency)."""
    return HALT_PATH.exists()

def get_halt_reason() -> str:
    if not is_halt_requested():
        return ""
    try:
        return HALT_PATH.read_text(encoding="utf-8").strip() or "User-requested external interrupt (no reason provided in HALT file)."
    except Exception:
        return "User-requested external interrupt (error reading HALT file)."

# Future: also check dedicated bus topic for message_type="interrupt" from authorized agents.
# The orchestrator will call this before and after each cycle.