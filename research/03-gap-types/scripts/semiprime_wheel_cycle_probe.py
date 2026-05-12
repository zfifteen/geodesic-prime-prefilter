#!/usr/bin/env python3
"""Test the simple odd-semiprime wheel-cycle hypothesis on typed PGS gaps."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DETAIL_CSV = ROOT / "research" / "03-gap-types" / "output" / "gwr_dni_gap_type_catalog_details.csv"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "03-gap-types" / "output" / "semiprime_wheel_cycle_probe"
POSITIONS = (2, 4, 6)
WHEEL_FIELDS: dict[str, str] = {
    "open_offset": "first_open_offset",
    "winner_offset_mod6": "next_peak_offset",
}


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Measure wheel transitions among simple odd-semiprime gap winners.",
    )
    parser.add_argument("--detail-csv", type=Path, default=DEFAULT_DETAIL_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def load_rows(detail_csv: Path) -> list[dict[str, str]]:
    """Load the typed gap catalog."""
    if not detail_csv.exists():
        raise FileNotFoundError(f"detail CSV does not exist: {detail_csv}")
    with detail_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("detail CSV must contain at least one row")
    return rows


def surface_order(rows: list[dict[str, str]]) -> list[str]:
    """Return the surface order preserved in the input CSV."""
    order: list[str] = []
    seen: set[str] = set()
    for row in rows:
        label = row["surface_display_label"]
        if label in seen:
            continue
        seen.add(label)
        order.append(label)
    return order


def is_simple_odd_semiprime(row: dict[str, str]) -> bool:
    """Return whether one row is a simple odd-semiprime winner."""
    return row["carrier_family"] == "odd_semiprime" and int(row["next_dmin"]) == 4


def advance_two(position: int) -> int:
    """Advance one position by +2 on the 2, 4, 6 wheel."""
    if position == 2:
        return 4
    if position == 4:
        return 6
    if position == 6:
        return 2
    raise ValueError(f"unsupported wheel position: {position}")


def open_offset_position(row: dict[str, str]) -> int:
    """Return the repo o2/o4/o6 position."""
    return int(row["first_open_offset"])


def winner_offset_mod6_position(row: dict[str, str]) -> int:
    """Return the winner-offset residue on the 2, 4, 6 wheel."""
    residue = int(row["next_peak_offset"]) % 6
    if residue == 0:
        return 6
    if residue in (2, 4):
        return residue
    raise ValueError(
        f"simple odd-semiprime winner has non-even offset: {row['next_peak_offset']}"
    )


def ratio(numerator: int, denominator: int) -> float:
    """Return a zero-safe ratio."""
    return numerator / denominator if denominator else 0.0


def expected_marginal_plus2(
    source_counts: Counter[int],
    target_counts: Counter[int],
    transition_count: int,
) -> float:
    """Return the independent-position expectation for +2 transitions."""
    if transition_count == 0:
        return 0.0
    value = 0.0
    for position in POSITIONS:
        value += (
            source_counts[position]
            / transition_count
            * target_counts[advance_two(position)]
            / transition_count
        )
    return value


def run_lengths(entries: list[tuple[int, dict[str, str], int]]) -> list[list[int]]:
    """Return consecutive simple-run position lists."""
    runs: list[list[int]] = []
    current: list[int] = []
    previous_index: int | None = None
    for row_index, _row, position in entries:
        if previous_index is None or row_index == previous_index + 1:
            current.append(position)
        else:
            runs.append(current)
            current = [position]
        previous_index = row_index
    if current:
        runs.append(current)
    return runs


def summarize_run_positions(runs: list[list[int]]) -> dict[str, int | float]:
    """Summarize consecutive simple runs."""
    if not runs:
        return {
            "run_count": 0,
            "max_run_length": 0,
            "longest_perfect_plus2_run": 0,
            "longest_local_plus2_run": 0,
            "run_transition_count": 0,
            "run_plus2_transition_count": 0,
            "run_plus2_transition_share": 0.0,
        }

    run_transition_count = 0
    run_plus2_transition_count = 0
    longest_perfect = 0
    longest_local = 0
    for run in runs:
        perfect = True
        local_length = 1
        longest_local = max(longest_local, local_length)
        for left, right in zip(run, run[1:]):
            run_transition_count += 1
            if right == advance_two(left):
                run_plus2_transition_count += 1
                local_length += 1
                longest_local = max(longest_local, local_length)
            else:
                perfect = False
                local_length = 1
        if perfect:
            longest_perfect = max(longest_perfect, len(run))

    return {
        "run_count": len(runs),
        "max_run_length": max(len(run) for run in runs),
        "longest_perfect_plus2_run": longest_perfect,
        "longest_local_plus2_run": longest_local,
        "run_transition_count": run_transition_count,
        "run_plus2_transition_count": run_plus2_transition_count,
        "run_plus2_transition_share": ratio(
            run_plus2_transition_count,
            run_transition_count,
        ),
    }


def summarize_entries(
    surface_label: str,
    wheel_field: str,
    gap_count: int,
    entries: list[tuple[int, dict[str, str], int]],
) -> tuple[dict[str, int | float | str], list[dict[str, int | str]]]:
    """Summarize one surface and one wheel-position definition."""
    return summarize_entry_groups(surface_label, wheel_field, gap_count, [entries])


def summarize_entry_groups(
    surface_label: str,
    wheel_field: str,
    gap_count: int,
    entry_groups: list[list[tuple[int, dict[str, str], int]]],
) -> tuple[dict[str, int | float | str], list[dict[str, int | str]]]:
    """Summarize one or more surfaces without crossing surface boundaries."""
    entries = [
        entry
        for group in entry_groups
        for entry in group
    ]
    position_counts = Counter(position for _row_index, _row, position in entries)
    transition_counts: dict[int, Counter[int]] = defaultdict(Counter)
    source_counts: Counter[int] = Counter()
    target_counts: Counter[int] = Counter()
    immediate_source_counts: Counter[int] = Counter()
    immediate_target_counts: Counter[int] = Counter()
    intervening_source_counts: Counter[int] = Counter()
    intervening_target_counts: Counter[int] = Counter()

    transition_count = 0
    plus2_count = 0
    immediate_count = 0
    immediate_plus2_count = 0
    intervening_count = 0
    intervening_plus2_count = 0
    break_count = 0
    breaks_with_intervening_complex = 0
    intervening_complex_gap_count = 0

    all_runs: list[list[int]] = []
    for group in entry_groups:
        for left, right in zip(group, group[1:]):
            left_index, _left_row, left_position = left
            right_index, _right_row, right_position = right
            has_intervening_complex = right_index > left_index + 1
            is_plus2 = right_position == advance_two(left_position)

            transition_count += 1
            transition_counts[left_position][right_position] += 1
            source_counts[left_position] += 1
            target_counts[right_position] += 1
            plus2_count += int(is_plus2)

            if has_intervening_complex:
                intervening_count += 1
                intervening_plus2_count += int(is_plus2)
                intervening_complex_gap_count += right_index - left_index - 1
                intervening_source_counts[left_position] += 1
                intervening_target_counts[right_position] += 1
            else:
                immediate_count += 1
                immediate_plus2_count += int(is_plus2)
                immediate_source_counts[left_position] += 1
                immediate_target_counts[right_position] += 1

            if not is_plus2:
                break_count += 1
                breaks_with_intervening_complex += int(has_intervening_complex)
        all_runs.extend(run_lengths(group))

    run_summary = summarize_run_positions(all_runs)
    summary = {
        "surface_display_label": surface_label,
        "wheel_field": wheel_field,
        "gap_count": gap_count,
        "simple_odd_semiprime_count": len(entries),
        "simple_odd_semiprime_share": ratio(len(entries), gap_count),
        "position_2_count": position_counts[2],
        "position_4_count": position_counts[4],
        "position_6_count": position_counts[6],
        "next_simple_transition_count": transition_count,
        "next_simple_plus2_count": plus2_count,
        "next_simple_plus2_share": ratio(plus2_count, transition_count),
        "independent_uniform_plus2_share": 1.0 / 3.0 if transition_count else 0.0,
        "independent_marginal_plus2_share": expected_marginal_plus2(
            source_counts,
            target_counts,
            transition_count,
        ),
        "immediate_simple_transition_count": immediate_count,
        "immediate_simple_plus2_count": immediate_plus2_count,
        "immediate_simple_plus2_share": ratio(immediate_plus2_count, immediate_count),
        "immediate_independent_marginal_plus2_share": expected_marginal_plus2(
            immediate_source_counts,
            immediate_target_counts,
            immediate_count,
        ),
        "intervening_complex_transition_count": intervening_count,
        "intervening_complex_plus2_count": intervening_plus2_count,
        "intervening_complex_plus2_share": ratio(
            intervening_plus2_count,
            intervening_count,
        ),
        "intervening_independent_marginal_plus2_share": expected_marginal_plus2(
            intervening_source_counts,
            intervening_target_counts,
            intervening_count,
        ),
        "intervening_complex_gap_count": intervening_complex_gap_count,
        "break_count": break_count,
        "breaks_with_intervening_complex": breaks_with_intervening_complex,
        "breaks_with_intervening_complex_share": ratio(
            breaks_with_intervening_complex,
            break_count,
        ),
        **run_summary,
    }

    matrix_rows: list[dict[str, int | str]] = []
    for current_position in POSITIONS:
        for next_position in POSITIONS:
            matrix_rows.append(
                {
                    "surface_display_label": surface_label,
                    "wheel_field": wheel_field,
                    "current_position": current_position,
                    "next_position": next_position,
                    "count": transition_counts[current_position][next_position],
                }
            )

    return summary, matrix_rows


def pooled_entries(
    rows_by_surface: dict[str, list[dict[str, str]]],
    position_of: Callable[[dict[str, str]], int],
) -> tuple[int, list[list[tuple[int, dict[str, str], int]]]]:
    """Return per-surface entries for pooled within-surface aggregation."""
    gap_count = 0
    entry_groups: list[list[tuple[int, dict[str, str], int]]] = []
    for surface_rows in rows_by_surface.values():
        gap_count += len(surface_rows)
        entry_groups.append(
            [
                (row_index, row, position_of(row))
                for row_index, row in enumerate(surface_rows)
                if is_simple_odd_semiprime(row)
            ]
        )
    return gap_count, entry_groups


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write CSV rows with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def plot_summary(
    surface_rows: list[dict[str, int | float | str]],
    matrix_rows: list[dict[str, int | str]],
    output_path: Path,
) -> None:
    """Render the measured transition result."""
    selected = ["<=10^6", "10^12", "10^15", "10^18", "pooled_within_surfaces"]
    fields = tuple(WHEEL_FIELDS)
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), constrained_layout=True)

    for field, color in zip(fields, ("#4c72b0", "#dd8452")):
        rows = [
            row for row in surface_rows
            if row["wheel_field"] == field and row["surface_display_label"] in selected
        ]
        rows.sort(key=lambda row: selected.index(str(row["surface_display_label"])))
        labels = [str(row["surface_display_label"]) for row in rows]
        values = [float(row["next_simple_plus2_share"]) for row in rows]
        axes[0, 0].plot(labels, values, marker="o", linewidth=2.0, color=color, label=field)
    axes[0, 0].axhline(1.0 / 3.0, color="#555555", linestyle="--", linewidth=1.2, label="uniform 1/3")
    axes[0, 0].set_title("+2 rate between consecutive simple odd-semiprime winners")
    axes[0, 0].set_ylabel("share")
    axes[0, 0].tick_params(axis="x", rotation=20)
    axes[0, 0].set_ylim(0.0, 1.0)
    axes[0, 0].grid(axis="y", alpha=0.25)
    axes[0, 0].legend()

    for field, color in zip(fields, ("#4c72b0", "#dd8452")):
        rows = [
            row for row in surface_rows
            if row["wheel_field"] == field and row["surface_display_label"] in selected
        ]
        rows.sort(key=lambda row: selected.index(str(row["surface_display_label"])))
        labels = [str(row["surface_display_label"]) for row in rows]
        values = [float(row["breaks_with_intervening_complex_share"]) for row in rows]
        axes[0, 1].plot(labels, values, marker="o", linewidth=2.0, color=color, label=field)
    axes[0, 1].set_title("Share of +2 breaks with a non-simple gap in between")
    axes[0, 1].set_ylabel("share of breaks")
    axes[0, 1].tick_params(axis="x", rotation=20)
    axes[0, 1].set_ylim(0.0, 1.0)
    axes[0, 1].grid(axis="y", alpha=0.25)
    axes[0, 1].legend()

    for axis, field in zip(axes[1], fields):
        pooled = [
            row for row in matrix_rows
            if row["wheel_field"] == field
            and row["surface_display_label"] == "pooled_within_surfaces"
        ]
        matrix = np.zeros((3, 3), dtype=float)
        for row in pooled:
            i = POSITIONS.index(int(row["current_position"]))
            j = POSITIONS.index(int(row["next_position"]))
            matrix[i, j] = int(row["count"])
        row_totals = matrix.sum(axis=1)
        for index, total in enumerate(row_totals):
            if total:
                matrix[index, :] /= total
        image = axis.imshow(matrix, cmap="viridis", vmin=0.0, vmax=1.0)
        axis.set_title(f"Pooled transition matrix: {field}")
        axis.set_xticks(range(3))
        axis.set_xticklabels(POSITIONS)
        axis.set_yticks(range(3))
        axis.set_yticklabels(POSITIONS)
        axis.set_xlabel("next simple position")
        axis.set_ylabel("current simple position")
        for i in range(3):
            for j in range(3):
                axis.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white")
        fig.colorbar(image, ax=axis, fraction=0.046, pad=0.04)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220)
    plt.close(fig)


def summarize(rows: list[dict[str, str]]) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    """Build the complete probe summary."""
    order = surface_order(rows)
    rows_by_surface = {
        label: [row for row in rows if row["surface_display_label"] == label]
        for label in order
    }
    position_functions: dict[str, Callable[[dict[str, str]], int]] = {
        "open_offset": open_offset_position,
        "winner_offset_mod6": winner_offset_mod6_position,
    }

    surface_summaries: list[dict[str, object]] = []
    matrix_rows: list[dict[str, object]] = []
    for wheel_field, position_of in position_functions.items():
        for surface_label in order:
            surface_entries = [
                (row_index, row, position_of(row))
                for row_index, row in enumerate(rows_by_surface[surface_label])
                if is_simple_odd_semiprime(row)
            ]
            summary, matrix = summarize_entries(
                surface_label,
                wheel_field,
                len(rows_by_surface[surface_label]),
                surface_entries,
            )
            surface_summaries.append(summary)
            matrix_rows.extend(matrix)

        gap_count, entry_groups = pooled_entries(rows_by_surface, position_of)
        summary, matrix = summarize_entry_groups(
            "pooled_within_surfaces",
            wheel_field,
            gap_count,
            entry_groups,
        )
        surface_summaries.append(summary)
        matrix_rows.extend(matrix)

    selected_labels = {"<=10^6", "10^12", "10^15", "10^18", "pooled_within_surfaces"}
    headline = [
        row for row in surface_summaries
        if row["wheel_field"] == "open_offset"
        and row["surface_display_label"] in selected_labels
    ]
    summary = {
        "hypothesis": (
            "Consecutive simple odd-semiprime gap winners advance by +2 on "
            "the 2,4,6 wheel, and +2 breaks are mainly reset by intervening "
            "non-simple gaps."
        ),
        "input_detail_csv": str(DEFAULT_DETAIL_CSV),
        "simple_winner_definition": {
            "carrier_family": "odd_semiprime",
            "next_dmin": 4,
        },
        "wheel_fields": {
            "open_offset": "repo o2/o4/o6 first_open_offset",
            "winner_offset_mod6": "GWR winner offset modulo 6, with 0 written as 6",
        },
        "headline_open_offset_rows": headline,
        "surface_summaries": surface_summaries,
    }
    return summary, surface_summaries, matrix_rows


def main() -> int:
    """Run the probe and write artifacts."""
    args = build_parser().parse_args()
    rows = load_rows(args.detail_csv)
    summary, surface_summaries, matrix_rows = summarize(rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.output_dir / "summary.json"
    surface_csv_path = args.output_dir / "surface_summary.csv"
    matrix_csv_path = args.output_dir / "transition_matrix.csv"
    plot_path = args.output_dir / "semiprime_wheel_cycle_probe.png"

    summary["input_detail_csv"] = str(args.detail_csv)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_csv(surface_csv_path, surface_summaries, list(surface_summaries[0].keys()))
    write_csv(matrix_csv_path, matrix_rows, list(matrix_rows[0].keys()))
    plot_summary(surface_summaries, matrix_rows, plot_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
