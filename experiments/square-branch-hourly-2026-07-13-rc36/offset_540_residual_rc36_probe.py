#!/usr/bin/env python3
"""Residual chamber claims RC36-RC38: opening isolation + peak/median + IQR/mean.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual markers (first_tau4_offset, trail_gap) with late tau=3 at D
  - successive inter-hit gaps on the ordered Tau4 set
  - mean inter-hit gap (last - first) / (tau4_count - 1)
  - median successive gap
  - IQR of successive gaps (linear-interpolation percentiles)
  - opening isolation first_tau4 / mean_gap
  - peak successive gap vs median max_gap / median_gap
  - robust scale vs mean iqr_gap / mean_gap

Prior residual surface ended at RC33-RC35 (IQR/median, trail/mean, body
last-quartile). This probe does not restate those as the primary deliverable.
It states and checks the next residual claims on segment utilization maxima
through 4e8-5e8 and the full o_q branch-max panel:

  P40 / RC36: Opening isolation in mean-gap units
              0.15 <= first_tau4 / mean_gap <= 2.00
  P41 / RC37: Peak successive gap vs median
              2.50 <= max_gap / median_gap <= 8.00
  P42 / RC38: IQR scaled by mean
              0.50 <= iqr_gap / mean_gap <= 1.20

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
The opening run to the first tau=4 hit is a bounded number of mean gaps
(opening isolation, not trail closing), the tallest successive Tau4 desert
is a bounded multiple of the median gap (peak vs central scale, not vs mean),
and the IQR of successive gaps stays a bounded fraction of the mean gap
(mean-relative robust scale, not median-relative IQR). Recurring offset 540
is not a law for D(r) (RC2 remains falsified). d=4 SDA is not revived.

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
RC33_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-13-rc33"
    / "offset_540_rc33_prediction_table.json"
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

OPEN_OVER_MEAN_MIN = 0.15
OPEN_OVER_MEAN_MAX = 2.00
MAX_OVER_MED_MIN = 2.50
MAX_OVER_MED_MAX = 8.00
IQR_OVER_MEAN_MIN = 0.50
IQR_OVER_MEAN_MAX = 1.20
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P40",
        "name": "opening_isolation_in_mean_gap_units",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the opening isolation "
            "first_tau4 / mean_gap satisfies "
            f"{OPEN_OVER_MEAN_MIN} <= first_tau4 / mean_gap <= "
            f"{OPEN_OVER_MEAN_MAX} (opening component only; not trail/mean)."
        ),
        "falsifier": (
            "any evaluated row with open_over_mean < "
            f"{OPEN_OVER_MEAN_MIN} or open_over_mean > {OPEN_OVER_MEAN_MAX}"
        ),
    },
    {
        "id": "P41",
        "name": "peak_successive_gap_over_median",
        "statement": (
            "On the same surface, the ratio of the maximum successive Tau4 "
            "inter-hit gap to the median successive gap satisfies "
            f"{MAX_OVER_MED_MIN} <= max_gap / median_gap <= "
            f"{MAX_OVER_MED_MAX} (peak vs central scale; not max/mean)."
        ),
        "falsifier": (
            "any evaluated row with max_over_median < "
            f"{MAX_OVER_MED_MIN} or max_over_median > {MAX_OVER_MED_MAX}"
        ),
    },
    {
        "id": "P42",
        "name": "iqr_scaled_by_mean",
        "statement": (
            "On the same surface, the ratio of the interquartile range of "
            "successive Tau4 gaps to the mean gap satisfies "
            f"{IQR_OVER_MEAN_MIN} <= iqr_gap / mean_gap <= "
            f"{IQR_OVER_MEAN_MAX} (mean-relative robust scale; not IQR/median)."
        ),
        "falsifier": (
            "any evaluated row with iqr_over_mean < "
            f"{IQR_OVER_MEAN_MIN} or iqr_over_mean > {IQR_OVER_MEAN_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def _percentile_linear(sorted_vals: list[float], p: float) -> float:
    """Linear-interpolation percentile on a non-empty sorted list."""
    n = len(sorted_vals)
    if n == 1:
        return float(sorted_vals[0])
    if p <= 0:
        return float(sorted_vals[0])
    if p >= 1:
        return float(sorted_vals[-1])
    k = (n - 1) * p
    f = int(k)
    c = min(f + 1, n - 1)
    return float(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f))


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, successive gaps, open/mean, max/med, IQR/mean.

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
        "q1_gap": None,
        "q3_gap": None,
        "iqr_gap": None,
        "open_over_mean": None,
        "max_over_median": None,
        "iqr_over_mean": None,
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
    sorted_gaps = sorted(float(g) for g in successive)
    q1_gap = _percentile_linear(sorted_gaps, 0.25)
    q3_gap = _percentile_linear(sorted_gaps, 0.75)
    iqr_gap = q3_gap - q1_gap
    open_over_mean = first_tau4 / mean_gap if mean_gap > 0 else None
    max_over_median = max_gap / median_gap if median_gap > 0 else None
    iqr_over_mean = iqr_gap / mean_gap if mean_gap > 0 else None
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
        "q1_gap": q1_gap,
        "q3_gap": q3_gap,
        "iqr_gap": iqr_gap,
        "open_over_mean": open_over_mean,
        "max_over_median": max_over_median,
        "iqr_over_mean": iqr_over_mean,
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
        "q1_gap": row["q1_gap"],
        "q3_gap": row["q3_gap"],
        "iqr_gap": row["iqr_gap"],
        "open_over_mean": row["open_over_mean"],
        "max_over_median": row["max_over_median"],
        "iqr_over_mean": row["iqr_over_mean"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p40(row: dict) -> dict:
    ratio = row["open_over_mean"]
    passed = (
        ratio is not None
        and float(ratio) >= OPEN_OVER_MEAN_MIN
        and float(ratio) <= OPEN_OVER_MEAN_MAX
    )
    return {
        "id": "P40",
        "name": "opening_isolation_in_mean_gap_units",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "open_over_mean": ratio,
            "bound_min": OPEN_OVER_MEAN_MIN,
            "bound_max": OPEN_OVER_MEAN_MAX,
            "first_tau4_offset": row["first_tau4_offset"],
            "mean_gap": row["mean_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p41(row: dict) -> dict:
    ratio = row["max_over_median"]
    passed = (
        ratio is not None
        and float(ratio) >= MAX_OVER_MED_MIN
        and float(ratio) <= MAX_OVER_MED_MAX
    )
    return {
        "id": "P41",
        "name": "peak_successive_gap_over_median",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "max_over_median": ratio,
            "bound_min": MAX_OVER_MED_MIN,
            "bound_max": MAX_OVER_MED_MAX,
            "max_successive_gap": row["max_successive_gap"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p42(row: dict) -> dict:
    ratio = row["iqr_over_mean"]
    passed = (
        ratio is not None
        and float(ratio) >= IQR_OVER_MEAN_MIN
        and float(ratio) <= IQR_OVER_MEAN_MAX
    )
    return {
        "id": "P42",
        "name": "iqr_scaled_by_mean",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "iqr_over_mean": ratio,
            "bound_min": IQR_OVER_MEAN_MIN,
            "bound_max": IQR_OVER_MEAN_MAX,
            "iqr_gap": row["iqr_gap"],
            "mean_gap": row["mean_gap"],
            "q1_gap": row["q1_gap"],
            "q3_gap": row["q3_gap"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC36-RC38 residual chamber probe "
            "(open/mean isolation, max/median peak, IQR/mean scale)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc33-table", type=Path, default=RC33_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc36_prediction_table.json",
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

    rc33_note = None
    if args.rc33_table.is_file():
        rc33 = json.loads(args.rc33_table.read_text(encoding="utf-8"))
        rc33_note = {
            "path": str(args.rc33_table),
            "conclusion": {
                k: rc33.get("conclusion", {}).get(k)
                for k in (
                    "RC33_tau4_successive_gap_iqr_over_median",
                    "RC34_trail_closing_isolation_mean_units",
                    "RC35_tau4_body_last_quartile_mass",
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
        "recomputing open/mean, max/median, IQR/mean "
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

    p40_results = [evaluate_p40(row) for row in evaluated]
    p41_results = [evaluate_p41(row) for row in evaluated]
    p42_results = [evaluate_p42(row) for row in evaluated]
    all_results = p40_results + p41_results + p42_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p40_holds = holds(p40_results)
    p41_holds = holds(p41_results)
    p42_holds = holds(p42_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    open_over_means = [
        float(r["open_over_mean"])
        for r in evaluated
        if r["open_over_mean"] is not None
    ]
    max_over_meds = [
        float(r["max_over_median"])
        for r in evaluated
        if r["max_over_median"] is not None
    ]
    iqr_over_means = [
        float(r["iqr_over_mean"])
        for r in evaluated
        if r["iqr_over_mean"] is not None
    ]

    residual_claims = [
        {
            "id": "RC36",
            "claim": (
                "Opening isolation in mean-gap units: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{OPEN_OVER_MEAN_MIN} <= first_tau4 / mean_gap <= "
                f"{OPEN_OVER_MEAN_MAX}."
            ),
            "status": "holds" if p40_holds else "falsified",
            "linked_prediction": "P40",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": OPEN_OVER_MEAN_MIN,
                "bound_max": OPEN_OVER_MEAN_MAX,
                "min_observed": min(open_over_means) if open_over_means else None,
                "max_observed": max(open_over_means) if open_over_means else None,
            },
        },
        {
            "id": "RC37",
            "claim": (
                "Peak successive gap vs median: "
                f"{MAX_OVER_MED_MIN} <= max_gap / median_gap <= "
                f"{MAX_OVER_MED_MAX} on util maxima + o_q panel "
                "(peak vs central scale; not max/mean)."
            ),
            "status": "holds" if p41_holds else "falsified",
            "linked_prediction": "P41",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": MAX_OVER_MED_MIN,
                "bound_max": MAX_OVER_MED_MAX,
                "min_observed": min(max_over_meds) if max_over_meds else None,
                "max_observed": max(max_over_meds) if max_over_meds else None,
            },
        },
        {
            "id": "RC38",
            "claim": (
                "IQR scaled by mean: "
                f"{IQR_OVER_MEAN_MIN} <= iqr_gap / mean_gap <= "
                f"{IQR_OVER_MEAN_MAX} on util maxima + o_q panel "
                "(mean-relative robust scale; not IQR/median)."
            ),
            "status": "holds" if p42_holds else "falsified",
            "linked_prediction": "P42",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": IQR_OVER_MEAN_MIN,
                "bound_max": IQR_OVER_MEAN_MAX,
                "min_observed": min(iqr_over_means) if iqr_over_means else None,
                "max_observed": max(iqr_over_means) if iqr_over_means else None,
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
            "id": "RC33_RC35_retained",
            "claim": (
                "Prior residual RC33-RC35 (IQR/median, trail/mean, body "
                "last-quartile) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P37-P39 (prior)",
            "evidence": rc33_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc33_prediction_table": (
                str(args.rc33_table) if args.rc33_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "open_over_mean_min": OPEN_OVER_MEAN_MIN,
            "open_over_mean_max": OPEN_OVER_MEAN_MAX,
            "max_over_median_min": MAX_OVER_MED_MIN,
            "max_over_median_max": MAX_OVER_MED_MAX,
            "iqr_over_mean_min": IQR_OVER_MEAN_MIN,
            "iqr_over_mean_max": IQR_OVER_MEAN_MAX,
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
            "RC36_opening_isolation_mean_units": (
                "holds" if p40_holds else "falsified"
            ),
            "RC37_peak_successive_gap_over_median": (
                "holds" if p41_holds else "falsified"
            ),
            "RC38_iqr_scaled_by_mean": "holds" if p42_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC33_RC35": "retained holds (not primary surface)",
            "open_over_mean_range": (
                [min(open_over_means), max(open_over_means)]
                if open_over_means
                else None
            ),
            "max_over_median_range": (
                [min(max_over_meds), max(max_over_meds)] if max_over_meds else None
            ),
            "iqr_over_mean_range": (
                [min(iqr_over_means), max(iqr_over_means)]
                if iqr_over_means
                else None
            ),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC36-RC38: opening isolation in "
                "mean-gap units, peak successive gap vs median, and IQR "
                "scaled by mean; does not restate RC33-RC35 IQR/median, "
                "trail/mean, or body last-quartile as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-13-rc36/"
            "offset_540_residual_rc36_probe.py"
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
