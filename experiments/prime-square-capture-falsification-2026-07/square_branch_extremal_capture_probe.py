#!/usr/bin/env python3
"""Square-branch extremal probe for hierarchical capture falsification.

Tests the capture insight on measured high-utilization square-branch rows
from bounded-compression search segments, where offsets reach hundreds.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import gmpy2

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
BENCH_DIR = ROOT / "research" / "02-gwr-dni" / "scripts"
for path in (FIELD_DIR, BENCH_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
import gwr_dni_recursive_walk as walk  # noqa: E402


EXTREMAL_R = [
    82_357_433,
    102_017_779,
    251_066_071,
]


def previous_prime_before(n: int) -> int:
    candidate = n - 1
    while not gmpy2.is_prime(candidate):
        candidate -= 1
    return int(candidate)


def analyze_square_row(r: int) -> dict[str, object]:
    square = r * r
    p = previous_prime_before(square)
    q = int(gmpy2.next_prime(square))
    counts = [int(v) for v in divisor_counts_segment(p + 1, q)]
    offsets = list(range(1, len(counts) + 1))
    min_tau = min(counts)
    w_index = counts.index(min_tau)
    w = p + 1 + w_index
    offset = w - p
    tau3_offsets = [h for h, t in zip(offsets, counts) if t == 3]
    tau4_offsets = [h for h, t in zip(offsets, counts) if t == 4]
    cutoff = walk.dynamic_cutoff(q)
    return {
        "r": r,
        "p": p,
        "q": q,
        "square": square,
        "w": w,
        "offset": offset,
        "tau_w": counts[w_index],
        "min_tau": min_tau,
        "cutoff": cutoff,
        "utilization": offset / cutoff,
        "w_is_square": w == square,
        "unique_tau3": len(tau3_offsets) == 1,
        "tau3_offsets": tau3_offsets,
        "first_tau4_offset": tau4_offsets[0] if tau4_offsets else None,
        "tau4_count_before_w": sum(1 for t in counts[:w_index] if t == 4),
        "capture_holds": w == square and min_tau == 3,
        "bypass_holds": bool(tau4_offsets) and tau4_offsets[0] < offset,
        "gap_size": q - p,
    }


def main() -> None:
    out_dir = Path("experiments/prime-square-capture-falsification-2026-07")
    rows = [analyze_square_row(r) for r in EXTREMAL_R]
    summary = {
        "regime": "square-branch extremal rows from bounded-compression search",
        "rows": rows,
        "f1_failures": [r for r in rows if not r["capture_holds"]],
        "f2_failures": [r for r in rows if not r["bypass_holds"]],
    }
    (out_dir / "square_branch_extremal_probe.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()