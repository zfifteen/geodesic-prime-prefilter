#!/usr/bin/env python3
"""Residual chamber claims RC42-RC44: interior Tau4 packing vs Dual markers.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual markers (first_tau4_offset, trail_gap) with late tau=3 at D
  - successive inter-hit gaps on the ordered Tau4 set
  - min, max, and median successive gaps
  - Dual L1 isolation dual_l1 = first_tau4 + trail_gap

Prior residual surface ended at RC39-RC41 (open/median, trail/median,
dual/median endpoint isolation). This probe does not restate those as the
primary deliverable. It states and checks the next residual claims on
segment utilization maxima through 4e8-5e8 and the full o_q branch-max panel:

  P46 / RC42: Floor packing of successive Tau4 gaps
              0.10 <= min_gap / median_gap <= 0.35
  P47 / RC43: Interior successive-gap dynamic range
              8 <= max_gap / min_gap <= 55
  P48 / RC44: Dual L1 relative to peak interior desert
              0.10 <= dual_l1 / max_gap <= 1.10

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
RC39-RC41 bound Dual endpoint isolation in median units. RC42-RC44 bound
interior packing floor, interior spacing dynamic range, and Dual scale
against the largest interior Tau4 desert. These are not Dual median
rescales and are not body/median (algebraically D/med - dual/med).

Recurring offset 540 is not a law for D(r) (RC2 remains falsified).
d=4 SDA is not revived.

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
RC39_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-14-rc39"
    / "offset_540_rc39_prediction_table.json"
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

MIN_OVER_MED_MIN = 0.10
MIN_OVER_MED_MAX = 0.35
MAX_OVER_MIN_MIN = 8.0
MAX_OVER_MIN_MAX = 55.0
DUAL_OVER_MAX_MIN = 0.10
DUAL_OVER_MAX_MAX = 1.10
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P46",
        "name": "successive_tau4_floor_over_median",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the floor packing ratio "
            "min_successive_gap / median_gap satisfies "
            f"{MIN_OVER_MED_MIN} <= min_gap / median_gap <= "
            f"{MIN_OVER_MED_MAX} (interior packing floor; not Dual "
            "endpoint isolation RC39-RC41; not max/median RC37)."
        ),
        "falsifier": (
            "any evaluated row with min_over_median < "
            f"{MIN_OVER_MED_MIN} or min_over_median > {MIN_OVER_MED_MAX}"
        ),
    },
    {
        "id": "P47",
        "name": "successive_tau4_dynamic_range",
        "statement": (
            "On the same surface, the interior successive-gap dynamic range "
            "max_successive_gap / min_successive_gap satisfies "
            f"{MAX_OVER_MIN_MIN} <= max_gap / min_gap <= {MAX_OVER_MIN_MAX} "
            "(body spacing range; independent of Dual median units)."
        ),
        "falsifier": (
            "any evaluated row with max_over_min < "
            f"{MAX_OVER_MIN_MIN} or max_over_min > {MAX_OVER_MIN_MAX}"
        ),
    },
    {
        "id": "P48",
        "name": "dual_l1_over_peak_interior_desert",
        "statement": (
            "On the same surface, Dual L1 relative to the peak interior "
            "Tau4 desert dual_l1 / max_successive_gap satisfies "
            f"{DUAL_OVER_MAX_MIN} <= dual_l1 / max_gap <= "
            f"{DUAL_OVER_MAX_MAX} (endpoint Dual vs largest body hole; "
            "not dual/median RC41)."
        ),
        "falsifier": (
            "any evaluated row with dual_over_max_gap < "
            f"{DUAL_OVER_MAX_MIN} or dual_over_max_gap > {DUAL_OVER_MAX_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers and interior packing residual ratios.

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
        "min_over_median": None,
        "max_over_min": None,
        "dual_over_max_gap": None,
        "open_over_median": None,
        "trail_over_median": None,
        "dual_over_median": None,
        "tau4_density": 0.0 if d > 1 else None,
        "prefix_min_tau": prefix_min_tau,
        "tau3_in_prefix": tau3_in_prefix,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        "domain_ok": False,
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
    domain_ok = median_gap > 0 and min_gap > 0 and max_gap > 0
    min_over_median = (min_gap / median_gap) if domain_ok else None
    max_over_min = (max_gap / min_gap) if domain_ok else None
    dual_over_max_gap = (dual_l1 / max_gap) if domain_ok else None
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
        "min_over_median": min_over_median,
        "max_over_min": max_over_min,
        "dual_over_max_gap": dual_over_max_gap,
        "open_over_median": open_over_median,
        "trail_over_median": trail_over_median,
        "dual_over_median": dual_over_median,
        "tau4_density": tau4_density,
        "prefix_min_tau": prefix_min_tau,
        "tau3_in_prefix": tau3_in_prefix,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        "domain_ok": domain_ok,
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
        "min_over_median": row["min_over_median"],
        "max_over_min": row["max_over_min"],
        "dual_over_max_gap": row["dual_over_max_gap"],
        "open_over_median": row["open_over_median"],
        "trail_over_median": row["trail_over_median"],
        "dual_over_median": row["dual_over_median"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
        "domain_ok": row["domain_ok"],
    }


def evaluate_p46(row: dict) -> dict:
    ratio = row["min_over_median"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P46",
            "name": "successive_tau4_floor_over_median",
            "statement": PREDICTIONS[0]["statement"],
            "falsifier": PREDICTIONS[0]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive gaps",
                "min_over_median": ratio,
            },
        }
    passed = float(ratio) >= MIN_OVER_MED_MIN and float(ratio) <= MIN_OVER_MED_MAX
    return {
        "id": "P46",
        "name": "successive_tau4_floor_over_median",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "min_over_median": ratio,
            "bound_min": MIN_OVER_MED_MIN,
            "bound_max": MIN_OVER_MED_MAX,
            "min_successive_gap": row["min_successive_gap"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p47(row: dict) -> dict:
    ratio = row["max_over_min"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P47",
            "name": "successive_tau4_dynamic_range",
            "statement": PREDICTIONS[1]["statement"],
            "falsifier": PREDICTIONS[1]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive gaps",
                "max_over_min": ratio,
            },
        }
    passed = float(ratio) >= MAX_OVER_MIN_MIN and float(ratio) <= MAX_OVER_MIN_MAX
    return {
        "id": "P47",
        "name": "successive_tau4_dynamic_range",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "max_over_min": ratio,
            "bound_min": MAX_OVER_MIN_MIN,
            "bound_max": MAX_OVER_MIN_MAX,
            "max_successive_gap": row["max_successive_gap"],
            "min_successive_gap": row["min_successive_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p48(row: dict) -> dict:
    ratio = row["dual_over_max_gap"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P48",
            "name": "dual_l1_over_peak_interior_desert",
            "statement": PREDICTIONS[2]["statement"],
            "falsifier": PREDICTIONS[2]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive gaps",
                "dual_over_max_gap": ratio,
            },
        }
    passed = float(ratio) >= DUAL_OVER_MAX_MIN and float(ratio) <= DUAL_OVER_MAX_MAX
    return {
        "id": "P48",
        "name": "dual_l1_over_peak_interior_desert",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_over_max_gap": ratio,
            "bound_min": DUAL_OVER_MAX_MIN,
            "bound_max": DUAL_OVER_MAX_MAX,
            "dual_l1": row["dual_l1"],
            "max_successive_gap": row["max_successive_gap"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC42-RC44 residual chamber probe "
            "(min/median floor, max/min range, dual/max_gap)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc39-table", type=Path, default=RC39_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc42_prediction_table.json",
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

    rc39_note = None
    if args.rc39_table.is_file():
        rc39 = json.loads(args.rc39_table.read_text(encoding="utf-8"))
        rc39_note = {
            "path": str(args.rc39_table),
            "conclusion": {
                k: rc39.get("conclusion", {}).get(k)
                for k in (
                    "RC39_opening_isolation_median_units",
                    "RC40_trail_closing_isolation_median_units",
                    "RC41_dual_l1_isolation_median_units",
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
        "recomputing min/median, max/min, dual/max_gap "
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

    p46_results = [evaluate_p46(row) for row in evaluated]
    p47_results = [evaluate_p47(row) for row in evaluated]
    p48_results = [evaluate_p48(row) for row in evaluated]
    all_results = p46_results + p47_results + p48_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p46_holds = holds(p46_results)
    p47_holds = holds(p47_results)
    p48_holds = holds(p48_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    # Unique-chamber ranges (dedupe duplicate r=424171123 primary/oq).
    unique_by_r: dict[int, dict] = {}
    for row in evaluated:
        unique_by_r[int(row["r"])] = row
    unique_rows = list(unique_by_r.values())

    min_over_meds = [
        float(r["min_over_median"])
        for r in unique_rows
        if r["min_over_median"] is not None
    ]
    max_over_mins = [
        float(r["max_over_min"])
        for r in unique_rows
        if r["max_over_min"] is not None
    ]
    dual_over_maxs = [
        float(r["dual_over_max_gap"])
        for r in unique_rows
        if r["dual_over_max_gap"] is not None
    ]

    residual_claims = [
        {
            "id": "RC42",
            "claim": (
                "Floor packing of successive Tau4 gaps: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{MIN_OVER_MED_MIN} <= min_successive_gap / median_gap <= "
                f"{MIN_OVER_MED_MAX}."
            ),
            "status": "holds" if p46_holds else "falsified",
            "linked_prediction": "P46",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": MIN_OVER_MED_MIN,
                "bound_max": MIN_OVER_MED_MAX,
                "min_observed": min(min_over_meds) if min_over_meds else None,
                "max_observed": max(min_over_meds) if min_over_meds else None,
            },
        },
        {
            "id": "RC43",
            "claim": (
                "Interior successive-gap dynamic range: "
                f"{MAX_OVER_MIN_MIN} <= max_successive_gap / min_successive_gap "
                f"<= {MAX_OVER_MIN_MAX} on util maxima + o_q panel "
                "(body spacing range; independent of Dual median units)."
            ),
            "status": "holds" if p47_holds else "falsified",
            "linked_prediction": "P47",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": MAX_OVER_MIN_MIN,
                "bound_max": MAX_OVER_MIN_MAX,
                "min_observed": min(max_over_mins) if max_over_mins else None,
                "max_observed": max(max_over_mins) if max_over_mins else None,
            },
        },
        {
            "id": "RC44",
            "claim": (
                "Dual L1 relative to peak interior Tau4 desert: "
                f"{DUAL_OVER_MAX_MIN} <= dual_l1 / max_successive_gap <= "
                f"{DUAL_OVER_MAX_MAX} on util maxima + o_q panel "
                "(endpoint Dual vs largest body hole; not dual/median)."
            ),
            "status": "holds" if p48_holds else "falsified",
            "linked_prediction": "P48",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": DUAL_OVER_MAX_MIN,
                "bound_max": DUAL_OVER_MAX_MAX,
                "min_observed": min(dual_over_maxs) if dual_over_maxs else None,
                "max_observed": max(dual_over_maxs) if dual_over_maxs else None,
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
            "id": "RC39_RC41_retained",
            "claim": (
                "Prior residual RC39-RC41 (open/median, trail/median, "
                "dual/median) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P43-P45 (prior)",
            "evidence": rc39_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc39_prediction_table": (
                str(args.rc39_table) if args.rc39_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "min_over_median_min": MIN_OVER_MED_MIN,
            "min_over_median_max": MIN_OVER_MED_MAX,
            "max_over_min_min": MAX_OVER_MIN_MIN,
            "max_over_min_max": MAX_OVER_MIN_MAX,
            "dual_over_max_gap_min": DUAL_OVER_MAX_MIN,
            "dual_over_max_gap_max": DUAL_OVER_MAX_MAX,
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
            "RC42_successive_floor_over_median": (
                "holds" if p46_holds else "falsified"
            ),
            "RC43_successive_dynamic_range": (
                "holds" if p47_holds else "falsified"
            ),
            "RC44_dual_over_peak_interior_desert": (
                "holds" if p48_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC39_RC41": "retained holds (not primary surface)",
            "min_over_median_range": (
                [min(min_over_meds), max(min_over_meds)]
                if min_over_meds
                else None
            ),
            "max_over_min_range": (
                [min(max_over_mins), max(max_over_mins)]
                if max_over_mins
                else None
            ),
            "dual_over_max_gap_range": (
                [min(dual_over_maxs), max(dual_over_maxs)]
                if dual_over_maxs
                else None
            ),
            "unique_chamber_count": len(unique_rows),
            "surface_row_count": len(evaluated),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC42-RC44: interior Tau4 packing "
                "floor (min/median), successive-gap dynamic range (max/min), "
                "and Dual L1 vs peak interior desert (dual/max_gap); does not "
                "restate RC39-RC41 open/trail/dual median isolation as sole "
                "deliverable; does not use body/median (D/med - dual/med)."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-14-rc42/"
            "offset_540_residual_rc42_probe.py"
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
