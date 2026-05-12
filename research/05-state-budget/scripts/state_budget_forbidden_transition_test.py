#!/usr/bin/env python3
"""Test whether square-room side forbids next PGS chamber states."""

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
MIN_TRAIN_BASE_ROWS = 6
MIN_TRAIN_SIDE_ROWS = 3
MIN_ELIGIBLE_ROWS = 100
MAX_VIOLATION_RATE = 0.05
MATCH_MODES = (
    "base",
    "mod30",
    "exact_tail",
    "mod30_exact_tail",
)
FOLD_FIELDS = (
    "match_mode",
    "heldout_power",
    "train_rows",
    "heldout_rows",
    "eligible_rows",
    "shrunk_rows",
    "violations",
    "average_base_menu_size",
    "average_side_menu_size",
    "average_shrinkage",
    "violation_rate",
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Ask whether square-room side removes possible next reduced states "
            "inside matched PGS current-chamber facts."
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
        help="Directory for forbidden-transition outputs.",
    )
    parser.add_argument("--min-power", type=int, default=DEFAULT_MIN_POWER)
    parser.add_argument("--max-power", type=int, default=DEFAULT_MAX_POWER)
    return parser


def load_detail_rows(detail_csv: Path) -> list[dict[str, object]]:
    """Load catalog detail rows."""
    if not detail_csv.exists():
        raise FileNotFoundError(f"detail CSV does not exist: {detail_csv}")
    with detail_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("detail CSV must contain at least one row")
    return rows


def build_transitions(
    detail_rows: list[dict[str, object]],
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, object]]:
    """Return d=4 current rows with previous and next chamber context."""
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
            room_root = int(nextprime(math.isqrt(w)))
            room_boundary = room_root * room_root
            tail_length = q - w
            room_size = room_boundary - w
            if room_size <= 0:
                raise ValueError(f"nonpositive square room for winner {w}")

            transitions.append(
                {
                    "power": power,
                    "previous_reduced_state": phase_probe.reduced_state(previous_row),
                    "current_winner_parity": "even" if w % 2 == 0 else "odd",
                    "current_carrier_family": str(current_row["carrier_family"]),
                    "current_winner_offset": int(current_row["next_peak_offset"]),
                    "current_first_open_offset": int(current_row["first_open_offset"]),
                    "endpoint_mod30": q % 30,
                    "tail_length": tail_length,
                    "square_room_utilization": tail_length / room_size,
                    "next_reduced_state": phase_probe.reduced_state(next_row),
                }
            )

    if not transitions:
        raise ValueError("requested power range did not produce any d=4 transitions")
    return transitions


def base_key(row: dict[str, object]) -> tuple[object, ...]:
    """Return the matched current PGS chamber fact cell."""
    return (
        str(row["previous_reduced_state"]),
        str(row["current_winner_parity"]),
        str(row["current_carrier_family"]),
        int(row["current_winner_offset"]),
        int(row["current_first_open_offset"]),
    )


def match_key(row: dict[str, object], match_mode: str) -> tuple[object, ...]:
    """Return the matched cell for one fixed mode."""
    key = base_key(row)
    if match_mode == "base":
        return key
    if match_mode == "mod30":
        return (*key, int(row["endpoint_mod30"]))
    if match_mode == "exact_tail":
        return (*key, int(row["tail_length"]))
    if match_mode == "mod30_exact_tail":
        return (*key, int(row["endpoint_mod30"]), int(row["tail_length"]))
    raise KeyError(f"unknown match mode: {match_mode}")


def median(values: list[float]) -> float:
    """Return the upper median for deterministic low/high splitting."""
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def train_rules(
    train_rows: list[dict[str, object]],
    match_mode: str,
) -> dict[tuple[object, ...], dict[str, object]]:
    """Return train-only state menus for square-room low and high sides."""
    rows_by_cell: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in train_rows:
        rows_by_cell[match_key(row, match_mode)].append(row)

    rules: dict[tuple[object, ...], dict[str, object]] = {}
    for key, rows in rows_by_cell.items():
        if len(rows) < MIN_TRAIN_BASE_ROWS:
            continue
        cutoff = median([float(row["square_room_utilization"]) for row in rows])
        side_rows = {
            "low": [row for row in rows if float(row["square_room_utilization"]) < cutoff],
            "high": [row for row in rows if float(row["square_room_utilization"]) >= cutoff],
        }
        base_menu = {str(row["next_reduced_state"]) for row in rows}
        side_menus = {
            side: {str(row["next_reduced_state"]) for row in members}
            for side, members in side_rows.items()
        }
        rules[key] = {
            "cutoff": cutoff,
            "base_menu": base_menu,
            "side_menus": side_menus,
            "side_counts": {side: len(members) for side, members in side_rows.items()},
        }
    return rules


