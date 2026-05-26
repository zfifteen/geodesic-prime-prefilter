#!/usr/bin/env python3
"""
Stage 1 (initial refinement): Local Deconvolution Model using GWR Envelope
(Core Insight Decisive Test)

PGS objects first: same as Stage 0 + the explicit GWR selector-to-packet coefficient
envelope already proved in local_control_of_prime_power_packets_by_gwr_ordering.md
and folded_packet_drift_inequality.md:

  n < w  ⇒ λ(n) < log(w) / d
  w < n < q ⇒ λ(n) < log(q) / (d-1)

where w = GWR point, d = τ(w).

This script re-computes the packet contributions D and R using the GWR-bounded
λ envelopes (a faithful local model of the deconvolution effect on the interior
support relative to the GWR minimum) instead of the conservative upper bound.

It then adds the Core Insight δ_GWR and compares the resulting effective ratio
to the Stage 0 baseline on the same regime.

All output uses mandatory strict separation language only.

Candidate construction under test on regime [Stage 1 local GWR-envelope deconvolution model].
Observed on finite set. The live target remains fully open.
"""

import math
import csv
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np
import matplotlib.pyplot as plt

# Reuse the exact helpers from Stage 0 (in practice one would import or share a module)
# For self-contained execution we duplicate the minimal necessary logic.

def divisor_counts(limit: int) -> List[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau

def find_primes_and_chambers(limit: int) -> Tuple[List[Tuple[int, int]], List[int]]:
    tau = divisor_counts(limit)
    primes = [n for n in range(2, limit + 1) if tau[n] == 2]
    chambers = [(primes[i], primes[i+1]) for i in range(len(primes)-1)]
    return chambers, tau

def e_n(n: int, tau_n: int) -> float:
    if n <= 1: return 0.0
    return (tau_n / 2.0 - 1.0) * math.log(n)

def find_gwr_in_chamber(p: int, q: int, tau: List[int]) -> int:
    min_e = float("inf")
    gwr = p + 1
    for n in range(p + 1, q):
        e = e_n(n, tau[n])
        if e < min_e:
            min_e = e
            gwr = n
    return gwr

def build_packet(p: int, q: int, tau: List[int]) -> List[int]:
    packet = [q]
    for r in range(2, int(math.sqrt(q)) + 1):
        if tau[r] != 2: continue
        val = r * r
        while val < q:
            if val > p: packet.append(val)
            val *= r
    return sorted(set(packet))

def centered_x(n: int, p: int, q: int) -> float:
    return math.log(n) - 0.5 * (math.log(p) + math.log(q))

def lambda_n(n: int, q: int) -> float:
    if n == q: return math.log(q)
    return math.log(n)   # conservative

def main():
    out_dir = Path("experiments/core-insight-decisive-test")
    out_dir.mkdir(parents=True, exist_ok=True)

    max_prime = 15000
    z = 1.0

    chambers, tau = find_primes_and_chambers(max_prime)

    rows = []
    for idx, (p, q) in enumerate(chambers):
        if q - p < 2: continue
        gwr = find_gwr_in_chamber(p, q, tau)
        packet = build_packet(p, q, tau)
        scale = math.log(q / p)
        e_gwr = e_n(gwr, tau[gwr])
        delta_gwr = e_gwr * scale

        d = tau[gwr]   # GWR minimum divisor count

        raw_D_gwr_bounded = 0.0
        raw_R_gwr_bounded = 0.0

        for n in packet:
            x = centered_x(n, p, q)
            # Use GWR envelope for interior points (exact on the document statements)
            if n < gwr:
                lam = math.log(gwr) / d
            elif n > gwr and n < q:
                lam = math.log(q) / (d - 1)
            else:
                lam = lambda_n(n, q)   # endpoint or GWR itself

            J = x / (z + x*x)
            K = 1.0 / (z + x*x)
            raw_D_gwr_bounded += lam * J
            raw_R_gwr_bounded += lam * K

        effective_R = raw_R_gwr_bounded + delta_gwr
        ratio = effective_R / scale if scale > 0 else 0.0

        rows.append({
            "chamber_index": idx,
            "p": p, "q": q, "gwr": gwr,
            "scale": round(scale, 8),
            "delta_gwr": round(delta_gwr, 8),
            "raw_R_gwr_bounded": round(raw_R_gwr_bounded, 8),
            "effective_R_after_delta": round(effective_R, 8),
            "ratio": round(ratio, 8),
        })

    # Write CSV
    csv_path = out_dir / "stage1_gwr_bounded_vs_drift.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    ratios = [r["ratio"] for r in rows]
    scales = [r["scale"] for r in rows]
    min_ratio = min(ratios)
    median_ratio = float(np.median(ratios))

    # Plot
    plt.figure(figsize=(9,5))
    plt.scatter(scales, ratios, s=10, alpha=0.5, color="#1a7a4c")
    plt.axhline(y=0, color="red", linestyle="--", linewidth=1)
    plt.axhline(y=median_ratio, color="green", linestyle=":", linewidth=1, label=f"median ≈ {median_ratio:.2f}")
    plt.xlabel("Chamber scale log(q/p)")
    plt.ylabel("Effective reserve after GWR δ (GWR-bounded λ) / scale")
    plt.title("Stage 1: GWR Envelope Deconvolution Model + Core Insight δ\nCandidate construction under test. Live target remains fully open.")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plot_path = out_dir / "stage1_gwr_bounded_ratio_vs_scale.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()

    # Strict report
    report = f"""Candidate construction under test on regime [Stage 1 local GWR-envelope deconvolution model, 1752 chambers, z=1.0].
PGS objects surfaced: ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR point w with d=τ(w),
deconvolved packet support P(p,q), centered x_n, J_z/K_z kernels, and the explicit GWR selector-to-packet coefficient
envelope (n<w ⇒ λ(n) < log(w)/d ; w<n<q ⇒ λ(n) < log(q)/(d-1)) from the reduction documents.

Observed on this finite set (1752 chambers):
  min ratio (GWR-bounded effective reserve after δ / scale) = {min_ratio:.6f}
  median ratio = {median_ratio:.6f}

The packet contributions D and R were recomputed using the GWR-bounded λ envelopes (a direct local model of the
effect of deconvolution relative to the GWR minimum). The Core Insight δ was then added exactly as before.

This is a refinement of the Stage 0 baseline using only already-proved local GWR control. No global objects used.

The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open.
No obligation discharged. Finite measured diagnostic on toy regime only.

CSV: {csv_path}
Plot: {plot_path}
"""
    (out_dir / "stage1_strict_report.txt").write_text(report)
    print(report)
    print(f"Artifacts in {out_dir}")

if __name__ == "__main__":
    main()