#!/usr/bin/env python3
"""Audit first carrier arrivals for rough rows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sympy import primerange


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_cover_prime_class_audit import build_prime_class_audit  # noqa: E402
from square_tail_rough_defect_audit import repeat_capable_cover  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"
DEFAULT_MILESTONES = [5_000, 10_000, 20_000, 50_000, 100_000, 500_000, 1_000_000]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=int,
        required=True,
        help="Source root whose first prime CRT representative seeds the audit.",
    )
    parser.add_argument(
        "--arrival-bound",
        type=int,
        default=1_000_000,
        help="Largest prime carrier to scan for first arrivals.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def rough_positions(root: int, limit: int) -> list[int]:
    """Return positions not covered by repeat-capable carriers."""
    covered = repeat_capable_cover(root, limit)
    return [m for m in range(1, limit + 1) if m not in covered]


def first_arrivals(root: int, limit: int, arrival_bound: int) -> dict[int, int]:
    """Return first prime-carrier arrivals for rough positions up to arrival_bound."""
    rough = set(rough_positions(root, limit))
    arrivals: dict[int, int] = {}
    for carrier in primerange(limit + 1, arrival_bound + 1):
        carrier_int = int(carrier)
        residue = (root * root * pow(2, -1, carrier_int)) % carrier_int
        if 1 <= residue <= limit and residue in rough and residue not in arrivals:
            arrivals[residue] = carrier_int
    return arrivals


def build_arrival_frontier(source_root: int, arrival_bound: int = 1_000_000) -> dict[str, object]:
    """Return first-arrival frontier data for the source root's prime representative."""
    representative_audit = build_prime_class_audit(source_root)
    representative = representative_audit["first_prime_representative"]
    if representative is None:
        raise RuntimeError("prime representative required for carrier-arrival audit")

    root = int(representative["root"])
    limit = int(representative["dynamic_cutoff"]) // 2
    rough = rough_positions(root, limit)
    arrivals = first_arrivals(root, limit, arrival_bound)
    unhit = sorted(set(rough) - set(arrivals))
    milestones = [
        milestone for milestone in DEFAULT_MILESTONES if milestone <= arrival_bound
    ]

    return {
        "source_root": source_root,
        "representative_root": str(root),
        "M": limit,
        "dynamic_cutoff": int(representative["dynamic_cutoff"]),
        "arrival_bound": arrival_bound,
        "rough_defect_count": len(rough),
        "arrived_count": len(arrivals),
        "unarrived_count": len(unhit),
        "milestones": [
            {
                "carrier_bound": bound,
                "arrived_count": sum(
                    int(carrier <= bound) for carrier in arrivals.values()
                ),
                "unarrived_count": len(rough)
                - sum(int(carrier <= bound) for carrier in arrivals.values()),
            }
            for bound in milestones
        ],
        "closing_m": int(representative["closing_m"]),
        "closing_offset": int(representative["previous_prime_offset"]),
        "closing_row_arrival": arrivals.get(int(representative["closing_m"])),
        "first_unarrived_offsets": [2 * m for m in unhit[:30]],
        "first_arrival_rows": [
            {
                "m": m,
                "offset": 2 * m,
                "first_carrier": arrivals[m],
            }
            for m in sorted(arrivals)[:30]
        ],
    }


def main(argv: list[str] | None = None) -> int:
    """Run the carrier-arrival frontier audit."""
    args = build_parser().parse_args(argv)
    payload = build_arrival_frontier(args.source_root, args.arrival_bound)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
