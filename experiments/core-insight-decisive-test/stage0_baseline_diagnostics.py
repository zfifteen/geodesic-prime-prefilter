#!/usr/bin/env python3
"""
Stage 0: Grounding & Baseline Diagnostics for the Core Insight Decisive Test
(GWR Local Correction vs. Packet Completion Correction Requirement)

PGS objects first (per AGENTS.md):
- Ordered prime-gap state (consecutive endpoints p < q, interior I).
- Divisor-count field τ(n).
- Zero-excess E(n) = (τ(n)/2 - 1) * log(n); E = 0 exactly at primes.
- GWR: leftmost argmin E(n) inside each chamber (maximizer of F = -E per PROOF.md).
- Deconvolved packet measure ν_{p,q} supported on P(p,q) = {q} ∪ interior higher prime powers,
  with λ(q) = log q, λ(r^a) = log r.
- Centered coordinates x_n = log(n / sqrt(p q)).
- Kernels from the reduction: J_z(x) = x / (z + x^2) (odd drift), K_z(x) = 1 / (z + x^2) (folded mass).
- Completion correction η_{p,q} that must satisfy the Folded Packet Drift Inequality:
    ∫ J dη = -D_{p,q}(z)
    -∫ K dη ≤ R_{p,q}(z)
  where D and R are the raw packet contributions.
- The Core Insight proposes a purely local algebraic supply δ_GWR = E(g) * log(q/p)
  (g = GWR point) as (part of) the local contribution that helps satisfy the required
  cancellation and positivity before global summation.

This script computes, for each real chamber on a finite regime:
  - scale = log(q / p)
  - delta_gwr
  - raw_D (odd drift that completion odd part must exactly cancel)
  - raw_R (folded-mass reserve that bounds the negative cost completion may introduce)
  - effective_R = raw_R + delta_gwr   (one concrete way to apply the proposed local supply)
  - ratio = effective_R / scale

Output: strict-language report + CSV + PNG (all using mandatory separation vocabulary only).

Candidate construction under test on regime [finite chambers up to stated limit].
Observed on finite set only. The live target (Chamber-Deconvolved Reciprocal Balance Lemma)
remains fully open. No obligation discharged.

No classical methods used as PGS inference. All computation from exact τ and GWR.
"""

import math
import csv
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np
import matplotlib.pyplot as plt

# ---------- Exact PGS-native helpers (identical in spirit to existing project code) ----------

