#!/usr/bin/env python3
"""Stated-regime CE pressure for H-210 and H-tau16 (hypothesis / measured only).

Hypotheses under pressure (NOT theorems):

  H-210:   if GWR w satisfies 210 | w, then g = 2
  H-tau16: if z(w) >= 4 on M_v1 and tau(w) > 16, then g = 2

One counterexample in the regime falsifies that hypothesis for universality.
Zero counterexamples yields verdict not_falsified_in_tested_regime only.

Classical primality/tau locate GWR carriers (audit scan). This script does not
wire residual trial into generator inference and does not restore historical z≥4⇒g=2 claim.

Repro:
  python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py
  python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py \\
      --p-max 200000 --out research/21-modular-residual-salvage/output/h210_htau16_pressure.json
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

from residual_partition import zero_count  # noqa: E402


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


def is_h210_antecedent(w: int) -> bool:
    return w % 210 == 0


def is_htau16_antecedent(w: int, tau_w: int, z: int) -> bool:
    return z >= 4 and tau_w > 16


def is_hypothesis_ce(gap: int, antecedent: bool) -> bool:
    """Universal implication antecedent => g=2 is falsified when antecedent and g>2."""
    return antecedent and gap > 2


def run_pressure(p_min: int, p_max: int) -> dict:
    t0 = time.time()
    primes = sieve_primes(p_max + 200)

    gaps_scanned = 0
    h210_antecedents = 0
    h210_ce_count = 0
    h210_ces: list[dict] = []
    htau16_antecedents = 0
    htau16_ce_count = 0
    htau16_ces: list[dict] = []
    bare_ss_fps = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        if p < p_min or p >= p_max or q <= p + 1:
            continue
        gaps_scanned += 1
        w, tw = gwr_witness(p, q)
        gap = q - p
        z = zero_count(w)
        row = {"p": p, "q": q, "gap": gap, "w": w, "tau_w": tw, "z": z}

        if z >= 4 and gap > 2:
            bare_ss_fps += 1

        if is_h210_antecedent(w):
            h210_antecedents += 1
            if is_hypothesis_ce(gap, True):
                h210_ce_count += 1
                if len(h210_ces) < 5:
                    h210_ces.append(row)

        if is_htau16_antecedent(w, tw, z):
            htau16_antecedents += 1
            if is_hypothesis_ce(gap, True):
                htau16_ce_count += 1
                if len(htau16_ces) < 5:
                    htau16_ces.append(row)

    def verdict(ce_count: int) -> str:
        if ce_count >= 1:
            return "falsified"
        return "not_falsified_in_tested_regime"

    elapsed = time.time() - t0
    return {
        "status": "hypothesis_measured_pressure_only",
        "claim_language": (
            "Finite CE pressure on H-210 and H-tau16. Not theorems. "
            "Empty regime is not a proof. z4 twin lock remains invalidated."
        ),
        "z4_universal_status_lock": "invalidated",
        "regime": {
            "p_min": p_min,
            "p_max": p_max,
            "description": (
                f"consecutive prime gaps with left prime p in [{p_min}, {p_max})"
            ),
        },
        "hypotheses": {
            "H-210": {
                "statement": "GWR w with 210|w  =>  g = 2",
                "status_label": "hypothesis / measured",
                "antecedent_count": h210_antecedents,
                "counterexample_count": h210_ce_count,
                "verdict": verdict(h210_ce_count),
                "counterexample_examples": h210_ces,
            },
            "H-tau16": {
                "statement": "z(w)>=4 and tau(w)>16  =>  g = 2",
                "status_label": "hypothesis / measured",
                "antecedent_count": htau16_antecedents,
                "counterexample_count": htau16_ce_count,
                "verdict": verdict(htau16_ce_count),
                "counterexample_examples": htau16_ces,
            },
        },
        "control": {
            "gaps_scanned": gaps_scanned,
            "bare_z4_false_positives_z4_g_gt_2": bare_ss_fps,
        },
        "elapsed_seconds": round(elapsed, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="CE pressure for H-210 and H-tau16 (hypothesis only)."
    )
    parser.add_argument("--p-min", type=int, default=11)
    parser.add_argument(
        "--p-max",
        type=int,
        default=200_000,
        help="exclusive upper bound on left prime p (default 200000)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=CHAPTER_DIR / "output" / "h210_htau16_pressure.json",
    )
    args = parser.parse_args(argv)
    if args.p_max <= args.p_min:
        print("error: p-max must exceed p-min", file=sys.stderr)
        return 2

    result = run_pressure(args.p_min, args.p_max)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("STATUS: hypothesis_measured_pressure_only (not theorems)")
    print(f"regime: p in [{result['regime']['p_min']}, {result['regime']['p_max']})")
    print(f"gaps_scanned: {result['control']['gaps_scanned']}")
    print(
        "bare_z4_twin_lock_fps_z4_g_gt_2: "
        f"{result['control']['bare_z4_false_positives_z4_g_gt_2']}"
    )
    for key in ("H-210", "H-tau16"):
        h = result["hypotheses"][key]
        print(
            f"{key}: antecedents={h['antecedent_count']} "
            f"ces={h['counterexample_count']} verdict={h['verdict']}"
        )
    print(f"wrote: {args.out}")
    print(f"elapsed_seconds: {result['elapsed_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
