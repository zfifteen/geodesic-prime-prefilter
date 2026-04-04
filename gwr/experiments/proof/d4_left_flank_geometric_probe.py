#!/usr/bin/env python3
"""Probe the direct geometric impossibility of earlier spoilers against d=4 winners."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment


SPOILER_SCAN_PATH = ROOT / "gwr" / "experiments" / "proof" / "earlier_spoiler_scan.py"


def load_spoiler_scan_module():
    """Load the exact score comparison helper."""
    module_name = "earlier_spoiler_scan_runtime_d4_geometric_probe"
    spec = importlib.util.spec_from_file_location(module_name, SPOILER_SCAN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load earlier_spoiler_scan")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


SPOILER_SCAN = load_spoiler_scan_module()


@dataclass(frozen=True)
class ClassRow:
    earlier_divisor_count: int
    candidate_count: int
    min_earlier_value: int
    min_log10_required_over_upper: float
    min_required_over_upper: float | None
    closest_left_prime: int
    closest_right_prime: int
    closest_earlier_value: int
    closest_winner_value: int

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Probe the direct geometric impossibility of earlier higher-divisor "
            "spoilers against d=4 winners."
        ),
    )
    parser.add_argument("--lo", type=int, required=True)
    parser.add_argument("--hi", type=int, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--plot-prefix", type=Path, required=True)
    parser.add_argument("--title", type=str, required=True)
    return parser


def required_over_upper_ratio(earlier_value: int, earlier_divisor_count: int) -> float:
    """Return the ratio of the required winner lower bound to the universal 2a upper bound."""
    if earlier_divisor_count <= 4:
        raise ValueError("earlier divisor count must exceed 4")
    return math.exp(
        0.5 * (earlier_divisor_count - 4) * math.log(earlier_value) - math.log(2.0)
    )


def safe_ratio_from_log10(log10_ratio: float) -> float | None:
    """Return the ratio if it fits in float, else None."""
    if log10_ratio > 300:
        return None
    return 10.0 ** log10_ratio


def log10_required_over_upper(earlier_value: int, earlier_divisor_count: int) -> float:
    """Return log10 of the required-over-upper ratio."""
    if earlier_divisor_count <= 4:
        raise ValueError("earlier divisor count must exceed 4")
    return 0.5 * (earlier_divisor_count - 4) * math.log10(earlier_value) - math.log10(2.0)


def analyze_interval(lo: int, hi: int) -> dict[str, object]:
    if lo < 2:
        raise ValueError("lo must be at least 2")
    if hi <= lo:
        raise ValueError("hi must exceed lo")

    divisor_count = divisor_counts_segment(lo, hi)
    values = np.arange(lo, hi, dtype=np.int64)
    primes = values[divisor_count == 2]

    d4_gap_count = 0
    earlier_candidate_count = 0
    exact_spoiler_count = 0
    class_rows: dict[int, ClassRow] = {}
    all_log10_ratios: list[float] = []
    closest_example: dict[str, int | float] | None = None
    closest_log10_ratio: float | None = None

    for left_prime, right_prime in zip(primes[:-1], primes[1:]):
        gap = int(right_prime - left_prime)
        if gap < 4:
            continue

        left_index = int(left_prime - lo + 1)
        right_index = int(right_prime - lo)
        gap_values = values[left_index:right_index]
        gap_divisors = divisor_count[left_index:right_index]

        winner_divisor_count = int(np.min(gap_divisors))
        if winner_divisor_count != 4:
            continue

        winner_index = int(np.flatnonzero(gap_divisors == winner_divisor_count)[0])
        winner_value = int(gap_values[winner_index])
        d4_gap_count += 1

        for earlier_index in range(winner_index):
            earlier_value = int(gap_values[earlier_index])
            earlier_divisor_count = int(gap_divisors[earlier_index])
            if earlier_divisor_count <= 4:
                raise RuntimeError("found non-spoiler candidate before first d=4 winner")

            earlier_candidate_count += 1
            if SPOILER_SCAN.score_strictly_greater(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            ):
                exact_spoiler_count += 1

            log10_ratio = log10_required_over_upper(earlier_value, earlier_divisor_count)
            all_log10_ratios.append(log10_ratio)
            ratio = safe_ratio_from_log10(log10_ratio)

            if closest_log10_ratio is None or log10_ratio < closest_log10_ratio:
                closest_log10_ratio = log10_ratio
                closest_example = {
                    "left_prime": int(left_prime),
                    "right_prime": int(right_prime),
                    "winner_value": winner_value,
                    "winner_divisor_count": winner_divisor_count,
                    "earlier_value": earlier_value,
                    "earlier_divisor_count": earlier_divisor_count,
                    "log10_required_over_upper": log10_ratio,
                    "required_over_upper": ratio,
                }

            row = class_rows.get(earlier_divisor_count)
            if row is None or log10_ratio < row.min_log10_required_over_upper:
                class_rows[earlier_divisor_count] = ClassRow(
                    earlier_divisor_count=earlier_divisor_count,
                    candidate_count=1 if row is None else row.candidate_count + 1,
                    min_earlier_value=earlier_value if row is None else min(row.min_earlier_value, earlier_value),
                    min_log10_required_over_upper=log10_ratio,
                    min_required_over_upper=ratio,
                    closest_left_prime=int(left_prime),
                    closest_right_prime=int(right_prime),
                    closest_earlier_value=earlier_value,
                    closest_winner_value=winner_value,
                )
            else:
                class_rows[earlier_divisor_count] = ClassRow(
                    earlier_divisor_count=earlier_divisor_count,
                    candidate_count=row.candidate_count + 1,
                    min_earlier_value=min(row.min_earlier_value, earlier_value),
                    min_log10_required_over_upper=row.min_log10_required_over_upper,
                    min_required_over_upper=row.min_required_over_upper,
                    closest_left_prime=row.closest_left_prime,
                    closest_right_prime=row.closest_right_prime,
                    closest_earlier_value=row.closest_earlier_value,
                    closest_winner_value=row.closest_winner_value,
                )

    summary_rows = [class_rows[key].to_dict() for key in sorted(class_rows)]
    payload = {
        "interval": {"lo": lo, "hi": hi},
        "d4_gap_count": d4_gap_count,
        "earlier_candidate_count": earlier_candidate_count,
        "exact_spoiler_count": exact_spoiler_count,
        "all_candidates_geometrically_impossible": exact_spoiler_count == 0
        and (closest_log10_ratio is not None and closest_log10_ratio >= 0.0),
        "closest_log10_required_over_upper": closest_log10_ratio,
        "closest_required_over_upper": None
        if closest_log10_ratio is None
        else safe_ratio_from_log10(closest_log10_ratio),
        "closest_example": closest_example,
        "class_summary": summary_rows,
        "log10_required_over_upper_summary": {
            "min": None if not all_log10_ratios else float(min(all_log10_ratios)),
            "median": None if not all_log10_ratios else float(np.median(all_log10_ratios)),
            "max": None if not all_log10_ratios else float(max(all_log10_ratios)),
        },
    }
    return payload


def make_plots(payload: dict[str, object], prefix: Path, title: str) -> list[Path]:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    rows = payload["class_summary"]
    if not rows:
        return []

    classes = [row["earlier_divisor_count"] for row in rows]
    min_observed = [row["min_earlier_value"] for row in rows]
    allowed_max = [4.0 ** (1.0 / (divisor_count - 4)) for divisor_count in classes]
    log10_ratios = payload["log10_required_over_upper_summary"]

    out_paths: list[Path] = []

    plt.figure(figsize=(10, 6))
    plt.plot(classes, min_observed, marker="o", linewidth=2, label="Minimum observed earlier value")
    plt.plot(
        classes,
        allowed_max,
        marker="s",
        linewidth=2,
        label="Maximum earlier value allowed by spoiler inequality",
    )
    plt.yscale("log")
    plt.xlabel("Earlier divisor count")
    plt.ylabel("Value")
    plt.title(f"{title}\nObserved earlier values versus allowed spoiler threshold")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    threshold_path = prefix.with_name(prefix.name + "_class_thresholds.png")
    plt.tight_layout()
    plt.savefig(threshold_path, dpi=180)
    plt.close()
    out_paths.append(threshold_path)

    plt.figure(figsize=(10, 6))
    plt.bar(classes, [row["min_log10_required_over_upper"] for row in rows], width=0.8)
    plt.axhline(0.0, color="red", linestyle="--", linewidth=2, label="Impossibility boundary")
    plt.xlabel("Earlier divisor count")
    plt.ylabel("Minimum log10(required lower bound / universal upper bound)")
    plt.title(f"{title}\nClosest observed candidate by divisor class")
    plt.grid(True, axis="y", alpha=0.25)
    plt.legend()
    margin_path = prefix.with_name(prefix.name + "_class_ratio.png")
    plt.tight_layout()
    plt.savefig(margin_path, dpi=180)
    plt.close()
    out_paths.append(margin_path)

    return out_paths


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = analyze_interval(args.lo, args.hi)
    plot_paths = make_plots(payload, args.plot_prefix, args.title)
    payload["plot_paths"] = [str(path) for path in plot_paths]

    serialized = json.dumps(payload, indent=2)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
