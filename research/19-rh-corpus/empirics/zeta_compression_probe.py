#!/usr/bin/env python3
"""GWR chamber → zeta compression probe (RH-105).

Uses src/python bridge API plus chamber-level ΔD/ΔB mapping from proved
gap invariants. Output: empirics/output/compression_probe_results.json

Measured regime: partial sums at five s-values with fixed term count N.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Repo src/python on path when run from root (see README).
_SRC = Path(__file__).resolve().parents[3] / "src" / "python"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from z_band_prime_rh_bridge.bridge import evaluate_partial_sum_bridge

from chamber_compression import (
    analyze_chamber_gap,
    chamber_dirichlet_increments,
    chamber_report_to_dict,
    increments_to_dict,
    load_f18_audit_summary,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

EXAMPLE_GAPS = ((23, 29), (89, 97))
# Five Re(s)>1 values; N=10^4 is tight near s=2 and excellent for s≥2.5.
PROBE_S_VALUES = (2.0, 2.5, 3.0, 3.5, 4.0)
PRIMARY_S = 2.5
PROBE_TERMS = 10_000
PROBE_DPS = 60


def _global_bridge_row(s: float) -> dict:
    evaluation = evaluate_partial_sum_bridge(s, PROBE_TERMS, PROBE_DPS)
    return {
        "s": s,
        "normalized_ratio_error": evaluation.normalized_ratio_error,
        "mangoldt_series_error": evaluation.mangoldt_series_error,
    }


def main() -> int:
    chambers = [analyze_chamber_gap(p, q) for p, q in EXAMPLE_GAPS]

    multi_s_increments = []
    for s in PROBE_S_VALUES:
        for p, q in EXAMPLE_GAPS:
            multi_s_increments.append(
                increments_to_dict(chamber_dirichlet_increments(s, p, q, PROBE_TERMS))
            )

    # Backward-compatible primary slice (s = PRIMARY_S).
    primary_increments = [
        row
        for row in multi_s_increments
        if abs(row["s"] - PRIMARY_S) < 1e-12
    ]

    f18 = load_f18_audit_summary()
    max_case = f18["max_case"]
    f18_chamber = analyze_chamber_gap(max_case["p"], max_case["q"])
    if max_case["q"] <= PROBE_TERMS:
        f18_inc = increments_to_dict(
            chamber_dirichlet_increments(
                PRIMARY_S, max_case["p"], max_case["q"], PROBE_TERMS
            )
        )
    else:
        f18_inc = {
            "skipped": True,
            "reason": f"q={max_case['q']} exceeds pinned terms={PROBE_TERMS}",
            "boundary": (
                "F18 integer branch invariants still measured; "
                "ΔD/ΔB deferred at this scale"
            ),
        }

    global_by_s = [_global_bridge_row(s) for s in PROBE_S_VALUES]
    primary_global = next(row for row in global_by_s if abs(row["s"] - PRIMARY_S) < 1e-12)

    payload = {
        "probe": "gwr_chamber_zeta_compression",
        "layer": "L3",
        "finding_id": "RH-105",
        "mapping": {
            "delta_d": "sum_{n in I} tau(n) / n^s",
            "delta_b": "sum_{n in I} H(n) / n^s via normalization_load",
            "rho_chamber": "delta_b / delta_d",
            "global_r": "evaluate_partial_sum_bridge -> -zeta'/zeta",
        },
        "s": PRIMARY_S,
        "s_values": list(PROBE_S_VALUES),
        "terms": PROBE_TERMS,
        "example_chambers": [chamber_report_to_dict(c) for c in chambers],
        "example_increments": primary_increments,
        "example_increments_multi_s": multi_s_increments,
        "f18_max_case": {
            "audit_summary": {
                "limit": f18["limit"],
                "max_ratio": f18["max_ratio"],
                "non_square_falsifiers_count": f18["non_square_falsifiers_count"],
            },
            "chamber": chamber_report_to_dict(f18_chamber),
            "increments": f18_inc,
        },
        "global_bridge": {
            "normalized_ratio_error": primary_global["normalized_ratio_error"],
            "mangoldt_series_error": primary_global["mangoldt_series_error"],
        },
        "global_bridge_by_s": global_by_s,
        "interpretation": {
            "status": "measured",
            "boundary": (
                "Chamber rho is local; global R(s) is not sum of chamber ratios. "
                "Finite N partial sums; not analytic continuation."
            ),
            "regime": f"N={PROBE_TERMS}, s in {list(PROBE_S_VALUES)}",
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "compression_probe_results.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(
        f"GWR chamber compression probe "
        f"(s_values={list(PROBE_S_VALUES)}, N={PROBE_TERMS})"
    )
    print("-" * 72)
    for chamber, inc in zip(chambers, primary_increments):
        print(
            f"gap {chamber.p}->{chamber.q}  w={chamber.w}  "
            f"branch={chamber.f18_branch}  rho_ch={inc['rho_chamber']:.6f}"
        )
    print(
        f"F18 max gap {f18_chamber.p}->{f18_chamber.q}  "
        f"branch={f18_chamber.f18_branch}  ratio={f18_chamber.offset_ratio:.4f}"
    )
    if f18_inc.get("skipped"):
        print(f"  (Dirichlet increments skipped: {f18_inc['reason']})")
    print("global |R+ζ'/ζ| errors by s:")
    for row in global_by_s:
        print(
            f"  s={row['s']}: ratio_err={row['normalized_ratio_error']:.3e}  "
            f"mangoldt_err={row['mangoldt_series_error']:.3e}"
        )
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
