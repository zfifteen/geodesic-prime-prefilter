#!/usr/bin/env python3
"""Test exact endpoint-pair exclusions with at-winner right-boundary gates."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from endpoint_pair_family_profile import parse_endpoint_pair
from first_gap_compatibility_check import write_json, write_jsonl
from hybrid_endpoint_pair_surface import split_slot
from slot_factor_public_quotient_test import factor_projection, public_projection, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_17001_19000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_19001_21000"
DEFAULT_PRIOR_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_21001_23000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_23001_25000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "joint_endpoint_pair_right_boundary_surface_23001_25000"
RULE_ID = "pedk_joint_endpoint_pair_right_boundary_surface_v1"
MIN_PUBLIC_SUPPORT = 5
MIN_FACTOR_SUPPORT = 5
TOP_K_VALUES = (200, 500, 1000)


RIGHT_INDEX_MODES = (
    "right_residues",
    "right_residue_phases",
)


def endpoint_pairs(row: dict[str, object]) -> tuple[tuple[str, str], tuple[str, str]]:
    """Return two unordered directed endpoint pairs."""
    pair_word = factor_projection(row, "unordered_endpoint_pair_residue_phase")
    first, second = pair_word.split(" || ", 1)
    return parse_endpoint_pair(first), parse_endpoint_pair(second)


def pair_identity_key(row: dict[str, object]) -> str:
    """Return exact unordered directed endpoint-pair identity."""
    return " || ".join(
        f"L={left}|R={right}"
        for left, right in endpoint_pairs(row)
    )


def right_index_key(row: dict[str, object], mode: str) -> str:
    """Return sorted right-boundary index for an exact endpoint pair."""
    rights = [right for _, right in endpoint_pairs(row)]
    if mode == "right_residues":
        return "Rres=" + "|".join(sorted(split_slot(right)[0] for right in rights))
    if mode == "right_residue_phases":
        return "R=" + "|".join(sorted(rights))
    raise ValueError(f"unknown right index mode: {mode}")


def endpoint_pair_fields(pair_key: str) -> dict[str, str]:
    """Return flat endpoint-pair fields for candidate output rows."""
    first, second = pair_key.split(" || ", 1)
    left_1, right_1 = parse_endpoint_pair(first)
    left_2, right_2 = parse_endpoint_pair(second)
    return {
        "endpoint_pair_left_1": left_1,
        "endpoint_pair_right_1": right_1,
        "endpoint_pair_left_2": left_2,
        "endpoint_pair_right_2": right_2,
    }


def public_key(row: dict[str, object]) -> str:
    """Return the broad public grammar key."""
    return public_projection(row, "public_word_gwr_side")


def public_is_at_winner(public_value: str) -> bool:
    """Return whether a public key is the at-winner public side."""
    return public_value.endswith("|at_winner")


def rate_ppm(falsified_count: int, testable_count: int) -> int | None:
    """Return integer falsification rate per million testable cells."""
    return falsified_count * 1_000_000 // testable_count if testable_count else None


def rate_mpermille(falsified_count: int, testable_count: int) -> int | None:
    """Return integer falsification rate per thousand testable cells."""
    return falsified_count * 1000 // testable_count if testable_count else None


def exact_surface(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the broad exact endpoint-pair surface."""
    public_counts = Counter(public_key(row) for row in rows)
    pair_counts = Counter(pair_identity_key(row) for row in rows)
    observed_counts = Counter((public_key(row), pair_identity_key(row)) for row in rows)
    supported_public = {
        key for key, count in public_counts.items() if count >= MIN_PUBLIC_SUPPORT
    }
    supported_pairs = {
        key for key, count in pair_counts.items() if count >= MIN_FACTOR_SUPPORT
    }
    observed_supported = {
        cell
        for cell in observed_counts
        if cell[0] in supported_public and cell[1] in supported_pairs
    }
    return {
        "public_counts": public_counts,
        "pair_counts": pair_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_pairs": supported_pairs,
        "observed_supported": observed_supported,
    }


def right_surface(
    rows: list[dict[str, object]],
    right_index_mode: str,
) -> dict[str, object]:
    """Return the at-winner right-boundary index surface."""
    projected = [
        (public_key(row), right_index_key(row, right_index_mode))
        for row in rows
        if str(row["public_gwr_side"]) == "at_winner"
    ]
    public_counts = Counter(public for public, _ in projected)
    right_counts = Counter(right for _, right in projected)
    observed_counts = Counter(projected)
    supported_public = {
        key for key, count in public_counts.items() if count >= MIN_PUBLIC_SUPPORT
    }
    supported_right = {
        key for key, count in right_counts.items() if count >= MIN_FACTOR_SUPPORT
    }
    observed_supported = {
        cell
        for cell in observed_counts
        if cell[0] in supported_public and cell[1] in supported_right
    }
    return {
        "public_counts": public_counts,
        "right_counts": right_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_right": supported_right,
        "observed_supported": observed_supported,
    }


