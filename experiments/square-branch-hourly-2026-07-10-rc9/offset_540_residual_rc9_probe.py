#!/usr/bin/env python3
"""Residual chamber claims RC9-RC11 after RC6-RC8 surface.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set inside the chamber prefix
  - early-half / late-span / inter-tau4 gap structure of that set

Prior residual surface (RC6-RC8) covered o_q-panel phase order, late-dominant
phase_gap, and near-540 exclusivity. This probe does not replay P1-P12 as the
primary deliverable. It states and checks the next residual claims on
segment utilization maxima through 4e8-5e8 and the full o_q branch-max panel:

  P13 / RC9:  early-half tau4 mass
              |{k in Tau4 : k <= D/2}| / |Tau4| >= 0.40
  P14 / RC10: late-span tau4 presence
              last_tau4_offset / D(r) >= 0.95
  P15 / RC11: no large tau4 desert
              max consecutive gap among tau4 offsets (incl. from 0) / D <= 0.10

Audit-only. Does not choose primes as PGS inference. Does not port d=4 SDA.
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
RC6_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10-rc6"
    / "offset_540_rc6_prediction_table.json"
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

EARLY_HALF_MASS_MIN = 0.40
LATE_SPAN_MIN = 0.95
MAX_GAP_FRAC_MAX = 0.10

PREDICTIONS = [
    {
        "id": "P13",
        "name": "early_half_tau4_mass",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            f"o_q branch-max panel, early-half tau4 mass "
            f"|{{k in Tau4 : k <= floor(D/2)}}| / |Tau4| >= {EARLY_HALF_MASS_MIN}."
        ),
        "falsifier": (
            f"any evaluated row with early_half_mass < {EARLY_HALF_MASS_MIN}"
        ),
    },
    {
        "id": "P14",
        "name": "late_span_tau4",
        "statement": (
            "On the same surface, last_tau4_offset / D(r) "
            f">= {LATE_SPAN_MIN} (tau4 appears near the late end of the chamber)."
        ),
        "falsifier": f"any evaluated row with last_tau4_offset / D < {LATE_SPAN_MIN}",
    },
    {
        "id": "P15",
        "name": "no_large_tau4_desert",
        "statement": (
            "On the same surface, the maximum consecutive gap among tau4 "
            "offsets measured from 0 through D (including lead-in before first "
            f"tau4 and trail after last tau4) satisfies max_gap / D <= {MAX_GAP_FRAC_MAX}."
        ),
        "falsifier": f"any evaluated row with max_gap / D > {MAX_GAP_FRAC_MAX}",
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def tau4_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute tau4 offset set geometry inside the chamber prefix.

    Offsets are 1-based from p: offset k labels n = p + k.
    The selected square sits at offset D and is not in the prefix.
    """
    d = int(offset)
    prefix = prefix_tau_values(p, square)
    if len(prefix) != d - 1:
        raise ValueError(
            f"prefix length mismatch: got {len(prefix)}, expected D-1={d - 1}"
        )
    tau4_offs = [i + 1 for i, value in enumerate(prefix) if value == 4]
    if not tau4_offs:
        return {
            "tau4_count": 0,
            "first_tau4_offset": None,
            "last_tau4_offset": None,
            "early_half_count": 0,
            "early_half_mass": float("nan"),
            "late_span": float("nan"),
            "max_gap": d,
            "max_gap_frac": 1.0,
            "trail_gap": d,
            "lead_gap": d,
        }

    half = d // 2
    early = sum(1 for o in tau4_offs if o <= half)
    first4 = tau4_offs[0]
    last4 = tau4_offs[-1]
    # Gaps from 0 -> first, between consecutive tau4, last -> D.
    markers = [0] + tau4_offs + [d]
    gaps = [markers[i + 1] - markers[i] for i in range(len(markers) - 1)]
    max_gap = max(gaps)
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": first4,
        "last_tau4_offset": last4,
        "early_half_count": early,
        "early_half_mass": float(early) / float(len(tau4_offs)),
        "late_span": float(last4) / float(d),
        "max_gap": max_gap,
        "max_gap_frac": float(max_gap) / float(d),
        "trail_gap": d - last4,
        "lead_gap": first4,  # distance from p to first tau4 is first4 steps of size 1; gap from 0 is first4
    }


def enrich_row(row: dict) -> dict:
    out = dict(row)
    structure = tau4_structure(int(row["p"]), int(row["square"]), int(row["offset"]))
    out.update(structure)
    # Cross-check retained chamber fields when present.
    if "first_tau4_offset" in row and structure["first_tau4_offset"] is not None:
        if int(row["first_tau4_offset"]) != int(structure["first_tau4_offset"]):
            raise ValueError(
                f"first_tau4 mismatch r={row['r']}: "
                f"table={row['first_tau4_offset']} recomputed={structure['first_tau4_offset']}"
            )
    if "prefix" in row:
        if int(row["prefix"]["tau4_count"]) != int(structure["tau4_count"]):
            raise ValueError(
                f"tau4_count mismatch r={row['r']}: "
                f"table={row['prefix']['tau4_count']} recomputed={structure['tau4_count']}"
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
        "early_half_count": row["early_half_count"],
        "early_half_mass": row["early_half_mass"],
        "late_span": row["late_span"],
        "max_gap": row["max_gap"],
        "max_gap_frac": row["max_gap_frac"],
        "lead_gap": row["lead_gap"],
        "trail_gap": row["trail_gap"],
    }


