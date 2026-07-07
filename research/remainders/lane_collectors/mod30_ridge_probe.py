#!/usr/bin/env python3
"""Lightweight left-prime mod-30 ridge probe for remainder investigation.

Computes right-edge share by p mod 30 on a bounded exact window without
running the full insight_probes suite.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment
from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile

RESIDUES = (1, 7, 11, 13, 17, 19, 23, 29)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-p", type=int, default=200_000)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def raw_z_peak_side(p: int, q: int) -> str:
    """Return left/right/center for within-gap raw-Z maximum (simplified)."""
    counts = list(divisor_counts_segment(p + 1, q))
    if not counts:
        return "center"
    peak = max(counts)
    peak_idx = counts.index(peak)
    k = peak_idx + 1
    g = q - p
    if k <= 2:
        return "left"
    if k >= g - 1:
        return "right"
    return "center"


def run_probe(max_p: int) -> dict:
    stats: dict[int, dict[str, int]] = {
        r: {"gaps": 0, "left": 0, "right": 0, "center": 0} for r in RESIDUES
    }
    global_counts = {"gaps": 0, "left": 0, "right": 0, "center": 0}

    p = 2
    while p <= max_p:
        prof = gwr_next_gap_profile(p)
        q = int(prof["next_prime"])
        if q > p + 1:
            side = raw_z_peak_side(p, q)
            residue = p % 30
            if residue in stats:
                stats[residue]["gaps"] += 1
                stats[residue][side] += 1
            global_counts["gaps"] += 1
            global_counts[side] += 1
        p = q

    global_right = global_counts["right"] / global_counts["gaps"] if global_counts["gaps"] else 0.0
    rows = []
    for residue in RESIDUES:
        s = stats[residue]
        gaps = s["gaps"]
        right_share = s["right"] / gaps if gaps else 0.0
        rows.append(
            {
                "p_mod_30": residue,
                "gaps": gaps,
                "right_share": right_share,
                "right_lift": right_share / global_right if global_right else 0.0,
            }
        )

    return {
        "lane": "mod30_ridge_probe",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "max_p": max_p,
        "global_gaps": global_counts["gaps"],
        "global_right_share": global_right,
        "by_residue": rows,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_probe(args.max_p)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())