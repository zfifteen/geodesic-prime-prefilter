#!/usr/bin/env python3
"""Residual chamber claims RC18-RC20: Dual L1 and tau4 span separation.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - Dual(r) = (first_tau4_offset, trail_gap) with
    trail_gap = D(r) - last_tau4_offset
  - late-tau3 landing at first_tau3_offset = D(r)

Prior residual surface ended at RC15-RC17 (componentwise dual markers).
This probe does not restate P19-P21 as the primary deliverable. It states and
checks the next residual claims on segment utilization maxima through
4e8-5e8 and the full o_q branch-max panel:

  P22 / RC18: Dual L1 envelope
              first_tau4_offset + trail_gap <= 24
  P23 / RC19: tau4 support span fraction
              (last_tau4 - first_tau4) / (D - 1) >= 0.95
  P24 / RC20: relative Dual L1 envelope
              (first_tau4_offset + trail_gap) / D <= 0.05

Structural reading: early tau=4 and late trail form a Dual whose absolute and
relative L1 sizes stay tight, while tau4 support spans almost the full chamber
prefix. Recurring offset 540 is not revived as a law (RC2 remains falsified).
d=4 SDA is not revived.

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
RC15_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-11-rc15"
    / "offset_540_rc15_prediction_table.json"
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

DUAL_L1_MAX = 24
SPAN_FRAC_MIN = 0.95
DUAL_L1_REL_MAX = 0.05
NEAR_540_CENTER = 540
NEAR_540_RADIUS = 20

PREDICTIONS = [
    {
        "id": "P22",
        "name": "dual_l1_envelope",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            f"o_q branch-max panel, Dual L1 = first_tau4_offset + trail_gap "
            f"satisfies Dual L1 <= {DUAL_L1_MAX} "
            "(early and late markers stay jointly tight)."
        ),
        "falsifier": (
            f"any evaluated row with first_tau4_offset + trail_gap > {DUAL_L1_MAX}"
        ),
    },
    {
        "id": "P23",
        "name": "tau4_support_span_fraction",
        "statement": (
            "On the same surface, tau4 support span fraction "
            "(last_tau4_offset - first_tau4_offset) / (D(r) - 1) "
            f">= {SPAN_FRAC_MIN} (tau4 support spans almost the full chamber)."
        ),
        "falsifier": (
            f"any evaluated row with span_frac < {SPAN_FRAC_MIN}"
        ),
    },
    {
        "id": "P24",
        "name": "relative_dual_l1_envelope",
        "statement": (
            "On the same surface, relative Dual L1 "
            f"(first_tau4_offset + trail_gap) / D(r) <= {DUAL_L1_REL_MAX}."
        ),
        "falsifier": (
            f"any evaluated row with (first_tau4 + trail_gap)/D > {DUAL_L1_REL_MAX}"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def early_late_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Dual markers, span, and relative Dual L1 inside the chamber.

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
            "span_frac": None,
            "dual_l1_rel": None,
            "prefix_min_tau": prefix_min_tau,
            "tau3_in_prefix": tau3_in_prefix,
            "abs_d_minus_540": abs(d - NEAR_540_CENTER),
            "near_540": abs(d - NEAR_540_CENTER) <= NEAR_540_RADIUS,
        }

    first_tau4 = tau4_offs[0]
    last_tau4 = tau4_offs[-1]
    trail_gap = d - last_tau4
    dual_l1 = first_tau4 + trail_gap
    span_frac = (last_tau4 - first_tau4) / (d - 1) if d > 1 else None
    dual_l1_rel = dual_l1 / d if d > 0 else None
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": first_tau4,
        "last_tau4_offset": last_tau4,
        "first_tau3_offset": d,
        "trail_gap": trail_gap,
        "dual_l1": dual_l1,
        "span_frac": span_frac,
        "dual_l1_rel": dual_l1_rel,
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
        "span_frac": row["span_frac"],
        "dual_l1_rel": row["dual_l1_rel"],
        "prefix_min_tau": row["prefix_min_tau"],
        "tau3_in_prefix": row["tau3_in_prefix"],
        "abs_d_minus_540": row["abs_d_minus_540"],
        "near_540": row["near_540"],
    }


def evaluate_p22(row: dict) -> dict:
    dual_l1 = row["dual_l1"]
    passed = dual_l1 is not None and int(dual_l1) <= DUAL_L1_MAX
    return {
        "id": "P22",
        "name": "dual_l1_envelope",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_l1": dual_l1,
            "bound": DUAL_L1_MAX,
            "first_tau4_offset": row["first_tau4_offset"],
            "trail_gap": row["trail_gap"],
            "D": row["offset"],
        },
    }


def evaluate_p23(row: dict) -> dict:
    span = row["span_frac"]
    passed = span is not None and float(span) >= SPAN_FRAC_MIN
    return {
        "id": "P23",
        "name": "tau4_support_span_fraction",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "span_frac": span,
            "bound": SPAN_FRAC_MIN,
            "first_tau4_offset": row["first_tau4_offset"],
            "last_tau4_offset": row["last_tau4_offset"],
            "D": row["offset"],
        },
    }


def evaluate_p24(row: dict) -> dict:
    rel = row["dual_l1_rel"]
    passed = rel is not None and float(rel) <= DUAL_L1_REL_MAX
    return {
        "id": "P24",
        "name": "relative_dual_l1_envelope",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "dual_l1_rel": rel,
            "bound": DUAL_L1_REL_MAX,
            "dual_l1": row["dual_l1"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC18-RC20 residual chamber probe "
            "(Dual L1 envelope, tau4 span fraction, relative Dual L1)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc15-table", type=Path, default=RC15_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc18_prediction_table.json",
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

    rc15_note = None
    if args.rc15_table.is_file():
        rc15 = json.loads(args.rc15_table.read_text(encoding="utf-8"))
        rc15_note = {
            "path": str(args.rc15_table),
            "conclusion": rc15.get("conclusion"),
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
        "recomputing Dual L1 / tau4 span on primary + o_q panel...",
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

    p22_results = [evaluate_p22(row) for row in evaluated]
    p23_results = [evaluate_p23(row) for row in evaluated]
    p24_results = [evaluate_p24(row) for row in evaluated]
    all_results = p22_results + p23_results + p24_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p22_holds = holds(p22_results)
    p23_holds = holds(p23_results)
    p24_holds = holds(p24_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]
    near_rows = [r for r in evaluated if r["near_540"]]

    dual_l1s = [int(r["dual_l1"]) for r in evaluated if r["dual_l1"] is not None]
    span_fracs = [float(r["span_frac"]) for r in evaluated if r["span_frac"] is not None]
    dual_l1_rels = [
        float(r["dual_l1_rel"]) for r in evaluated if r["dual_l1_rel"] is not None
    ]
    near_dual_l1s = [int(r["dual_l1"]) for r in near_rows if r["dual_l1"] is not None]

    residual_claims = [
        {
            "id": "RC18",
            "claim": (
                "Dual L1 envelope: on segment utilization maxima through "
                f"4e8-5e8 and the full o_q branch-max panel, "
                f"first_tau4_offset + trail_gap <= {DUAL_L1_MAX}."
            ),
            "status": "holds" if p22_holds else "falsified",
            "linked_prediction": "P22",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": DUAL_L1_MAX,
                "min_observed": min(dual_l1s) if dual_l1s else None,
                "max_observed": max(dual_l1s) if dual_l1s else None,
            },
        },
        {
            "id": "RC19",
            "claim": (
                "Tau4 support span fraction: "
                f"(last_tau4 - first_tau4) / (D - 1) >= {SPAN_FRAC_MIN} "
                "on util maxima + o_q panel."
            ),
            "status": "holds" if p23_holds else "falsified",
            "linked_prediction": "P23",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": SPAN_FRAC_MIN,
                "min_observed": min(span_fracs) if span_fracs else None,
                "max_observed": max(span_fracs) if span_fracs else None,
            },
        },
        {
            "id": "RC20",
            "claim": (
                "Relative Dual L1 envelope: "
                f"(first_tau4_offset + trail_gap) / D <= {DUAL_L1_REL_MAX} "
                "on util maxima + o_q panel."
            ),
            "status": "holds" if p24_holds else "falsified",
            "linked_prediction": "P24",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": DUAL_L1_REL_MAX,
                "min_observed": min(dual_l1_rels) if dual_l1_rels else None,
                "max_observed": max(dual_l1_rels) if dual_l1_rels else None,
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
            "id": "RC15_RC17_retained",
            "claim": (
                "Prior residual RC15-RC17 (trail tightness, absolute early tau4, "
                "near-540 dual marker) retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P19-P21 (prior)",
            "evidence": rc15_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc15_prediction_table": (
                str(args.rc15_table) if args.rc15_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "dual_l1_max": DUAL_L1_MAX,
            "span_frac_min": SPAN_FRAC_MIN,
            "dual_l1_rel_max": DUAL_L1_REL_MAX,
            "near_540_center": NEAR_540_CENTER,
            "near_540_radius": NEAR_540_RADIUS,
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
            "RC18_dual_l1_envelope": "holds" if p22_holds else "falsified",
            "RC19_tau4_support_span_fraction": (
                "holds" if p23_holds else "falsified"
            ),
            "RC20_relative_dual_l1_envelope": (
                "holds" if p24_holds else "falsified"
            ),
            "RC2_fixed_band": "falsified (retained)",
            "RC15_RC17": "retained holds (not primary surface)",
            "dual_l1_range": (
                [min(dual_l1s), max(dual_l1s)] if dual_l1s else None
            ),
            "span_frac_range": (
                [min(span_fracs), max(span_fracs)] if span_fracs else None
            ),
            "dual_l1_rel_range": (
                [min(dual_l1_rels), max(dual_l1_rels)] if dual_l1_rels else None
            ),
            "near_540_count": len(near_rows),
            "near_540_dual_l1_range": (
                [min(near_dual_l1s), max(near_dual_l1s)] if near_dual_l1s else None
            ),
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC18-RC20: Dual L1 envelope "
                "(joint early+late marker size), tau4 support span fraction, "
                "and relative Dual L1; does not restate RC15-RC17 componentwise "
                "bounds as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-11-rc18/"
            "offset_540_residual_rc18_probe.py"
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
