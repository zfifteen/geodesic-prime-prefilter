#!/usr/bin/env python3
"""Residual chamber claims RC30-RC32: gap-list central shape + body mass balance.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual markers (first_tau4_offset, trail_gap) with late tau=3 at D
  - successive inter-hit gaps on the ordered Tau4 set
  - mean inter-hit gap on Tau4 body
  - median successive gap / mean_gap (central shape, not peak or CV)
  - fraction of successive gaps <= mean (sub-mean majority)
  - early-body Tau4 mass: share of Tau4 hits in the first half of
    [first_tau4, last_tau4] (body-halves, not D-halves)

Prior residual surface ended at RC27-RC29 (max/mean, gap CV, Dual/mean).
This probe does not restate those as the primary deliverable. It states and
checks the next residual claims on segment utilization maxima through
4e8-5e8 and the full o_q branch-max panel:

  P34 / RC30: Tau4 successive median/mean ratio
              0.65 <= median(gaps) / mean_gap <= 0.95
  P35 / RC31: Sub-mean successive gap majority
              frac(gaps <= mean_gap) >= 0.50
  P36 / RC32: Tau4 body early-mass balance
              0.40 <= early_body_frac <= 0.55
              where early_body_frac counts Tau4 hits with offset < body midpoint

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
Between Dual markers the Tau4 body has positively skewed successive gaps
(median below mean; majority of steps at most the mean) and roughly balanced
early/late body mass. Recurring offset 540 is not a law for D(r)
(RC2 remains falsified). d=4 SDA is not revived.

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
RC27_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-13-rc27"
    / "offset_540_rc27_prediction_table.json"
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

MED_OVER_MEAN_MIN = 0.65
MED_OVER_MEAN_MAX = 0.95
FRAC_LE_MEAN_MIN = 0.50
EARLY_BODY_FRAC_MIN = 0.40
EARLY_BODY_FRAC_MAX = 0.55
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P34",
        "name": "tau4_successive_median_over_mean",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the ratio of the median successive Tau4 "
            "inter-hit gap to the mean inter-hit gap satisfies "
            f"{MED_OVER_MEAN_MIN} <= median(gaps) / mean_gap <= "
            f"{MED_OVER_MEAN_MAX} (positive central skew: median below mean)."
        ),
        "falsifier": (
            "any evaluated row with median_over_mean < "
            f"{MED_OVER_MEAN_MIN} or median_over_mean > {MED_OVER_MEAN_MAX}"
        ),
    },
    {
        "id": "P35",
        "name": "tau4_submean_successive_gap_majority",
        "statement": (
            "On the same surface, the fraction of successive Tau4 inter-hit "
            "gaps that are at most the mean gap satisfies "
            f"frac(gaps <= mean_gap) >= {FRAC_LE_MEAN_MIN}."
        ),
        "falsifier": (
            "any evaluated row with frac_le_mean < "
            f"{FRAC_LE_MEAN_MIN}"
        ),
    },
    {
        "id": "P36",
        "name": "tau4_body_early_mass_balance",
        "statement": (
            "On the same surface, the share of Tau4 hits lying strictly before "
            "the midpoint of the Tau4 body [first_tau4, last_tau4] satisfies "
            f"{EARLY_BODY_FRAC_MIN} <= early_body_frac <= "
            f"{EARLY_BODY_FRAC_MAX} (body-half mass, not D-half mass)."
        ),
        "falsifier": (
            "any evaluated row with early_body_frac < "
            f"{EARLY_BODY_FRAC_MIN} or early_body_frac > "
            f"{EARLY_BODY_FRAC_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, successive gaps, median shape, body-mass balance.

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
        "median_over_mean": None,
        "frac_le_mean": None,
        "early_body_frac": None,
        "body_midpoint": None,
        "skew_mean_median": None,
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
    median_over_mean = median_gap / mean_gap if mean_gap > 0 else None
    frac_le_mean = (
        sum(1 for g in successive if g <= mean_gap) / len(successive)
        if successive
        else None
    )
    body_midpoint = (first_tau4 + last_tau4) / 2.0
    early_body_count = sum(1 for t in tau4_offs if t < body_midpoint)
    early_body_frac = early_body_count / len(tau4_offs)
    skew_mean_median = (
        (mean_gap - median_gap) / mean_gap if mean_gap > 0 else None
    )
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
        "median_over_mean": median_over_mean,
        "frac_le_mean": frac_le_mean,
        "early_body_frac": early_body_frac,
        "body_midpoint": body_midpoint,
        "skew_mean_median": skew_mean_median,
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
        "median_over_mean": row["median_over_mean"],
        "frac_le_mean": row["frac_le_mean"],
        "early_body_frac": row["early_body_frac"],
        "body_midpoint": row["body_midpoint"],
        "skew_mean_median": row["skew_mean_median"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p34(row: dict) -> dict:
    ratio = row["median_over_mean"]
    passed = (
        ratio is not None
        and float(ratio) >= MED_OVER_MEAN_MIN
        and float(ratio) <= MED_OVER_MEAN_MAX
    )
    return {
        "id": "P34",
        "name": "tau4_successive_median_over_mean",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "median_over_mean": ratio,
            "bound_min": MED_OVER_MEAN_MIN,
            "bound_max": MED_OVER_MEAN_MAX,
            "median_gap": row["median_gap"],
            "mean_gap": row["mean_gap"],
            "skew_mean_median": row["skew_mean_median"],
            "D": row["offset"],
        },
    }


def evaluate_p35(row: dict) -> dict:
    frac = row["frac_le_mean"]
    passed = frac is not None and float(frac) >= FRAC_LE_MEAN_MIN
    return {
        "id": "P35",
        "name": "tau4_submean_successive_gap_majority",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "frac_le_mean": frac,
            "bound_min": FRAC_LE_MEAN_MIN,
            "mean_gap": row["mean_gap"],
            "median_gap": row["median_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p36(row: dict) -> dict:
    frac = row["early_body_frac"]
    passed = (
        frac is not None
        and float(frac) >= EARLY_BODY_FRAC_MIN
        and float(frac) <= EARLY_BODY_FRAC_MAX
    )
    return {
        "id": "P36",
        "name": "tau4_body_early_mass_balance",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "early_body_frac": frac,
            "bound_min": EARLY_BODY_FRAC_MIN,
            "bound_max": EARLY_BODY_FRAC_MAX,
            "body_midpoint": row["body_midpoint"],
            "first_tau4_offset": row["first_tau4_offset"],
            "last_tau4_offset": row["last_tau4_offset"],
            "tau4_count": row["tau4_count"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC30-RC32 residual chamber probe "
            "(median/mean gap shape, sub-mean majority, body early-mass)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc27-table", type=Path, default=RC27_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc30_prediction_table.json",
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

    rc27_note = None
    if args.rc27_table.is_file():
        rc27 = json.loads(args.rc27_table.read_text(encoding="utf-8"))
        rc27_note = {
            "path": str(args.rc27_table),
            "conclusion": rc27.get("conclusion"),
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
        "recomputing median/mean, sub-mean majority, body early-mass "
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

    p34_results = [evaluate_p34(row) for row in evaluated]
    p35_results = [evaluate_p35(row) for row in evaluated]
    p36_results = [evaluate_p36(row) for row in evaluated]
    all_results = p34_results + p35_results + p36_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p34_holds = holds(p34_results)
    p35_holds = holds(p35_results)
    p36_holds = holds(p36_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    med_over_means = [
        float(r["median_over_mean"])
        for r in evaluated
        if r["median_over_mean"] is not None
    ]
    frac_le_means = [
        float(r["frac_le_mean"]) for r in evaluated if r["frac_le_mean"] is not None
    ]
    early_body_fracs = [
        float(r["early_body_frac"])
        for r in evaluated
        if r["early_body_frac"] is not None
    ]

    residual_claims = [
        {
            "id": "RC30",
            "claim": (
                "Tau4 successive median/mean ratio: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{MED_OVER_MEAN_MIN} <= median(gaps) / mean_gap <= "
                f"{MED_OVER_MEAN_MAX}."
            ),
            "status": "holds" if p34_holds else "falsified",
            "linked_prediction": "P34",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": MED_OVER_MEAN_MIN,
                "bound_max": MED_OVER_MEAN_MAX,
                "min_observed": min(med_over_means) if med_over_means else None,
                "max_observed": max(med_over_means) if med_over_means else None,
            },
        },
        {
            "id": "RC31",
            "claim": (
                "Sub-mean successive gap majority: "
                f"frac(gaps <= mean_gap) >= {FRAC_LE_MEAN_MIN} "
                "on util maxima + o_q panel."
            ),
            "status": "holds" if p35_holds else "falsified",
            "linked_prediction": "P35",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": FRAC_LE_MEAN_MIN,
                "min_observed": min(frac_le_means) if frac_le_means else None,
                "max_observed": max(frac_le_means) if frac_le_means else None,
            },
        },
        {
            "id": "RC32",
            "claim": (
                "Tau4 body early-mass balance: "
                f"{EARLY_BODY_FRAC_MIN} <= early_body_frac <= "
                f"{EARLY_BODY_FRAC_MAX} on util maxima + o_q panel "
                "(body-half mass, not D-half mass)."
            ),
            "status": "holds" if p36_holds else "falsified",
            "linked_prediction": "P36",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": EARLY_BODY_FRAC_MIN,
                "bound_max": EARLY_BODY_FRAC_MAX,
                "min_observed": min(early_body_fracs) if early_body_fracs else None,
                "max_observed": max(early_body_fracs) if early_body_fracs else None,
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
            "id": "RC27_RC29_retained",
            "claim": (
                "Prior residual RC27-RC29 (successive max/mean, gap CV, Dual "
                "isolation in mean-gap units) retained as measured holds; "
                "not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P31-P33 (prior)",
            "evidence": rc27_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc27_prediction_table": (
                str(args.rc27_table) if args.rc27_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "med_over_mean_min": MED_OVER_MEAN_MIN,
            "med_over_mean_max": MED_OVER_MEAN_MAX,
            "frac_le_mean_min": FRAC_LE_MEAN_MIN,
            "early_body_frac_min": EARLY_BODY_FRAC_MIN,
            "early_body_frac_max": EARLY_BODY_FRAC_MAX,
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
            "RC30_tau4_successive_median_over_mean": (
                "holds" if p34_holds else "falsified"
            ),
            "RC31_tau4_submean_gap_majority": (
                "holds" if p35_holds else "falsified"
            ),
            "RC32_tau4_body_early_mass_balance": (
                "holds" if p36_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC27_RC29": "retained holds (not primary surface)",
            "median_over_mean_range": (
                [min(med_over_means), max(med_over_means)]
                if med_over_means
                else None
            ),
            "frac_le_mean_range": (
                [min(frac_le_means), max(frac_le_means)] if frac_le_means else None
            ),
            "early_body_frac_range": (
                [min(early_body_fracs), max(early_body_fracs)]
                if early_body_fracs
                else None
            ),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC30-RC32: Tau4 successive "
                "median/mean ratio, sub-mean successive gap majority, and "
                "Tau4 body early-mass balance; does not restate RC27-RC29 "
                "max/mean, CV, or Dual/mean as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-13-rc30/"
            "offset_540_residual_rc30_probe.py"
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
