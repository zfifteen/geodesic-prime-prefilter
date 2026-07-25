#!/usr/bin/env python3
"""Falsification probe: Gap Winner as one-way complexity valve.

PGS objects first:
  - consecutive prime gap (p, q)
  - divisor-count field tau on the interior
  - Gap Winner w = leftmost interior argmin tau
  - pre-valve interval (p, w) and residual interval (w, q)

Primary prediction under attack (share H1):
  mean(tau on residual) > mean(tau on pre-valve)
  whenever both intervals are nonempty.

Field prep uses divisor accumulation and tau==2 primes.
No primality API, Miller-Rabin, or gcd gate chooses the valve or the decision.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


def dynamic_cutoff(q: int) -> int:
    """Compression window C(q) = max(64, ceil(0.5 * log(q)^2))."""
    return max(64, math.ceil(0.5 * math.log(q) ** 2))


def divisor_counts(limit: int) -> list[int]:
    """Exact tau[n] for n in 0..limit (linear accumulation, field prep)."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def primes_from_tau(tau: list[int]) -> list[int]:
    """Primes as n with tau[n] == 2."""
    return [n for n in range(2, len(tau)) if tau[n] == 2]


def leftmost_min_tau(p: int, q: int, tau: list[int]) -> tuple[int, int]:
    """Return (w, min_tau) for leftmost interior argmin of tau."""
    first = p + 1
    last = q - 1
    min_tau = tau[first]
    w = first
    for n in range(first + 1, last + 1):
        t = tau[n]
        if t < min_tau:
            min_tau = t
            w = n
    return w, min_tau


def interval_mean(lo: int, hi_exclusive: int, tau: list[int]) -> float | None:
    """Mean of tau on integer interval [lo, hi_exclusive). Empty -> None."""
    if hi_exclusive <= lo:
        return None
    total = 0
    count = 0
    for n in range(lo, hi_exclusive):
        total += tau[n]
        count += 1
    return total / count


def spearman_rho(xs: list[float], ys: list[float]) -> float | None:
    """Spearman rank correlation. Returns None if undefined (n < 2 or ties all)."""
    n = len(xs)
    if n < 2 or n != len(ys):
        return None

    def ranks(vals: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: vals[i])
        out = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            # average rank for ties (1-based ranks)
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    rx = ranks(xs)
    ry = ranks(ys)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for a, b in zip(rx, ry):
        da = a - mx
        db = b - my
        num += da * db
        dx2 += da * da
        dy2 += db * db
    if dx2 == 0.0 or dy2 == 0.0:
        return None
    return num / math.sqrt(dx2 * dy2)


@dataclass(frozen=True)
class GapRow:
    p: int
    q: int
    gap: int
    w: int
    tau_w: int
    offset: int
    cutoff: int
    in_window: bool
    eligible: bool
    mean_pre: float | None
    mean_res: float | None
    ratio: float | None
    ratio_le_1: bool
    nls_undercut: bool
    undercut_n: int | None
    undercut_tau: int | None
    n_pre: int
    n_res: int


def analyze_gap(p: int, q: int, tau: list[int]) -> GapRow | None:
    """Analyze one gap. Twin / empty interior returns None (silent skip)."""
    if q - p < 2:
        return None
    if q - p == 2:
        # empty interior: out of scope for valve means
        return None

    w, min_tau = leftmost_min_tau(p, q, tau)
    # Pre-valve: (p, w) = [p+1, w); residual: (w, q) = [w+1, q)
    n_pre = max(0, w - (p + 1))
    n_res = max(0, (q - 1) - w)
    mean_pre = interval_mean(p + 1, w, tau)
    mean_res = interval_mean(w + 1, q, tau)
    eligible = mean_pre is not None and mean_res is not None

    ratio: float | None = None
    ratio_le_1 = False
    if eligible and mean_pre is not None and mean_res is not None:
        if mean_pre == 0.0:
            # tau is always >= 2 on composites/primes; defensive
            ratio = float("inf") if mean_res > 0 else float("nan")
        else:
            ratio = mean_res / mean_pre
        ratio_le_1 = bool(ratio <= 1.0)

    undercut_n: int | None = None
    undercut_tau: int | None = None
    nls_undercut = False
    for n in range(w + 1, q):
        if tau[n] < min_tau:
            nls_undercut = True
            undercut_n = n
            undercut_tau = tau[n]
            break

    cutoff = dynamic_cutoff(q)
    offset = w - p
    return GapRow(
        p=p,
        q=q,
        gap=q - p,
        w=w,
        tau_w=min_tau,
        offset=offset,
        cutoff=cutoff,
        in_window=offset <= cutoff,
        eligible=eligible,
        mean_pre=mean_pre,
        mean_res=mean_res,
        ratio=ratio,
        ratio_le_1=ratio_le_1,
        nls_undercut=nls_undercut,
        undercut_n=undercut_n,
        undercut_tau=undercut_tau,
        n_pre=n_pre,
        n_res=n_res,
    )


