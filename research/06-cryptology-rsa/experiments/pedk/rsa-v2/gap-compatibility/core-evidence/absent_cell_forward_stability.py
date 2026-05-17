#!/usr/bin/env python3
"""Forward-test survived PEDK absent cells under one frozen projection."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from intermediate_projection_surface import factor_key, public_key


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_9001_11000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_11001_13000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_13001_15000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000"
RULE_ID = "pedk_absent_cell_forward_stability_v1"
PUBLIC_MODE = "public_word_gwr_side"
FACTOR_MODE = "oriented_factor_phase_word"
DEFAULT_MIN_PUBLIC_SUPPORT = 5
DEFAULT_MIN_FACTOR_SUPPORT = 5
DEFAULT_TOP_N = 200
DEFAULT_SUPPORTED_OBSERVATION_THRESHOLD = 5


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def projection_counts(
    rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
) -> dict[str, Counter[object]]:
    """Return marginal and cell counts for one projection."""
    public_counts = Counter(public_key(row, public_mode) for row in rows)
    factor_counts = Counter(factor_key(row, factor_mode) for row in rows)
    observed_counts = Counter(
        (public_key(row, public_mode), factor_key(row, factor_mode))
        for row in rows
    )
    return {
        "public": public_counts,
        "factor": factor_counts,
        "observed": observed_counts,
    }


def supported_keys(counts: Counter[object], minimum: int) -> set[str]:
    """Return keys with at least minimum support."""
    return {str(key) for key, count in counts.items() if count >= minimum}


def select_candidate_cells(
    train: dict[str, Counter[object]],
    calibration: dict[str, Counter[object]],
    min_public_support: int,
    min_factor_support: int,
    top_n: int,
) -> list[dict[str, object]]:
    """Select top survived absent cells from train to calibration."""
    train_public = supported_keys(train["public"], min_public_support)
    train_factor = supported_keys(train["factor"], min_factor_support)
    calibration_public = supported_keys(calibration["public"], min_public_support)
    calibration_factor = supported_keys(calibration["factor"], min_factor_support)

    train_observed = set(train["observed"])
    calibration_observed = set(calibration["observed"])
    candidates = []
    for public_value, factor_value in itertools.product(train_public, train_factor):
        cell = (public_value, factor_value)
        if cell in train_observed:
            continue
        if public_value not in calibration_public or factor_value not in calibration_factor:
            continue
        if cell in calibration_observed:
            continue
        candidates.append(
            {
                "public_key": public_value,
                "factor_key": factor_value,
                "train_public_support": train["public"][public_value],
                "train_factor_support": train["factor"][factor_value],
                "calibration_public_support": calibration["public"][public_value],
                "calibration_factor_support": calibration["factor"][factor_value],
                "calibration_observed_count": 0,
                "calibration_support_product": (
                    calibration["public"][public_value]
                    * calibration["factor"][factor_value]
                ),
                "train_support_product": (
                    train["public"][public_value] * train["factor"][factor_value]
                ),
            }
        )

    candidates.sort(
        key=lambda row: (
            -int(row["calibration_support_product"]),
            -int(row["train_support_product"]),
            str(row["public_key"]),
            str(row["factor_key"]),
        )
    )
    return candidates[:top_n]


def evaluate_forward(
    selected_cells: list[dict[str, object]],
    forward: dict[str, Counter[object]],
    min_public_support: int,
    min_factor_support: int,
    supported_observation_threshold: int,
) -> list[dict[str, object]]:
    """Evaluate selected absent cells in a forward band."""
    forward_public = supported_keys(forward["public"], min_public_support)
    forward_factor = supported_keys(forward["factor"], min_factor_support)
    rows = []
    for rank, selected in enumerate(selected_cells, start=1):
        public_value = str(selected["public_key"])
        factor_value = str(selected["factor_key"])
        observed_count = forward["observed"][(public_value, factor_value)]
        forward_testable = (
            public_value in forward_public and factor_value in forward_factor
        )
        if not forward_testable:
            status = "not_testable_forward"
        elif observed_count >= supported_observation_threshold:
            status = "supported_falsification"
        elif observed_count > 0:
            status = "thin_observation"
        else:
            status = "survived_absent"
        row = dict(selected)
        row.update(
            {
                "rule_id": RULE_ID,
                "rank": rank,
                "public_mode": PUBLIC_MODE,
                "factor_mode": FACTOR_MODE,
                "forward_public_support": forward["public"][public_value],
                "forward_factor_support": forward["factor"][factor_value],
                "forward_observed_count": observed_count,
                "forward_testable": forward_testable,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def summarize(
    rows: list[dict[str, object]],
    train_rows: int,
    calibration_rows: int,
    forward_rows: int,
    min_public_support: int,
    min_factor_support: int,
    supported_observation_threshold: int,
) -> dict[str, object]:
    """Summarize forward stability rows."""
    status_counts = Counter(str(row["status"]) for row in rows)
    testable_rows = [row for row in rows if row["forward_testable"]]
    supported_falsifications = status_counts["supported_falsification"]
    thin_observations = status_counts["thin_observation"]
    survived_absent = status_counts["survived_absent"]
    denominator = len(testable_rows)
    return {
        "rule_id": RULE_ID,
        "status": "measured_absent_cell_forward_stability",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_mode": PUBLIC_MODE,
        "factor_mode": FACTOR_MODE,
        "train_row_count": train_rows,
        "calibration_row_count": calibration_rows,
        "forward_row_count": forward_rows,
        "min_public_support": min_public_support,
        "min_factor_support": min_factor_support,
        "supported_observation_threshold": supported_observation_threshold,
        "selected_candidate_cell_count": len(rows),
        "forward_testable_cell_count": denominator,
        "survived_absent_count": survived_absent,
        "thin_observation_count": thin_observations,
        "supported_falsification_count": supported_falsifications,
        "not_testable_forward_count": status_counts["not_testable_forward"],
        "supported_falsification_rate_mpermille": (
            supported_falsifications * 1000 // denominator if denominator else 0
        ),
        "any_observation_rate_mpermille": (
            (supported_falsifications + thin_observations) * 1000 // denominator
            if denominator
            else 0
        ),
        "falsification_boundary": (
            "representation/extraction is insufficient if at least 15 percent "
            "of forward-testable selected cells become supported observations"
        ),
        "boundary_result": (
            "failed_boundary"
            if denominator and supported_falsifications * 100 >= 15 * denominator
            else "passed_boundary"
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Forward-test survived PEDK absent cells.")
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-public-support", type=int, default=DEFAULT_MIN_PUBLIC_SUPPORT)
    parser.add_argument("--min-factor-support", type=int, default=DEFAULT_MIN_FACTOR_SUPPORT)
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    parser.add_argument(
        "--supported-observation-threshold",
        type=int,
        default=DEFAULT_SUPPORTED_OBSERVATION_THRESHOLD,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run absent-cell forward stability test."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    train = projection_counts(train_rows, PUBLIC_MODE, FACTOR_MODE)
    calibration = projection_counts(calibration_rows, PUBLIC_MODE, FACTOR_MODE)
    forward = projection_counts(forward_rows, PUBLIC_MODE, FACTOR_MODE)
    selected = select_candidate_cells(
        train,
        calibration,
        args.min_public_support,
        args.min_factor_support,
        args.top_n,
    )
    result_rows = evaluate_forward(
        selected,
        forward,
        args.min_public_support,
        args.min_factor_support,
        args.supported_observation_threshold,
    )
    summary = summarize(
        result_rows,
        len(train_rows),
        len(calibration_rows),
        len(forward_rows),
        args.min_public_support,
        args.min_factor_support,
        args.supported_observation_threshold,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "forward_stability_rows.jsonl", result_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
