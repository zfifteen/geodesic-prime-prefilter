#!/usr/bin/env python3
"""Carrier-Lock Horizon Transfer (CLHT) coupling probe — candidate 2.

Tests whether chamber-reset tail geometry + carrier lock at anchor p
bounds the divisor horizon needed for shadow-chain / modulus-link closure.

Coupling fields:
  - tail_after_reset_offsets
  - lock_carrier_d / lock_carrier_offset
  - modulus-link locked_endpoint_count and chain_steps
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "python"))
sys.path.insert(0, str(ROOT / "research" / "06-cryptology-rsa" / "scripts"))

from scale_pgs_chain_modulus_link import (  # noqa: E402
    SCALE_CASES,
    recursive_chain_modulus_lock,
)
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)

VISIBLE_DIVISOR_BOUND = 10_000
DEFAULT_CANDIDATE_BOUND = 128


def chamber_row(p: int, candidate_bound: int = DEFAULT_CANDIDATE_BOUND) -> dict | None:
    """Return CLHT-relevant chamber-reset fields for one anchor."""
    cert = pgs_chamber_reset_state_certificate(int(p), int(candidate_bound))
    if cert is None:
        return None
    tail = list(cert.get("tail_after_reset_offsets", []))
    max_tail = max(tail) if tail else 0
    gap = int(cert["gap_offset"])
    lock_offset = cert.get("lock_carrier_offset")
    lock_d = cert.get("lock_carrier_d")
    return {
        "p": int(p),
        "q": int(cert["q"]),
        "gap_offset": gap,
        "carrier_d": cert.get("carrier_d"),
        "lock_carrier_offset": lock_offset,
        "lock_carrier_d": lock_d,
        "lower_d_threat_offset": cert.get("lower_d_threat_offset"),
        "tail_after_reset_offsets": tail,
        "tail_count": len(tail),
        "max_tail_offset": max_tail,
        "h_clht": VISIBLE_DIVISOR_BOUND + max_tail,
        "h_clht_over_sqrt_q": (VISIBLE_DIVISOR_BOUND + max_tail) / math.isqrt(int(cert["q"])),
        "h_clht_ratio_to_candidate_bound": (VISIBLE_DIVISOR_BOUND + max_tail) / candidate_bound,
        "tail_to_gap_ratio": max_tail / gap if gap else 0.0,
        "lock_to_gap_ratio": (lock_offset / gap) if (lock_offset and gap) else None,
    }


def modulus_row(label: str, n: int, seed: int) -> dict:
    """Return modulus-link walk summary for one semiprime case."""
    result = recursive_chain_modulus_lock(int(n), int(seed))
    chamber = chamber_row(seed)
    return {
        "label": label,
        "modulus_n": int(n),
        "seed": int(seed),
        "chain_steps": result.chain_steps,
        "locked_endpoint_count": result.locked_endpoint_count,
        "skipped_floor_closures": result.skipped_floor_closures,
        "stop_reason": result.stop_reason,
        "seed_max_tail_offset": chamber["max_tail_offset"] if chamber else None,
        "seed_tail_count": chamber["tail_count"] if chamber else None,
        "seed_h_clht": chamber["h_clht"] if chamber else None,
        "steps_per_locked_endpoint": result.chain_steps / result.locked_endpoint_count,
        "steps_minus_tail_count": (
            result.chain_steps - chamber["tail_count"] if chamber else None
        ),
    }


def prime_surface_sample(limit: int = 2000) -> list[int]:
    """Return primes below limit via simple sieve."""
    if limit < 2:
        return []
    sieve = [True] * limit
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]


def summarize_chamber_surface(primes: list[int]) -> dict:
    """Aggregate CLHT statistics over a prime chamber surface."""
    rows = [chamber_row(p) for p in primes]
    rows = [row for row in rows if row is not None]
    if not rows:
        return {"count": 0}
    h_values = [row["h_clht"] for row in rows]
    tail_counts = [row["tail_count"] for row in rows]
    max_tails = [row["max_tail_offset"] for row in rows]
    return {
        "count": len(rows),
        "h_clht_min": min(h_values),
        "h_clht_max": max(h_values),
        "h_clht_median": sorted(h_values)[len(h_values) // 2],
        "tail_count_median": sorted(tail_counts)[len(tail_counts) // 2],
        "max_tail_offset_max": max(max_tails),
        "zero_tail_fraction": sum(1 for c in tail_counts if c == 0) / len(rows),
        "h_clht_over_sqrt_q_max": max(row["h_clht_over_sqrt_q"] for row in rows),
        "visible_divisor_bound": VISIBLE_DIVISOR_BOUND,
        "candidate_bound": DEFAULT_CANDIDATE_BOUND,
    }


def main() -> int:
    out_dir = Path(__file__).resolve().parent
    primes = prime_surface_sample(2000)
    chamber_rows = [chamber_row(p) for p in primes]
    chamber_rows = [row for row in chamber_rows if row is not None]
    modulus_rows = [
        modulus_row(case.label, case.n, case.seed) for case in SCALE_CASES
    ]

    payload = {
        "rule_id": "carrier_lock_horizon_transfer_v1_candidate_2",
        "insight": (
            "Shadow-chain divisor horizon inherits chamber-reset tail envelope "
            "and carrier lock at anchor p; modulus-link chain depth couples "
            "to tail_count at seed."
        ),
        "h_clht_formula": "visible_divisor_bound + max(tail_after_reset_offsets(p))",
        "visible_divisor_bound": VISIBLE_DIVISOR_BOUND,
        "chamber_surface_summary": summarize_chamber_surface(primes),
        "modulus_link_coupling": modulus_rows,
        "sample_chamber_rows": chamber_rows[:20],
    }

    summary_path = out_dir / "clht_coupling_summary.json"
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["chamber_surface_summary"], indent=2))
    print()
    print("modulus_link_coupling:")
    for row in modulus_rows:
        print(
            f"  {row['label']}: steps={row['chain_steps']} "
            f"locked={row['locked_endpoint_count']} "
            f"tail_count={row['seed_tail_count']} "
            f"h_clht={row['seed_h_clht']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())