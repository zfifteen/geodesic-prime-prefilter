#!/usr/bin/env python3
"""Run the reciprocal-shadow one-factor ladder through 48-bit semiprimes."""

from __future__ import annotations

import json
import math
from pathlib import Path


FIXED_RADIUS = 300
BIT_RUNGS = [16, 20, 24, 28, 32, 36, 40, 44, 48]
MAX_BITS = 48
P_ROOT_NUMERATOR = 97
P_ROOT_DENOMINATOR = 100
SIEVE_LIMIT = math.isqrt(1 << MAX_BITS) + 1000
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "reciprocal_shadow_vote_ladder_48"


def prime_sieve(limit: int) -> tuple[list[int], bytearray]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for value in range(4, limit + 1, 2):
        flags[value] = 0
    for value in range(3, math.isqrt(limit) + 1, 2):
        if flags[value]:
            start = value * value
            step = value * 2
            flags[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [2] + [value for value in range(3, limit + 1, 2) if flags[value]], flags


def previous_prime_at_or_below(value: int, flags: bytearray) -> int:
    candidate = min(value, len(flags) - 1)
    while candidate >= 2:
        if flags[candidate]:
            return candidate
        candidate -= 1
    raise ValueError("no previous prime")


def next_prime_at_or_above(value: int, flags: bytearray) -> int:
    candidate = max(2, value)
    while candidate < len(flags):
        if flags[candidate]:
            return candidate
        candidate += 1
    raise ValueError("sieve limit too small")


def factorization_with_primes(value: int, primes: list[int]) -> dict[int, int]:
    remaining = value
    factors: dict[int, int] = {}
    for prime in primes:
        if prime * prime > remaining:
            break
        while remaining % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            remaining //= prime
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def divisor_count(factors: dict[int, int]) -> int:
    total = 1
    for exponent in factors.values():
        total *= exponent + 1
    return total


def build_case(bits: int, flags: bytearray) -> dict[str, int]:
    target = 1 << (bits - 1)
    root = math.isqrt(target)
    p_target = (root * P_ROOT_NUMERATOR) // P_ROOT_DENOMINATOR
    p_value = previous_prime_at_or_below(p_target, flags)
    q_start = (target + p_value - 1) // p_value
    q_value = next_prime_at_or_above(q_start, flags)
    n_value = p_value * q_value
    if n_value.bit_length() != bits:
        raise ValueError(f"failed to construct {bits}-bit semiprime")
    return {"bits": bits, "p": p_value, "q": q_value, "N": n_value}


def composite_rows(n_value: int, radius: int, primes: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for value in range(n_value - radius, n_value + radius + 1):
        if value < 4 or value == n_value:
            continue
        factors = factorization_with_primes(value, primes)
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


def reciprocal_shadow_score(n_value: int, candidate: int, rows: list[dict[str, object]]) -> dict[str, object]:
    partner_estimate = round(n_value / candidate)
    votes = 0
    hits = 0
    skipped = 0
    for row in rows:
        offset = int(row["offset"])
        for factor in row["factors"]:
            r = int(factor)
            if math.gcd(candidate, r) != 1:
                skipped += 1
                continue
            implied_partner_residue = ((-offset) * pow(candidate % r, -1, r)) % r
            votes += 1
            if partner_estimate % r == implied_partner_residue:
                hits += 1
    return {
        "candidate": candidate,
        "partner_estimate": partner_estimate,
        "votes": votes,
        "hits": hits,
        "skipped": skipped,
        "coherence": 0.0 if votes == 0 else hits / votes,
    }


def run_case(case: dict[str, int], primes: list[int], flags: bytearray) -> dict[str, object]:
    n_value = case["N"]
    p_value = case["p"]
    q_value = case["q"]
    rows = composite_rows(n_value, FIXED_RADIUS, primes)
    heldout_rows = [
        row
        for row in rows
        if p_value not in row["factors"] and q_value not in row["factors"]
    ]
    direct_rows_removed = len(rows) - len(heldout_rows)
    sqrt_n = math.isqrt(n_value)
    candidate = previous_prime_at_or_below(sqrt_n, flags)
    scored_candidates = 0
    while candidate >= 2:
        score = reciprocal_shadow_score(n_value, candidate, heldout_rows)
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
                "heldout_rows": len(heldout_rows),
                "direct_rows_removed": direct_rows_removed,
                "sqrt_N": sqrt_n,
                "candidate_count_below_sqrt": sum(1 for prime in primes if prime <= sqrt_n),
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
        candidate = previous_prime_at_or_below(candidate - 1, flags)
    return {
        **case,
        "radius": FIXED_RADIUS,
        "composite_rows": len(rows),
        "heldout_rows": len(heldout_rows),
        "direct_rows_removed": direct_rows_removed,
        "sqrt_N": sqrt_n,
        "candidate_count_below_sqrt": sum(1 for prime in primes if prime <= sqrt_n),
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
        "# Reciprocal Shadow Vote 48-Bit Ladder",
        "",
        "## Contract",
        "",
        "The ladder keeps the reciprocal-shadow score and the fixed observation",
        f"radius `{FIXED_RADIUS}`. Only `N = p q` changes across rungs.",
        f"The lower audit factor is constructed at `{P_ROOT_NUMERATOR} / "
        f"{P_ROOT_DENOMINATOR}` of the target square-root scale.",
        "",
        "Each rung streams prime lower-endpoint candidates downward from",
        "`floor(sqrt(N))` and stops at the first audit hit on either hidden",
        "factor. One factor is the success condition.",
        "",
        "## Results",
        "",
        "| bits | N | p | q | hit factor | hit candidate | scored until hit | candidates below sqrt | coherence | heldout rows | direct rows removed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {bits} | {N} | {p} | {q} | {hit_factor} | {hit_candidate} | "
            "{scored_candidates_until_hit} | {candidate_count_below_sqrt} | "
            "{hit_coherence:.6f} | {heldout_rows} | {direct_rows_removed} |".format(**row)
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
            "```",
            "",
            "## Boundary",
            "",
            "This is a measured ladder for the indirect-web hypothesis. It is not",
            "a universal theorem and not a live factor resolver.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    primes, flags = prime_sieve(SIEVE_LIMIT)
    cases = [build_case(bits, flags) for bits in BIT_RUNGS]
    rows = [run_case(case, primes, flags) for case in cases]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUTPUT_DIR / "rungs.jsonl", rows)
    write_summary(OUTPUT_DIR / "summary.md", rows)


if __name__ == "__main__":
    main()