def run_probe(
    p_max: int,
    p_min: int = 11,
    sample_ce_cap: int = 50,
) -> dict[str, Any]:
    """Scan consecutive gaps with left prime in [p_min, p_max]."""
    t0 = time.time()
    # Extra room so the last left prime near p_max still has a next prime.
    hard_limit = p_max + max(400, int(2 * math.log(p_max + 3) ** 2) + 100)
    tau = divisor_counts(hard_limit)
    primes = primes_from_tau(tau)

    rows_eligible_ratios: list[float] = []
    rows_eligible_tau_w: list[float] = []
    n_gaps_nonempty = 0
    n_eligible = 0
    n_one_sided = 0
    n_ratio_le_1 = 0
    n_nls_undercuts = 0
    n_out_of_window = 0
    n_in_window = 0

    bucket_sums: dict[int, float] = defaultdict(float)
    bucket_counts: dict[int, int] = defaultdict(int)
    counterexamples: list[dict[str, Any]] = []
    undercuts: list[dict[str, Any]] = []

    for i, p in enumerate(primes):
        if p < p_min:
            continue
        if p > p_max:
            break
        if i + 1 >= len(primes):
            break
        q = primes[i + 1]
        if q >= hard_limit:
            # incomplete field for this gap
            break
        row = analyze_gap(p, q, tau)
        if row is None:
            continue
        n_gaps_nonempty += 1

        if row.nls_undercut:
            n_nls_undercuts += 1
            if len(undercuts) < sample_ce_cap:
                undercuts.append(asdict(row))

        if not row.eligible:
            n_one_sided += 1
            continue

        n_eligible += 1
        assert row.ratio is not None
        rows_eligible_ratios.append(float(row.ratio))
        rows_eligible_tau_w.append(float(row.tau_w))
        bucket_sums[row.tau_w] += float(row.ratio)
        bucket_counts[row.tau_w] += 1

        if row.ratio_le_1:
            n_ratio_le_1 += 1
            if len(counterexamples) < sample_ce_cap:
                counterexamples.append(asdict(row))

        if row.in_window:
            n_in_window += 1
        else:
            n_out_of_window += 1

    rho = spearman_rho(rows_eligible_tau_w, rows_eligible_ratios)

    buckets: list[dict[str, Any]] = []
    for t in sorted(bucket_counts):
        c = bucket_counts[t]
        buckets.append(
            {
                "tau_w": t,
                "n": c,
                "mean_ratio": bucket_sums[t] / c,
            }
        )

    # Adjacent high-sample bucket decreases (weak H2 pressure).
    adjacent_decreases: list[dict[str, Any]] = []
    high = [b for b in buckets if b["n"] >= 50]
    for a, b in zip(high, high[1:]):
        if b["mean_ratio"] < a["mean_ratio"]:
            adjacent_decreases.append(
                {
                    "tau_a": a["tau_w"],
                    "mean_ratio_a": a["mean_ratio"],
                    "n_a": a["n"],
                    "tau_b": b["tau_w"],
                    "mean_ratio_b": b["mean_ratio"],
                    "n_b": b["n"],
                }
            )

    # Outcome labels for this regime only.
    h1_falsified = n_ratio_le_1 > 0
    h2_falsified = (
        n_eligible >= 1000 and (rho is None or rho <= 0.0)
    )
    h3_failed = n_nls_undercuts > 0

    if h1_falsified:
        h1_status = "falsified"
    else:
        h1_status = "did_not_falsify"

    if n_eligible < 1000:
        h2_status = "insufficient_eligible_for_hard_rule"
    elif h2_falsified:
        h2_status = "falsified"
    else:
        h2_status = "did_not_falsify"

    if h3_failed:
        h3_status = "surface_failure"
    else:
        h3_status = "did_not_falsify"

    elapsed = time.time() - t0
    mean_ratio_all = (
        sum(rows_eligible_ratios) / len(rows_eligible_ratios)
        if rows_eligible_ratios
        else None
    )
    frac_ratio_le_1 = (
        n_ratio_le_1 / n_eligible if n_eligible else None
    )
    frac_out_window = (
        n_out_of_window / n_eligible if n_eligible else None
    )

    return {
        "hypothesis": "gap_winner_one_way_complexity_valve",
        "status_language": "measured_on_regime_only",
        "regime": {
            "p_min": p_min,
            "p_max": p_max,
            "hard_limit": hard_limit,
        },
        "counts": {
            "gaps_nonempty_interior": n_gaps_nonempty,
            "eligible_both_sides_nonempty": n_eligible,
            "one_sided_ineligible": n_one_sided,
            "ratio_le_1": n_ratio_le_1,
            "nls_undercuts": n_nls_undercuts,
            "in_window": n_in_window,
            "out_of_window": n_out_of_window,
        },
        "metrics": {
            "mean_ratio_eligible": mean_ratio_all,
            "frac_ratio_le_1": frac_ratio_le_1,
            "spearman_tau_w_vs_ratio": rho,
            "frac_out_of_window": frac_out_window,
        },
        "buckets_by_tau_w": buckets,
        "adjacent_high_sample_decreases": adjacent_decreases,
        "outcomes": {
            "H1_residual_mean_elevation": h1_status,
            "H2_ratio_scales_with_tau_w": h2_status,
            "H3_nls_consistency": h3_status,
            "H1_falsified": h1_falsified,
            "H2_falsified": h2_falsified,
            "H3_surface_failure": h3_failed,
            "H2_adjacent_decreases": len(adjacent_decreases),
        },
        "sample_ratio_le_1": counterexamples,
        "sample_nls_undercuts": undercuts,
        "elapsed_seconds": elapsed,
    }


