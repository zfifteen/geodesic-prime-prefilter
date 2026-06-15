#!/usr/bin/env python3
"""Chamber budget and packet-drift analyzer for PGS-RH placement empirics.

PGS objects (source-first):
  - ordered prime-gap chambers I = {p+1, ..., q-1}
  - divisor-count field tau(n)
  - zero-excess E(n) = (tau(n)/2 - 1) * log(n)
  - GWR carrier w = leftmost argmin E(n) in I
  - excess budget B(I) = sum_{n in I} E(n)
  - fractional position frac_pos(w) = (w - p) / (q - p)

Audit/comparison only. Does not choose primes or perform PGS inference.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import time
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = Path(__file__).resolve().parent


def sieve_primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0] = 0
    if limit >= 1:
        is_prime[1] = 0
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            step = p
            start = p * p
            is_prime[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i in range(2, limit + 1) if is_prime[i]]


def build_tau_table(limit: int) -> list[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            tau[m] += 1
    return tau


def zero_excess(n: int, tau: list[int]) -> float:
    return (tau[n] / 2.0 - 1.0) * math.log(n)


def smallest_prime_factor(n: int) -> int | None:
    if n < 2:
        return None
    if n % 2 == 0:
        return 2
    r = int(n**0.5)
    f = 3
    while f <= r:
        if n % f == 0:
            return f
        f += 2
    return None


def is_prime_trial(n: int) -> bool:
    return n >= 2 and smallest_prime_factor(n) is None


def classify_packet(tau_n: int, n: int) -> str:
    if tau_n == 4:
        spf = smallest_prime_factor(n)
        if spf is None:
            return "d4_other"
        cof = n // spf
        if cof == spf * spf:
            return "d4_prime_cube"
        if cof == spf:
            return "d4_prime_square"
        if is_prime_trial(cof):
            return "d4_semiprime"
        return "d4_other"
    if tau_n == 6:
        return "d6"
    if tau_n >= 8:
        return "d8_plus"
    if tau_n == 3:
        return "d3_prime_square"
    return f"d{tau_n}_other"


def pearson_corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = sum((x - mx) ** 2 for x in xs)
    den_y = sum((y - my) ** 2 for y in ys)
    if den_x == 0 or den_y == 0:
        return float("nan")
    return num / math.sqrt(den_x * den_y)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    k = (len(ordered) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return ordered[int(k)]
    return ordered[f] * (c - k) + ordered[c] * (k - f)


def analyze_chambers(
    limit: int,
    *,
    sample_rows: int = 0,
    csv_path: Path | None = None,
) -> dict:
    tau = build_tau_table(limit)
    primes = sieve_primes(limit)
    rows: list[dict] = []
    frac_positions: list[float] = []
    budgets: list[float] = []
    gap_lengths: list[int] = []
    packet_counts: dict[str, int] = {}

    for p, q in zip(primes, primes[1:]):
        if q > limit:
            break
        gap_len = q - p
        if gap_len <= 1:
            continue
        interior = range(p + 1, q)
        min_tau = min(tau[n] for n in interior)
        w = next(n for n in interior if tau[n] == min_tau)
        budget = sum(zero_excess(n, tau) for n in interior)
        frac_pos = (w - p) / gap_len
        packet = classify_packet(tau[w], w)

        row = {
            "p": p,
            "q": q,
            "gap_len": gap_len,
            "w": w,
            "tau_w": tau[w],
            "frac_pos": frac_pos,
            "budget": budget,
            "packet": packet,
        }
        rows.append(row)
        frac_positions.append(frac_pos)
        budgets.append(budget)
        gap_lengths.append(gap_len)
        packet_counts[packet] = packet_counts.get(packet, 0) + 1

    d4_carrier = sum(1 for r in rows if r["tau_w"] == 4)
    chamber_count = len(rows)

    summary = {
        "limit": limit,
        "chamber_count": chamber_count,
        "frac_pos_mean": statistics.mean(frac_positions) if frac_positions else None,
        "frac_pos_median": statistics.median(frac_positions) if frac_positions else None,
        "frac_pos_p90": percentile(frac_positions, 90),
        "frac_pos_max": max(frac_positions) if frac_positions else None,
        "d4_carrier_count": d4_carrier,
        "d4_carrier_share": d4_carrier / chamber_count if chamber_count else None,
        "budget_gap_len_corr": pearson_corr([float(g) for g in gap_lengths], budgets),
        "packet_counts": packet_counts,
    }

    if csv_path is not None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["p", "q", "gap_len", "w", "tau_w", "frac_pos", "budget", "packet"],
            )
            writer.writeheader()
            out_rows = rows
            if sample_rows > 0 and len(rows) > sample_rows:
                step = len(rows) / sample_rows
                indices = sorted({int(i * step) for i in range(sample_rows)})
                out_rows = [rows[i] for i in indices]
            writer.writerows(out_rows)

    summary["rows_written"] = sample_rows if sample_rows > 0 else len(rows)
    summary["rows_total"] = len(rows)
    return summary


def write_summary_md(summary: dict, path: Path) -> None:
    lines = [
        "# Chamber Budget Analyzer Summary",
        "",
        f"**Limit**: {summary['limit']:,}",
        f"**Nonempty chambers**: {summary['chamber_count']:,}",
        "",
        "## Drift proxy (fractional position of leftmost min-E)",
        "",
        f"- mean: {summary['frac_pos_mean']:.6f}",
        f"- median: {summary['frac_pos_median']:.6f}",
        f"- P90: {summary['frac_pos_p90']:.6f}",
        f"- max: {summary['frac_pos_max']:.6f}",
        "",
        "## Packet dominance at GWR carrier",
        "",
        f"- d=4 carrier count: {summary['d4_carrier_count']:,}",
        f"- d=4 carrier share: {100 * summary['d4_carrier_share']:.4f}%",
        "",
        "## Excess budget B(I)",
        "",
        f"- correlation with gap length: {summary['budget_gap_len_corr']:.6f}",
        "",
        "## Packet classification counts",
        "",
        "| packet | count |",
        "| --- | ---: |",
    ]
    for packet, count in sorted(summary["packet_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {packet} | {count:,} |")
    lines.append("")
    lines.append("Status: measured result on the stated regime. Not a theorem boundary.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1_000_000, help="Upper bound on primes/chambers")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Directory for summary/json/csv artifacts",
    )
    parser.add_argument(
        "--sample-csv",
        type=int,
        default=10_000,
        help="Max rows in sampled CSV (0 = write all chambers)",
    )
    parser.add_argument("--no-csv", action="store_true", help="Skip CSV output")
    args = parser.parse_args(list(argv) if argv is not None else None)

    started = time.perf_counter()
    csv_path = None if args.no_csv else args.out_dir / f"pgs_chamber_budget_gap_stats_{args.limit}.csv"
    summary = analyze_chambers(args.limit, sample_rows=args.sample_csv, csv_path=csv_path)
    summary["runtime_seconds"] = time.perf_counter() - started

    args.out_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.out_dir / f"pgs_chamber_budget_summary_{args.limit}.json"
    md_path = args.out_dir / f"pgs_chamber_budget_summary_{args.limit}.md"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary_md(summary, md_path)

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    if csv_path is not None:
        print(f"Wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())