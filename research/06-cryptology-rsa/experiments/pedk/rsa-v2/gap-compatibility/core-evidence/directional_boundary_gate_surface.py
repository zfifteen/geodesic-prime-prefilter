#!/usr/bin/env python3
"""Compare left and right at-winner boundary gates on exact endpoint pairs."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from endpoint_pair_family_profile import parse_endpoint_pair
from first_gap_compatibility_check import write_json, write_jsonl
from hybrid_endpoint_pair_surface import split_slot
from joint_endpoint_pair_right_boundary_surface import (
    TOP_K_VALUES,
    containing_type_from_public,
    endpoint_pair_fields,
    exact_candidate_cells,
    exact_surface,
    pair_identity_key,
    public_is_at_winner,
    public_key,
    rate_mpermille,
    rate_ppm,
    top_k_metrics,
)
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_19001_21000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_21001_23000"
DEFAULT_PRIOR_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_23001_25000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_25001_27000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "directional_boundary_gate_surface_25001_27000"
RULE_ID = "pedk_directional_boundary_gate_surface_v1"
MIN_PUBLIC_SUPPORT = 5
MIN_BOUNDARY_SUPPORT = 5


BOUNDARY_MODES = (
    "left_residues",
    "right_residues",
    "left_residue_phases",
    "right_residue_phases",
    "both_residues",
)


def slots_from_pair_key(pair_key: str) -> tuple[list[str], list[str]]:
    """Return left and right slots from an exact endpoint-pair key."""
    lefts = []
    rights = []
    for part in pair_key.split(" || "):
        left, right = parse_endpoint_pair(part)
        lefts.append(left)
        rights.append(right)
    return lefts, rights


def boundary_index_from_pair_key(pair_key: str, mode: str) -> str:
    """Return a directional boundary index from an exact endpoint-pair key."""
    lefts, rights = slots_from_pair_key(pair_key)
    if mode == "left_residues":
        return "Lres=" + "|".join(sorted(split_slot(left)[0] for left in lefts))
    if mode == "right_residues":
        return "Rres=" + "|".join(sorted(split_slot(right)[0] for right in rights))
    if mode == "left_residue_phases":
        return "L=" + "|".join(sorted(lefts))
    if mode == "right_residue_phases":
        return "R=" + "|".join(sorted(rights))
    if mode == "both_residues":
        left_value = "|".join(sorted(split_slot(left)[0] for left in lefts))
        right_value = "|".join(sorted(split_slot(right)[0] for right in rights))
        return f"Lres={left_value};Rres={right_value}"
    raise ValueError(f"unknown boundary mode: {mode}")


def boundary_values(pair_key: str) -> dict[str, str]:
    """Return flat boundary values for output rows."""
    lefts, rights = slots_from_pair_key(pair_key)
    return {
        "left_boundary_residues": "|".join(sorted(split_slot(left)[0] for left in lefts)),
        "left_boundary_phases": "|".join(sorted(split_slot(left)[1] for left in lefts)),
        "right_boundary_residues": "|".join(sorted(split_slot(right)[0] for right in rights)),
        "right_boundary_phases": "|".join(sorted(split_slot(right)[1] for right in rights)),
    }


def boundary_surface(rows: list[dict[str, object]], mode: str) -> dict[str, object]:
    """Return the at-winner directional boundary-index surface."""
    projected = [
        (public_key(row), boundary_index_from_pair_key(pair_identity_key(row), mode))
        for row in rows
        if str(row["public_gwr_side"]) == "at_winner"
    ]
    public_counts = Counter(public for public, _ in projected)
    boundary_counts = Counter(boundary for _, boundary in projected)
    observed_counts = Counter(projected)
    supported_public = {
        key for key, count in public_counts.items() if count >= MIN_PUBLIC_SUPPORT
    }
    supported_boundary = {
        key for key, count in boundary_counts.items() if count >= MIN_BOUNDARY_SUPPORT
    }
    observed_supported = {
        cell
        for cell in observed_counts
        if cell[0] in supported_public and cell[1] in supported_boundary
    }
    return {
        "public_counts": public_counts,
        "boundary_counts": boundary_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_boundary": supported_boundary,
        "observed_supported": observed_supported,
    }


def boundary_absent_cells(surfaces: tuple[dict[str, object], ...]) -> set[tuple[str, str]]:
    """Return at-winner boundary-index cells supported in every surface and absent."""
    candidate_cells = set(
        itertools.product(
            surfaces[0]["supported_public"],
            surfaces[0]["supported_boundary"],
        )
    )
    for surface in surfaces:
        candidate_cells &= set(
            itertools.product(surface["supported_public"], surface["supported_boundary"])
        )
        candidate_cells -= surface["observed_supported"]
    return candidate_cells


def analyze(
    train_rows: list[dict[str, object]],
    calibration_rows: list[dict[str, object]],
    prior_forward_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
    mode: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Analyze exact pair exclusions gated by one directional boundary index."""
    train = exact_surface(train_rows)
    calibration = exact_surface(calibration_rows)
    prior_forward = exact_surface(prior_forward_rows)
    forward = exact_surface(forward_rows)
    train_boundary = boundary_surface(train_rows, mode)
    calibration_boundary = boundary_surface(calibration_rows, mode)
    prior_forward_boundary = boundary_surface(prior_forward_rows, mode)
    forward_boundary = boundary_surface(forward_rows, mode)

    exact_candidates = exact_candidate_cells(train, calibration, prior_forward)
    at_winner_candidates = {
        cell for cell in exact_candidates if public_is_at_winner(cell[0])
    }
    boundary_absences = boundary_absent_cells(
        (train_boundary, calibration_boundary, prior_forward_boundary)
    )
    rows = []
    for public_value, pair_value in sorted(at_winner_candidates):
        boundary_value = boundary_index_from_pair_key(pair_value, mode)
        if (public_value, boundary_value) not in boundary_absences:
            continue
        forward_pair_testable = (
            public_value in forward["supported_public"]
            and pair_value in forward["supported_pairs"]
        )
        forward_boundary_testable = (
            public_value in forward_boundary["supported_public"]
            and boundary_value in forward_boundary["supported_boundary"]
        )
        exact_falsified = (
            forward_pair_testable
            and (public_value, pair_value) in forward["observed_supported"]
        )
        boundary_falsified = (
            forward_boundary_testable
            and (public_value, boundary_value) in forward_boundary["observed_supported"]
        )
        status = "not_testable_forward"
        if forward_pair_testable:
            status = "falsified_forward" if exact_falsified else "survived_forward"
        row = {
            "rule_id": RULE_ID,
            "boundary_mode": mode,
            "public_key": public_value,
            "public_containing_exact_type_key": containing_type_from_public(public_value),
            "public_gwr_side": "at_winner",
            "pair_identity_key": pair_value,
            "boundary_index_key": boundary_value,
            "minimum_prior_pair_support": min(
                train["pair_counts"][pair_value],
                calibration["pair_counts"][pair_value],
                prior_forward["pair_counts"][pair_value],
            ),
            "minimum_prior_boundary_support": min(
                train_boundary["boundary_counts"][boundary_value],
                calibration_boundary["boundary_counts"][boundary_value],
                prior_forward_boundary["boundary_counts"][boundary_value],
            ),
            "minimum_prior_right_index_support": min(
                train_boundary["boundary_counts"][boundary_value],
                calibration_boundary["boundary_counts"][boundary_value],
                prior_forward_boundary["boundary_counts"][boundary_value],
            ),
            "forward_observed_count": forward["observed_counts"][(public_value, pair_value)],
            "forward_boundary_observed_count": forward_boundary["observed_counts"][
                (public_value, boundary_value)
            ],
            "exact_pair_falsified": exact_falsified,
            "boundary_index_falsified": boundary_falsified,
            "status": status,
        }
        row.update(endpoint_pair_fields(pair_value))
        row.update(boundary_values(pair_value))
        rows.append(row)

    testable = [row for row in rows if row["status"] != "not_testable_forward"]
    falsified = [row for row in testable if row["exact_pair_falsified"]]
    boundary_testable = [
        row for row in rows
        if (
            row["public_key"] in forward_boundary["supported_public"]
            and row["boundary_index_key"] in forward_boundary["supported_boundary"]
        )
    ]
    boundary_falsified = [
        row for row in boundary_testable
        if row["boundary_index_falsified"]
    ]
    summary = {
        "rule_id": RULE_ID,
        "boundary_mode": mode,
        "min_public_support": MIN_PUBLIC_SUPPORT,
        "min_boundary_support": MIN_BOUNDARY_SUPPORT,
        "exact_absent_candidate_cell_count": len(exact_candidates),
        "at_winner_exact_absent_candidate_cell_count": len(at_winner_candidates),
        "boundary_absent_cell_count": len(boundary_absences),
        "joint_candidate_cell_count": len(rows),
        "forward_testable_cell_count": len(testable),
        "survived_forward_cell_count": len(testable) - len(falsified),
        "falsified_forward_cell_count": len(falsified),
        "not_testable_forward_cell_count": len(rows) - len(testable),
        "strict_falsification_rate_mpermille": rate_mpermille(
            len(falsified),
            len(testable),
        ),
        "strict_falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
        "boundary_forward_testable_cell_count": len(boundary_testable),
        "boundary_falsified_cell_count": len(boundary_falsified),
        "boundary_falsification_rate_mpermille": rate_mpermille(
            len(boundary_falsified),
            len(boundary_testable),
        ),
        "boundary_falsification_rate_ppm": rate_ppm(
            len(boundary_falsified),
            len(boundary_testable),
        ),
        "top_k_metrics": top_k_metrics(rows),
    }
    return summary, rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Compare at-winner directional boundary gates."
    )
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--prior-forward-dir", type=Path, default=DEFAULT_PRIOR_FORWARD_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run directional boundary gate comparison."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(args.prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    surface_rows = []
    candidate_rows = []
    for mode in BOUNDARY_MODES:
        summary, rows = analyze(
            train_rows,
            calibration_rows,
            prior_forward_rows,
            forward_rows,
            mode,
        )
        surface_rows.append(summary)
        candidate_rows.extend(rows)
    surface_rows.sort(
        key=lambda row: (
            row["strict_falsification_rate_ppm"]
            if row["strict_falsification_rate_ppm"] is not None
            else 1_000_001,
            -int(row["forward_testable_cell_count"]),
            str(row["boundary_mode"]),
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_directional_boundary_gate_surface",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "train_row_count": len(train_rows),
        "calibration_row_count": len(calibration_rows),
        "prior_forward_row_count": len(prior_forward_rows),
        "forward_row_count": len(forward_rows),
        "surface_count": len(surface_rows),
        "top_surfaces": surface_rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "surface_rows.jsonl", surface_rows)
    write_jsonl(args.output_dir / "candidate_rows.jsonl", candidate_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
