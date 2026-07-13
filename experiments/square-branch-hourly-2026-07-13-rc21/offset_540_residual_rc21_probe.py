#!/usr/bin/env python3
"""Residual chamber claims RC21-RC23: tau4 density, Dual max-share, near-540 floor.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual(r) = (first_tau4_offset, trail_gap) with
    trail_gap = D(r) - last_tau4_offset
  - late-tau3 landing at first_tau3_offset = D(r)

Prior residual surface ended at RC18-RC20 (Dual L1 absolute/relative and tau4
span fraction). This probe does not restate those as the primary deliverable.
It states and checks the next residual claims on segment utilization maxima
through 4e8-5e8 and the full o_q branch-max panel:

  P25 / RC21: Tau4 density envelope
              0.10 <= tau4_count / (D - 1) <= 0.135
  P26 / RC22: Dual max-component share
              max(first_tau4, trail_gap) / Dual L1 <= 0.85
  P27 / RC23: Near-540 Dual L1 floor (conditional residual)
              if |D - 540| <= 20 then Dual L1 >= 14

Structural reading: early tau=4 and late trail form a Dual whose mass is not
monopolized by one side, while tau4 hits the chamber at a stable density.
Recurring offset 540 is not a law for D(r) (RC2 remains falsified); near-540
rows instead carry an elevated Dual L1 floor. d=4 SDA is not revived.

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
RC18_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-11-rc18"
    / "offset_540_rc18_prediction_table.json"
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

TAU4_DENSITY_MIN = 0.10
TAU4_DENSITY_MAX = 0.135
DUAL_MAX_SHARE_MAX = 0.85
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20
NEAR_540_DUAL_L1_MIN = 14

PREDICTIONS = [
    {
        "id": "P25",
        "name": "tau4_density_envelope",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, tau4 density "
            f"tau4_count / (D(r) - 1) lies in "
            f"[{TAU4_DENSITY_MIN}, {TAU4_DENSITY_MAX}]."
        ),
        "falsifier": (
            "any evaluated row with tau4_density < "
            f"{TAU4_DENSITY_MIN} or tau4_density > {TAU4_DENSITY_MAX}"
        ),
    },
    {
        "id": "P26",
        "name": "dual_max_component_share",
        "statement": (
            "On the same surface, Dual max-component share "
            "max(first_tau4_offset, trail_gap) / Dual L1 "
            f"satisfies share <= {DUAL_MAX_SHARE_MAX} "
            "(early and late markers do not monopolize Dual)."
        ),
        "falsifier": (
            f"any evaluated row with dual_max_share > {DUAL_MAX_SHARE_MAX}"
        ),
    },
    {
        "id": "P27",
        "name": "near_540_dual_l1_floor",
        "statement": (
            "On the same surface, if |D(r) - 540| <= "
            f"{NEAR_540_RADIUS}, then Dual L1 = first_tau4_offset + trail_gap "
            f">= {NEAR_540_DUAL_L1_MIN} (conditional residual on the "
            "recurring-540 band; not a universal offset law for D)."
        ),
        "falsifier": (
            "any near-540 row (|D-540|<="
            f"{NEAR_540_RADIUS}) with dual_l1 < {NEAR_540_DUAL_L1_MIN}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, density, and max-share inside the chamber.

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
            "tau4_density": 0.0 if d > 1 else None,
            "dual_max_share": None,
            "prefix_min_tau": prefix_min_tau,
            "tau3_in_prefix": tau3_in_prefix,
            "abs_d_minus_540": abs(d - NEAR_540_CENTER),
            "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        }

    first_tau4 = tau4_offs[0]
    last_tau4 = tau4_offs[-1]
    trail_gap = d - last_tau4
    dual_l1 = first_tau4 + trail_gap
    tau4_density = len(tau4_offs) / (d - 1) if d > 1 else None
    dual_max_share = max(first_tau4, trail_gap) / dual_l1 if dual_l1 > 0 else None
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": first_tau4,
        "last_tau4_offset": last_tau4,
        "first_tau3_offset": d,
        "trail_gap": trail_gap,
        "dual_l1": dual_l1,
        "tau4_density": tau4_density,
        "dual_max_share": dual_max_share,
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
        "tau4_density": row["tau4_density"],
        "dual_max_share": row["dual_max_share"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p25(row: dict) -> dict:
    dens = row["tau4_density"]
    passed = (
        dens is not None
        and float(dens) >= TAU4_DENSITY_MIN
        and float(dens) <= TAU4_DENSITY_MAX
    )
    return {
        "id": "P25",
        "name": "tau4_density_envelope",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "tau4_density": dens,
            "bound_min": TAU4_DENSITY_MIN,
            "bound_max": TAU4_DENSITY_MAX,
            "tau4_count": row["tau4_count"],
            "D": row["offset"],
        },
    }


def evaluate_p26(row: dict) -> dict:
    share = row["dual_max_share"]
    passed = share is not None and float(share) <= DUAL_MAX_SHARE_MAX
    return {
        "id": "P26",
        "name": "dual_max_component_share",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_max_share": share,
            "bound": DUAL_MAX_SHARE_MAX,
            "first_tau4_offset": row["first_tau4_offset"],
            "trail_gap": row["trail_gap"],
            "dual_l1": row["dual_l1"],
            "D": row["offset"],
        },
    }


def evaluate_p27(row: dict) -> dict | None:
    """Conditional residual: only evaluated on near-540 rows."""
    if not row["near_540"]:
        return {
            "id": "P27",
            "name": "near_540_dual_l1_floor",
            "statement": PREDICTIONS[2]["statement"],
            "falsifier": PREDICTIONS[2]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "not_applicable",
            "detail": {
                "near_540": False,
                "abs_d_minus_540": row["abs_d_minus_540"],
                "dual_l1": row["dual_l1"],
                "bound": NEAR_540_DUAL_L1_MIN,
            },
        }
    dual_l1 = row["dual_l1"]
    passed = dual_l1 is not None and int(dual_l1) >= NEAR_540_DUAL_L1_MIN
    return {
        "id": "P27",
        "name": "near_540_dual_l1_floor",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "near_540": True,
            "abs_d_minus_540": row["abs_d_minus_540"],
            "dual_l1": dual_l1,
            "bound": NEAR_540_DUAL_L1_MIN,
            "first_tau4_offset": row["first_tau4_offset"],
            "trail_gap": row["trail_gap"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC21-RC23 residual chamber probe "
            "(tau4 density, Dual max-share, near-540 Dual L1 floor)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc18-table", type=Path, default=RC18_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc21_prediction_table.json",
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

    rc18_note = None
    if args.rc18_table.is_file():
        rc18 = json.loads(args.rc18_table.read_text(encoding="utf-8"))
        rc18_note = {
            "path": str(args.rc18_table),
            "conclusion": rc18.get("conclusion"),
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
        "recomputing tau4 density / Dual max-share / near-540 Dual floor "
        "on primary + o_q panel...",
        flush=True,
    )
    primary_rows = [enrich_row(row) for row in primary_src]
    oq_rows = [enrich_row(row) for row in oq_src]
    evaluated = primary_rows + oq_rows

    # Guard: prefix must have no tau=3 (late landing only at D).
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

    p25_results = [evaluate_p25(row) for row in evaluated]
    p26_results = [evaluate_p26(row) for row in evaluated]
    p27_results = [evaluate_p27(row) for row in evaluated]
    all_results = p25_results + p26_results + p27_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p25_holds = holds(p25_results)
    p26_holds = holds(p26_results)
    p27_holds = holds(p27_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    densities = [
        float(r["tau4_density"]) for r in evaluated if r["tau4_density"] is not None
    ]
    shares = [
        float(r["dual_max_share"]) for r in evaluated if r["dual_max_share"] is not None
    ]
    dual_l1s = [int(r["dual_l1"]) for r in evaluated if r["dual_l1"] is not None]
    near_dual_l1s = [int(r["dual_l1"]) for r in near_rows if r["dual_l1"] is not None]

    residual_claims = [
        {
            "id": "RC21",
            "claim": (
                "Tau4 density envelope: on segment utilization maxima through "
                f"4e8-5e8 and the full o_q branch-max panel, "
                f"{TAU4_DENSITY_MIN} <= tau4_count/(D-1) <= {TAU4_DENSITY_MAX}."
            ),
            "status": "holds" if p25_holds else "falsified",
            "linked_prediction": "P25",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound_min": TAU4_DENSITY_MIN,
                "bound_max": TAU4_DENSITY_MAX,
                "min_observed": min(densities) if densities else None,
                "max_observed": max(densities) if densities else None,
            },
        },
        {
            "id": "RC22",
            "claim": (
                "Dual max-component share: "
                f"max(first_tau4, trail_gap) / Dual L1 <= {DUAL_MAX_SHARE_MAX} "
                "on util maxima + o_q panel."
            ),
            "status": "holds" if p26_holds else "falsified",
            "linked_prediction": "P26",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": DUAL_MAX_SHARE_MAX,
                "min_observed": min(shares) if shares else None,
                "max_observed": max(shares) if shares else None,
            },
        },
        {
            "id": "RC23",
            "claim": (
                "Near-540 Dual L1 floor: if |D-540| <= "
                f"{NEAR_540_RADIUS}, then Dual L1 >= {NEAR_540_DUAL_L1_MIN} "
                "(conditional residual; RC2 fixed-band law remains falsified)."
            ),
            "status": "holds" if p27_holds else "falsified",
            "linked_prediction": "P27",
            "evidence": {
                "near_540_rows": [_compact(r) for r in near_rows],
                "bound": NEAR_540_DUAL_L1_MIN,
                "near_540_count": len(near_rows),
                "min_observed": min(near_dual_l1s) if near_dual_l1s else None,
                "max_observed": max(near_dual_l1s) if near_dual_l1s else None,
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
            "id": "RC18_RC20_retained",
            "claim": (
                "Prior residual RC18-RC20 (Dual L1 envelope, tau4 span fraction, "
                "relative Dual L1) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P22-P24 (prior)",
            "evidence": rc18_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc18_prediction_table": (
                str(args.rc18_table) if args.rc18_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "tau4_density_min": TAU4_DENSITY_MIN,
            "tau4_density_max": TAU4_DENSITY_MAX,
            "dual_max_share_max": DUAL_MAX_SHARE_MAX,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "near_540_dual_l1_min": NEAR_540_DUAL_L1_MIN,
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
            "RC21_tau4_density_envelope": "holds" if p25_holds else "falsified",
            "RC22_dual_max_component_share": (
                "holds" if p26_holds else "falsified"
            ),
            "RC23_near_540_dual_l1_floor": "holds" if p27_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC18_RC20": "retained holds (not primary surface)",
            "tau4_density_range": (
                [min(densities), max(densities)] if densities else None
            ),
            "dual_max_share_range": (
                [min(shares), max(shares)] if shares else None
            ),
            "dual_l1_range": (
                [min(dual_l1s), max(dual_l1s)] if dual_l1s else None
            ),
            "near_540_count": len(near_rows),
            "near_540_dual_l1_range": (
                [min(near_dual_l1s), max(near_dual_l1s)] if near_dual_l1s else None
            ),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC21-RC23: tau4 density envelope, "
                "Dual max-component share (early/late non-monopoly), and "
                "near-540 Dual L1 floor; does not restate RC18-RC20 Dual L1 "
                "absolute/relative or span fraction as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-13-rc21/"
            "offset_540_residual_rc21_probe.py"
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
