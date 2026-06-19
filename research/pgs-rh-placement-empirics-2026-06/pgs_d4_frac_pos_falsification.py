#!/usr/bin/env python3
"""Falsification harness for d=4 fractional-position bound (Phases 5–7).

Checks proved/measured obligations from d4_fractional_position_bound.md on finite
regimes. Audit only — does not perform PGS inference.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

from pgs_chamber_budget_analyzer import build_tau_table, classify_packet, sieve_primes


def next_prime_square_after(n: int, primes: list[int]) -> int:
    root = int(n**0.5) + 1
    for p in primes:
        if p >= root:
            return p * p
    raise ValueError(f"no prime square found above {n}")


def first_tau4_offset(p: int, q: int, tau: list[int]) -> int | None:
    for n in range(p + 1, q):
        if tau[n] == 4:
            return n - p
    return None


def short_divisor_average_bound(p: int, H: int) -> float:
    if H <= 0:
        return 0.0
    N = p + H
    return H * (math.log(N) + 2.0) + 2.0 * math.sqrt(N)


def r_sda_analytic(p: int, max_search: int = 10_000) -> int:
    """Least r >= 1 where a tau<=4-free prefix of length r-1 cannot satisfy 5H <= SDA."""
    for r in range(1, max_search + 1):
        H = r - 1
        if H == 0:
            continue
        if 5 * H > short_divisor_average_bound(p, H):
            return r
    return max_search


def analyze_d4_bounds(limit: int) -> dict:
    tau = build_tau_table(limit)
    primes = sieve_primes(limit)
    r_sda_cache: dict[int, int] = {}

    d4_rows = 0
    violations = {
        "not_first_tau4": 0,
        "closure_q_gt_square": 0,
        "left_bound_exceeded": 0,
        "combined_bound_exceeded": 0,
        "theta_half_exceeded": 0,
    }
    max_frac_pos = 0.0
    min_margin = None
    examples: dict[str, list] = {k: [] for k in violations}

    for p, q in zip(primes, primes[1:]):
        if q > limit:
            break
        g = q - p
        if g <= 1:
            continue
        interior = list(range(p + 1, q))
        min_tau = min(tau[n] for n in interior)
        w = next(n for n in interior if tau[n] == min_tau)
        if tau[w] != 4:
            continue
        d4_rows += 1
        r = w - p
        m = q - w
        frac_pos = r / g
        max_frac_pos = max(max_frac_pos, frac_pos)
        min_margin = m if min_margin is None else min(min_margin, m)

        first_r = first_tau4_offset(p, q, tau)
        if first_r != r:
            violations["not_first_tau4"] += 1
            if len(examples["not_first_tau4"]) < 5:
                examples["not_first_tau4"].append({"p": p, "q": q, "w": w, "first_r": first_r})

        sq = next_prime_square_after(w, primes)
        if q > sq:
            violations["closure_q_gt_square"] += 1
            if len(examples["closure_q_gt_square"]) < 5:
                examples["closure_q_gt_square"].append({"p": p, "q": q, "w": w, "S+": sq})

        if p not in r_sda_cache:
            r_sda_cache[p] = r_sda_analytic(p)
        R = r_sda_cache[p]
        left_bound = R / g
        right_bound = 1 - m / g
        combined = min(left_bound, right_bound)
        if frac_pos > left_bound + 1e-12:
            violations["left_bound_exceeded"] += 1
        if frac_pos > combined + 1e-12:
            violations["combined_bound_exceeded"] += 1
            if len(examples["combined_bound_exceeded"]) < 5:
                examples["combined_bound_exceeded"].append(
                    {"p": p, "q": q, "w": w, "frac_pos": frac_pos, "bound": combined, "R": R, "m": m, "g": g}
                )
        if frac_pos > 0.5 + 1e-12:
            violations["theta_half_exceeded"] += 1

    structural_total = (
        violations["not_first_tau4"]
        + violations["closure_q_gt_square"]
        + violations["left_bound_exceeded"]
        + violations["combined_bound_exceeded"]
    )
    return {
        "limit": limit,
        "d4_chambers": d4_rows,
        "violations": violations,
        "structural_violation_total": structural_total,
        "theta_half_invalidated": violations["theta_half_exceeded"] > 0,
        "max_frac_pos": max_frac_pos,
        "min_right_margin": min_margin,
        "examples": examples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()

    started = time.perf_counter()
    result = analyze_d4_bounds(args.limit)
    result["runtime_seconds"] = time.perf_counter() - started

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"pgs_d4_frac_pos_falsification_{args.limit}.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"Wrote {out}")
    return 0 if result["structural_violation_total"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())