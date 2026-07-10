#!/usr/bin/env python3
"""Finite-regime modular-closed measurement among z>=4 GWR carriers.

MEASURED ONLY. This does not restore Super-Signal or prove a twin lock.

Scan consecutive prime gaps with left prime p in [p_min, p_max). For each gap,
compute the GWR witness w (leftmost interior min tau). If z(w) >= 4 on M_v1,
classify neighbor w+1 under residual_partition.wheel / residual_state.

Classical primality and tau are used only to locate GWR carriers (audit scan).
Residual closed/open is decided solely by residual_partition (set emptiness).

Repro:
  python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py
  python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py \\
      --p-max 50000 --out research/21-modular-residual-salvage/output/modular_closed_measure.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from math import isqrt
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from residual_partition import (  # noqa: E402
    STATE_MODULAR_CLOSED,
    classify_neighbor,
    zero_count,
)


def sieve_primes(limit: int) -> list[int]:
    if limit < 2:
        return []
    s = bytearray(b"\x01") * (limit + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if s[i]:
            start = i * i
            s[start : limit + 1 : i] = b"\x00" * (((limit - start) // i) + 1)
    return [i for i in range(2, limit + 1) if s[i]]


def tau(n: int) -> int:
    """Divisor count (audit scan only; not residual decision)."""
    t = 1
    x = n
    e = 0
    while x % 2 == 0:
        e += 1
        x //= 2
    if e:
        t *= e + 1
    d = 3
    while d * d <= x:
        e = 0
        while x % d == 0:
            e += 1
            x //= d
        if e:
            t *= e + 1
        d += 2
    if x > 1:
        t *= 2
    return t


def gwr_witness(p: int, q: int) -> tuple[int, int]:
    best_t = 10**18
    best_w = p + 1
    for n in range(p + 1, q):
        t = tau(n)
        if t < best_t:
            best_t = t
            best_w = n
    return best_w, best_t


def run_measure(p_min: int, p_max: int) -> dict:
    t0 = time.time()
    # Need primes up through the first prime >= p_max for consecutive pairs.
    primes = sieve_primes(p_max + 200)
    primes = [p for p in primes if p >= 2]

    gaps_scanned = 0
    z4_carriers = 0
    modular_closed = 0
    residual_open = 0
    modular_closed_and_twin = 0
    modular_closed_examples: list[dict] = []
    residual_open_examples: list[dict] = []

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        if p < p_min:
            continue
        if p >= p_max:
            break
        if q <= p + 1:
            continue
        gaps_scanned += 1
        w, tw = gwr_witness(p, q)
        z = zero_count(w)
        if z < 4:
            continue
        z4_carriers += 1
        rec = classify_neighbor(w, offset=1)
        gap = q - p
        row = {
            "p": p,
            "q": q,
            "gap": gap,
            "w": w,
            "tau_w": tw,
            "z": z,
            "residual_state": rec["residual_state"],
            "wheel": rec["wheel"],
            "residual_set_size": len(rec["residual_set"]),
        }
        if rec["residual_state"] == STATE_MODULAR_CLOSED:
            modular_closed += 1
            if gap == 2:
                modular_closed_and_twin += 1
            if len(modular_closed_examples) < 5:
                modular_closed_examples.append(row)
        else:
            residual_open += 1
            if len(residual_open_examples) < 5:
                residual_open_examples.append(row)

    elapsed = time.time() - t0
    rate = (modular_closed / z4_carriers) if z4_carriers else None
    return {
        "status": "measured_only",
        "claim_language": (
            "Finite regime measurement of modular-closed rate among GWR carriers "
            "with z(w) >= 4. Does not restore Super-Signal. Not a theorem."
        ),
        "super_signal_universal_lock": "invalidated",
        "regime": {
            "p_min": p_min,
            "p_max": p_max,
            "description": (
                f"consecutive prime gaps with left prime p in [{p_min}, {p_max})"
            ),
        },
        "counts": {
            "gaps_scanned": gaps_scanned,
            "z4_gwr_carriers": z4_carriers,
            "modular_closed_w_plus_1": modular_closed,
            "residual_open_w_plus_1": residual_open,
            "modular_closed_and_gap_2": modular_closed_and_twin,
        },
        "modular_closed_rate_among_z4": rate,
        "examples": {
            "modular_closed": modular_closed_examples,
            "residual_open": residual_open_examples,
        },
        "elapsed_seconds": round(elapsed, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Measure modular-closed rate for z>=4 GWR carriers (measured only)."
        )
    )
    parser.add_argument("--p-min", type=int, default=11)
    parser.add_argument(
        "--p-max",
        type=int,
        default=50_000,
        help="exclusive upper bound on left prime p (default 50000)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=CHAPTER_DIR / "output" / "modular_closed_measure.json",
    )
    args = parser.parse_args(argv)

    if args.p_max <= args.p_min:
        print("error: p-max must exceed p-min", file=sys.stderr)
        return 2

    result = run_measure(args.p_min, args.p_max)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("STATUS: measured_only (not a theorem; Super-Signal remains invalidated)")
    print(f"regime: p in [{result['regime']['p_min']}, {result['regime']['p_max']})")
    c = result["counts"]
    print(f"gaps_scanned: {c['gaps_scanned']}")
    print(f"z4_gwr_carriers: {c['z4_gwr_carriers']}")
    print(f"modular_closed_w_plus_1: {c['modular_closed_w_plus_1']}")
    print(f"residual_open_w_plus_1: {c['residual_open_w_plus_1']}")
    print(f"modular_closed_and_gap_2: {c['modular_closed_and_gap_2']}")
    print(f"modular_closed_rate_among_z4: {result['modular_closed_rate_among_z4']}")
    print(f"wrote: {args.out}")
    print(f"elapsed_seconds: {result['elapsed_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
