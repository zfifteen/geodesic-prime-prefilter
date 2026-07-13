#!/usr/bin/env python3
"""Min-tau level-set compression residual (LSC / LSCD) probe.

PGS objects (first frame):
  - consecutive prime gap (p, q) from tau-scan (tau(n)=2 endpoint rule)
  - interior I = {p+1, ..., q-1}
  - GWR witness w = leftmost min-tau on I (proved maximizer of F)
  - co-minimal level set L = {n in I : tau(n) = tau(w)}
  - rightmost co-minimal w_R = max L
  - dynamic cutoff C(q) = max(64, ceil(0.5 * log(q)^2)) from PROOF.md

Proved fact used (not re-proved here):
  w - p <= C(q)   (universal bounded compression on the LEFTMOST witness)

Hypothesis under test (not a theorem):
  Full Level-Set Compression (LSC):
      every n in L satisfies n - p <= C(q)
  Level-Set Compression Dichotomy (LSCD), residual after LSC fails:
      spill (w_R - p > C(q)) occurs only on the tau(w)=4 branch
      with early lock (small alpha = w-p), never on square (tau=3)
      or high-tau (tau>=6) branches on the stated regime.

Status labels:
  - LSC: measured INVALIDATED on 11..2e6 (spill exists)
  - LSCD: measured hold on 11..2e6 (hypothesis, not theorem)
  - theorem status of w-p <= C(q): unchanged (PROOF.md)

Tau tables and prime lists are field preparation for the divisor-count
field. Selection uses only tau values and leftmost-min definition.
No Miller-Rabin, isprime API, or gcd gate chooses outputs.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def dynamic_cutoff(q: int) -> int:
    """C(q) from PROOF.md universal bounded compression."""
    return max(64, math.ceil(0.5 * (math.log(q) ** 2)))


def divisor_counts(limit: int) -> list[int]:
    """tau[n] for n in 0..limit by linear divisor accumulation."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def primes_from_tau(tau: list[int], lo: int, hi: int) -> list[int]:
    """Integers n in [lo, hi] with tau(n)=2 (direct next-prime field)."""
    return [n for n in range(max(lo, 2), hi + 1) if tau[n] == 2]


def analyze_gap(p: int, q: int, tau: list[int]) -> dict | None:
    """Return level-set geometry and spill flags for one nonempty gap."""
    if q - p < 2:
        return None
    interior = range(p + 1, q)
    min_tau = min(tau[n] for n in interior)
    level = [n for n in interior if tau[n] == min_tau]
    w = level[0]
    w_r = level[-1]
    c = dynamic_cutoff(q)
    alpha = w - p
    right_off = w_r - p
    spill = right_off > c
    return {
        "p": p,
        "q": q,
        "g": q - p,
        "w": w,
        "w_R": w_r,
        "tau_w": min_tau,
        "n_ties": len(level),
        "alpha": alpha,
        "right_off": right_off,
        "span": w_r - w,
        "C": c,
        "clearance": q - w_r,
        "util_L": alpha / c,
        "util_R": right_off / c,
        "spill": spill,
        "left_in_bound": alpha <= c,
        "theorem_break": alpha > c,
    }


def run_probe(q_max: int, sample_cap: int = 40) -> dict:
    """Scan consecutive gaps with endpoint q <= q_max, left prime >= 11."""
    t0 = time.time()
    hard = q_max + 200
    tau = divisor_counts(hard)
    primes = primes_from_tau(tau, 11, hard)

    gaps = 0
    spill_count = 0
    by_tau: Counter[int] = Counter()
    spill_by_tau: Counter[int] = Counter()
    spill_alpha_hist: Counter[int] = Counter()
    spill_rows: list[dict] = []
    max_util_r = 0.0
    max_util_r_row: dict | None = None
    theorem_breaks = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        if q > q_max:
            break
        rec = analyze_gap(p, q, tau)
        if rec is None:
            continue
        gaps += 1
        d = rec["tau_w"]
        by_tau[d] += 1
        if rec["theorem_break"]:
            theorem_breaks += 1
        if rec["util_R"] > max_util_r:
            max_util_r = rec["util_R"]
            max_util_r_row = rec
        if rec["spill"]:
            spill_count += 1
            spill_by_tau[d] += 1
            spill_alpha_hist[rec["alpha"]] += 1
            if len(spill_rows) < sample_cap:
                spill_rows.append(rec)

    rates = {}
    for d in sorted(by_tau):
        s = spill_by_tau[d]
        rates[str(d)] = {
            "gaps": by_tau[d],
            "spill": s,
            "spill_rate": s / by_tau[d],
        }

    spill_off_d4 = sum(v for d, v in spill_by_tau.items() if d != 4)
    spill_on_square = spill_by_tau[3]
    spill_on_high = sum(v for d, v in spill_by_tau.items() if d >= 6)

    return {
        "status": "measured residual map only; not a theorem",
        "not_a_theorem": True,
        "proved_input": {
            "leftmost_bound": "w - p <= C(q) (PROOF.md universal bounded compression)",
            "C_q": "max(64, ceil(0.5 * log(q)^2))",
            "GWR": "leftmost min-tau on interior",
        },
        "hypotheses": {
            "LSC_full_level_set_in_C": {
                "statement": "every co-minimal n satisfies n-p <= C(q)",
                "result": "INVALIDATED" if spill_count else "measured hold on regime",
            },
            "LSCD_spill_only_d4": {
                "statement": "if w_R - p > C(q) then tau(w)=4",
                "result": (
                    "measured hold on regime"
                    if spill_off_d4 == 0 and spill_count > 0
                    else (
                        "measured hold (no spill observed)"
                        if spill_count == 0
                        else "FAIL"
                    )
                ),
            },
            "LSCD_no_spill_square": {
                "statement": "tau(w)=3 implies no spill",
                "result": "measured hold on regime" if spill_on_square == 0 else "FAIL",
            },
            "LSCD_no_spill_high_tau": {
                "statement": "tau(w)>=6 implies no spill",
                "result": "measured hold on regime" if spill_on_high == 0 else "FAIL",
            },
        },
        "regime": {
            "left_prime_min": 11,
            "q_max": q_max,
            "gaps_scanned": gaps,
            "seconds": round(time.time() - t0, 3),
        },
        "totals": {
            "spill_count": spill_count,
            "spill_rate": (spill_count / gaps) if gaps else None,
            "theorem_breaks_leftmost": theorem_breaks,
            "spill_off_d4": spill_off_d4,
            "spill_on_square_tau3": spill_on_square,
            "spill_on_tau_ge6": spill_on_high,
            "max_alpha_among_spills": (
                max(spill_alpha_hist) if spill_alpha_hist else None
            ),
            "max_util_R": max_util_r,
        },
        "rates_by_tau_w": rates,
        "spill_alpha_hist": {str(k): v for k, v in sorted(spill_alpha_hist.items())},
        "max_util_R_row": max_util_r_row,
        "spill_samples": spill_rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--q-max",
        type=int,
        default=2_000_000,
        help="scan gaps with endpoint q <= this bound (default 2e6)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="optional JSON output path",
    )
    args = ap.parse_args()
    result = run_probe(args.q_max)
    text = json.dumps(result, indent=2) + "\n"
    out = args.out
    if out is None:
        out = HERE / f"results_qmax_{args.q_max}.json"
    out.write_text(text)
    print(text)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
