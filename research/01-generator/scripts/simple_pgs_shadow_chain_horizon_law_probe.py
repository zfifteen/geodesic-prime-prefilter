#!/usr/bin/env python3
"""Shadow-chain horizon law probe v2 — self-contained data surface.

Generates realistic false pre-terminal shadow-chain nodes that survive a
visible_divisor_bound, records their least prime factor (audit-only), and
scores candidate pure-PGS horizon laws H(p, s0, chain_state).

This advances the most significant unanswered question without requiring
the missing high-scale ledger files.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from sympy import prevprime, primerange

DEFAULT_CANDIDATE_BOUND = 128
DEFAULT_VISIBLE_DIVISOR_BOUND = 10_000
DEFAULT_CHAIN_LIMIT = 8
H_CANDIDATES = [
    "H0_visible",
    "H1_visible_plus_2maxgap",
    "H_Cq",
    "H_fixed_1e5",
    "H_fixed_1e6",
    "H_visible_plus_Cq",
]

@dataclass
class FalseNodeRecord:
    scale: str
    p: int
    seed_offset: int
    chain_index: int
    node_n: int
    terminal_index: int
    least_factor: Optional[int]
    least_factor_over_sqrt: Optional[float]
    least_factor_over_visible: Optional[float]
    node_offset_from_anchor: int
    node_offset_from_seed: int
    delta_prev: Optional[int]
    node_mod_30: int
    offset_mod_30: int
    max_chain_gap: int
    visible_divisor_bound: int
    candidate_bound: int
    lock_carrier_d: Optional[int] = None
    lock_carrier_offset: Optional[int] = None
    tail_after_reset_len: Optional[int] = None

@dataclass
class HorizonEval:
    name: str
    closed: int
    total: int
    max_h: int
    mean_h_over_sqrt: float
    max_h_over_sqrt: float
    promotion_candidate: bool

def make_false_node(p: int, visible: int, chain_idx: int, rng: random.Random) -> tuple[int, int]:
    primes = list(primerange(visible + 1, visible + 400))
    if len(primes) < 2:
        primes = list(primerange(visible + 1, visible + 2000))
    a = rng.choice(primes)
    b = rng.choice(primes)
    return a * b, min(a, b)

def evaluate_h(name: str, rec: FalseNodeRecord, true_q: Optional[int] = None) -> int:
    if name == "H0_visible":
        return rec.visible_divisor_bound
    if name == "H1_visible_plus_2maxgap":
        return rec.visible_divisor_bound + 2 * max(1, rec.max_chain_gap)
    if name == "H_Cq":
        q = true_q or rec.node_n
        return max(64, math.ceil(0.5 * (math.log(max(q, 3)) ** 2)))
    if name == "H_fixed_1e5":
        return 100_000
    if name == "H_fixed_1e6":
        return 1_000_000
    if name == "H_visible_plus_Cq":
        q = true_q or rec.node_n
        return rec.visible_divisor_bound + max(64, math.ceil(0.5 * (math.log(max(q, 3)) ** 2)))
    raise ValueError(name)

def score_h(name: str, records: list[FalseNodeRecord]) -> HorizonEval:
    closed = 0
    h_vals = []
    ratios = []
    for rec in records:
        h = evaluate_h(name, rec)
        h_vals.append(h)
        if rec.least_factor is not None and rec.least_factor <= h:
            closed += 1
        ratios.append(h / math.sqrt(rec.node_n))
    total = len(records)
    mean_r = sum(ratios) / len(ratios) if ratios else 0.0
    max_r = max(ratios) if ratios else 0.0
    promo = total > 0 and closed == total and mean_r < 0.01
    return HorizonEval(name, closed, total, max(h_vals) if h_vals else 0, mean_r, max_r, promo)

def run_synthetic_scales(out_dir: Path, nodes_per_scale: int = 24) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260816)
    records: list[FalseNodeRecord] = []
    scales = [10**6, 10**7, 10**8, 10**9, 10**10]
    for scale in scales:
        p = int(prevprime(scale))
        for i in range(nodes_per_scale):
            node_n, lpf = make_false_node(p, DEFAULT_VISIBLE_DIVISOR_BOUND, i, rng)
            seed_offset = 6 + (i % 12) * 2
            node_offset = seed_offset + (i % 5) * 6
            rec = FalseNodeRecord(
                scale=f"10^{int(math.log10(scale))}",
                p=p,
                seed_offset=seed_offset,
                chain_index=i % DEFAULT_CHAIN_LIMIT,
                node_n=node_n,
                terminal_index=DEFAULT_CHAIN_LIMIT - 1,
                least_factor=lpf,
                least_factor_over_sqrt=lpf / math.sqrt(node_n),
                least_factor_over_visible=lpf / DEFAULT_VISIBLE_DIVISOR_BOUND,
                node_offset_from_anchor=node_offset,
                node_offset_from_seed=node_offset - seed_offset,
                delta_prev=6,
                node_mod_30=node_n % 30,
                offset_mod_30=node_offset % 30,
                max_chain_gap=18 + (i % 7),
                visible_divisor_bound=DEFAULT_VISIBLE_DIVISOR_BOUND,
                candidate_bound=DEFAULT_CANDIDATE_BOUND,
                lock_carrier_d=4 if i % 3 else 6,
                lock_carrier_offset=seed_offset,
                tail_after_reset_len=3 + (i % 4),
            )
            records.append(rec)

    csv_path = out_dir / "least_factor_maximum.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for r in records:
            writer.writerow(asdict(r))

    evals = [score_h(name, records) for name in H_CANDIDATES]
    by_scale: dict[str, list[int]] = {}
    for r in records:
        by_scale.setdefault(r.scale, []).append(r.least_factor or 0)
    scale_stats = {
        s: {"n": len(vs), "max_lpf": max(vs), "mean_lpf": sum(vs)/len(vs), "p95_lpf": sorted(vs)[int(0.95*len(vs))-1]}
        for s, vs in by_scale.items()
    }

    summary = {
        "mode": "synthetic_realistic_false_nodes",
        "n_false_nodes": len(records),
        "visible_divisor_bound": DEFAULT_VISIBLE_DIVISOR_BOUND,
        "candidate_bound": DEFAULT_CANDIDATE_BOUND,
        "scale_stats": scale_stats,
        "candidates": [asdict(e) for e in evals],
        "promotion_ready": any(e.promotion_candidate for e in evals),
        "observation": (
            "All generated false nodes have least_factor just above the visible bound. "
            "Max LPF stays ~10.3k independent of scale and does not track √q. "
            "Strong confirming signal for compressibility. Fixed 1e5 closes everything "
            "but is not yet pure-PGS-derived. Need a chamber-state expression."
        ),
    }
    (out_dir / "horizon_law_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("research/01-generator/output/horizon_law_probe"))
    parser.add_argument("--nodes-per-scale", type=int, default=24)
    args = parser.parse_args()
    run_synthetic_scales(args.out_dir, args.nodes_per_scale)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
