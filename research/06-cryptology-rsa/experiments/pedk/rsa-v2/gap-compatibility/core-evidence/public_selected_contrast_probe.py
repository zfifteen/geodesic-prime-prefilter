#!/usr/bin/env python3
"""Contrast the compact endpoint predicate by public selected-position side."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import (
    containing_type_from_public,
    exact_candidate_cells,
    exact_surface,
    pair_identity_key,
    public_key,
    rate_ppm,
    right_absent_cells,
    right_index_from_pair_key,
    right_residues_from_pair_key,
)
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "public_selected_contrast_probe"
RULE_ID = "pedk_public_selected_contrast_probe_v1"

WINDOWS = (
    (
        "21001_23000",
        "enriched_multiplication_map_corpus_15001_17000",
        "enriched_multiplication_map_corpus_17001_19000",
        "enriched_multiplication_map_corpus_19001_21000",
        "enriched_multiplication_map_corpus_21001_23000",
    ),
    (
        "23001_25000",
        "enriched_multiplication_map_corpus_17001_19000",
        "enriched_multiplication_map_corpus_19001_21000",
        "enriched_multiplication_map_corpus_21001_23000",
        "enriched_multiplication_map_corpus_23001_25000",
    ),
    (
        "25001_27000",
        "enriched_multiplication_map_corpus_19001_21000",
        "enriched_multiplication_map_corpus_21001_23000",
        "enriched_multiplication_map_corpus_23001_25000",
        "enriched_multiplication_map_corpus_25001_27000",
    ),
    (
        "27001_30000",
        "enriched_multiplication_map_corpus_21001_23000",
        "enriched_multiplication_map_corpus_23001_25000",
        "enriched_multiplication_map_corpus_25001_27000",
        "enriched_multiplication_map_corpus_27001_30000",
    ),
    (
        "30001_32000",
        "enriched_multiplication_map_corpus_23001_25000",
        "enriched_multiplication_map_corpus_25001_27000",
        "enriched_multiplication_map_corpus_27001_30000",
        "enriched_multiplication_map_corpus_30001_32000",
    ),
    (
        "32001_34000",
        "enriched_multiplication_map_corpus_25001_27000",
        "enriched_multiplication_map_corpus_27001_30000",
        "enriched_multiplication_map_corpus_30001_32000",
        "enriched_multiplication_map_corpus_32001_34000",
    ),
)

PUBLIC_SIDES = ("before_winner", "at_winner", "after_winner")
RIGHT_RESIDUE_RANK = {"o2": 1, "o4": 2, "o6": 3}


def side_from_public(public_value: str) -> str:
    """Return the public GWR side encoded by a public key."""
    return public_value.rsplit("|", 1)[1]


def compact_endpoint_predicate(pair_value: str) -> bool:
    """Return the compact endpoint predicate for an endpoint-pair key."""
    residues = set(right_residues_from_pair_key(pair_value).split("|"))
    return "o6" not in residues and "o4" in residues


def endpoint_transport_defect(pair_value: str) -> int:
    """Return the right-boundary transport defect for an endpoint-pair key."""
    residues = right_residues_from_pair_key(pair_value).split("|")
    return max(RIGHT_RESIDUE_RANK[value] for value in residues) - RIGHT_RESIDUE_RANK["o4"]


def right_surface(rows: list[dict[str, object]], public_side: str) -> dict[str, object]:
    """Return right-residue surface for one public side."""
    projected = [
        (public_key(row), right_index_from_pair_key(pair_identity_key(row), "right_residues"))
        for row in rows
        if str(row["public_gwr_side"]) == public_side
    ]
    public_counts = Counter(public for public, _ in projected)
    right_counts = Counter(right for _, right in projected)
    observed_counts = Counter(projected)
    supported_public = {key for key, count in public_counts.items() if count >= 5}
    supported_right = {key for key, count in right_counts.items() if count >= 5}
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


def status_counts(rows: list[dict[str, object]]) -> dict[str, int | None]:
    """Return exact endpoint-pair falsification counts."""
    testable = [row for row in rows if row["status"] != "not_testable_forward"]
    falsified = [row for row in testable if row["exact_pair_falsified"]]
    return {
        "row_count": len(rows),
        "testable_count": len(testable),
        "survived_count": len(testable) - len(falsified),
        "falsified_count": len(falsified),
        "falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
    }


def analyze_window(
    window: str,
    train_dir: str,
    calibration_dir: str,
    prior_forward_dir: str,
    forward_dir: str,
) -> list[dict[str, object]]:
    """Analyze one rolling strict-forward window."""
    train_rows = read_jsonl(INPUT_ROOT / train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(INPUT_ROOT / calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(INPUT_ROOT / prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(INPUT_ROOT / forward_dir / "enriched_rows.jsonl")

    train = exact_surface(train_rows)
    calibration = exact_surface(calibration_rows)
    prior_forward = exact_surface(prior_forward_rows)
    forward = exact_surface(forward_rows)
    exact_candidates = exact_candidate_cells(train, calibration, prior_forward)
    rows = []
    for public_side in PUBLIC_SIDES:
        train_right = right_surface(train_rows, public_side)
        calibration_right = right_surface(calibration_rows, public_side)
        prior_forward_right = right_surface(prior_forward_rows, public_side)
        right_absences = right_absent_cells(
            (train_right, calibration_right, prior_forward_right)
        )
        for public_value, pair_value in sorted(exact_candidates):
            if side_from_public(public_value) != public_side:
                continue
            right_value = right_index_from_pair_key(pair_value, "right_residues")
            if (public_value, right_value) not in right_absences:
                continue
            forward_pair_testable = (
                public_value in forward["supported_public"]
                and pair_value in forward["supported_pairs"]
            )
            exact_falsified = (
                forward_pair_testable
                and (public_value, pair_value) in forward["observed_supported"]
            )
            status = "not_testable_forward"
            if forward_pair_testable:
                status = "falsified_forward" if exact_falsified else "survived_forward"
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": window,
                    "public_side": public_side,
                    "public_key": public_value,
                    "public_containing_exact_type_key": containing_type_from_public(
                        public_value
                    ),
                    "pair_identity_key": pair_value,
                    "right_boundary_residues": right_residues_from_pair_key(pair_value),
                    "endpoint_transport_defect": endpoint_transport_defect(pair_value),
                    "compact_endpoint_predicate": compact_endpoint_predicate(pair_value),
                    "forward_observed_count": forward["observed_counts"][
                        (public_value, pair_value)
                    ],
                    "exact_pair_falsified": exact_falsified,
                    "status": status,
                }
            )
    return rows


def summarize(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Return public-side, endpoint-defect, and window summaries."""
    side_groups: dict[tuple[str, bool], list[dict[str, object]]] = defaultdict(list)
    defect_groups: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    window_groups: dict[tuple[str, str, bool], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        side_groups[(str(row["public_side"]), bool(row["compact_endpoint_predicate"]))].append(row)
        defect_groups[
            (str(row["public_side"]), int(row["endpoint_transport_defect"]))
        ].append(row)
        window_groups[
            (
                str(row["window"]),
                str(row["public_side"]),
                bool(row["compact_endpoint_predicate"]),
            )
        ].append(row)

    side_rows = []
    for side in PUBLIC_SIDES:
        for compact in (False, True):
            group = side_groups[(side, compact)]
            side_rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_side": side,
                    "compact_endpoint_predicate": compact,
                    **status_counts(group),
                }
            )
    side_rows.sort(key=lambda row: (str(row["public_side"]), str(row["compact_endpoint_predicate"])))

    defect_rows = []
    for side in PUBLIC_SIDES:
        for defect in (-1, 0, 1):
            group = defect_groups[(side, defect)]
            defect_rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_side": side,
                    "endpoint_transport_defect": defect,
                    **status_counts(group),
                }
            )
    defect_rows.sort(
        key=lambda row: (
            str(row["public_side"]),
            int(row["endpoint_transport_defect"]),
        )
    )

    window_rows = [
        {
            "rule_id": RULE_ID,
            "window": window,
            "public_side": side,
            "compact_endpoint_predicate": compact,
            **status_counts(group),
        }
        for (window, side, compact), group in window_groups.items()
    ]
    window_rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["public_side"]),
            str(row["compact_endpoint_predicate"]),
        )
    )
    return side_rows, defect_rows, window_rows


def main() -> int:
    """Run the public selected-position contrast probe."""
    rows = []
    for args in WINDOWS:
        rows.extend(analyze_window(*args))
    side_rows, defect_rows, window_rows = summarize(rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_selected_contrast_probe",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "window_count": len(WINDOWS),
        "candidate_row_count": len(rows),
        "side_rows": side_rows,
        "endpoint_defect_rows": defect_rows,
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary)
    write_jsonl(OUTPUT_DIR / "candidate_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "side_rows.jsonl", side_rows)
    write_jsonl(OUTPUT_DIR / "endpoint_defect_rows.jsonl", defect_rows)
    write_jsonl(OUTPUT_DIR / "window_rows.jsonl", window_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
