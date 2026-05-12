#!/usr/bin/env python3
"""Run residue-matched pairwise ruler tests for PGS state-budget rows."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from sympy import nextprime


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import gwr_phase_budget_hidden_state_probe as phase_probe


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DETAIL_CSV = ROOT / "research" / "03-gap-types" / "output" / "gwr_dni_gap_type_catalog_details.csv"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "05-state-budget" / "output"
DEFAULT_MIN_POWER = 12
DEFAULT_MAX_POWER = 18
DEFAULT_MIN_CLASS_COUNT = 1
DEFAULT_MIN_DECISIVE_PAIRS = 100
DEFAULT_MIN_CONTROL_MARGIN = 15
MATCH_MODES = (
    "base",
    "mod30",
    "mod30_prev_gap",
    "mod210",
)
PER_POWER_FIELDS = (
    "match_mode",
    "measure",
    "power",
    "eligible_cells",
    "decisive_pairs",
    "signed_advantage",
    "tie_pairs",
    "advantage_share",
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Ask whether the square ruler still beats tail length after residue "
            "context is included in the matched-pair cells."
        ),
    )
    parser.add_argument(
        "--detail-csv",
        type=Path,
        default=DEFAULT_DETAIL_CSV,
        help="Catalog detail CSV emitted by gwr_dni_gap_type_catalog.py.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for residue-matched pairwise outputs.",
    )
    parser.add_argument("--min-power", type=int, default=DEFAULT_MIN_POWER)
    parser.add_argument("--max-power", type=int, default=DEFAULT_MAX_POWER)
    parser.add_argument(
        "--min-class-count",
        type=int,
        default=DEFAULT_MIN_CLASS_COUNT,
        help="Minimum target and non-target rows required inside a matched cell.",
    )
    parser.add_argument(
        "--min-decisive-pairs",
        type=int,
        default=DEFAULT_MIN_DECISIVE_PAIRS,
        help="Minimum aggregate decisive pairs required for a non-unresolved verdict.",
    )
    parser.add_argument(
        "--min-control-margin",
        type=int,
        default=DEFAULT_MIN_CONTROL_MARGIN,
        help="Minimum signed-win margin required over the tail-length control.",
    )
    return parser


def per_power_path(output_dir: Path) -> Path:
    """Return the per-power CSV path."""
    return output_dir / "state_budget_residue_matched_pair_per_power.csv"


def summary_path(output_dir: Path) -> Path:
    """Return the summary JSON path."""
    return output_dir / "state_budget_residue_matched_pair_summary.json"


def build_transitions(
    detail_rows: list[dict[str, object]],
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, object]]:
    """Return current d=4 rows with residue and gap context."""
    by_surface: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in detail_rows:
        by_surface[str(row["surface_label"])].append(row)

    transitions: list[dict[str, object]] = []
    for surface_label in sorted(by_surface):
        surface_rows = sorted(
            by_surface[surface_label],
            key=lambda row: int(row["surface_row_index"]),
        )
        power_text = str(surface_rows[0]["power"])
        if power_text == "":
            continue
        power = int(power_text)
        if power < min_power or power > max_power:
            continue

        for previous_row, current_row, next_row in zip(
            surface_rows[:-2],
            surface_rows[1:-1],
            surface_rows[2:],
        ):
            if int(current_row["next_dmin"]) != 4:
                continue
            w = int(current_row["winner"])
            q = int(current_row["next_right_prime"])
            left_prime = int(current_row["current_right_prime"])
            next_prime_square_root = int(nextprime(math.isqrt(w)))
            next_prime_square = next_prime_square_root * next_prime_square_root

            transitions.append(
                {
                    "power": power,
                    "previous_reduced_state": phase_probe.reduced_state(previous_row),
                    "current_winner_parity": "even" if w % 2 == 0 else "odd",
                    "current_carrier_family": str(current_row["carrier_family"]),
                    "current_winner_offset": int(current_row["next_peak_offset"]),
                    "current_first_open_offset": int(current_row["first_open_offset"]),
                    "left_prime_mod30": left_prime % 30,
                    "left_prime_mod210": left_prime % 210,
                    "previous_gap_width": int(previous_row["next_gap_width"]),
                    "current_gap_width": int(current_row["next_gap_width"]),
                    "next_is_triad": int(
                        str(next_row["carrier_family"]) == "odd_semiprime"
                        and int(next_row["next_dmin"]) <= 4
                    ),
                    "square_ruler": (q - w) / (next_prime_square - w),
                    "tail_length": q - w,
                }
            )

    if not transitions:
        raise ValueError("requested power range did not produce any d=4 transitions")
    return transitions


def base_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the PGS-native matched current-gap fact cell."""
    return (
        str(row["previous_reduced_state"]),
        str(row["current_winner_parity"]),
        str(row["current_carrier_family"]),
        int(row["current_winner_offset"]),
        int(row["current_first_open_offset"]),
    )


