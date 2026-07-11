#!/usr/bin/env python3
"""Residual chamber claims RC15-RC17: early-tau4 / late-tau3 dual markers.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - late-tau3 landing at first_tau3_offset = D(r)
  - trail gap from last tau4 support to the late tau3 endpoint

Prior residual surface ended at RC12-RC14 (quartile mass / median). This probe
does not replay P1-P18 as the primary deliverable. It states and checks the
next residual claims on segment utilization maxima through 4e8-5e8 and the
full o_q branch-max panel:

  P19 / RC15: late-tau3 trail tightness
              1 <= trail_gap = D - last_tau4_offset <= 24
  P20 / RC16: absolute early tau4 on full panel
              first_tau4_offset <= 16
  P21 / RC17: near-540 dual marker (conditional residual)
              if |D - 540| <= 20 then first_tau4_offset <= 10
              and trail_gap <= 20

Structural reading: early tau=4 opens the chamber; late tau=3 closes it at
the selected square; the trail between last tau4 and D is short. Recurring
offset 540, when it reappears, tightens both early and late markers. Fixed
band RC2 remains falsified; d=4 SDA is not revived.

Audit-only. Does not choose primes as PGS inference.
Prime-Square Proximity Theorem remains proved in PROOF.md; residual audit only.
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
RC12_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-11-rc12"
    / "offset_540_rc12_prediction_table.json"
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

TRAIL_GAP_MAX = 24
FIRST_TAU4_PANEL_MAX = 16
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20
NEAR_540_FIRST_TAU4_MAX = 10
NEAR_540_TRAIL_MAX = 20

PREDICTIONS = [
    {
        "id": "P19",
        "name": "late_tau3_trail_tightness",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            f"o_q branch-max panel, trail_gap = D(r) - last_tau4_offset "
            f"satisfies 1 <= trail_gap <= {TRAIL_GAP_MAX} "
            "(tau4 support ends tightly before late tau3 at D)."
        ),
        "falsifier": (
            f"any evaluated row with trail_gap < 1 or trail_gap > {TRAIL_GAP_MAX}"
        ),
    },
    {
        "id": "P20",
        "name": "absolute_early_tau4_full_panel",
        "statement": (
            "On the same surface (util maxima + full o_q panel), "
            f"first_tau4_offset <= {FIRST_TAU4_PANEL_MAX}."
        ),
        "falsifier": (
            f"any evaluated row with first_tau4_offset > {FIRST_TAU4_PANEL_MAX}"
        ),
    },
    {
        "id": "P21",
        "name": "near_540_dual_marker",
        "statement": (
            f"On the same surface, if |D(r) - {NEAR_540_CENTER}| "
            f"<= {NEAR_540_RADIUS}, then first_tau4_offset "
            f"<= {NEAR_540_FIRST_TAU4_MAX} and trail_gap "
            f"<= {NEAR_540_TRAIL_MAX} (conditional residual on the "
            "recurring-540 band; not a universal offset law)."
        ),
        "falsifier": (
            f"any near-540 row (|D-540|<={NEAR_540_RADIUS}) with "
            f"first_tau4_offset > {NEAR_540_FIRST_TAU4_MAX} or "
            f"trail_gap > {NEAR_540_TRAIL_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute early-tau4 / late-tau3 dual markers inside the chamber.

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
            "prefix_min_tau": prefix_min_tau,
            "tau3_in_prefix": tau3_in_prefix,
            "abs_d_minus_540": abs(d - NEAR_540_CENTER),
            "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        }

    first_tau4 = tau4_offs[0]
    last_tau4 = tau4_offs[-1]
    trail_gap = d - last_tau4
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": first_tau4,
        "last_tau4_offset": last_tau4,
        "first_tau3_offset": d,
        "trail_gap": trail_gap,
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
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p19(row: dict) -> dict:
    trail = row["trail_gap"]
    passed = trail is not None and 1 <= int(trail) <= TRAIL_GAP_MAX
    return {
        "id": "P19",
        "name": "late_tau3_trail_tightness",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "trail_gap": trail,
            "bound": [1, TRAIL_GAP_MAX],
            "last_tau4_offset": row["last_tau4_offset"],
            "first_tau3_offset": row["first_tau3_offset"],
            "D": row["offset"],
        },
    }


def evaluate_p20(row: dict) -> dict:
    first = row["first_tau4_offset"]
    passed = first is not None and int(first) <= FIRST_TAU4_PANEL_MAX
    return {
        "id": "P20",
        "name": "absolute_early_tau4_full_panel",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "first_tau4_offset": first,
            "bound": FIRST_TAU4_PANEL_MAX,
        },
    }


def evaluate_p21(row: dict) -> dict:
    near = bool(row["near_540"])
    first = row["first_tau4_offset"]
    trail = row["trail_gap"]
    if not near:
        return {
            "id": "P21",
            "name": "near_540_dual_marker",
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
                "first_tau4_offset": first,
                "trail_gap": trail,
            },
        }
    passed = (
        first is not None
        and trail is not None
        and int(first) <= NEAR_540_FIRST_TAU4_MAX
        and int(trail) <= NEAR_540_TRAIL_MAX
    )
    return {
        "id": "P21",
        "name": "near_540_dual_marker",
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
            "first_tau4_offset": first,
            "first_tau4_bound": NEAR_540_FIRST_TAU4_MAX,
            "trail_gap": trail,
            "trail_bound": NEAR_540_TRAIL_MAX,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC15-RC17 residual chamber probe "
            "(late-tau3 trail, absolute early tau4, near-540 dual marker)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc12-table", type=Path, default=RC12_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc15_prediction_table.json",
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

    rc12_note = None
    if args.rc12_table.is_file():
        rc12 = json.loads(args.rc12_table.read_text(encoding="utf-8"))
        rc12_note = {
            "path": str(args.rc12_table),
            "conclusion": rc12.get("conclusion"),
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
        "recomputing early-tau4 / late-tau3 dual markers on primary + o_q panel...",
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

    p19_results = [evaluate_p19(row) for row in evaluated]
    p20_results = [evaluate_p20(row) for row in evaluated]
    p21_results = [evaluate_p21(row) for row in evaluated]
    all_results = p19_results + p20_results + p21_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p19_holds = holds(p19_results)
    p20_holds = holds(p20_results)
    p21_holds = holds(p21_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    trails = [int(r["trail_gap"]) for r in evaluated if r["trail_gap"] is not None]
    firsts = [
        int(r["first_tau4_offset"])
        for r in evaluated
        if r["first_tau4_offset"] is not None
    ]
    near_trails = [int(r["trail_gap"]) for r in near_rows]
    near_firsts = [int(r["first_tau4_offset"]) for r in near_rows]

    residual_claims = [
        {
            "id": "RC15",
            "claim": (
                "Late-tau3 trail tightness: on segment utilization maxima "
                f"through 4e8-5e8 and the full o_q branch-max panel, "
                f"trail_gap = D - last_tau4_offset satisfies "
                f"1 <= trail_gap <= {TRAIL_GAP_MAX}."
            ),
            "status": "holds" if p19_holds else "falsified",
            "linked_prediction": "P19",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": [1, TRAIL_GAP_MAX],
                "min_observed": min(trails) if trails else None,
                "max_observed": max(trails) if trails else None,
            },
        },
        {
            "id": "RC16",
            "claim": (
                "Absolute early tau4 on full panel: first_tau4_offset "
                f"<= {FIRST_TAU4_PANEL_MAX} on util maxima + o_q panel "
                "(tightens RC4's util-only bound of 20 and extends coverage)."
            ),
            "status": "holds" if p20_holds else "falsified",
            "linked_prediction": "P20",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": FIRST_TAU4_PANEL_MAX,
                "max_observed": max(firsts) if firsts else None,
            },
        },
        {
            "id": "RC17",
            "claim": (
                f"Near-540 dual marker: if |D - {NEAR_540_CENTER}| "
                f"<= {NEAR_540_RADIUS}, then first_tau4_offset "
                f"<= {NEAR_540_FIRST_TAU4_MAX} and trail_gap "
                f"<= {NEAR_540_TRAIL_MAX}. Conditional residual on the "
                "recurring-540 band; not a universal offset law. RC2 remains "
                "falsified on utilization maxima."
            ),
            "status": "holds" if p21_holds else "falsified",
            "linked_prediction": "P21",
            "evidence": {
                "near_540_rows": [_compact(r) for r in near_rows],
                "near_540_count": len(near_rows),
                "first_tau4_bound": NEAR_540_FIRST_TAU4_MAX,
                "trail_bound": NEAR_540_TRAIL_MAX,
                "max_first_tau4_on_near_540": (
                    max(near_firsts) if near_firsts else None
                ),
                "max_trail_on_near_540": (
                    max(near_trails) if near_trails else None
                ),
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
            "id": "RC12_RC14_retained",
            "claim": (
                "Prior residual RC12-RC14 (first/last-quarter mass, median "
                "mid-band) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P16-P18 (prior)",
            "evidence": rc12_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc12_prediction_table": (
                str(args.rc12_table) if args.rc12_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "trail_gap_max": TRAIL_GAP_MAX,
            "first_tau4_panel_max": FIRST_TAU4_PANEL_MAX,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
            "near_540_first_tau4_max": NEAR_540_FIRST_TAU4_MAX,
            "near_540_trail_max": NEAR_540_TRAIL_MAX,
            "invalidated_route": "d=4 SDA transfer (not revived)",
            "theorem_status": (
                "Prime-Square Proximity proved in PROOF.md; residual audit only"
            ),
        },
        "predictions": PREDICTIONS,
        "primary_rows": primary_compact,
        "oq_panel_rows": oq_compact,
        "prediction_results": all_results,
        "residual_claims": residual_claims,
        "conclusion": {
            "RC15_late_tau3_trail_tightness": (
                "holds" if p19_holds else "falsified"
            ),
            "RC16_absolute_early_tau4_full_panel": (
                "holds" if p20_holds else "falsified"
            ),
            "RC17_near_540_dual_marker": "holds" if p21_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC12_RC14": "retained holds (not primary surface)",
            "trail_gap_range": (
                [min(trails), max(trails)] if trails else None
            ),
            "first_tau4_range": (
                [min(firsts), max(firsts)] if firsts else None
            ),
            "near_540_count": len(near_rows),
            "near_540_trail_range": (
                [min(near_trails), max(near_trails)] if near_trails else None
            ),
            "near_540_first_tau4_range": (
                [min(near_firsts), max(near_firsts)] if near_firsts else None
            ),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC15-RC17: late-tau3 trail "
                "tightness, absolute early tau4 on full util+o_q panel, "
                "and conditional near-540 dual early/late markers; does not "
                "restate RC12-RC14 as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-11-rc15/"
            "offset_540_residual_rc15_probe.py"
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
