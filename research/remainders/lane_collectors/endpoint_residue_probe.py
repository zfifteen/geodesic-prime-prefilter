#!/usr/bin/env python3
"""Lightweight endpoint residue probe for remainder investigation.

Measures q mod 30 and small-prime residue state along a consecutive GWR gap
chain. Produces JSON summary for the endpoint-residue lane.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile

SMALL_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-p", type=int, default=10_000_000_007)
    parser.add_argument("--max-gaps", type=int, default=10_000)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def run_probe(start_p: int, max_gaps: int) -> dict:
    mod30 = Counter()
    gap_widths: list[int] = []
    p = start_p
    for _ in range(max_gaps):
        prof = gwr_next_gap_profile(p)
        q = int(prof["next_prime"])
        mod30[q % 30] += 1
        gap_widths.append(q - p)
        p = q

    return {
        "lane": "endpoint_residue_probe",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "start_p": start_p,
        "gaps_measured": max_gaps,
        "q_mod_30_counts": {str(k): v for k, v in sorted(mod30.items())},
        "mean_gap": sum(gap_widths) / len(gap_widths) if gap_widths else 0.0,
        "max_gap": max(gap_widths) if gap_widths else 0,
        "small_primes_tracked": list(SMALL_PRIMES),
        "note": "Fresh measurement on GWR walk chain; complements hourly mask artifact.",
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary = run_probe(args.start_p, args.max_gaps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())