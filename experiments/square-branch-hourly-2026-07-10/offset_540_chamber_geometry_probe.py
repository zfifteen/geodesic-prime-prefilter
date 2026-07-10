#!/usr/bin/env python3
"""PGS-native chamber-geometry audit on the 4e8-5e8 utilization maximum.

Objects:
  - ordered prime-gap state before first interior prime square w = r^2
  - divisor-count field tau on prefix {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - early tau=4 chamber vs late tau=3 (prime-square) separation

Predictions P1-P5 test chamber separation on segment utilization maxima.
Prediction P6 tests the residual fixed-band claim D(r) in [528, 552].

Audit-only surface. Does not choose primes or perform PGS inference.
Does not port d=4 SDA. Prime-Square Proximity Theorem remains proved in PROOF.md;
this probe measures residual chamber structure only.
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

# Prior segment utilization maxima (measured; not re-derived here as theorem bounds).
PRIOR_EXTREMAL_ROWS = [
    {"segment": "3e7-1e8", "r": 82_357_433, "offset": 540},
    {"segment": "1e8-2e8", "r": 102_017_779, "offset": 462},
    {"segment": "2e8-3e8", "r": 251_066_071, "offset": 540},
    {"segment": "3e8-4e8", "r": 358_018_553, "offset": 546},
]

NEW_SEGMENT = "4e8-5e8"
OFFSET_BAND = (528, 552)

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
        "falsifier": "prefix_min_tau != 4 on a segment extremal row",
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
        "falsifier": "offset outside band on a segment utilization maximum",
    },
]


def previous_prime_before_square(square: int) -> int:
    """Audit helper: walk back from r^2-2 to locate P(r^2). Not a PGS gate."""
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


def analyze_row(
    r: int,
    expected_offset: int | None = None,
    previous_prime: int | None = None,
) -> dict[str, object]:
    square = r * r
    p = int(previous_prime) if previous_prime is not None else previous_prime_before_square(square)
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
        "early_tau4_bound": max(1, int(0.05 * offset)),
    }


def evaluate_prediction(prediction: dict[str, str], row: dict[str, object]) -> dict[str, object]:
    offset = int(row["offset"])
    prefix = row["prefix"]
    band_lo, band_hi = OFFSET_BAND

    if prediction["id"] == "P1":
        passed = bool(row["selected_square_branch"])
    elif prediction["id"] == "P2":
        passed = prefix["prefix_min_tau"] == 4
    elif prediction["id"] == "P3":
        passed = int(row["first_tau3_offset"]) == offset
    elif prediction["id"] == "P4":
        passed = int(row["first_tau4_offset"]) <= max(1, int(0.05 * offset))
    elif prediction["id"] == "P5":
        passed = int(prefix["tau5_count"]) == 0
    elif prediction["id"] == "P6":
        passed = band_lo <= offset <= band_hi
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
        "pass": passed,
        "status": "holds" if passed else "falsified",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Offset-540 / chamber-geometry probe on 4e8-5e8 extremal."
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        default=ROOT
        / "research"
        / "04-bounded-compression"
        / "output"
        / "square_branch_dynamic_cutoff_search_4e8_5e8"
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
    new_row = analyze_row(
        int(max_row["p"]),
        int(max_row["offset"]),
        previous_prime=int(max_row["previous_prime"]),
    ) | {
        "segment": NEW_SEGMENT,
        "utilization": summary["max_dynamic_cutoff_utilization"],
        "dynamic_cutoff": max_row["dynamic_cutoff"],
        "o_q": max_row["o_q"],
    }

    # Secondary residual surface: per-o_q maxima on the same segment (not the law).
    oq_rows: list[dict[str, object]] = []
    for o_q_key, row in sorted(summary.get("max_row_by_o_q", {}).items(), key=lambda item: int(item[0])):
        analyzed = analyze_row(
            int(row["p"]),
            int(row["offset"]),
            previous_prime=int(row["previous_prime"]),
        ) | {
            "segment": f"{NEW_SEGMENT}/o_q={o_q_key}",
            "utilization": row["dynamic_cutoff_utilization"],
            "dynamic_cutoff": row["dynamic_cutoff"],
            "o_q": row["o_q"],
        }
        oq_rows.append(analyzed)

    prior_rows = [
        analyze_row(item["r"], item["offset"]) | {"segment": item["segment"]}
        for item in PRIOR_EXTREMAL_ROWS
    ]

    # Primary evaluation surface: prior segment maxima + new global max.
    primary_rows = prior_rows + [new_row]
    prediction_results = [
        evaluate_prediction(prediction, row)
        for prediction in PREDICTIONS
        for row in primary_rows
    ]

    new_results = [
        result for result in prediction_results if result["segment"] == NEW_SEGMENT
    ]
    falsified_on_new = [result for result in new_results if not result["pass"]]
    chamber_ids = {"P1", "P2", "P3", "P4", "P5"}
    chamber_on_new = [result for result in new_results if result["id"] in chamber_ids]
    chamber_holds = all(result["pass"] for result in chamber_on_new)
    p6_new = next(result for result in new_results if result["id"] == "P6")

    # o_q secondary table (chamber checks only; P6 band is not claimed per o_q).
    oq_chamber_results = [
        evaluate_prediction(prediction, row)
        for prediction in PREDICTIONS
        if prediction["id"] in chamber_ids
        for row in oq_rows
    ]

    prior_pass_counts = {
        prediction["id"]: sum(
            1
            for result in prediction_results
            if result["id"] == prediction["id"]
            and result["segment"] != NEW_SEGMENT
            and result["pass"]
        )
        for prediction in PREDICTIONS
    }

    residual_claims = [
        {
            "id": "RC1",
            "claim": (
                "Early tau=4 / late tau=3 chamber separation (P1-P5) holds on "
                "segment utilization maxima through 4e8-5e8."
            ),
            "status": "holds" if chamber_holds else "falsified",
            "evidence_row": {
                "segment": NEW_SEGMENT,
                "r": new_row["r"],
                "offset": new_row["offset"],
                "first_tau4_offset": new_row["first_tau4_offset"],
                "first_tau3_offset": new_row["first_tau3_offset"],
                "tau4_count": new_row["prefix"]["tau4_count"],
                "tau5_count": new_row["prefix"]["tau5_count"],
            },
        },
        {
            "id": "RC2",
            "claim": (
                "Fixed near-540 band D(r) in [528, 552] on segment utilization "
                "maxima is not a law."
            ),
            "status": "falsified" if not p6_new["pass"] else "holds",
            "evidence_row": {
                "segment": NEW_SEGMENT,
                "r": new_row["r"],
                "offset": new_row["offset"],
                "band": list(OFFSET_BAND),
            },
        },
    ]

    payload = {
        "inputs": {
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe_note": (
                "prefix_tau_floor_probe.json (3 prior rows) was read from the "
                "source clone; chamber fields match prior rows used here. "
                "d4 SDA transfer remains invalidated and is not re-tested."
            ),
            "prior_extremal_count": len(prior_rows),
            "new_extremal": {
                "segment": NEW_SEGMENT,
                "r": new_row["r"],
                "offset": new_row["offset"],
                "utilization": summary["max_dynamic_cutoff_utilization"],
                "dynamic_cutoff": max_row["dynamic_cutoff"],
                "o_q": max_row["o_q"],
            },
            "offset_band": list(OFFSET_BAND),
        },
        "predictions": PREDICTIONS,
        "prior_rows": prior_rows,
        "new_row": new_row,
        "oq_rows": oq_rows,
        "prediction_results": prediction_results,
        "prior_pass_counts": prior_pass_counts,
        "new_segment_results": new_results,
        "oq_chamber_results": oq_chamber_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "chamber_geometry_holds_on_new_extremal": chamber_holds,
            "falsified_predictions_on_new_extremal": [
                item["id"] for item in falsified_on_new
            ],
            "offset_540_band_holds_on_new_extremal": bool(p6_new["pass"]),
            "fixed_540_band_status": (
                "falsified_on_4e8_5e8_utilization_maximum"
                if not p6_new["pass"]
                else "holds_on_new_extremal"
            ),
            "theorem_status": (
                "Prime-Square Proximity Theorem proved in PROOF.md; this probe "
                "is residual chamber-structure audit only"
            ),
            "invalidated_route": "d=4 SDA transfer (not tested here; remains invalidated)",
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-10/"
            "offset_540_chamber_geometry_probe.py"
        ),
    }

    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["conclusion"], indent=2))
    print("residual_claims:")
    print(json.dumps(residual_claims, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
