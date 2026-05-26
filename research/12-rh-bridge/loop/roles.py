#!/usr/bin/env python3
"""
4-Role execution engine for the PGS-RH Bridge Autonomous Research Loop.
research/12-rh-bridge/loop/roles.py

PGS objects first (AGENTS.md):
- Ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR selector, deconvolved λ=Λ(n), Chamber-Deconvolved Reciprocal Balance Lemma (live target).

This module simulates (Phase 1–3) or orchestrates (later) the four roles from the approved charter/ledger pattern:
1. PGS Guardian — first pass on every Action Card; enforces PGS objects first, strict separation, no contract violation. Can veto.
2. Analyst — classical completion / analytic side (after PGS frame is locked).
3. Numerics — designs/runs the (generalized) harness verification on the chosen regime or symbolic probe.
4. Proof Architect — maintains draft, writes ledger entry + strict report, proposes resolution updates only on real status change.

Every output from every role must use the mandatory strict separation vocabulary.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class ActionCard:
    target: str
    narrow_item: str
    regime_or_scope: str
    expected_artifact: str
    success_criteria: List[str]
    falsification_criteria: List[str]
    pgs_objects_surface: List[str]

def run_pgs_guardian(card: ActionCard) -> dict:
    """
    PGS Guardian review (always first, real veto power).
    Enforces AGENTS.md + strict separation on every cycle and artifact.
    Vetoes on: missing PGS objects surface, forbidden language (solved/ proved the lemma / progress theater / heuristic etc.), premature closure claims, or any language that treats the live target as resolved before all 3 obligations audited with cross-ref proof artifact.
    """
    forbidden_phrases = [
        "solved", "lemma is proved", "we have shown", "closure achieved", "bridge is solved",
        "the target is resolved", "publication worthy breakthrough here", "paradigm shift delivered",
        "heuristic", "appears to", "suggests", "validated so far", "empirical", "promising"
    ]
    text_to_scan = " ".join([
        card.target or "", card.narrow_item or "", card.regime_or_scope or "",
        " ".join(card.success_criteria or []), " ".join(card.falsification_criteria or []),
        " ".join(card.pgs_objects_surface or [])
    ]).lower()

    violations = [p for p in forbidden_phrases if p in text_to_scan]
    pgs_surface_ok = any("ordered prime-gap" in s.lower() or "gwr" in s.lower() or "deconvolved" in s.lower() or "chamber-deconvolved" in s.lower() for s in (card.pgs_objects_surface or []))

    notes = [
        "PGS objects surfaced at start of review: ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR selector, deconvolved chamber load λ=Λ(n), Chamber-Deconvolved Reciprocal Balance Lemma (live target).",
        "No classical method used as first frame.",
        "Strict separation vocabulary enforced in card and all downstream.",
    ]

    if violations:
        notes.append(f"FORBIDDEN LANGUAGE DETECTED: {violations}. Guardian veto.")
        return {"role": "PGS Guardian", "verdict": "veto", "notes": notes, "reason": "forbidden language or overclaim"}
    if not pgs_surface_ok:
        notes.append("PGS objects surface incomplete or absent from ActionCard. Guardian veto.")
        return {"role": "PGS Guardian", "verdict": "veto", "notes": notes, "reason": "PGS objects not surfaced"}

    notes.append("PGS Guardian audit passed. No contract violation. No premature solution language. Live target remains fully open per strict contract.")
    return {"role": "PGS Guardian", "verdict": "passed", "notes": notes}

def run_analyst(card: ActionCard) -> dict:
    """Analyst designs the probe (numerical or symbolic) after Guardian pass."""
    return {"role": "Analyst", "design": f"Extend generalized harness for {card.narrow_item} on {card.regime_or_scope}. Coefficients from living draft / prior improved Analyst runs.", "notes": ["Classical completion terms analyzed only after PGS frame."]}

def run_numerics(card: ActionCard) -> dict:
    """Numerics executes the harness and produces the strict report."""
    return {"role": "Numerics", "report_path": card.expected_artifact, "observed": "Candidate construction under test on regime X; observed on finite set; remains fully open.", "notes": ["Honest computational limits documented exactly as in verified Regime G improved harness."]}

def run_proof_architect(card: ActionCard, guardian_result: dict, analyst_result: dict, numerics_result: dict) -> dict:
    """Proof Architect writes the ledger entry and (if real status change) proposes updates."""
    observed = numerics_result.get("observed", numerics_result.get("status", "harness executed with strict language"))
    return {
        "role": "Proof Architect",
        "ledger_entry": f"Candidate construction under test on {card.regime_or_scope}. {observed} Live target (Chamber-Deconvolved Reciprocal Balance Lemma) remains fully open.",
        "strict_language_used": True,
        "propose_resolution_update": False,  # only True on real closure with full cross-refs + audits
    }