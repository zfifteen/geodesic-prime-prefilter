#!/usr/bin/env python3
"""Sweep current-chamber divisor-field carriers against tail plus residue controls."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

import gwr_phase_budget_hidden_state_probe as phase_probe
from z_band_prime_composite_field import divisor_counts_segment


DEFAULT_DETAIL_CSV = ROOT / "research" / "03-gap-types" / "output" / "gwr_dni_gap_type_catalog_details.csv"
DEFAULT_OUTPUT_DIR = ROOT / "research" / "05-state-budget" / "output"
DEFAULT_MIN_POWER = 12
DEFAULT_MAX_POWER = 18
MIN_TOTAL_DECISIVE_PAIRS = 5000
MIN_FOLD_DECISIVE_PAIRS = 100
MIN_DIRECTIONAL_FOLDS = 6
MIN_FIXED_MARGIN = 50
MIN_PROPORTIONAL_MARGIN = 0.005

MATCH_MODES = (
    "mod30",
    "mod30_prev_gap_bin",
    "mod30_prev_gap_exact",
)
CANDIDATE_MEASURES = (
    "d4_count",
    "d4_span",
    "d4_last_to_endpoint",
    "d4_centroid_offset",
    "divisor_sum",
    "divisor_mean",
    "low_divisor_load",
    "tail_mod30",
    "tail_mod210",
    "endpoint_mod210",
    "current_gap_width",
)
CONTROL_MEASURES = (
    "tail_length",
)
FOLD_FIELDS = (
    "match_mode",
    "measure",
    "measure_role",
    "heldout_power",
    "train_direction",
    "eligible_cells",
    "decisive_pairs",
    "raw_signed_advantage",
    "oriented_signed_advantage",
    "tie_pairs",
    "advantage_share",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Test scalar PGS-native current-chamber quantities as ordering "
            "carriers after endpoint residue and tail controls."
        ),
    )
    parser.add_argument("--detail-csv", type=Path, default=DEFAULT_DETAIL_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-power", type=int, default=DEFAULT_MIN_POWER)
    parser.add_argument("--max-power", type=int, default=DEFAULT_MAX_POWER)
    return parser


def previous_gap_bin(width: int) -> str:
    if width <= 6:
        return "le6"
    if width <= 12:
        return "8_12"
    if width <= 20:
        return "14_20"
    return "gt20"


def divisor_payload(left_prime: int, right_prime: int) -> dict[str, float | int]:
    counts = [int(value) for value in divisor_counts_segment(left_prime + 1, right_prime)]
    d4_offsets = [
        offset
        for offset, divisor_count in enumerate(counts, start=1)
        if divisor_count == 4
    ]
    if not d4_offsets:
        raise ValueError(f"d=4 current chamber expected for ({left_prime}, {right_prime})")

    d4_count = len(d4_offsets)
    d4_first = d4_offsets[0]
    d4_last = d4_offsets[-1]
    divisor_sum = sum(counts)
    low_divisor_load = sum(1.0 / divisor_count for divisor_count in counts)
    return {
        "d4_count": d4_count,
        "d4_span": d4_last - d4_first,
        "d4_last_to_endpoint": right_prime - (left_prime + d4_last),
        "d4_centroid_offset": sum(d4_offsets) / d4_count,
        "divisor_sum": divisor_sum,
        "divisor_mean": divisor_sum / len(counts),
        "low_divisor_load": low_divisor_load,
    }


def build_transitions(
    detail_rows: list[dict[str, object]],
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, object]]:
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

            left_prime = int(current_row["current_right_prime"])
            q = int(current_row["next_right_prime"])
            w = int(current_row["winner"])
            tail_length = q - w
            payload = divisor_payload(left_prime, q)
            transition = {
                "power": power,
                "previous_reduced_state": phase_probe.reduced_state(previous_row),
                "current_winner_parity": "even" if w % 2 == 0 else "odd",
                "current_carrier_family": str(current_row["carrier_family"]),
                "current_winner_offset": int(current_row["next_peak_offset"]),
                "current_first_open_offset": int(current_row["first_open_offset"]),
                "endpoint_mod30": q % 30,
                "endpoint_mod210": q % 210,
                "previous_gap_width": int(previous_row["next_gap_width"]),
                "previous_gap_bin": previous_gap_bin(int(previous_row["next_gap_width"])),
                "current_gap_width": int(current_row["next_gap_width"]),
                "tail_length": tail_length,
                "tail_mod30": tail_length % 30,
                "tail_mod210": tail_length % 210,
                "next_is_triad": int(
                    str(next_row["carrier_family"]) == "odd_semiprime"
                    and int(next_row["next_dmin"]) <= 4
                ),
            }
            transition.update(payload)
            transitions.append(transition)

    if not transitions:
        raise ValueError("requested power range did not produce any d=4 transitions")
    return transitions


def base_key(row: dict[str, object]) -> tuple[object, ...]:
    return (
        str(row["previous_reduced_state"]),
        str(row["current_winner_parity"]),
        str(row["current_carrier_family"]),
        int(row["current_winner_offset"]),
        int(row["current_first_open_offset"]),
    )


def match_key(row: dict[str, object], match_mode: str) -> tuple[object, ...]:
    key = (*base_key(row), int(row["endpoint_mod30"]))
    if match_mode == "mod30":
        return key
    if match_mode == "mod30_prev_gap_bin":
        return (*key, str(row["previous_gap_bin"]))
    if match_mode == "mod30_prev_gap_exact":
        return (*key, int(row["previous_gap_width"]))
    raise KeyError(f"unknown match mode: {match_mode}")


def compare_members(members: list[dict[str, object]], measure: str) -> tuple[int, int, int]:
    targets = [row for row in members if int(row["next_is_triad"]) == 1]
    non_targets = [row for row in members if int(row["next_is_triad"]) == 0]
    if not targets or not non_targets:
        return 0, 0, 0

    decisive_pairs = 0
    signed_advantage = 0
    tie_pairs = 0
    for target in targets:
        for non_target in non_targets:
            target_value = float(target[measure])
            non_target_value = float(non_target[measure])
            decisive_pairs += 1
            if target_value < non_target_value:
                signed_advantage += 1
            elif target_value > non_target_value:
                signed_advantage -= 1
            else:
                tie_pairs += 1
    return decisive_pairs, signed_advantage, tie_pairs


def score_rows(
    rows: list[dict[str, object]],
    *,
    match_mode: str,
    measure: str,
) -> tuple[int, int, int, int]:
    by_cell: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_cell[match_key(row, match_mode)].append(row)

    eligible_cells = 0
    decisive_pairs = 0
    signed_advantage = 0
    tie_pairs = 0
    for members in by_cell.values():
        pairs, signed, ties = compare_members(members, measure)
        if pairs == 0:
            continue
        eligible_cells += 1
        decisive_pairs += pairs
        signed_advantage += signed
        tie_pairs += ties
    return eligible_cells, decisive_pairs, signed_advantage, tie_pairs


def score_measure_folds(
    transitions: list[dict[str, object]],
    *,
    match_mode: str,
    measure: str,
    measure_role: str,
) -> list[dict[str, object]]:
    powers = sorted({int(row["power"]) for row in transitions})
    fold_rows: list[dict[str, object]] = []
    for heldout_power in powers:
        train_rows = [row for row in transitions if int(row["power"]) != heldout_power]
        heldout_rows = [row for row in transitions if int(row["power"]) == heldout_power]
        _, train_pairs, train_signed, _ = score_rows(
            train_rows,
            match_mode=match_mode,
            measure=measure,
        )
        train_direction = 1 if train_signed >= 0 else -1
        eligible_cells, decisive_pairs, raw_signed, tie_pairs = score_rows(
            heldout_rows,
            match_mode=match_mode,
            measure=measure,
        )
        oriented_signed = train_direction * raw_signed
        fold_rows.append(
            {
                "match_mode": match_mode,
                "measure": measure,
                "measure_role": measure_role,
                "heldout_power": heldout_power,
                "train_direction": train_direction if train_pairs else 0,
                "eligible_cells": eligible_cells,
                "decisive_pairs": decisive_pairs,
                "raw_signed_advantage": raw_signed,
                "oriented_signed_advantage": oriented_signed if train_pairs else 0,
                "tie_pairs": tie_pairs,
                "advantage_share": (
                    oriented_signed / decisive_pairs if decisive_pairs and train_pairs else None
                ),
            }
        )
    return fold_rows


def summarize_measure(fold_rows: list[dict[str, object]]) -> dict[str, object]:
    decisive_pairs = sum(int(row["decisive_pairs"]) for row in fold_rows)
    oriented_signed = sum(int(row["oriented_signed_advantage"]) for row in fold_rows)
    folds_with_support = sum(int(row["decisive_pairs"]) >= MIN_FOLD_DECISIVE_PAIRS for row in fold_rows)
    positive_folds = sum(int(row["oriented_signed_advantage"]) > 0 for row in fold_rows)
    negative_folds = sum(int(row["oriented_signed_advantage"]) < 0 for row in fold_rows)
    return {
        "match_mode": str(fold_rows[0]["match_mode"]) if fold_rows else "",
        "measure": str(fold_rows[0]["measure"]) if fold_rows else "",
        "measure_role": str(fold_rows[0]["measure_role"]) if fold_rows else "",
        "fold_count": len(fold_rows),
        "folds_with_min_support": folds_with_support,
        "positive_oriented_folds": positive_folds,
        "negative_oriented_folds": negative_folds,
        "eligible_cells": sum(int(row["eligible_cells"]) for row in fold_rows),
        "decisive_pairs": decisive_pairs,
        "oriented_signed_advantage": oriented_signed,
        "tie_pairs": sum(int(row["tie_pairs"]) for row in fold_rows),
        "advantage_share": oriented_signed / decisive_pairs if decisive_pairs else None,
    }


def evaluate_surface(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    transitions = build_transitions(
        phase_probe.load_detail_rows(detail_csv),
        min_power=min_power,
        max_power=max_power,
    )

    fold_rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for match_mode in MATCH_MODES:
        for measure in CONTROL_MEASURES:
            rows = score_measure_folds(
                transitions,
                match_mode=match_mode,
                measure=measure,
                measure_role="control",
            )
            fold_rows.extend(rows)
            summaries.append(summarize_measure(rows))
        for measure in CANDIDATE_MEASURES:
            rows = score_measure_folds(
                transitions,
                match_mode=match_mode,
                measure=measure,
                measure_role="candidate",
            )
            fold_rows.extend(rows)
            summaries.append(summarize_measure(rows))

    control_by_mode = {
        str(summary["match_mode"]): summary
        for summary in summaries
        if str(summary["measure"]) == "tail_length"
    }
    candidate_summaries = []
    carrier_hits = []
    for summary in summaries:
        if str(summary["measure_role"]) != "candidate":
            continue
        control = control_by_mode[str(summary["match_mode"])]
        decisive_pairs = int(summary["decisive_pairs"])
        threshold = max(
            MIN_FIXED_MARGIN,
            int(MIN_PROPORTIONAL_MARGIN * decisive_pairs),
        )
        edge_over_tail = int(summary["oriented_signed_advantage"]) - int(
            control["oriented_signed_advantage"]
        )
        candidate_summary = dict(summary)
        candidate_summary["tail_control_signed_advantage"] = int(
            control["oriented_signed_advantage"]
        )
        candidate_summary["edge_over_tail_control"] = edge_over_tail
        candidate_summary["required_edge"] = threshold
        candidate_summary["ordering_carrier_stop_condition_met"] = bool(
            decisive_pairs >= MIN_TOTAL_DECISIVE_PAIRS
            and int(summary["folds_with_min_support"]) == int(summary["fold_count"])
            and int(summary["positive_oriented_folds"]) >= MIN_DIRECTIONAL_FOLDS
            and edge_over_tail >= threshold
        )
        candidate_summaries.append(candidate_summary)
        if candidate_summary["ordering_carrier_stop_condition_met"]:
            carrier_hits.append(candidate_summary)

    strongest = sorted(
        candidate_summaries,
        key=lambda row: (
            int(row["edge_over_tail_control"]),
            int(row["oriented_signed_advantage"]),
            int(row["decisive_pairs"]),
        ),
        reverse=True,
    )[:10]
    row_count = sum(1 for row in phase_probe.load_detail_rows(detail_csv) if str(row["power"]) != "")
    summary = {
        "question": (
            "After current PGS chamber facts and endpoint residue are fixed, "
            "does any retained current-chamber scalar beat endpoint tail length?"
        ),
        "detail_csv": str(detail_csv),
        "input_catalog_power_window_row_count": row_count,
        "min_power": min_power,
        "max_power": max_power,
        "transition_count": len(transitions),
        "match_modes": list(MATCH_MODES),
        "candidate_measures": list(CANDIDATE_MEASURES),
        "control_measures": list(CONTROL_MEASURES),
        "ordering_carrier_thresholds": {
            "min_total_decisive_pairs": MIN_TOTAL_DECISIVE_PAIRS,
            "min_fold_decisive_pairs": MIN_FOLD_DECISIVE_PAIRS,
            "min_directional_folds": MIN_DIRECTIONAL_FOLDS,
            "min_edge_over_control": "max(50, 0.005 * decisive_pairs)",
        },
        "control_summaries": list(control_by_mode.values()),
        "candidate_summaries": candidate_summaries,
        "strongest_candidates_by_edge_over_tail": strongest,
        "ordering_carrier_hits": carrier_hits,
        "verdict": "ordering_carrier_found" if carrier_hits else "no_ordering_carrier_found",
    }
    return fold_rows, summary


def format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_fold_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(FOLD_FIELDS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: format_value(row.get(field)) for field in FOLD_FIELDS})


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fold_rows, summary = evaluate_surface(
        args.detail_csv,
        min_power=args.min_power,
        max_power=args.max_power,
    )
    fold_path = args.output_dir / "state_budget_divisor_carrier_sweep_folds.csv"
    summary_path = args.output_dir / "state_budget_divisor_carrier_sweep_summary.json"
    write_fold_csv(fold_path, fold_rows)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
