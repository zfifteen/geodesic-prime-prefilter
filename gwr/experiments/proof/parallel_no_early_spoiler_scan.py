#!/usr/bin/env python3
"""Run deterministic segmented GWR scans with checkpointable segment outputs."""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import gmpy2
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment


DEFAULT_LO = 20_000_001
DEFAULT_HI = 100_000_001
DEFAULT_SEGMENT_SIZE = 1_000_000
DEFAULT_SEGMENT_OUTPUT_DIR = ROOT / "output" / "gwr_proof" / "parallel_no_early_spoiler_segments"
TOP_CASE_LIMIT = 20


@dataclass(frozen=True)
class SegmentTask:
    """One deterministic segment assignment."""

    segment_lo: int
    segment_hi: int
    output_path: str


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Scan prime gaps by deterministic segments, write one JSON checkpoint "
            "per segment, and emit one aggregate summary."
        ),
    )
    parser.add_argument("--lo", type=int, default=DEFAULT_LO, help="Inclusive lower bound.")
    parser.add_argument("--hi", type=int, default=DEFAULT_HI, help="Exclusive upper bound.")
    parser.add_argument(
        "--segment-size",
        type=int,
        default=DEFAULT_SEGMENT_SIZE,
        help="Segment width for deterministic work partitioning.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="Worker-process count.",
    )
    parser.add_argument(
        "--segment-output-dir",
        type=Path,
        default=DEFAULT_SEGMENT_OUTPUT_DIR,
        help="Directory where one JSON checkpoint per segment is written.",
    )
    parser.add_argument(
        "--aggregate-output",
        type=Path,
        default=None,
        help="Optional path for the aggregate JSON summary.",
    )
    return parser


def _round_float(value: float) -> float:
    """Return a stable JSON float."""
    return float(f"{value:.18g}")


def score_strictly_greater(
    left_n: int,
    left_divisor_count: int,
    right_n: int,
    right_divisor_count: int,
) -> bool:
    """Return whether the score at the left value is strictly greater."""
    if left_divisor_count < 3 or right_divisor_count < 3:
        raise ValueError("exact score comparison requires composite inputs")
    return pow(left_n, left_divisor_count - 2) < pow(right_n, right_divisor_count - 2)


def log_score_margin(
    earlier_value: int,
    earlier_divisor_count: int,
    winner_value: int,
    winner_divisor_count: int,
) -> float:
    """Return the positive winner-minus-earlier log-score margin."""
    earlier_score = (1.0 - earlier_divisor_count / 2.0) * math.log(earlier_value)
    winner_score = (1.0 - winner_divisor_count / 2.0) * math.log(winner_value)
    return winner_score - earlier_score


def critical_ratio_margin(
    earlier_value: int,
    earlier_divisor_count: int,
    winner_value: int,
    winner_divisor_count: int,
) -> tuple[float, float, float]:
    """Return the critical ratio, actual log ratio, and their positive margin."""
    critical_ratio = (earlier_divisor_count - 2) / (winner_divisor_count - 2)
    actual_ratio = math.log(winner_value) / math.log(earlier_value)
    return critical_ratio, actual_ratio, critical_ratio - actual_ratio


def _case_record(
    left_prime: int,
    right_prime: int,
    winner_value: int,
    winner_divisor_count: int,
    earlier_value: int,
    earlier_divisor_count: int,
    log_margin: float,
    critical_ratio: float,
    actual_ratio: float,
    ratio_margin: float,
) -> dict[str, int | float]:
    """Return one JSON-ready candidate record."""
    critical_excess = critical_ratio - 1.0
    actual_excess = actual_ratio - 1.0
    bridge_load = actual_excess / critical_excess
    return {
        "left_prime": left_prime,
        "right_prime": right_prime,
        "gap": right_prime - left_prime,
        "winner_value": winner_value,
        "winner_divisor_count": winner_divisor_count,
        "winner_offset": winner_value - left_prime,
        "earlier_value": earlier_value,
        "earlier_divisor_count": earlier_divisor_count,
        "earlier_offset": earlier_value - left_prime,
        "delta": earlier_divisor_count - winner_divisor_count,
        "log_score_margin": _round_float(log_margin),
        "critical_ratio": _round_float(critical_ratio),
        "actual_log_ratio": _round_float(actual_ratio),
        "critical_ratio_margin": _round_float(ratio_margin),
        "critical_excess": _round_float(critical_excess),
        "actual_excess": _round_float(actual_excess),
        "bridge_load": _round_float(bridge_load),
    }


