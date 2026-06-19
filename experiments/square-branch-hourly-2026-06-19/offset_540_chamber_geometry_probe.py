#!/usr/bin/env python3
"""PGS-native chamber-geometry audit for recurring square offsets near 540.

Objects:
  - gap interior I = {p+1, ..., r^2 - 1} before first interior prime square
  - divisor-count field tau(n)
  - backward distance D(r) = r^2 - P(r^2)

Predictions test early tau=4 chamber vs late tau=3 (prime-square) separation.
Audit-only: does not choose primes or perform PGS inference. No d=4 SDA port.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2
from sympy import prevprime

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
if str(FIELD_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_DIR))

from z_band_prime_composite_field import divisor_counts_segment

PRIOR_EXTREMAL_ROWS = [
    {"segment": "3e7-1e8", "r": 82_357_433, "offset": 540},
    {"segment": "1e8-2e8", "r": 102_017_779, "offset": 462},
    {"segment": "2e8-3e8", "r": 251_066_071, "offset": 540},
]

NEW_EXTREMAL_ROW = {"segment": "3e8-4e8", "r": 358_018_553, "offset": 546}

PREDICTIONS = [
    {
        "id": "P1",
        "name": "selected_square_branch",
        "statement": "s^2 < p < r^2 for prime s immediately before r",
        "falsifier": "any extremal row fails selected-square characterization",
    },
    {
        "id": "P2",
        "name": "prefix_min_tau_is_4",
        "statement": "min tau over {p+1, ..., r^2-1} equals 4 (no tau<=3 before square)",
        "falsifier": "prefix_min_tau < 4 on a segment extremal row",
    },
    {
        "id": "P3",
        "name": "late_tau3_at_offset",
        "statement": "first offset with tau<=3 equals observed D(r)",
        "falsifier": "first_tau3_offset != offset",
    },
    {
        "id": "P4",
        "name": "early_tau4_chamber",
        "statement": "first offset with tau<=4 is at most 0.05 * D(r)",
        "falsifier": "first_tau4_offset > 0.05 * offset",
    },
    {
        "id": "P5",
        "name": "no_tau5_prefix",
        "statement": "prefix before r^2 contains zero integers with tau=5",
        "falsifier": "tau5_count > 0",
    },
    {
        "id": "P6",
        "name": "offset_near_540_band",
        "statement": "D(r) lies in [528, 552] on segment utilization maxima",
        "falsifier": "offset outside band on a new segment maximum",
    },
]


def previous_prime_before_square(square: int) -> int:
    candidate = square - 2
    while not gmpy2.is_prime(candidate):
        candidate -= 2
    return int(candidate)


def prefix_tau_values(p: int, square: int) -> list[int]:
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def first_offset_with_tau_at_most(tau_values: list[int], k: int) -> int:
    for offset, value in enumerate(tau_values, start=1):
        if value <= k:
            return offset
    return len(tau_values) + 1


def prefix_summary(tau_values: list[int]) -> dict[str, object]:
    if not tau_values:
        return {
            "prefix_length": 0,
            "prefix_min_tau": None,
            "prefix_max_tau": None,
            "tau4_count": 0,
            "tau5_count": 0,
        }
    return {
        "prefix_length": len(tau_values),
        "prefix_min_tau": min(tau_values),
        "prefix_max_tau": max(tau_values),
        "tau4_count": sum(1 for value in tau_values if value == 4),
        "tau5_count": sum(1 for value in tau_values if value == 5),
    }


def analyze_row(r: int, expected_offset: int | None = None) -> dict[str, object]:
    square = r * r
    p = previous_prime_before_square(square)
    s = int(prevprime(r))
    offset = square - p
    tau_values = prefix_tau_values(p, square)
    prefix = prefix_summary(tau_values)
    first_tau4 = first_offset_with_tau_at_most(tau_values, 4)
    first_tau3 = first_offset_with_tau_at_most(tau_values, 3)
    return {
        "r": r,
        "p": p,
        "s": s,
        "square": square,
        "offset": offset,
        "expected_offset": expected_offset,
        "selected_square_branch": s * s < p < square,
        "prefix": prefix,
        "first_tau4_offset": first_tau4,
        "first_tau3_offset": first_tau3,
    }


def evaluate_prediction(prediction: dict[str, str], row: dict[str, object]) -> dict[str, object]:
    offset = int(row["offset"])
    prefix = row["prefix"]
    checks: dict[str, bool] = {}

    if prediction["id"] == "P1":
        checks["pass"] = bool(row["selected_square_branch"])
    elif prediction["id"] == "P2":
        checks["pass"] = prefix["prefix_min_tau"] == 4
    elif prediction["id"] == "P3":
        checks["pass"] = int(row["first_tau3_offset"]) == offset
    elif prediction["id"] == "P4":
        checks["pass"] = int(row["first_tau4_offset"]) <= max(1, int(0.05 * offset))
    elif prediction["id"] == "P5":
        checks["pass"] = int(prefix["tau5_count"]) == 0
    elif prediction["id"] == "P6":
        checks["pass"] = 528 <= offset <= 552
    else:
        raise ValueError(f"unknown prediction id: {prediction['id']}")

    return {
        "id": prediction["id"],
        "name": prediction["name"],
        "statement": prediction["statement"],
        "falsifier": prediction["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": offset,
        "pass": checks["pass"],
        "status": "holds" if checks["pass"] else "falsified",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Offset-540 chamber geometry probe.")
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=ROOT
        / "research"
        / "04-bounded-compression"
        / "output"
        / "square_branch_dynamic_cutoff_search_3e8_4e8"
        / "square_branch_dynamic_cutoff_search_summary.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_prediction_table.json",
    )
    args = parser.parse_args()

    summary = json.loads(args.summary_json.read_text(encoding="utf-8"))
    max_row = summary["max_row"]
    new_row = analyze_row(int(max_row["p"]), int(max_row["offset"])) | NEW_EXTREMAL_ROW
    prior_rows = [
        analyze_row(item["r"], item["offset"]) | {"segment": item["segment"]}
        for item in PRIOR_EXTREMAL_ROWS
    ]

    all_rows = prior_rows + [new_row]
    prediction_results = [
        evaluate_prediction(prediction, row)
        for prediction in PREDICTIONS
        for row in all_rows
    ]

    prior_pass_counts = {
        prediction["id"]: sum(
            1
            for result in prediction_results
            if result["id"] == prediction["id"] and result["segment"] != NEW_EXTREMAL_ROW["segment"] and result["pass"]
        )
        for prediction in PREDICTIONS
    }

    new_results = [
        result for result in prediction_results if result["segment"] == NEW_EXTREMAL_ROW["segment"]
    ]
    falsified_on_new = [result for result in new_results if not result["pass"]]

    payload = {
        "inputs": {
            "falsification_summary_json": str(args.summary_json),
            "prior_extremal_count": len(prior_rows),
            "new_extremal": {
                "segment": new_row["segment"],
                "r": new_row["r"],
                "offset": new_row["offset"],
                "utilization": summary["max_dynamic_cutoff_utilization"],
            },
        },
        "predictions": PREDICTIONS,
        "prior_rows": prior_rows,
        "new_row": new_row,
        "prediction_results": prediction_results,
        "prior_pass_counts": prior_pass_counts,
        "new_segment_results": new_results,
        "conclusion": {
            "chamber_geometry_holds_on_new_extremal": len(falsified_on_new) == 0,
            "falsified_predictions_on_new_extremal": [item["id"] for item in falsified_on_new],
            "offset_540_band_holds_on_new_extremal": any(
                item["id"] == "P6" and item["pass"] for item in new_results
            ),
            "theorem_status": "unresolved",
            "invalidated_route": "d=4 SDA transfer (not tested here; remains invalidated)",
        },
    }

    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["conclusion"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())