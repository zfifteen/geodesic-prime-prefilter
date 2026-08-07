#!/usr/bin/env python3
"""
Generate the GWR witness-offset scatter plot and summary statistics.

Requires: sympy, numpy, matplotlib

Usage:
    python generate_witness_offset_plot.py [--limit N]

Default limit is 1_000_000 (primes up to 10^6).
"""

import argparse
import json
import math
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sympy import primerange, nextprime, divisors


def compute_offsets(limit: int):
    """Return lists of ln(q) and (w - p) for every gap with p < limit."""
    ps = list(primerange(10, limit))
    offsets = []
    logs = []
    max_off = 0
    t0 = time.time()
    for i, p in enumerate(ps[:-1]):
        q = nextprime(p)
        interior = range(p + 1, q)
        if not interior:
            continue
        ds = [len(divisors(n)) for n in interior]
        min_d = min(ds)
        w = next(n for n, d in zip(interior, ds) if d == min_d)
        off = w - p
        offsets.append(off)
        logs.append(math.log(q))
        if off > max_off:
            max_off = off
        if i % 10000 == 0 and i > 0:
            print(f"  {i} gaps processed, max offset so far {max_off}, elapsed {time.time()-t0:.1f}s")
    print(f"Finished {len(offsets)} gaps in {time.time()-t0:.1f}s. Max offset = {max_off}")
    return np.array(logs), np.array(offsets)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--out-dir", type=str, default=".")
    args = parser.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"Computing offsets for primes up to {args.limit} ...")
    logs, offsets = compute_offsets(args.limit)

    # Statistics
    stats = {
        "num_gaps": int(len(offsets)),
        "max_offset": int(offsets.max()),
        "mean_offset": float(offsets.mean()),
        "median_offset": float(np.median(offsets)),
        "p90": float(np.percentile(offsets, 90)),
        "p95": float(np.percentile(offsets, 95)),
        "p99": float(np.percentile(offsets, 99)),
        "fraction_offset_le_5": float(np.mean(offsets <= 5)),
        "fraction_offset_le_10": float(np.mean(offsets <= 10)),
        "fraction_offset_le_20": float(np.mean(offsets <= 20)),
        "max_lnq": float(logs.max()),
        "limit": args.limit,
    }
    stats_path = out / "offset_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print("Wrote", stats_path)
    print(json.dumps(stats, indent=2))

    # Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(logs, offsets, c="blue", alpha=0.25, s=6, label="Actual w - p")

    lnqs = np.linspace(logs.min(), logs.max(), 500)
    bounds = np.maximum(64, np.ceil(0.5 * lnqs ** 2))
    ax.plot(lnqs, bounds, "r--", linewidth=2, label="Bound max(64, 0.5 (ln q)^2)")

    ax.set_xlabel("ln(q)", fontsize=12)
    ax.set_ylabel("Witness offset w - p", fontsize=12)
    ax.set_title(
        f"Bounded Compression: GWR Witness Offset vs Bound\n"
        f"(primes from 10 to {args.limit}, {len(offsets)} gaps)",
        fontsize=14,
    )
    ax.legend(loc="upper left")
    ax.set_yscale("log")
    ax.set_ylim(0.8, max(200, bounds.max() * 1.1))
    ax.grid(True, which="both", alpha=0.3)
    plt.tight_layout()

    plot_path = out / f"bounded_compression_{args.limit}.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    print("Wrote", plot_path)


if __name__ == "__main__":
    main()
