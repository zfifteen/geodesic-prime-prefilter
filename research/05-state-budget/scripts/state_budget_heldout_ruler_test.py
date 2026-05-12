#!/usr/bin/env python3
"""Run the held-out square-budget ruler test for the PGS state-budget probe."""

from __future__ import annotations

import argparse
import csv
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
DEFAULT_BALANCE_FLOOR = 0.10
DEFAULT_MIN_SCORED_ROWS = 20
OUTPUT_FIELDS = (
    "heldout_power",
    "scored_rows",
    "low_count",
    "high_count",
    "min_class_share",
    "baseline_loss",
    "budget_loss",
    "gain",
    "low_target_share",
    "high_target_share",
    "lift",
    "control_best_gain",
    "verdict",
)
CONTROL_IDS = (
    "offset_only",
    "selected_integer_family_only",
    "first_open_offset_only",
    "cyclic_budget_label",
    "wrong_square_boundary_label",
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Test whether the real square-budget ruler improves held-out "
            "next-gap prediction after standard current-gap facts are present."
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
        help="Directory for state_budget_heldout_ruler_test.csv.",
    )
    parser.add_argument(
        "--min-power",
        type=int,
        default=DEFAULT_MIN_POWER,
        help="Smallest held-out decade power.",
    )
    parser.add_argument(
        "--max-power",
        type=int,
        default=DEFAULT_MAX_POWER,
        help="Largest held-out decade power.",
    )
    parser.add_argument(
        "--balance-floor",
        type=float,
        default=DEFAULT_BALANCE_FLOOR,
        help="Minimum share required for the smaller held-out low/high class.",
    )
    parser.add_argument(
        "--min-scored-rows",
        type=int,
        default=DEFAULT_MIN_SCORED_ROWS,
        help="Minimum scored held-out rows required before a fold is decisive.",
    )
    return parser


def output_path(output_dir: Path) -> Path:
    """Return the held-out ruler test CSV path."""
    return output_dir / "state_budget_heldout_ruler_test.csv"


def reduced_state(row: dict[str, object]) -> str:
    """Return the reduced state label used by the existing catalog surface."""
    return phase_probe.reduced_state(row)


def build_transitions(
    detail_rows: list[dict[str, object]],
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, object]]:
    """Return previous/current/next rows with real and fake ruler positions."""
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
            winner = int(current_row["winner"])
            q = int(current_row["next_right_prime"])
            current_next_dmin = int(current_row["next_dmin"])
            square_budget = None
            wrong_square_budget = None

            if current_next_dmin == 4:
                next_prime_square_root = int(nextprime(math.isqrt(winner)))
                next_prime_square = next_prime_square_root * next_prime_square_root
                square_budget = (q - winner) / (next_prime_square - winner)

                wrong_square = (math.isqrt(winner) + 1) ** 2
                wrong_square_budget = (q - winner) / (wrong_square - winner)

            transitions.append(
                {
                    "surface_label": surface_label,
                    "power": power,
                    "surface_row_index": int(current_row["surface_row_index"]),
                    "winner": winner,
                    "q": q,
                    "current_gap_width": int(current_row["next_gap_width"]),
                    "current_first_open_offset": int(current_row["first_open_offset"]),
                    "current_winner_offset": int(current_row["next_peak_offset"]),
                    "current_winner_parity": "even" if winner % 2 == 0 else "odd",
                    "current_carrier_family": str(current_row["carrier_family"]),
                    "current_next_dmin": current_next_dmin,
                    "previous_reduced_state": reduced_state(previous_row),
                    "square_budget": square_budget,
                    "wrong_square_budget": wrong_square_budget,
                    "next_is_triad": int(
                        str(next_row["carrier_family"]) == "odd_semiprime"
                        and int(next_row["next_dmin"]) <= 4
                    ),
                }
            )

    if not transitions:
        raise ValueError("requested power range did not produce any transitions")
    return transitions