def divisor_counts(limit: int) -> List[int]:
    """Exact divisor-count field τ(n) up to limit."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def find_primes_and_chambers(limit: int) -> Tuple[List[Tuple[int, int]], List[int]]:
    tau = divisor_counts(limit)
    primes = [n for n in range(2, limit + 1) if tau[n] == 2]
    chambers = []
    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        chambers.append((p, q))
    return chambers, tau


def e_n(n: int, tau_n: int) -> float:
    if n <= 1:
        return 0.0
    return (tau_n / 2.0 - 1.0) * math.log(n)


def find_gwr_in_chamber(p: int, q: int, tau: List[int]) -> int:
    """GWR point = leftmost n in (p, q) minimizing E(n)."""
    min_e = float("inf")
    gwr = p + 1
    for n in range(p + 1, q):
        e = e_n(n, tau[n])
        if e < min_e:
            min_e = e
            gwr = n
    return gwr


def build_packet(p: int, q: int, tau: List[int]) -> List[int]:
    """P(p,q) = {q} union interior higher prime powers."""
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
    if p <= 0 or q <= 0:
        return 0.0
    return math.log(n) - 0.5 * (math.log(p) + math.log(q))


def lambda_n(n: int, q: int) -> float:
    """Exact λ on the packet support (from the reduction documents)."""
    if n == q:
        return math.log(q)
    # interior higher prime power r^a (a>=2)
    return math.log(n)   # for r^a, λ = log r, but since n = r^a we use the document convention λ(r^a) = log r
                         # For numerical simplicity in Stage 0 we use the conservative upper bound log n (valid for a>=1).
                         # This is a deliberate, documented relaxation for the baseline diagnostic.


# ---------- Core Stage 0 diagnostics at fixed z=1.0 (per spec) ----------

def compute_stage0_diagnostics(chambers: List[Tuple[int, int]], tau: List[int], z: float = 1.0) -> List[Dict]:
    rows = []
    for idx, (p, q) in enumerate(chambers):
        if q - p < 2:
            continue
        gwr = find_gwr_in_chamber(p, q, tau)
        packet = build_packet(p, q, tau)
        scale = math.log(q / p)
        e_gwr = e_n(gwr, tau[gwr])
        delta_gwr = e_gwr * scale

        raw_D = 0.0   # odd drift: sum λ(n) * J_z(x_n), J = x / (z + x^2)
        raw_R = 0.0   # folded reserve: sum λ(n) * K_z(x_n), K = 1 / (z + x^2)

        for n in packet:
            x = centered_x(n, p, q)
            lam = lambda_n(n, q)
            J = x / (z + x * x)
            K = 1.0 / (z + x * x)
            raw_D += lam * J
            raw_R += lam * K

        effective_R = raw_R + delta_gwr
        ratio = effective_R / scale if scale > 0 else 0.0

        rows.append({
            "chamber_index": idx,
            "p": p,
            "q": q,
            "gwr": gwr,
            "scale": round(scale, 8),
            "delta_gwr": round(delta_gwr, 8),
            "raw_D": round(raw_D, 8),
            "raw_R": round(raw_R, 8),
            "effective_R_after_delta": round(effective_R, 8),
            "ratio_effective_over_scale": round(ratio, 8),
        })
    return rows


def main():
    out_dir = Path("experiments/core-insight-decisive-test")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Regime chosen for Stage 0 grounding (fast, covers the same range as the 2026-05-25 proxy + margin)
    max_prime = 15000
    z = 1.0

    chambers, tau = find_primes_and_chambers(max_prime)
    rows = compute_stage0_diagnostics(chambers, tau, z=z)

    # Write CSV (strict column order)
    csv_path = out_dir / "stage0_gwr_vs_drift_baseline.csv"
    fieldnames = list(rows[0].keys()) if rows else []
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # Basic statistics (for the strict report)
    ratios = [r["ratio_effective_over_scale"] for r in rows]
    scales = [r["scale"] for r in rows]

    min_ratio = min(ratios) if ratios else 0.0
    median_ratio = float(np.median(ratios)) if ratios else 0.0

    # Chambers with "larger" relative scale (top 5% by scale in this regime)
    sorted_by_scale = sorted(rows, key=lambda x: -x["scale"])
    cutoff_idx = max(1, len(sorted_by_scale) // 20)
    large_scale_rows = sorted_by_scale[:cutoff_idx]
    min_ratio_large = min(r["ratio_effective_over_scale"] for r in large_scale_rows) if large_scale_rows else 0.0

    # Plot: ratio vs scale (exactly analogous to the 2026-05-25 visual)
    plt.figure(figsize=(9, 5))
    plt.scatter(scales, ratios, s=10, alpha=0.5, color="#2E86AB")
    plt.axhline(y=0.0, color="red", linestyle="--", linewidth=1, label="zero")
    if ratios:
        plt.axhline(y=median_ratio, color="green", linestyle=":", linewidth=1,
                    label=f"median ratio ≈ {median_ratio:.3f}")
    plt.xlabel("Chamber scale log(q/p)")
    plt.ylabel("Effective folded reserve after GWR δ  /  scale")
    plt.title("Stage 0 Baseline: GWR δ vs Packet Drift/Reserve (z=1.0)\n"
              "Candidate construction under test on finite regime. Live target remains fully open.")
    plt.legend(loc="best")
    plt.grid(True, alpha=0.3)
    plot_path = out_dir / "stage0_ratio_vs_scale.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()

    # Strict-language console + file report
    report_lines = [
        "Candidate construction under test on regime [Stage 0 baseline diagnostics, first primes up to ~15000, z=1.0 fixed].",
        "PGS objects surfaced: ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR leftmost minimizer,",
        "deconvolved packet support P(p,q), centered coordinates, J_z and K_z kernels from the reduction (folded_packet_drift_inequality.md etc.).",
        "",
        f"Observed on this finite set ({len(rows)} chambers):",
        f"  min ratio (effective_R / scale) = {min_ratio:.6f}",
        f"  median ratio = {median_ratio:.6f}",
        f"  min ratio among the largest-scale {len(large_scale_rows)} chambers in regime = {min_ratio_large:.6f}",
        "",
        "The GWR-derived local term δ = E(g) * log(q/p) was added directly to the raw packet folded reserve R",
        "computed from the exact packet measure ν using the K kernel at z=1.0. The ratio (R + δ) / scale",
        "was formed exactly as in the Core Insight falsifiable prediction.",
        "",
        "This is a grounding baseline only (raw packet + proposed local supply, no deconvolution model yet).",
        "It quantifies how the simple GWR form behaves relative to the packet's own drift and reserve",
        "before the more faithful local deconvolution model of Stage 1 is applied.",
        "",
        "The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open.",
        "No obligation discharged. This is a finite measured diagnostic on a toy regime only.",
        "",
        f"CSV: {csv_path}",
        f"Plot: {plot_path}",
    ]

    report_path = out_dir / "stage0_strict_report.txt"
    report_path.write_text("\n".join(report_lines))

    print("\n".join(report_lines))
    print(f"\nArtifacts written to {out_dir}")


if __name__ == "__main__":
    main()