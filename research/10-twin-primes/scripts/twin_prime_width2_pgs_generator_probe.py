#!/usr/bin/env python3
"""Probe the PGS chamber-reset contract specialized to width-2 chambers."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment
from z_band_prime_predictor.simple_pgs_generator import pgs_probe_certificate

DEFAULT_OUTPUT_DIR = ROOT / "research" / "10-twin-primes" / "output" / "twin_prime_width2_pgs_generator_probe"
DEFAULT_MAX_RIGHT_PRIME = 1_000_000
ELIGIBLE_RESIDUES = (11, 17, 29)
WIDTH2_BOUND = 2
STATUS_EXCLUDED = "excluded"
STATUS_UNRESOLVED = "unresolved"
ENDPOINT_PRIME_CLOSURE = "prime_closure"
ENDPOINT_COMPOSITE_OBSTRUCTION = "composite_obstruction"
KNOBS = (
    "pgs_width2_full",
    "endpoint_fixed_point",
    "endpoint_below_forced_load",
    "forced_interior_carrier",
)
GAP_TYPE_PROBE_PATH = Path(__file__).with_name("gwr_dni_gap_type_probe.py")


def load_gap_type_probe():
    """Load the experiment-local gap-type probe."""
    spec = importlib.util.spec_from_file_location("gwr_dni_gap_type_probe", GAP_TYPE_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load gwr_dni_gap_type_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GAP_TYPE_PROBE = load_gap_type_probe()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run the width-2 PGS chamber exclusion generator probe.",
    )
    parser.add_argument(
        "--max-right-prime",
        type=int,
        default=DEFAULT_MAX_RIGHT_PRIME,
        help="Largest eligible current prime q included in the probe.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated rows and audit artifacts.",
    )
    return parser


def divisor_count_at(n: int) -> int:
    """Return the exact divisor count at one integer."""
    return int(divisor_counts_segment(n, n + 1)[0])


def width2_record(q: int) -> dict[str, object]:
    """Emit one minimal width-2 PGS exclusion record."""
    q = int(q)
    if q % 30 not in ELIGIBLE_RESIDUES:
        raise ValueError(f"q={q} is not eligible for a width-2 chamber")

    candidate = q + 2
    certificate = pgs_probe_certificate(q, WIDTH2_BOUND)
    status = STATUS_UNRESOLVED
    if certificate is None:
        status = STATUS_EXCLUDED
    elif int(certificate["q"]) != candidate:
        raise RuntimeError(f"width-2 certificate resolved an unexpected endpoint for q={q}")

    return {
        "q": q,
        "candidate": candidate,
        "status": status,
    }


def eligible_anchors(max_right_prime: int) -> list[int]:
    """Return eligible current primes through one cutoff."""
    anchors: list[int] = []
    for row in GAP_TYPE_PROBE.type_rows(int(max_right_prime)):
        q = int(row["current_right_prime"])
        if q <= int(max_right_prime) and q % 30 in ELIGIBLE_RESIDUES:
            anchors.append(q)
    if not anchors:
        raise ValueError("no eligible width-2 anchors found")
    return anchors


def generated_records(max_right_prime: int) -> list[dict[str, object]]:
    """Return generated width-2 records through one cutoff."""
    return [width2_record(q) for q in eligible_anchors(max_right_prime)]


def audit_record(record: dict[str, object]) -> dict[str, object]:
    """Attach downstream audit fields to one generated record."""
    q = int(record["q"])
    candidate = int(record["candidate"])
    w = q + 1
    tau_w = divisor_count_at(w)
    tau_candidate = divisor_count_at(candidate)
    endpoint_class = ENDPOINT_PRIME_CLOSURE if tau_candidate == 2 else ENDPOINT_COMPOSITE_OBSTRUCTION
    status = str(record["status"])
    false_exclusion = status == STATUS_EXCLUDED and endpoint_class == ENDPOINT_PRIME_CLOSURE
    unresolved_composite = status == STATUS_UNRESOLVED and endpoint_class == ENDPOINT_COMPOSITE_OBSTRUCTION
    return {
        **record,
        "w": w,
        "tau_w": tau_w,
        "tau_candidate": tau_candidate,
        "endpoint_class": endpoint_class,
        "forced_interior_carrier": tau_w > 2,
        "endpoint_fixed_point": tau_candidate == 2,
        "endpoint_below_forced_load": tau_candidate < tau_w,
        "endpoint_equal_forced_load": tau_candidate == tau_w,
        "endpoint_above_forced_load": tau_candidate > tau_w,
        "false_exclusion": false_exclusion,
        "unresolved_composite": unresolved_composite,
    }


def audited_rows(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return downstream audit rows."""
    return [audit_record(record) for record in records]


def knob_status(row: dict[str, object], knob: str) -> str:
    """Return excluded/unresolved status under one decision knob."""
    if knob == "pgs_width2_full":
        return str(row["status"])
    if knob == "endpoint_fixed_point":
        if bool(row["endpoint_fixed_point"]):
            return STATUS_UNRESOLVED
        return STATUS_EXCLUDED
    if knob == "endpoint_below_forced_load":
        if bool(row["endpoint_below_forced_load"]):
            return STATUS_UNRESOLVED
        return STATUS_EXCLUDED
    if knob == "forced_interior_carrier":
        if bool(row["forced_interior_carrier"]):
            return STATUS_EXCLUDED
        return STATUS_UNRESOLVED
    raise ValueError(f"unknown decision knob: {knob}")


