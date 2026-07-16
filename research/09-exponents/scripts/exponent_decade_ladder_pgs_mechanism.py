#!/usr/bin/env python3
"""PGS-only exponent-decade ladder mechanism."""

from __future__ import annotations

import argparse
import csv
import json
import signal
import sys
from pathlib import Path

from sympy import divisor_count


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import pgs_mersenne_prime_generator as pgsmpg
import toy_exponent_wall_pgs_mechanism as toy_mechanism


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "09-exponents" / "output" / "exponent_decade_ladder_probe"
DEFAULT_RUNG_MAX_EXPONENTS = (31, 100, 1000)
DEFAULT_CANDIDATE_BOUND = 4096
DEFAULT_CANDIDATE_SECONDS_LIMIT = 1.0
NUMBER_FAMILY = "power_of_two"
STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO = "exponent_divisor_count_not_two"
STATUS_LEFT_PRIME_RESOLVED = "left_prime_resolved"
STATUS_LEFT_PRIME_UNRESOLVED = "left_prime_unresolved"
# Phase 2 default: Mersenne inference matches live PGSMPG residue-return.
INFERENCE_RESIDUE_RETURN = "residue_return"
INFERENCE_LEFT_PRIME = "left_prime"
DEFAULT_MERSENNE_INFERENCE = INFERENCE_RESIDUE_RETURN
VALID_MERSENNE_INFERENCE_MODES = frozenset(
    {INFERENCE_RESIDUE_RETURN, INFERENCE_LEFT_PRIME}
)


PGS_FIELDNAMES = [
    "rung_min_exponent",
    "rung_max_exponent",
    "exponent",
    "exponent_divisor_count",
    "exponent_status",
    "number_family",
    "mersenne_inference_mode",
    "left_prime_rule_id",
    "candidate_bound",
    "candidate_seconds_limit",
    "candidate_checks",
    "rejected_candidate_offsets_before_left_prime",
    "unresolved_reason",
    "unresolved_candidate_offset",
    "power_of_two",
    "mersenne_number",
    "distance_to_left_prime",
    "mersenne_location_inferred",
    "left_prime",
    "residue_return_status",
    "exact_divisor_count",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Run the PGS exponent-decade ladder.")
    parser.add_argument(
        "--rungs",
        default=",".join(str(value) for value in DEFAULT_RUNG_MAX_EXPONENTS),
        help="Comma-separated maximum exponents for each ladder rung.",
    )
    parser.add_argument("--candidate-bound", type=int, default=DEFAULT_CANDIDATE_BOUND)
    parser.add_argument(
        "--candidate-seconds-limit",
        type=float,
        default=DEFAULT_CANDIDATE_SECONDS_LIMIT,
    )
    parser.add_argument(
        "--mersenne-inference",
        choices=sorted(VALID_MERSENNE_INFERENCE_MODES),
        default=DEFAULT_MERSENNE_INFERENCE,
        help=(
            "residue_return: offset-1 pressure only (live PGSMPG rule). "
            "left_prime: multi-offset nearest-left recovery (legacy diagnostic)."
        ),
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


class CandidateWorkLimitReached(RuntimeError):
    """Raised when one candidate does not clear within the configured work limit."""


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(n))


def limited_tau(n: int, seconds_limit: float) -> int:
    """Return exact divisor count with an explicit per-candidate work limit."""
    if seconds_limit <= 0:
        return tau(n)

    def handler(_signum, _frame):
        raise CandidateWorkLimitReached

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds_limit)
    try:
        return tau(n)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def parse_rungs(value: str) -> list[int]:
    """Parse and validate ladder rungs."""
    rungs = [int(part) for part in value.split(",") if part.strip()]
    if not rungs:
        raise ValueError("at least one rung is required")
    if any(rung < 2 for rung in rungs):
        raise ValueError("all rungs must be at least 2")
    return sorted(dict.fromkeys(rungs))


def rung_windows(rungs: list[int]) -> list[tuple[int, int]]:
    """Return non-cumulative exponent windows for sorted rungs."""
    windows: list[tuple[int, int]] = []
    previous = 1
    for rung in rungs:
        start = max(2, previous + 1)
        if start <= rung:
            windows.append((start, rung))
        previous = rung
    return windows


