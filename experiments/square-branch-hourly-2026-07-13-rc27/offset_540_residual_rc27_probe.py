#!/usr/bin/env python3
"""Residual chamber claims RC27-RC29: gap regularity + Dual isolation in mean units.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual(r) = (first_tau4_offset, trail_gap) with
    trail_gap = D(r) - last_tau4_offset
  - successive inter-hit gaps on the ordered Tau4 set
  - mean inter-hit gap on Tau4 body
  - max successive gap / mean_gap (spacing regularity peak)
  - coefficient of variation of successive gaps (spacing regularity)
  - Dual L1 / mean_gap (early/late isolation in mean-gap units)

Prior residual surface ended at RC24-RC26 (mean gap envelope, Dual signed
imbalance, chamber open fraction). This probe does not restate those as the
primary deliverable. It states and checks the next residual claims on
segment utilization maxima through 4e8-5e8 and the full o_q branch-max
panel:

  P31 / RC27: Tau4 successive max/mean ratio
              max_successive_gap / mean_gap <= 5.5
  P32 / RC28: Tau4 successive gap CV envelope
              0.55 <= pstdev(gaps) / mean_gap <= 1.0
  P33 / RC29: Dual isolation in mean-gap units
              0.30 <= dual_l1 / mean_gap <= 3.0

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
Between Dual markers the Tau4 body is moderately regular (peak gap is a
few mean spacings; CV is O(1) and below 1), and Dual isolation measured
against that mean spacing stays a few mean-gaps, not a macroscopic fraction
of D. Recurring offset 540 is not a law for D(r) (RC2 remains falsified).
d=4 SDA is not revived.

Audit-only. Does not choose primes as PGS inference.
Prime-square proximity remains an unresolved obligation in PROOF.md;
residual audit only.
"""

from __future__ import annotations

import argparse
import json
import math
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
RC24_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-13-rc24"
    / "offset_540_rc24_prediction_table.json"
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

