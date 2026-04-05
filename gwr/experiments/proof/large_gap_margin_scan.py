#!/usr/bin/env python3
"""Extract exact no-early-spoiler margins on the large-gap surface."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment


MARGIN_SCAN_PATH = ROOT / "gwr" / "experiments" / "proof" / "no_early_spoiler_margin_scan.py"
DEFAULT_TOP_GAP_LIMIT = 100


def load_margin_scan_module():
    """Load the exact margin-scan helpers directly from file."""
    module_name = "no_early_spoiler_margin_scan_runtime_large_gap"
    spec = importlib.util.spec_from_file_location(module_name, MARGIN_SCAN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load no_early_spoiler_margin_scan")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


MARGIN_SCAN = load_margin_scan_module()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Scan one exact interval and record worst no-early-spoiler margins "
            "for the largest gaps and for each exact gap size."
        ),
    )
    parser.add_argument(
        "--lo",
        type=int,
        default=2,
        help="Inclusive lower bound of the natural-number interval.",
    )
    parser.add_argument(
        "--hi",
        type=int,
        default=20_000_001,
        help="Exclusive upper bound of the natural-number interval.",
    )
    parser.add_argument(
        "--top-gap-limit",
        type=int,
        default=DEFAULT_TOP_GAP_LIMIT,
        help="How many largest gaps to retain.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def _gap_case(
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
    """Return a JSON-ready worst-case record for one gap."""
    return MARGIN_SCAN._case_record(
        left_prime=left_prime,
        right_prime=right_prime,
        winner_value=winner_value,
        winner_divisor_count=winner_divisor_count,
        earlier_value=earlier_value,
        earlier_divisor_count=earlier_divisor_count,
        log_margin=log_margin,
        critical_ratio=critical_ratio,
        actual_ratio=actual_ratio,
        ratio_margin=ratio_margin,
    )


def analyze_interval(lo: int, hi: int, top_gap_limit: int) -> dict[str, object]:
    """Return exact large-gap and gap-size no-early-spoiler margins."""
    if lo < 2:
        raise ValueError("lo must be at least 2")
    if hi <= lo:
        raise ValueError("hi must be greater than lo")
    if top_gap_limit < 1:
        raise ValueError("top_gap_limit must be at least 1")

    divisor_count = divisor_counts_segment(lo, hi)
    values = np.arange(lo, hi, dtype=np.int64)
    primes = values[divisor_count == 2]

    gap_count = 0
    gap_with_earlier_candidates_count = 0
    largest_gap_cases: list[dict[str, int | float]] = []
    gap_size_best_case: dict[int, dict[str, int | float]] = {}

    for left_prime_raw, right_prime_raw in zip(primes[:-1], primes[1:]):
        left_prime = int(left_prime_raw)
        right_prime = int(right_prime_raw)
        gap = right_prime - left_prime
        if gap < 4:
            continue

        gap_count += 1
        left_index = left_prime - lo + 1
        right_index = right_prime - lo
        gap_values = values[left_index:right_index]
        gap_divisors = divisor_count[left_index:right_index]

        winner_divisor_count = int(np.min(gap_divisors))
        winner_index = int(np.flatnonzero(gap_divisors == winner_divisor_count)[0])
        if winner_index == 0:
            continue

        gap_with_earlier_candidates_count += 1
        winner_value = int(gap_values[winner_index])

        worst_case: dict[str, int | float] | None = None
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

            log_margin = MARGIN_SCAN.log_score_margin(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            )
            critical_ratio, actual_ratio, ratio_margin = MARGIN_SCAN.critical_ratio_margin(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            )
            case = _gap_case(
                left_prime=left_prime,
                right_prime=right_prime,
                winner_value=winner_value,
                winner_divisor_count=winner_divisor_count,
                earlier_value=earlier_value,
                earlier_divisor_count=earlier_divisor_count,
                log_margin=log_margin,
                critical_ratio=critical_ratio,
                actual_ratio=actual_ratio,
                ratio_margin=ratio_margin,
            )

            if worst_case is None or float(case["critical_ratio_margin"]) < float(
                worst_case["critical_ratio_margin"]
            ):
                worst_case = case

        if worst_case is None:
            raise RuntimeError("gap with earlier candidates produced no worst case")

        largest_gap_cases.append(worst_case)
        largest_gap_cases.sort(
            key=lambda row: (-int(row["gap"]), float(row["critical_ratio_margin"]), int(row["left_prime"]))
        )
        del largest_gap_cases[top_gap_limit:]

        best_for_size = gap_size_best_case.get(gap)
        if best_for_size is None or float(worst_case["critical_ratio_margin"]) < float(
            best_for_size["critical_ratio_margin"]
        ):
            gap_size_best_case[gap] = worst_case

    gap_size_frontier = [
        gap_size_best_case[gap]
        for gap in sorted(gap_size_best_case)
    ]

    return {
        "interval": {"lo": lo, "hi": hi},
        "decision_surface": (
            "Exact worst no-early-spoiler margins on the large-gap surface and "
            "for each realized gap size."
        ),
        "gap_count": gap_count,
        "gap_with_earlier_candidates_count": gap_with_earlier_candidates_count,
        "top_gap_limit": top_gap_limit,
        "largest_gap_cases": largest_gap_cases,
        "gap_size_frontier": gap_size_frontier,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the large-gap margin scan and emit a JSON artifact."""
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = analyze_interval(args.lo, args.hi, args.top_gap_limit)
    serialized = json.dumps(payload, indent=2)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")

    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
