#!/usr/bin/env python3
"""Residual chamber claims RC6-RC8 after RC3-RC5 surface.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - early-tau=4 / late-tau=3 chamber phase order
  - wheel first-open class o_q of endpoint prime p = P(r^2)

Prior residual surface (RC3-RC5) covered tau4 density, absolute early tau4,
and o_q=2 near-540 local attractor on utilization maxima. This probe does
not replay P1-P9 as the primary deliverable. It states and checks the next
residual claims on the full 4e8-5e8 per-o_q branch-max panel:

  P10 / RC6: S2-A phase order on full o_q panel {2,4,6}
             1 <= first_tau4 < first_tau3 = D(r), prefix_min_tau = 4, tau5=0
  P11 / RC7: late-dominant phase gap
             (D(r) - first_tau4) / D(r) >= 0.95 on util maxima and o_q panel
  P12 / RC8: o_q-stratified near-540 exclusivity on 4e8-5e8 branch maxima
             only o_q=2 has |D-540| <= 20; o_q=4 and o_q=6 escape

Audit-only. Does not choose primes as PGS inference. Does not port d=4 SDA.
Prime-Square Proximity Theorem remains proved in PROOF.md; residual audit only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PRIOR_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10"
    / "offset_540_prediction_table.json"
)
RC3_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10-rc3"
    / "offset_540_rc3_prediction_table.json"
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

PHASE_GAP_MIN = 0.95
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20
REQUIRED_OQ = {2, 4, 6}

PREDICTIONS = [
    {
        "id": "P10",
        "name": "oq_panel_phase_order",
        "statement": (
            "On 4e8-5e8 per-o_q branch maxima (o_q in {2,4,6}): "
            "1 <= first_tau4_offset < first_tau3_offset = D(r), "
            "prefix_min_tau = 4, and tau5_count = 0."
        ),
        "falsifier": (
            "any o_q branch-max row fails early-tau4 / late-tau3 phase order "
            "or has prefix_min_tau != 4 or tau5_count > 0"
        ),
    },
    {
        "id": "P11",
        "name": "late_dominant_phase_gap",
        "statement": (
            f"On segment utilization maxima and 4e8-5e8 o_q panel, "
            f"phase_gap = (D(r) - first_tau4_offset) / D(r) >= {PHASE_GAP_MIN}."
        ),
        "falsifier": f"any evaluated row with phase_gap < {PHASE_GAP_MIN}",
    },
    {
        "id": "P12",
        "name": "oq_near_540_exclusivity",
        "statement": (
            "On 4e8-5e8 per-o_q branch maxima, only o_q=2 satisfies "
            f"|D(r) - {NEAR_540_CENTER}| <= {NEAR_540_RADIUS}; "
            "o_q=4 and o_q=6 escape the near-540 band."
        ),
        "falsifier": (
            "o_q=2 branch max escapes |D-540|<=20, or o_q in {4,6} "
            "branch max enters |D-540|<=20"
        ),
    },
]


def _annotate(row: dict) -> dict:
    out = dict(row)
    offset = int(out["offset"])
    first4 = int(out["first_tau4_offset"])
    first3 = int(out["first_tau3_offset"])
    prefix = out["prefix"]
    out["phase_gap"] = (
        float(offset - first4) / float(offset) if offset > 0 else float("nan")
    )
    out["abs_d_minus_540"] = abs(offset - NEAR_540_CENTER)
    out["phase_order_ok"] = (
        1 <= first4 < first3 == offset
        and int(prefix["prefix_min_tau"]) == 4
        and int(prefix["tau5_count"]) == 0
    )
    out["rho4"] = (
        float(prefix["tau4_count"]) / float(offset) if offset > 0 else float("nan")
    )
    return out


def _compact(row: dict) -> dict:
    return {
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "first_tau4_offset": row["first_tau4_offset"],
        "first_tau3_offset": row["first_tau3_offset"],
        "prefix_min_tau": row["prefix"]["prefix_min_tau"],
        "tau4_count": row["prefix"]["tau4_count"],
        "tau5_count": row["prefix"]["tau5_count"],
        "rho4": row["rho4"],
        "phase_gap": row["phase_gap"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "phase_order_ok": row["phase_order_ok"],
    }


def evaluate_p10(row: dict) -> dict:
    passed = bool(row["phase_order_ok"])
    return {
        "id": "P10",
        "name": "oq_panel_phase_order",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "first_tau4_offset": row["first_tau4_offset"],
            "first_tau3_offset": row["first_tau3_offset"],
            "prefix_min_tau": row["prefix"]["prefix_min_tau"],
            "tau5_count": row["prefix"]["tau5_count"],
        },
    }


def evaluate_p11(row: dict) -> dict:
    gap = float(row["phase_gap"])
    passed = gap >= PHASE_GAP_MIN
    return {
        "id": "P11",
        "name": "late_dominant_phase_gap",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "phase_gap": gap,
            "bound": PHASE_GAP_MIN,
            "first_tau4_offset": row["first_tau4_offset"],
        },
    }


def evaluate_p12_panel(oq_rows: list[dict]) -> dict:
    by_oq = {int(row["o_q"]): row for row in oq_rows}
    missing = sorted(REQUIRED_OQ - set(by_oq))
    if missing:
        return {
            "id": "P12",
            "name": "oq_near_540_exclusivity",
            "statement": PREDICTIONS[2]["statement"],
            "falsifier": PREDICTIONS[2]["falsifier"],
            "segment": "4e8-5e8/o_q_panel",
            "r": None,
            "offset": None,
            "o_q": None,
            "pass": False,
            "status": "falsified",
            "detail": {"missing_o_q": missing},
        }

    oq2_near = int(by_oq[2]["abs_d_minus_540"]) <= NEAR_540_RADIUS
    oq4_escapes = int(by_oq[4]["abs_d_minus_540"]) > NEAR_540_RADIUS
    oq6_escapes = int(by_oq[6]["abs_d_minus_540"]) > NEAR_540_RADIUS
    passed = oq2_near and oq4_escapes and oq6_escapes
    return {
        "id": "P12",
        "name": "oq_near_540_exclusivity",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": "4e8-5e8/o_q_panel",
        "r": None,
        "offset": None,
        "o_q": "panel",
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "o_q=2": {
                "r": by_oq[2]["r"],
                "offset": by_oq[2]["offset"],
                "abs_d_minus_540": by_oq[2]["abs_d_minus_540"],
                "near_540": oq2_near,
            },
            "o_q=4": {
                "r": by_oq[4]["r"],
                "offset": by_oq[4]["offset"],
                "abs_d_minus_540": by_oq[4]["abs_d_minus_540"],
                "escapes": oq4_escapes,
            },
            "o_q=6": {
                "r": by_oq[6]["r"],
                "offset": by_oq[6]["offset"],
                "abs_d_minus_540": by_oq[6]["abs_d_minus_540"],
                "escapes": oq6_escapes,
            },
            "radius": NEAR_540_RADIUS,
            "center": NEAR_540_CENTER,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="RC6-RC8 residual chamber probe (o_q panel phase + near-540 exclusivity)."
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc3-table", type=Path, default=RC3_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc6_prediction_table.json",
    )
    args = parser.parse_args()

    if not args.prior_table.is_file():
        print(f"missing prior table: {args.prior_table}", file=sys.stderr)
        return 2
    if not args.summary_json.is_file():
        print(f"missing summary json: {args.summary_json}", file=sys.stderr)
        return 2

    prior = json.loads(args.prior_table.read_text(encoding="utf-8"))
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

    rc3_note = None
    if args.rc3_table.is_file():
        rc3 = json.loads(args.rc3_table.read_text(encoding="utf-8"))
        rc3_note = {
            "path": str(args.rc3_table),
            "conclusion": rc3.get("conclusion"),
        }

    primary_rows = [
        _annotate(row) for row in prior["prior_rows"] + [prior["new_row"]]
    ]
    oq_rows = [_annotate(row) for row in prior.get("oq_rows", [])]

    # Validate o_q panel matches summary branch maxima offsets.
    summary_by_oq = summary.get("max_row_by_o_q", {})
    for row in oq_rows:
        key = str(int(row["o_q"]))
        if key in summary_by_oq:
            expected = int(summary_by_oq[key]["offset"])
            if int(row["offset"]) != expected:
                print(
                    f"o_q panel offset mismatch for o_q={key}: "
                    f"table={row['offset']} summary={expected}",
                    file=sys.stderr,
                )
                return 3

    p10_results = [evaluate_p10(row) for row in oq_rows]
    p11_results = [evaluate_p11(row) for row in primary_rows + oq_rows]
    p12_result = evaluate_p12_panel(oq_rows)
    all_results = p10_results + p11_results + [p12_result]

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p10_holds = holds(p10_results)
    p11_holds = holds(p11_results)
    p12_holds = bool(p12_result["pass"])

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]

    residual_claims = [
        {
            "id": "RC6",
            "claim": (
                "On 4e8-5e8 per-o_q branch maxima (o_q in {2,4,6}), S2-A chamber "
                "phase order holds: 1 <= first_tau4 < first_tau3 = D(r), "
                "prefix_min_tau = 4, tau5_count = 0."
            ),
            "status": "holds" if p10_holds else "falsified",
            "linked_prediction": "P10",
            "evidence": oq_compact,
        },
        {
            "id": "RC7",
            "claim": (
                f"Late-dominant phase gap: (D(r) - first_tau4) / D(r) >= "
                f"{PHASE_GAP_MIN} on segment utilization maxima through "
                f"4e8-5e8 and on the full o_q branch-max panel."
            ),
            "status": "holds" if p11_holds else "falsified",
            "linked_prediction": "P11",
            "evidence": {
                "primary_rows": [
                    {
                        "segment": row["segment"],
                        "r": row["r"],
                        "offset": row["offset"],
                        "first_tau4_offset": row["first_tau4_offset"],
                        "phase_gap": row["phase_gap"],
                    }
                    for row in primary_rows
                ],
                "oq_panel": [
                    {
                        "segment": row["segment"],
                        "o_q": row["o_q"],
                        "r": row["r"],
                        "offset": row["offset"],
                        "first_tau4_offset": row["first_tau4_offset"],
                        "phase_gap": row["phase_gap"],
                    }
                    for row in oq_rows
                ],
                "bound": PHASE_GAP_MIN,
            },
        },
        {
            "id": "RC8",
            "claim": (
                "On 4e8-5e8 per-o_q branch maxima, near-540 is exclusive to "
                "the o_q=2 branch max (|D-540|<=20); o_q=4 and o_q=6 branch "
                "maxima escape. Strengthens RC5 from local attractor to "
                "panel exclusivity residual (not a universal law)."
            ),
            "status": "holds" if p12_holds else "falsified",
            "linked_prediction": "P12",
            "evidence": p12_result["detail"],
        },
        {
            "id": "RC2_retained",
            "claim": (
                "Fixed near-540 band D(r) in [528, 552] on segment utilization "
                "maxima is not a law."
            ),
            "status": "falsified",
            "linked_prediction": "P6 (prior)",
            "evidence": {
                "segment": "4e8-5e8",
                "r": 424171123,
                "offset": 738,
            },
        },
        {
            "id": "RC3_RC5_retained",
            "claim": (
                "Prior residual RC3-RC5 (tau4 density, absolute early tau4, "
                "o_q=2 local attractor) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P7-P9 (prior)",
            "evidence": rc3_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc3_prediction_table": str(args.rc3_table) if args.rc3_table.is_file() else None,
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "phase_gap_min": PHASE_GAP_MIN,
            "near_540_radius": NEAR_540_RADIUS,
            "required_o_q": sorted(REQUIRED_OQ),
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-Square Proximity proved in PROOF.md; residual audit only"
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC6_oq_panel_phase_order": "holds" if p10_holds else "falsified",
            "RC7_late_dominant_phase_gap": "holds" if p11_holds else "falsified",
            "RC8_oq_near_540_exclusivity": "holds" if p12_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC3_RC5": "retained holds (not primary surface)",
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC6-RC8: full o_q-panel S2-A phase "
                "order, late-dominant phase-gap bound, and o_q-stratified "
                "near-540 exclusivity; does not restate RC3-RC5 as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-10-rc6/"
            "offset_540_residual_rc6_probe.py"
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