MAX_OVER_MEAN_MAX = 5.5
CV_MIN = 0.55
CV_MAX = 1.0
DUAL_OVER_MEAN_MIN = 0.30
DUAL_OVER_MEAN_MAX = 3.0
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P31",
        "name": "tau4_successive_max_over_mean",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the ratio of the largest successive Tau4 "
            "inter-hit gap to the mean inter-hit gap satisfies "
            f"max_gap / mean_gap <= {MAX_OVER_MEAN_MAX}."
        ),
        "falsifier": (
            "any evaluated row with max_successive_gap / mean_gap > "
            f"{MAX_OVER_MEAN_MAX}"
        ),
    },
    {
        "id": "P32",
        "name": "tau4_successive_gap_cv_envelope",
        "statement": (
            "On the same surface, the population coefficient of variation of "
            "successive Tau4 inter-hit gaps satisfies "
            f"{CV_MIN} <= pstdev(gaps) / mean_gap <= {CV_MAX}."
        ),
        "falsifier": (
            "any evaluated row with gap_cv < "
            f"{CV_MIN} or gap_cv > {CV_MAX}"
        ),
    },
    {
        "id": "P33",
        "name": "dual_isolation_in_mean_gap_units",
        "statement": (
            "On the same surface, Dual L1 measured in mean-gap units satisfies "
            f"{DUAL_OVER_MEAN_MIN} <= dual_l1 / mean_gap <= {DUAL_OVER_MEAN_MAX} "
            "(early/late isolation is O(1) mean spacings, not macroscopic in D)."
        ),
        "falsifier": (
            "any evaluated row with dual_l1 / mean_gap < "
            f"{DUAL_OVER_MEAN_MIN} or dual_l1 / mean_gap > "
            f"{DUAL_OVER_MEAN_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def population_stdev(values: list[float]) -> float:
    """Population standard deviation (divide by n, not n-1)."""
    n = len(values)
    if n == 0:
        return float("nan")
    mean = sum(values) / n
    return math.sqrt(sum((x - mean) ** 2 for x in values) / n)


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, successive gaps, regularity, isolation ratios.

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
        "max_over_mean": None,
        "gap_cv": None,
        "dual_over_mean": None,
        "trail_over_mean": None,
        "first_over_mean": None,
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
    max_over_mean = max_gap / mean_gap if mean_gap > 0 else None
    gap_cv = (
        population_stdev([float(g) for g in successive]) / mean_gap
        if mean_gap > 0
        else None
    )
    dual_over_mean = dual_l1 / mean_gap if mean_gap > 0 else None
    trail_over_mean = trail_gap / mean_gap if mean_gap > 0 else None
    first_over_mean = first_tau4 / mean_gap if mean_gap > 0 else None
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
        "max_over_mean": max_over_mean,
        "gap_cv": gap_cv,
        "dual_over_mean": dual_over_mean,
        "trail_over_mean": trail_over_mean,
        "first_over_mean": first_over_mean,
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
        "max_over_mean": row["max_over_mean"],
        "gap_cv": row["gap_cv"],
        "dual_over_mean": row["dual_over_mean"],
        "trail_over_mean": row["trail_over_mean"],
        "first_over_mean": row["first_over_mean"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p31(row: dict) -> dict:
    ratio = row["max_over_mean"]
    passed = ratio is not None and float(ratio) <= MAX_OVER_MEAN_MAX
    return {
        "id": "P31",
        "name": "tau4_successive_max_over_mean",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "max_over_mean": ratio,
            "bound_max": MAX_OVER_MEAN_MAX,
            "max_successive_gap": row["max_successive_gap"],
            "mean_gap": row["mean_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p32(row: dict) -> dict:
    cv = row["gap_cv"]
    passed = (
        cv is not None
        and float(cv) >= CV_MIN
        and float(cv) <= CV_MAX
    )
    return {
        "id": "P32",
        "name": "tau4_successive_gap_cv_envelope",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "gap_cv": cv,
            "bound_min": CV_MIN,
            "bound_max": CV_MAX,
            "mean_gap": row["mean_gap"],
            "min_successive_gap": row["min_successive_gap"],
            "max_successive_gap": row["max_successive_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p33(row: dict) -> dict:
    ratio = row["dual_over_mean"]
    passed = (
        ratio is not None
        and float(ratio) >= DUAL_OVER_MEAN_MIN
        and float(ratio) <= DUAL_OVER_MEAN_MAX
    )
    return {
        "id": "P33",
        "name": "dual_isolation_in_mean_gap_units",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_over_mean": ratio,
            "bound_min": DUAL_OVER_MEAN_MIN,
            "bound_max": DUAL_OVER_MEAN_MAX,
            "dual_l1": row["dual_l1"],
            "mean_gap": row["mean_gap"],
            "first_tau4_offset": row["first_tau4_offset"],
            "trail_gap": row["trail_gap"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC27-RC29 residual chamber probe "
            "(successive gap regularity, Dual isolation in mean-gap units)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc24-table", type=Path, default=RC24_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc27_prediction_table.json",
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

    rc24_note = None
    if args.rc24_table.is_file():
        rc24 = json.loads(args.rc24_table.read_text(encoding="utf-8"))
        rc24_note = {
            "path": str(args.rc24_table),
            "conclusion": rc24.get("conclusion"),
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
        "recomputing successive-gap regularity / Dual isolation "
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

    p31_results = [evaluate_p31(row) for row in evaluated]
    p32_results = [evaluate_p32(row) for row in evaluated]
    p33_results = [evaluate_p33(row) for row in evaluated]
    all_results = p31_results + p32_results + p33_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p31_holds = holds(p31_results)
    p32_holds = holds(p32_results)
    p33_holds = holds(p33_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    max_over_means = [
        float(r["max_over_mean"])
        for r in evaluated
        if r["max_over_mean"] is not None
    ]
    gap_cvs = [
        float(r["gap_cv"]) for r in evaluated if r["gap_cv"] is not None
    ]
    dual_over_means = [
        float(r["dual_over_mean"])
        for r in evaluated
        if r["dual_over_mean"] is not None
    ]

    residual_claims = [
        {
            "id": "RC27",
            "claim": (
                "Tau4 successive max/mean ratio: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"max_successive_gap / mean_gap <= {MAX_OVER_MEAN_MAX}."
            ),
            "status": "holds" if p31_holds else "falsified",
            "linked_prediction": "P31",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_max": MAX_OVER_MEAN_MAX,
                "min_observed": min(max_over_means) if max_over_means else None,
                "max_observed": max(max_over_means) if max_over_means else None,
            },
        },
        {
            "id": "RC28",
            "claim": (
                "Tau4 successive gap CV envelope: "
                f"{CV_MIN} <= pstdev(gaps) / mean_gap <= {CV_MAX} "
                "on util maxima + o_q panel."
            ),
            "status": "holds" if p32_holds else "falsified",
            "linked_prediction": "P32",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": CV_MIN,
                "bound_max": CV_MAX,
                "min_observed": min(gap_cvs) if gap_cvs else None,
                "max_observed": max(gap_cvs) if gap_cvs else None,
            },
        },
        {
            "id": "RC29",
            "claim": (
                "Dual isolation in mean-gap units: "
                f"{DUAL_OVER_MEAN_MIN} <= dual_l1 / mean_gap <= "
                f"{DUAL_OVER_MEAN_MAX} on util maxima + o_q panel "
                "(early/late isolation is O(1) mean spacings)."
            ),
            "status": "holds" if p33_holds else "falsified",
            "linked_prediction": "P33",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": DUAL_OVER_MEAN_MIN,
                "bound_max": DUAL_OVER_MEAN_MAX,
                "min_observed": min(dual_over_means) if dual_over_means else None,
                "max_observed": max(dual_over_means) if dual_over_means else None,
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
            "id": "RC24_RC26_retained",
            "claim": (
                "Prior residual RC24-RC26 (mean inter-hit gap envelope, Dual "
                "signed imbalance, chamber open fraction) retained as "
                "measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P28-P30 (prior)",
            "evidence": rc24_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc24_prediction_table": (
                str(args.rc24_table) if args.rc24_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "max_over_mean_max": MAX_OVER_MEAN_MAX,
            "cv_min": CV_MIN,
            "cv_max": CV_MAX,
            "dual_over_mean_min": DUAL_OVER_MEAN_MIN,
            "dual_over_mean_max": DUAL_OVER_MEAN_MAX,
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
            "RC27_tau4_successive_max_over_mean": (
                "holds" if p31_holds else "falsified"
            ),
            "RC28_tau4_successive_gap_cv": (
                "holds" if p32_holds else "falsified"
            ),
            "RC29_dual_isolation_mean_units": (
                "holds" if p33_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC24_RC26": "retained holds (not primary surface)",
            "max_over_mean_range": (
                [min(max_over_means), max(max_over_means)]
                if max_over_means
                else None
            ),
            "gap_cv_range": (
                [min(gap_cvs), max(gap_cvs)] if gap_cvs else None
            ),
            "dual_over_mean_range": (
                [min(dual_over_means), max(dual_over_means)]
                if dual_over_means
                else None
            ),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC27-RC29: Tau4 successive "
                "max/mean ratio, successive gap CV envelope, and Dual "
                "isolation in mean-gap units; does not restate RC24-RC26 "
                "mean-gap envelope / signed imbalance / open fraction as "
                "sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-13-rc27/"
            "offset_540_residual_rc27_probe.py"
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
