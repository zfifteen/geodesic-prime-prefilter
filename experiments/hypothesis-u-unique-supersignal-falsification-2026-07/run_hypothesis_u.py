#!/usr/bin/env python3
"""Falsification hunt for Hypothesis U (Unique Super-Signal).

Hypothesis U (status: hypothesis):
  If GWR witness w has z(w) >= 4 on M_v1 AND the interior tau-minimum is
  unique (ties == 1), then gap size g = 2.

One counterexample (g > 2, z >= 4, ties == 1) falsifies U.
Zero CEs in a stated regime is measured support only — not a proof.

Classical tools used as audit only.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from array import array
from collections import defaultdict
from pathlib import Path

MODULI = (2, 3, 5, 7, 30, 210, 2310)
HERE = Path(__file__).resolve().parent


def zcount(n: int) -> int:
    return sum(1 for m in MODULI if n % m == 0)


def sieve_primes(n: int) -> list[int]:
    s = bytearray(b"\x01") * (n + 1)
    s[0:2] = b"\x00\x00"
    r = int(n**0.5)
    for i in range(2, r + 1):
        if s[i]:
            start = i * i
            s[start : n + 1 : i] = b"\x00" * (((n - start) // i) + 1)
    return [i for i in range(2, n + 1) if s[i]]


def sieve_tau(n: int) -> array:
    """Compact tau table: unsigned short is enough (tau(n) << 65535 for n<=1e8+)."""
    t = array("H", [0]) * (n + 1)
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            t[j] += 1
    return t


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


def phase_a(p_max: int, max_ce: int = 50) -> dict:
    print(f"PHASE A: sieve + full gaps, left prime p in [11, {p_max})", flush=True)
    t0 = time.time()
    primes = sieve_primes(p_max + 400)
    tau = sieve_tau(p_max + 400)
    print(f"  sieve done in {time.time() - t0:.1f}s  primes={len(primes)}", flush=True)

    out = {
        "gaps": 0,
        "hypothesis_u_ce": [],
        "bare_z4_fp": [],
        "h210_fp": [],
        "htau16_fp": [],
        "counts": defaultdict(int),
    }

    t1 = time.time()
    for i in range(len(primes) - 1):
        p, q = primes[i], primes[i + 1]
        if p < 11:
            continue
        if p >= p_max:
            break
        if q - p < 2:
            continue
        out["gaps"] += 1
        best_t = 10**9
        best_w = 0
        for n in range(p + 1, q):
            tn = tau[n]
            if tn < best_t:
                best_t = tn
                best_w = n
        ties = 0
        for n in range(p + 1, q):
            if tau[n] == best_t:
                ties += 1
        z = zcount(best_w)
        g = q - p
        rec = record(p, q, best_w, best_t, ties, z)

        if z >= 4:
            out["counts"]["z4_hits"] += 1
            if g == 2:
                out["counts"]["z4_twins"] += 1
            else:
                out["counts"]["bare_z4_fp"] += 1
                if len(out["bare_z4_fp"]) < max_ce:
                    out["bare_z4_fp"].append(rec)
            if ties == 1:
                out["counts"]["u_hits"] += 1
                if g == 2:
                    out["counts"]["u_twins"] += 1
                else:
                    out["counts"]["hypothesis_u_ce"] += 1
                    if len(out["hypothesis_u_ce"]) < max_ce:
                        out["hypothesis_u_ce"].append(rec)
            if best_t > 16:
                out["counts"]["tau16_hits"] += 1
                if g != 2:
                    out["counts"]["htau16_fp"] += 1
                    if len(out["htau16_fp"]) < max_ce:
                        out["htau16_fp"].append(rec)
        if best_w % 210 == 0:
            out["counts"]["h210_hits"] += 1
            if g == 2:
                out["counts"]["h210_twins"] += 1
            else:
                out["counts"]["h210_fp"] += 1
                if len(out["h210_fp"]) < max_ce:
                    out["h210_fp"].append(rec)

    out["counts"] = dict(out["counts"])
    out["seconds"] = round(time.time() - t1, 2)
    print(
        f"  gaps={out['gaps']}  U_CE={len(out['hypothesis_u_ce'])}  "
        f"bare_z4_fp={out['counts'].get('bare_z4_fp', 0)}  "
        f"time={out['seconds']}s",
        flush=True,
    )
    return out


def phase_b(p_lo: int, p_hi: int, max_ce: int = 50) -> dict:
    """Extension: sympy primerange + divisor_count on interiors only."""
    import sympy as sp

    print(f"PHASE B: extension gaps, left prime p in [{p_lo}, {p_hi})", flush=True)
    t0 = time.time()
    out = {
        "gaps": 0,
        "hypothesis_u_ce": [],
        "bare_z4_fp": [],
        "h210_fp": [],
        "htau16_fp": [],
        "counts": defaultdict(int),
    }

    # process in chunks for progress
    chunk = 5_000_000
    lo = p_lo
    while lo < p_hi:
        hi = min(lo + chunk, p_hi)
        ps = list(sp.primerange(lo, hi + 400))
        for i in range(len(ps) - 1):
            p, q = int(ps[i]), int(ps[i + 1])
            if p < lo or p >= hi:
                continue
            if q - p < 2:
                continue
            out["gaps"] += 1
            best_t = 10**9
            best_w = 0
            rows = []
            for n in range(p + 1, q):
                tn = int(sp.divisor_count(n))
                rows.append(tn)
                if tn < best_t:
                    best_t = tn
                    best_w = n
            ties = sum(1 for tn in rows if tn == best_t)
            z = zcount(best_w)
            g = q - p
            rec = record(p, q, best_w, best_t, ties, z)

            if z >= 4:
                out["counts"]["z4_hits"] += 1
                if g == 2:
                    out["counts"]["z4_twins"] += 1
                else:
                    out["counts"]["bare_z4_fp"] += 1
                    if len(out["bare_z4_fp"]) < max_ce:
                        out["bare_z4_fp"].append(rec)
                if ties == 1:
                    out["counts"]["u_hits"] += 1
                    if g == 2:
                        out["counts"]["u_twins"] += 1
                    else:
                        out["counts"]["hypothesis_u_ce"] += 1
                        if len(out["hypothesis_u_ce"]) < max_ce:
                            out["hypothesis_u_ce"].append(rec)
                            print(f"  HYPOTHESIS U CE FOUND: {rec}", flush=True)
                if best_t > 16 and g != 2:
                    out["counts"]["htau16_fp"] += 1
                    if len(out["htau16_fp"]) < max_ce:
                        out["htau16_fp"].append(rec)
            if best_w % 210 == 0:
                out["counts"]["h210_hits"] += 1
                if g == 2:
                    out["counts"]["h210_twins"] += 1
                else:
                    out["counts"]["h210_fp"] += 1
                    if len(out["h210_fp"]) < max_ce:
                        out["h210_fp"].append(rec)
                        print(f"  H-210 CE FOUND: {rec}", flush=True)
        print(
            f"  chunk [{lo},{hi}) gaps_so_far={out['gaps']} "
            f"U_CE={len(out['hypothesis_u_ce'])} bare_fp={out['counts'].get('bare_z4_fp', 0)} "
            f"elapsed={time.time() - t0:.1f}s",
            flush=True,
        )
        lo = hi

    out["counts"] = dict(out["counts"])
    out["seconds"] = round(time.time() - t0, 2)
    return out


def merge_phase(a: dict, b: dict) -> dict:
    keys_list = ("hypothesis_u_ce", "bare_z4_fp", "h210_fp", "htau16_fp")
    merged = {
        "gaps": a["gaps"] + b["gaps"],
        "seconds": round(a.get("seconds", 0) + b.get("seconds", 0), 2),
        "counts": defaultdict(int),
    }
    for k, v in a.get("counts", {}).items():
        merged["counts"][k] += v
    for k, v in b.get("counts", {}).items():
        merged["counts"][k] += v
    merged["counts"] = dict(merged["counts"])
    for k in keys_list:
        merged[k] = list(a.get(k, [])) + list(b.get(k, []))
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p-max-a", type=int, default=50_000_000, help="Phase A exclusive left-prime max")
    ap.add_argument("--p-max-b", type=int, default=120_000_000, help="Phase B exclusive left-prime max")
    ap.add_argument("--skip-b", action="store_true", help="Run Phase A only")
    args = ap.parse_args()

    print("=== Hypothesis U falsification experiment ===", flush=True)
    print("Primary: z>=4 AND unique min (ties==1) => g==2", flush=True)
    print(f"Regime: Phase A p<[11,{args.p_max_a}); Phase B p in [{args.p_max_a},{args.p_max_b})", flush=True)

    a = phase_a(args.p_max_a)
    if args.skip_b or args.p_max_b <= args.p_max_a:
        b = {
            "gaps": 0,
            "hypothesis_u_ce": [],
            "bare_z4_fp": [],
            "h210_fp": [],
            "htau16_fp": [],
            "counts": {},
            "seconds": 0.0,
        }
    else:
        b = phase_b(args.p_max_a, args.p_max_b)

    m = merge_phase(a, b)
    u_ce = m["hypothesis_u_ce"]
    if u_ce:
        verdict = "falsified"
    else:
        verdict = "not_falsified_in_tested_regime"

    result = {
        "hypothesis_id": "hypothesis_u_unique_supersignal",
        "status": "hypothesis",
        "statement": "If GWR w has z(w)>=4 on M_v1 and unique tau-minimum (ties==1), then g=2",
        "verdict": verdict,
        "regime": {
            "phase_a_p_max_exclusive": args.p_max_a,
            "phase_b_p_max_exclusive": args.p_max_b if not args.skip_b else args.p_max_a,
            "left_prime_min": 11,
            "gaps_scanned": m["gaps"],
            "seconds": m["seconds"],
        },
        "counts": m["counts"],
        "hypothesis_u_counterexamples": u_ce,
        "control_bare_z4_false_positives_sample": m["bare_z4_fp"][:20],
        "secondary_h210_false_positives": m["h210_fp"][:20],
        "secondary_htau16_false_positives": m["htau16_fp"][:20],
        "interpretation": {
            "falsified": "Hypothesis U is false; unique min + z>=4 does not force twin gaps.",
            "not_falsified_in_tested_regime": (
                "No CE found in the stated regime. Measured support only. "
                "Not a proof. Hypothesis remains open."
            ),
        }[verdict],
        "not_a_theorem": True,
    }

    out_path = HERE / "results.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n=== RESULT ===", flush=True)
    print(f"verdict: {verdict}", flush=True)
    print(f"gaps_scanned: {m['gaps']}", flush=True)
    print(f"Hypothesis U counterexamples: {len(u_ce)}", flush=True)
    for ce in u_ce[:10]:
        print(f"  CE {ce}", flush=True)
    print(
        f"control bare z>=4 FPs (count): {m['counts'].get('bare_z4_fp', 0)}",
        flush=True,
    )
    print(f"H-210 FPs: {m['counts'].get('h210_fp', 0)}", flush=True)
    print(f"H-tau>16 FPs: {m['counts'].get('htau16_fp', 0)}", flush=True)
    print(f"wrote {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