def _keep_smallest(top_cases: list[dict[str, int | float]], case: dict[str, int | float], key: str) -> None:
    """Keep only the smallest cases for one positive margin."""
    top_cases.append(case)
    top_cases.sort(key=lambda row: (float(row[key]), int(row["winner_value"])))
    del top_cases[TOP_CASE_LIMIT:]


def _keep_largest(top_cases: list[dict[str, int | float]], case: dict[str, int | float], key: str) -> None:
    """Keep only the largest cases for one load quantity."""
    top_cases.append(case)
    top_cases.sort(key=lambda row: (-float(row[key]), int(row["winner_value"])))
    del top_cases[TOP_CASE_LIMIT:]


def segment_tasks(lo: int, hi: int, segment_size: int, output_dir: Path) -> list[SegmentTask]:
    """Return the deterministic segment schedule."""
    if lo < 2:
        raise ValueError("lo must be at least 2")
    if hi <= lo:
        raise ValueError("hi must be greater than lo")
    if segment_size <= 0:
        raise ValueError("segment_size must be positive")

    tasks: list[SegmentTask] = []
    for segment_lo in range(lo, hi, segment_size):
        segment_hi = min(segment_lo + segment_size, hi)
        output_path = output_dir / f"segment_{segment_lo}_{segment_hi}.json"
        tasks.append(
            SegmentTask(
                segment_lo=segment_lo,
                segment_hi=segment_hi,
                output_path=str(output_path),
            )
        )
    return tasks


def padded_interval(segment_lo: int, segment_hi: int) -> tuple[int, int]:
    """Return the exact padded interval needed for one segment."""
    if segment_lo <= 2:
        padded_lo = 2
    else:
        padded_lo = int(gmpy2.prev_prime(segment_lo))
    padded_hi = int(gmpy2.next_prime(segment_hi - 1)) + 1
    return padded_lo, padded_hi


