#!/usr/bin/env python3
"""Falsification probe: Hierarchical Capture of the Selected Integer by Prime Squares.

PGS objects (AGENTS.md entry frame):
  - ordered prime-gap state (p, q) with interior I = {p+1, ..., q-1}
  - divisor-count field tau(n)
  - GWR selected witness w = leftmost interior argmin tau(n)
  - prefix distance offset = w - p
  - dynamic cutoff C(q) = max(64, ceil(0.5 * log(q)^2))

This script is audit-only. It does not perform PGS inference beyond reading
proved GWR selection from exact divisor counts.

Falsification targets (Core Insight claims):
  F1  Capture: when interior has unique tau=3 integer, GWR is that prime square.
  F2  Bypass: long square-branch offsets have earlier tau=4 in prefix (ignored).
  F3  Worst-case class: top utilization/offset rows are square-branch (tau(w)=3).
  F4  Decoupling: non-square gaps cannot match square-branch extreme offsets.
  F5  Adjacency break: square at p+1 is a documented trivial exception.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
if str(FIELD_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_DIR))

from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile  # noqa: E402


def dynamic_cutoff(q: int) -> int:
    return max(64, math.ceil(0.5 * math.log(q) ** 2))


def divisor_counts(limit: int) -> list[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def is_prime_square(n: int, tau: list[int]) -> bool:
    if tau[n] != 3:
        return False
    root = math.isqrt(n)
    return root * root == n and tau[root] == 2


def interior_prime_squares(p: int, q: int, tau: list[int]) -> list[int]:
    squares: list[int] = []
    r = 2
    while True:
        sq = r * r
        if sq >= q:
            break
        if sq > p and tau[r] == 2:
            squares.append(sq)
        r += 1
    return squares


def first_offset_with_tau(p: int, q: int, tau: list[int], target: int) -> int | None:
    for n in range(p + 1, q):
        if tau[n] == target:
            return n - p
    return None


def count_tau_in_prefix(p: int, end_exclusive: int, tau: list[int], target: int) -> int:
    return sum(1 for n in range(p + 1, end_exclusive) if tau[n] == target)


@dataclass(frozen=True)
class GapRecord:
    p: int
    q: int
    gap_size: int
    w: int
    offset: int
    tau_w: int
    min_tau: int
    cutoff: int
    utilization: float
    interior_squares: tuple[int, ...]
    tau3_count: int
    unique_tau3: bool
    square_capture: bool
    first_tau4_offset: int | None
    first_tau3_offset: int | None
    tau4_before_w: int
    adjacent_square: bool
    capture_mechanism_holds: bool


def analyze_gap(p: int, q: int, tau: list[int]) -> GapRecord | None:
    if q - p <= 1:
        return None

    min_tau = min(tau[n] for n in range(p + 1, q))
    w = p + 1
    for n in range(p + 1, q):
        if tau[n] == min_tau:
            w = n
            break

    offset = w - p
    squares = interior_prime_squares(p, q, tau)
    tau3_positions = [n for n in range(p + 1, q) if tau[n] == 3]
    unique_tau3 = len(tau3_positions) == 1
    square_capture = min_tau == 3 and is_prime_square(w, tau)
    first_tau4 = first_offset_with_tau(p, q, tau, 4)
    first_tau3 = first_offset_with_tau(p, q, tau, 3)
    tau4_before_w = count_tau_in_prefix(p, w, tau, 4)
    adjacent_square = bool(squares) and squares[0] == p + 1

    capture_mechanism_holds = True
    if unique_tau3:
        only_tau3 = tau3_positions[0]
        capture_mechanism_holds = (
            w == only_tau3
            and is_prime_square(only_tau3, tau)
            and min_tau == 3
        )

    cutoff = dynamic_cutoff(q)
    return GapRecord(
        p=p,
        q=q,
        gap_size=q - p,
        w=w,
        offset=offset,
        tau_w=tau[w],
        min_tau=min_tau,
        cutoff=cutoff,
        utilization=offset / cutoff,
        interior_squares=tuple(squares),
        tau3_count=len(tau3_positions),
        unique_tau3=unique_tau3,
        square_capture=square_capture,
        first_tau4_offset=first_tau4,
        first_tau3_offset=first_tau3,
        tau4_before_w=tau4_before_w,
        adjacent_square=adjacent_square,
        capture_mechanism_holds=capture_mechanism_holds,
    )


def scan_gaps(limit: int) -> list[GapRecord]:
    tau = divisor_counts(limit)
    primes = [n for n in range(2, limit + 1) if tau[n] == 2]
    records: list[GapRecord] = []
    for p, q in zip(primes, primes[1:]):
        row = analyze_gap(p, q, tau)
        if row is not None:
            records.append(row)
    return records


def top_rows(records: Iterable[GapRecord], key, n: int) -> list[GapRecord]:
    return sorted(records, key=key, reverse=True)[:n]


def summarize(records: list[GapRecord], top_n: int) -> dict[str, object]:
    total = len(records)
    square_branch = [r for r in records if r.tau_w == 3]
    d4_branch = [r for r in records if r.tau_w == 4]
    with_square = [r for r in records if r.interior_squares]
    unique_tau3 = [r for r in records if r.unique_tau3]

    f1_failures = [r for r in unique_tau3 if not r.capture_mechanism_holds]
    long_square = [r for r in square_branch if r.offset >= 64]
    f2_failures = [
        r for r in long_square
        if r.first_tau4_offset is None or r.first_tau4_offset >= r.offset
    ]

    by_offset = top_rows(records, lambda r: r.offset, top_n)
    by_util = top_rows(records, lambda r: r.utilization, top_n)

    def branch_counts(rows: list[GapRecord]) -> dict[str, int]:
        return {
            "tau3": sum(1 for r in rows if r.tau_w == 3),
            "tau4": sum(1 for r in rows if r.tau_w == 4),
            "other": sum(1 for r in rows if r.tau_w not in (3, 4)),
        }

    max_square_offset = max((r.offset for r in square_branch), default=0)
    max_d4_offset = max((r.offset for r in d4_branch), default=0)
    max_d4_util = max((r.utilization for r in d4_branch), default=0.0)

    d4_exceeds_square = [
        r for r in d4_branch
        if r.offset > max_square_offset or r.utilization >= max((x.utilization for x in square_branch), default=0.0)
    ]

    non_square_high_util = [
        r for r in d4_branch if r.utilization >= 0.5
    ]

    adjacent_cases = [r for r in records if r.adjacent_square]

    return {
        "regime": {"prime_limit": records[-1].q if records else None, "gaps_with_interior": total},
        "branch_counts": {
            "tau_w_3": len(square_branch),
            "tau_w_4": len(d4_branch),
            "gaps_with_interior_prime_square": len(with_square),
            "gaps_with_unique_tau3": len(unique_tau3),
        },
        "f1_capture_unique_tau3": {
            "tested": len(unique_tau3),
            "failures": len(f1_failures),
            "falsified": bool(f1_failures),
            "counterexamples": [
                {
                    "p": r.p,
                    "q": r.q,
                    "w": r.w,
                    "offset": r.offset,
                    "tau_w": r.tau_w,
                    "interior_squares": list(r.interior_squares),
                }
                for r in f1_failures[:10]
            ],
        },
        "f2_bypass_early_tau4_before_long_square": {
            "long_square_branch_threshold_offset_ge_64": len(long_square),
            "failures_no_early_tau4": len(f2_failures),
            "falsified": bool(f2_failures),
            "counterexamples": [
                {"p": r.p, "q": r.q, "offset": r.offset, "first_tau4_offset": r.first_tau4_offset}
                for r in f2_failures[:10]
            ],
        },
        "f3_worst_case_class": {
            "top_by_offset_n": top_n,
            "top_offset_branch_counts": branch_counts(by_offset),
            "top_utilization_branch_counts": branch_counts(by_util),
            "max_square_offset": max_square_offset,
            "max_d4_offset": max_d4_offset,
            "d4_offset_exceeds_global_square_max": max_d4_offset > max_square_offset,
            "falsified_top_offset_not_majority_square": branch_counts(by_offset)["tau3"] < top_n // 2,
        },
        "f4_decoupling_non_square_extremes": {
            "d4_gaps_matching_or_exceeding_square_extreme": len(d4_exceeds_square),
            "d4_utilization_ge_0_5": len(non_square_high_util),
            "max_d4_utilization": max_d4_util,
            "falsified": bool(d4_exceeds_square) or max_d4_util >= 0.5,
            "examples": [
                {
                    "p": r.p,
                    "q": r.q,
                    "offset": r.offset,
                    "utilization": round(r.utilization, 6),
                    "tau4_before_w": r.tau4_before_w,
                }
                for r in sorted(d4_exceeds_square, key=lambda x: -x.utilization)[:10]
            ],
        },
        "f5_adjacent_square_exception": {
            "count": len(adjacent_cases),
            "rows": [
                {
                    "p": r.p,
                    "square": r.interior_squares[0] if r.interior_squares else None,
                    "offset": r.offset,
                    "tau_w": r.tau_w,
                }
                for r in adjacent_cases[:15]
            ],
        },
        "frontier_top_utilization": [
            {
                "p": r.p,
                "q": r.q,
                "w": r.w,
                "offset": r.offset,
                "tau_w": r.tau_w,
                "utilization": round(r.utilization, 6),
                "square_capture": r.square_capture,
                "tau4_before_w": r.tau4_before_w,
            }
            for r in by_util
        ],
        "frontier_top_offset": [
            {
                "p": r.p,
                "q": r.q,
                "w": r.w,
                "offset": r.offset,
                "tau_w": r.tau_w,
                "utilization": round(r.utilization, 6),
                "square_capture": r.square_capture,
            }
            for r in by_offset
        ],
    }


def write_csv(path: Path, records: list[GapRecord]) -> None:
    fields = [
        "p", "q", "gap_size", "w", "offset", "tau_w", "min_tau", "cutoff",
        "utilization", "interior_squares", "tau3_count", "unique_tau3",
        "square_capture", "first_tau4_offset", "first_tau3_offset",
        "tau4_before_w", "adjacent_square", "capture_mechanism_holds",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            writer.writerow({
                "p": row.p,
                "q": row.q,
                "gap_size": row.gap_size,
                "w": row.w,
                "offset": row.offset,
                "tau_w": row.tau_w,
                "min_tau": row.min_tau,
                "cutoff": row.cutoff,
                "utilization": row.utilization,
                "interior_squares": ";".join(str(s) for s in row.interior_squares),
                "tau3_count": row.tau3_count,
                "unique_tau3": row.unique_tau3,
                "square_capture": row.square_capture,
                "first_tau4_offset": row.first_tau4_offset,
                "first_tau3_offset": row.first_tau3_offset,
                "tau4_before_w": row.tau4_before_w,
                "adjacent_square": row.adjacent_square,
                "capture_mechanism_holds": row.capture_mechanism_holds,
            })


def cross_check_profile(records: list[GapRecord], sample: int = 200) -> dict[str, object]:
    """Cross-check a sample against gwr_next_gap_profile."""
    mismatches: list[dict[str, int]] = []
    checked = 0
    for row in records[:: max(1, len(records) // sample)]:
        profile = gwr_next_gap_profile(row.p)
        if profile["next_prime"] != row.q:
            mismatches.append({"p": row.p, "expected_q": row.q, "profile_q": profile["next_prime"]})
        if profile["winner_offset"] is not None and profile["winner_offset"] != row.offset:
            mismatches.append({
                "p": row.p,
                "expected_offset": row.offset,
                "profile_offset": profile["winner_offset"],
            })
        checked += 1
    return {"checked": checked, "mismatches": mismatches, "ok": not mismatches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2_000_000, help="Upper prime bound.")
    parser.add_argument("--top-n", type=int, default=50, help="Frontier row count.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/prime-square-capture-falsification-2026-07"),
    )
    args = parser.parse_args()

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    records = scan_gaps(args.limit)
    summary = summarize(records, args.top_n)
    summary["cross_check"] = cross_check_profile(records)

    write_csv(out_dir / "gap_scan_details.csv", records)
    (out_dir / "falsification_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()