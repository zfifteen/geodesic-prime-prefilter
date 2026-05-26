#!/usr/bin/env python3
"""
Minimal deterministic probe for the Core Insight hypothesis
("Per-Chamber Positivity from the GWR Maximizer Identity").

For each successive real prime-gap chamber [p, q]:
  - Find the GWR point w = leftmost n in (p, q) with minimal τ(n).
  - Compute a simple GWR-derived local correction δ using only E(w) and log(q/p).
  - Form the packet (q + interior prime powers), centered coordinates x_n.
  - Compute the net signed contribution of this chamber to the folded kernel
    at a fixed moderate z (e.g. z=1.0) both before and after the correction.
  - Record the ratio: (net contribution after δ) / log(q/p)

Look for whether this ratio stays above some positive lower bound for larger chambers.

This is a cheap, fully reproducible, finite check using only exact divisor counts.
No statistics over many packets, no limits, no classical zeta machinery.

Run this script directly. It produces:
  - A CSV with per-chamber data
  - A simple plot (saved as PNG) showing the ratio vs chamber scale

Requirements: matplotlib, numpy (standard scientific Python stack).
"""

import math
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ---------- PGS-native helpers (same spirit as the project's harness) ----------

def divisor_counts(limit: int) -> list[int]:
    """Exact divisor-count field τ(n) up to limit."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau

def find_primes_and_chambers(limit: int):
    """
    Return list of (p, q) chambers where p and q are consecutive primes
    up to limit, using exact τ.
    """
    tau = divisor_counts(limit)
    primes = [n for n in range(2, limit + 1) if tau[n] == 2]
    chambers = []
    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        chambers.append((p, q))
    return chambers, tau

def e_n(n: int, tau_n: int) -> float:
    """Zero-excess coordinate E(n) = (τ(n)/2 - 1) * log(n)."""
    if n <= 1:
        return 0.0
    return (tau_n / 2.0 - 1.0) * math.log(n)

def find_gwr_in_chamber(p: int, q: int, tau: list[int]) -> int:
    """
    GWR point: leftmost n in (p, q) that minimizes E(n), i.e. minimizes τ(n)
    and takes the leftmost in case of ties (as per the project's convention).
    """
    min_e = float("inf")
    gwr = p + 1
    for n in range(p + 1, q):
        e = e_n(n, tau[n])
        if e < min_e:
            min_e = e
            gwr = n
    return gwr

def build_packet(p: int, q: int, tau: list[int]) -> list[int]:
    """Packet = {q} union interior prime powers r^a (a>=2) with p < r^a < q."""
    packet = [q]
    for r in range(2, int(math.sqrt(q)) + 1):
        if tau[r] != 2:
            continue
        val = r * r
        while val < q:
            if val > p:
                packet.append(val)
            val *= r
    return sorted(set(packet))

def centered_x(n: int, p: int, q: int) -> float:
    """Centered log coordinate inside the chamber."""
    if p <= 0 or q <= 0:
        return 0.0
    return math.log(n) - 0.5 * (math.log(p) + math.log(q))

# ---------- Simple GWR-derived local correction (the hypothesis under test) ----------

def proposed_local_correction(p: int, q: int, gwr: int, tau: list[int]) -> float:
    """
    A minimal concrete proposal for the "GWR-derived local correction" δ.

    This is deliberately simple and local:
      δ = E(gwr) * log(q / p)   (or a small multiple; the exact constant
                                 can be tuned later, but the functional form
                                 is what the Core Insight claims is forced
                                 by the maximizer property).

    The hypothesis is that after adding this δ to the packet's folded
    contribution, the net per-chamber mass is nonnegative (or at least
    bounded below by a positive multiple of the chamber scale) for all
    sufficiently large chambers.
    """
    if p <= 1 or q <= p:
        return 0.0
    e_gwr = e_n(gwr, tau[gwr])
    scale = math.log(q / p)
    return e_gwr * scale

# ---------- The actual probe ----------

def run_probe(max_prime: int = 5000, z: float = 1.0):
    """
    For each real chamber up to max_prime:
      - Find GWR point
      - Build packet
      - Compute net signed contribution at fixed z, before and after the
        proposed local correction.
      - Record ratio = (net after correction) / log(q/p)

    Saves:
      - CSV with the data
      - PNG plot of the ratio vs chamber scale
    """
    chambers, tau = find_primes_and_chambers(max_prime)

    rows = []
    for idx, (p, q) in enumerate(chambers):
        if q - p < 2:
            continue

        gwr = find_gwr_in_chamber(p, q, tau)
        packet = build_packet(p, q, tau)
        delta = proposed_local_correction(p, q, gwr, tau)
        scale = math.log(q / p)

        # Raw packet contribution at this z (before any correction)
        raw_sum = 0.0
        for n in packet:
            x = centered_x(n, p, q)
            raw_sum += 1.0 / (z + x * x)

        # After the proposed local correction (simple additive shift in the
        # folded picture for this fixed z; this is a minimal proxy for the
        # "local completion correction" in the Core Insight)
        corrected_sum = raw_sum + delta

        ratio = corrected_sum / scale if scale > 0 else 0.0

        rows.append({
            "chamber_index": idx,
            "p": p,
            "q": q,
            "gwr": gwr,
            "scale_log_q_over_p": round(scale, 6),
            "raw_folded_at_z": round(raw_sum, 6),
            "delta_proposed": round(delta, 6),
            "corrected_folded_at_z": round(corrected_sum, 6),
            "ratio_corrected_over_scale": round(ratio, 6),
        })

    # Write CSV
    out_dir = Path("experiments/brainstorm")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "gwr_local_correction_probe.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Simple plot: ratio vs chamber scale
    scales = [r["scale_log_q_over_p"] for r in rows]
    ratios = [r["ratio_corrected_over_scale"] for r in rows]

    plt.figure(figsize=(9, 5))
    plt.scatter(scales, ratios, s=12, alpha=0.6, color="#2E86AB")
    plt.axhline(y=0.0, color="red", linestyle="--", linewidth=1, label="zero")
    # Optional: a very crude "looks positive" reference line
    if ratios:
        positive_ratios = [r for r in ratios if r > 0]
        if positive_ratios:
            median_pos = float(np.median(positive_ratios))
            plt.axhline(y=median_pos, color="green", linestyle=":", linewidth=1,
                        label=f"median of positive ratios ≈ {median_pos:.3f}")

    plt.xlabel("Chamber scale log(q/p)")
    plt.ylabel("Net contribution after proposed GWR correction  /  scale")
    plt.title("Core Insight Probe: Per-Chamber Ratio after Local Correction\n"
              "(larger chambers should stay above some positive floor if the hypothesis holds)")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)

    plot_path = out_dir / "gwr_local_correction_ratio_vs_scale.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"CSV written to:  {csv_path}")
    print(f"Plot written to: {plot_path}")
    print(f"Total chambers examined: {len(rows)}")
    if ratios:
        print(f"Median ratio (all chambers): {float(np.median(ratios)):.4f}")
        pos = [r for r in ratios if r > 0]
        if pos:
            print(f"Median ratio (positive only): {float(np.median(pos)):.4f}")

if __name__ == "__main__":
    # Feel free to increase max_prime (5000 is fast; 20000 is still seconds).
    run_probe(max_prime=8000, z=1.0)
