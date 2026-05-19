#!/usr/bin/env python3
"""Run only the new reciprocal-shadow ladder rungs from 52 through 64 bits."""

from __future__ import annotations

import json
import math
from pathlib import Path


FIXED_RADIUS = 300
BIT_RUNGS = [52, 56, 60, 64]
P_ROOT_NUMERATOR = 97
P_ROOT_DENOMINATOR = 100
MR_BASES_64 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "reciprocal_shadow_vote_ladder_64_new_rungs"


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
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
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
        divisor = 1
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


def segmented_prime_flags(low: int, high: int) -> bytearray:
    size = high - low + 1
    flags = bytearray(b"\x01") * size
    for prime in simple_sieve(math.isqrt(high)):
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
    heldout_rows = [
        row
        for row in rows
        if p_value not in row["factors"] and q_value not in row["factors"]
    ]
    direct_rows_removed = len(rows) - len(heldout_rows)
    sqrt_n = math.isqrt(n_value)
    flags = segmented_prime_flags(p_value, sqrt_n)
    streamed_candidates = 0
    for offset in range(len(flags) - 1, -1, -1):
        if not flags[offset]:
            continue
        candidate = p_value + offset
        streamed_candidates += 1
        partner_estimate = round(n_value / candidate)
        if candidate not in {p_value, q_value} and partner_estimate not in {p_value, q_value}:
            continue
        score = reciprocal_shadow_score(n_value, candidate, heldout_rows)
        hit_factor = candidate if candidate in {p_value, q_value} else partner_estimate
        return {
            **case,
            "radius": FIXED_RADIUS,
            "composite_rows": len(rows),
            "heldout_rows": len(heldout_rows),
            "direct_rows_removed": direct_rows_removed,
            "sqrt_N": sqrt_n,
            "streamed_candidates_until_hit": streamed_candidates,
            "hit_factor": hit_factor,
            "hit_candidate": candidate,
            "hit_partner_estimate": score["partner_estimate"],
            "hit_votes": score["votes"],
            "hit_hits": score["hits"],
            "hit_skipped": score["skipped"],
            "hit_coherence": score["coherence"],
            "one_factor_success": True,
        }
    return {
        **case,
        "radius": FIXED_RADIUS,
        "composite_rows": len(rows),
        "heldout_rows": len(heldout_rows),
        "direct_rows_removed": direct_rows_removed,
        "sqrt_N": sqrt_n,
        "streamed_candidates_until_hit": streamed_candidates,
        "one_factor_success": False,
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_summary(path: Path, rows: list[dict[str, object]]) -> None:
    lines = [
        "# Reciprocal Shadow Vote 64-Bit New Rungs",
        "",
        "## Contract",
        "",
        "This run tests only the new rungs above the existing 48-bit ladder.",
        "The reciprocal-shadow score and fixed observation radius are unchanged.",
        f"The radius is `{FIXED_RADIUS}` and the lower audit factor is built at",
        f"`{P_ROOT_NUMERATOR} / {P_ROOT_DENOMINATOR}` of the target square-root scale.",
        "",
        "Each rung streams prime lower-endpoint candidates downward from",
        "`floor(sqrt(N))` and stops at the first audit hit on either hidden",
        "factor. One factor is the success condition.",
        "",
        "## Results",
        "",
        "| bits | N | p | q | hit factor | hit candidate | streamed until hit | coherence | heldout rows | direct rows removed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {bits} | {N} | {p} | {q} | {hit_factor} | {hit_candidate} | "
            "{streamed_candidates_until_hit} | {hit_coherence:.6f} | "
            "{heldout_rows} | {direct_rows_removed} |".format(**row)
        )
    successes = sum(1 for row in rows if row["one_factor_success"])
    lines.extend(
        [
            "",
            "## Measured Surface",
            "",
            "```text",
            f"new_rungs = {len(rows)}",
            f"one_factor_success = {successes} / {len(rows)}",
            f"max_bits = {max(int(row['bits']) for row in rows)}",
            f"fixed_radius = {FIXED_RADIUS}",
            "```",
            "",
            "## Boundary",
            "",
            "This is a measured new-rung extension of the indirect-web hypothesis.",
            "It is not a universal theorem and not a live factor resolver.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cases = [build_case(bits) for bits in BIT_RUNGS]
    rows = [run_case(case) for case in cases]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_jsonl(OUTPUT_DIR / "rungs.jsonl", rows)
    write_summary(OUTPUT_DIR / "summary.md", rows)


if __name__ == "__main__":
    main()
