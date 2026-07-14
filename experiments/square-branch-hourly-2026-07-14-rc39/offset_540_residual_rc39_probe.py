#!/usr/bin/env python3
"""Residual chamber claims RC39-RC41: Dual isolation in median-gap units.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual markers (first_tau4_offset, trail_gap) with late tau=3 at D
  - successive inter-hit gaps on the ordered Tau4 set
  - median successive gap (central scale of Tau4 spacing)
  - opening isolation first_tau4 / median_gap
  - trail closing isolation trail_gap / median_gap
  - Dual L1 isolation dual_l1 / median_gap

Prior residual surface ended at RC36-RC38 (open/mean, max/med, IQR/mean).
This probe does not restate those as the primary deliverable. It states and
checks the next residual claims on segment utilization maxima through
4e8-5e8 and the full o_q branch-max panel:

  P43 / RC39: Opening isolation in median-gap units
              0.20 <= first_tau4 / median_gap <= 2.50
  P44 / RC40: Trail closing isolation in median-gap units
              0.20 <= trail_gap / median_gap <= 3.50
  P45 / RC41: Dual L1 isolation in median-gap units
              0.40 <= dual_l1 / median_gap <= 4.50

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
The opening run, the trail run, and their Dual sum each stay a bounded
number of median successive Tau4 gaps (median-relative Dual isolation,
not mean-relative RC36/RC34/RC29). Recurring offset 540 is not a law for
D(r) (RC2 remains falsified). d=4 SDA is not revived.

Audit-only. Does not choose primes as PGS inference.
Prime-square proximity remains an unresolved obligation in PROOF.md;
residual audit only.
"""

from __future__ import annotations

import argparse
import json
import statistics
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
RC36_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-13-rc36"
    / "offset_540_rc36_prediction_table.json"
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

