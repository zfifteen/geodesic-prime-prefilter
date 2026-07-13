#!/usr/bin/env python3
"""Residual chamber claims RC24-RC26: mean tau4 gap, Dual signed imbalance, open frac.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual(r) = (first_tau4_offset, trail_gap) with
    trail_gap = D(r) - last_tau4_offset
  - late-tau3 landing at first_tau3_offset = D(r)
  - mean inter-hit gap on Tau4 body
  - Dual signed imbalance (trail - first) / Dual L1
  - chamber open fraction (D - first_tau4) / D

Prior residual surface ended at RC21-RC23 (tau4 density envelope, Dual
max-component share, near-540 Dual L1 floor). This probe does not restate
those as the primary deliverable. It states and checks the next residual
claims on segment utilization maxima through 4e8-5e8 and the full o_q
branch-max panel:

  P28 / RC24: Tau4 mean inter-hit gap envelope
              7.0 <= (last_tau4 - first_tau4) / (tau4_count - 1) <= 10.0
  P29 / RC25: Dual signed imbalance envelope
              -0.55 <= (trail_gap - first_tau4) / Dual L1 <= 0.70
  P30 / RC26: Chamber open fraction
              (D - first_tau4) / D >= 0.96

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
Between the Dual markers the Tau4 body has stable mean spacing, Dual
asymmetry is bounded in both directions, and the open length from first
tau4 to the late tau3 endpoint covers almost all of D. Recurring offset
540 is not a law for D(r) (RC2 remains falsified). d=4 SDA is not revived.

Audit-only. Does not choose primes as PGS inference.
Prime-square proximity remains an unresolved obligation in PROOF.md;
residual audit only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
if str(FIELD_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_DIR))

from z_band_prime_composite_field import divisor_counts_segment

PRIOR_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10"
    / "offset_540_prediction_table.json"
)
RC21_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-13-rc21"
    / "offset_540_rc21_prediction_table.json"
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

MEAN_GAP_MIN = 7.0
MEAN_GAP_MAX = 10.0
SIGNED_IMBALANCE_MIN = -0.55
SIGNED_IMBALANCE_MAX = 0.70
OPEN_FRAC_MIN = 0.96
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P28",
        "name": "tau4_mean_inter_hit_gap_envelope",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, Tau4 mean inter-hit gap "
            "(last_tau4 - first_tau4) / (tau4_count - 1) lies in "
            f"[{MEAN_GAP_MIN}, {MEAN_GAP_MAX}]."
        ),
        "falsifier": (
            "any evaluated row with mean_gap < "
            f"{MEAN_GAP_MIN} or mean_gap > {MEAN_GAP_MAX}"
        ),
    },
    {
        "id": "P29",
        "name": "dual_signed_imbalance_envelope",
        "statement": (
            "On the same surface, Dual signed imbalance "
            "(trail_gap - first_tau4_offset) / Dual L1 satisfies "
            f"{SIGNED_IMBALANCE_MIN} <= signed <= {SIGNED_IMBALANCE_MAX} "
            "(early/late Dual asymmetry is two-sided bounded)."
        ),
        "falsifier": (
            "any evaluated row with dual_signed_imbalance < "
            f"{SIGNED_IMBALANCE_MIN} or dual_signed_imbalance > "
            f"{SIGNED_IMBALANCE_MAX}"
        ),
    },
    {
        "id": "P30",
        "name": "chamber_open_fraction",
        "statement": (
            "On the same surface, chamber open fraction "
            "(D(r) - first_tau4_offset) / D(r) satisfies "
            f"open_frac >= {OPEN_FRAC_MIN} "
            "(early tau4 opens before the late tau3 endpoint covers almost "
            "all of the chamber length)."
        ),
        "falsifier": (
            f"any evaluated row with open_frac < {OPEN_FRAC_MIN}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, mean gap, signed imbalance, open frac.

    Offsets are 1-based from p: offset k labels n = p + k.
    The selected square sits at offset D and is not in the prefix.
    first_tau3_offset is defined as D under the square-branch residual
    (no tau<=3 in the prefix; late landing at the selected square).
    """
    d = int(offset)
    prefix = prefix_tau_values(p, square)
    if len(prefix) != d - 1:
        raise ValueError(
            f"prefix length mismatch: got {len(prefix)}, expected D-1={d - 1}"
        )
    tau4_offs = [i + 1 for i, value in enumerate(prefix) if value == 4]
    tau3_in_prefix = sum(1 for value in prefix if value == 3)
    prefix_min_tau = min(prefix) if prefix else None
    if not tau4_offs:
        return {
            "tau4_count": 0,
            "first_tau4_offset": None,
            "last_tau4_offset": None,
            "first_tau3_offset": d,
            "trail_gap": None,
            "dual_l1": None,
            "tau4_body": None,
            "mean_gap": None,
            "dual_signed_imbalance": None,
            "open_frac": None,
            "tau4_density": 0.0 if d > 1 else None,
            "prefix_min_tau": prefix_min_tau,
            "tau3_in_prefix": tau3_in_prefix,
            "abs_d_minus_540": abs(d - NEAR_540_CENTER),
            "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        }

    first_tau4 = tau4_offs[0]
    last_tau4 = tau4_offs[-1]
    trail_gap = d - last_tau4
    dual_l1 = first_tau4 + trail_gap
    tau4_body = last_tau4 - first_tau4
    mean_gap = (
        tau4_body / (len(tau4_offs) - 1) if len(tau4_offs) > 1 else None
    )
    dual_signed = (
        (trail_gap - first_tau4) / dual_l1 if dual_l1 > 0 else None
    )
    open_frac = (d - first_tau4) / d if d > 0 else None
    tau4_density = len(tau4_offs) / (d - 1) if d > 1 else None
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": first_tau4,
        "last_tau4_offset": last_tau4,
        "first_tau3_offset": d,
        "trail_gap": trail_gap,
        "dual_l1": dual_l1,
        "tau4_body": tau4_body,
        "mean_gap": mean_gap,
        "dual_signed_imbalance": dual_signed,
        "open_frac": open_frac,
        "tau4_density": tau4_density,
        "prefix_min_tau": prefix_min_tau,
        "tau3_in_prefix": tau3_in_prefix,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
    }


