#!/usr/bin/env python3
"""
Near-maximal GWR witness-offset audit (F18-004 / RH-103).

Status: measured / falsification surface (not a proof of F18-004).

For each consecutive prime gap p < q with nonempty interior up to --limit:
  - Locate GWR witness w = leftmost n in (p, q) with minimal tau(n)
  - d = tau(w), offset = w - p
  - C(q) = max(64, ceil(0.5 * log(q)^2))
  - ratio = offset / C

F18-004 falsifier (non-square rough-witness claim):
  ratio >= ratio_threshold
  and q > q_min
  and w is not a prime square
  and d < max(6, floor(d_log_coeff * log q))

Authority references:
  - research/18-derived-half-coefficient/docs/FINDING_STATEMENT.md (F18-004)
  - PROOF.md: Witness Threshold, Short Divisor-Average, Prime-Square Proximity
  - Issue #45: promote F18-004 or produce explicit falsifier

Repro:
  PYTHONPATH=src/python python3 \\
    research/18-derived-half-coefficient/scripts/near_maximal_witness_audit.py \\
    --limit 1000000 --output research/18-derived-half-coefficient/output/audit_1M.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from math import ceil, floor, log
from pathlib import Path
from typing import Any

import numpy as np

# Defaults match FINDING_STATEMENT.md F18-004 pinned campaign.
DEFAULT_LIMIT = 40_000_000
DEFAULT_RATIO_THRESHOLD = 0.65
DEFAULT_Q_MIN = 10_000_000
DEFAULT_D_LOG_COEFF = 0.75
DEFAULT_PROGRESS_EVERY = 100_000
REPO_DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1] / "output" / "near_maximal_audit_results.json"
)


@dataclass(frozen=True)
class GapCase:
    p: int
    q: int
    w: int
    d: int
    offset: int
    C: int
    ratio: float
    logq: float
    is_prime_square: bool

    def rough_floor(self, d_log_coeff: float) -> int:
        return max(6, floor(d_log_coeff * self.logq))

    def is_f18_004_falsifier(
        self,
        ratio_threshold: float,
        q_min: int,
        d_log_coeff: float,
    ) -> bool:
        if self.ratio < ratio_threshold:
            return False
        if self.q <= q_min:
            return False
        if self.is_prime_square:
            return False
        return self.d < self.rough_floor(d_log_coeff)


def sieve_spf(limit: int) -> np.ndarray:
    """Smallest-prime-factor sieve on 0..limit (inclusive)."""
    spf = np.arange(limit + 1, dtype=np.int32)
    root = int(limit**0.5)
    for i in range(2, root + 1):
        if spf[i] == i:
            start = i * i
            spf[start : limit + 1 : i] = np.minimum(spf[start : limit + 1 : i], i)
    return spf


def divisor_count(n: int, spf: np.ndarray) -> int:
    """Exact tau(n) via SPF factorization."""
    if n <= 1:
        return 1
    cnt = 1
    while n > 1:
        p = int(spf[n])
        exp = 0
        while n % p == 0:
            n //= p
            exp += 1
        cnt *= exp + 1
    return cnt


def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r * r == n


def is_prime_square_witness(w: int, d: int) -> bool:
    """Prime squares are exactly the integers with tau = 3."""
    return d == 3 and is_perfect_square(w)


def compression_bound(q: int) -> int:
    """C(q) = max(64, ceil(0.5 * (log q)^2)), matching PROOF.md packaging."""
    lq = log(q)
    return max(64, ceil(0.5 * lq * lq))


def scan_gaps(
    limit: int,
    progress_every: int,
) -> tuple[list[GapCase], GapCase | None, int]:
    """
    Exhaustive GWR replay on all gaps with q <= limit.

    Returns (all_cases_with_interior, max_ratio_case, total_interior_gaps).
    """
    print(f"Building SPF sieve up to {limit}...", flush=True)
    spf = sieve_spf(limit)
    print("Extracting primes...", flush=True)
    primes = [i for i in range(2, limit + 1) if int(spf[i]) == i]
    print(f"Found {len(primes)} primes. Starting gap scan...", flush=True)

    cases: list[GapCase] = []
    max_case: GapCase | None = None
    max_ratio = -1.0
    total_gaps = 0
    processed = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        if q > limit:
            break
        interior_start = p + 1
        interior_end = q - 1
        if interior_start > interior_end:
            continue

        total_gaps += 1
        processed += 1
        if progress_every > 0 and processed % progress_every == 0:
            print(
                f"  Processed {processed:,} interior gaps... (current q ≈ {q:,})",
                flush=True,
            )

        min_tau: int | None = None
        w: int | None = None
        for n in range(interior_start, interior_end + 1):
            tau = divisor_count(n, spf)
            if min_tau is None or tau < min_tau:
                min_tau = tau
                w = n

        assert w is not None and min_tau is not None
        offset = w - p
        lq = log(q)
        c_q = compression_bound(q)
        ratio = offset / c_q if c_q > 0 else 0.0
        case = GapCase(
            p=p,
            q=q,
            w=w,
            d=min_tau,
            offset=offset,
            C=c_q,
            ratio=ratio,
            logq=lq,
            is_prime_square=is_prime_square_witness(w, min_tau),
        )
        cases.append(case)
        if ratio > max_ratio:
            max_ratio = ratio
            max_case = case

    return cases, max_case, total_gaps


def threshold_matrix(
    cases: list[GapCase],
    ratio_levels: list[float],
    q_min: int,
    d_log_coeff: float,
) -> list[dict[str, Any]]:
    """
    For each ratio threshold, count high-ratio cases and F18-004 falsifiers.

    Reports both unrestricted (all q) and q > q_min slices so small LIMIT
    smokes remain informative when q_min is the campaign gate (10^7).
    """
    rows: list[dict[str, Any]] = []
    for r in ratio_levels:
        high = [c for c in cases if c.ratio >= r]
        high_q = [c for c in high if c.q > q_min]
        non_sq_all = [c for c in high if not c.is_prime_square]
        non_sq = [c for c in high_q if not c.is_prime_square]
        sq_all = [c for c in high if c.is_prime_square]
        sq = [c for c in high_q if c.is_prime_square]
        falsifiers = [
            c
            for c in cases
            if c.is_f18_004_falsifier(r, q_min, d_log_coeff)
        ]
        # Legacy d<=5 non-square high-ratio count (FINDING_STATEMENT table).
        legacy_low_d_all = [c for c in non_sq_all if c.d <= 5]
        legacy_low_d = [c for c in non_sq if c.d <= 5]
        min_d_non_sq_all = min((c.d for c in non_sq_all), default=None)
        min_d_non_sq = min((c.d for c in non_sq), default=None)
        min_floor = (
            min((c.rough_floor(d_log_coeff) for c in non_sq_all), default=None)
            if non_sq_all
            else None
        )
        rows.append(
            {
                "ratio_threshold": r,
                "high_ratio_total": len(high),
                "high_ratio_q_gt_qmin": len(high_q),
                "non_square_high_ratio_all_q": len(non_sq_all),
                "non_square_high_ratio": len(non_sq),
                "square_high_ratio_all_q": len(sq_all),
                "square_high_ratio": len(sq),
                "legacy_non_square_d_le_5_all_q": len(legacy_low_d_all),
                "legacy_non_square_d_le_5": len(legacy_low_d),
                "f18_004_falsifiers": len(falsifiers),
                "min_d_non_square_high_ratio_all_q": min_d_non_sq_all,
                "min_d_non_square_high_ratio": min_d_non_sq,
                "min_rough_floor_among_non_square_all_q": min_floor,
            }
        )
    return rows


def parse_ratio_levels(raw: str) -> list[float]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    levels = [float(p) for p in parts]
    if not levels:
        raise ValueError("ratio levels list is empty")
    for x in levels:
        if not (0.0 < x <= 1.0):
            raise ValueError(f"ratio level out of (0,1]: {x}")
    return sorted(set(levels))


def build_results(
    limit: int,
    ratio_threshold: float,
    q_min: int,
    d_log_coeff: float,
    cases: list[GapCase],
    max_case: GapCase | None,
    total_gaps: int,
    ratio_levels: list[float],
) -> dict[str, Any]:
    primary_falsifiers = [
        c
        for c in cases
        if c.is_f18_004_falsifier(ratio_threshold, q_min, d_log_coeff)
    ]
    high_primary = [c for c in cases if c.ratio >= ratio_threshold]
    square_high = [c for c in high_primary if c.is_prime_square and c.q > q_min]
    # Legacy table field: non-square, d<=5, ratio >= threshold (any q).
    legacy = [
        c
        for c in high_primary
        if (not c.is_prime_square) and c.d <= 5
    ]

    def case_dict(c: GapCase) -> dict[str, Any]:
        d = asdict(c)
        d["logq"] = round(c.logq, 6)
        d["rough_floor"] = c.rough_floor(d_log_coeff)
        d["low_d_legacy"] = c.d <= 5
        return d

    return {
        "status": "measured",
        "claim": "F18-004 rough-witness signature",
        "issue": 45,
        "limit": limit,
        "ratio_threshold": ratio_threshold,
        "q_min": q_min,
        "d_log_coeff": d_log_coeff,
        "total_gaps": total_gaps,
        "max_ratio": max_case.ratio if max_case else None,
        "max_case": case_dict(max_case) if max_case else None,
        "near_max_count": len(high_primary),
        "non_square_falsifiers_count": len(legacy),
        "f18_004_falsifiers_count": len(primary_falsifiers),
        "square_high_ratio_count": len(square_high),
        "non_square_falsifiers": [case_dict(c) for c in legacy[:50]],
        "f18_004_falsifiers": [case_dict(c) for c in primary_falsifiers[:50]],
        "square_cases": [case_dict(c) for c in square_high[:20]],
        "threshold_matrix": threshold_matrix(
            cases, ratio_levels, q_min, d_log_coeff
        ),
        "boundary": (
            "Measured surface only. Does not promote F18-004 to theorem. "
            "Not RH. Not a claim about all large gaps."
        ),
    }


def print_summary(results: dict[str, Any]) -> None:
    print("\n=== AUDIT SUMMARY ===")
    print(f"LIMIT: {results['limit']:,}")
    print(f"Total gaps with interior: {results['total_gaps']:,}")
    print(f"Global max ratio (w-p)/C: {results['max_ratio']}")
    mc = results.get("max_case")
    if mc:
        print(
            f"  max at p={mc['p']}, q={mc['q']}, w={mc['w']}, d={mc['d']}, "
            f"offset={mc['offset']}, C={mc['C']}"
        )
    print(
        f"\nPrimary F18-004 falsifiers "
        f"(ratio>={results['ratio_threshold']}, q>{results['q_min']}, "
        f"non-square, d < max(6, floor({results['d_log_coeff']} log q))): "
        f"{results['f18_004_falsifiers_count']}"
    )
    print(
        f"Legacy non-square d<=5 high-ratio (any q): "
        f"{results['non_square_falsifiers_count']}"
    )
    print(f"Prime-square high-ratio (q>q_min): {results['square_high_ratio_count']}")
    print("\n=== THRESHOLD MATRIX ===")
    for row in results["threshold_matrix"]:
        print(
            f"  r>={row['ratio_threshold']:.2f}: "
            f"high_all={row['high_ratio_total']} "
            f"(q>qmin={row['high_ratio_q_gt_qmin']}), "
            f"non_sq_all={row['non_square_high_ratio_all_q']}, "
            f"falsifiers={row['f18_004_falsifiers']}, "
            f"min_d_non_sq_all={row['min_d_non_square_high_ratio_all_q']}, "
            f"legacy_d<=5_all={row['legacy_non_square_d_le_5_all_q']}"
        )
    if results["f18_004_falsifiers_count"] > 0:
        print("\n*** F18-004 FALSIFIED on this regime ***")
    else:
        print("\nNo F18-004 falsifier on this regime (measured pass only).")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="F18-004 near-maximal GWR witness-offset audit (measured)."
    )
    p.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Scan primes/gaps with q <= LIMIT (default {DEFAULT_LIMIT}).",
    )
    p.add_argument(
        "--ratio-threshold",
        type=float,
        default=DEFAULT_RATIO_THRESHOLD,
        help="Primary ratio threshold for F18-004 (default 0.65).",
    )
    p.add_argument(
        "--q-min",
        type=int,
        default=DEFAULT_Q_MIN,
        help="Only count F18-004 falsifiers with q > q_min (default 1e7).",
    )
    p.add_argument(
        "--d-log-coeff",
        type=float,
        default=DEFAULT_D_LOG_COEFF,
        help="Coefficient in floor(coeff * log q) rough floor (default 0.75).",
    )
    p.add_argument(
        "--ratio-levels",
        type=str,
        default="0.50,0.55,0.60,0.65,0.70,0.75,0.80",
        help="Comma-separated ratio thresholds for matrix output.",
    )
    p.add_argument(
        "--progress-every",
        type=int,
        default=DEFAULT_PROGRESS_EVERY,
        help="Progress print period in interior gaps (0 disables).",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=REPO_DEFAULT_OUTPUT,
        help="JSON output path.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.limit < 5:
        print("LIMIT must be >= 5", file=sys.stderr)
        return 2
    if not (0.0 < args.ratio_threshold <= 1.0):
        print("--ratio-threshold must be in (0,1]", file=sys.stderr)
        return 2
    if args.d_log_coeff <= 0:
        print("--d-log-coeff must be positive", file=sys.stderr)
        return 2

    ratio_levels = parse_ratio_levels(args.ratio_levels)
    if args.ratio_threshold not in ratio_levels:
        ratio_levels = sorted(set(ratio_levels + [args.ratio_threshold]))

    cases, max_case, total_gaps = scan_gaps(args.limit, args.progress_every)
    results = build_results(
        limit=args.limit,
        ratio_threshold=args.ratio_threshold,
        q_min=args.q_min,
        d_log_coeff=args.d_log_coeff,
        cases=cases,
        max_case=max_case,
        total_gaps=total_gaps,
        ratio_levels=ratio_levels,
    )
    print_summary(results)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
        f.write("\n")
    print(f"\nWrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
