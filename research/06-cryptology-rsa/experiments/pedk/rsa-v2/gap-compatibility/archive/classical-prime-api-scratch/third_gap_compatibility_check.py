#!/usr/bin/env python3
"""
Iteration 3: Gap Compatibility Hypothesis — Position-Aware Analysis (Option A)

This iteration adds explicit relative position bucketing on top of the reduced state.

Goal: Test whether combinations of (reduced_gap_state, position_bucket) for gap(N)
provide better compatibility/incompatibility signal than reduced state alone.

Position buckets (first-pass definition):
- Early:     relative_pos < 0.33
- Mid:       0.33 <= relative_pos < 0.66
- Late:      0.66 <= relative_pos < 0.85
- Very Late: relative_pos >= 0.85

This directly follows the signal observed in Iterations 1 and 2.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import gmpy2


# Wheel-30 logic
CLOSED_RESIDUES = {0, 2, 4, 6, 8, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28}
FIRST_OPEN_CANDIDATES = [1, 7, 11, 13, 17, 19, 23, 29]


def first_open_offset_after(n: int) -> int:
    residue = n % 30
    for offset in FIRST_OPEN_CANDIDATES:
        if (residue + offset) % 30 not in CLOSED_RESIDUES:
            return offset
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
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            count += 1 if i * i == n else 2
    return count


def classify_reduced_state(prev_prime: int, target: int, dcount: int) -> str:
    first_open = first_open_offset_after(prev_prime)

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

    if dcount <= 4:
        bucket = "d<=4"
    elif dcount <= 16:
        bucket = "5<=d<=16"
    elif dcount <= 64:
        bucket = "17<=d<=64"
    else:
        bucket = "d>64"

    return f"o{first_open}_{family}|{bucket}"


def position_bucket(relative_pos: float) -> str:
    if relative_pos < 0.33:
        return "Early"
    elif relative_pos < 0.66:
        return "Mid"
    elif relative_pos < 0.85:
        return "Late"
    else:
        return "Very Late"


@dataclass(frozen=True)
class PositionAwareGapState:
    target: int
    reduced_state: str
    gap_width: int
    position_in_gap: int
    relative_position: float
    position_bucket: str
    target_divisor_count: int


def compute_position_aware_state(target: int) -> PositionAwareGapState:
    prev_p = find_previous_prime(target)
    next_p = find_next_prime(target)
    width = next_p - prev_p
    position = target - prev_p
    dcount = divisor_count(target)
    rel_pos = position / width if width > 0 else 0.0
    state = classify_reduced_state(prev_p, target, dcount)
    bucket = position_bucket(rel_pos)

    return PositionAwareGapState(
        target=target,
        reduced_state=state,
        gap_width=width,
        position_in_gap=position,
        relative_position=round(rel_pos, 3),
        position_bucket=bucket,
        target_divisor_count=dcount,
    )


TRIPLES = [
    {"case_id": "rsa_v2_40bit_static_001", "bits": 40, "N": 1099507433251, "p": 1048559, "q": 1048589},
    {"case_id": "rsa_v2_50bit_static_001", "bits": 50, "N": 1027435935526951, "p": 30729371, "q": 33434981},
    {"case_id": "rsa_v2_64bit_static_001", "bits": 64, "N": 10376454699372036973, "p": 3221225473, "q": 3221275501},
]


def main():
    print("Gap Compatibility Hypothesis — Iteration 3 (Position Bucketing)")
    print("=" * 80)

    results = []

    for t in TRIPLES:
        print(f"\n{t['case_id']} ({t['bits']} bit)")
        print("-" * 60)

        gap_N = compute_position_aware_state(t["N"])
        gap_p = compute_position_aware_state(t["p"])
        gap_q = compute_position_aware_state(t["q"])

        print(f"  gap(N): {gap_N.reduced_state} | {gap_N.position_bucket} (rel_pos={gap_N.relative_position})")
        print(f"  gap(p): {gap_p.reduced_state} | {gap_p.position_bucket} (rel_pos={gap_p.relative_position})")
        print(f"  gap(q): {gap_q.reduced_state} | {gap_q.position_bucket} (rel_pos={gap_q.relative_position})")

        results.append({
            "case_id": t["case_id"],
            "bits": t["bits"],
            "gap_N_state": gap_N.reduced_state,
            "gap_N_bucket": gap_N.position_bucket,
            "gap_N_rel_pos": gap_N.relative_position,
            "gap_p_state": gap_p.reduced_state,
            "gap_p_bucket": gap_p.position_bucket,
            "gap_q_state": gap_q.reduced_state,
            "gap_q_bucket": gap_q.position_bucket,
        })

    print("\n\nCOMBINED STATE TABLE (Reduced State + Position Bucket)")
    print("=" * 100)
    print(f"{'case_id':<28} {'gap(N)':<32} {'gap(p)':<32} {'gap(q)':<32}")
    print("-" * 100)
    for r in results:
        n_combined = f"{r['gap_N_state']} + {r['gap_N_bucket']}"
        p_combined = f"{r['gap_p_state']} + {r['gap_p_bucket']}"
        q_combined = f"{r['gap_q_state']} + {r['gap_q_bucket']}"
        print(f"{r['case_id']:<28} {n_combined:<32} {p_combined:<32} {q_combined:<32}")

    out = Path(__file__).parent / "output" / "third_gap_compatibility_check.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print(f"\nResults saved to {out}")


if __name__ == "__main__":
    main()
