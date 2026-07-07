#!/usr/bin/env python3
"""Endpoint residue + wheel-open mask probe for remainder investigation.

Measures q mod 30, small-prime residue state, and whether each gap's next
prime falls inside a fixed wheel-open certification mask (default width 96).
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

from z_band_prime_predictor.gpe_nlsc_selector import WHEEL_OPEN_RESIDUES_MOD30
from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile

SMALL_PRIMES = (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
MASK_WIDTH = 96
WHEEL_OPEN_EVEN_OFFSETS = tuple(range(2, MASK_WIDTH + 2, 2))


def wheel_open_positions_after(p: int) -> list[tuple[int, int]]:
    """Return (offset, candidate) for wheel-open even offsets up to mask width."""
    positions: list[tuple[int, int]] = []
    for offset in WHEEL_OPEN_EVEN_OFFSETS:
        candidate = p + offset
        if candidate % 30 in WHEEL_OPEN_RESIDUES_MOD30:
            positions.append((offset, candidate))
    return positions


def certified_composite_by_small_primes(n: int) -> bool:
    """True when some prime <= 47 divides n (individual certification)."""
    if n < 2:
        return False
    for prime in SMALL_PRIMES:
        if n % prime == 0:
            return True
    return False


def mask_stats_for_gap(p: int, q: int) -> dict[str, int | bool]:
    """Compute wheel-open mask resolution for one gap ending at prime q."""
    positions = wheel_open_positions_after(p)
    certified_prefix = 0
    q_offset = q - p
    q_wheel_index = -1

    for index, (offset, candidate) in enumerate(positions):
        if offset == q_offset:
            q_wheel_index = index
            break
        if not certified_composite_by_small_primes(candidate):
            break
        certified_prefix += 1

    resolved_in_mask = q_wheel_index >= 0 and (
        q_wheel_index == 0
        or all(
            certified_composite_by_small_primes(cand)
            for _off, cand in positions[:q_wheel_index]
        )
    )
    return {
        "gap_width": q - p,
        "q_offset": q_offset,
        "q_wheel_open_index": q_wheel_index,
        "certified_opening_prefix_len": certified_prefix,
        "resolved_in_mask": resolved_in_mask,
    }


def run_probe(start_p: int, max_gaps: int, mask_width: int) -> dict:
    mod30 = Counter()
    gap_widths: list[int] = []
    resolved_count = 0
    max_wheel_index = 0
    prefix_lengths: list[int] = []
    residue_state_sample: list[dict[str, int]] = []

    p = start_p
    for i in range(max_gaps):
        prof = gwr_next_gap_profile(p)
        q = int(prof["next_prime"])
        mod30[q % 30] += 1
        gap_widths.append(q - p)

        stats = mask_stats_for_gap(p, q)
        if stats["resolved_in_mask"]:
            resolved_count += 1
        if int(stats["q_wheel_open_index"]) > max_wheel_index:
            max_wheel_index = int(stats["q_wheel_open_index"])
        prefix_lengths.append(int(stats["certified_opening_prefix_len"]))

        if i < 3:
            residue_state_sample.append(
                {"p": p, "q": q, **{f"q_mod_{pr}": q % pr for pr in SMALL_PRIMES[:9]}}
            )

        p = q

    gaps = max_gaps
    return {
        "lane": "endpoint_residue_mask_probe",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "start_p": start_p,
        "gaps_measured": gaps,
        "mask_width": mask_width,
        "wheel_open_offsets_scanned": len(WHEEL_OPEN_EVEN_OFFSETS),
        "q_mod_30_counts": {str(k): v for k, v in sorted(mod30.items())},
        "mean_gap": sum(gap_widths) / gaps if gaps else 0.0,
        "max_gap": max(gap_widths) if gap_widths else 0,
        "resolved_in_mask_count": resolved_count,
        "resolved_in_mask_fraction": resolved_count / gaps if gaps else 0.0,
        "max_q_wheel_open_index": max_wheel_index,
        "mean_certified_opening_prefix_len": sum(prefix_lengths) / len(prefix_lengths)
        if prefix_lengths
        else 0.0,
        "small_primes_for_certification": list(SMALL_PRIMES),
        "residue_state_sample": residue_state_sample,
        "note": (
            "Fresh mask-resolution measurement: next prime q must appear at a "
            "wheel-open offset; prior wheel-open candidates certified composite "
            f"by primes <= {SMALL_PRIMES[-1]}."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-p", type=int, default=10_000_000_000_037)
    parser.add_argument("--max-gaps", type=int, default=10_000)
    parser.add_argument("--mask-width", type=int, default=MASK_WIDTH)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    global MASK_WIDTH, WHEEL_OPEN_EVEN_OFFSETS
    MASK_WIDTH = args.mask_width
    WHEEL_OPEN_EVEN_OFFSETS = tuple(range(2, MASK_WIDTH + 2, 2))

    summary = run_probe(args.start_p, args.max_gaps, args.mask_width)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())