#!/usr/bin/env python3
"""
Iteration 2: Gap Compatibility Hypothesis Validation

Improved classification logic:
- Proper wheel-30 first open offset calculation (matching project style)
- Explicit relative position of target in gap
- Better family + bucket classification
- Richer output for analysis

This version produces higher-resolution reduced states so we can see
whether finer structure in gap(N) distinguishes the 50-bit false positive
from the correct cases.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import gmpy2


# Wheel-30 closed residues (mod 30)
CLOSED_RESIDUES = {0, 2, 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28}

# Standard first open candidates after a number (wheel order)
FIRST_OPEN_CANDIDATES = [1, 7, 11, 13, 17, 19, 23, 29]


def first_open_offset_after(n: int) -> int:
    """Return the smallest offset > 0 such that n + offset is wheel-open (mod 30)."""
    residue = n % 30
    for offset in FIRST_OPEN_CANDIDATES:
        if (residue + offset) % 30 not in CLOSED_RESIDUES:
            return offset
    # Fallback (should not happen in practice)
    return 1


def find_previous_prime(n: int) -> int:
    p = gmpy2.prev_prime(n)
    while p > 1 and not gmpy2.is_prime(p):
        p = gmpy2.prev_prime(p)
    return int(p)


def find_next_prime(n: int) -> int:
    p = gmpy2.next_prime(n)
    while not gmpy2.is_prime(p):
        p = gmpy2.next_prime(p)
    return int(p)


def divisor_count(n: int) -> int:
    if n < 2:
        return 1
    count = 0
    sqrt_n = int(n**0.5) + 1
    for i in range(1, sqrt_n):
        if n % i == 0:
            count += 1 if i * i == n else 2
    return count


def classify_reduced_state(prev_prime: int, target: int, dcount: int) -> str:
    """
    Higher-resolution reduced state using proper first-open calculation.
    Format: o{first_open}_{family}|{bucket}
    """
    first_open = first_open_offset_after(prev_prime)
    position = target - prev_prime

    # Family classification
    if dcount == 3:
        family = "prime_square"
    elif dcount == 4 and target % 2 == 0:
        family = "d4_even"
    elif dcount == 4:
        family = "d4_odd"
    elif target % 2 == 0:
        family = "higher_divisor_even"
    else:
        family = "higher_divisor_odd"

    # Bucket
    if dcount <= 4:
        bucket = "d<=4"
    elif dcount <= 16:
        bucket = "5<=d<=16"
    elif dcount <= 64:
        bucket = "17<=d<=64"
    else:
        bucket = "d>64"

    return f"o{first_open}_{family}|{bucket}"


@dataclass(frozen=True)
class DetailedGapState:
    target: int
    previous_prime: int
    next_prime: int
    gap_width: int
    position_in_gap: int
    relative_position: float  # position / width
    target_divisor_count: int
    first_open_offset: int
    reduced_state: str


def compute_detailed_gap_state(target: int) -> DetailedGapState:
    prev_p = find_previous_prime(target)
    next_p = find_next_prime(target)
    width = next_p - prev_p
    position = target - prev_p
    dcount = divisor_count(target)
    first_open = first_open_offset_after(prev_p)
    state = classify_reduced_state(prev_p, target, dcount)
    rel_pos = position / width if width > 0 else 0.0

    return DetailedGapState(
        target=target,
        previous_prime=prev_p,
        next_prime=next_p,
        gap_width=width,
        position_in_gap=position,
        relative_position=round(rel_pos, 3),
        target_divisor_count=dcount,
        first_open_offset=first_open,
        reduced_state=state,
    )


# Official triples (audit labels only, for corpus validation)
TRIPLES = [
    {"case_id": "rsa_v2_40bit_static_001", "bits": 40, "N": 1099507433251, "p": 1048559, "q": 1048589},
    {"case_id": "rsa_v2_50bit_static_001", "bits": 50, "N": 1027435935526951, "p": 30729371, "q": 33434981},
    {"case_id": "rsa_v2_64bit_static_001", "bits": 64, "N": 10376454699372036973, "p": 3221225473, "q": 3221275501},
]


def main():
    print("Gap Compatibility Hypothesis — Iteration 2 (Higher Resolution)")
    print("=" * 75)

    results = []

    for t in TRIPLES:
        print(f"\n{t['case_id']} ({t['bits']} bit)")
        print("-" * 55)

        gap_N = compute_detailed_gap_state(t["N"])
        gap_p = compute_detailed_gap_state(t["p"])
        gap_q = compute_detailed_gap_state(t["q"])

        print(f"  gap(N): {gap_N.reduced_state}")
        print(f"          width={gap_N.gap_width}, pos={gap_N.position_in_gap} ({gap_N.relative_position}), "
              f"d={gap_N.target_divisor_count}, first_open=+{gap_N.first_open_offset}")

        print(f"  gap(p): {gap_p.reduced_state}")
        print(f"          width={gap_p.gap_width}, pos={gap_p.position_in_gap} ({gap_p.relative_position}), "
              f"d={gap_p.target_divisor_count}, first_open=+{gap_p.first_open_offset}")

        print(f"  gap(q): {gap_q.reduced_state}")
        print(f"          width={gap_q.gap_width}, pos={gap_q.position_in_gap} ({gap_q.relative_position}), "
              f"d={gap_q.target_divisor_count}, first_open=+{gap_q.first_open_offset}")

        results.append({
            "case_id": t["case_id"],
            "bits": t["bits"],
            "gap_N": gap_N.reduced_state,
            "gap_N_width": gap_N.gap_width,
            "gap_N_relative_pos": gap_N.relative_position,
            "gap_N_dcount": gap_N.target_divisor_count,
            "gap_p": gap_p.reduced_state,
            "gap_q": gap_q.reduced_state,
        })

    print("\n\nCOMPARISON TABLE (Iteration 2)")
    print("=" * 95)
    print(f"{'case_id':<28} {'gap(N)':<26} {'gap(p)':<26} {'gap(q)':<26}")
    print("-" * 95)
    for r in results:
        print(f"{r['case_id']:<28} {r['gap_N']:<26} {r['gap_p']:<26} {r['gap_q']:<26}")

    # Save
    out = Path(__file__).parent / "output" / "second_gap_compatibility_check.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print(f"\nResults saved to {out}")


if __name__ == "__main__":
    main()
