#!/usr/bin/env python3
"""Super-Signal FP residual catalog probe (hypothesis / measured only).

Does not restore Super-Signal. Does not claim theorem status.
Writes measure.json with a single regenerable schema.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def sieve_primes_and_tau(n: int):
    primes = []
    spf = [0] * (n + 1)
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
    tau = [0] * (n + 1)
    tau[1] = 1
    for i in range(2, n + 1):
        x = i
        t = 1
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            t *= (e + 1)
        tau[i] = t
    return primes, tau


def enrich(fp: dict) -> dict:
    w = fp["w"]
    r = w // 30 if w % 30 == 0 else None
    form_30r = (
        r is not None
        and fp["class_A"]
        and fp["g"] == 8
        and fp["p"] == 30 * r - 1
        and fp["q"] == 30 * r + 7
    )
    # tau=16 is forced when w=2*3*5*r with r prime; record cofactor only
    out = dict(fp)
    out["r"] = r
    out["form_p_30r_minus_1_q_30r_plus_7"] = form_30r
    return out


def scan_fps_to(p_max: int, primes, tau):
    fps = []
    n_nontwin = 0
    ps = [p for p in primes if p >= 11]
    for i in range(len(ps) - 1):
        p = ps[i]
        if p >= p_max:
            break
        q = ps[i + 1]
        g = q - p
        if g <= 2:
            continue
        n_nontwin += 1
        min_tau = 10**9
        w = None
        for n in range(p + 1, q):
            t = tau[n]
            if t < min_tau:
                min_tau = t
                w = n
        if w % 30 != 0:
            continue
        row = {
            "p": p,
            "q": q,
            "g": g,
            "w": w,
            "tau_w": min_tau,
            "off": w - p,
            "w_mod_7": w % 7,
            "w_mod_210": w % 210,
            "class_A": w == p + 1,
            "tau_eq_16": min_tau == 16,
            "g_eq_8": g == 8,
            "seven_open": (w % 7) != 0,
            "h210_antecedent": (w % 210) == 0,
        }
        row["in_R0"] = (
            row["class_A"]
            and row["tau_eq_16"]
            and row["g_eq_8"]
            and row["seven_open"]
        )
        fps.append(enrich(row))
    return n_nontwin, fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p-max", type=int, default=50_000_000)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "measure.json",
    )
    args = ap.parse_args()
    n = args.p_max + 200
    t0 = time.time()
    primes, tau = sieve_primes_and_tau(n)
    n_nontwin, fps = scan_fps_to(args.p_max, primes, tau)
    outside = [fp for fp in fps if not fp["in_R0"]]
    payload = {
        "probe": "super_signal_fp_signature",
        "hypothesis_status": "hypothesis",
        "claim_language": (
            "measured catalog on named regimes only; not verified/validated; "
            "not theorem; Super-Signal remains invalidated"
        ),
        "anti_revival": (
            "This does not repair Super-Signal. z(w)>=4 => g=2 stays invalidated. "
            "Class R0 describes observed failures; it is not the theorem "
            "z>=4 => (g=2 or R0)."
        ),
        "R0_definition": {
            "clauses": [
                "class_A: w = p + 1",
                "tau(w) = 16",
                "g = 8",
                "seven_open: w % 7 != 0",
            ],
            "independence_note": (
                "On the measured algebraic form w=2*3*5*r with r prime, "
                "tau(w)=16 is forced. Non-redundant pressure is mainly "
                "class-A, g=8, and seven-open (plus absence of other forms)."
            ),
        },
        "algebraic_form_measured": {
            "status": "measured_on_fps_in_this_package",
            "form": "w = 2*3*5*r (r prime), p = 30*r - 1, q = 30*r + 7",
            "all_fps_match_form": all(
                fp.get("form_p_30r_minus_1_q_30r_plus_7") for fp in fps
            )
            if fps
            else None,
        },
        "measured_fact": {
            "p_min": 11,
            "p_max": args.p_max,
            "nontwin_gaps": n_nontwin,
            "fp_count": len(fps),
            "fp_outside_R0": len(outside),
            "fps": fps,
            "evaluation": (
                "vacuous_no_fp"
                if len(fps) == 0
                else (
                    "all_fps_in_R0"
                    if len(outside) == 0
                    else "fp_outside_R0_found"
                )
            ),
        },
        "hypothesis_universal_R0": {
            "statement": "every Super-Signal FP at any scale lies in R0",
            "status": "hypothesis",
            "support_on_this_regime": (
                None if len(fps) == 0 else len(outside) == 0
            ),
            "disconfirmation": (
                "any FP with off!=1 or tau(w)!=16 or g!=8 or 7|w"
            ),
        },
        "h210_ce_among_fps": sum(1 for f in fps if f["h210_antecedent"]),
        "h210_note": (
            "Zero H-210 CEs among bare Super-Signal FPs does not prove H-210; "
            "R0 FPs are seven-open so they are outside the H-210 antecedent."
        ),
        "sieve_N": n,
        "elapsed_sec": time.time() - t0,
        "reproduce_command": (
            f"python3 research/16-predictions/probes/"
            f"super-signal-fp-signature-2026-07/probe_fp_signature.py "
            f"--p-max {args.p_max}"
        ),
    }
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "p_max": args.p_max,
                "fp_count": len(fps),
                "fp_outside_R0": len(outside),
                "evaluation": payload["measured_fact"]["evaluation"],
                "all_form": payload["algebraic_form_measured"]["all_fps_match_form"],
                "h210_ce_among_fps": payload["h210_ce_among_fps"],
                "out": str(args.out),
                "elapsed_sec": payload["elapsed_sec"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
