#!/usr/bin/env python3
"""Audit obstruction inheritance on full-cutoff local CRT assigned carriers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_full_cutoff_crt_model import build_full_cutoff_crt_model  # noqa: E402
from square_tail_rough_defect_audit import build_rough_defect_audit  # noqa: E402


SOURCE_ROOT = 509


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def carrier_obstruction_row(root: int) -> dict[str, object]:
    """Return obstruction status for one assigned carrier root."""
    audit = build_rough_defect_audit(root)
    return {
        "root": root,
        "M": audit["full_counterexample_even_count"],
        "rough_defect_count": audit["rough_defect_count"],
        "rough_prime_defect_count": audit["rough_prime_defect_count"],
        "closed_by_rough_prime_defect": audit["closed_by_rough_prime_defect"],
        "O_holds": not bool(audit["closed_by_rough_prime_defect"]),
    }


def build_local_model_inheritance_audit() -> dict[str, object]:
    """Return obstruction-inheritance data for the local CRT assigned carriers."""
    model = build_full_cutoff_crt_model(SOURCE_ROOT)
    carriers = [int(row["carrier"]) for row in model["carrier_rows"]]
    carrier_rows = [carrier_obstruction_row(root) for root in carriers]
    obstructed_rows = [row for row in carrier_rows if bool(row["O_holds"])]
    prime_counts = [int(row["rough_prime_defect_count"]) for row in carrier_rows]
    return {
        "source_root": SOURCE_ROOT,
        "representative_root": model["representative_root"],
        "parent_local_model_consistent": model["local_model_consistent"],
        "parent_rough_defect_count": model["rough_defect_count"],
        "assigned_carrier_count": len(carriers),
        "assigned_carriers_with_O_count": len(obstructed_rows),
        "assigned_carriers_closed_count": len(carrier_rows) - len(obstructed_rows),
        "all_assigned_carriers_closed": len(obstructed_rows) == 0,
        "min_assigned_carrier_rough_prime_defect_count": (
            min(prime_counts) if prime_counts else None
        ),
        "max_assigned_carrier_rough_prime_defect_count": (
            max(prime_counts) if prime_counts else None
        ),
        "least_factor_boundary": (
            "assigned carriers are congruence carriers, not certified least-factor "
            "children of the modeled rows"
        ),
        "boundary": (
            "local CRT complete carrier cover does not force obstruction on assigned "
            "carriers; all assigned carriers are closed"
        ),
        "first_assigned_carrier_rows": carrier_rows[:20],
        "obstructed_assigned_carrier_rows": obstructed_rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the local-model obstruction-inheritance audit."""
    args = build_parser().parse_args(argv)
    payload = build_local_model_inheritance_audit()
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