def analyze_segment(segment_lo: int, segment_hi: int) -> dict[str, object]:
    """Return the exact GWR summary for one deterministic segment."""
    if segment_hi <= segment_lo:
        raise ValueError("segment_hi must be greater than segment_lo")

    analysis_lo, analysis_hi = padded_interval(segment_lo, segment_hi)
    divisor_count = divisor_counts_segment(analysis_lo, analysis_hi)
    values = np.arange(analysis_lo, analysis_hi, dtype=np.int64)
    primes = values[divisor_count == 2]

    gap_count = 0
    earlier_candidate_count = 0
    exact_spoiler_count = 0
    bridge_failure_count = 0

    min_log_margin_case: dict[str, int | float] | None = None
    min_ratio_margin_case: dict[str, int | float] | None = None
    max_bridge_load_case: dict[str, int | float] | None = None

    top_log_margin_cases: list[dict[str, int | float]] = []
    top_ratio_margin_cases: list[dict[str, int | float]] = []
    top_bridge_load_cases: list[dict[str, int | float]] = []

    for left_prime_raw, right_prime_raw in zip(primes[:-1], primes[1:]):
        left_prime = int(left_prime_raw)
        right_prime = int(right_prime_raw)
        if left_prime < segment_lo or left_prime >= segment_hi:
            continue

        gap = right_prime - left_prime
        if gap < 4:
            continue

        gap_count += 1
        left_index = left_prime - analysis_lo + 1
        right_index = right_prime - analysis_lo
        gap_values = values[left_index:right_index]
        gap_divisors = divisor_count[left_index:right_index]

        winner_divisor_count = int(np.min(gap_divisors))
        winner_index = int(np.flatnonzero(gap_divisors == winner_divisor_count)[0])
        winner_value = int(gap_values[winner_index])

        for earlier_value_raw, earlier_divisor_raw in zip(
            gap_values[:winner_index],
            gap_divisors[:winner_index],
        ):
            earlier_value = int(earlier_value_raw)
            earlier_divisor_count = int(earlier_divisor_raw)
            if earlier_divisor_count <= winner_divisor_count:
                raise RuntimeError(
                    "winner is not the leftmost carrier of the minimal divisor class"
                )

            earlier_candidate_count += 1
            winner_beats_earlier = score_strictly_greater(
                winner_value,
                winner_divisor_count,
                earlier_value,
                earlier_divisor_count,
            )
            if not winner_beats_earlier:
                exact_spoiler_count += 1

            current_log_margin = log_score_margin(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            )
            critical_ratio, actual_ratio, ratio_margin = critical_ratio_margin(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            )
            case = _case_record(
                left_prime=left_prime,
                right_prime=right_prime,
                winner_value=winner_value,
                winner_divisor_count=winner_divisor_count,
                earlier_value=earlier_value,
                earlier_divisor_count=earlier_divisor_count,
                log_margin=current_log_margin,
                critical_ratio=critical_ratio,
                actual_ratio=actual_ratio,
                ratio_margin=ratio_margin,
            )

            if float(case["bridge_load"]) >= 1.0:
                bridge_failure_count += 1

            if min_log_margin_case is None or float(case["log_score_margin"]) < float(
                min_log_margin_case["log_score_margin"]
            ):
                min_log_margin_case = case
            if min_ratio_margin_case is None or float(case["critical_ratio_margin"]) < float(
                min_ratio_margin_case["critical_ratio_margin"]
            ):
                min_ratio_margin_case = case
            if max_bridge_load_case is None or float(case["bridge_load"]) > float(
                max_bridge_load_case["bridge_load"]
            ):
                max_bridge_load_case = case

            _keep_smallest(top_log_margin_cases, case, "log_score_margin")
            _keep_smallest(top_ratio_margin_cases, case, "critical_ratio_margin")
            _keep_largest(top_bridge_load_cases, case, "bridge_load")

    if max_bridge_load_case is None:
        max_bridge_load_case = {}
    if min_log_margin_case is None:
        min_log_margin_case = {}
    if min_ratio_margin_case is None:
        min_ratio_margin_case = {}

    return {
        "segment_interval": {"lo": segment_lo, "hi": segment_hi},
        "analysis_interval": {"lo": analysis_lo, "hi": analysis_hi},
        "gap_count": gap_count,
        "earlier_candidate_count": earlier_candidate_count,
        "exact_spoiler_count": exact_spoiler_count,
        "bridge_failure_count": bridge_failure_count,
        "min_log_margin_case": min_log_margin_case,
        "min_ratio_margin_case": min_ratio_margin_case,
        "max_bridge_load": max_bridge_load_case.get("bridge_load"),
        "max_bridge_load_case": max_bridge_load_case,
        "top_log_margin_cases": top_log_margin_cases,
        "top_ratio_margin_cases": top_ratio_margin_cases,
        "top_bridge_load_cases": top_bridge_load_cases,
    }