OPEN_OVER_MED_MIN = 0.20
OPEN_OVER_MED_MAX = 2.50
TRAIL_OVER_MED_MIN = 0.20
TRAIL_OVER_MED_MAX = 3.50
DUAL_OVER_MED_MIN = 0.40
DUAL_OVER_MED_MAX = 4.50
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P43",
        "name": "opening_isolation_in_median_gap_units",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the opening isolation "
            "first_tau4 / median_gap satisfies "
            f"{OPEN_OVER_MED_MIN} <= first_tau4 / median_gap <= "
            f"{OPEN_OVER_MED_MAX} (opening component only; median scale, "
            "not open/mean)."
        ),
        "falsifier": (
            "any evaluated row with open_over_median < "
            f"{OPEN_OVER_MED_MIN} or open_over_median > {OPEN_OVER_MED_MAX}"
        ),
    },
    {
        "id": "P44",
        "name": "trail_closing_isolation_in_median_gap_units",
        "statement": (
            "On the same surface, the trail closing isolation "
            "trail_gap / median_gap satisfies "
            f"{TRAIL_OVER_MED_MIN} <= trail_gap / median_gap <= "
            f"{TRAIL_OVER_MED_MAX} (closing component only; median scale, "
            "not trail/mean)."
        ),
        "falsifier": (
            "any evaluated row with trail_over_median < "
            f"{TRAIL_OVER_MED_MIN} or trail_over_median > {TRAIL_OVER_MED_MAX}"
        ),
    },
    {
        "id": "P45",
        "name": "dual_l1_isolation_in_median_gap_units",
        "statement": (
            "On the same surface, the Dual L1 isolation "
            "dual_l1 / median_gap satisfies "
            f"{DUAL_OVER_MED_MIN} <= dual_l1 / median_gap <= "
            f"{DUAL_OVER_MED_MAX} (combined open+trail isolation; median "
            "scale, not dual/mean)."
        ),
        "falsifier": (
            "any evaluated row with dual_over_median < "
            f"{DUAL_OVER_MED_MIN} or dual_over_median > {DUAL_OVER_MED_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers and median-scaled isolation ratios.

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
    empty = {
        "tau4_count": 0,
        "first_tau4_offset": None,
        "last_tau4_offset": None,
        "first_tau3_offset": d,
        "trail_gap": None,
        "dual_l1": None,
        "tau4_body": None,
        "mean_gap": None,
        "successive_gaps": [],
        "min_successive_gap": None,
        "max_successive_gap": None,
        "median_gap": None,
        "open_over_median": None,
        "trail_over_median": None,
        "dual_over_median": None,
        "tau4_density": 0.0 if d > 1 else None,
        "prefix_min_tau": prefix_min_tau,
        "tau3_in_prefix": tau3_in_prefix,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
    }
    if len(tau4_offs) < 2:
        return empty

    first_tau4 = tau4_offs[0]
    last_tau4 = tau4_offs[-1]
    trail_gap = d - last_tau4
    dual_l1 = first_tau4 + trail_gap
    tau4_body = last_tau4 - first_tau4
    successive = [tau4_offs[i + 1] - tau4_offs[i] for i in range(len(tau4_offs) - 1)]
    mean_gap = tau4_body / (len(tau4_offs) - 1)
    max_gap = max(successive)
    min_gap = min(successive)
    median_gap = float(statistics.median(successive))
    open_over_median = first_tau4 / median_gap if median_gap > 0 else None
    trail_over_median = trail_gap / median_gap if median_gap > 0 else None
    dual_over_median = dual_l1 / median_gap if median_gap > 0 else None
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
        "successive_gaps": successive,
        "min_successive_gap": min_gap,
        "max_successive_gap": max_gap,
        "median_gap": median_gap,
        "open_over_median": open_over_median,
        "trail_over_median": trail_over_median,
        "dual_over_median": dual_over_median,
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
        "min_successive_gap": row["min_successive_gap"],
        "max_successive_gap": row["max_successive_gap"],
        "median_gap": row["median_gap"],
        "open_over_median": row["open_over_median"],
        "trail_over_median": row["trail_over_median"],
        "dual_over_median": row["dual_over_median"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p43(row: dict) -> dict:
    ratio = row["open_over_median"]
    passed = (
        ratio is not None
        and float(ratio) >= OPEN_OVER_MED_MIN
        and float(ratio) <= OPEN_OVER_MED_MAX
    )
    return {
        "id": "P43",
        "name": "opening_isolation_in_median_gap_units",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "open_over_median": ratio,
            "bound_min": OPEN_OVER_MED_MIN,
            "bound_max": OPEN_OVER_MED_MAX,
            "first_tau4_offset": row["first_tau4_offset"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p44(row: dict) -> dict:
    ratio = row["trail_over_median"]
    passed = (
        ratio is not None
        and float(ratio) >= TRAIL_OVER_MED_MIN
        and float(ratio) <= TRAIL_OVER_MED_MAX
    )
    return {
        "id": "P44",
        "name": "trail_closing_isolation_in_median_gap_units",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "trail_over_median": ratio,
            "bound_min": TRAIL_OVER_MED_MIN,
            "bound_max": TRAIL_OVER_MED_MAX,
            "trail_gap": row["trail_gap"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p45(row: dict) -> dict:
    ratio = row["dual_over_median"]
    passed = (
        ratio is not None
        and float(ratio) >= DUAL_OVER_MED_MIN
        and float(ratio) <= DUAL_OVER_MED_MAX
    )
    return {
        "id": "P45",
        "name": "dual_l1_isolation_in_median_gap_units",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_over_median": ratio,
            "bound_min": DUAL_OVER_MED_MIN,
            "bound_max": DUAL_OVER_MED_MAX,
            "dual_l1": row["dual_l1"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC39-RC41 residual chamber probe "
            "(open/median, trail/median, dual/median isolation)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc36-table", type=Path, default=RC36_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc39_prediction_table.json",
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

    rc36_note = None
    if args.rc36_table.is_file():
        rc36 = json.loads(args.rc36_table.read_text(encoding="utf-8"))
        rc36_note = {
            "path": str(args.rc36_table),
            "conclusion": {
                k: rc36.get("conclusion", {}).get(k)
                for k in (
                    "RC36_opening_isolation_mean_units",
                    "RC37_peak_successive_gap_over_median",
                    "RC38_iqr_scaled_by_mean",
                    "RC2_fixed_band",
                )
            },
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
        "recomputing open/median, trail/median, dual/median "
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

    p43_results = [evaluate_p43(row) for row in evaluated]
    p44_results = [evaluate_p44(row) for row in evaluated]
    p45_results = [evaluate_p45(row) for row in evaluated]
    all_results = p43_results + p44_results + p45_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p43_holds = holds(p43_results)
    p44_holds = holds(p44_results)
    p45_holds = holds(p45_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    open_over_meds = [
        float(r["open_over_median"])
        for r in evaluated
        if r["open_over_median"] is not None
    ]
    trail_over_meds = [
        float(r["trail_over_median"])
        for r in evaluated
        if r["trail_over_median"] is not None
    ]
    dual_over_meds = [
        float(r["dual_over_median"])
        for r in evaluated
        if r["dual_over_median"] is not None
    ]

    residual_claims = [
        {
            "id": "RC39",
            "claim": (
                "Opening isolation in median-gap units: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{OPEN_OVER_MED_MIN} <= first_tau4 / median_gap <= "
                f"{OPEN_OVER_MED_MAX}."
            ),
            "status": "holds" if p43_holds else "falsified",
            "linked_prediction": "P43",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": OPEN_OVER_MED_MIN,
                "bound_max": OPEN_OVER_MED_MAX,
                "min_observed": min(open_over_meds) if open_over_meds else None,
                "max_observed": max(open_over_meds) if open_over_meds else None,
            },
        },
        {
            "id": "RC40",
            "claim": (
                "Trail closing isolation in median-gap units: "
                f"{TRAIL_OVER_MED_MIN} <= trail_gap / median_gap <= "
                f"{TRAIL_OVER_MED_MAX} on util maxima + o_q panel "
                "(closing component; median scale, not trail/mean)."
            ),
            "status": "holds" if p44_holds else "falsified",
            "linked_prediction": "P44",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": TRAIL_OVER_MED_MIN,
                "bound_max": TRAIL_OVER_MED_MAX,
                "min_observed": min(trail_over_meds) if trail_over_meds else None,
                "max_observed": max(trail_over_meds) if trail_over_meds else None,
            },
        },
        {
            "id": "RC41",
            "claim": (
                "Dual L1 isolation in median-gap units: "
                f"{DUAL_OVER_MED_MIN} <= dual_l1 / median_gap <= "
                f"{DUAL_OVER_MED_MAX} on util maxima + o_q panel "
                "(combined open+trail; median scale, not dual/mean)."
            ),
            "status": "holds" if p45_holds else "falsified",
            "linked_prediction": "P45",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": DUAL_OVER_MED_MIN,
                "bound_max": DUAL_OVER_MED_MAX,
                "min_observed": min(dual_over_meds) if dual_over_meds else None,
                "max_observed": max(dual_over_meds) if dual_over_meds else None,
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
            "id": "RC36_RC38_retained",
            "claim": (
                "Prior residual RC36-RC38 (open/mean, max/med, IQR/mean) "
                "retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P40-P42 (prior)",
            "evidence": rc36_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc36_prediction_table": (
                str(args.rc36_table) if args.rc36_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "open_over_median_min": OPEN_OVER_MED_MIN,
            "open_over_median_max": OPEN_OVER_MED_MAX,
            "trail_over_median_min": TRAIL_OVER_MED_MIN,
            "trail_over_median_max": TRAIL_OVER_MED_MAX,
            "dual_over_median_min": DUAL_OVER_MED_MIN,
            "dual_over_median_max": DUAL_OVER_MED_MAX,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-square proximity remains unresolved in PROOF.md "
                "section Square-Branch Reduction; residual audit only. "
                "Direct next-prime and Interior Maximizer remain proved."
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC39_opening_isolation_median_units": (
                "holds" if p43_holds else "falsified"
            ),
            "RC40_trail_closing_isolation_median_units": (
                "holds" if p44_holds else "falsified"
            ),
            "RC41_dual_l1_isolation_median_units": (
                "holds" if p45_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC36_RC38": "retained holds (not primary surface)",
            "open_over_median_range": (
                [min(open_over_meds), max(open_over_meds)]
                if open_over_meds
                else None
            ),
            "trail_over_median_range": (
                [min(trail_over_meds), max(trail_over_meds)]
                if trail_over_meds
                else None
            ),
            "dual_over_median_range": (
                [min(dual_over_meds), max(dual_over_meds)]
                if dual_over_meds
                else None
            ),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC39-RC41: Dual isolation in "
                "median-gap units (open/median, trail/median, dual/median); "
                "does not restate RC36-RC38 open/mean, max/med, or IQR/mean "
                "as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-14-rc39/"
            "offset_540_residual_rc39_probe.py"
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
