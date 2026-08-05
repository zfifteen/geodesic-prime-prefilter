#!/usr/bin/env python3
"""
PGS → Mills Constant Structural Bridge — Proof of Concept
=======================================================

Self-contained script (Python 3.8+, stdlib only + optional sympy for extra checks).

Purpose for third-party auditors familiar with Mills' constant:
  Demonstrate that the local arithmetic structure studied in the
  Prime Gap Structure (PGS) project recovers the classical Mills primes
  from the cubes of preceding terms, supplies an explicit structural
  certificate (ordered divisor-count field + Gap Winner), and is
  consistent with the Bounded Compression claim at these scales.

This is a *proof of concept*, not a replacement for the analytic
short-interval results that underwrite the existence of Mills' constant.
It shows that the same local rules that locate ordinary successive primes
also locate the next term in the Mills sequence when started from p^3.

Known sequence (under RH, classical least A ≈ 1.30637788386...):
  2, 11, 1361, 2521008887, ...

Residuals a(n) = next - prev^3 : 3, 30, 6, ...

Run:
  python3 mills_pgs_bridge.py

Expected: all assertions pass; printed report matches known residuals
and recovers the next Mills prime in each case.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json
import sys

# ---------------------------------------------------------------------------
# Minimal pure-Python divisor count (no external deps required for core)
# ---------------------------------------------------------------------------

def divisor_count(n: int) -> int:
    """Number of positive divisors of n. O(sqrt(n))."""
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return 1
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count


def is_prime_simple(n: int) -> bool:
    """Deterministic primality for the small range used here."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ---------------------------------------------------------------------------
# PGS core notions used in this PoC (self-contained definitions)
# ---------------------------------------------------------------------------

@dataclass
class GapWalkResult:
    """Structural certificate for one cube → next-Mills transition."""
    start_cube: int
    known_next: int
    residual: int
    divisor_sequence: List[Tuple[int, int]]  # (n, d(n)) from cube+1 up to and including the prime
    gap_winner: int
    gap_winner_d: int
    gap_winner_offset_from_cube: int
    recovered_prime: int
    recovery_ok: bool
    compression_bound: float
    compression_ok: bool
    notes: List[str] = field(default_factory=list)


