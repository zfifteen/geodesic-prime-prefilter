#!/usr/bin/env python3
"""GWR chamber → zeta compression probe (RH-105).

Uses src/python bridge API plus chamber-level ΔD/ΔB mapping from proved
gap invariants. Output: empirics/output/compression_probe_results.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
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
PROBE_S = 2.5
PROBE_TERMS = 10_000
PROBE_DPS = 60


def main() -> int:
    chambers = [analyze_chamber_gap(p, q) for p, q in EXAMPLE_GAPS]
    increments = [
        increments_to_dict(
            chamber_dirichlet_increments(PROBE_S, p, q, PROBE_TERMS)
        )
        for p, q in EXAMPLE_GAPS
    ]

    f18 = load_f18_audit_summary()
    max_case = f18["max_case"]
    f18_chamber = analyze_chamber_gap(max_case["p"], max_case["q"])
    if max_case["q"] <= PROBE_TERMS:
        f18_inc = increments_to_dict(
            chamber_dirichlet_increments(
                PROBE_S, max_case["p"], max_case["q"], PROBE_TERMS
            )
        )
    else:
        f18_inc = {
            "skipped": True,
            "reason": f"q={max_case['q']} exceeds pinned terms={PROBE_TERMS}",
            "boundary": "F18 integer branch invariants still measured; ΔD/ΔB deferred at this scale",
        }

    global_eval = evaluate_partial_sum_bridge(PROBE_S, PROBE_TERMS, PROBE_DPS)

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
        "s": PROBE_S,
        "terms": PROBE_TERMS,
        "example_chambers": [chamber_report_to_dict(c) for c in chambers],
        "example_increments": increments,
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
            "normalized_ratio_error": global_eval.normalized_ratio_error,
            "mangoldt_series_error": global_eval.mangoldt_series_error,
        },
        "interpretation": {
            "status": "measured",
            "boundary": "Chamber rho is local; global R(s) is not sum of chamber ratios",
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "compression_probe_results.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"GWR chamber compression probe (s={PROBE_S}, N={PROBE_TERMS})")
    print("-" * 72)
    for chamber, inc in zip(chambers, increments):
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
    print(f"global |R+ζ'/ζ| error = {global_eval.normalized_ratio_error:.3e}")
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())