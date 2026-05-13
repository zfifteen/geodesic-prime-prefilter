#!/usr/bin/env python3
"""Audit whether child closing primes cover the parent window directly."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_dynamic_tail_descent_audit import build_dynamic_tail_descent_audit  # noqa: E402
from square_tail_rough_defect_audit import build_rough_defect_audit  # noqa: E402


RECORD_ROOT = 424_171_123
REPRESENTATIVE_SOURCE_ROOT = 509


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def parent_residue(parent_root: int, carrier: int) -> int:
    """Return the first positive parent m covered by carrier."""
    residue = (parent_root * parent_root * pow(2, -1, carrier)) % carrier
    return residue if residue != 0 else carrier


def child_prime_rows_for_child(child_root: int) -> list[dict[str, int]]:
    """Return prime-valued M-rough rows for one child root."""
    child = build_rough_defect_audit(child_root)
    rows = []
    for offset in child["rough_prime_defect_offsets"]:
        offset_int = int(offset)
        child_prime = child_root * child_root - offset_int
        rows.append(
            {
                "child_root": child_root,
                "child_prime_offset": offset_int,
                "child_prime": child_prime,
            }
        )
    return rows


def standing_record_child_roots() -> tuple[int, int, list[int]]:
    """Return parent root, parent M, and composite child roots for the record."""
    parent = build_rough_defect_audit(RECORD_ROOT)
    child_roots = [
        int(row["least_factor"])
        for row in parent["rough_rows"]
        if not bool(row["is_prime"])
    ]
    return RECORD_ROOT, int(parent["full_counterexample_even_count"]), child_roots


def representative_child_roots() -> tuple[int, int, list[int]]:
    """Return parent root, parent M, and composite child roots for the representative."""
    parent = build_dynamic_tail_descent_audit(REPRESENTATIVE_SOURCE_ROOT)
    child_roots = [
        int(row["least_factor"])
        for row in parent["rough_tail_rows"]
        if not bool(row["is_prime"])
    ]
    return int(parent["actual_root"]), int(parent["actual_M"]), child_roots


def audit_parent_surface(label: str, parent_root: int, parent_m: int, child_roots: list[int]) -> dict[str, object]:
    """Audit direct parent residues induced by child closing primes."""
    inside_rows = []
    checked_count = 0
    child_prime_row_count = 0
    for child_root in child_roots:
        child_rows = child_prime_rows_for_child(child_root)
        child_prime_row_count += len(child_rows)
        for child_row in child_rows:
            checked_count += 1
            residue = parent_residue(parent_root, int(child_row["child_prime"]))
            if residue <= parent_m:
                inside_rows.append(
                    {
                        **child_row,
                        "parent_residue_m": residue,
                        "parent_residue_offset": 2 * residue,
                    }
                )
    return {
        "label": label,
        "parent_root": str(parent_root),
        "parent_M": parent_m,
        "composite_child_root_count": len(child_roots),
        "child_prime_row_count": child_prime_row_count,
        "parent_residue_rows_checked": checked_count,
        "inside_parent_M_count": len(inside_rows),
        "outside_parent_M_count": checked_count - len(inside_rows),
        "first_inside_parent_M_rows": inside_rows[:20],
    }


def build_child_closure_parent_residue_audit() -> dict[str, object]:
    """Return direct child-closure parent-residue audit data."""
    record_parent_root, record_m, record_children = standing_record_child_roots()
    representative_parent_root, representative_m, representative_children = (
        representative_child_roots()
    )
    surfaces = [
        audit_parent_surface(
            "standing_record_actual_composite_rough_children",
            record_parent_root,
            record_m,
            record_children,
        ),
        audit_parent_surface(
            "representative_actual_composite_rough_tail_children",
            representative_parent_root,
            representative_m,
            representative_children,
        ),
    ]
    return {
        "all_child_closing_prime_residues_outside_parent_M": all(
            int(surface["inside_parent_M_count"]) == 0 for surface in surfaces
        ),
        "boundary": (
            "child closing primes do not directly cover the measured parent "
            "windows, so direct back-cover is not the missing transport law"
        ),
        "surfaces": surfaces,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the direct child-closure parent-residue audit."""
    args = build_parser().parse_args(argv)
    payload = build_child_closure_parent_residue_audit()
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
