#!/usr/bin/env python3
"""Residual chamber claims RC12-RC14 after RC9-RC11 surface.

PGS objects:
  - ordered prime-gap prefix before selected square endpoint w = r^2
  - divisor-count field tau on {p+1, ..., r^2-1}
  - offset D(r) = r^2 - P(r^2)
  - tau=4 offset set Tau4 inside the chamber prefix
  - quartile mass / median location of that set

Prior residual surface (RC9-RC11) covered early-half mass, late-span presence,
and max inter-tau4 desert. This probe does not replay P1-P15 as the primary
deliverable. It states and checks the next residual claims on segment
utilization maxima through 4e8-5e8 and the full o_q branch-max panel:

  P16 / RC12: first-quarter tau4 mass
              |{k in Tau4 : k <= floor(D/4)}| / |Tau4| >= 0.15
  P17 / RC13: last-quarter tau4 mass
              |{k in Tau4 : k > floor(3D/4)}| / |Tau4| >= 0.15
  P18 / RC14: median tau4 mid-band
              0.40 <= median(Tau4) / D <= 0.65

Together: the tau4 field is not early-half-only or late-endpoint-only; each
outer quarter carries mass, and the median sits in the chamber mid-band.

Audit-only. Does not choose primes as PGS inference. Does not port d=4 SDA.
Prime-Square Proximity Theorem remains proved in PROOF.md; residual audit only.
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
RC9_TABLE = (
    ROOT
    / "experiments"
    / "square-branch-hourly-2026-07-10-rc9"
    / "offset_540_rc9_prediction_table.json"
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

FIRST_QUARTER_MASS_MIN = 0.15
LAST_QUARTER_MASS_MIN = 0.15
MEDIAN_BAND = (0.40, 0.65)

PREDICTIONS = [
    {
        "id": "P16",
        "name": "first_quarter_tau4_mass",
        "statement": (
            "On segment utilization maxima through 4e8-5e8 and the 4e8-5e8 "
            f"o_q branch-max panel, first-quarter tau4 mass "
            f"|{{k in Tau4 : k <= floor(D/4)}}| / |Tau4| >= {FIRST_QUARTER_MASS_MIN}."
        ),
        "falsifier": (
            f"any evaluated row with first_quarter_mass < {FIRST_QUARTER_MASS_MIN}"
        ),
    },
    {
        "id": "P17",
        "name": "last_quarter_tau4_mass",
        "statement": (
            "On the same surface, last-quarter tau4 mass "
            f"|{{k in Tau4 : k > floor(3D/4)}}| / |Tau4| >= {LAST_QUARTER_MASS_MIN}."
        ),
        "falsifier": (
            f"any evaluated row with last_quarter_mass < {LAST_QUARTER_MASS_MIN}"
        ),
    },
    {
        "id": "P18",
        "name": "median_tau4_mid_band",
        "statement": (
            "On the same surface, median(Tau4) / D(r) lies in "
            f"[{MEDIAN_BAND[0]}, {MEDIAN_BAND[1]}] (median sits in chamber mid-band)."
        ),
        "falsifier": (
            f"any evaluated row with median_frac outside "
            f"[{MEDIAN_BAND[0]}, {MEDIAN_BAND[1]}]"
        ),
    },
]


def prefix_tau_values(p: int, square: int) -> list[int]:
    """tau on {p+1, ..., r^2-1} via half-open segment [p+1, square)."""
    return [int(value) for value in divisor_counts_segment(p + 1, square)]


def tau4_quartile_structure(p: int, square: int, offset: int) -> dict[str, object]:
    """Compute Tau4 quartile mass and median geometry inside the chamber prefix.

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
            "first_quarter_count": 0,
            "first_quarter_mass": float("nan"),
            "last_quarter_count": 0,
            "last_quarter_mass": float("nan"),
            "median_tau4_offset": None,
            "median_frac": float("nan"),
            "q1_cut": d // 4,
            "q3_cut": (3 * d) // 4,
        }

    q1_cut = d // 4
    q3_cut = (3 * d) // 4
    first_q = sum(1 for o in tau4_offs if o <= q1_cut)
    last_q = sum(1 for o in tau4_offs if o > q3_cut)
    median_off = float(statistics.median(tau4_offs))
    return {
        "tau4_count": len(tau4_offs),
        "first_tau4_offset": tau4_offs[0],
        "last_tau4_offset": tau4_offs[-1],
        "first_quarter_count": first_q,
        "first_quarter_mass": float(first_q) / float(len(tau4_offs)),
        "last_quarter_count": last_q,
        "last_quarter_mass": float(last_q) / float(len(tau4_offs)),
        "median_tau4_offset": median_off,
        "median_frac": median_off / float(d),
        "q1_cut": q1_cut,
        "q3_cut": q3_cut,
    }