def blank_boundary_fields(
    mersenne_inference_mode: str = DEFAULT_MERSENNE_INFERENCE,
) -> dict[str, object]:
    """Return empty boundary fields for rows without boundary recovery."""
    return {
        "mersenne_inference_mode": mersenne_inference_mode,
        "left_prime_rule_id": toy_mechanism.PGS_LEFT_PRIME_RULE_ID,
        "candidate_bound": "",
        "candidate_seconds_limit": "",
        "candidate_checks": "",
        "rejected_candidate_offsets_before_left_prime": "",
        "unresolved_reason": "",
        "unresolved_candidate_offset": "",
        "power_of_two": "",
        "mersenne_number": "",
        "distance_to_left_prime": "",
        "mersenne_location_inferred": False,
        "left_prime": "",
        "residue_return_status": "",
        "exact_divisor_count": "",
    }


def excluded_exponent_row(
    rung_min_exponent: int,
    rung_max_exponent: int,
    exponent: int,
    exponent_tau: int,
    mersenne_inference_mode: str = DEFAULT_MERSENNE_INFERENCE,
) -> dict[str, object]:
    """Return a row excluded by exponent divisor count."""
    return {
        "rung_min_exponent": rung_min_exponent,
        "rung_max_exponent": rung_max_exponent,
        "exponent": exponent,
        "exponent_divisor_count": exponent_tau,
        "exponent_status": STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO,
        "number_family": NUMBER_FAMILY,
        **blank_boundary_fields(mersenne_inference_mode),
    }