def write_ce_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Falsify residual mean elevation after Gap Winner valve"
    )
    parser.add_argument("--p-min", type=int, default=11)
    parser.add_argument("--p-max", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--csv-ce",
        type=Path,
        default=None,
        help="Optional CSV of ratio<=1 counter-example samples",
    )
    parser.add_argument("--sample-ce-cap", type=int, default=50)
    args = parser.parse_args()

    result = run_probe(
        p_max=args.p_max,
        p_min=args.p_min,
        sample_ce_cap=args.sample_ce_cap,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    if args.csv_ce is not None:
        write_ce_csv(args.csv_ce, result["sample_ratio_le_1"])

    o = result["outcomes"]
    c = result["counts"]
    m = result["metrics"]
    print(
        json.dumps(
            {
                "p_max": args.p_max,
                "eligible": c["eligible_both_sides_nonempty"],
                "ratio_le_1": c["ratio_le_1"],
                "nls_undercuts": c["nls_undercuts"],
                "mean_ratio": m["mean_ratio_eligible"],
                "spearman": m["spearman_tau_w_vs_ratio"],
                "H1": o["H1_residual_mean_elevation"],
                "H2": o["H2_ratio_scales_with_tau_w"],
                "H3": o["H3_nls_consistency"],
                "elapsed_s": round(result["elapsed_seconds"], 3),
                "out": str(args.out),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
