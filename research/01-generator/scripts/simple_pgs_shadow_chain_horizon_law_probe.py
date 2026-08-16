#!/usr/bin/env python3
"""Shadow-chain horizon law probe.

Goal
----
Mine the least-factor maximum of every false pre-terminal node that currently
forces chain_horizon_closure to fall back to divisor exhaustion.

This is the sharpest experiment required by
docs/unanswered-questions/chain-horizon-closure/00_question.md.

Promotion gate (must all pass before any H is promoted):
1. H closes 100 % of pre-terminal false nodes on the tested surface.
2. The first surviving terminal node is identical to the current
   chain_horizon_closure result.
3. H / sqrt(n) is observably decreasing with scale and stays << 1.
4. H is computed from PGS-visible state only (no factorization, no audit labels).

Usage (once high-scale ledgers are available or regenerable):

    PYTHONPATH=src/python python research/01-generator/scripts/simple_pgs_shadow_chain_horizon_law_probe.py \
        --ledger path/to/high_scale_rows.jsonl \
        --out-dir research/01-generator/output/horizon_law_probe/

Until full ledgers are restored, the script can still run in synthetic mode
to validate the logging schema and candidate H evaluators.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

# ---------------------------------------------------------------------------
# Constants that mirror the documented generator surface
# ---------------------------------------------------------------------------
DEFAULT_CANDIDATE_BOUND = 128
DEFAULT_VISIBLE_DIVISOR_BOUND = 10_000
DEFAULT_CHAIN_LIMIT = 8

# Candidate horizon families (to be expanded once real data is in)
H_CANDIDATES = [
    "H0_visible",
    "H1_visible_plus_2maxgap",
    "H_Cq",
    "H_fixed_1e5",
    "H_fixed_1e6",
]


@dataclass
class FalseNodeRecord:
    """One false pre-terminal shadow-chain node."""
    scale: str
    p: int
    seed_offset: int
    chain_index: int
    node_n: int
    terminal_index: int
    least_factor: Optional[int]  # None if > search limit (audit only)
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
    # PGS-visible state (extend as real certificates become available)
    lock_carrier_d: Optional[int] = None
    lock_carrier_offset: Optional[int] = None
    tail_after_reset_len: Optional[int] = None


@dataclass
class HorizonEval:
    """Result of testing one H candidate against a set of false nodes."""
    name: str
    closed: int
    total: int
    max_h: int
    mean_h_over_sqrt: float
    promotion_candidate: bool


def isqrt(n: int) -> int:
    return int(math.isqrt(n))


def trial_least_factor(n: int, limit: int) -> Optional[int]:
    """Return smallest prime factor of n if it is <= limit, else None.

    This function is audit-only. It must never appear in generator inference.
    """
    if n % 2 == 0:
        return 2
    f = 3
    while f * f <= n and f <= limit:
        if n % f == 0:
            return f
        f += 2
    if n <= limit:
        return n  # n itself is prime and small
    return None


def evaluate_h(
    name: str,
    node: FalseNodeRecord,
    true_q: Optional[int] = None,
) -> int:
    """Return the numeric horizon value for the named candidate."""
    if name == "H0_visible":
        return node.visible_divisor_bound
    if name == "H1_visible_plus_2maxgap":
        return node.visible_divisor_bound + 2 * max(1, node.max_chain_gap)
    if name == "H_Cq":
        q = true_q or node.node_n
        return max(64, math.ceil(0.5 * (math.log(q) ** 2)))
    if name == "H_fixed_1e5":
        return 100_000
    if name == "H_fixed_1e6":
        return 1_000_000
    raise ValueError(f"unknown H candidate: {name}")


def score_h_family(
    name: str,
    records: list[FalseNodeRecord],
) -> HorizonEval:
    closed = 0
    h_values: list[int] = []
    ratios: list[float] = []
    for rec in records:
        h = evaluate_h(name, rec)
        h_values.append(h)
        if rec.least_factor is not None and rec.least_factor <= h:
            closed += 1
        if rec.least_factor_over_sqrt is not None:
            ratios.append(h / math.sqrt(rec.node_n))
    total = len(records)
    mean_ratio = sum(ratios) / len(ratios) if ratios else 0.0
    # Harsh promotion gate (preliminary)
    promotion = (
        total > 0
        and closed == total
        and mean_ratio < 0.01
    )
    return HorizonEval(
        name=name,
        closed=closed,
        total=total,
        max_h=max(h_values) if h_values else 0,
        mean_h_over_sqrt=mean_ratio,
        promotion_candidate=promotion,
    )


def synthetic_demo(out_dir: Path) -> None:
    """Generate a small synthetic surface so the schema can be validated."""
    out_dir.mkdir(parents=True, exist_ok=True)
    records: list[FalseNodeRecord] = []
    # Synthetic false nodes that survive a visible bound of 10k
    for i, (p, seed, node, lpf) in enumerate(
        [
            (10**12 + 7, 6, 10**12 + 37, 10007),
            (10**12 + 13, 12, 10**12 + 61, 10037),
            (10**15 + 19, 18, 10**15 + 97, 10067),
            (10**18 + 31, 24, 10**18 + 127, 10091),
        ]
    ):
        rec = FalseNodeRecord(
            scale=f"10^{len(str(p))-1}",
            p=p,
            seed_offset=seed,
            chain_index=i % 4,
            node_n=node,
            terminal_index=4,
            least_factor=lpf,
            least_factor_over_sqrt=lpf / math.sqrt(node),
            least_factor_over_visible=lpf / DEFAULT_VISIBLE_DIVISOR_BOUND,
            node_offset_from_anchor=node - p,
            node_offset_from_seed=node - (p + seed),
            delta_prev=6,
            node_mod_30=node % 30,
            offset_mod_30=(node - p) % 30,
            max_chain_gap=18,
            visible_divisor_bound=DEFAULT_VISIBLE_DIVISOR_BOUND,
            candidate_bound=DEFAULT_CANDIDATE_BOUND,
            lock_carrier_d=4,
            lock_carrier_offset=6,
            tail_after_reset_len=3,
        )
        records.append(rec)

    # Write least-factor ledger
    csv_path = out_dir / "least_factor_maximum.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for r in records:
            writer.writerow(asdict(r))

    # Score every candidate H
    evals = [score_h_family(name, records) for name in H_CANDIDATES]
    summary = {
        "mode": "synthetic_demo",
        "n_false_nodes": len(records),
        "candidates": [asdict(e) for e in evals],
        "promotion_ready": any(e.promotion_candidate for e in evals),
        "note": (
            "Synthetic surface only. Real high-scale ledgers must be attached "
            "before any promotion decision. See STATUS.md."
        ),
    }
    (out_dir / "horizon_law_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(json.dumps(summary, indent=2))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        type=Path,
        default=None,
        help="Path to high-scale JSONL ledger (optional; falls back to synthetic)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("research/01-generator/output/horizon_law_probe"),
        help="Directory for least_factor_maximum.csv and summary",
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Force synthetic demo even if a ledger is supplied",
    )
    args = parser.parse_args(argv)

    if args.synthetic or args.ledger is None:
        print("Running synthetic schema validation…", file=sys.stderr)
        synthetic_demo(args.out_dir)
        return 0

    # Real-ledger path is intentionally a stub until the high-scale surfaces
    # are re-attached or regenerated. The schema and evaluation machinery are
    # already in place.
    print(
        "Real-ledger mode not yet wired. Supply --synthetic or restore the "
        "10^15 / 10^18 probe surfaces.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
