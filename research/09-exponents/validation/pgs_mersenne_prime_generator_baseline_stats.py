#!/usr/bin/env python3
"""Baseline cost stats for the current PGSMPG generator."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "research" / "09-exponents" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import pgs_mersenne_prime_generator as generator


DEFAULT_VALUE_CEILING = 10**50
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "09-exponents"
    / "output"
    / "pgs_mersenne_prime_generator_baseline_stats"
)

TRANSITION_FIELDS = [
    "p",
    "q",
    "status",
    "value_ceiling",
    "max_exponent",
    "candidate_bound",
    "attempt_count",
    "attempted_exponents",
    "tau_call_count",
    "exact_tau_call_count",
    "exponent_tau_call_count",
    "residue_return_tau_call_count",
    "boundary_tau_call_count",
    "tau_elapsed_seconds",
    "wall_elapsed_seconds",
    "max_tau_call_seconds",
    "max_tau_input_bit_length",
    "max_boundary_input_bit_length",
]

TAU_CALL_FIELDS = [
    "transition_p",
    "transition_status",
    "call_index",
    "bit_length",
    "tau",
    "elapsed_seconds",
    "call_role",
    "work_kind",
    "exact_divisor_count",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Capture current PGSMPG cost stats.")
    parser.add_argument("--value-ceiling", type=int, default=DEFAULT_VALUE_CEILING)
    parser.add_argument("--start-exponent", type=int, default=2)
    parser.add_argument("--candidate-bound", type=int, default=generator.DEFAULT_CANDIDATE_BOUND)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def max_exponent_for_value_ceiling(value_ceiling: int) -> int:
    """Return largest exponent e with 2^e - 1 <= value_ceiling."""
    value_ceiling = int(value_ceiling)
    if value_ceiling < 3:
        raise ValueError("value_ceiling must be at least 3")
    return (value_ceiling + 1).bit_length() - 1


def measured_transition(
    p: int,
    value_ceiling: int,
    max_exponent: int,
    candidate_bound: int,
) -> tuple[dict[str, object], list[dict[str, object]], int | None]:
    """Run one PGSMPG transition with measured tau calls."""
    original_tau = generator.tau
    original_residue_return_pressure = generator.residue_return_pressure
    original_left_boundary_state_certificate = generator.left_boundary_state_certificate
    current_call_role = "exponent"
    tau_calls: list[dict[str, object]] = []

    def measured_tau(n: int) -> int:
        started = time.perf_counter()
        tau_value = original_tau(n)
        elapsed = time.perf_counter() - started
        tau_calls.append(
            {
                "bit_length": int(n).bit_length(),
                "tau": tau_value,
                "elapsed_seconds": elapsed,
                "call_role": current_call_role,
            }
        )
        return tau_value

    def measured_left_boundary_state_certificate(
        exponent: int,
        candidate_bound: int = generator.DEFAULT_CANDIDATE_BOUND,
    ) -> dict[str, object] | None:
        nonlocal current_call_role
        previous_call_role = current_call_role
        current_call_role = "boundary"
        try:
            return original_left_boundary_state_certificate(exponent, candidate_bound)
        finally:
            current_call_role = previous_call_role

    def measured_residue_return_pressure(exponent: int) -> dict[str, object]:
        nonlocal current_call_role
        previous_call_role = current_call_role
        current_call_role = "residue_return"
        calls_before = len(tau_calls)
        started = time.perf_counter()
        try:
            pressure = original_residue_return_pressure(exponent)
        finally:
            current_call_role = previous_call_role
        # Thresholded pressure may settle without calling tau. Record one
        # residue-return work row so cost roles still reflect offset-1 checks.
        residue_tau_made = any(
            row["call_role"] == "residue_return" for row in tau_calls[calls_before:]
        )
        if not residue_tau_made:
            tau_calls.append(
                {
                    "bit_length": int(pressure["candidate_bit_length"]),
                    "tau": int(pressure["candidate_divisor_count"]),
                    "elapsed_seconds": time.perf_counter() - started,
                    "call_role": "residue_return",
                    "work_kind": "thresholded_scan",
                    "exact_divisor_count": bool(pressure.get("exact_divisor_count", True)),
                }
            )
        return pressure

    started = time.perf_counter()
    generator.tau = measured_tau
    generator.residue_return_pressure = measured_residue_return_pressure
    generator.left_boundary_state_certificate = measured_left_boundary_state_certificate
    try:
        attempts: list[dict[str, object]] = []
        q = None
        status = "terminal_unresolved"
        for exponent in range(int(p) + 1, int(max_exponent) + 1):
            current_call_role = "exponent"
            attempt = generator.exponent_attempt_row(
                exponent,
                candidate_bound=candidate_bound,
            )
            attempts.append(attempt)
            if bool(attempt["mersenne_location_inferred"]):
                q = int(exponent)
                status = "resolved"
                break
    finally:
        generator.tau = original_tau
        generator.residue_return_pressure = original_residue_return_pressure
        generator.left_boundary_state_certificate = original_left_boundary_state_certificate
    wall_elapsed = time.perf_counter() - started

    attempted_exponents = [int(row["exponent"]) for row in attempts]
    exponent_tau_call_count = sum(1 for row in tau_calls if row["call_role"] == "exponent")
    residue_return_calls = [
        row for row in tau_calls if row["call_role"] == "residue_return"
    ]
    for index, row in enumerate(tau_calls, start=1):
        row["transition_p"] = int(p)
        row["transition_status"] = status
        row["call_index"] = index
        row.setdefault("work_kind", "exact_tau")
        row.setdefault("exact_divisor_count", True)

    boundary_calls = [row for row in tau_calls if row["call_role"] == "boundary"]
    exact_tau_calls = [row for row in tau_calls if row.get("work_kind", "exact_tau") == "exact_tau"]
    transition_row = {
        "p": int(p),
        "q": "" if q is None else int(q),
        "status": status,
        "value_ceiling": int(value_ceiling),
        "max_exponent": int(max_exponent),
        "candidate_bound": int(candidate_bound),
        "attempt_count": len(attempts),
        "attempted_exponents": ";".join(str(value) for value in attempted_exponents),
        "tau_call_count": len(tau_calls),
        "exact_tau_call_count": len(exact_tau_calls),
        "exponent_tau_call_count": exponent_tau_call_count,
        "residue_return_tau_call_count": len(residue_return_calls),
        "boundary_tau_call_count": len(boundary_calls),
        "tau_elapsed_seconds": sum(float(row["elapsed_seconds"]) for row in tau_calls),
        "wall_elapsed_seconds": wall_elapsed,
        "max_tau_call_seconds": (
            max(float(row["elapsed_seconds"]) for row in tau_calls) if tau_calls else 0.0
        ),
        "max_tau_input_bit_length": (
            max(int(row["bit_length"]) for row in tau_calls) if tau_calls else 0
        ),
        "max_boundary_input_bit_length": (
            max(int(row["bit_length"]) for row in boundary_calls) if boundary_calls else 0
        ),
    }
    return transition_row, tau_calls, q


def collect_stats(
    start_exponent: int,
    value_ceiling: int,
    candidate_bound: int,
) -> tuple[list[int], list[dict[str, object]], list[dict[str, object]]]:
    """Return baseline stats through one value ceiling."""
    max_exponent = max_exponent_for_value_ceiling(value_ceiling)
    exponents = [int(start_exponent)]
    transition_rows: list[dict[str, object]] = []
    tau_rows: list[dict[str, object]] = []
    current = int(start_exponent)
    while True:
        transition, tau_calls, q = measured_transition(
            current,
            value_ceiling,
            max_exponent,
            candidate_bound,
        )
        transition_rows.append(transition)
        tau_rows.extend(tau_calls)
        if q is None or int(q) > max_exponent:
            break
        exponents.append(int(q))
        current = int(q)
    return exponents, transition_rows, tau_rows


def summarize(
    exponents: list[int],
    transition_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    value_ceiling: int,
    candidate_bound: int,
) -> dict[str, object]:
    """Return compact baseline stats."""
    resolved = [row for row in transition_rows if row["status"] == "resolved"]
    terminal = [row for row in transition_rows if row["status"] == "terminal_unresolved"]
    boundary_rows = [row for row in tau_rows if row["call_role"] == "boundary"]
    residue_return_rows = [
        row for row in tau_rows if row["call_role"] == "residue_return"
    ]
    wall_elapsed_seconds = sum(
        float(row["wall_elapsed_seconds"]) for row in transition_rows
    )
    resolved_wall_elapsed_seconds = sum(
        float(row["wall_elapsed_seconds"]) for row in resolved
    )
    terminal_wall_elapsed_seconds = sum(
        float(row["wall_elapsed_seconds"]) for row in terminal
    )
    return {
        "value_ceiling": int(value_ceiling),
        "max_exponent": max_exponent_for_value_ceiling(value_ceiling),
        "candidate_bound": int(candidate_bound),
        "live_rule_id": generator.PGSMPG_RESIDUE_RETURN_RULE_ID,
        "live_path": "residue_return_offset_1",
        "mersenne_exponents": exponents,
        "mersenne_exponent_count": len(exponents),
        "resolved_transition_count": len(resolved),
        "terminal_unresolved_count": len(terminal),
        "tau_call_count": len(tau_rows),
        "exact_tau_call_count": sum(
            1 for row in tau_rows if row.get("work_kind", "exact_tau") == "exact_tau"
        ),
        "thresholded_scan_call_count": sum(
            1 for row in tau_rows if row.get("work_kind") == "thresholded_scan"
        ),
        "exponent_tau_call_count": sum(
            1 for row in tau_rows if row["call_role"] == "exponent"
        ),
        "residue_return_tau_call_count": len(residue_return_rows),
        "boundary_tau_call_count": len(boundary_rows),
        "tau_elapsed_seconds": sum(float(row["elapsed_seconds"]) for row in tau_rows),
        "wall_elapsed_seconds": wall_elapsed_seconds,
        "resolved_wall_elapsed_seconds": resolved_wall_elapsed_seconds,
        "terminal_wall_elapsed_seconds": terminal_wall_elapsed_seconds,
        "max_tau_call_seconds": (
            max(float(row["elapsed_seconds"]) for row in tau_rows) if tau_rows else 0.0
        ),
        "max_tau_input_bit_length": (
            max(int(row["bit_length"]) for row in tau_rows) if tau_rows else 0
        ),
        "max_boundary_input_bit_length": (
            max(int(row["bit_length"]) for row in boundary_rows) if boundary_rows else 0
        ),
        "transition_rows": len(transition_rows),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    exponents: list[int],
    transition_rows: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    value_ceiling: int,
    candidate_bound: int,
) -> None:
    """Write baseline stats outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "transition_stats_rows.csv", transition_rows, TRANSITION_FIELDS)
    write_csv(output_dir / "tau_call_rows.csv", tau_rows, TAU_CALL_FIELDS)
    with (output_dir / "mersenne_exponents.jsonl").open(
        "w",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        for exponent in exponents:
            handle.write(
                json.dumps(
                    {
                        "e": exponent,
                        "mersenne_value_bit_length": exponent,
                    }
                )
                + "\n"
            )
    (output_dir / "summary.json").write_text(
        json.dumps(
            summarize(exponents, transition_rows, tau_rows, value_ceiling, candidate_bound),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run baseline stats capture."""
    args = build_parser().parse_args(argv)
    exponents, transition_rows, tau_rows = collect_stats(
        args.start_exponent,
        args.value_ceiling,
        args.candidate_bound,
    )
    write_outputs(
        args.output_dir,
        exponents,
        transition_rows,
        tau_rows,
        args.value_ceiling,
        args.candidate_bound,
    )
    print("PGSMPG baseline exponents: " + ", ".join(str(value) for value in exponents))
    print(f"PGSMPG baseline tau calls: {len(tau_rows)}")
    print(f"Output dir: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
