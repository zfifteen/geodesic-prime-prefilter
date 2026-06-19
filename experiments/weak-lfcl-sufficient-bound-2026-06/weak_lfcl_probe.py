#!/usr/bin/env python3
"""Weak L_FCL sufficient-bound probe + audit-demoted τ=2 lemma."""

from __future__ import annotations

import argparse
import csv
import json
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

from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)

from certificate_replay import replay_selection_at_bound  # noqa: E402
from demoted_audit import demoted_zero_excess_signature, structural_unique_resolved  # noqa: E402

MIN_PRIME = 11
PRIME_LIMIT = 1_000_000


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


def run_probe(output_dir: Path) -> dict[str, object]:
    tau = build_tau_table(PRIME_LIMIT + 1)
    primes = sieve_primes(PRIME_LIMIT)

    counters = {
        "gaps_total": 0,
        "cert_match_count": 0,
        "replay_match_count": 0,
        "unique_resolved_count": 0,
        "demoted_audit_pass_count": 0,
        "lane_v_tau2_pass_count": 0,
        "semantic_composite_only_count": 0,
        "cert_unresolved_count": 0,
        "replay_unresolved_count": 0,
    }
    failures: list[dict[str, object]] = []

    started = time.time()
    for index in range(len(primes) - 1):
        p = primes[index]
        q_true = primes[index + 1]
        if p < MIN_PRIME:
            continue

        gap = q_true - p
        counters["gaps_total"] += 1
        q_reference = q_ref_from_tau(p, q_true, tau)

        cert = pgs_chamber_reset_state_certificate(p, gap)
        replay = replay_selection_at_bound(p, gap)

        if cert is None:
            counters["cert_unresolved_count"] += 1
        else:
            q_cert = int(cert["q"])
            if q_cert == q_reference:
                counters["cert_match_count"] += 1
            else:
                failures.append({"p": p, "reason": "cert_mismatch", "q_cert": q_cert})

        if replay is None:
            counters["replay_unresolved_count"] += 1
        else:
            q_replay = int(replay["q"])
            if q_replay == q_reference:
                counters["replay_match_count"] += 1
            else:
                failures.append({"p": p, "reason": "replay_mismatch", "q_replay": q_replay})

            if structural_unique_resolved(replay):
                counters["unique_resolved_count"] += 1

            if bool(replay["used_composite_witness_only"]):
                counters["semantic_composite_only_count"] += 1

            demoted_pass = demoted_zero_excess_signature(replay)
            lane_v_pass = tau[q_reference] == 2

            if demoted_pass:
                counters["demoted_audit_pass_count"] += 1
            if lane_v_pass:
                counters["lane_v_tau2_pass_count"] += 1

            if demoted_pass != lane_v_pass:
                failures.append(
                    {
                        "p": p,
                        "reason": "demoted_vs_lane_v",
                        "demoted_pass": demoted_pass,
                        "lane_v_pass": lane_v_pass,
                    }
                )

    elapsed = time.time() - started
    total = counters["gaps_total"] or 1
    summary = {
        "regime": "R2-sufficient-bound",
        "prime_limit": PRIME_LIMIT,
        "min_prime": MIN_PRIME,
        "bound_policy": "B = gap",
        "elapsed_seconds": round(elapsed, 3),
        **counters,
        "cert_match_rate": counters["cert_match_count"] / total,
        "replay_match_rate": counters["replay_match_count"] / total,
        "unique_resolved_rate": counters["unique_resolved_count"] / total,
        "demoted_audit_pass_rate": counters["demoted_audit_pass_count"] / total,
        "lane_v_tau2_pass_rate": counters["lane_v_tau2_pass_count"] / total,
        "semantic_composite_only_rate": counters["semantic_composite_only_count"] / total,
        "weak_lfcl_supported_on_surface": (
            counters["cert_match_count"] == total
            and counters["demoted_audit_pass_count"] == total
            and counters["unique_resolved_count"] == total
            and not failures
        ),
        "first_failure": failures[0] if failures else None,
        "failure_count": len(failures),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failures:
        with (output_dir / "failures.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(failures[0].keys()))
            writer.writeheader()
            writer.writerows(failures)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = run_probe(args.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if summary["failure_count"]:
        print("HALT: weak L_FCL probe failures", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())