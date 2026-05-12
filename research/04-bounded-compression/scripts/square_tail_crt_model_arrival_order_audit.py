#!/usr/bin/env python3
"""Audit first-arrival order inside a full-cutoff CRT model."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from sympy import primerange


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_full_cutoff_crt_model import build_full_cutoff_crt_model  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=int, required=True)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def build_arrival_order_audit(source_root: int) -> dict[str, object]:
    """Return first-arrival order data for the full-cutoff CRT model."""
    model = build_full_cutoff_crt_model(source_root, include_model_values=True)
    root = int(model["model_residue"])
    limit = int(model["M"])
    rough = {int(row["m"]) for row in model["carrier_rows"]}
    assigned_by_m = {
        int(row["m"]): int(row["carrier"])
        for row in model["carrier_rows"]
    }
    assigned_m_by_carrier = {
        int(row["carrier"]): int(row["m"])
        for row in model["carrier_rows"]
    }
    last_assigned = int(model["last_assigned_carrier"])
    last_assigned_m = assigned_m_by_carrier[last_assigned]
    last_assigned_value = root * root - 2 * last_assigned_m
    last_assigned_sqrt_boundary = math.isqrt(last_assigned_value)

    first_arrivals: dict[int, int] = {}
    for carrier in primerange(limit + 1, last_assigned + 1):
        carrier_int = int(carrier)
        residue = (root * root * pow(2, -1, carrier_int)) % carrier_int
        if 1 <= residue <= limit and residue in rough and residue not in first_arrivals:
            first_arrivals[residue] = carrier_int

    mismatches = []
    for m in sorted(rough):
        assigned = assigned_by_m[m]
        first = first_arrivals.get(m)
        if first != assigned:
            mismatches.append(
                {
                    "m": m,
                    "offset": 2 * m,
                    "assigned_carrier": assigned,
                    "first_arrival": first,
                }
            )

    return {
        "source_root": source_root,
        "M": limit,
        "rough_defect_count": len(rough),
        "last_assigned_carrier": last_assigned,
        "last_assigned_m": last_assigned_m,
        "last_assigned_offset": 2 * last_assigned_m,
        "last_assigned_sqrt_boundary_digits": len(str(last_assigned_sqrt_boundary)),
        "last_assigned_carrier_before_sqrt_boundary": (
            last_assigned < last_assigned_sqrt_boundary
        ),
        "first_arrived_by_last_assigned_count": len(first_arrivals),
        "unarrived_by_last_assigned_count": len(rough) - len(first_arrivals),
        "assigned_first_match_count": len(rough) - len(mismatches),
        "assigned_first_mismatch_count": len(mismatches),
        "first_mismatches": mismatches[:30],
    }


def main(argv: list[str] | None = None) -> int:
    """Run the CRT model arrival-order audit."""
    args = build_parser().parse_args(argv)
    payload = build_arrival_order_audit(args.source_root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