def exact_candidate_cells(*surfaces: dict[str, object]) -> set[tuple[str, str]]:
    """Return cells supported in every broad surface and absent in prior surfaces."""
    candidate_cells = set(
        itertools.product(surfaces[0]["supported_public"], surfaces[0]["supported_pairs"])
    )
    for surface in surfaces:
        candidate_cells &= set(
            itertools.product(surface["supported_public"], surface["supported_pairs"])
        )
        candidate_cells -= surface["observed_supported"]
    return candidate_cells


def right_absent_cells(
    right_surfaces: tuple[dict[str, object], ...],
) -> set[tuple[str, str]]:
    """Return at-winner right-index cells supported in every surface and absent."""
    candidate_cells = set(
        itertools.product(
            right_surfaces[0]["supported_public"],
            right_surfaces[0]["supported_right"],
        )
    )
    for surface in right_surfaces:
        candidate_cells &= set(
            itertools.product(surface["supported_public"], surface["supported_right"])
        )
        candidate_cells -= surface["observed_supported"]
    return candidate_cells


def top_k_metrics(rows: list[dict[str, object]]) -> dict[str, dict[str, int | None]]:
    """Return survival metrics for highest-support joint cells."""
    ordered = sorted(
        rows,
        key=lambda row: (
            -int(row["minimum_prior_pair_support"]),
            -int(row["minimum_prior_right_index_support"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        ),
    )
    out = {}
    for value in TOP_K_VALUES:
        selected = ordered[:value]
        testable = [
            row for row in selected
            if row["status"] != "not_testable_forward"
        ]
        falsified = [
            row for row in testable
            if row["exact_pair_falsified"]
        ]
        out[f"top_{value}"] = {
            "row_count": len(selected),
            "testable_count": len(testable),
            "falsified_count": len(falsified),
            "strict_falsification_rate_mpermille": rate_mpermille(
                len(falsified),
                len(testable),
            ),
            "strict_falsification_rate_ppm": rate_ppm(
                len(falsified),
                len(testable),
            ),
        }
    return out


def analyze(
    train_rows: list[dict[str, object]],
    calibration_rows: list[dict[str, object]],
    prior_forward_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
    right_index_mode: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Analyze exact pair exclusions gated by at-winner right-boundary absence."""
    train = exact_surface(train_rows)
    calibration = exact_surface(calibration_rows)
    prior_forward = exact_surface(prior_forward_rows)
    forward = exact_surface(forward_rows)
    train_right = right_surface(train_rows, right_index_mode)
    calibration_right = right_surface(calibration_rows, right_index_mode)
    prior_forward_right = right_surface(prior_forward_rows, right_index_mode)
    forward_right = right_surface(forward_rows, right_index_mode)

    exact_candidates = exact_candidate_cells(train, calibration, prior_forward)
    at_winner_candidates = {
        cell for cell in exact_candidates if public_is_at_winner(cell[0])
    }
    right_absences = right_absent_cells(
        (train_right, calibration_right, prior_forward_right)
    )
    rows = []
    for public_value, pair_value in sorted(at_winner_candidates):
        right_value = right_index_from_pair_key(pair_value, right_index_mode)
        if (public_value, right_value) not in right_absences:
            continue
        forward_pair_testable = (
            public_value in forward["supported_public"]
            and pair_value in forward["supported_pairs"]
        )
        forward_right_testable = (
            public_value in forward_right["supported_public"]
            and right_value in forward_right["supported_right"]
        )
        exact_falsified = (
            forward_pair_testable
            and (public_value, pair_value) in forward["observed_supported"]
        )
        right_falsified = (
            forward_right_testable
            and (public_value, right_value) in forward_right["observed_supported"]
        )
        if not forward_pair_testable:
            status = "not_testable_forward"
        elif exact_falsified:
            status = "falsified_forward"
        else:
            status = "survived_forward"
        endpoint_fields = endpoint_pair_fields(pair_value)
        row = {
            "rule_id": RULE_ID,
            "right_index_mode": right_index_mode,
            "public_key": public_value,
            "public_containing_exact_type_key": containing_type_from_public(public_value),
            "public_gwr_side": "at_winner",
            "pair_identity_key": pair_value,
            "right_index_key": right_value,
            "right_boundary_residues": right_residues_from_pair_key(pair_value),
            "right_boundary_phases": right_phases_from_pair_key(pair_value),
            "train_public_support": train["public_counts"][public_value],
            "train_pair_support": train["pair_counts"][pair_value],
            "train_right_index_support": train_right["right_counts"][right_value],
            "calibration_public_support": calibration["public_counts"][public_value],
            "calibration_pair_support": calibration["pair_counts"][pair_value],
            "calibration_right_index_support": calibration_right["right_counts"][right_value],
            "prior_forward_public_support": prior_forward["public_counts"][public_value],
            "prior_forward_pair_support": prior_forward["pair_counts"][pair_value],
            "prior_forward_right_index_support": prior_forward_right["right_counts"][right_value],
            "forward_public_support": forward["public_counts"][public_value],
            "forward_pair_support": forward["pair_counts"][pair_value],
            "forward_right_index_support": forward_right["right_counts"][right_value],
            "forward_observed_count": forward["observed_counts"][(public_value, pair_value)],
            "forward_right_observed_count": forward_right["observed_counts"][
                (public_value, right_value)
            ],
            "minimum_prior_pair_support": min(
                train["pair_counts"][pair_value],
                calibration["pair_counts"][pair_value],
                prior_forward["pair_counts"][pair_value],
            ),
            "minimum_prior_right_index_support": min(
                train_right["right_counts"][right_value],
                calibration_right["right_counts"][right_value],
                prior_forward_right["right_counts"][right_value],
            ),
            "exact_pair_falsified": exact_falsified,
            "right_index_falsified": right_falsified,
            "status": status,
        }
        row.update(endpoint_fields)
        rows.append(row)

    testable = [row for row in rows if row["status"] != "not_testable_forward"]
    falsified = [row for row in testable if row["exact_pair_falsified"]]
    survived = [row for row in testable if not row["exact_pair_falsified"]]
    right_testable = [
        row for row in rows
        if (
            row["public_key"] in forward_right["supported_public"]
            and row["right_index_key"] in forward_right["supported_right"]
        )
    ]
    right_falsified = [row for row in right_testable if row["right_index_falsified"]]
    summary = {
        "rule_id": RULE_ID,
        "right_index_mode": right_index_mode,
        "min_public_support": MIN_PUBLIC_SUPPORT,
        "min_factor_support": MIN_FACTOR_SUPPORT,
        "exact_absent_candidate_cell_count": len(exact_candidates),
        "at_winner_exact_absent_candidate_cell_count": len(at_winner_candidates),
        "right_absent_cell_count": len(right_absences),
        "joint_candidate_cell_count": len(rows),
        "forward_testable_cell_count": len(testable),
        "survived_forward_cell_count": len(survived),
        "falsified_forward_cell_count": len(falsified),
        "not_testable_forward_cell_count": len(rows) - len(testable),
        "strict_falsification_rate_mpermille": rate_mpermille(
            len(falsified),
            len(testable),
        ),
        "strict_falsification_rate_ppm": rate_ppm(
            len(falsified),
            len(testable),
        ),
        "right_index_forward_testable_cell_count": len(right_testable),
        "right_index_falsified_cell_count": len(right_falsified),
        "right_index_falsification_rate_mpermille": rate_mpermille(
            len(right_falsified),
            len(right_testable),
        ),
        "right_index_falsification_rate_ppm": rate_ppm(
            len(right_falsified),
            len(right_testable),
        ),
        "top_k_metrics": top_k_metrics(rows),
    }
    return summary, rows


def right_index_from_pair_key(pair_key: str, mode: str) -> str:
    """Return right-boundary index from an exact endpoint-pair key."""
    rights = [
        parse_endpoint_pair(part)[1]
        for part in pair_key.split(" || ")
    ]
    if mode == "right_residues":
        return "Rres=" + "|".join(sorted(split_slot(right)[0] for right in rights))
    if mode == "right_residue_phases":
        return "R=" + "|".join(sorted(rights))
    raise ValueError(f"unknown right index mode: {mode}")


def right_residues_from_pair_key(pair_key: str) -> str:
    """Return sorted right-boundary residues from a pair key."""
    rights = [parse_endpoint_pair(part)[1] for part in pair_key.split(" || ")]
    return "|".join(sorted(split_slot(right)[0] for right in rights))


def right_phases_from_pair_key(pair_key: str) -> str:
    """Return sorted right-boundary phases from a pair key."""
    rights = [parse_endpoint_pair(part)[1] for part in pair_key.split(" || ")]
    return "|".join(sorted(split_slot(right)[1] for right in rights))


def containing_type_from_public(public_value: str) -> str:
    """Extract the containing exact type from a public word key."""
    marker = "|containing="
    start = public_value.index(marker) + len(marker)
    end = public_value.index("@", start)
    return public_value[start:end]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test exact endpoint-pair exclusions with right-boundary gates."
    )
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--prior-forward-dir", type=Path, default=DEFAULT_PRIOR_FORWARD_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run joint endpoint-pair/right-boundary surface tests."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(args.prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    surface_rows = []
    candidate_rows = []
    for mode in RIGHT_INDEX_MODES:
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
            row["strict_falsification_rate_mpermille"]
            if row["strict_falsification_rate_mpermille"] is not None
            else 1001,
            -int(row["forward_testable_cell_count"]),
            str(row["right_index_mode"]),
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_joint_endpoint_pair_right_boundary_surface",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "train_row_count": len(train_rows),
        "calibration_row_count": len(calibration_rows),
        "prior_forward_row_count": len(prior_forward_rows),
        "forward_row_count": len(forward_rows),
        "surface_count": len(surface_rows),
        "surfaces": surface_rows,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "surface_rows.jsonl", surface_rows)
    write_jsonl(args.output_dir / "candidate_rows.jsonl", candidate_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