def summarize_knob(rows: list[dict[str, object]], knob: str) -> dict[str, object]:
    """Return audit metrics for one decision knob."""
    projected = []
    for row in rows:
        status = knob_status(row, knob)
        endpoint_class = str(row["endpoint_class"])
        projected.append(
            {
                "status": status,
                "false_exclusion": status == STATUS_EXCLUDED and endpoint_class == ENDPOINT_PRIME_CLOSURE,
                "unresolved_composite": (
                    status == STATUS_UNRESOLVED and endpoint_class == ENDPOINT_COMPOSITE_OBSTRUCTION
                ),
                "endpoint_class": endpoint_class,
            }
        )

    excluded = [row for row in projected if row["status"] == STATUS_EXCLUDED]
    unresolved = [row for row in projected if row["status"] == STATUS_UNRESOLVED]
    false_exclusions = [row for row in projected if row["false_exclusion"]]
    unresolved_composites = [row for row in projected if row["unresolved_composite"]]
    composite_rows = [row for row in projected if row["endpoint_class"] == ENDPOINT_COMPOSITE_OBSTRUCTION]
    prime_rows = [row for row in projected if row["endpoint_class"] == ENDPOINT_PRIME_CLOSURE]
    excluded_composites = [
        row
        for row in projected
        if row["status"] == STATUS_EXCLUDED and row["endpoint_class"] == ENDPOINT_COMPOSITE_OBSTRUCTION
    ]
    return {
        "knob": knob,
        "excluded_count": len(excluded),
        "unresolved_count": len(unresolved),
        "false_exclusion_count": len(false_exclusions),
        "unresolved_composite_count": len(unresolved_composites),
        "exclusion_coverage_among_composites": (
            len(excluded_composites) / len(composite_rows) if composite_rows else 0.0
        ),
        "unresolved_prime_closure_share": (
            len(prime_rows) / len(unresolved) if unresolved else 0.0
        ),
        "audit_status": "PASS" if not false_exclusions and not unresolved_composites else "FAIL",
    }


def knob_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return audit rows for all tested decision knobs."""
    return [summarize_knob(rows, knob) for knob in KNOBS]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return summary metrics for the width-2 contract."""
    excluded = [row for row in rows if row["status"] == STATUS_EXCLUDED]
    unresolved = [row for row in rows if row["status"] == STATUS_UNRESOLVED]
    false_exclusions = [row for row in rows if row["false_exclusion"]]
    unresolved_composites = [row for row in rows if row["unresolved_composite"]]
    composite_rows = [row for row in rows if row["endpoint_class"] == ENDPOINT_COMPOSITE_OBSTRUCTION]
    prime_rows = [row for row in rows if row["endpoint_class"] == ENDPOINT_PRIME_CLOSURE]
    excluded_composites = [
        row
        for row in rows
        if row["status"] == STATUS_EXCLUDED and row["endpoint_class"] == ENDPOINT_COMPOSITE_OBSTRUCTION
    ]
    return {
        "eligible_residues": list(ELIGIBLE_RESIDUES),
        "eligible_anchor_count": len(rows),
        "excluded_count": len(excluded),
        "unresolved_count": len(unresolved),
        "prime_closure_count": len(prime_rows),
        "composite_obstruction_count": len(composite_rows),
        "false_exclusion_count": len(false_exclusions),
        "unresolved_composite_count": len(unresolved_composites),
        "exclusion_coverage_among_composites": (
            len(excluded_composites) / len(composite_rows) if composite_rows else 0.0
        ),
        "unresolved_prime_closure_share": (
            len(prime_rows) / len(unresolved) if unresolved else 0.0
        ),
        "decision_knobs": knob_rows(rows),
        "audit_status": "PASS" if not false_exclusions and not unresolved_composites else "FAIL",
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the width-2 PGS generator probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records = generated_records(args.max_right_prime)
    rows = audited_rows(records)
    summary = summarize(rows)

    write_jsonl(args.output_dir / "generated_records.jsonl", records)
    write_csv(
        args.output_dir / "audit_rows.csv",
        rows,
        [
            "q",
            "candidate",
            "status",
            "w",
            "tau_w",
            "tau_candidate",
            "endpoint_class",
            "forced_interior_carrier",
            "endpoint_fixed_point",
            "endpoint_below_forced_load",
            "endpoint_equal_forced_load",
            "endpoint_above_forced_load",
            "false_exclusion",
            "unresolved_composite",
        ],
    )
    write_csv(
        args.output_dir / "decision_knob_rows.csv",
        knob_rows(rows),
        [
            "knob",
            "excluded_count",
            "unresolved_count",
            "false_exclusion_count",
            "unresolved_composite_count",
            "exclusion_coverage_among_composites",
            "unresolved_prime_closure_share",
            "audit_status",
        ],
    )
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
