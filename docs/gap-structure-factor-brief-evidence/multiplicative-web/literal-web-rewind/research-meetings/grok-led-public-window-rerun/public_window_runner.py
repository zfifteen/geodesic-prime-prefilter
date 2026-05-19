#!/usr/bin/env python3
"""Public-only window nomination runner for the Grok-led sparse-window rerun.

Strict contract:
- Receives ONLY N and public policy parameters (R, threads, top_k).
- Never receives, imports, or uses p, q, min(p,q), factorint, gcd, or any secret.
- Uses the sparse thread pattern (arithmetic progressions of public small primes)
  to nominate offsets.
- "First thread" rule: each offset is assigned only the smallest r that hits it
  (in the ordered threads list); later threads "stop" for that offset.
- Ranking for top holes: purely by ascending |offset| (proximity), since every
  nominated offset carries exactly one first_thread label (support proxy = 1).
- All outputs contain only N, public R, policy name, nominated data, and cost.
  No p, q, recovered_factor, audit_kind, or any secret-derived field.

This runner can be executed on any N with no knowledge of its factors.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PUBLIC_OUT_ROOT = HERE / "output" / "public_first_thread_proximity_v1"

# Public policy constants (frozen for this rerun)
PUBLIC_THREADS: tuple[int, ...] = (2, 3, 5)
PUBLIC_R: int = 1 << 18          # 262144 -- chosen public compute budget for this experiment
PUBLIC_TOP_K: int = 20


def generate_congruence_offsets(res: int, r: int, radius: int) -> list[int]:
    """Generate all t in [-radius, radius] with t != 0, t ≡ res (mod r), value = N+t >=4 is caller responsibility."""
    if r <= 0 or radius < 0:
        return []
    ts: list[int] = []
    # Positive direction starting from smallest positive congruent
    t0 = res
    if t0 == 0:
        t0 = r
    t = t0
    while t <= radius:
        ts.append(t)
        t += r
    # Negative direction
    t = t0 - r
    while t >= -radius:
        if t != 0:
            ts.append(t)
        t -= r
    return ts


def public_nominate(n: int, radius: int | None = None, threads: tuple[int, ...] | None = None, top_k: int | None = None) -> dict[str, Any]:
    """Pure public nomination.

    Returns a dict containing only public information derived from N and the policy.
    The caller (or audit) may re-run this exact function on the same N to obtain
    reproducible full ordered lists for rank computation.
    """
    if radius is None:
        radius = PUBLIC_R
    if threads is None:
        threads = PUBLIC_THREADS
    if top_k is None:
        top_k = PUBLIC_TOP_K

    if n < 4:
        raise ValueError("N must be >= 4")

    started = time.perf_counter()

    seen: set[int] = set()
    nominated: list[dict[str, Any]] = []
    generator_steps = 0

    for r in threads:
        res = (-n) % r
        cands = generate_congruence_offsets(res, r, radius)
        for t in cands:
            generator_steps += 1
            if t in seen:
                continue
            value = n + t
            if value < 4:
                continue
            seen.add(t)
            nominated.append({
                "offset": t,
                "first_thread": r,
                "value": value,
            })

    # Public ranking: proximity (ascending |offset|), then offset for determinism
    nominated.sort(key=lambda item: (abs(item["offset"]), item["offset"]))

    top_nominated = nominated[:top_k]

    elapsed = time.perf_counter() - started

    cost = {
        "generator_steps": generator_steps,
        "unique_nominated_within_R": len(nominated),
        "top_k_emitted": len(top_nominated),
        "elapsed_seconds": round(elapsed, 6),
    }

    return {
        "policy": "first_thread_proximity_v1",
        "R": radius,
        "threads": list(threads),
        "top_k": top_k,
        "N": n,
        "N_bits": n.bit_length(),
        "nominated_count": len(nominated),
        "top_nominated": top_nominated,
        "cost": cost,
        "public_only": True,   # marker that this record was produced without secrets
    }


def write_public_result(n: int, case_name: str, result: dict[str, Any]) -> Path:
    """Write the frozen public result for a single N. Never includes secrets."""
    case_dir = PUBLIC_OUT_ROOT / case_name
    case_dir.mkdir(parents=True, exist_ok=True)
    out_path = case_dir / "public_result.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    """Example direct invocation: runs on a few hardcoded public N values (toy scale only)."""
    # These N values are public; the runner does not need to know they are semiprimes.
    test_ns = [
        (713, "toy_23x31"),
        (2537, "toy_43x59"),
        (5063, "toy_61x83"),
        (10057, "toy_89x113"),
        (18905157503, "continuation_00_public_N"),
    ]
    PUBLIC_OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for n, name in test_ns:
        res = public_nominate(n)
        path = write_public_result(n, name, res)
        print(f"Public result for {name} (N={n}, {n.bit_length()} bits) written to {path}")
        print(f"  nominated_within_R={res['nominated_count']}, top{res['top_k']} smallest-abs offsets emitted")
        if res["top_nominated"]:
            first = res["top_nominated"][0]
            print(f"  closest: offset={first['offset']} by r={first['first_thread']}")


if __name__ == "__main__":
    main()