def enrich_row(row: dict) -> dict:
    out = dict(row)
    structure = tau4_quartile_structure(
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
        "first_quarter_count": row["first_quarter_count"],
        "first_quarter_mass": row["first_quarter_mass"],
        "last_quarter_count": row["last_quarter_count"],
        "last_quarter_mass": row["last_quarter_mass"],
        "median_tau4_offset": row["median_tau4_offset"],
        "median_frac": row["median_frac"],
        "q1_cut": row["q1_cut"],
        "q3_cut": row["q3_cut"],
    }


def evaluate_p16(row: dict) -> dict:
    mass = float(row["first_quarter_mass"])
    passed = mass >= FIRST_QUARTER_MASS_MIN
    return {
        "id": "P16",
        "name": "first_quarter_tau4_mass",
        "statement": PREDICTIONS[0]["statement"],
        "falsifier": PREDICTIONS[0]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "first_quarter_mass": mass,
            "bound": FIRST_QUARTER_MASS_MIN,
            "first_quarter_count": row["first_quarter_count"],
            "tau4_count": row["tau4_count"],
            "q1_cut": row["q1_cut"],
        },
    }


def evaluate_p17(row: dict) -> dict:
    mass = float(row["last_quarter_mass"])
    passed = mass >= LAST_QUARTER_MASS_MIN
    return {
        "id": "P17",
        "name": "last_quarter_tau4_mass",
        "statement": PREDICTIONS[1]["statement"],
        "falsifier": PREDICTIONS[1]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "last_quarter_mass": mass,
            "bound": LAST_QUARTER_MASS_MIN,
            "last_quarter_count": row["last_quarter_count"],
            "tau4_count": row["tau4_count"],
            "q3_cut": row["q3_cut"],
        },
    }


