#!/usr/bin/env python3
"""Validate the Mersenne order-filter obstruction surface."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import factorint, isprime, primerange


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MAX_EXPONENT = 127
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "09-exponents"
    / "output"
    / "pgs_mersenne_order_filter_validation"
)
DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT = 10000

ROW_FIELDS = [
    "exponent",
    "mersenne_number_is_prime",
    "least_factor",
    "least_factor_mod_2e",
    "least_factor_mod_8",
    "order_filter_pass",
    "order_filter_multiplier",
    "order_filter_candidate_rank",
]

RESIDUE_RETURN_EVENT_FIELDS = [
    "exponent",
    "event_index",
    "order_filter_rank",
    "order_filter_multiplier",
    "candidate",
    "pressure",
    "is_zero_pressure",
]

RESIDUE_RETURN_COMPRESSION_FIELDS = [
    "exponent",
    "least_factor",
    "raw_candidate_rank",
    "scan_status",
    "record_low_event_count",
    "compression_ratio",
    "previous_record_low_rank",
    "previous_record_low_pressure",
    "gap_from_previous_record",
    "zero_pressure_rank",
    "zero_pressure_event_index",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Validate order-filter obstruction rows for Mersenne candidates.",
    )
    parser.add_argument("--max-exponent", type=int, default=DEFAULT_MAX_EXPONENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--residue-return-scan-rank-limit",
        type=int,
        default=DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
    )
    return parser


def order_filter_candidate_allowed(exponent: int, multiplier: int) -> bool:
    """Return whether one multiplier gives an order-filter candidate."""
    candidate = 2 * int(exponent) * int(multiplier) + 1
    return candidate % 8 in {1, 7}


def order_filter_candidate_rank(exponent: int, factor: int) -> int:
    """Return the rank of one factor inside the order-filtered candidate list."""
    exponent = int(exponent)
    factor = int(factor)
    multiplier = (factor - 1) // (2 * exponent)
    if exponent == 2:
        return sum(
            1
            for value in range(1, multiplier + 1)
            if (2 * exponent * value + 1) % 8 in {1, 7}
        )
    if exponent % 4 == 1:
        return (multiplier // 4) * 2 + sum(
            1 for residue in range(1, multiplier % 4 + 1) if residue in {3}
        )
    return (multiplier // 4) * 2 + sum(
        1 for residue in range(1, multiplier % 4 + 1) if residue in {1}
    )


def fixed_point_pressure(exponent: int, candidate: int) -> int:
    """Return the residue distance from the fixed point modulo one candidate."""
    candidate = int(candidate)
    residue = pow(2, int(exponent), candidate)
    return min((residue - 1) % candidate, (1 - residue) % candidate)


def residue_return_events(
    exponent: int,
    factor: int,
    max_rank: int = DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
) -> list[dict[str, object]]:
    """Return record-low fixed-point residue events before the least factor."""
    raw_rank = order_filter_candidate_rank(exponent, factor)
    if raw_rank > int(max_rank):
        return []

    factor_multiplier = (int(factor) - 1) // (2 * int(exponent))
    events: list[dict[str, object]] = []
    best_pressure: int | None = None
    rank = 0
    for multiplier in range(1, factor_multiplier + 1):
        if not order_filter_candidate_allowed(exponent, multiplier):
            continue
        rank += 1
        candidate = 2 * int(exponent) * multiplier + 1
        pressure = fixed_point_pressure(exponent, candidate)
        if best_pressure is None or pressure < best_pressure:
            best_pressure = pressure
            events.append(
                {
                    "exponent": exponent,
                    "event_index": len(events) + 1,
                    "order_filter_rank": rank,
                    "order_filter_multiplier": multiplier,
                    "candidate": candidate,
                    "pressure": pressure,
                    "is_zero_pressure": pressure == 0,
                }
            )
        if candidate == int(factor):
            break
    return events


def validation_row(exponent: int) -> dict[str, object]:
    """Return one order-filter validation row for a prime exponent."""
    mersenne_number = 2**int(exponent) - 1
    if bool(isprime(mersenne_number)):
        return {
            "exponent": exponent,
            "mersenne_number_is_prime": True,
            "least_factor": "",
            "least_factor_mod_2e": "",
            "least_factor_mod_8": "",
            "order_filter_pass": True,
            "order_filter_multiplier": "",
            "order_filter_candidate_rank": "",
        }

    least_factor = min(factorint(mersenne_number))
    multiplier = (least_factor - 1) // (2 * int(exponent))
    return {
        "exponent": exponent,
        "mersenne_number_is_prime": False,
        "least_factor": least_factor,
        "least_factor_mod_2e": least_factor % (2 * int(exponent)),
        "least_factor_mod_8": least_factor % 8,
        "order_filter_pass": (
            least_factor % (2 * int(exponent)) == 1
            and least_factor % 8 in {1, 7}
        ),
        "order_filter_multiplier": multiplier,
        "order_filter_candidate_rank": order_filter_candidate_rank(exponent, least_factor),
    }


def collect_rows(max_exponent: int) -> list[dict[str, object]]:
    """Return validation rows for prime exponents through the bound."""
    return [validation_row(exponent) for exponent in primerange(2, int(max_exponent) + 1)]


def residue_return_compression_row(
    row: dict[str, object],
    max_rank: int = DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
) -> dict[str, object]:
    """Return the record-low residue compression row for one composite obstruction."""
    raw_rank = int(row["order_filter_candidate_rank"])
    if raw_rank > int(max_rank):
        return {
            "exponent": row["exponent"],
            "least_factor": row["least_factor"],
            "raw_candidate_rank": raw_rank,
            "scan_status": "skipped_rank_above_limit",
            "record_low_event_count": "",
            "compression_ratio": "",
            "previous_record_low_rank": "",
            "previous_record_low_pressure": "",
            "gap_from_previous_record": "",
            "zero_pressure_rank": "",
            "zero_pressure_event_index": "",
        }

    events = residue_return_events(
        int(row["exponent"]),
        int(row["least_factor"]),
        max_rank=max_rank,
    )
    zero_events = [event for event in events if bool(event["is_zero_pressure"])]
    previous = events[-2] if len(events) >= 2 else None
    zero_event = zero_events[-1] if zero_events else None
    event_count = len(events)
    return {
        "exponent": row["exponent"],
        "least_factor": row["least_factor"],
        "raw_candidate_rank": raw_rank,
        "scan_status": "scanned",
        "record_low_event_count": event_count,
        "compression_ratio": raw_rank / event_count if event_count else "",
        "previous_record_low_rank": (
            previous["order_filter_rank"] if previous is not None else ""
        ),
        "previous_record_low_pressure": previous["pressure"] if previous is not None else "",
        "gap_from_previous_record": (
            raw_rank - int(previous["order_filter_rank"])
            if previous is not None
            else ""
        ),
        "zero_pressure_rank": (
            zero_event["order_filter_rank"] if zero_event is not None else ""
        ),
        "zero_pressure_event_index": zero_event["event_index"] if zero_event is not None else "",
    }


def residue_return_outputs(
    rows: list[dict[str, object]],
    max_rank: int = DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return residue-return event rows and per-obstruction compression rows."""
    composite_rows = [row for row in rows if not bool(row["mersenne_number_is_prime"])]
    event_rows: list[dict[str, object]] = []
    compression_rows: list[dict[str, object]] = []
    for row in composite_rows:
        compression_rows.append(residue_return_compression_row(row, max_rank=max_rank))
        if int(row["order_filter_candidate_rank"]) <= int(max_rank):
            event_rows.extend(
                residue_return_events(
                    int(row["exponent"]),
                    int(row["least_factor"]),
                    max_rank=max_rank,
                )
            )
    return event_rows, compression_rows


