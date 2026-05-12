#!/usr/bin/env python3
"""Classify the dynamic tail beyond a source rough-cover model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2
from sympy import primerange


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_cover_model import build_cover_model  # noqa: E402
from square_tail_rough_cover_prime_class_audit import build_prime_class_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Root used to seed the CRT model.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def carrier_matches(m: int, rows: list[dict[str, object]]) -> list[int]:
    """Return assigned large carriers whose residue class covers m."""
    return [
        int(row["carrier"])
        for row in rows
        if m % int(row["carrier"]) == int(row["m"]) % int(row["carrier"])
    ]


def build_dynamic_tail_audit(root: int) -> dict[str, object]:
    """Return the dynamic-tail classification for one source CRT model."""
    model = build_cover_model(root)
    representative_audit = build_prime_class_audit(root)
    representative = representative_audit["first_prime_representative"]
    if representative is None:
        raise RuntimeError("prime representative required for dynamic-tail audit")

    source_m = int(model["M"])
    actual_root = int(representative["root"])
    actual_square = actual_root * actual_root
    closing_m = int(representative["closing_m"])
    actual_m = int(representative["dynamic_cutoff"]) // 2
    source_small_primes = [int(prime) for prime in primerange(3, source_m + 1)]
    actual_small_primes = [int(prime) for prime in primerange(3, actual_m + 1)]
    assigned_carriers = {int(row["carrier"]) for row in model["carrier_rows"]}
    source_modeled_carriers = set(source_small_primes) | assigned_carriers

    rows = []
    counts = {
        "tail_position_count": 0,
        "source_small_covered_count": 0,
        "source_assigned_large_covered_count": 0,
        "source_modeled_covered_count": 0,
        "new_repeat_capable_covered_count": 0,
        "actual_rough_count": 0,
        "prime_value_count": 0,
    }

    for m in range(source_m + 1, closing_m + 1):
        value = actual_square - 2 * m
        source_small = [
            prime for prime in source_small_primes if value % prime == 0
        ]
        source_large = carrier_matches(m, model["carrier_rows"])
        actual_small = [
            prime for prime in actual_small_primes if value % prime == 0
        ]
        new_repeat_capable = [
            prime for prime in actual_small if prime not in source_modeled_carriers
        ]
        is_prime = bool(gmpy2.is_prime(value))
        actual_rough = not actual_small

        counts["tail_position_count"] += 1
        counts["source_small_covered_count"] += int(bool(source_small))
        counts["source_assigned_large_covered_count"] += int(bool(source_large))
        counts["source_modeled_covered_count"] += int(bool(source_small or source_large))
        counts["new_repeat_capable_covered_count"] += int(bool(new_repeat_capable))
        counts["actual_rough_count"] += int(actual_rough)
        counts["prime_value_count"] += int(is_prime)

        if actual_rough or is_prime:
            rows.append(
                {
                    "m": m,
                    "offset": 2 * m,
                    "actual_rough": actual_rough,
                    "is_prime": is_prime,
                    "source_small_carriers": source_small,
                    "source_assigned_large_carriers": source_large,
                    "new_repeat_capable_carriers": new_repeat_capable,
                }
            )

    prime_rows = [row for row in rows if bool(row["is_prime"])]
    actual_rough_rows = [row for row in rows if bool(row["actual_rough"])]

    return {
        "source_root": root,
        "source_M": source_m,
        "actual_root": representative["root"],
        "actual_dynamic_cutoff": representative["dynamic_cutoff"],
        "actual_M": actual_m,
        "closing_m": closing_m,
        "closing_offset": 2 * closing_m,
        "tail_m_range": [source_m + 1, closing_m],
        "tail_even_offset_range": [2 * (source_m + 1), 2 * closing_m],
        "counts": counts,
        "actual_rough_offsets": [int(row["offset"]) for row in actual_rough_rows],
        "prime_offsets": [int(row["offset"]) for row in prime_rows],
        "prime_rows": prime_rows,
        "rough_or_prime_rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the dynamic-tail audit."""
    args = build_parser().parse_args(argv)
    payload = build_dynamic_tail_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
