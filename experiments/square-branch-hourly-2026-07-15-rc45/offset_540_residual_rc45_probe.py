#!/usr/bin/env python3
"""Residual chamber claims RC45-RC47: mean-floor packing, Dual-per-hit, peak body share.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual markers (first_tau4_offset, trail_gap) with late tau=3 at D
  - successive inter-hit gaps on the ordered Tau4 set
  - mean inter-hit gap on the Tau4 body
  - Dual L1 isolation dual_l1 = first_tau4 + trail_gap
  - Tau4 body span tau4_body = last_tau4 - first_tau4

Prior residual surface ended at RC42-RC44 (min/median, max/min, dual/max_gap).
This probe does not restate those as the primary deliverable. It states and
checks the next residual claims on segment utilization maxima through
4e8-5e8 and the full o_q branch-max panel:

  P49 / RC45: Floor packing of successive Tau4 gaps in mean units
              0.08 <= min_gap / mean_gap <= 0.30
  P50 / RC46: Dual L1 isolation density per Tau4 hit
              0.05 <= dual_l1 / tau4_count <= 0.50
  P51 / RC47: Peak interior desert as share of Tau4 body span
              0.03 <= max_gap / tau4_body <= 0.12

Structural reading: early tau=4 opens the chamber; late tau=3 closes at D.
RC42-RC44 bound interior packing floor (median), dynamic range, and Dual
vs peak desert. RC45 places the packing floor in mean units. RC46 bounds
Dual isolation per Tau4 hit (mass-normalized Dual). RC47 bounds peak desert
as a fraction of Tau4 body support (not of D, not of min).

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
RC42_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-14-rc42"
    / "offset_540_rc42_prediction_table.json"
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

MIN_OVER_MEAN_MIN = 0.08
MIN_OVER_MEAN_MAX = 0.30
DUAL_PER_HIT_MIN = 0.05
DUAL_PER_HIT_MAX = 0.50
MAX_OVER_BODY_MIN = 0.03
MAX_OVER_BODY_MAX = 0.12
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P49",
        "name": "successive_tau4_floor_over_mean",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            "o_q branch-max panel, the floor packing ratio "
            "min_successive_gap / mean_gap satisfies "
            f"{MIN_OVER_MEAN_MIN} <= min_gap / mean_gap <= "
            f"{MIN_OVER_MEAN_MAX} (mean-unit packing floor; not min/median "
            "RC42; not max/mean RC27)."
        ),
        "falsifier": (
            "any evaluated row with min_over_mean < "
            f"{MIN_OVER_MEAN_MIN} or min_over_mean > {MIN_OVER_MEAN_MAX}"
        ),
    },
    {
        "id": "P50",
        "name": "dual_l1_per_tau4_hit",
        "statement": (
            "On the same surface, Dual L1 isolation density dual_l1 / "
            "tau4_count satisfies "
            f"{DUAL_PER_HIT_MIN} <= dual_l1 / tau4_count <= "
            f"{DUAL_PER_HIT_MAX} (mass-normalized Dual; not dual/max_gap "
            "RC44; not dual/median RC41; not density RC21)."
        ),
        "falsifier": (
            "any evaluated row with dual_per_hit < "
            f"{DUAL_PER_HIT_MIN} or dual_per_hit > {DUAL_PER_HIT_MAX}"
        ),
    },
    {
        "id": "P51",
        "name": "peak_desert_body_share",
        "statement": (
            "On the same surface, peak interior Tau4 desert as a share of "
            "Tau4 body span max_successive_gap / tau4_body satisfies "
            f"{MAX_OVER_BODY_MIN} <= max_gap / tau4_body <= "
            f"{MAX_OVER_BODY_MAX} (body-support relative desert; not "
            "max/D RC11; not max/min RC43)."
        ),
        "falsifier": (
            "any evaluated row with max_over_body < "
            f"{MAX_OVER_BODY_MIN} or max_over_body > {MAX_OVER_BODY_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers and RC45-RC47 residual ratios.

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
        "min_over_mean": None,
        "dual_per_hit": None,
        "max_over_body": None,
        "min_over_median": None,
        "max_over_min": None,
        "dual_over_max_gap": None,
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
    domain_ok = (
        mean_gap > 0
        and min_gap > 0
        and max_gap > 0
        and tau4_body > 0
        and len(tau4_offs) > 0
    )
    min_over_mean = (min_gap / mean_gap) if domain_ok else None
    dual_per_hit = (dual_l1 / len(tau4_offs)) if domain_ok else None
    max_over_body = (max_gap / tau4_body) if domain_ok else None
    min_over_median = (min_gap / median_gap) if median_gap > 0 else None
    max_over_min = (max_gap / min_gap) if min_gap > 0 else None
    dual_over_max_gap = (dual_l1 / max_gap) if max_gap > 0 else None
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
        "min_over_mean": min_over_mean,
        "dual_per_hit": dual_per_hit,
        "max_over_body": max_over_body,
        "min_over_median": min_over_median,
        "max_over_min": max_over_min,
        "dual_over_max_gap": dual_over_max_gap,
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
        "min_over_mean": row["min_over_mean"],
        "dual_per_hit": row["dual_per_hit"],
        "max_over_body": row["max_over_body"],
        "min_over_median": row["min_over_median"],
        "max_over_min": row["max_over_min"],
        "dual_over_max_gap": row["dual_over_max_gap"],
        "tau4_density": row["tau4_density"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
        "domain_ok": row["domain_ok"],
    }


def evaluate_p49(row: dict) -> dict:
    ratio = row["min_over_mean"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P49",
            "name": "successive_tau4_floor_over_mean",
            "statement": PREDICTIONS[0]["statement"],
            "falsifier": PREDICTIONS[0]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive gaps/mean",
                "min_over_mean": ratio,
            },
        }
    passed = float(ratio) >= MIN_OVER_MEAN_MIN and float(ratio) <= MIN_OVER_MEAN_MAX
    return {
        "id": "P49",
        "name": "successive_tau4_floor_over_mean",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "min_over_mean": ratio,
            "bound_min": MIN_OVER_MEAN_MIN,
            "bound_max": MIN_OVER_MEAN_MAX,
            "min_successive_gap": row["min_successive_gap"],
            "mean_gap": row["mean_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p50(row: dict) -> dict:
    ratio = row["dual_per_hit"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P50",
            "name": "dual_l1_per_tau4_hit",
            "statement": PREDICTIONS[1]["statement"],
            "falsifier": PREDICTIONS[1]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive dual",
                "dual_per_hit": ratio,
            },
        }
    passed = float(ratio) >= DUAL_PER_HIT_MIN and float(ratio) <= DUAL_PER_HIT_MAX
    return {
        "id": "P50",
        "name": "dual_l1_per_tau4_hit",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_per_hit": ratio,
            "bound_min": DUAL_PER_HIT_MIN,
            "bound_max": DUAL_PER_HIT_MAX,
            "dual_l1": row["dual_l1"],
            "tau4_count": row["tau4_count"],
            "D": row["offset"],
        },
    }


def evaluate_p51(row: dict) -> dict:
    ratio = row["max_over_body"]
    if ratio is None or not row.get("domain_ok"):
        return {
            "id": "P51",
            "name": "peak_desert_body_share",
            "statement": PREDICTIONS[2]["statement"],
            "falsifier": PREDICTIONS[2]["falsifier"],
            "segment": row.get("segment"),
            "r": row["r"],
            "offset": row["offset"],
            "o_q": row.get("o_q"),
            "pass": None,
            "status": "unresolved",
            "detail": {
                "reason": "domain gate: need |Tau4|>=2 and positive body/max",
                "max_over_body": ratio,
            },
        }
    passed = float(ratio) >= MAX_OVER_BODY_MIN and float(ratio) <= MAX_OVER_BODY_MAX
    return {
        "id": "P51",
        "name": "peak_desert_body_share",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "max_over_body": ratio,
            "bound_min": MAX_OVER_BODY_MIN,
            "bound_max": MAX_OVER_BODY_MAX,
            "max_successive_gap": row["max_successive_gap"],
            "tau4_body": row["tau4_body"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC45-RC47 residual chamber probe "
            "(min/mean floor, dual/count density, max/body desert share)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc42-table", type=Path, default=RC42_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc45_prediction_table.json",
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

    rc42_note = None
    if args.rc42_table.is_file():
        rc42 = json.loads(args.rc42_table.read_text(encoding="utf-8"))
        rc42_note = {
            "path": str(args.rc42_table),
            "conclusion": {
                k: rc42.get("conclusion", {}).get(k)
                for k in (
                    "RC42_successive_floor_over_median",
                    "RC43_successive_dynamic_range",
                    "RC44_dual_over_peak_interior_desert",
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
        "recomputing min/mean, dual/count, max/body "
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

    p49_results = [evaluate_p49(row) for row in evaluated]
    p50_results = [evaluate_p50(row) for row in evaluated]
    p51_results = [evaluate_p51(row) for row in evaluated]
    all_results = p49_results + p50_results + p51_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p49_holds = holds(p49_results)
    p50_holds = holds(p50_results)
    p51_holds = holds(p51_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    unique_by_r: dict[int, dict] = {}
    for row in evaluated:
        unique_by_r[int(row["r"])] = row
    unique_rows = list(unique_by_r.values())

    min_over_means = [
        float(r["min_over_mean"])
        for r in unique_rows
        if r["min_over_mean"] is not None
    ]
    dual_per_hits = [
        float(r["dual_per_hit"])
        for r in unique_rows
        if r["dual_per_hit"] is not None
    ]
    max_over_bodies = [
        float(r["max_over_body"])
        for r in unique_rows
        if r["max_over_body"] is not None
    ]

    residual_claims = [
        {
            "id": "RC45",
            "claim": (
                "Floor packing of successive Tau4 gaps in mean units: on "
                "segment utilization maxima through 4e8-5e8 and the full "
                "o_q branch-max panel, "
                f"{MIN_OVER_MEAN_MIN} <= min_successive_gap / mean_gap <= "
                f"{MIN_OVER_MEAN_MAX}."
            ),
            "status": "holds" if p49_holds else "falsified",
            "linked_prediction": "P49",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": MIN_OVER_MEAN_MIN,
                "bound_max": MIN_OVER_MEAN_MAX,
                "min_observed": min(min_over_means) if min_over_means else None,
                "max_observed": max(min_over_means) if min_over_means else None,
            },
        },
        {
            "id": "RC46",
            "claim": (
                "Dual L1 isolation density per Tau4 hit: "
                f"{DUAL_PER_HIT_MIN} <= dual_l1 / tau4_count <= "
                f"{DUAL_PER_HIT_MAX} on util maxima + o_q panel "
                "(mass-normalized Dual; not dual/max_gap or dual/median)."
            ),
            "status": "holds" if p50_holds else "falsified",
            "linked_prediction": "P50",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": DUAL_PER_HIT_MIN,
                "bound_max": DUAL_PER_HIT_MAX,
                "min_observed": min(dual_per_hits) if dual_per_hits else None,
                "max_observed": max(dual_per_hits) if dual_per_hits else None,
            },
        },
        {
            "id": "RC47",
            "claim": (
                "Peak interior Tau4 desert as share of Tau4 body span: "
                f"{MAX_OVER_BODY_MIN} <= max_successive_gap / tau4_body <= "
                f"{MAX_OVER_BODY_MAX} on util maxima + o_q panel "
                "(body-support relative desert; not max/D or max/min)."
            ),
            "status": "holds" if p51_holds else "falsified",
            "linked_prediction": "P51",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "unique_chamber_count": len(unique_rows),
                "bound_min": MAX_OVER_BODY_MIN,
                "bound_max": MAX_OVER_BODY_MAX,
                "min_observed": min(max_over_bodies) if max_over_bodies else None,
                "max_observed": max(max_over_bodies) if max_over_bodies else None,
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
            "id": "RC42_RC44_retained",
            "claim": (
                "Prior residual RC42-RC44 (min/median, max/min, dual/max_gap) "
                "retained as measured holds; not re-proved as primary surface."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P46-P48 (prior)",
            "evidence": rc42_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc42_prediction_table": (
                str(args.rc42_table) if args.rc42_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "min_over_mean_min": MIN_OVER_MEAN_MIN,
            "min_over_mean_max": MIN_OVER_MEAN_MAX,
            "dual_per_hit_min": DUAL_PER_HIT_MIN,
            "dual_per_hit_max": DUAL_PER_HIT_MAX,
            "max_over_body_min": MAX_OVER_BODY_MIN,
            "max_over_body_max": MAX_OVER_BODY_MAX,
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
            "RC45_successive_floor_over_mean": (
                "holds" if p49_holds else "falsified"
            ),
            "RC46_dual_l1_per_tau4_hit": (
                "holds" if p50_holds else "falsified"
            ),
            "RC47_peak_desert_body_share": (
                "holds" if p51_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC42_RC44": "retained holds (not primary surface)",
            "min_over_mean_range": (
                [min(min_over_means), max(min_over_means)]
                if min_over_means
                else None
            ),
            "dual_per_hit_range": (
                [min(dual_per_hits), max(dual_per_hits)]
                if dual_per_hits
                else None
            ),
            "max_over_body_range": (
                [min(max_over_bodies), max(max_over_bodies)]
                if max_over_bodies
                else None
            ),
            "unique_chamber_count": len(unique_rows),
            "surface_row_count": len(evaluated),
            "near_540_count": len(near_rows),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC45-RC47: mean-unit Tau4 packing "
                "floor (min/mean), Dual L1 per Tau4 hit (dual/count), and "
                "peak desert as Tau4 body-share (max/body); does not restate "
                "RC42-RC44 min/median, max/min, dual/max_gap as sole "
                "deliverable; does not revive fixed-band 540 or d=4 SDA."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-15-rc45/"
            "offset_540_residual_rc45_probe.py"
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
