#!/usr/bin/env python3
"""
State loader for the PGS-RH Bridge Autonomous Research Loop.
research/12-rh-bridge/loop/state.py

PGS objects first (AGENTS.md non-negotiable):
- Ordered prime-gap state (consecutive endpoints p, q with q = min {n > p : τ(n)=2}).
- Divisor-count field τ(n).
- Zero-excess E(n) = (τ(n)/2 - 1) log n; E(n)=0 exactly at primes (n>1).
- GWR / Leftmost Minimum-Divisor Rule (proved in PROOF.md): leftmost argmin E(n) inside nonempty chamber is the unique maximizer of F(n) = -E(n).
- Bridge load H(n) = log n + E(n) = τ(n) log n / 2.
- Exact DNI compression: D(s) = ζ(s)^2, R(s) = -ζ'(s)/ζ(s) after the normalized quotient.
- Deconvolved load λ = τ_Dir^{-1} * H yields λ(n) = Λ(n).
- Live target: Chamber-Deconvolved Reciprocal Balance Lemma (chamber_deconvolved_reciprocal_balance_lemma.md + chamber_load_spectral_centering_resolution.md). After deconvolution, completion, folding to z = u² the residual must be a nonnegative Stieltjes measure (reciprocal balance + nonnegativity). This is the precise source obligation for source-to-spectral placement.

This stub (Phase 1) hardcodes the live target for scaffold testing. Phase 2 will replace with real parser over the resolution .md files + README chain + latest ledger.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

LOOP_DIR = Path(__file__).parent
REPO_ROOT = LOOP_DIR.parent.parent.parent

@dataclass
class LiveTarget:
    name: str
    resolution_file: str
    current_narrow_item: str
    verification_matrix_summary: List[str]
    status: str  # "unresolved" only for the live lemma

def load_live_target() -> LiveTarget:
    """
    Phase 1 stub: returns the canonical live target.
    Real implementation (Phase 2) will parse:
    - research/12-rh-bridge/docs/chamber_deconvolved_reciprocal_balance_lemma.md
    - research/12-rh-bridge/docs/chamber_load_spectral_centering_resolution.md
    - research/12-rh-bridge/README.md (the "live narrow target" paragraphs and verification matrices)
    - Latest entries in proof-construction/ or loop/LOOP_LEDGER.md for "remains fully open" items.
    """
    return LiveTarget(
        name="Chamber-Deconvolved Reciprocal Balance Lemma",
        resolution_file="research/12-rh-bridge/docs/chamber_deconvolved_reciprocal_balance_lemma.md",
        current_narrow_item="Deconvolution survival + reciprocal balance + nonnegative folded mass after completion (see verification matrix in parent README and the three obligations in the lemma document).",
        verification_matrix_summary=[
            "Deconvolution survival: chamber structure must survive λ = τ_Dir^{-1} * H and still admit chamber-derived decomposition (not merely global zeta-side sequence).",
            "Reciprocal balance: after completion and main/trivial removal, folded residual in z = u² must cancel all nontrivial carriers with real exponent a ≠ 0.",
            "Nonnegative folded mass: the final kernel must be a positive measure on the nonnegative t-axis (Stieltjes form).",
        ],
        status="unresolved (live narrow target for autonomous loop)",
    )

def get_current_verification_matrix(target: LiveTarget) -> Dict[str, Any]:
    """
    Returns the three canonical obligations of the live lemma as the verification matrix.
    These are extracted directly from chamber_deconvolved_reciprocal_balance_lemma.md (the authoritative source).
    Real Phase 2+ parser will also cross-reference the parent README reduction chain for the current narrowest sub-item and any "remains open" ledger notes.
    """
    obligations = [
        {
            "id": "deconvolution_survival",
            "description": "The chamber structure is not destroyed by λ = τ_Dir^{-1} * H. The deconvolved coefficients λ(n)=Λ(n) must still admit a chamber-derived decomposition (not merely a global zeta-side sequence).",
            "falsifiable_test_type": "numerical or symbolic check that PGS chamber facts (GWR selector, excess pattern) survive the division by D(s) and produce identifiable packet structure in the Λ coefficients on small chambers.",
        },
        {
            "id": "reciprocal_balance",
            "description": "After completion and removal of main/trivial terms, the deconvolved chamber residual must fold evenly around u=0 in the centered log-scale coordinate. All nontrivial carriers with real exponent a ≠ 0 must cancel.",
            "falsifiable_test_type": "packet drift / folded inequality checks on finite regimes (see existing folded_packet_drift_inequality.md and packet_drift_weighted_average_lemma.md reductions); look for surviving odd negative cost after reciprocal completion.",
        },
        {
            "id": "nonnegative_folded_mass",
            "description": "The folded residual must be positive in the Stieltjes sense. The final kernel must be a positive measure on the nonnegative t-axis (not a signed symmetric distribution).",
            "falsifiable_test_type": "sign-regularity and positivity diagnostics on the folded, deconvolved, completed packets (see chamber_deconvolved_reciprocal_balance_lemma.md and sign-regularity notes in the chain).",
        },
    ]

    return {
        "target": target.name,
        "source": "research/12-rh-bridge/docs/chamber_deconvolved_reciprocal_balance_lemma.md (lemma statement + 'What The Lemma Must Prove From PGS' section)",
        "open_items": obligations,
        "recommended_first_action_rule": "Prefer the narrowest falsifiable scalar or small-regime check that directly tests one obligation (start with deconvolution survival or a concrete packet-drift inequality on the smallest reproducible chamber set, using the generalized harness). Surface PGS objects (GWR, E(n), deconvolved λ) explicitly in every diagnostic. Record as 'candidate construction under test on regime X; observed on finite set; remains fully open'.",
        "pgs_objects": ["ordered prime-gap state", "divisor-count field τ(n)", "zero-excess E(n)", "GWR selector", "deconvolved λ=Λ(n)", "Chamber-Deconvolved Reciprocal Balance Lemma (live target)"],
    }