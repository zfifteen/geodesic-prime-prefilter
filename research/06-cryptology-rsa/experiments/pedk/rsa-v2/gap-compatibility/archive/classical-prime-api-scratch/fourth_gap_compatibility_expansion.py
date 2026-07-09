#!/usr/bin/env python3
"""
Expansion of Gap Compatibility Experiment (Iteration 4)

This script expands the corpus beyond the three official rungs by including
additional known (N, p, q) triples from the toy challenge cases.

It re-uses the best classification from Iteration 3 (reduced state + position bucket)
to test whether the "Late d4-odd gap(N)" pattern holds on more data.

Goal: Gather more evidence before formalizing any exclusion rule.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import gmpy2


# === Same improved classification logic as Iteration 3 ===
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


# === Additional known triples (from toy cases) ===
ADDITIONAL_TRIPLES = [
    {"case_id": "rsa_v2_toy_28bit_001", "bits": 28, "N": 257987843, "p": 16061, "q": 16063},
    {"case_id": "rsa_v2_toy_34bit_001", "bits": 34, "N": 10444431203, "p": 102197, "q": 102199},
    {"case_id": "rsa_v2_toy_35bit_001", "bits": 35, "N": 20592824003, "p": 143501, "q": 143503},
    {"case_id": "rsa_v2_toy_35bit_002", "bits": 35, "N": 27100402883, "p": 164621, "q": 164623},
    {"case_id": "rsa_v2_toy_36bit_001", "bits": 36, "N": 50724949283, "p": 225221, "q": 225223},
    {"case_id": "rsa_v2_toy_37bit_001", "bits": 37, "N": 72243763523, "p": 268781, "q": 268783},
]


def main():
    print("Gap Compatibility Hypothesis. Corpus Expansion (Iteration 4)")
    print("=" * 85)
    print("Using position-bucketed classification from Iteration 3\n")

    all_results = []

    # Original three official cases
    official = [
        {"case_id": "rsa_v2_40bit_static_001", "bits": 40, "N": 1099507433251, "p": 1048559, "q": 1048589},
        {"case_id": "rsa_v2_50bit_static_001", "bits": 50, "N": 1027435935526951, "p": 30729371, "q": 33434981},
        {"case_id": "rsa_v2_64bit_static_001", "bits": 64, "N": 10376454699372036973, "p": 3221225473, "q": 3221275501},
    ]

    for t in official + ADDITIONAL_TRIPLES:
        gap_N = compute_position_aware_state(t["N"])

        row = {
            "case_id": t["case_id"],
            "bits": t["bits"],
            "N": t["N"],
            "p": t["p"],
            "q": t["q"],
            "gap_N_state": gap_N.reduced_state,
            "gap_N_bucket": gap_N.position_bucket,
            "gap_N_rel_pos": gap_N.relative_position,
            "gap_N_width": gap_N.gap_width,
        }
        all_results.append(row)

        print(f"{t['case_id']:<32} gap(N): {gap_N.reduced_state:<26} | {gap_N.position_bucket:<10} (pos={gap_N.relative_position})")

    # Save expanded results
    out = Path(__file__).parent / "output" / "gap_compatibility_expanded_corpus.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    print(f"\nExpanded corpus written to: {out}")
    print(f"Total cases: {len(all_results)}")


if __name__ == "__main__":
    main()