def process_segment_task(task: SegmentTask) -> dict[str, object]:
    """Process one segment and write its checkpoint JSON."""
    payload = analyze_segment(task.segment_lo, task.segment_hi)
    output_path = Path(task.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise FileExistsError(f"segment output already exists: {output_path}")
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def _merge_top_cases(
    rows: list[dict[str, int | float]],
    incoming: list[dict[str, int | float]],
    key: str,
    reverse: bool,
) -> None:
    """Merge one top-case list deterministically."""
    rows.extend(incoming)
    if reverse:
        rows.sort(key=lambda row: (-float(row[key]), int(row["winner_value"])))
    else:
        rows.sort(key=lambda row: (float(row[key]), int(row["winner_value"])))
    del rows[TOP_CASE_LIMIT:]


def aggregate_reports(lo: int, hi: int, segment_size: int, reports: list[dict[str, object]]) -> dict[str, object]:
    """Return one aggregate summary over completed segments."""
    total_gap_count = 0
    total_earlier_candidate_count = 0
    total_exact_spoiler_count = 0
    total_bridge_failure_count = 0

    min_log_margin_case: dict[str, int | float] | None = None
    min_ratio_margin_case: dict[str, int | float] | None = None
    max_bridge_load_case: dict[str, int | float] | None = None

    top_log_margin_cases: list[dict[str, int | float]] = []
    top_ratio_margin_cases: list[dict[str, int | float]] = []
    top_bridge_load_cases: list[dict[str, int | float]] = []
    segment_rows: list[dict[str, object]] = []

    for report in reports:
        total_gap_count += int(report["gap_count"])
        total_earlier_candidate_count += int(report["earlier_candidate_count"])
        total_exact_spoiler_count += int(report["exact_spoiler_count"])
        total_bridge_failure_count += int(report["bridge_failure_count"])

        segment_rows.append(report["segment_interval"])

        log_case = report["min_log_margin_case"]
        if log_case and (
            min_log_margin_case is None
            or float(log_case["log_score_margin"]) < float(min_log_margin_case["log_score_margin"])
        ):
            min_log_margin_case = log_case

        ratio_case = report["min_ratio_margin_case"]
        if ratio_case and (
            min_ratio_margin_case is None
            or float(ratio_case["critical_ratio_margin"])
            < float(min_ratio_margin_case["critical_ratio_margin"])
        ):
            min_ratio_margin_case = ratio_case

        bridge_case = report["max_bridge_load_case"]
        if bridge_case and (
            max_bridge_load_case is None
            or float(bridge_case["bridge_load"]) > float(max_bridge_load_case["bridge_load"])
        ):
            max_bridge_load_case = bridge_case

        _merge_top_cases(
            top_log_margin_cases,
            report["top_log_margin_cases"],
            "log_score_margin",
            reverse=False,
        )
        _merge_top_cases(
            top_ratio_margin_cases,
            report["top_ratio_margin_cases"],
            "critical_ratio_margin",
            reverse=False,
        )
        _merge_top_cases(
            top_bridge_load_cases,
            report["top_bridge_load_cases"],
            "bridge_load",
            reverse=True,
        )

    return {
        "interval": {"lo": lo, "hi": hi},
        "segment_size": segment_size,
        "segment_count": len(reports),
        "segment_intervals": segment_rows,
        "gap_count": total_gap_count,
        "earlier_candidate_count": total_earlier_candidate_count,
        "exact_spoiler_count": total_exact_spoiler_count,
        "bridge_failure_count": total_bridge_failure_count,
        "min_log_margin_case": min_log_margin_case,
        "min_ratio_margin_case": min_ratio_margin_case,
        "max_bridge_load": None if max_bridge_load_case is None else max_bridge_load_case["bridge_load"],
        "max_bridge_load_case": max_bridge_load_case,
        "top_log_margin_cases": top_log_margin_cases,
        "top_ratio_margin_cases": top_ratio_margin_cases,
        "top_bridge_load_cases": top_bridge_load_cases,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic parallel scan."""
    args = build_parser().parse_args(argv)
    tasks = segment_tasks(args.lo, args.hi, args.segment_size, args.segment_output_dir)
    if not tasks:
        raise RuntimeError("scan produced no work segments")

    if args.jobs == 1:
        reports = [process_segment_task(task) for task in tasks]
    else:
        with multiprocessing.Pool(args.jobs) as pool:
            reports = pool.map(process_segment_task, tasks)

    reports.sort(key=lambda row: int(row["segment_interval"]["lo"]))
    aggregate = aggregate_reports(args.lo, args.hi, args.segment_size, reports)
    serialized = json.dumps(aggregate, indent=2)

    if args.aggregate_output is not None:
        args.aggregate_output.parent.mkdir(parents=True, exist_ok=True)
        args.aggregate_output.write_text(serialized + "\n", encoding="utf-8")

    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