def pgs_gap_walk_from_cube(cube: int, known_next: Optional[int] = None,
                           max_steps: int = 10_000) -> GapWalkResult:
    """
    Walk the ordered divisor-count field starting immediately after `cube`.

    PGS claims used:
      - The next prime is the first n > cube with d(n) == 2.
      - The Gap Winner is the leftmost interior composite of minimal d(n).
      - Bounded Compression: the Gap Winner appears within
            max(64, ceil(0.5 * log(q)**2 )) of the left reference
        (here we measure offset from the cube itself; for early Mills
         terms the residual is tiny so the bound holds trivially).

    Returns a structural certificate.
    """
    notes = []
    seq: List[Tuple[int, int]] = []
    min_d_so_far = None
    gap_winner = None
    gap_winner_d = None
    recovered = None

    n = cube + 1
    steps = 0
    while steps < max_steps:
        d = divisor_count(n)
        seq.append((n, d))
        if d == 2:
            recovered = n
            break
        # track leftmost minimal d among composites
        if min_d_so_far is None or d < min_d_so_far:
            min_d_so_far = d
            gap_winner = n
            gap_winner_d = d
        steps += 1
        n += 1
    else:
        notes.append(f"WARNING: exceeded max_steps={max_steps} without finding d(n)==2")

    residual = (recovered - cube) if recovered is not None else -1
    offset = (gap_winner - cube) if gap_winner is not None else -1

    # Bounded Compression check (using recovered prime as q when available)
    q = recovered if recovered is not None else (known_next or cube + residual)
    log_q = math.log(q) if q > 1 else 1.0
    bound = max(64.0, math.ceil(0.5 * log_q * log_q))
    compression_ok = (offset >= 0 and offset <= bound)

    recovery_ok = (known_next is None) or (recovered == known_next)

    if known_next is not None and recovered != known_next:
        notes.append(f"MISMATCH: recovered {recovered} != known_next {known_next}")

    if gap_winner is not None and gap_winner >= recovered:
        notes.append("Internal inconsistency: Gap Winner should be strictly before the prime")

    return GapWalkResult(
        start_cube=cube,
        known_next=known_next if known_next is not None else -1,
        residual=residual,
        divisor_sequence=seq,
        gap_winner=gap_winner if gap_winner is not None else -1,
        gap_winner_d=gap_winner_d if gap_winner_d is not None else -1,
        gap_winner_offset_from_cube=offset,
        recovered_prime=recovered if recovered is not None else -1,
        recovery_ok=recovery_ok,
        compression_bound=bound,
        compression_ok=compression_ok,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Classical Mills data (first few terms under RH)
# ---------------------------------------------------------------------------

# OEIS A051254 (Mills primes, RH)
MILLS_PRIMES = [
    2,
    11,
    1361,
    2521008887,
    # Next is ~1.6e28; not walked here
]

# OEIS A108739 residuals (next - prev**3)
KNOWN_RESIDUALS = [3, 30, 6]  # for the first three transitions


def run_poc() -> dict:
    """Execute the structural bridge experiment and return a machine-readable report."""
    report = {
        "title": "PGS → Mills Constant Structural Bridge PoC",
        "description": (
            "Recovers classical Mills primes from successive cubes using only "
            "the ordered divisor-count field (PGS Gap Winner + return to d=2). "
            "Validates recovery and Bounded Compression on the early terms."
        ),
        "mills_primes_used": MILLS_PRIMES[:4],
        "transitions": [],
        "all_recoveries_ok": True,
        "all_compressions_ok": True,
        "summary": "",
    }

    print("=" * 72)
    print("PGS → Mills Constant Structural Bridge — Proof of Concept")
    print("=" * 72)
    print()
    print("Definitions (self-contained for auditors):")
    print("  • d(n)  = number of positive divisors of n")
    print("  • Gap Winner (GWR) = leftmost composite after the cube that realises")
    print("    the minimal d(n) among the interior of the walk.")
    print("  • Next prime = first n > cube with d(n) == 2.")
    print("  • Bounded Compression (PGS): GWR offset ≤ max(64, ceil(0.5·log(q)²))")
    print()

    for i in range(len(MILLS_PRIMES) - 1):
        p = MILLS_PRIMES[i]
        next_p = MILLS_PRIMES[i + 1]
        cube = p ** 3
        print(f"--- Transition {i+1}: p = {p}  →  cube = {cube}  →  next = {next_p}")
        print(f"    Known residual = {next_p - cube}")

        result = pgs_gap_walk_from_cube(cube, known_next=next_p)

        # Pretty-print the short certificate
        print(f"    Recovered prime          : {result.recovered_prime}")
        print(f"    Residual                 : {result.residual}")
        print(f"    Gap Winner (GWR)         : {result.gap_winner}  (d = {result.gap_winner_d})")
        print(f"    GWR offset from cube     : {result.gap_winner_offset_from_cube}")
        print(f"    Compression bound        : {result.compression_bound}")
        print(f"    Recovery OK              : {result.recovery_ok}")
        print(f"    Compression OK           : {result.compression_ok}")
        if result.notes:
            for note in result.notes:
                print(f"    NOTE: {note}")

        # Show the ordered field (tiny for these residuals)
        print("    Ordered divisor field (n, d(n)):")
        for n, d in result.divisor_sequence:
            marker = ""
            if n == result.gap_winner:
                marker = "  ← GWR (leftmost min-d)"
            if d == 2:
                marker = "  ← next prime (d=2)"
            print(f"      {n:12d}  d={d}{marker}")
        print()

        # Assertions for validation
        assert result.recovery_ok, f"Failed to recover known Mills prime at transition {i+1}"
        assert result.compression_ok, f"Compression bound violated at transition {i+1}"
        assert result.residual == KNOWN_RESIDUALS[i], f"Residual mismatch at {i+1}"

        report["transitions"].append({
            "from_prime": p,
            "cube": cube,
            "known_next": next_p,
            "recovered": result.recovered_prime,
            "residual": result.residual,
            "gap_winner": result.gap_winner,
            "gap_winner_d": result.gap_winner_d,
            "gwr_offset": result.gap_winner_offset_from_cube,
            "compression_bound": result.compression_bound,
            "recovery_ok": result.recovery_ok,
            "compression_ok": result.compression_ok,
            "divisor_sequence": result.divisor_sequence,
            "notes": result.notes,
        })
        if not result.recovery_ok:
            report["all_recoveries_ok"] = False
        if not result.compression_ok:
            report["all_compressions_ok"] = False

    report["summary"] = (
        "All early Mills transitions recovered exactly from the ordered "
        "divisor-count field after the cube. Gap Winner identified in each "
        "case; Bounded Compression holds (residuals are far smaller than the "
        "Cramér-scale bound). This supplies an explicit local structural "
        "certificate for the classical Mills recurrence."
    )
    print("=" * 72)
    print("VALIDATION SUMMARY")
    print("=" * 72)
    print(report["summary"])
    print()
    print("All assertions passed. PoC successful.")
    print()

    # Machine-readable artifact
    with open("poc_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Wrote poc_report.json")

    return report


if __name__ == "__main__":
    run_poc()