def enrich_row(row: dict) -> dict:
    out = dict(row)
    structure = early_late_structure(
        int(row["p"]), int(row["square"]), int(row["offset"])
    )
    out.update(structure)
    if "first_tau4_offset" in row and structure["first_tau4_offset"] is not None:
        if int(row["first_tau4_offset"]) != int(structure["first_tau4_offset"]):
            raise ValueError(
                f"first_tau4 mismatch r={row['r']}: "
                f"table={row['first_tau4_offset']} "
                f"recomputed={structure['first_tau4_offset']}"
            )
    if "prefix" in row:
        if int(row["prefix"]["tau4_count"]) != int(structure["tau4_count"]):
            raise ValueError(
                f"tau4_count mismatch r={row['r']}: "
                f"table={row['prefix']['tau4_count']} "
                f"recomputed={structure['tau4_count']}"
            )
        if int(row["prefix"]["prefix_min_tau"]) != int(structure["prefix_min_tau"]):
            raise ValueError(
                f"prefix_min_tau mismatch r={row['r']}: "
                f"table={row['prefix']['prefix_min_tau']} "
                f"recomputed={structure['prefix_min_tau']}"
            )
    return out


def _compact(row: dict) -> dict:
    return {
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "tau4_count": row["tau4_count"],
        "first_tau4_offset": row["first_tau4_offset"],
        "last_tau4_offset": row["last_tau4_offset"],
        "first_tau3_offset": row["first_tau3_offset"],
        "trail_gap": row["trail_gap"],
        "dual_l1": row["dual_l1"],
        "tau4_body": row["tau4_body"],
        "mean_gap": row["mean_gap"],
        "dual_signed_imbalance": row["dual_signed_imbalance"],
        "open_frac": row["open_frac"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p28(row: dict) -> dict:
    mean_gap = row["mean_gap"]
    passed = (
        mean_gap is not None
        and float(mean_gap) >= MEAN_GAP_MIN
        and float(mean_gap) <= MEAN_GAP_MAX
    )
    return {
        "id": "P28",
        "name": "tau4_mean_inter_hit_gap_envelope",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "mean_gap": mean_gap,
            "bound_min": MEAN_GAP_MIN,
            "bound_max": MEAN_GAP_MAX,
            "tau4_body": row["tau4_body"],
            "tau4_count": row["tau4_count"],
            "D": row["offset"],
        },
    }


def evaluate_p29(row: dict) -> dict:
    signed = row["dual_signed_imbalance"]
    passed = (
        signed is not None
        and float(signed) >= SIGNED_IMBALANCE_MIN
        and float(signed) <= SIGNED_IMBALANCE_MAX
    )
    return {
        "id": "P29",
        "name": "dual_signed_imbalance_envelope",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_signed_imbalance": signed,
            "bound_min": SIGNED_IMBALANCE_MIN,
            "bound_max": SIGNED_IMBALANCE_MAX,
            "first_tau4_offset": row["first_tau4_offset"],
            "trail_gap": row["trail_gap"],
            "dual_l1": row["dual_l1"],
            "D": row["offset"],
        },
    }