def evaluate_p13(row: dict) -> dict:
    mass = float(row["early_half_mass"])
    passed = mass >= EARLY_HALF_MASS_MIN
    return {
        "id": "P13",
        "name": "early_half_tau4_mass",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "early_half_mass": mass,
            "bound": EARLY_HALF_MASS_MIN,
            "early_half_count": row["early_half_count"],
            "tau4_count": row["tau4_count"],
        },
    }


def evaluate_p14(row: dict) -> dict:
    span = float(row["late_span"])
    passed = span >= LATE_SPAN_MIN
    return {
        "id": "P14",
        "name": "late_span_tau4",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "late_span": span,
            "bound": LATE_SPAN_MIN,
            "last_tau4_offset": row["last_tau4_offset"],
            "D": row["offset"],
        },
    }


def evaluate_p15(row: dict) -> dict:
    frac = float(row["max_gap_frac"])
    passed = frac <= MAX_GAP_FRAC_MAX
    return {
        "id": "P15",
        "name": "no_large_tau4_desert",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "max_gap": row["max_gap"],
            "max_gap_frac": frac,
            "bound": MAX_GAP_FRAC_MAX,
            "lead_gap": row["lead_gap"],
            "trail_gap": row["trail_gap"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC9-RC11 residual chamber probe "
            "(early-half tau4 mass, late span, max gap)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc6-table", type=Path, default=RC6_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc9_prediction_table.json",
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

    rc6_note = None
    if args.rc6_table.is_file():
        rc6 = json.loads(args.rc6_table.read_text(encoding="utf-8"))
        rc6_note = {
            "path": str(args.rc6_table),
            "conclusion": rc6.get("conclusion"),
        }

    primary_src = prior["prior_rows"] + [prior["new_row"]]
    oq_src = prior.get("oq_rows", [])

    # Validate o_q panel matches summary branch maxima offsets.
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

    print("recomputing tau4 structure on primary + o_q panel rows...", flush=True)
    primary_rows = [enrich_row(row) for row in primary_src]
    oq_rows = [enrich_row(row) for row in oq_src]
    evaluated = primary_rows + oq_rows

    p13_results = [evaluate_p13(row) for row in evaluated]
    p14_results = [evaluate_p14(row) for row in evaluated]
    p15_results = [evaluate_p15(row) for row in evaluated]
    all_results = p13_results + p14_results + p15_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p13_holds = holds(p13_results)
    p14_holds = holds(p14_results)
    p15_holds = holds(p15_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]

    min_early = min(float(r["early_half_mass"]) for r in evaluated)
    min_late = min(float(r["late_span"]) for r in evaluated)
    max_gapf = max(float(r["max_gap_frac"]) for r in evaluated)

    residual_claims = [
        {
            "id": "RC9",
            "claim": (
                "Early-half tau4 mass: on segment utilization maxima through "
                f"4e8-5e8 and the full o_q branch-max panel, "
                f"|{{k in Tau4 : k <= floor(D/2)}}| / |Tau4| >= {EARLY_HALF_MASS_MIN}."
            ),
            "status": "holds" if p13_holds else "falsified",
            "linked_prediction": "P13",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": EARLY_HALF_MASS_MIN,
                "min_observed": min_early,
            },
        },
        {
            "id": "RC10",
            "claim": (
                "Late-span tau4 presence: last_tau4_offset / D(r) "
                f">= {LATE_SPAN_MIN} on the same surface (tau4 is not confined "
                "to the early chamber alone)."
            ),
            "status": "holds" if p14_holds else "falsified",
            "linked_prediction": "P14",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": LATE_SPAN_MIN,
                "min_observed": min_late,
            },
        },
        {
            "id": "RC11",
            "claim": (
                "No large tau4 desert: max consecutive gap among tau4 offsets "
                f"(from 0 through D, including lead and trail) / D <= {MAX_GAP_FRAC_MAX} "
                "on the same surface."
            ),
            "status": "holds" if p15_holds else "falsified",
            "linked_prediction": "P15",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": MAX_GAP_FRAC_MAX,
                "max_observed": max_gapf,
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
            "id": "RC6_RC8_retained",
            "claim": (
                "Prior residual RC6-RC8 (o_q-panel phase order, late-dominant "
                "phase_gap, near-540 exclusivity) retained as measured holds; "
                "not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P10-P12 (prior)",
            "evidence": rc6_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc6_prediction_table": str(args.rc6_table) if args.rc6_table.is_file() else None,
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "early_half_mass_min": EARLY_HALF_MASS_MIN,
            "late_span_min": LATE_SPAN_MIN,
            "max_gap_frac_max": MAX_GAP_FRAC_MAX,
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
            "RC9_early_half_tau4_mass": "holds" if p13_holds else "falsified",
            "RC10_late_span_tau4": "holds" if p14_holds else "falsified",
            "RC11_no_large_tau4_desert": "holds" if p15_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC6_RC8": "retained holds (not primary surface)",
            "min_early_half_mass": min_early,
            "min_late_span": min_late,
            "max_gap_frac": max_gapf,
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC9-RC11: early-half tau4 mass, "
                "late-span tau4 presence, and max inter-tau4 gap bound on util "
                "maxima + o_q panel; does not restate RC6-RC8 as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-10-rc9/"
            "offset_540_residual_rc9_probe.py"
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
