#!/usr/bin/env python3
"""Falsification hunt for Hypothesis U (Unique Super-Signal).

Hypothesis U (status: hypothesis):
  If GWR witness w has z(w) >= 4 on M_v1 AND the interior tau-minimum is
  unique (ties == 1), then gap size g = 2.

One counterexample (g > 2, z >= 4, ties == 1) falsifies U.
Zero CEs in a stated regime is measured support only — not a proof.

Classical tools used as audit only.

Default regime: full consecutive-prime gaps with left prime p in [11, 1.2e8).
"""

from __future__ import annotations

import argparse
import bisect
import json
import time
from collections import defaultdict
from pathlib import Path

MODULI = (2, 3, 5, 7, 30, 210, 2310)
HERE = Path(__file__).resolve().parent


def zcount(n: int) -> int:
    return sum(1 for m in MODULI if n % m == 0)


def gwr_from_tau_segment(p: int, q: int, tau_fn) -> tuple[int, int, int]:
    """Return (w, tau(w), tie_count) for gap (p,q) using callable tau_fn(n)."""
    best_t = 10**18
    best_w = 0
    for n in range(p + 1, q):
        tn = int(tau_fn(n))
        if tn < best_t:
            best_t = tn
            best_w = n
    ties = sum(1 for n in range(p + 1, q) if int(tau_fn(n)) == best_t)
    return best_w, best_t, ties


def classify_gap(p: int, q: int, w: int, tw: int, ties: int) -> dict:
    """Classify a gap against Hypothesis U and the bare Super-Signal control."""
    g = q - p
    z = zcount(w)
    unique = ties == 1
    z4 = z >= 4
    return {
        "g": g,
        "z": z,
        "ties": ties,
        "tau_w": tw,
        "hypothesis_u_hit": bool(z4 and unique),
        "hypothesis_u_ce": bool(z4 and unique and g > 2),
        "bare_z4_fp": bool(z4 and g > 2),
        "h210_fp": bool(w % 210 == 0 and g > 2),
        "htau16_fp": bool(z4 and tw > 16 and g > 2),
    }