def evaluate_p18(row: dict) -> dict:
    frac = float(row["median_frac"])
    lo, hi = MEDIAN_BAND
    passed = lo <= frac <= hi
    return {
        "id": "P18",
        "name": "median_tau4_mid_band",
        "statement": PREDICTIONS[2]["statement"],
        "falsifier": PREDICTIONS[2]["falsifier"],
        "segment": row.get("segment"),
        "r": row["r"],
        "offset": row["offset"],
        "o_q": row.get("o_q"),
        "pass": passed,
        "status": "holds" if passed else "falsified",
        "detail": {
            "median_frac": frac,
            "band": list(MEDIAN_BAND),
            "median_tau4_offset": row["median_tau4_offset"],
            "D": row["offset"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "RC12-RC14 residual chamber probe "
            "(first/last quarter tau4 mass, median mid-band)."
        )
    )
    parser.add_argument("--prior-table", type=Path, default=PRIOR_TABLE)
    parser.add_argument("--rc9-table", type=Path, default=RC9_TABLE)
    parser.add_argument("--summary-json", type=Path, default=SUMMARY_JSON)
    parser.add_argument("--prefix-tau-json", type=Path, default=PREFIX_TAU_JSON)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "offset_540_rc12_prediction_table.json",
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

    rc9_note = None
    if args.rc9_table.is_file():
        rc9 = json.loads(args.rc9_table.read_text(encoding="utf-8"))
        rc9_note = {
            "path": str(args.rc9_table),
            "conclusion": rc9.get("conclusion"),
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
        "recomputing tau4 quartile structure on primary + o_q panel rows...",
        flush=True,
    )
    primary_rows = [enrich_row(row) for row in primary_src]
    oq_rows = [enrich_row(row) for row in oq_src]
    evaluated = primary_rows + oq_rows

    p16_results = [evaluate_p16(row) for row in evaluated]
    p17_results = [evaluate_p17(row) for row in evaluated]
    p18_results = [evaluate_p18(row) for row in evaluated]
    all_results = p16_results + p17_results + p18_results

    def holds(results: list[dict]) -> bool:
        subset = [r for r in results if r.get("pass") is not None]
        return bool(subset) and all(r["pass"] for r in subset)

    p16_holds = holds(p16_results)
    p17_holds = holds(p17_results)
    p18_holds = holds(p18_results)

    primary_compact = [_compact(row) for row in primary_rows]
    oq_compact = [_compact(row) for row in oq_rows]

    min_first_q = min(float(r["first_quarter_mass"]) for r in evaluated)
    min_last_q = min(float(r["last_quarter_mass"]) for r in evaluated)
    min_med = min(float(r["median_frac"]) for r in evaluated)
    max_med = max(float(r["median_frac"]) for r in evaluated)

    residual_claims = [
        {
            "id": "RC12",
            "claim": (
                "First-quarter tau4 mass: on segment utilization maxima through "
                f"4e8-5e8 and the full o_q branch-max panel, "
                f"|{{k in Tau4 : k <= floor(D/4)}}| / |Tau4| "
                f">= {FIRST_QUARTER_MASS_MIN}."
            ),
            "status": "holds" if p16_holds else "falsified",
            "linked_prediction": "P16",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": FIRST_QUARTER_MASS_MIN,
                "min_observed": min_first_q,
            },
        },
        {
            "id": "RC13",
            "claim": (
                "Last-quarter tau4 mass: "
                f"|{{k in Tau4 : k > floor(3D/4)}}| / |Tau4| "
                f">= {LAST_QUARTER_MASS_MIN} on the same surface "
                "(tau4 is not confined to the early chamber alone as mass)."
            ),
            "status": "holds" if p17_holds else "falsified",
            "linked_prediction": "P17",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "bound": LAST_QUARTER_MASS_MIN,
                "min_observed": min_last_q,
            },
        },
        {
            "id": "RC14",
            "claim": (
                "Median tau4 mid-band: median(Tau4) / D(r) lies in "
                f"[{MEDIAN_BAND[0]}, {MEDIAN_BAND[1]}] on the same surface."
            ),
            "status": "holds" if p18_holds else "falsified",
            "linked_prediction": "P18",
            "evidence": {
                "primary_rows": primary_compact,
                "oq_panel": oq_compact,
                "band": list(MEDIAN_BAND),
                "min_observed": min_med,
                "max_observed": max_med,
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
            "id": "RC9_RC11_retained",
            "claim": (
                "Prior residual RC9-RC11 (early-half mass, late-span, max desert) "
                "retained as measured holds; not re-proved."
            ),
            "status": "holds (retained; not re-evaluated as primary surface)",
            "linked_prediction": "P13-P15 (prior)",
            "evidence": rc9_note,
        },
    ]

    payload = {
        "inputs": {
            "prior_prediction_table": str(args.prior_table),
            "rc9_prediction_table": (
                str(args.rc9_table) if args.rc9_table.is_file() else None
            ),
            "falsification_summary_json": str(args.summary_json),
            "prefix_tau_floor_probe": prefix_tau_note,
            "first_quarter_mass_min": FIRST_QUARTER_MASS_MIN,
            "last_quarter_mass_min": LAST_QUARTER_MASS_MIN,
            "median_band": list(MEDIAN_BAND),
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
            "RC12_first_quarter_tau4_mass": "holds" if p16_holds else "falsified",
            "RC13_last_quarter_tau4_mass": "holds" if p17_holds else "falsified",
            "RC14_median_tau4_mid_band": "holds" if p18_holds else "falsified",
            "RC2_fixed_band": "falsified (retained)",
            "RC9_RC11": "retained holds (not primary surface)",
            "min_first_quarter_mass": min_first_q,
            "min_last_quarter_mass": min_last_q,
            "median_frac_range": [min_med, max_med],
            "falsified_new_predictions": [
                r["id"] for r in all_results if r.get("pass") is False
            ],
            "advance_over_prior_hour": (
                "New residual claim table RC12-RC14: first-quarter tau4 mass, "
                "last-quarter tau4 mass, and median mid-band on util maxima + "
                "o_q panel; does not restate RC9-RC11 as sole deliverable."
            ),
        },
        "falsification_command": (
            "python3 experiments/square-branch-hourly-2026-07-11-rc12/"
            "offset_540_residual_rc12_probe.py"
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