def matched_cell_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the full standard current-gap control cell."""
    return (
        str(row["previous_reduced_state"]),
        str(row["current_winner_parity"]),
        str(row["current_carrier_family"]),
        int(row["current_winner_offset"]),
        int(row["current_first_open_offset"]),
    )


def median_by_cell(
    rows: list[dict[str, object]],
    value_field: str,
) -> dict[tuple[object, ...], float]:
    """Return medians for cells whose training rows split into both classes."""
    values_by_cell: dict[tuple[object, ...], list[float]] = defaultdict(list)
    for row in rows:
        if int(row["current_next_dmin"]) != 4:
            continue
        value = row[value_field]
        if value is None:
            continue
        values_by_cell[matched_cell_key(row)].append(float(value))

    medians = {}
    for key, values in values_by_cell.items():
        ordered = sorted(values)
        median = ordered[len(ordered) // 2]
        low_count = sum(1 for value in ordered if value < median)
        high_count = len(ordered) - low_count
        if low_count > 0 and high_count > 0:
            medians[key] = median
    return medians


def label_for(
    row: dict[str, object],
    *,
    medians: dict[tuple[object, ...], float],
    value_field: str,
    low_label: str = "d4_low",
    high_label: str = "d4_high",
) -> str | None:
    """Return a low/high ruler label for one row, or None if unscoreable."""
    if int(row["current_next_dmin"]) != 4:
        return None
    key = matched_cell_key(row)
    if key not in medians or row[value_field] is None:
        return None
    return low_label if float(row[value_field]) < medians[key] else high_label


def reversed_label(label: str) -> str:
    """Return the opposite directional budget label."""
    if label == "d4_low":
        return "d4_high"
    if label == "d4_high":
        return "d4_low"
    raise ValueError(f"cannot reverse label: {label}")


def attach_fold_labels(
    train_rows: list[dict[str, object]],
    heldout_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Attach fold-specific real, wrong-boundary, and cyclic control labels."""
    real_medians = median_by_cell(train_rows, "square_budget")
    wrong_medians = median_by_cell(train_rows, "wrong_square_budget")

    labeled_train = []
    for row in train_rows:
        real_label = label_for(row, medians=real_medians, value_field="square_budget")
        wrong_label = label_for(
            row,
            medians=wrong_medians,
            value_field="wrong_square_budget",
            low_label="wrong_low",
            high_label="wrong_high",
        )
        if real_label is None or wrong_label is None:
            continue
        item = dict(row)
        item["budget_label"] = real_label
        item["reversed_budget_label"] = reversed_label(real_label)
        item["wrong_square_boundary_label"] = wrong_label
        labeled_train.append(item)

    labeled_heldout = []
    for row in heldout_rows:
        real_label = label_for(row, medians=real_medians, value_field="square_budget")
        wrong_label = label_for(
            row,
            medians=wrong_medians,
            value_field="wrong_square_budget",
            low_label="wrong_low",
            high_label="wrong_high",
        )
        if real_label is None or wrong_label is None:
            continue
        item = dict(row)
        item["budget_label"] = real_label
        item["reversed_budget_label"] = reversed_label(real_label)
        item["wrong_square_boundary_label"] = wrong_label
        labeled_heldout.append(item)

    attach_cyclic_labels(labeled_train)
    attach_cyclic_labels(labeled_heldout)
    return labeled_train, labeled_heldout


def attach_cyclic_labels(rows: list[dict[str, object]]) -> None:
    """Attach a deterministic within-power one-step shifted budget label."""
    by_power: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_power[int(row["power"])].append(row)

    for power_rows in by_power.values():
        ordered = sorted(
            power_rows,
            key=lambda row: (str(row["surface_label"]), int(row["surface_row_index"])),
        )
        if not ordered:
            continue
        labels = [str(row["budget_label"]) for row in ordered]
        shifted = labels[-1:] + labels[:-1]
        for row, label in zip(ordered, shifted):
            row["cyclic_budget_label"] = label


def laplace_probability(positive_count: int, total_count: int) -> float:
    """Return the Laplace-smoothed Bernoulli probability."""
    return (positive_count + 1.0) / (total_count + 2.0)


