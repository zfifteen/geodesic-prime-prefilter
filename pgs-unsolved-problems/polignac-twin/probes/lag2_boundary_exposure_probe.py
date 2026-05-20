#!/usr/bin/env python3
"""Measure lag-2 residue-lifted exposure to width-2 high-load closures.

This probe stays on the committed PGS gap-type catalog. It does not generate
primes, test candidates, or use classical factor selection. It reads the
ordered chamber-state rows already produced by the PGS catalog and asks whether
the two immediately preceding residue-lifted reduced states expose the next
width-2 high-load boundary better than the current lifted state alone.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = REPO_ROOT / "research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv"
OUTPUT_DIR = REPO_ROOT / "pgs-unsolved-problems/polignac-twin/output/lag2_boundary_exposure_probe"

TOP_SHARES = (0.05, 0.10, 0.20)
MATERIAL_MARGIN = 0.05
TOP_DECILE_MIN_CAPTURE = 0.45

REQUIRED_FIELDS = {
    "surface_label",
    "surface_display_label",
    "surface_kind",
    "surface_row_index",
    "current_right_prime",
    "next_right_prime",
    "next_gap_width",
    "residue_mod30",
    "first_open_offset",
    "next_dmin",
    "carrier_family",
}


def int_field(row: dict[str, str], field: str) -> int:
    return int(row[field])


def divisor_bucket(d_value: int) -> str:
    if d_value <= 4:
        return "d<=4"
    if d_value <= 16:
        return "5<=d<=16"
    if d_value <= 64:
        return "17<=d<=64"
    return "d>64"


def reduced_state(row: dict[str, str]) -> str:
    offset = int_field(row, "first_open_offset")
    family = row["carrier_family"]
    bucket = divisor_bucket(int_field(row, "next_dmin"))
    return f"o{offset}_{family}|{bucket}"


def lifted_state(row: dict[str, str]) -> str:
    return f"{reduced_state(row)}|r{int_field(row, 'residue_mod30')}"


def is_width2_high_load(row: dict[str, str]) -> bool:
    return (
        int_field(row, "next_gap_width") == 2
        and int_field(row, "first_open_offset") == 2
        and row["carrier_family"] == "higher_divisor_even"
        and int_field(row, "next_dmin") > 16
    )


def read_catalog() -> dict[str, list[dict[str, str]]]:
    with CATALOG_PATH.open(newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_FIELDS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"catalog missing required fields: {sorted(missing)}")
        surfaces: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in reader:
            surfaces[row["surface_label"]].append(row)

    for rows in surfaces.values():
        rows.sort(key=lambda item: int_field(item, "surface_row_index"))

    return dict(sorted(surfaces.items()))


def build_events(surfaces: dict[str, list[dict[str, str]]]) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for surface_label, rows in surfaces.items():
        surface_size = len(rows)
        split_at = surface_size // 2
        for target_pos in range(2, surface_size):
            lag2_row = rows[target_pos - 2]
            source_row = rows[target_pos - 1]
            target_row = rows[target_pos]
            target_lifted = lifted_state(target_row)
            high_load = is_width2_high_load(target_row)
            if surface_label == "baseline_1e6":
                split = "exact_baseline_train" if target_pos < split_at else "exact_baseline_test"
            elif target_row["surface_kind"] == "sampled_decade_window":
                split = "sampled_decade_windows"
            else:
                split = "other"
            events.append(
                {
                    "surface_label": surface_label,
                    "surface_display_label": target_row["surface_display_label"],
                    "surface_kind": target_row["surface_kind"],
                    "target_pos": target_pos,
                    "split": split,
                    "target_right_prime": int_field(target_row, "current_right_prime"),
                    "target_next_prime": int_field(target_row, "next_right_prime"),
                    "target_gap_width": int_field(target_row, "next_gap_width"),
                    "target_lifted_state": target_lifted,
                    "target_reduced_state": reduced_state(target_row),
                    "current_lifted_state": lifted_state(source_row),
                    "lag2_arrival_pair": f"{lifted_state(lag2_row)} -> {lifted_state(source_row)}",
                    "is_high_load_exit": high_load,
                }
            )
    return events


def rank_features(events: list[dict[str, object]], feature_field: str) -> list[dict[str, object]]:
    high_counts: Counter[str] = Counter()
    total_counts: Counter[str] = Counter()
    for event in events:
        feature = str(event[feature_field])
        total_counts[feature] += 1
        if event["is_high_load_exit"]:
            high_counts[feature] += 1

    ranked = []
    for feature in total_counts:
        high_count = high_counts[feature]
        total_count = total_counts[feature]
        ranked.append(
            {
                "feature": feature,
                "high_exit_count": high_count,
                "total_event_count": total_count,
                "high_exit_rate": high_count / total_count if total_count else 0.0,
            }
        )

    ranked.sort(
        key=lambda item: (
            -int(item["high_exit_count"]),
            -int(item["total_event_count"]),
            str(item["feature"]),
        )
    )
    return ranked


def evaluate_feature_set(
    eval_events: list[dict[str, object]],
    feature_field: str,
    selected_features: set[str],
) -> dict[str, object]:
    eval_event_count = len(eval_events)
    high_events = [event for event in eval_events if event["is_high_load_exit"]]
    exposure_events = [event for event in eval_events if str(event[feature_field]) in selected_features]
    captured_events = [event for event in high_events if str(event[feature_field]) in selected_features]

    eval_high_count = len(high_events)
    exposure_count = len(exposure_events)
    captured_count = len(captured_events)
    background_high_rate = eval_high_count / eval_event_count if eval_event_count else 0.0
    selected_high_rate = captured_count / exposure_count if exposure_count else 0.0
    exposure_share = exposure_count / eval_event_count if eval_event_count else 0.0
    capture_share = captured_count / eval_high_count if eval_high_count else 0.0

    return {
        "eval_event_count": eval_event_count,
        "eval_high_exit_count": eval_high_count,
        "eval_background_high_exit_rate": background_high_rate,
        "eval_background_exposure_count": exposure_count,
        "eval_background_exposure_share": exposure_share,
        "captured_high_exit_count": captured_count,
        "high_exit_capture_share": capture_share,
        "high_exit_rate_inside_selected": selected_high_rate,
        "high_exit_rate_lift_vs_background": (
            selected_high_rate / background_high_rate if background_high_rate else 0.0
        ),
    }


def threshold_rows(
    train_events: list[dict[str, object]],
    eval_events_by_label: dict[str, list[dict[str, object]]],
) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    rows: list[dict[str, object]] = []
    rankings = {
        "current_lifted_state": rank_features(train_events, "current_lifted_state"),
        "lag2_arrival_pair": rank_features(train_events, "lag2_arrival_pair"),
    }

    train_high_count = sum(1 for event in train_events if event["is_high_load_exit"])
    for feature_kind, ranking in rankings.items():
        feature_count = len(ranking)
        for top_share in TOP_SHARES:
            selected_count = max(1, math.ceil(feature_count * top_share))
            selected_features = {str(item["feature"]) for item in ranking[:selected_count]}
            for eval_label, eval_events in eval_events_by_label.items():
                row = {
                    "evaluation_label": eval_label,
                    "feature_kind": feature_kind,
                    "top_feature_share": top_share,
                    "train_feature_count": feature_count,
                    "selected_feature_count": selected_count,
                    "train_high_exit_count": train_high_count,
                }
                row.update(evaluate_feature_set(eval_events, feature_kind, selected_features))
                rows.append(row)

    return rows, rankings


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    surfaces = read_catalog()
    events = build_events(surfaces)
    train_events = [event for event in events if event["split"] == "exact_baseline_train"]
    exact_test_events = [event for event in events if event["split"] == "exact_baseline_test"]
    sampled_events = [event for event in events if event["split"] == "sampled_decade_windows"]

    eval_events_by_label = {
        "exact_baseline_heldout": exact_test_events,
        "sampled_decade_windows": sampled_events,
    }

    rows, rankings = threshold_rows(train_events, eval_events_by_label)
    exact_decile = {
        row["feature_kind"]: row
        for row in rows
        if row["evaluation_label"] == "exact_baseline_heldout"
        and abs(float(row["top_feature_share"]) - 0.10) < 1e-12
    }
    sampled_decile = {
        row["feature_kind"]: row
        for row in rows
        if row["evaluation_label"] == "sampled_decade_windows"
        and abs(float(row["top_feature_share"]) - 0.10) < 1e-12
    }

    current_exact_capture = float(exact_decile["current_lifted_state"]["high_exit_capture_share"])
    lag2_exact_capture = float(exact_decile["lag2_arrival_pair"]["high_exit_capture_share"])
    exact_margin = lag2_exact_capture - current_exact_capture
    exact_disconfirmed = (
        lag2_exact_capture <= TOP_DECILE_MIN_CAPTURE
        or exact_margin <= MATERIAL_MARGIN
    )

    current_sampled_capture = float(sampled_decile["current_lifted_state"]["high_exit_capture_share"])
    lag2_sampled_capture = float(sampled_decile["lag2_arrival_pair"]["high_exit_capture_share"])

    high_load_rows = [
        row
        for surface_rows in surfaces.values()
        for row in surface_rows
        if is_width2_high_load(row)
    ]
    non_width2_high_load = [
        row for row in high_load_rows if int_field(row, "next_gap_width") != 2
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    threshold_fieldnames = [
        "evaluation_label",
        "feature_kind",
        "top_feature_share",
        "train_feature_count",
        "selected_feature_count",
        "train_high_exit_count",
        "eval_event_count",
        "eval_high_exit_count",
        "eval_background_high_exit_rate",
        "eval_background_exposure_count",
        "eval_background_exposure_share",
        "captured_high_exit_count",
        "high_exit_capture_share",
        "high_exit_rate_inside_selected",
        "high_exit_rate_lift_vs_background",
    ]
    write_csv(OUTPUT_DIR / "threshold_summary.csv", rows, threshold_fieldnames)

    ranking_fieldnames = [
        "rank",
        "feature",
        "high_exit_count",
        "total_event_count",
        "high_exit_rate",
    ]
    for feature_kind, filename in (
        ("current_lifted_state", "ranked_current_states.csv"),
        ("lag2_arrival_pair", "ranked_lag2_pairs.csv"),
    ):
        ranking_rows = []
        for rank, item in enumerate(rankings[feature_kind], start=1):
            ranking_rows.append({"rank": rank, **item})
        write_csv(OUTPUT_DIR / filename, ranking_rows, ranking_fieldnames)

    surface_summary = []
    for surface_label, rows_for_surface in surfaces.items():
        surface_events = [event for event in events if event["surface_label"] == surface_label]
        surface_summary.append(
            {
                "surface_label": surface_label,
                "surface_display_label": rows_for_surface[0]["surface_display_label"],
                "surface_kind": rows_for_surface[0]["surface_kind"],
                "row_count": len(rows_for_surface),
                "event_count_with_lag2_context": len(surface_events),
                "high_load_width2_rows": sum(1 for row in rows_for_surface if is_width2_high_load(row)),
                "high_load_exits_with_lag2_context": sum(
                    1 for event in surface_events if event["is_high_load_exit"]
                ),
            }
        )

    summary = {
        "catalog_path": str(CATALOG_PATH.relative_to(REPO_ROOT)),
        "output_dir": str(OUTPUT_DIR.relative_to(REPO_ROOT)),
        "pgs_object": "residue-lifted reduced chamber-state sequence",
        "pgs_invariant": "lag-2 ordered arrival pair before a width-2 high-load endpoint-closing state",
        "pgs_rule_or_law_tested": "lag-2 boundary exposure as a candidate bridge toward high-load width-2 recurrence",
        "status": "ADVANCE",
        "surface_count": len(surfaces),
        "catalog_row_count": sum(len(rows_for_surface) for rows_for_surface in surfaces.values()),
        "event_count_with_lag2_context": len(events),
        "high_load_width2_row_count": len(high_load_rows),
        "non_width2_high_load_row_count": len(non_width2_high_load),
        "exact_baseline_train_event_count": len(train_events),
        "exact_baseline_test_event_count": len(exact_test_events),
        "sampled_decade_event_count": len(sampled_events),
        "exact_heldout_top_decile": {
            "current_lifted_capture": current_exact_capture,
            "lag2_arrival_pair_capture": lag2_exact_capture,
            "lag2_minus_current_capture": exact_margin,
            "disconfirmed_by_contract": exact_disconfirmed,
            "disconfirmation_rule": (
                "lag-2 top decile captures <= 45% of held-out high-load exits "
                "or beats current lifted state by <= 5 percentage points"
            ),
        },
        "sampled_decade_top_decile": {
            "current_lifted_capture": current_sampled_capture,
            "lag2_arrival_pair_capture": lag2_sampled_capture,
            "lag2_minus_current_capture": lag2_sampled_capture - current_sampled_capture,
        },
        "surface_summary": surface_summary,
        "output_files": [
            "summary.json",
            "threshold_summary.csv",
            "ranked_current_states.csv",
            "ranked_lag2_pairs.csv",
        ],
    }

    with (OUTPUT_DIR / "summary.json").open("w", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