def sieve_primes(n: int) -> list[int]:
    s = bytearray(b"\x01") * (n + 1)
    s[0:2] = b"\x00\x00"
    r = int(n**0.5)
    for i in range(2, r + 1):
        if s[i]:
            start = i * i
            s[start : n + 1 : i] = b"\x00" * (((n - start) // i) + 1)
    return [i for i in range(2, n + 1) if s[i]]


def tau_segment(left: int, right: int, small_primes: list[int]) -> list[int]:
    """tau values for absolute integers in [left, right)."""
    n = right - left
    vals = list(range(left, right))
    tau = [1] * n
    for p in small_primes:
        if p * p >= right:
            break
        start = ((left + p - 1) // p) * p
        for x in range(start, right, p):
            i = x - left
            exp = 0
            while vals[i] % p == 0:
                vals[i] //= p
                exp += 1
            if exp:
                tau[i] *= exp + 1
    for i in range(n):
        if vals[i] > 1:
            tau[i] *= 2
    return tau


def record(p: int, q: int, w: int, tw: int, ties: int, z: int) -> dict:
    return {
        "p": p,
        "q": q,
        "g": q - p,
        "w": w,
        "tau_w": tw,
        "ties": ties,
        "z": z,
        "div30": w % 30 == 0,
        "div210": w % 210 == 0,
    }


def run_scan(p_max: int, seg: int = 10_000_000, max_store: int = 40) -> dict:
    print(f"Sieving primes to {p_max}+pad ...", flush=True)
    t0 = time.time()
    primes = sieve_primes(p_max + 400)
    small = sieve_primes(int((p_max + 400) ** 0.5) + 2)
    print(f"  primes={len(primes)} in {time.time() - t0:.1f}s", flush=True)

    counts: dict[str, int] = defaultdict(int)
    u_ce: list[dict] = []
    bare: list[dict] = []
    h210: list[dict] = []
    htau: list[dict] = []
    gaps = 0
    t1 = time.time()

    for w0 in range(0, p_max, seg):
        w1 = min(w0 + seg, p_max)
        left = max(2, w0)
        right = min(p_max + 400, w1 + 400)
        if right <= left:
            continue
        tau = tau_segment(left, right, small)
        i0 = bisect.bisect_left(primes, max(11, w0))
        for i in range(i0, len(primes) - 1):
            p = primes[i]
            if p >= w1:
                break
            if p < 11:
                continue
            q = primes[i + 1]
            if q - p < 2 or q > right:
                continue
            gaps += 1
            best_t = 10**9
            best_w = 0
            for n in range(p + 1, q):
                tn = tau[n - left]
                if tn < best_t:
                    best_t = tn
                    best_w = n
            ties = sum(1 for n in range(p + 1, q) if tau[n - left] == best_t)
            z = zcount(best_w)
            g = q - p
            rec = record(p, q, best_w, best_t, ties, z)

            if z >= 4:
                counts["z4_hits"] += 1
                if g == 2:
                    counts["z4_twins"] += 1
                else:
                    counts["bare_z4_fp"] += 1
                    if len(bare) < max_store:
                        bare.append(rec)
                if ties == 1:
                    counts["u_hits"] += 1
                    if g == 2:
                        counts["u_twins"] += 1
                    else:
                        counts["u_ce"] += 1
                        u_ce.append(rec)
                        print(f"  HYPOTHESIS U CE: {rec}", flush=True)
                if best_t > 16:
                    counts["tau16_hits"] += 1
                    if g != 2:
                        counts["htau16_fp"] += 1
                        if len(htau) < max_store:
                            htau.append(rec)
            if best_w % 210 == 0:
                counts["h210_hits"] += 1
                if g == 2:
                    counts["h210_twins"] += 1
                else:
                    counts["h210_fp"] += 1
                    if len(h210) < max_store:
                        h210.append(rec)

        print(
            f"  window [{w0},{w1}) gaps={gaps} U_CE={counts['u_ce']} "
            f"bare_fp={counts['bare_z4_fp']} 210_fp={counts['h210_fp']} "
            f"t={time.time() - t1:.1f}s",
            flush=True,
        )

    return {
        "gaps": gaps,
        "counts": dict(counts),
        "u_ce": u_ce,
        "bare": bare,
        "h210": h210,
        "htau": htau,
        "seconds": round(time.time() - t0, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--p-max",
        type=int,
        default=120_000_000,
        help="Exclusive max left prime (default 1.2e8)",
    )
    args = ap.parse_args()

    print("=== Hypothesis U falsification experiment ===", flush=True)
    print("Primary: z>=4 AND unique min (ties==1) => g==2", flush=True)
    print(f"Regime: full gaps, left prime p in [11, {args.p_max})", flush=True)

    out = run_scan(args.p_max)
    u_ce = out["u_ce"]
    counts = out["counts"]
    verdict = "falsified" if u_ce else "not_falsified_in_tested_regime"

    result = {
        "hypothesis_id": "hypothesis_u_unique_supersignal",
        "status": "hypothesis",
        "statement": "If GWR w has z(w)>=4 on M_v1 and unique tau-minimum (ties==1), then g=2",
        "verdict": verdict,
        "regime": {
            "method": "full consecutive-prime gaps; primes sieve + segmented tau",
            "left_prime_min": 11,
            "left_prime_max_exclusive": args.p_max,
            "gaps_scanned": out["gaps"],
            "seconds": out["seconds"],
        },
        "counts": counts,
        "hypothesis_u_counterexamples": u_ce,
        "control_bare_z4_false_positives_sample": out["bare"],
        "control_bare_z4_false_positive_count": counts.get("bare_z4_fp", 0),
        "secondary_h210_false_positives": out["h210"],
        "secondary_htau16_false_positives": out["htau"],
        "interpretation": (
            "Hypothesis U FALSIFIED by listed CE(s)."
            if u_ce
            else (
                f"No counterexample to Hypothesis U among {out['gaps']} gaps "
                f"with left prime p in [11, {args.p_max}). "
                f"Bare z>=4 non-twin count = {counts.get('bare_z4_fp', 0)}. "
                f"H-210 non-twin = {counts.get('h210_fp', 0)}; "
                f"H-tau>16 non-twin = {counts.get('htau16_fp', 0)}. "
                "Measured support only. Not a proof. Hypothesis remains open."
            )
        ),
        "not_a_theorem": True,
    }

    path = HERE / "results.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n=== RESULT ===", flush=True)
    print(f"verdict: {verdict}", flush=True)
    print(f"gaps_scanned: {out['gaps']}", flush=True)
    print(f"Hypothesis U counterexamples: {len(u_ce)}", flush=True)
    print(f"U hits/twins: {counts.get('u_hits', 0)}/{counts.get('u_twins', 0)}", flush=True)
    print(f"bare z>=4 FPs: {counts.get('bare_z4_fp', 0)}", flush=True)
    print(f"H-210 FPs: {counts.get('h210_fp', 0)}", flush=True)
    print(f"H-tau>16 FPs: {counts.get('htau16_fp', 0)}", flush=True)
    print(f"wrote {path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
