#!/usr/bin/env python3
"""Residual chamber claims RC51-RC53: proximity slack / headroom / high-pressure locus.

PGS objects:
  - selected square endpoint w = r^2
  - left prime q = P(w) (table field "p")
  - offset D(r) = w - q
  - dynamic cutoff C_dyn(q) = max(64, ceil(0.5 * log(q)^2))
  - proximity utilization u(r) = D(r) / C_dyn(q)
  - absolute headroom h(r) = C_dyn(q) - D(r)

Prior residual surface ended at RC48-RC50 (Tau4 successive-gap multiset
occupancy and peak-desert body locus). Those are packing objects on the
chamber prefix. This probe states endpoint-budget residual claims that need
only (D, C_dyn), not the Tau4 multiset.

  P55 / RC51: Proximity utilization envelope on util-max + o_q panel
              0.55 <= u = D/C_dyn <= 0.98
  P56 / RC52: Absolute headroom envelope
              45 <= h = C_dyn - D <= 350
  P57 / RC53: High-pressure locus (conditional)
              if u >= 0.85 then o_q = 6 and |D - 540| >= 150

Structural reading: early tau=4 / late tau=3 chamber separation (RC1) is
retained as prior geometry. Recurring offset 540 is not a law for D(r)
(RC2 remains falsified at D=738). High utilization on this panel sits far
from the historical 540 cluster (RC53).

u(r) <= 1 is Target S1* (Annulus emptiness), still UNRESOLVED in PROOF.md.
Panel envelopes below are residual audit only and do not prove S1*.

d=4 SDA is not revived.
Not multiset renorm of RC48-RC50.
Not Dual / density renorm of RC3-RC47.

Audit-only. Does not choose primes as PGS inference.
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

from gwr_dni_recursive_walk import dynamic_cutoff  # noqa: E402

PRIOR_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10"
    / "offset_540_prediction_table.json"
)
RC48_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-16-rc48"
    / "offset_540_rc48_prediction_table.json"
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

U_MIN = 0.55
U_MAX = 0.98
H_MIN = 45
H_MAX = 350
HIGH_U_THRESH = 0.85
HIGH_U_ABS_D_MIN = 150
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P55",
        "name": "proximity_utilization_envelope",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, proximity utilization "
            "u(r) = D(r)/C_dyn(q) satisfies "
            f"{U_MIN} <= u <= {U_MAX} "
            "(endpoint budget pressure; not Tau4 multiset RC48-RC50; "
            "not Dual renorm; residual panel audit only — not Target S1*)."
        ),
        "falsifier": (
            f"any evaluated row with u < {U_MIN} or u > {U_MAX}"
        ),
    },
    {
        "id": "P56",
        "name": "absolute_headroom_envelope",
        "statement": (
            "On the same surface, absolute headroom "
            "h(r) = C_dyn(q) - D(r) satisfies "
            f"{H_MIN} <= h <= {H_MAX} "
            "(integer remaining budget to S1* breach line u=1; "
            "complement of RC51; residual audit only)."
        ),
        "falsifier": (
            f"any evaluated row with h < {H_MIN} or h > {H_MAX}"
        ),
    },
    {
        "id": "P57",
        "name": "high_pressure_locus",
        "statement": (
            "On the same surface, if u(r) >= "
            f"{HIGH_U_THRESH}, then o_q = 6 and "
            f"|D(r) - 540| >= {HIGH_U_ABS_D_MIN} "
            "(high proximity pressure sits outside the historical 540 cluster; "
            "supports RC2 falsification as structural reading, not a new law)."
        ),
        "falsifier": (
            f"any row with u >= {HIGH_U_THRESH} and "
            f"(o_q != 6 or |D-540| < {HIGH_U_ABS_D_MIN})"
        ),
    },
]


def slack_structure(row: dict) -> dict[str, object]:
    """Compute u = D/C_dyn and h = C_dyn - D from stored chamber endpoints.

    Uses the same dynamic_cutoff(q) as square_branch_dynamic_cutoff_search
    (q = previous prime before the selected square). No tau segment scan.
    """
    q = int(row["p"])
    d = int(row["offset"])
    c = int(dynamic_cutoff(q))
    if c <= 0 or d <= 0:
        return {
            "dynamic_cutoff": c,
            "proximity_slack_u": None,
            "headroom_h": None,
            "abs_d_minus_540": abs(d - NEAR_540_CENTER),
            "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
            "domain_ok": False,
        }
    u = d / c
    h = c - d
    stored_c = row.get("dynamic_cutoff")
    stored_u = row.get("utilization")
    if stored_c is not None and int(stored_c) != c:
        raise ValueError(
            f"dynamic_cutoff mismatch for r={row.get('r')}: "
            f"stored={stored_c} recomputed={c}"
        )
    if stored_u is not None and abs(float(stored_u) - u) > 1e-12:
        raise ValueError(
            f"utilization mismatch for r={row.get('r')}: "
            f"stored={stored_u} recomputed={u}"
        )
    return {
        "dynamic_cutoff": c,
        "proximity_slack_u": u,
        "headroom_h": h,
        "abs_d_minus_540": abs(d - NEAR_540_CENTER),
        "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        "domain_ok": True,
        "table_utilization": stored_u,
        "table_dynamic_cutoff": stored_c,
    }


def enrich_row(row: dict) -> dict:
    out = dict(row)
    out.update(slack_structure(row))
    return out


def _compact(row: dict) -> dict:
    return {
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "dynamic_cutoff": row["dynamic_cutoff"],
        "proximity_slack_u": row["proximity_slack_u"],
        "headroom_h": row["headroom_h"],
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
            "detail": {"reason": "domain gate failed", metric_key: value},
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
            "dynamic_cutoff": row.get("dynamic_cutoff"),
            "D": row["offset"],
        },
    }


def _eval_high_pressure(row: dict) -> dict:
    pred = PREDICTIONS[2]
    u = row.get("proximity_slack_u")
    if u is None or not row.get("domain_ok"):
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
            "detail": {"reason": "domain gate failed"},
        }
    if float(u) < HIGH_U_THRESH:
        return {
            "id": pred["id"],
            "name": pred["name"],
            "statement": pred["statement"],
            "falsifier": pred["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": True,
            "status": "holds",
            "detail": {
                "antecedent": False,
                "proximity_slack_u": u,
                "high_u_thresh": HIGH_U_THRESH,
                "note": "antecedent u>=thresh false; conditional auto-pass",
            },
        }
    o_q = row.get("o_q")
    abs_d = int(row["abs_d_minus_540"])
    passed = (o_q is not None and int(o_q) == 6) and abs_d >= HIGH_U_ABS_D_MIN
    return {
        "id": pred["id"],
        "name": pred["name"],
        "statement": pred["statement"],
        "falsifier": pred["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": o_q,
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "antecedent": True,
            "proximity_slack_u": u,
            "o_q": o_q,
            "abs_d_minus_540": abs_d,
            "require_o_q": 6,
            "require_abs_d_min": HIGH_U_ABS_D_MIN,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC51-RC53 residual chamber probe "
            "(proximity utilization, headroom, high-pressure locus)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc48-table", type=Path, default=RC48_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "offset_540_rc51_prediction_table.json",
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

    rc48_note = None
    if args.rc48_table.is_file():
        rc48 = json.loads(args.rc48_table.read_text(encoding="utf-8"))
        rc48_note = {
            "path": str(args.rc48_table),
            "conclusion": {
                k: rc48.get("conclusion", {}).get(k)
                for k in (
                    "RC48_tight_pair_mass",
                    "RC49_peak_desert_body_locus",
                    "RC50_large_desert_tail_share",
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
        "computing proximity_slack_u and headroom_h on primary + o_q panel...",
        flush=True,
    )
    try:
        primary_rows = [enrich_row(row) for row in primary_src]
        oq_rows = [enrich_row(row) for row in oq_src]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 4
    evaluated = primary_rows + oq_rows

    p55_results = [
        _eval_bound(row, 0, "proximity_slack_u", U_MIN, U_MAX)
        for row in evaluated
    ]
    p56_results = [
        _eval_bound(row, 1, "headroom_h", H_MIN, H_MAX) for row in evaluated
    ]
    p57_results = [_eval_high_pressure(row) for row in evaluated]
    all_results = p55_results + p56_results + p57_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p55_holds = holds(p55_results)
    p56_holds = holds(p56_results)
    p57_holds = holds(p57_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]

    unique_by_r: dict[int, dict] = {}
    for row in evaluated:
        unique_by_r[int(row["r"])] = row
    unique_rows = list(unique_by_r.values())

    u_vals = [
        float(r["proximity_slack_u"])
        for r in unique_rows
        if r["proximity_slack_u"] is not None
    ]
    h_vals = [
        float(r["headroom_h"]) for r in unique_rows if r["headroom_h"] is not None
    ]
    high_u_rows = [
        {
            "r": int(r["r"]),
            "offset": int(r["offset"]),
            "o_q": r.get("o_q"),
            "proximity_slack_u": r["proximity_slack_u"],
            "abs_d_minus_540": r["abs_d_minus_540"],
        }
        for r in unique_rows
        if r["proximity_slack_u"] is not None
        and float(r["proximity_slack_u"]) >= HIGH_U_THRESH
    ]

    residual_claims = [
        {
            "id": "RC51",
            "claim": (
                "Proximity utilization envelope: on segment utilization "
                "maxima through 4e8-5e8 and the full o_q branch-max panel, "
                f"{U_MIN} <= D/C_dyn <= {U_MAX} "
                "(endpoint budget residual; not S1* closure)."
            ),
            "status": "holds" if p55_holds else "falsified",
            "linked_prediction": "P55",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": U_MIN,
                "bound_max": U_MAX,
                "min_observed": min(u_vals) if u_vals else None,
                "max_observed": max(u_vals) if u_vals else None,
            },
        },
        {
            "id": "RC52",
            "claim": (
                "Absolute headroom envelope: "
                f"{H_MIN} <= C_dyn - D <= {H_MAX} "
                "on util maxima + o_q panel "
                "(integer remaining budget to S1* breach line)."
            ),
            "status": "holds" if p56_holds else "falsified",
            "linked_prediction": "P56",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": H_MIN,
                "bound_max": H_MAX,
                "min_observed": min(h_vals) if h_vals else None,
                "max_observed": max(h_vals) if h_vals else None,
            },
        },
        {
            "id": "RC53",
            "claim": (
                "High-pressure locus: if u >= "
                f"{HIGH_U_THRESH} on the panel, then o_q = 6 and "
                f"|D-540| >= {HIGH_U_ABS_D_MIN} "
                "(high util sits outside historical 540 cluster)."
            ),
            "status": "holds" if p57_holds else "falsified",
            "linked_prediction": "P57",
            "evidence": {
                "high_u_rows": high_u_rows,
                "high_u_thresh": HIGH_U_THRESH,
                "require_o_q": 6,
                "require_abs_d_min": HIGH_U_ABS_D_MIN,
                "unique_chamber_count": len(unique_rows),
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
                "proximity_slack_u": 0.9341772151898734,
            },
        },
        {
            "id": "RC48_RC50_retained",
            "claim": (
                "Prior residual RC48-RC50 (tight_frac, desert_pos, large_frac) "
                "retained as measured holds; not re-proved as primary surface."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P52-P54 (prior)",
            "evidence": rc48_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc48_prediction_table": (
                str(args.rc48_table) if args.rc48_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "u_min": U_MIN,
            "u_max": U_MAX,
            "h_min": H_MIN,
            "h_max": H_MAX,
            "high_u_thresh": HIGH_U_THRESH,
            "high_u_abs_d_min": HIGH_U_ABS_D_MIN,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-square proximity / Target S1* (u<=1 for all selected "
                "square roots; Annulus emptiness) remains unresolved in "
                "PROOF.md section Square-Branch Reduction; residual audit "
                "only. Direct next-prime and Interior Maximizer remain proved. "
                "Panel envelope u<=0.98 is not S1*."
            ),
            "geometry_note": (
                "RC51-RC53 measure endpoint budget D vs C_dyn(q) and where "
                "high utilization sits relative to historical offset 540. "
                "Not Tau4 multiset occupancy (RC48-RC50). Not Dual/density "
                "renorms (RC3-RC47). C_dyn from gwr_dni_recursive_walk."
                "dynamic_cutoff(previous_prime), matching the search script."
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC51_proximity_utilization_envelope": (
                "holds" if p55_holds else "falsified"
            ),
            "RC52_absolute_headroom_envelope": (
                "holds" if p56_holds else "falsified"
            ),
            "RC53_high_pressure_locus": "holds" if p57_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC48_RC50_multiset": "holds (retained; not primary surface)",
            "u_range_unique_chambers": (
                [min(u_vals), max(u_vals)] if u_vals else None
            ),
            "h_range_unique_chambers": (
                [min(h_vals), max(h_vals)] if h_vals else None
            ),
            "unique_chamber_count": len(unique_rows),
            "surface_row_count": len(evaluated),
            "high_u_rows": high_u_rows,
            "target_S1_star": "UNRESOLVED",
            "advance_over_prior_hour": (
                "New residual object class: proximity utilization u=D/C_dyn "
                "and headroom h=C-D on the util-max + o_q panel; high-pressure "
                "locus ties u>=0.85 to o_q=6 far from 540. Distinct from "
                "RC48-RC50 MultisetOccupancy and from Dual/density ladder."
            ),
            "d4_sda_revived": False,
            "prefix_tau_d4_sda_transfers": (
                prefix_tau_note.get("d4_sda_transfers") if prefix_tau_note else None
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-16-rc51/"
            "offset_540_residual_rc51_probe.py"
        ),
        "s1_star_primary_falsifier": (
            "python3 research/04-bounded-compression/scripts/"
            "square_branch_dynamic_cutoff_search.py "
            "--min-prime 500000001 --max-prime 600000000 "
            "--output-dir research/04-bounded-compression/output/"
            "square_branch_dynamic_cutoff_search_5e8_6e8"
        ),
    }

    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload["conclusion"], indent=2))
    print("residual_claims:")
    for claim in residual_claims:
        print(f"  {claim['id']}: {claim['status']}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