def score_fold(
    transitions: list[dict[str, object]],
    *,
    match_mode: str,
    heldout_power: int,
) -> dict[str, object]:
    """Score one deterministic held-out power."""
    train_rows = [row for row in transitions if int(row["power"]) != heldout_power]
    heldout_rows = [row for row in transitions if int(row["power"]) == heldout_power]
    rules = train_rules(train_rows, match_mode)

    eligible_rows = 0
    shrunk_rows = 0
    violations = 0
    base_menu_size_sum = 0
    side_menu_size_sum = 0
    shrinkage_sum = 0

    for row in heldout_rows:
        rule = rules.get(match_key(row, match_mode))
        if rule is None:
            continue
        side = (
            "low"
            if float(row["square_room_utilization"]) < float(rule["cutoff"])
            else "high"
        )
        if int(rule["side_counts"][side]) < MIN_TRAIN_SIDE_ROWS:
            continue

        base_menu = set(rule["base_menu"])
        side_menu = set(rule["side_menus"][side])
        shrinkage = len(base_menu) - len(side_menu)
        eligible_rows += 1
        base_menu_size_sum += len(base_menu)
        side_menu_size_sum += len(side_menu)
        shrinkage_sum += shrinkage
        if shrinkage > 0:
            shrunk_rows += 1
        if str(row["next_reduced_state"]) not in side_menu:
            violations += 1

    return {
        "match_mode": match_mode,
        "heldout_power": heldout_power,
        "train_rows": len(train_rows),
        "heldout_rows": len(heldout_rows),
        "eligible_rows": eligible_rows,
        "shrunk_rows": shrunk_rows,
        "violations": violations,
        "average_base_menu_size": (
            base_menu_size_sum / eligible_rows if eligible_rows else 0.0
        ),
        "average_side_menu_size": (
            side_menu_size_sum / eligible_rows if eligible_rows else 0.0
        ),
        "average_shrinkage": shrinkage_sum / eligible_rows if eligible_rows else 0.0,
        "violation_rate": violations / eligible_rows if eligible_rows else 0.0,
    }


def summarize_mode(fold_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return aggregate verdict payload for one match mode."""
    eligible_rows = sum(int(row["eligible_rows"]) for row in fold_rows)
    shrunk_rows = sum(int(row["shrunk_rows"]) for row in fold_rows)
    violations = sum(int(row["violations"]) for row in fold_rows)
    shrinkage_sum = sum(
        float(row["average_shrinkage"]) * int(row["eligible_rows"])
        for row in fold_rows
    )
    avg_shrinkage = shrinkage_sum / eligible_rows if eligible_rows else 0.0
    violation_rate = violations / eligible_rows if eligible_rows else 0.0
    scoreable_folds = sum(int(row["eligible_rows"]) > 0 for row in fold_rows)

    if eligible_rows < MIN_ELIGIBLE_ROWS or scoreable_folds < 3:
        verdict = "unresolved"
    elif avg_shrinkage <= 0.0:
        verdict = "does_not"
    elif violation_rate <= MAX_VIOLATION_RATE:
        verdict = "does"
    else:
        verdict = "does_not"

    return {
        "match_mode": str(fold_rows[0]["match_mode"]) if fold_rows else "",
        "folds": len(fold_rows),
        "scoreable_folds": scoreable_folds,
        "eligible_rows": eligible_rows,
        "shrunk_rows": shrunk_rows,
        "violations": violations,
        "average_shrinkage": avg_shrinkage,
        "violation_rate": violation_rate,
        "verdict": verdict,
    }


def summary_path(output_dir: Path) -> Path:
    """Return the summary JSON path."""
    return output_dir / "state_budget_forbidden_transition_summary.json"


def fold_path(output_dir: Path) -> Path:
    """Return the per-fold CSV path."""
    return output_dir / "state_budget_forbidden_transition_folds.csv"


def evaluate_surface(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return fold rows and summary payload for one retained surface."""
    detail_rows = load_detail_rows(detail_csv)
    transitions = build_transitions(
        detail_rows,
        min_power=min_power,
        max_power=max_power,
    )

    fold_rows: list[dict[str, object]] = []
    powers = sorted({int(row["power"]) for row in transitions})
    for match_mode in MATCH_MODES:
        for heldout_power in powers:
            fold_rows.append(
                score_fold(
                    transitions,
                    match_mode=match_mode,
                    heldout_power=heldout_power,
                )
            )

    modes = [
        summarize_mode([row for row in fold_rows if str(row["match_mode"]) == match_mode])
        for match_mode in MATCH_MODES
    ]
    summary = {
        "question": (
            "Does square-room side forbid next reduced states inside matched "
            "current PGS chamber facts?"
        ),
        "detail_csv": str(detail_csv),
        "min_power": min_power,
        "max_power": max_power,
        "transition_count": len(transitions),
        "rules": {
            "min_train_base_rows": MIN_TRAIN_BASE_ROWS,
            "min_train_side_rows": MIN_TRAIN_SIDE_ROWS,
            "min_eligible_rows": MIN_ELIGIBLE_ROWS,
            "max_violation_rate": MAX_VIOLATION_RATE,
        },
        "modes": modes,
    }
    return fold_rows, summary


def main(argv: list[str] | None = None) -> int:
    """Run the forbidden-transition test and write artifacts."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fold_rows, summary = evaluate_surface(
        args.detail_csv,
        min_power=args.min_power,
        max_power=args.max_power,
    )

    with fold_path(args.output_dir).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FOLD_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(fold_rows)
    summary_path(args.output_dir).write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
