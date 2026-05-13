#!/usr/bin/env python3
"""Measure exact chamber grammar for low solved RSA challenge labels."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = THIS_DIR.parents[1]
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
RULE_ID = "rsa_challenge_exact_grammar_evidence_v1"
FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
CLOSED_RESIDUES = {0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27}
TRIAL_PRIME_LIMIT = 1_000_000
GP_TIMEOUT_SECONDS = 5


def small_primes(limit: int) -> list[int]:
    """Return every prime up to one small trial limit."""
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    root = math.isqrt(limit)
    for candidate in range(2, root + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start : limit + 1 : candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    return [index for index, is_prime in enumerate(sieve) if is_prime]


TRIAL_PRIMES = small_primes(TRIAL_PRIME_LIMIT)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def previous_prime(value: int) -> int:
    """Return the previous prime endpoint at or below one coordinate."""
    candidate = value if value % 2 else value - 1
    while candidate >= 2:
        if gmpy2.is_prime(candidate):
            return candidate
        candidate -= 2
    raise ValueError(f"no previous prime found for {value}")


def next_prime(value: int) -> int:
    """Return the next prime endpoint at or above one coordinate."""
    if value <= 2:
        return 2
    candidate = value if value % 2 else value + 1
    while True:
        if gmpy2.is_prime(candidate):
            return candidate
        candidate += 2


def first_open_offset(left_endpoint: int) -> int:
    """Return the first wheel-open even offset after one endpoint."""
    residue = left_endpoint % 30
    for offset in FIRST_OPEN_OFFSETS:
        if (residue + offset) % 30 not in CLOSED_RESIDUES:
            return offset
    raise RuntimeError(f"no open offset found after residue {residue}")


def reduced_state(first_open: int, divisor_count: int, value: int) -> str:
    """Return the reduced grammar state for one selected carrier."""
    if divisor_count == 3:
        family = "prime_square"
    elif divisor_count == 4 and value % 2 == 0:
        family = "d4_even"
    elif divisor_count == 4:
        family = "d4_odd"
    elif value % 2 == 0:
        family = "higher_divisor_even"
    else:
        family = "higher_divisor_odd"
    if divisor_count <= 4:
        bucket = "d<=4"
    elif divisor_count <= 16:
        bucket = "5<=d<=16"
    elif divisor_count <= 64:
        bucket = "17<=d<=64"
    else:
        bucket = "d>64"
    return f"o{first_open}_{family}|{bucket}"


def exact_type_key(first_open: int, divisor_count: int, offset: int, value: int) -> str:
    """Return the exact grammar key for one selected carrier."""
    if divisor_count == 3:
        family = "prime_square"
    elif divisor_count == 4 and value % 2 == 0:
        family = "d4_even"
    elif divisor_count == 4:
        family = "d4_odd"
    elif value % 2 == 0:
        family = "higher_divisor_even"
    else:
        family = "higher_divisor_odd"
    return f"o{first_open}_d{divisor_count}_a{offset}_{family}"


def low_divisor_count(value: int) -> int | None:
    """Return exact d<=4, a known >4 sentinel, or unresolved."""
    root = math.isqrt(value)
    if root * root == value and gmpy2.is_prime(root):
        return 3

    residual = value
    count = 1
    for prime in TRIAL_PRIMES:
        if prime * prime > residual:
            break
        if residual % prime == 0:
            exponent = 0
            while residual % prime == 0:
                residual //= prime
                exponent += 1
            count *= exponent + 1
            if count > 4:
                return 5

    if residual == 1:
        return count
    if gmpy2.is_prime(residual):
        return count * 2
    root = math.isqrt(residual)
    if root * root == residual and gmpy2.is_prime(root):
        return count * 3
    if count > 1:
        return 5
    return None


def gp_numdiv(value: int) -> int | None:
    """Return one exact divisor count from PARI/GP, or unresolved on timeout."""
    completed = subprocess.run(
        ["gp", "-q"],
        input=f"print(numdiv({value}));\n\\q\n",
        text=True,
        capture_output=True,
        timeout=GP_TIMEOUT_SECONDS,
        check=False,
    )
    if completed.returncode != 0:
        return None
    output = completed.stdout.strip()
    return None if not output else int(output)


def bounded_gp_numdiv(value: int) -> int | None:
    """Return one exact divisor count while preserving explicit unresolved state."""
    try:
        return gp_numdiv(value)
    except subprocess.TimeoutExpired:
        return None


def select_needed_offsets(
    best_count: int | None,
    best_offset: int | None,
    unresolved_offsets: list[int],
    unresolved_values: list[int],
) -> list[tuple[int, int]]:
    """Return unresolved coordinates that can still alter the chamber grammar."""
    if best_count in (3, 4) and best_offset is not None:
        return [
            (offset, value)
            for offset, value in zip(unresolved_offsets, unresolved_values)
            if offset < best_offset
        ]
    return list(zip(unresolved_offsets, unresolved_values))


def resolve_unresolved_offsets(
    needed: list[tuple[int, int]],
    best_count: int | None,
    best_offset: int | None,
    best_value: int | None,
) -> tuple[int | None, int | None, int | None, list[int]]:
    """Resolve needed offsets exactly where possible and report open offsets."""
    open_offsets: list[int] = []
    for offset, value in needed:
        divisor_count = bounded_gp_numdiv(value)
        if divisor_count is None:
            open_offsets.append(offset)
            continue
        if (
            best_count is None
            or divisor_count < best_count
            or (divisor_count == best_count and offset < best_offset)
        ):
            best_count = divisor_count
            best_offset = offset
            best_value = value
    return best_count, best_offset, best_value, open_offsets


def gap_grammar(role: str, left_endpoint: int, right_endpoint: int) -> dict[str, object]:
    """Return exact grammar for one adjacent-prime chamber."""
    first_open = first_open_offset(left_endpoint)
    best_offset: int | None = None
    best_count: int | None = None
    best_value: int | None = None
    unresolved_values: list[int] = []
    unresolved_offsets: list[int] = []

    for offset in range(1, right_endpoint - left_endpoint):
        value = left_endpoint + offset
        divisor_count = low_divisor_count(value)
        if divisor_count is None:
            unresolved_values.append(value)
            unresolved_offsets.append(offset)
            continue
        if (
            best_count is None
            or divisor_count < best_count
            or (divisor_count == best_count and offset < best_offset)
        ):
            best_count = divisor_count
            best_offset = offset
            best_value = value
        if best_count in (3, 4):
            break

    needed = select_needed_offsets(best_count, best_offset, unresolved_offsets, unresolved_values)
    best_count, best_offset, best_value, open_offsets = resolve_unresolved_offsets(
        needed,
        best_count,
        best_offset,
        best_value,
    )

    if best_count is None or best_offset is None or best_value is None:
        raise RuntimeError(f"empty chamber for {role}")

    status = "exact_closed" if not open_offsets else "unresolved_prior_carrier"
    unresolved_reason = (
        None
        if not open_offsets
        else "requires_gwr_nlsc_prior_carrier_elimination"
    )

    return {
        "role": role,
        "status": status,
        "unresolved_reason": unresolved_reason,
        "left_endpoint": str(left_endpoint),
        "right_endpoint": str(right_endpoint),
        "gap_width": right_endpoint - left_endpoint,
        "winner_value": str(best_value),
        "winner_offset": best_offset,
        "winner_d": best_count,
        "unresolved_offsets": open_offsets,
        "exact_type_key": exact_type_key(first_open, best_count, best_offset, best_value),
        "reduced_state": reduced_state(first_open, best_count, best_value),
    }


def public_rows(case: dict[str, object]) -> list[dict[str, object]]:
    """Return public N grammar rows for one solved RSA label."""
    n_value = int(str(case["n"]))
    left = previous_prime(n_value - 1)
    right = next_prime(n_value + 1)
    previous = previous_prime(left - 1)
    following = next_prime(right + 1)
    gaps = [
        gap_grammar("n_previous", previous, left),
        gap_grammar("n_containing", left, right),
        gap_grammar("n_following", right, following),
    ]
    return [
        {
            "case_id": case["case_id"],
            "bits": case["bits"],
            "rule_id": RULE_ID,
            "anchor": "N",
            **gap,
        }
        for gap in gaps
    ]


def target_rows(case: dict[str, object]) -> list[dict[str, object]]:
    """Return downstream p/q target-side grammar rows for one solved RSA label."""
    rows: list[dict[str, object]] = []
    for side in ("p", "q"):
        value = int(str(case[side]))
        left = previous_prime(value - 1)
        right = next_prime(value + 1)
        for gap in (
            gap_grammar(f"{side}_left", left, value),
            gap_grammar(f"{side}_right", value, right),
        ):
            rows.append(
                {
                    "case_id": case["case_id"],
                    "bits": case["bits"],
                    "rule_id": RULE_ID,
                    "target_side": side,
                    **gap,
                }
            )
    return rows


def summarize(public: list[dict[str, object]], target: list[dict[str, object]]) -> dict[str, object]:
    """Return compact exact grammar evidence counts."""
    outward = sum(
        1
        for row in target
        if (
            (row["role"] == "p_left" or row["role"] == "q_right")
            and "higher_divisor" in str(row["reduced_state"])
        )
    )
    inward = sum(
        1
        for row in target
        if (
            (row["role"] == "p_right" or row["role"] == "q_left")
            and "higher_divisor" in str(row["reduced_state"])
        )
    )
    return {
        "rule_id": RULE_ID,
        "case_count": len({row["case_id"] for row in public}),
        "public_row_count": len(public),
        "target_row_count": len(target),
        "n_containing_higher_count": sum(
            1
            for row in public
            if row["role"] == "n_containing" and "higher_divisor" in str(row["reduced_state"])
        ),
        "public_unresolved_row_count": sum(1 for row in public if row["status"] != "exact_closed"),
        "target_unresolved_row_count": sum(1 for row in target if row["status"] != "exact_closed"),
        "outward_higher_count": outward,
        "inward_higher_count": inward,
        "outward_fraction": None if outward + inward == 0 else outward / (outward + inward),
        "outward_intrusion_index": None if inward == 0 else outward / inward,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Measure exact solved RSA challenge grammar.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "solved_rsa_challenge_cases.jsonl",
        help="Solved RSA challenge labels.",
    )
    parser.add_argument(
        "--case-limit",
        type=int,
        default=1,
        help="Number of smallest solved RSA rows to measure.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "rsa_challenge_exact_grammar",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the exact solved RSA grammar measurement."""
    args = parse_args(argv)
    cases = read_jsonl(args.cases)[: args.case_limit]
    public: list[dict[str, object]] = []
    target: list[dict[str, object]] = []
    for case in cases:
        public.extend(public_rows(case))
        target.extend(target_rows(case))
    summary = summarize(public, target)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "public_grammar_rows.jsonl", public)
    write_jsonl(args.output_dir / "target_grammar_rows.jsonl", target)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
