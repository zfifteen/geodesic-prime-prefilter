#!/usr/bin/env python3
"""Audit obstruction inheritance on full-cutoff local CRT assigned carriers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from sympy import primerange


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


def first_arrival_carriers(model: dict[str, object]) -> list[int]:
    """Return first-arrival carriers for every modeled rough row."""
    model_with_values = build_full_cutoff_crt_model(SOURCE_ROOT, include_model_values=True)
    root = int(model_with_values["model_residue"])
    limit = int(model["M"])
    rough = {int(row["m"]) for row in model["carrier_rows"]}
    last_assigned = int(model["last_assigned_carrier"])
    first_arrivals: dict[int, int] = {}
    for carrier in primerange(limit + 1, last_assigned + 1):
        carrier_int = int(carrier)
        residue = (root * root * pow(2, -1, carrier_int)) % carrier_int
        if 1 <= residue <= limit and residue in rough and residue not in first_arrivals:
            first_arrivals[residue] = carrier_int
    if len(first_arrivals) != len(rough):
        raise RuntimeError("first-arrival cover incomplete")
    return [first_arrivals[m] for m in sorted(rough)]


def carrier_summary(label: str, carriers: list[int]) -> dict[str, object]:
    """Return obstruction summary for a carrier family."""
    rows = [carrier_obstruction_row(root) for root in carriers]
    obstructed_rows = [row for row in rows if bool(row["O_holds"])]
    prime_counts = [int(row["rough_prime_defect_count"]) for row in rows]
    return {
        "label": label,
        "carrier_count": len(carriers),
        "distinct_carrier_count": len(set(carriers)),
        "carriers_with_O_count": len(obstructed_rows),
        "carriers_closed_count": len(rows) - len(obstructed_rows),
        "all_carriers_closed": len(obstructed_rows) == 0,
        "min_carrier_rough_prime_defect_count": min(prime_counts) if prime_counts else None,
        "max_carrier_rough_prime_defect_count": max(prime_counts) if prime_counts else None,
        "first_carrier_rows": rows[:20],
        "obstructed_carrier_rows": obstructed_rows,
    }


def build_local_model_inheritance_audit() -> dict[str, object]:
    """Return obstruction-inheritance data for the local CRT carrier families."""
    model = build_full_cutoff_crt_model(SOURCE_ROOT)
    carriers = [int(row["carrier"]) for row in model["carrier_rows"]]
    first_arrivals = first_arrival_carriers(model)
    assigned_summary = carrier_summary("assigned_singleton_carriers", carriers)
    first_arrival_summary = carrier_summary("first_arrival_carriers", first_arrivals)
    return {
        "source_root": SOURCE_ROOT,
        "representative_root": model["representative_root"],
        "parent_local_model_consistent": model["local_model_consistent"],
        "parent_rough_defect_count": model["rough_defect_count"],
        "assigned_carrier_count": assigned_summary["carrier_count"],
        "assigned_carriers_with_O_count": assigned_summary["carriers_with_O_count"],
        "all_assigned_carriers_closed": assigned_summary["all_carriers_closed"],
        "first_arrival_carrier_count": first_arrival_summary["carrier_count"],
        "first_arrival_distinct_carrier_count": first_arrival_summary[
            "distinct_carrier_count"
        ],
        "first_arrival_carriers_with_O_count": first_arrival_summary[
            "carriers_with_O_count"
        ],
        "all_first_arrival_carriers_closed": first_arrival_summary[
            "all_carriers_closed"
        ],
        "least_factor_boundary": (
            "first-arrival carriers are local least-factor analogues, but the model "
            "root is not an actual prime-root theorem instance"
        ),
        "boundary": (
            "local CRT complete carrier cover does not force obstruction on assigned "
            "or first-arrival carriers; all such carriers are closed"
        ),
        "carrier_summaries": [assigned_summary, first_arrival_summary],
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
