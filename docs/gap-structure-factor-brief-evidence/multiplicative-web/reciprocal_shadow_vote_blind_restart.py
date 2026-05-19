#!/usr/bin/env python3
"""Restart the reciprocal-shadow ladder under a blind inference contract."""

from __future__ import annotations

import json
import math
from pathlib import Path


FIXED_RADIUS = 300
BIT_RUNGS = [20, 24, 28, 32, 36, 40, 44, 48, 52]
P_ROOT_NUMERATOR = 97
P_ROOT_DENOMINATOR = 100
SEGMENT_SIZE = 1_000_000
MR_BASES_64 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "reciprocal_shadow_vote_blind_restart"


def simple_sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for value in range(4, limit + 1, 2):
        flags[value] = 0
    for value in range(3, math.isqrt(limit) + 1, 2):
        if flags[value]:
            start = value * value
            step = value * 2
            flags[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [2] + [value for value in range(3, limit + 1, 2) if flags[value]]


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for prime in MR_BASES_64:
        if value == prime:
            return True
        if value % prime == 0:
            return False

    odd_part = value - 1
    shifts = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shifts += 1

    for base in MR_BASES_64:
        if base >= value:
            continue
        witness = pow(base, odd_part, value)
        if witness in {1, value - 1}:
            continue
        for _ in range(shifts - 1):
            witness = (witness * witness) % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def previous_prime_at_or_below(value: int) -> int:
    candidate = value if value % 2 else value - 1
    while candidate >= 3:
        if is_prime(candidate):
            return candidate
        candidate -= 2
    return 2


def next_prime_at_or_above(value: int) -> int:
    if value <= 2:
        return 2
    candidate = value if value % 2 else value + 1
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 2


def deterministic_factor(value: int) -> int:
    if value % 2 == 0:
        return 2
    if value % 3 == 0:
        return 3
    for constant in range(1, 65):
        x_value = 2
        y_value = 2
        for _ in range(200000):
            x_value = (x_value * x_value + constant) % value
            y_value = (y_value * y_value + constant) % value
            y_value = (y_value * y_value + constant) % value
            divisor = math.gcd(abs(x_value - y_value), value)
            if divisor == 1:
                continue
            if divisor != value:
                return divisor
            break
    raise ValueError(f"deterministic factorization did not split {value}")


def add_factor(value: int, factors: dict[int, int]) -> None:
    if value == 1:
        return
    if is_prime(value):
        factors[value] = factors.get(value, 0) + 1
        return
    divisor = deterministic_factor(value)
    add_factor(divisor, factors)
    add_factor(value // divisor, factors)


def factorization(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    add_factor(value, factors)
    return dict(sorted(factors.items()))


def divisor_count(factors: dict[int, int]) -> int:
    total = 1
    for exponent in factors.values():
        total *= exponent + 1
    return total


def build_case(bits: int) -> dict[str, int]:
    target = 1 << (bits - 1)
    root = math.isqrt(target)
    p_target = (root * P_ROOT_NUMERATOR) // P_ROOT_DENOMINATOR
    p_value = previous_prime_at_or_below(p_target)
    q_start = (target + p_value - 1) // p_value
    q_value = next_prime_at_or_above(q_start)
    n_value = p_value * q_value
    if n_value.bit_length() != bits:
        raise ValueError(f"failed to construct {bits}-bit semiprime")
    return {"bits": bits, "p": p_value, "q": q_value, "N": n_value}


def composite_rows(n_value: int, radius: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for value in range(n_value - radius, n_value + radius + 1):
        if value < 4 or value == n_value:
            continue
        factors = factorization(value)
        if len(factors) == 1 and factors.get(value) == 1:
            continue
        rows.append(
            {
                "value": value,
                "offset": value - n_value,
                "factors": factors,
                "divisor_count": divisor_count(factors),
            }
        )
    return rows


def flatten_threads(rows: list[dict[str, object]]) -> list[tuple[int, int]]:
    threads: list[tuple[int, int]] = []
    for row in rows:
        offset = int(row["offset"])
        for factor in row["factors"]:
            threads.append((offset, int(factor)))
    return threads


def reciprocal_shadow_score(n_value: int, candidate: int, threads: list[tuple[int, int]]) -> dict[str, object]:
    quotient, remainder = divmod(n_value, candidate)
    partner_estimate = quotient + int(2 * remainder >= candidate)
    votes = 0
    hits = 0
    skipped = 0
    for offset, r_value in threads:
        if candidate == r_value:
            skipped += 1
            continue
        votes += 1
        if (candidate * partner_estimate + offset) % r_value == 0:
            hits += 1
    return {
        "candidate": candidate,
        "partner_estimate": partner_estimate,
        "votes": votes,
        "hits": hits,
        "skipped": skipped,
        "coherence": 0.0 if votes == 0 else hits / votes,
    }


def segmented_prime_flags(low: int, high: int, base_primes: list[int]) -> bytearray:
    size = high - low + 1
    flags = bytearray(b"\x01") * size
    for prime in base_primes:
        if prime * prime > high:
            break
        start = max(prime * prime, ((low + prime - 1) // prime) * prime)
        if start > high:
            continue
        flags[start - low : size : prime] = b"\x00" * (((high - start) // prime) + 1)
    for value in range(low, min(high, 1) + 1):
        flags[value - low] = 0
    return flags


def run_case(case: dict[str, int]) -> dict[str, object]:
    n_value = case["N"]
    p_value = case["p"]
    q_value = case["q"]
    rows = composite_rows(n_value, FIXED_RADIUS)
    threads = flatten_threads(rows)
    sqrt_n = math.isqrt(n_value)
    base_primes = simple_sieve(math.isqrt(sqrt_n) + 1)
    high = sqrt_n
    scored_candidates = 0
    segment_count = 0
    while high >= 2:
        low = max(2, high - SEGMENT_SIZE + 1)
        flags = segmented_prime_flags(low, high, base_primes)
        segment_count += 1
        for offset in range(len(flags) - 1, -1, -1):
            if not flags[offset]:
                continue
            candidate = low + offset
            score = reciprocal_shadow_score(n_value, candidate, threads)
            scored_candidates += 1
            hit_factor = None
            if candidate in {p_value, q_value}:
                hit_factor = candidate
            elif score["partner_estimate"] in {p_value, q_value}:
                hit_factor = score["partner_estimate"]
            if hit_factor is not None:
                return {
                    **case,
                    "radius": FIXED_RADIUS,
                    "composite_rows": len(rows),
                    "thread_count": len(threads),
                    "direct_rows_containing_audit_factor": sum(
                        1 for row in rows if p_value in row["factors"] or q_value in row["factors"]
                    ),
                    "sqrt_N": sqrt_n,
                    "segments_read": segment_count,
                    "scored_candidates_until_hit": scored_candidates,
                    "hit_factor": hit_factor,
                    "hit_candidate": candidate,
                    "hit_partner_estimate": score["partner_estimate"],
                    "hit_votes": score["votes"],
                    "hit_hits": score["hits"],
                    "hit_skipped": score["skipped"],
                    "hit_coherence": score["coherence"],
                    "one_factor_success": True,
                }
        high = low - 1
    return {
        **case,
        "radius": FIXED_RADIUS,
        "composite_rows": len(rows),
        "thread_count": len(threads),
        "sqrt_N": sqrt_n,
        "segments_read": segment_count,
        "scored_candidates_until_hit": scored_candidates,
        "one_factor_success": False,
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_summary(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Reciprocal Shadow Vote Blind Restart",
        "",
        "## Contract",
        "",
        "This restart uses `p` and `q` only for case construction and final audit.",
        "The candidate stream begins at public `floor(sqrt(N))`, scans downward",
        "in fixed public segments, scores every prime candidate it sees, and",
        "stops only after a scored candidate has been checked against the audit",
        "factors.",
        "",
        "No hidden factor is used as a candidate bound, filter, or scoring input.",
        "",
        "## Results",
        "",
        "| bits | N | hit factor | hit candidate | scored until hit | segments | coherence | rows | threads | direct audit rows |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {bits} | {N} | {hit_factor} | {hit_candidate} | "
            "{scored_candidates_until_hit} | {segments_read} | {hit_coherence:.6f} | "
            "{composite_rows} | {thread_count} | {direct_rows_containing_audit_factor} |".format(**row)
        )
    successes = sum(1 for row in rows if row["one_factor_success"])
    lines.extend(
        [
            "",
            "## Measured Surface",
            "",
            "```text",
            f"rungs = {len(rows)}",
            f"one_factor_success = {successes} / {len(rows)}",
            f"max_bits = {max(int(row['bits']) for row in rows)}",
            f"fixed_radius = {FIXED_RADIUS}",
            "candidate_lower_bound = public scan to 2",
            "hidden_factor_candidate_bound = none",
            "```",
            "",
            "## Boundary",
            "",
            "This is a blind restart of the measured ladder. It still uses",
            "candidate enumeration and exact neighboring-composite factorization,",
            "so it is not a scalable resolver.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = [run_case(build_case(bits)) for bits in BIT_RUNGS]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUTPUT_DIR / "rungs.jsonl", rows)
    write_summary(OUTPUT_DIR / "summary.md", rows)


if __name__ == "__main__":
    main()