def evaluate_p30(row: dict) -> dict:
    open_frac = row["open_frac"]
    passed = open_frac is not None and float(open_frac) >= OPEN_FRAC_MIN
    return {
        "id": "P30",
        "name": "chamber_open_fraction",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "open_frac": open_frac,
            "bound_min": OPEN_FRAC_MIN,
            "first_tau4_offset": row["first_tau4_offset"],
            "first_tau3_offset": row["first_tau3_offset"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC24-RC26 residual chamber probe "
            "(mean tau4 gap, Dual signed imbalance, chamber open fraction)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc21-table", type=Path, default=RC21_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc24_prediction_table.json",
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

    rc21_note = None
    if args.rc21_table.is_file():
        rc21 = json.loads(args.rc21_table.read_text(encoding="utf-8"))
        rc21_note = {
            "path": str(args.rc21_table),
            "conclusion": rc21.get("conclusion"),
        }

    primary_src = prior["prior_rows"] + [prior["new_row"]]
    oq_src = prior.get("oq_rows", [])

    summary_by_oq = summary.get("max_row_by_o_q", {})
    for row in oq_src:
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

    print(
        "recomputing mean gap / Dual signed imbalance / open fraction "
        "on primary + o_q panel...",
        flush=True,
    )
    primary_rows = [enrich_row(row) for row in primary_src]
    oq_rows = [enrich_row(row) for row in oq_src]
    evaluated = primary_rows + oq_rows

    for row in evaluated:
        if int(row["tau3_in_prefix"]) != 0:
            print(
                f"unexpected tau=3 in prefix for r={row['r']}",
                file=sys.stderr,
            )
            return 4
        if int(row["prefix_min_tau"]) != 4:
            print(
                f"unexpected prefix_min_tau for r={row['r']}: "
                f"{row['prefix_min_tau']}",
                file=sys.stderr,
            )
            return 4

    p28_results = [evaluate_p28(row) for row in evaluated]
    p29_results = [evaluate_p29(row) for row in evaluated]
    p30_results = [evaluate_p30(row) for row in evaluated]
    all_results = p28_results + p29_results + p30_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p28_holds = holds(p28_results)
    p29_holds = holds(p29_results)
    p30_holds = holds(p30_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    mean_gaps = [
        float(r["mean_gap"]) for r in evaluated if r["mean_gap"] is not None
    ]
    signed_vals = [
        float(r["dual_signed_imbalance"])
        for r in evaluated
        if r["dual_signed_imbalance"] is not None
    ]
    open_fracs = [
        float(r["open_frac"]) for r in evaluated if r["open_frac"] is not None
    ]

    residual_claims = [
        {
            "id": "RC24",
            "claim": (
                "Tau4 mean inter-hit gap envelope: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{MEAN_GAP_MIN} <= (last_tau4 - first_tau4) / "
                f"(tau4_count - 1) <= {MEAN_GAP_MAX}."
            ),
            "status": "holds" if p28_holds else "falsified",
            "linked_prediction": "P28",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": MEAN_GAP_MIN,
                "bound_max": MEAN_GAP_MAX,
                "min_observed": min(mean_gaps) if mean_gaps else None,
                "max_observed": max(mean_gaps) if mean_gaps else None,
            },
        },
        {
            "id": "RC25",
            "claim": (
                "Dual signed imbalance envelope: "
                f"{SIGNED_IMBALANCE_MIN} <= "
                "(trail_gap - first_tau4) / Dual L1 <= "
                f"{SIGNED_IMBALANCE_MAX} on util maxima + o_q panel."
            ),
            "status": "holds" if p29_holds else "falsified",
            "linked_prediction": "P29",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": SIGNED_IMBALANCE_MIN,
                "bound_max": SIGNED_IMBALANCE_MAX,
                "min_observed": min(signed_vals) if signed_vals else None,
                "max_observed": max(signed_vals) if signed_vals else None,
            },
        },
        {
            "id": "RC26",
            "claim": (
                "Chamber open fraction: "
                f"(D - first_tau4) / D >= {OPEN_FRAC_MIN} "
                "on util maxima + o_q panel "
                "(early tau4 to late tau3 separation covers almost all of D)."
            ),
            "status": "holds" if p30_holds else "falsified",
            "linked_prediction": "P30",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": OPEN_FRAC_MIN,
                "min_observed": min(open_fracs) if open_fracs else None,
                "max_observed": max(open_fracs) if open_fracs else None,
            },
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
            "id": "RC21_RC23_retained",
            "claim": (
                "Prior residual RC21-RC23 (tau4 density envelope, Dual "
                "max-component share, near-540 Dual L1 floor) retained as "
                "measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P25-P27 (prior)",
            "evidence": rc21_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc21_prediction_table": (
                str(args.rc21_table) if args.rc21_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "mean_gap_min": MEAN_GAP_MIN,
            "mean_gap_max": MEAN_GAP_MAX,
            "signed_imbalance_min": SIGNED_IMBALANCE_MIN,
            "signed_imbalance_max": SIGNED_IMBALANCE_MAX,
            "open_frac_min": OPEN_FRAC_MIN,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-square proximity remains unresolved in PROOF.md; "
                "residual audit only"
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC24_tau4_mean_inter_hit_gap": (
                "holds" if p28_holds else "falsified"
            ),
            "RC25_dual_signed_imbalance": (
                "holds" if p29_holds else "falsified"
            ),
            "RC26_chamber_open_fraction": (
                "holds" if p30_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC21_RC23": "retained holds (not primary surface)",
            "mean_gap_range": (
                [min(mean_gaps), max(mean_gaps)] if mean_gaps else None
            ),
            "dual_signed_imbalance_range": (
                [min(signed_vals), max(signed_vals)] if signed_vals else None
            ),
            "open_frac_range": (
                [min(open_fracs), max(open_fracs)] if open_fracs else None
            ),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC24-RC26: Tau4 mean inter-hit gap "
                "envelope, Dual signed imbalance (two-sided early/late "
                "asymmetry), and chamber open fraction "
                "(early tau4 to late tau3 separation); does not restate "
                "RC21-RC23 density/share/near-540 Dual L1 floor as sole "
                "deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-13-rc24/"
            "offset_540_residual_rc24_probe.py"
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