def probability_map(
    rows: list[dict[str, object]],
    key_func,
) -> dict[tuple[object, ...], float]:
    """Return smoothed target probabilities by context key."""
    counts: dict[tuple[object, ...], list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        key = key_func(row)
        counts[key][0] += int(row["next_is_triad"])
        counts[key][1] += 1
    return {
        key: laplace_probability(positive_count, total_count)
        for key, (positive_count, total_count) in counts.items()
    }


def mean_log_loss(
    train_rows: list[dict[str, object]],
    test_rows: list[dict[str, object]],
    key_func,
) -> float | None:
    """Return mean held-out log loss, or None when a context is unseen."""
    probabilities = probability_map(train_rows, key_func)
    loss = 0.0
    for row in test_rows:
        key = key_func(row)
        if key not in probabilities:
            return None
        probability = probabilities[key]
        loss += -(
            math.log(probability)
            if int(row["next_is_triad"])
            else math.log(1.0 - probability)
        )
    return loss / len(test_rows) if test_rows else None


def baseline_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the standard current-gap fact key."""
    return matched_cell_key(row)


def budget_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the standard fact key plus the real square-budget label."""
    return (*matched_cell_key(row), str(row["budget_label"]))


def offset_only_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the baseline key; offset is already part of the matched cell."""
    return (*matched_cell_key(row), int(row["current_winner_offset"]))


def family_only_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the baseline key; selected-integer family is already present."""
    return (*matched_cell_key(row), str(row["current_carrier_family"]))


def first_open_only_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the baseline key; first-open offset is already present."""
    return (*matched_cell_key(row), int(row["current_first_open_offset"]))


def cyclic_budget_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the standard fact key plus a cyclically shifted budget label."""
    return (*matched_cell_key(row), str(row["cyclic_budget_label"]))


def wrong_boundary_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the standard fact key plus the wrong-square-boundary label."""
    return (*matched_cell_key(row), str(row["wrong_square_boundary_label"]))


def control_key_funcs() -> dict[str, object]:
    """Return deterministic controls scored against the same baseline."""
    return {
        "offset_only": offset_only_key,
        "selected_integer_family_only": family_only_key,
        "first_open_offset_only": first_open_only_key,
        "cyclic_budget_label": cyclic_budget_key,
        "wrong_square_boundary_label": wrong_boundary_key,
    }


def target_share(rows: list[dict[str, object]]) -> float | None:
    """Return the target share for a nonempty row list."""
    if not rows:
        return None
    return sum(int(row["next_is_triad"]) for row in rows) / len(rows)


def format_number(value: float | int | None) -> str:
    """Format CSV numeric fields while preserving unresolved blanks."""
    if value is None:
        return ""
    if isinstance(value, int):
        return str(value)
    return f"{value:.12g}"


def evaluate_fold(
    rows: list[dict[str, object]],
    *,
    heldout_power: int,
    balance_floor: float,
    min_scored_rows: int,
) -> dict[str, object]:
    """Return one held-out fold verdict row."""
    train_rows = [row for row in rows if int(row["power"]) != heldout_power]
    heldout_rows = [row for row in rows if int(row["power"]) == heldout_power]
    labeled_train, labeled_heldout = attach_fold_labels(train_rows, heldout_rows)

    low_rows = [
        row for row in labeled_heldout if str(row["budget_label"]) == "d4_low"
    ]
    high_rows = [
        row for row in labeled_heldout if str(row["budget_label"]) == "d4_high"
    ]
    scored_rows = len(low_rows) + len(high_rows)
    low_count = len(low_rows)
    high_count = len(high_rows)
    min_class_share = (
        min(low_count, high_count) / scored_rows if scored_rows else 0.0
    )

    row: dict[str, object] = {
        "heldout_power": heldout_power,
        "scored_rows": scored_rows,
        "low_count": low_count,
        "high_count": high_count,
        "min_class_share": min_class_share,
        "baseline_loss": None,
        "budget_loss": None,
        "gain": None,
        "low_target_share": target_share(low_rows),
        "high_target_share": target_share(high_rows),
        "lift": None,
        "control_best_gain": None,
        "verdict": "unresolved",
    }
    if row["low_target_share"] is not None and row["high_target_share"] is not None:
        row["lift"] = float(row["low_target_share"]) - float(row["high_target_share"])

    if scored_rows < min_scored_rows:
        return row
    if low_count == 0 or high_count == 0:
        return row
    if min_class_share < balance_floor:
        return row

    baseline_loss = mean_log_loss(labeled_train, labeled_heldout, baseline_key)
    budget_loss = mean_log_loss(labeled_train, labeled_heldout, budget_key)
    if baseline_loss is None or budget_loss is None:
        return row

    gain = baseline_loss - budget_loss
    control_gains = []
    for key_func in control_key_funcs().values():
        control_loss = mean_log_loss(labeled_train, labeled_heldout, key_func)
        if control_loss is not None:
            control_gains.append(baseline_loss - control_loss)

    control_best_gain = max(control_gains) if control_gains else None
    row["baseline_loss"] = baseline_loss
    row["budget_loss"] = budget_loss
    row["gain"] = gain
    row["control_best_gain"] = control_best_gain

    if gain <= 0.0:
        row["verdict"] = "does_not"
    elif control_best_gain is not None and control_best_gain >= gain:
        row["verdict"] = "does_not"
    elif row["lift"] is None or float(row["lift"]) <= 0.0:
        row["verdict"] = "does_not"
    else:
        row["verdict"] = "does"
    return row


def evaluate_surface(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
    balance_floor: float,
    min_scored_rows: int,
) -> list[dict[str, object]]:
    """Return held-out fold rows for the requested retained surface."""
    detail_rows = phase_probe.load_detail_rows(detail_csv)
    transitions = build_transitions(
        detail_rows,
        min_power=min_power,
        max_power=max_power,
    )
    return [
        evaluate_fold(
            transitions,
            heldout_power=power,
            balance_floor=balance_floor,
            min_scored_rows=min_scored_rows,
        )
        for power in range(min_power, max_power + 1)
    ]


def write_table(path: Path, rows: list[dict[str, object]]) -> None:
    """Write the held-out fold table with LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(OUTPUT_FIELDS),
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: format_number(row[field])
                    if field != "verdict"
                    else row[field]
                    for field in OUTPUT_FIELDS
                }
            )


def main(argv: list[str] | None = None) -> int:
    """Run the held-out ruler test and write the fold table."""
    args = build_parser().parse_args(argv)
    if args.balance_floor < 0.0 or args.balance_floor > 0.5:
        raise ValueError("balance floor must be between 0.0 and 0.5")
    if args.min_scored_rows < 1:
        raise ValueError("min scored rows must be at least 1")

    rows = evaluate_surface(
        args.detail_csv,
        min_power=args.min_power,
        max_power=args.max_power,
        balance_floor=args.balance_floor,
        min_scored_rows=args.min_scored_rows,
    )
    write_table(output_path(args.output_dir), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