def summarize(
    rows: list[dict[str, object]],
    max_exponent: int,
    max_residue_return_rank: int = DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
) -> dict[str, object]:
    """Return compact order-filter validation summary."""
    composite_rows = [row for row in rows if not bool(row["mersenne_number_is_prime"])]
    prime_rows = [row for row in rows if bool(row["mersenne_number_is_prime"])]
    failed_rows = [row for row in composite_rows if not bool(row["order_filter_pass"])]
    ranks = [
        int(row["order_filter_candidate_rank"])
        for row in composite_rows
        if row["order_filter_candidate_rank"] != ""
    ]
    event_rows, compression_rows = residue_return_outputs(
        rows,
        max_rank=max_residue_return_rank,
    )
    scanned_rows = [
        row for row in compression_rows if row["scan_status"] == "scanned"
    ]
    skipped_rows = [
        row for row in compression_rows if row["scan_status"] == "skipped_rank_above_limit"
    ]
    zero_pressure_rows = [
        row for row in scanned_rows if row["zero_pressure_rank"] != ""
    ]
    event_counts = [
        int(row["record_low_event_count"])
        for row in scanned_rows
        if row["record_low_event_count"] != ""
    ]
    compression_ratios = [
        float(row["compression_ratio"])
        for row in scanned_rows
        if row["compression_ratio"] != ""
    ]
    return {
        "max_exponent": int(max_exponent),
        "prime_exponent_count": len(rows),
        "mersenne_prime_count": len(prime_rows),
        "mersenne_composite_count": len(composite_rows),
        "composite_order_filter_pass_count": len(composite_rows) - len(failed_rows),
        "composite_order_filter_failure_count": len(failed_rows),
        "max_order_filter_candidate_rank": max(ranks) if ranks else 0,
        "median_order_filter_candidate_rank": sorted(ranks)[len(ranks) // 2] if ranks else 0,
        "residue_return_scan_rank_limit": int(max_residue_return_rank),
        "residue_return_scanned_composite_count": len(scanned_rows),
        "residue_return_skipped_composite_count": len(skipped_rows),
        "residue_return_event_count": len(event_rows),
        "residue_return_zero_pressure_found_count": len(zero_pressure_rows),
        "max_residue_return_compression_ratio": (
            max(compression_ratios) if compression_ratios else 0
        ),
        "median_residue_return_event_count": (
            sorted(event_counts)[len(event_counts) // 2] if event_counts else 0
        ),
        "result": (
            "SURVIVES"
            if composite_rows and not failed_rows
            else "FALSIFIED"
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, object]],
    max_exponent: int,
    max_residue_return_rank: int = DEFAULT_RESIDUE_RETURN_SCAN_RANK_LIMIT,
) -> None:
    """Write validation outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    event_rows, compression_rows = residue_return_outputs(
        rows,
        max_rank=max_residue_return_rank,
    )
    write_csv(output_dir / "order_filter_rows.csv", rows, ROW_FIELDS)
    write_csv(
        output_dir / "composite_obstruction_rows.csv",
        [row for row in rows if not bool(row["mersenne_number_is_prime"])],
        ROW_FIELDS,
    )
    write_csv(
        output_dir / "residue_return_event_rows.csv",
        event_rows,
        RESIDUE_RETURN_EVENT_FIELDS,
    )
    write_csv(
        output_dir / "residue_return_compression_rows.csv",
        compression_rows,
        RESIDUE_RETURN_COMPRESSION_FIELDS,
    )
    (output_dir / "summary.json").write_text(
        json.dumps(
            summarize(
                rows,
                max_exponent,
                max_residue_return_rank=max_residue_return_rank,
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run order-filter validation."""
    args = build_parser().parse_args(argv)
    rows = collect_rows(args.max_exponent)
    write_outputs(
        args.output_dir,
        rows,
        args.max_exponent,
        max_residue_return_rank=args.residue_return_scan_rank_limit,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
