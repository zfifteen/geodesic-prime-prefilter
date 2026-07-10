#!/usr/bin/env python3
"""Residual chamber claims RC3-RC5 after fixed near-540 band death (RC2).

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - early tau=4 chamber load (tau4_count, first_tau4_offset)
  - wheel first-open class o_q of the endpoint prime p = P(r^2)

Prior hour falsified fixed band RC2 / P6 on the 4e8-5e8 utilization maximum
(D=738). This probe does not replay P1-P6 as the primary surface. It states
and checks the next residual claims:

  P7 / RC3: tau4 density rho4 = tau4_count / D(r) in [0.10, 0.14]
  P8 / RC4: absolute early chamber first_tau4_offset <= 20
  P9 / RC5: o_q=2 branch maximum near-540 attractor |D-540| <= 20
            (local residual only; not a universal offset law)

Audit-only. Does not choose primes as PGS inference. Does not port d=4 SDA.
Prime-Square Proximity Theorem remains proved in PROOF.md; this is residual
structure after the fixed-band residual failed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WALK_DIR = ROOT / "research" / "02-gwr-dni" / "scripts"
if str(WALK_DIR) not in sys.path:
    sys.path.insert(0, str(WALK_DIR))

import gwr_dni_recursive_walk as walk  # noqa: E402

PRIOR_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10"
    / "offset_540_prediction_table.json"
)
SUMMARY_JSON = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "output"
    / "square_branch_dynamic_cutoff_search_4e8_5e8"
    / "square_branch_dynamic_cutoff_search_summary.json"
)
PREFIX_TAU_JSON = (
    ROOT
    / "experiments"
    / "square-branch-sda-invalidation-2026-06"
    / "prefix_tau_floor_probe.json"
)

RHO4_LO = 0.10
RHO4_HI = 0.14
FIRST_TAU4_ABS = 20
NEAR_540_RADIUS = 20
NEAR_540_CENTER = 540

PREDICTIONS = [
    {
        "id": "P7",
        "name": "tau4_density_band",
        "statement": (
            f"On segment utilization maxima, rho4 = tau4_count / D(r) "
            f"lies in [{RHO4_LO}, {RHO4_HI}]."
        ),
        "falsifier": f"any primary row with rho4 outside [{RHO4_LO}, {RHO4_HI}]",
    },
    {
        "id": "P8",
        "name": "absolute_early_tau4",
        "statement": (
            f"On segment utilization maxima, first_tau4_offset <= {FIRST_TAU4_ABS}."
        ),
        "falsifier": f"any primary row with first_tau4_offset > {FIRST_TAU4_ABS}",
    },
    {
        "id": "P9",
        "name": "oq2_near_540_attractor",
        "statement": (
            f"On per-o_q=2 segment maxima, |D(r) - {NEAR_540_CENTER}| "
            f"<= {NEAR_540_RADIUS} (local residual, not a universal law)."
        ),
        "falsifier": (
            f"any o_q=2 branch maximum with |D-540| > {NEAR_540_RADIUS}"
        ),
    },
]


def _rho4(row: dict) -> float:
    offset = int(row["offset"])
    if offset <= 0:
        return float("nan")
    return float(row["prefix"]["tau4_count"]) / float(offset)


def _with_o_q(row: dict) -> dict:
    out = dict(row)
    # Row field p is the previous prime before r^2 (endpoint prime for D(r)).
    p = int(row["p"])
    out["o_q"] = int(walk.first_open_offset(p % 30))
    out["rho4"] = _rho4(row)
    out["abs_d_minus_540"] = abs(int(row["offset"]) - NEAR_540_CENTER)
    return out


def evaluate(prediction: dict, row: dict) -> dict:
    offset = int(row["offset"])
    if prediction["id"] == "P7":
        rho = float(row["rho4"])
        passed = RHO4_LO <= rho <= RHO4_HI
        detail = {"rho4": rho, "band": [RHO4_LO, RHO4_HI]}
    elif prediction["id"] == "P8":
        first4 = int(row["first_tau4_offset"])
        passed = first4 <= FIRST_TAU4_ABS
        detail = {"first_tau4_offset": first4, "bound": FIRST_TAU4_ABS}
    elif prediction["id"] == "P9":
        # Only evaluate on o_q=2 rows.
        if int(row.get("o_q", -1)) != 2:
            return {
                "id": prediction["id"],
                "name": prediction["name"],
                "statement": prediction["statement"],
                "falsifier": prediction["falsifier"],
                "segment": row.get("segment"),
                "r": row["r"],
                "offset": offset,
                "o_q": row.get("o_q"),
                "pass": None,
                "status": "not_applicable",
                "detail": {"reason": "row is not o_q=2"},
            }
        gap = int(row["abs_d_minus_540"])
        passed = gap <= NEAR_540_RADIUS
        detail = {
            "abs_d_minus_540": gap,
            "radius": NEAR_540_RADIUS,
            "center": NEAR_540_CENTER,
        }
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
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": detail,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="RC3-RC5 residual chamber probe after fixed-540 band death."
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc3_prediction_table.json",
    )
    args = parser.parse_args()

    prior_payload = json.loads(args.prior_table.read_text(encoding="utf-8"))
    summary = json.loads(args.summary_json.read_text(encoding="utf-8"))
    prefix_tau_note = None
    if args.prefix_tau_json.is_file():
        prefix_tau = json.loads(args.prefix_tau_json.read_text(encoding="utf-8"))
        prefix_tau_note = {
            "path": str(args.prefix_tau_json),
            "extremal_count": len(prefix_tau.get("extremal_rows", [])),
            "d4_sda_transfers": prefix_tau.get("conclusion", {}).get(
                "d4_tau5_sda_route_transfers_to_square_branch"
            ),
        }

    primary_rows = [
        _with_o_q(row) for row in prior_payload["prior_rows"] + [prior_payload["new_row"]]
    ]
    oq_rows = [_with_o_q(row) for row in prior_payload.get("oq_rows", [])]

    # Ensure o_q=2 branch max from summary is present (should already be in oq_rows).
    oq2_rows = [row for row in oq_rows if int(row["o_q"]) == 2]
    if not oq2_rows and "2" in summary.get("max_row_by_o_q", {}):
        # Fallback: cannot rebuild chamber without tau scan; fail closed.
        raise SystemExit("missing o_q=2 chamber row in prior table")

    results_primary = [
        evaluate(pred, row)
        for pred in PREDICTIONS
        if pred["id"] in {"P7", "P8"}
        for row in primary_rows
    ]
    results_oq2 = [
        evaluate(PREDICTIONS[2], row)  # P9
        for row in oq2_rows
    ]

    def holds_all(pid: str, results: list[dict]) -> bool:
        subset = [r for r in results if r["id"] == pid and r["pass"] is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p7_holds = holds_all("P7", results_primary)
    p8_holds = holds_all("P8", results_primary)
    p9_holds = holds_all("P9", results_oq2)

    # Annotate primary rows with o_q for the residual table.
    primary_o_q_summary = [
        {
            "segment": row["segment"],
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row["o_q"],
            "rho4": row["rho4"],
            "first_tau4_offset": row["first_tau4_offset"],
            "tau4_count": row["prefix"]["tau4_count"],
            "abs_d_minus_540": row["abs_d_minus_540"],
        }
        for row in primary_rows
    ]
    oq2_summary = [
        {
            "segment": row["segment"],
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row["o_q"],
            "rho4": row["rho4"],
            "first_tau4_offset": row["first_tau4_offset"],
            "abs_d_minus_540": row["abs_d_minus_540"],
        }
        for row in oq2_rows
    ]

    residual_claims = [
        {
            "id": "RC3",
            "claim": (
                "On segment utilization maxima through 4e8-5e8, tau4 density "
                f"rho4 = tau4_count/D(r) lies in [{RHO4_LO}, {RHO4_HI}]."
            ),
            "status": "holds" if p7_holds else "falsified",
            "linked_prediction": "P7",
            "evidence": primary_o_q_summary,
        },
        {
            "id": "RC4",
            "claim": (
                "On segment utilization maxima through 4e8-5e8, absolute early "
                f"chamber bound first_tau4_offset <= {FIRST_TAU4_ABS} holds."
            ),
            "status": "holds" if p8_holds else "falsified",
            "linked_prediction": "P8",
            "evidence": [
                {
                    "segment": row["segment"],
                    "first_tau4_offset": row["first_tau4_offset"],
                    "bound": FIRST_TAU4_ABS,
                }
                for row in primary_rows
            ],
        },
        {
            "id": "RC5",
            "claim": (
                "Local residual after RC2 death: the o_q=2 branch maximum on "
                "4e8-5e8 stays near 540 (|D-540|<=20), while the global "
                "utilization maximum (o_q=6, D=738) escapes the fixed band. "
                "Near-540 is an o_q=2 local attractor residual, not a law."
            ),
            "status": "holds" if p9_holds else "falsified",
            "linked_prediction": "P9",
            "evidence": {
                "oq2_rows": oq2_summary,
                "global_max": {
                    "segment": primary_rows[-1]["segment"],
                    "r": primary_rows[-1]["r"],
                    "offset": primary_rows[-1]["offset"],
                    "o_q": primary_rows[-1]["o_q"],
                    "abs_d_minus_540": primary_rows[-1]["abs_d_minus_540"],
                },
                "note": (
                    "Exact D=540 also appears on non-o_q=2 segment maxima "
                    "(o_q=4 and o_q=6); RC5 is only the o_q=2 local attractor, "
                    "not a claim that 540 is exclusive to o_q=2."
                ),
            },
        },
        {
            "id": "RC2_retained",
            "claim": (
                "Fixed near-540 band D(r) in [528, 552] on segment utilization "
                "maxima is not a law (retained from prior hour)."
            ),
            "status": "falsified",
            "linked_prediction": "P6 (prior)",
            "evidence": {
                "segment": "4e8-5e8",
                "r": 424171123,
                "offset": 738,
            },
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "rho4_band": [RHO4_LO, RHO4_HI],
            "first_tau4_absolute_bound": FIRST_TAU4_ABS,
            "near_540_radius": NEAR_540_RADIUS,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-Square Proximity proved in PROOF.md; residual audit only"
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_o_q_summary,
        "oq2_rows": oq2_summary,
        "prediction_results": results_primary + results_oq2,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC3_tau4_density_band": "holds" if p7_holds else "falsified",
            "RC4_absolute_early_tau4": "holds" if p8_holds else "falsified",
            "RC5_oq2_near_540_local_attractor": (
                "holds" if p9_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "falsified_new_predictions": [
                r["id"]
                for r in results_primary + results_oq2
                if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC3-RC5 after fixed-band death; "
                "does not restate P1-P6 as the sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-10-rc3/"
            "offset_540_residual_rc3_probe.py"
        ),
    }

    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["conclusion"], indent=2))
    print("residual_claims:")
    for claim in residual_claims:
        print(f"  {claim['id']}: {claim['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
