#!/usr/bin/env python3
"""Residual chamber claims RC48-RC50: multiset occupancy + peak-desert locus.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - ordered Tau4 offset set inside the chamber prefix
  - successive inter-hit gap multiset on Tau4
  - peak successive desert locus (argmax gap index, body midpoint)

Prior residual surface ended at RC45-RC47 (min/mean, dual/count, max/body).
Those are affine renorms of envelope scalars. This probe states multiset
occupancy and ordered desert *position* claims that need the full gap
sequence, not only {min, max, mean, dual, n, body, D}.

  P52 / RC48: Tight-pair mass of successive Tau4 gaps
              0.08 <= #{g <= 2} / #{gaps} <= 0.30
  P53 / RC49: Peak-desert body locus (midpoint of max successive gap)
              0.25 <= desert_pos_frac <= 0.98
  P54 / RC50: Large-desert tail share above 2 * median gap
              0.08 <= #{g >= 2*median} / #{gaps} <= 0.35

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
RC48 measures packing-floor *mass* in the gap multiset (not min alone).
RC49 measures *where* the peak desert sits on the Tau4 body (not max/body).
RC50 measures large-gap *occupancy* (not max/median height).

Recurring offset 540 is not a law for D(r) (RC2 remains falsified).
d=4 SDA is not revived.
Not pure Dual/scale ratio minting of the RC18-RC47 ladder.

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
RC45_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-15-rc45"
    / "offset_540_rc45_prediction_table.json"
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

TIGHT_FRAC_MIN = 0.08
TIGHT_FRAC_MAX = 0.30
DESERT_POS_MIN = 0.25
DESERT_POS_MAX = 0.98
LARGE_FRAC_MIN = 0.08
LARGE_FRAC_MAX = 0.35
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P52",
        "name": "tau4_tight_pair_mass",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the successive Tau4 gap multiset tight-pair "
            "mass tight_frac = #{g <= 2} / #{gaps} satisfies "
            f"{TIGHT_FRAC_MIN} <= tight_frac <= {TIGHT_FRAC_MAX} "
            "(multiset occupancy at packing floor; not min/mean RC45; "
            "not min/median RC42)."
        ),
        "falsifier": (
            "any evaluated row with tight_frac < "
            f"{TIGHT_FRAC_MIN} or tight_frac > {TIGHT_FRAC_MAX}"
        ),
    },
    {
        "id": "P53",
        "name": "peak_desert_body_locus",
        "statement": (
            "On the same surface, the body-midpoint locus of the leftmost "
            "maximum successive Tau4 desert desert_pos_frac = "
            "(mid(i*) - first_tau4) / tau4_body satisfies "
            f"{DESERT_POS_MIN} <= desert_pos_frac <= {DESERT_POS_MAX} "
            "(ordered peak-desert position; not max/body RC47; not max/D RC11)."
        ),
        "falsifier": (
            "any evaluated row with desert_pos_frac < "
            f"{DESERT_POS_MIN} or desert_pos_frac > {DESERT_POS_MAX}"
        ),
    },
    {
        "id": "P54",
        "name": "large_desert_tail_share",
        "statement": (
            "On the same surface, the large-desert tail share "
            "large_frac = #{g >= 2 * median_gap} / #{gaps} satisfies "
            f"{LARGE_FRAC_MIN} <= large_frac <= {LARGE_FRAC_MAX} "
            "(multiset tail occupancy; not max/median RC37; not max/mean RC27)."
        ),
        "falsifier": (
            "any evaluated row with large_frac < "
            f"{LARGE_FRAC_MIN} or large_frac > {LARGE_FRAC_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers plus multiset occupancy / desert locus metrics.

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
        "i_star": None,
        "desert_pos_frac": None,
        "desert_rank_frac": None,
        "peak_desert_interior": None,
        "tight_frac": None,
        "large_frac": None,
        "prefix_min_tau": prefix_min_tau,
        "tau3_in_prefix": tau3_in_prefix,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        "domain_ok": False,
    }
    # Need |Tau4| >= 3 so there are >= 2 successive gaps and a meaningful rank.
    if len(tau4_offs) < 3:
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
    # Leftmost maximum successive desert.
    i_star = min(
        (i for i, g in enumerate(successive) if g == max_gap),
        default=0,
    )
    mid = (tau4_offs[i_star] + tau4_offs[i_star + 1]) / 2.0
    desert_pos_frac = (mid - first_tau4) / tau4_body if tau4_body > 0 else None
    n_gaps = len(successive)
    desert_rank_frac = (
        i_star / (n_gaps - 1) if n_gaps > 1 else None
    )
    peak_desert_interior = 0 < i_star < (n_gaps - 1)
    tight_frac = sum(1 for g in successive if g <= 2) / n_gaps
    large_frac = sum(1 for g in successive if g >= 2.0 * median_gap) / n_gaps
    domain_ok = (
        mean_gap > 0
        and min_gap > 0
        and max_gap > 0
        and tau4_body > 0
        and desert_pos_frac is not None
        and n_gaps >= 2
    )
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
        "i_star": i_star,
        "desert_pos_frac": desert_pos_frac,
        "desert_rank_frac": desert_rank_frac,
        "peak_desert_interior": peak_desert_interior,
        "tight_frac": tight_frac,
        "large_frac": large_frac,
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
        "i_star": row["i_star"],
        "desert_pos_frac": row["desert_pos_frac"],
        "desert_rank_frac": row["desert_rank_frac"],
        "peak_desert_interior": row["peak_desert_interior"],
        "tight_frac": row["tight_frac"],
        "large_frac": row["large_frac"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
        "domain_ok": row["domain_ok"],
    }


def _eval_bound(
    row: dict,
    pred_index: int,
    metric_key: str,
    bound_min: float,
    bound_max: float,
) -> dict:
    pred = PREDICTIONS[pred_index]
    value = row.get(metric_key)
    if value is None or not row.get("domain_ok"):
        return {
            "id": pred["id"],
            "name": pred["name"],
            "statement": pred["statement"],
            "falsifier": pred["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=3 and positive body/gaps",
                metric_key: value,
            },
        }
    passed = float(value) >= bound_min and float(value) <= bound_max
    return {
        "id": pred["id"],
        "name": pred["name"],
        "statement": pred["statement"],
        "falsifier": pred["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            metric_key: value,
            "bound_min": bound_min,
            "bound_max": bound_max,
            "i_star": row.get("i_star"),
            "max_successive_gap": row.get("max_successive_gap"),
            "median_gap": row.get("median_gap"),
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC48-RC50 residual chamber probe "
            "(tight-pair mass, peak-desert locus, large-desert tail share)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc45-table", type=Path, default=RC45_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "offset_540_rc48_prediction_table.json",
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

    rc45_note = None
    if args.rc45_table.is_file():
        rc45 = json.loads(args.rc45_table.read_text(encoding="utf-8"))
        rc45_note = {
            "path": str(args.rc45_table),
            "conclusion": {
                k: rc45.get("conclusion", {}).get(k)
                for k in (
                    "RC45_successive_floor_over_mean",
                    "RC46_dual_l1_per_tau4_hit",
                    "RC47_peak_desert_body_share",
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
        "recomputing tight_frac, desert_pos_frac, large_frac "
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

    p52_results = [
        _eval_bound(row, 0, "tight_frac", TIGHT_FRAC_MIN, TIGHT_FRAC_MAX)
        for row in evaluated
    ]
    p53_results = [
        _eval_bound(row, 1, "desert_pos_frac", DESERT_POS_MIN, DESERT_POS_MAX)
        for row in evaluated
    ]
    p54_results = [
        _eval_bound(row, 2, "large_frac", LARGE_FRAC_MIN, LARGE_FRAC_MAX)
        for row in evaluated
    ]
    all_results = p52_results + p53_results + p54_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p52_holds = holds(p52_results)
    p53_holds = holds(p53_results)
    p54_holds = holds(p54_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    unique_by_r: dict[int, dict] = {}
    for row in evaluated:
        unique_by_r[int(row["r"])] = row
    unique_rows = list(unique_by_r.values())

    tight_vals = [
        float(r["tight_frac"])
        for r in unique_rows
        if r["tight_frac"] is not None
    ]
    desert_vals = [
        float(r["desert_pos_frac"])
        for r in unique_rows
        if r["desert_pos_frac"] is not None
    ]
    large_vals = [
        float(r["large_frac"])
        for r in unique_rows
        if r["large_frac"] is not None
    ]
    interior_all = all(
        bool(r.get("peak_desert_interior")) for r in unique_rows if r.get("domain_ok")
    )

    residual_claims = [
        {
            "id": "RC48",
            "claim": (
                "Tight-pair mass of successive Tau4 gaps: on segment "
                "utilization maxima through 4e8-5e8 and the full o_q "
                "branch-max panel, "
                f"{TIGHT_FRAC_MIN} <= count(g<=2)/count(gaps) <= "
                f"{TIGHT_FRAC_MAX}."
            ),
            "status": "holds" if p52_holds else "falsified",
            "linked_prediction": "P52",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": TIGHT_FRAC_MIN,
                "bound_max": TIGHT_FRAC_MAX,
                "min_observed": min(tight_vals) if tight_vals else None,
                "max_observed": max(tight_vals) if tight_vals else None,
            },
        },
        {
            "id": "RC49",
            "claim": (
                "Peak successive Tau4 desert body locus: "
                f"{DESERT_POS_MIN} <= desert_pos_frac <= {DESERT_POS_MAX} "
                "on util maxima + o_q panel (midpoint of leftmost max gap "
                "mapped onto Tau4 body; not max/body size)."
            ),
            "status": "holds" if p53_holds else "falsified",
            "linked_prediction": "P53",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": DESERT_POS_MIN,
                "bound_max": DESERT_POS_MAX,
                "min_observed": min(desert_vals) if desert_vals else None,
                "max_observed": max(desert_vals) if desert_vals else None,
                "all_peak_deserts_interior": interior_all,
            },
        },
        {
            "id": "RC50",
            "claim": (
                "Large-desert tail share of successive Tau4 gaps: "
                f"{LARGE_FRAC_MIN} <= count(g>=2*median)/count(gaps) <= "
                f"{LARGE_FRAC_MAX} on util maxima + o_q panel "
                "(multiset tail occupancy; not max/median height)."
            ),
            "status": "holds" if p54_holds else "falsified",
            "linked_prediction": "P54",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": LARGE_FRAC_MIN,
                "bound_max": LARGE_FRAC_MAX,
                "min_observed": min(large_vals) if large_vals else None,
                "max_observed": max(large_vals) if large_vals else None,
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
            "id": "RC45_RC47_retained",
            "claim": (
                "Prior residual RC45-RC47 (min/mean, dual/count, max/body) "
                "retained as measured holds; not re-proved as primary surface."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P49-P51 (prior)",
            "evidence": rc45_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc45_prediction_table": (
                str(args.rc45_table) if args.rc45_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "tight_frac_min": TIGHT_FRAC_MIN,
            "tight_frac_max": TIGHT_FRAC_MAX,
            "desert_pos_min": DESERT_POS_MIN,
            "desert_pos_max": DESERT_POS_MAX,
            "large_frac_min": LARGE_FRAC_MIN,
            "large_frac_max": LARGE_FRAC_MAX,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-square proximity remains unresolved in PROOF.md "
                "section Square-Branch Reduction; residual audit only. "
                "Direct next-prime and Interior Maximizer remain proved."
            ),
            "geometry_note": (
                "RC48-RC50 use full successive-gap multiset occupancy and "
                "ordered peak-desert locus; not affine renorms of "
                "{min,max,mean,med,dual,n,body,D} alone."
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC48_tight_pair_mass": "holds" if p52_holds else "falsified",
            "RC49_peak_desert_body_locus": (
                "holds" if p53_holds else "falsified"
            ),
            "RC50_large_desert_tail_share": (
                "holds" if p54_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC45_RC47": "retained holds (not primary surface)",
            "tight_frac_range": (
                [min(tight_vals), max(tight_vals)] if tight_vals else None
            ),
            "desert_pos_frac_range": (
                [min(desert_vals), max(desert_vals)] if desert_vals else None
            ),
            "large_frac_range": (
                [min(large_vals), max(large_vals)] if large_vals else None
            ),
            "all_peak_deserts_interior": interior_all,
            "unique_chamber_count": len(unique_rows),
            "surface_row_count": len(evaluated),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC48-RC50: successive Tau4 gap "
                "multiset tight-pair mass (tight_frac), ordered peak-desert "
                "body locus (desert_pos_frac), and large-desert tail share "
                "(large_frac); does not restate RC45-RC47 envelope ratios as "
                "sole deliverable; does not revive fixed-band 540 or d=4 SDA; "
                "does not empty Annulus(r) / close S1*."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-16-rc48/"
            "offset_540_residual_rc48_probe.py"
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