def limited_call(seconds_limit: float, func, *args, **kwargs):
    """Run one callable under an optional real-time work limit."""
    if seconds_limit <= 0:
        return func(*args, **kwargs)

    def handler(_signum, _frame):
        raise CandidateWorkLimitReached

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds_limit)
    try:
        return func(*args, **kwargs)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def residue_return_row(
    rung_min_exponent: int,
    rung_max_exponent: int,
    exponent: int,
    exponent_tau: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Return one prime-exponent row using live PGSMPG offset-1 residue-return."""
    power_of_two = 1 << exponent
    mersenne_number = power_of_two - 1
    try:
        pressure = limited_call(
            candidate_seconds_limit,
            pgsmpg.residue_return_pressure,
            exponent,
        )
    except CandidateWorkLimitReached:
        return {
            "rung_min_exponent": rung_min_exponent,
            "rung_max_exponent": rung_max_exponent,
            "exponent": exponent,
            "exponent_divisor_count": exponent_tau,
            "exponent_status": STATUS_LEFT_PRIME_UNRESOLVED,
            "number_family": NUMBER_FAMILY,
            "mersenne_inference_mode": INFERENCE_RESIDUE_RETURN,
            "left_prime_rule_id": pgsmpg.PGSMPG_RESIDUE_RETURN_RULE_ID,
            "candidate_bound": "",
            "candidate_seconds_limit": candidate_seconds_limit,
            "candidate_checks": 1,
            "rejected_candidate_offsets_before_left_prime": "",
            "unresolved_reason": "candidate_work_limit",
            "unresolved_candidate_offset": 1,
            "power_of_two": power_of_two,
            "mersenne_number": mersenne_number,
            "distance_to_left_prime": "",
            "mersenne_location_inferred": False,
            "left_prime": "",
            "residue_return_status": "",
            "exact_divisor_count": "",
        }

    inferred = pressure["status"] == pgsmpg.STATUS_RESIDUE_RETURN_RESOLVED_SURVIVOR
    return {
        "rung_min_exponent": rung_min_exponent,
        "rung_max_exponent": rung_max_exponent,
        "exponent": exponent,
        "exponent_divisor_count": exponent_tau,
        "exponent_status": STATUS_LEFT_PRIME_RESOLVED,
        "number_family": NUMBER_FAMILY,
        "mersenne_inference_mode": INFERENCE_RESIDUE_RETURN,
        "left_prime_rule_id": pgsmpg.PGSMPG_RESIDUE_RETURN_RULE_ID,
        "candidate_bound": "",
        "candidate_seconds_limit": candidate_seconds_limit,
        "candidate_checks": 1,
        "rejected_candidate_offsets_before_left_prime": "",
        "unresolved_reason": "",
        "unresolved_candidate_offset": "",
        "power_of_two": power_of_two,
        "mersenne_number": mersenne_number,
        "distance_to_left_prime": 1 if inferred else "",
        "mersenne_location_inferred": inferred,
        "left_prime": mersenne_number if inferred else "",
        "residue_return_status": pressure["status"],
        "exact_divisor_count": bool(pressure.get("exact_divisor_count", True)),
    }


def left_prime_row(
    rung_min_exponent: int,
    rung_max_exponent: int,
    exponent: int,
    exponent_tau: int,
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Return one prime-exponent row using multi-offset left-prime recovery."""
    power_of_two = 2**exponent
    rejected_offsets: list[int] = []
    for offset in toy_mechanism.left_prime_candidate_offsets(power_of_two, candidate_bound):
        candidate = power_of_two - offset
        try:
            candidate_tau = limited_tau(candidate, candidate_seconds_limit)
        except CandidateWorkLimitReached:
            return {
                "rung_min_exponent": rung_min_exponent,
                "rung_max_exponent": rung_max_exponent,
                "exponent": exponent,
                "exponent_divisor_count": exponent_tau,
                "exponent_status": STATUS_LEFT_PRIME_UNRESOLVED,
                "number_family": NUMBER_FAMILY,
                "mersenne_inference_mode": INFERENCE_LEFT_PRIME,
                "left_prime_rule_id": toy_mechanism.PGS_LEFT_PRIME_RULE_ID,
                "candidate_bound": candidate_bound,
                "candidate_seconds_limit": candidate_seconds_limit,
                "candidate_checks": len(rejected_offsets) + 1,
                "rejected_candidate_offsets_before_left_prime": ";".join(
                    str(value) for value in rejected_offsets
                ),
                "unresolved_reason": "candidate_work_limit",
                "unresolved_candidate_offset": offset,
                "power_of_two": power_of_two,
                "mersenne_number": power_of_two - 1,
                "distance_to_left_prime": "",
                "mersenne_location_inferred": False,
                "left_prime": "",
                "residue_return_status": "",
                "exact_divisor_count": "",
            }
        if candidate_tau == 2:
            distance = offset
            return {
                "rung_min_exponent": rung_min_exponent,
                "rung_max_exponent": rung_max_exponent,
                "exponent": exponent,
                "exponent_divisor_count": exponent_tau,
                "exponent_status": STATUS_LEFT_PRIME_RESOLVED,
                "number_family": NUMBER_FAMILY,
                "mersenne_inference_mode": INFERENCE_LEFT_PRIME,
                "left_prime_rule_id": toy_mechanism.PGS_LEFT_PRIME_RULE_ID,
                "candidate_bound": candidate_bound,
                "candidate_seconds_limit": candidate_seconds_limit,
                "candidate_checks": len(rejected_offsets) + 1,
                "rejected_candidate_offsets_before_left_prime": ";".join(
                    str(value) for value in rejected_offsets
                ),
                "unresolved_reason": "",
                "unresolved_candidate_offset": "",
                "power_of_two": power_of_two,
                "mersenne_number": power_of_two - 1,
                "distance_to_left_prime": distance,
                "mersenne_location_inferred": distance == 1,
                "left_prime": candidate,
                "residue_return_status": "",
                "exact_divisor_count": True,
            }
        rejected_offsets.append(offset)
    return {
        "rung_min_exponent": rung_min_exponent,
        "rung_max_exponent": rung_max_exponent,
        "exponent": exponent,
        "exponent_divisor_count": exponent_tau,
        "exponent_status": STATUS_LEFT_PRIME_UNRESOLVED,
        "number_family": NUMBER_FAMILY,
        "mersenne_inference_mode": INFERENCE_LEFT_PRIME,
        "left_prime_rule_id": toy_mechanism.PGS_LEFT_PRIME_RULE_ID,
        "candidate_bound": candidate_bound,
        "candidate_seconds_limit": candidate_seconds_limit,
        "candidate_checks": len(rejected_offsets),
        "rejected_candidate_offsets_before_left_prime": ";".join(
            str(value) for value in rejected_offsets
        ),
        "unresolved_reason": "candidate_bound_exhausted",
        "unresolved_candidate_offset": "",
        "power_of_two": power_of_two,
        "mersenne_number": power_of_two - 1,
        "distance_to_left_prime": "",
        "mersenne_location_inferred": False,
        "left_prime": "",
        "residue_return_status": "",
        "exact_divisor_count": "",
    }


def pgs_row(
    rung_max_exponent: int,
    exponent: int,
    candidate_bound: int,
    candidate_seconds_limit: float = DEFAULT_CANDIDATE_SECONDS_LIMIT,
    rung_min_exponent: int = 2,
    mersenne_inference: str = DEFAULT_MERSENNE_INFERENCE,
) -> dict[str, object]:
    """Return one PGS ladder row."""
    mode = str(mersenne_inference)
    if mode not in VALID_MERSENNE_INFERENCE_MODES:
        raise ValueError(
            f"mersenne_inference must be one of {sorted(VALID_MERSENNE_INFERENCE_MODES)}"
        )
    exponent_tau = tau(exponent)
    if exponent_tau != 2:
        return excluded_exponent_row(
            rung_min_exponent,
            rung_max_exponent,
            exponent,
            exponent_tau,
            mode,
        )
    if mode == INFERENCE_RESIDUE_RETURN:
        return residue_return_row(
            rung_min_exponent,
            rung_max_exponent,
            exponent,
            exponent_tau,
            candidate_seconds_limit,
        )
    return left_prime_row(
        rung_min_exponent,
        rung_max_exponent,
        exponent,
        exponent_tau,
        candidate_bound,
        candidate_seconds_limit,
    )


def collect_rows(
    rungs: list[int],
    candidate_bound: int,
    candidate_seconds_limit: float = DEFAULT_CANDIDATE_SECONDS_LIMIT,
    mersenne_inference: str = DEFAULT_MERSENNE_INFERENCE,
) -> list[dict[str, object]]:
    """Return PGS rows for all ladder rungs."""
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")
    if candidate_seconds_limit < 0:
        raise ValueError("candidate_seconds_limit must be nonnegative")
    mode = str(mersenne_inference)
    if mode not in VALID_MERSENNE_INFERENCE_MODES:
        raise ValueError(
            f"mersenne_inference must be one of {sorted(VALID_MERSENNE_INFERENCE_MODES)}"
        )
    rows: list[dict[str, object]] = []
    for start, rung in rung_windows(rungs):
        for exponent in range(start, rung + 1):
            rows.append(
                pgs_row(
                    rung,
                    exponent,
                    candidate_bound,
                    candidate_seconds_limit,
                    start,
                    mode,
                )
            )
    return rows


def grouped_counts(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    """Return grouped counts for one field."""
    counts: dict[object, int] = {}
    for row in rows:
        value = row[field]
        counts[value] = counts.get(value, 0) + 1
    return [
        {field: value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def rung_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return one summary row for each rung."""
    by_rung: dict[tuple[int, int], list[dict[str, object]]] = {}
    for row in rows:
        key = (int(row["rung_min_exponent"]), int(row["rung_max_exponent"]))
        by_rung.setdefault(key, []).append(row)
    summaries = []
    for (start, rung), rung_rows in sorted(by_rung.items()):
        summaries.append(
            {
                "rung_min_exponent": start,
                "rung_max_exponent": rung,
                "row_count": len(rung_rows),
                "excluded_exponent_count": sum(
                    row["exponent_status"] == STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
                    for row in rung_rows
                ),
                "left_prime_resolved_count": sum(
                    row["exponent_status"] == STATUS_LEFT_PRIME_RESOLVED
                    for row in rung_rows
                ),
                "left_prime_unresolved_count": sum(
                    row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
                    for row in rung_rows
                ),
                "mersenne_location_inferred_count": sum(
                    bool(row["mersenne_location_inferred"]) for row in rung_rows
                ),
            }
        )
    return summaries


def cumulative_summary_rows(rows: list[dict[str, object]], rungs: list[int]) -> list[dict[str, object]]:
    """Return cumulative summary rows through each rung."""
    summaries = []
    for rung in rungs:
        cumulative_rows = [row for row in rows if int(row["exponent"]) <= rung]
        summaries.append(
            {
                "rung_max_exponent": rung,
                "row_count": len(cumulative_rows),
                "excluded_exponent_count": sum(
                    row["exponent_status"] == STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
                    for row in cumulative_rows
                ),
                "left_prime_resolved_count": sum(
                    row["exponent_status"] == STATUS_LEFT_PRIME_RESOLVED
                    for row in cumulative_rows
                ),
                "left_prime_unresolved_count": sum(
                    row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
                    for row in cumulative_rows
                ),
                "mersenne_location_inferred_count": sum(
                    bool(row["mersenne_location_inferred"]) for row in cumulative_rows
                ),
            }
        )
    return summaries


def summarize(
    rows: list[dict[str, object]],
    rungs: list[int],
    candidate_bound: int,
    candidate_seconds_limit: float,
    mersenne_inference: str = DEFAULT_MERSENNE_INFERENCE,
) -> dict[str, object]:
    """Return compact PGS ladder summary."""
    return {
        "rungs": rungs,
        "row_model": "non_cumulative_exponent_windows",
        "mersenne_inference_mode": mersenne_inference,
        "candidate_bound": candidate_bound,
        "candidate_seconds_limit": candidate_seconds_limit,
        "row_count": len(rows),
        "unique_exponents_tested": len({int(row["exponent"]) for row in rows}),
        "unique_exponents_excluded_by_tau_e": len(
            {
                int(row["exponent"])
                for row in rows
                if row["exponent_status"] == STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
            }
        ),
        "unique_left_prime_resolved": len(
            {
                int(row["exponent"])
                for row in rows
                if row["exponent_status"] == STATUS_LEFT_PRIME_RESOLVED
            }
        ),
        "unique_left_prime_unresolved": len(
            {
                int(row["exponent"])
                for row in rows
                if row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
            }
        ),
        "unique_mersenne_locations_inferred": len(
            {int(row["exponent"]) for row in rows if bool(row["mersenne_location_inferred"])}
        ),
        "excluded_exponent_count": sum(
            row["exponent_status"] == STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
            for row in rows
        ),
        "left_prime_resolved_count": sum(
            row["exponent_status"] == STATUS_LEFT_PRIME_RESOLVED
            for row in rows
        ),
        "left_prime_unresolved_count": sum(
            row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
            for row in rows
        ),
        "mersenne_location_inferred_count": sum(
            bool(row["mersenne_location_inferred"]) for row in rows
        ),
        "exponent_status_distribution": grouped_counts(rows, "exponent_status"),
        "distance_to_left_prime_distribution": grouped_counts(
            [
                row
                for row in rows
                if row["exponent_status"] == STATUS_LEFT_PRIME_RESOLVED
                and row["distance_to_left_prime"] != ""
            ],
            "distance_to_left_prime",
        ),
        "unresolved_reason_distribution": grouped_counts(
            [
                row
                for row in rows
                if row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
            ],
            "unresolved_reason",
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, object]],
    rungs: list[int],
    candidate_bound: int,
    candidate_seconds_limit: float,
    mersenne_inference: str = DEFAULT_MERSENNE_INFERENCE,
) -> None:
    """Write PGS ladder outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "pgs_ladder_rows.csv", rows, PGS_FIELDNAMES)
    write_csv(
        output_dir / "pgs_rung_summary_rows.csv",
        rung_summary_rows(rows),
        [
            "rung_min_exponent",
            "rung_max_exponent",
            "row_count",
            "excluded_exponent_count",
            "left_prime_resolved_count",
            "left_prime_unresolved_count",
            "mersenne_location_inferred_count",
        ],
    )
    write_csv(
        output_dir / "pgs_cumulative_summary_rows.csv",
        cumulative_summary_rows(rows, rungs),
        [
            "rung_max_exponent",
            "row_count",
            "excluded_exponent_count",
            "left_prime_resolved_count",
            "left_prime_unresolved_count",
            "mersenne_location_inferred_count",
        ],
    )
    write_csv(
        output_dir / "mersenne_location_inferred_rows.csv",
        [row for row in rows if bool(row["mersenne_location_inferred"])],
        PGS_FIELDNAMES,
    )
    write_csv(
        output_dir / "pgs_unresolved_rows.csv",
        [
            row
            for row in rows
            if row["exponent_status"] == STATUS_LEFT_PRIME_UNRESOLVED
        ],
        PGS_FIELDNAMES,
    )
    (output_dir / "pgs_summary.json").write_text(
        json.dumps(
            summarize(
                rows,
                rungs,
                candidate_bound,
                candidate_seconds_limit,
                mersenne_inference,
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run the PGS exponent-decade ladder mechanism."""
    args = build_parser().parse_args(argv)
    rungs = parse_rungs(args.rungs)
    rows = collect_rows(
        rungs,
        args.candidate_bound,
        args.candidate_seconds_limit,
        args.mersenne_inference,
    )
    write_outputs(
        args.output_dir,
        rows,
        rungs,
        args.candidate_bound,
        args.candidate_seconds_limit,
        args.mersenne_inference,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
