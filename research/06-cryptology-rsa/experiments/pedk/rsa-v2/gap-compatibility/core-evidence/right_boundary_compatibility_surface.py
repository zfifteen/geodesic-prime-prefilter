#!/usr/bin/env python3
"""Test public containing grammar against endpoint-pair right boundaries."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from endpoint_pair_family_profile import parse_endpoint_pair
from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import factor_projection, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_15001_17000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_17001_19000"
DEFAULT_PRIOR_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_19001_21000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_21001_23000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "right_boundary_compatibility_surface_21001_23000"
RULE_ID = "pedk_right_boundary_compatibility_surface_v1"
MIN_PUBLIC_SUPPORT = 5
MIN_FACTOR_SUPPORT = 5


PUBLIC_MODES = (
    "containing_type_side",
    "containing_phase_side",
    "containing_type_at_winner",
    "containing_phase_at_winner",
)

FACTOR_MODES = (
    "endpoint_right_values",
    "endpoint_left_values",
    "endpoint_left_right_values",
)


def public_key(row: dict[str, object], mode: str) -> str:
    """Return public containing grammar projection."""
    side = str(row["public_gwr_side"])
    containing_type = str(row["public_containing_exact_type_key"])
    containing_phase = f"{containing_type}@{row['public_containing_phase_bucket']}"
    if mode == "containing_type_side":
        return f"containing={containing_type}|{side}"
    if mode == "containing_phase_side":
        return f"containing={containing_phase}|{side}"
    if mode == "containing_type_at_winner":
        return f"containing={containing_type}|at_winner" if side == "at_winner" else ""
    if mode == "containing_phase_at_winner":
        return f"containing={containing_phase}|at_winner" if side == "at_winner" else ""
    raise ValueError(f"unknown public mode: {mode}")


def endpoint_values(row: dict[str, object], mode: str) -> str:
    """Return directed endpoint-pair boundary values."""
    pair_word = factor_projection(row, "unordered_endpoint_pair_residue_phase")
    first, second = pair_word.split(" || ", 1)
    pair_a = parse_endpoint_pair(first)
    pair_b = parse_endpoint_pair(second)
    left_values = "|".join(sorted((pair_a[0], pair_b[0])))
    right_values = "|".join(sorted((pair_a[1], pair_b[1])))
    if mode == "endpoint_right_values":
        return f"R={right_values}"
    if mode == "endpoint_left_values":
        return f"L={left_values}"
    if mode == "endpoint_left_right_values":
        return f"L={left_values}|R={right_values}"
    raise ValueError(f"unknown factor mode: {mode}")


def surface(
    rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
) -> dict[str, object]:
    """Return supported keys and observed cells."""
    projected = [
        (public_key(row, public_mode), endpoint_values(row, factor_mode))
        for row in rows
    ]
    projected = [(public, factor) for public, factor in projected if public]
    public_counts = Counter(public for public, _ in projected)
    factor_counts = Counter(factor for _, factor in projected)
    observed_counts = Counter(projected)
    supported_public = {
        key for key, count in public_counts.items() if count >= MIN_PUBLIC_SUPPORT
    }
    supported_factor = {
        key for key, count in factor_counts.items() if count >= MIN_FACTOR_SUPPORT
    }
    observed_supported = {
        cell
        for cell in observed_counts
        if cell[0] in supported_public and cell[1] in supported_factor
    }
    return {
        "public_counts": public_counts,
        "factor_counts": factor_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_factor": supported_factor,
        "observed_supported": observed_supported,
    }


def analyze(
    train_rows: list[dict[str, object]],
    calibration_rows: list[dict[str, object]],
    prior_forward_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Analyze one public/factor right-boundary surface."""
    train = surface(train_rows, public_mode, factor_mode)
    calibration = surface(calibration_rows, public_mode, factor_mode)
    prior_forward = surface(prior_forward_rows, public_mode, factor_mode)
    forward = surface(forward_rows, public_mode, factor_mode)

    candidate_cells = set(
        itertools.product(train["supported_public"], train["supported_factor"])
    )
    for older in (train, calibration, prior_forward):
        candidate_cells &= set(
            itertools.product(older["supported_public"], older["supported_factor"])
        )
        candidate_cells -= older["observed_supported"]

    forward_product = set(
        itertools.product(forward["supported_public"], forward["supported_factor"])
    )
    testable = candidate_cells & forward_product
    falsified = testable & forward["observed_supported"]
    survived = testable - falsified
    not_testable = candidate_cells - testable

    rows = []
    for status, cells in (
        ("survived_forward", survived),
        ("falsified_forward", falsified),
        ("not_testable_forward", not_testable),
    ):
        for public_value, factor_value in sorted(cells):
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_mode": public_mode,
                    "factor_mode": factor_mode,
                    "public_key": public_value,
                    "factor_key": factor_value,
                    "train_public_support": train["public_counts"][public_value],
                    "train_factor_support": train["factor_counts"][factor_value],
                    "calibration_public_support": calibration["public_counts"][public_value],
                    "calibration_factor_support": calibration["factor_counts"][factor_value],
                    "prior_forward_public_support": prior_forward["public_counts"][public_value],
                    "prior_forward_factor_support": prior_forward["factor_counts"][factor_value],
                    "forward_public_support": forward["public_counts"][public_value],
                    "forward_factor_support": forward["factor_counts"][factor_value],
                    "forward_observed_count": forward["observed_counts"][
                        (public_value, factor_value)
                    ],
                    "status": status,
                }
            )
    summary = {
        "rule_id": RULE_ID,
        "public_mode": public_mode,
        "factor_mode": factor_mode,
        "min_public_support": MIN_PUBLIC_SUPPORT,
        "min_factor_support": MIN_FACTOR_SUPPORT,
        "candidate_clean_absent_cell_count": len(candidate_cells),
        "forward_testable_cell_count": len(testable),
        "survived_forward_cell_count": len(survived),
        "falsified_forward_cell_count": len(falsified),
        "not_testable_forward_cell_count": len(not_testable),
        "strict_falsification_rate_mpermille": (
            len(falsified) * 1000 // len(testable) if testable else None
        ),
    }
    return summary, rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test endpoint-pair right-boundary compatibility."
    )
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--prior-forward-dir", type=Path, default=DEFAULT_PRIOR_FORWARD_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run right-boundary compatibility surface."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(args.prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")

    rows = []
    candidate_rows = []
    for public_mode in PUBLIC_MODES:
        for factor_mode in FACTOR_MODES:
            summary, candidates = analyze(
                train_rows,
                calibration_rows,
                prior_forward_rows,
                forward_rows,
                public_mode,
                factor_mode,
            )
            rows.append(summary)
            candidate_rows.extend(candidates)
    rows.sort(
        key=lambda row: (
            row["strict_falsification_rate_mpermille"]
            if row["strict_falsification_rate_mpermille"] is not None
            else 1001,
            -int(row["forward_testable_cell_count"]),
            str(row["public_mode"]),
            str(row["factor_mode"]),
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_right_boundary_compatibility_surface",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "train_row_count": len(train_rows),
        "calibration_row_count": len(calibration_rows),
        "prior_forward_row_count": len(prior_forward_rows),
        "forward_row_count": len(forward_rows),
        "surface_count": len(rows),
        "top_surfaces": rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "surface_rows.jsonl", rows)
    write_jsonl(args.output_dir / "candidate_rows.jsonl", candidate_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
