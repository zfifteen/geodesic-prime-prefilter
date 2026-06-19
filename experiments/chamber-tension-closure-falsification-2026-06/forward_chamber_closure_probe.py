#!/usr/bin/env python3
"""Forward chamber-closure falsification probe (H_CTC experiment, rev 4)."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_PYTHON = ROOT / "src" / "python"
EXPERIMENT_DIR = Path(__file__).resolve().parent
if str(SRC_PYTHON) not in sys.path:
    sys.path.insert(0, str(SRC_PYTHON))
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)

from f2rx_selector import f2rx_certificate  # noqa: E402

MIN_PRIME = 11
REGIME_LIMITS = {
    "R1": 1_000_000,
    "R2": 1_000_000,
}


def build_tau_table(limit: int) -> list[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for m in range(d, limit + 1, d):
            tau[m] += 1
    return tau


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
            is_prime[start : limit + 1 : step] = b"\x00" * (
                ((limit - start) // step) + 1
            )
    return [i for i in range(2, limit + 1) if is_prime[i]]


def q_ref_from_tau(p: int, q_true: int, tau: list[int]) -> int:
    for n in range(p + 1, q_true + 1):
        if tau[n] == 2:
            return n
    return q_true


def gwr_offset_from_counts(counts: list[int]) -> int | None:
    best: int | None = None
    best_off: int | None = None
    for off, value in enumerate(counts, start=1):
        if value <= 2:
            continue
        if best is None or value < best:
            best = value
            best_off = off
    return best_off


def zero_excess(n: int, tau: list[int]) -> float:
    return (tau[n] / 2.0 - 1.0) * math.log(n)


def chamber_geometry(p: int, q_ref: int, tau: list[int]) -> tuple[int | None, int | None, float]:
    if q_ref - p <= 1:
        return None, None, 0.0
    best_tau: int | None = None
    w_offset: int | None = None
    budget = 0.0
    for n in range(p + 1, q_ref):
        t = tau[n]
        budget += zero_excess(n, tau)
        if best_tau is None or t < best_tau:
            best_tau = t
            w_offset = n - p
    return w_offset, best_tau, budget


def bound_for_regime(regime: str, gap: int) -> int:
    if regime == "R1":
        return 128
    return gap


def should_sample_decision_offset(p: int, gap: int, regime: str) -> bool:
    if gap > 64:
        return True
    if regime == "R2":
        return p % 64 == 0
    return p % 512 == 0


def decision_offset_f1(p: int, q_ref: int, gap: int) -> int | None:
    for bound in range(1, gap + 1):
        cert = pgs_chamber_reset_state_certificate(p, bound)
        if cert is not None and int(cert["q"]) == q_ref:
            return bound
    return None


def decision_offset_f2rx(p: int, q_ref: int, gap: int) -> int | None:
    for bound in range(1, gap + 1):
        counts = [int(v) for v in divisor_counts_segment(p + 1, p + bound + 1)]
        cert = f2rx_certificate(p, counts, bound)
        if cert is not None and int(cert["q"]) == q_ref:
            return bound
    return None


def run_regime(regime: str, output_dir: Path) -> dict[str, object]:
    limit = REGIME_LIMITS[regime]
    tau = build_tau_table(limit + 1)
    primes = sieve_primes(limit)

    rows: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []

    counters = {
        "gaps_total": 0,
        "f0_match_count": 0,
        "f1_match_count": 0,
        "f2rx_match_count": 0,
        "f1_unresolved_count": 0,
        "f2rx_unresolved_count": 0,
        "bound_miss_count": 0,
        "prefix_none_at_gap_minus_1_count": 0,
        "prefix_gap_minus_1_total": 0,
        "decision_sample_total": 0,
        "decision_offset_eq_gap_count": 0,
        "audit_tau2_f1_fail": 0,
        "audit_tau2_f2rx_fail": 0,
    }

    started = time.time()
    for index in range(len(primes) - 1):
        p = primes[index]
        q_true = primes[index + 1]
        if p < MIN_PRIME:
            continue

        gap = q_true - p
        counters["gaps_total"] += 1
        q_reference = q_ref_from_tau(p, q_true, tau)
        bound = bound_for_regime(regime, gap)

        counts = [int(v) for v in divisor_counts_segment(p + 1, p + bound + 1)]
        gwr_off = gwr_offset_from_counts(counts[:gap])
        q_f0 = None if gwr_off is None else p + gwr_off

        cert_f1 = pgs_chamber_reset_state_certificate(p, bound)
        if cert_f1 is None:
            counters["f1_unresolved_count"] += 1
            q_f1 = None
        else:
            q_f1 = int(cert_f1["q"])

        cert_f2 = f2rx_certificate(p, counts[:bound], bound)
        if cert_f2 is None:
            counters["f2rx_unresolved_count"] += 1
            q_f2rx = None
        else:
            q_f2rx = int(cert_f2["q"])

        match_f0 = q_f0 == q_reference
        match_f1 = q_f1 == q_reference
        match_f2rx = q_f2rx == q_reference

        if match_f0:
            counters["f0_match_count"] += 1
        if match_f1:
            counters["f1_match_count"] += 1
        if match_f2rx:
            counters["f2rx_match_count"] += 1

        if regime == "R1" and gap > bound and (cert_f1 is None or q_f1 != q_reference):
            counters["bound_miss_count"] += 1

        audit_tau2_f1 = q_f1 is not None and tau[q_f1] == 2
        audit_tau2_f2rx = q_f2rx is not None and tau[q_f2rx] == 2
        if q_f1 is not None and not audit_tau2_f1:
            counters["audit_tau2_f1_fail"] += 1
        if q_f2rx is not None and not audit_tau2_f2rx:
            counters["audit_tau2_f2rx_fail"] += 1

        prefix_none = False
        if gap >= 2:
            counters["prefix_gap_minus_1_total"] += 1
            prefix_cert = pgs_chamber_reset_state_certificate(p, gap - 1)
            prefix_none = prefix_cert is None
            if prefix_none:
                counters["prefix_none_at_gap_minus_1_count"] += 1

        w_offset, w_tau, b_i = chamber_geometry(p, q_reference, tau)
        lock_offset = None if cert_f1 is None else cert_f1.get("lock_carrier_offset")
        threat_offset = None if cert_f1 is None else cert_f1.get("lower_d_threat_offset")

        decision_f1 = None
        decision_f2 = None
        if should_sample_decision_offset(p, gap, regime):
            counters["decision_sample_total"] += 1
            decision_f1 = decision_offset_f1(p, q_reference, gap)
            decision_f2 = decision_offset_f2rx(p, q_reference, gap)
            if decision_f1 == gap and decision_f2 == gap:
                counters["decision_offset_eq_gap_count"] += 1

        row = {
            "p": p,
            "q_ref": q_reference,
            "gap": gap,
            "bound": bound,
            "w_offset": w_offset,
            "w_tau": w_tau,
            "B_I": b_i,
            "gwr_offset": gwr_off,
            "q_f0": q_f0,
            "q_f1": q_f1,
            "q_f2rx": q_f2rx,
            "match_f0": match_f0,
            "match_f1": match_f1,
            "match_f2rx": match_f2rx,
            "audit_tau2_f1": audit_tau2_f1,
            "audit_tau2_f2rx": audit_tau2_f2rx,
            "prefix_cert_none_at_gap_minus_1": prefix_none,
            "lock_carrier_offset": lock_offset,
            "lower_d_threat_offset": threat_offset,
            "decision_offset_f1": decision_f1,
            "decision_offset_f2rx": decision_f2,
        }
        rows.append(row)

        if not match_f1 or not match_f2rx or match_f0:
            mismatches.append(row)

    elapsed = time.time() - started
    total = counters["gaps_total"] or 1
    sample_total = counters["decision_sample_total"] or 1
    prefix_total = counters["prefix_gap_minus_1_total"] or 1

    summary = {
        "regime": regime,
        "prime_limit": limit,
        "min_prime": MIN_PRIME,
        "elapsed_seconds": round(elapsed, 3),
        **counters,
        "f0_match_rate": counters["f0_match_count"] / total,
        "f1_match_rate": counters["f1_match_count"] / total,
        "f2rx_match_rate": counters["f2rx_match_count"] / total,
        "decision_offset_eq_gap_rate": (
            counters["decision_offset_eq_gap_count"] / sample_total
        ),
        "prefix_none_at_gap_minus_1_rate": (
            counters["prefix_none_at_gap_minus_1_count"] / prefix_total
        ),
        "first_mismatch_row": mismatches[0] if mismatches else None,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    gaps_path = output_dir / "gaps.csv"
    if rows:
        fieldnames = list(rows[0].keys())
        with gaps_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    if mismatches:
        mismatches_path = output_dir / "mismatches.csv"
        fieldnames = list(mismatches[0].keys())
        with mismatches_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mismatches)

    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regime",
        choices=sorted(REGIME_LIMITS),
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    summary = run_regime(args.regime, args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["f0_match_count"]:
        print("HALT: F0 negative control matched q_ref", file=sys.stderr)
        return 2
    if summary["regime"] == "R2" and summary["f1_match_rate"] < 1.0:
        print("HALT: F1 mismatch on R2", file=sys.stderr)
        return 3
    if summary["regime"] == "R2" and summary["f2rx_match_rate"] < 1.0:
        print("HALT: F2-RX mismatch on R2", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())