def matched_key(row: dict[str, object], match_mode: str) -> tuple[object, ...]:
    """Return the matched cell for one residue-control mode."""
    key = base_key(row)
    if match_mode == "base":
        return key
    if match_mode == "mod30":
        return (*key, int(row["left_prime_mod30"]))
    if match_mode == "mod30_prev_gap":
        return (
            *key,
            int(row["left_prime_mod30"]),
            int(row["previous_gap_width"]),
        )
    if match_mode == "mod210":
        return (*key, int(row["left_prime_mod210"]))
    raise KeyError(f"unknown match mode: {match_mode}")


def compare_pairs(
    targets: list[dict[str, object]],
    non_targets: list[dict[str, object]],
    *,
    value_field: str,
) -> tuple[int, int, int]:
    """Return pair count, signed advantage, and ties."""
    pairs = 0
    signed_advantage = 0
    ties = 0
    for target in targets:
        for non_target in non_targets:
            pairs += 1
            target_value = float(target[value_field])
            non_target_value = float(non_target[value_field])
            if target_value < non_target_value:
                signed_advantage += 1
            elif target_value > non_target_value:
                signed_advantage -= 1
            else:
                ties += 1
    return pairs, signed_advantage, ties


def measure_rows(
    transitions: list[dict[str, object]],
    *,
    match_mode: str,
    measure: str,
    value_field: str,
    min_class_count: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return per-power and aggregate pairwise rows."""
    rows_by_cell: dict[tuple[int, tuple[object, ...]], list[dict[str, object]]] = defaultdict(list)
    for row in transitions:
        rows_by_cell[(int(row["power"]), matched_key(row, match_mode))].append(row)

    per_power: dict[int, dict[str, int | str]] = defaultdict(
        lambda: {
            "match_mode": match_mode,
            "measure": measure,
            "eligible_cells": 0,
            "decisive_pairs": 0,
            "signed_advantage": 0,
            "tie_pairs": 0,
        }
    )
    for (power, _key), members in rows_by_cell.items():
        targets = [row for row in members if int(row["next_is_triad"]) == 1]
        non_targets = [row for row in members if int(row["next_is_triad"]) == 0]
        if len(targets) < min_class_count or len(non_targets) < min_class_count:
            continue
        pairs, signed_advantage, ties = compare_pairs(
            targets,
            non_targets,
            value_field=value_field,
        )
        per_power[power]["eligible_cells"] = int(per_power[power]["eligible_cells"]) + 1
        per_power[power]["decisive_pairs"] = int(per_power[power]["decisive_pairs"]) + pairs
        per_power[power]["signed_advantage"] = int(per_power[power]["signed_advantage"]) + signed_advantage
        per_power[power]["tie_pairs"] = int(per_power[power]["tie_pairs"]) + ties

    per_power_rows = []
    for power in sorted(per_power):
        row = dict(per_power[power])
        pairs = int(row["decisive_pairs"])
        row["power"] = power
        row["advantage_share"] = int(row["signed_advantage"]) / pairs if pairs else None
        per_power_rows.append(row)

    summary = {
        "match_mode": match_mode,
        "measure": measure,
        "eligible_cells": sum(int(row["eligible_cells"]) for row in per_power_rows),
        "decisive_pairs": sum(int(row["decisive_pairs"]) for row in per_power_rows),
        "signed_advantage": sum(int(row["signed_advantage"]) for row in per_power_rows),
        "tie_pairs": sum(int(row["tie_pairs"]) for row in per_power_rows),
    }
    summary["advantage_share"] = (
        summary["signed_advantage"] / summary["decisive_pairs"]
        if summary["decisive_pairs"]
        else None
    )
    return per_power_rows, summary


def verdict(
    square_summary: dict[str, object],
    tail_summary: dict[str, object],
    *,
    min_decisive_pairs: int,
    min_control_margin: int,
) -> str:
    """Return the finite residue-matched verdict."""
    if int(square_summary["decisive_pairs"]) < min_decisive_pairs:
        return "unresolved"
    square_advantage = int(square_summary["signed_advantage"])
    tail_advantage = int(tail_summary["signed_advantage"])
    if square_advantage <= 0:
        return "does_not"
    if square_advantage - tail_advantage < min_control_margin:
        return "unresolved"
    return "does"


def evaluate_surface(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
    min_class_count: int,
    min_decisive_pairs: int,
    min_control_margin: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return per-power rows and summary for all residue match modes."""
    transitions = build_transitions(
        phase_probe.load_detail_rows(detail_csv),
        min_power=min_power,
        max_power=max_power,
    )
    all_rows = []
    mode_summaries = []
    for match_mode in MATCH_MODES:
        square_rows, square_summary = measure_rows(
            transitions,
            match_mode=match_mode,
            measure="square_ruler",
            value_field="square_ruler",
            min_class_count=min_class_count,
        )
        tail_rows, tail_summary = measure_rows(
            transitions,
            match_mode=match_mode,
            measure="tail_length",
            value_field="tail_length",
            min_class_count=min_class_count,
        )
        mode_summaries.append(
            {
                "match_mode": match_mode,
                "measure_summaries": [square_summary, tail_summary],
                "verdict": verdict(
                    square_summary,
                    tail_summary,
                    min_decisive_pairs=min_decisive_pairs,
                    min_control_margin=min_control_margin,
                ),
            }
        )
        all_rows.extend(square_rows)
        all_rows.extend(tail_rows)

    summary = {
        "min_power": min_power,
        "max_power": max_power,
        "min_class_count": min_class_count,
        "min_decisive_pairs": min_decisive_pairs,
        "min_control_margin": min_control_margin,
        "mode_summaries": mode_summaries,
    }
    return all_rows, summary


def format_number(value: object) -> str:
    """Format numeric CSV fields with blank None values."""
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_per_power(path: Path, rows: list[dict[str, object]]) -> None:
    """Write per-power rows with LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(PER_POWER_FIELDS),
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: format_number(row.get(field)) for field in PER_POWER_FIELDS})


def write_summary(path: Path, summary: dict[str, object]) -> None:
    """Write summary JSON with LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the residue-matched pairwise test and write artifacts."""
    args = build_parser().parse_args(argv)
    if args.min_class_count < 1:
        raise ValueError("min class count must be at least 1")
    if args.min_decisive_pairs < 1:
        raise ValueError("min decisive pairs must be at least 1")
    if args.min_control_margin < 1:
        raise ValueError("min control margin must be at least 1")

    per_power_rows, summary = evaluate_surface(
        args.detail_csv,
        min_power=args.min_power,
        max_power=args.max_power,
        min_class_count=args.min_class_count,
        min_decisive_pairs=args.min_decisive_pairs,
        min_control_margin=args.min_control_margin,
    )
    write_per_power(per_power_path(args.output_dir), per_power_rows)
    write_summary(summary_path(args.output_dir), summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
