#!/usr/bin/env python3
"""Residual-class surface for GWR remainder zeros (post Super-Signal kill).

PGS objects first:
  - consecutive prime gap (p, q)
  - divisor-count field tau on the interior
  - GWR witness w = leftmost interior n with minimal tau
  - remainder-zero count z(w) on fixed moduli M_v1 = (2,3,5,7,30,210,2310)
  - gap size g = q - p
  - tie count = number of interior n with tau(n) = tau(w)

Purpose (measured residual map only; not a theorem):
  Partition every gap by residual class so the invalidated Super-Signal rule
  cannot re-enter as soft "often twin" language.

Classes (primary):
  A  z>=4 and g==2                              (true twin with z4 witness)
  B  z>=4 and g>2 and ties>1                    (non-twin, min-tau ties)
  C  z>=4 and g>2 and ties==1                   (non-twin, unique min-tau)
  D  z<4                                        (all other gaps)

Status labels:
  Super-Signal universal rule: invalidated (repo + public counterexample).
  This probe: measured residual counts only.

Classical sieve/tau construction is field computation for tau, not PGS
inference. No isprime / nextprime / Miller-Rabin gate chooses outputs.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

MODULI = (2, 3, 5, 7, 30, 210, 2310)
HERE = Path(__file__).resolve().parent


def zcount(n: int) -> int:
    """Count remainder zeros of n against M_v1."""
    return sum(1 for m in MODULI if n % m == 0)


def sieve_primes(limit: int) -> list[int]:
    """Primes in [2, limit] via Eratosthenes (field prep, not inference)."""
    if limit < 2:
        return []
    s = bytearray(b"\x01") * (limit + 1)
    s[0:2] = b"\x00\x00"
    r = int(limit**0.5)
    for i in range(2, r + 1):
        if s[i]:
            start = i * i
            s[start : limit + 1 : i] = b"\x00" * (((limit - start) // i) + 1)
    return [i for i in range(2, limit + 1) if s[i]]


def divisor_counts(limit: int) -> list[int]:
    """tau[n] for all n in 0..limit by linear sieve accumulation."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def residual_class(z: int, g: int, ties: int) -> str:
    """Map (z, g, ties) to primary residual class label."""
    if z < 4:
        return "D_z_lt_4"
    if g == 2:
        return "A_z4_twin"
    if ties > 1:
        return "B_z4_nontwin_ties"
    return "C_z4_nontwin_unique"


def analyze_gap(p: int, q: int, tau: list[int]) -> dict | None:
    """Compute GWR fields and residual class for one gap."""
    if q - p < 2:
        return None
    interior = range(p + 1, q)
    min_tau = min(tau[n] for n in interior)
    w = next(n for n in interior if tau[n] == min_tau)
    ties = sum(1 for n in interior if tau[n] == min_tau)
    first_min_index = w - p  # 1 = immediately after p
    g = q - p
    z = zcount(w)
    cls = residual_class(z, g, ties)
    return {
        "p": p,
        "q": q,
        "g": g,
        "w": w,
        "tau_w": tau[w],
        "ties": ties,
        "z": z,
        "first_min_index": first_min_index,
        "div30": w % 30 == 0,
        "div210": w % 210 == 0,
        "class": cls,
    }


def run_probe(p_max: int, sample_cap: int = 25) -> dict:
    """Scan all consecutive gaps with left prime p in [11, p_max]."""
    t0 = time.time()
    # Need tau and primes up through the next prime after p_max.
    hard_limit = p_max + 400
    primes = sieve_primes(hard_limit)
    tau = divisor_counts(hard_limit)

    class_counts: Counter[str] = Counter()
    z_hist: Counter[int] = Counter()
    g_hist_z4: Counter[int] = Counter()
    samples: dict[str, list[dict]] = defaultdict(list)
    gaps = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        if p < 11:
            continue
        if p > p_max:
            break
        q = primes[i + 1]
        if q > hard_limit:
            break
        rec = analyze_gap(p, q, tau)
        if rec is None:
            continue
        gaps += 1
        cls = rec["class"]
        class_counts[cls] += 1
        z_hist[rec["z"]] += 1
        if rec["z"] >= 4:
            g_hist_z4[rec["g"]] += 1
        if len(samples[cls]) < sample_cap:
            samples[cls].append(rec)

    # Secondary measured cross-tabs (not theorems)
    z4_total = sum(c for k, c in class_counts.items() if k.startswith(("A_", "B_", "C_")))
    bare_ss_false = class_counts["B_z4_nontwin_ties"] + class_counts["C_z4_nontwin_unique"]

    return {
        "status": "measured",
        "not_a_theorem": True,
        "super_signal_universal": "invalidated",
        "moduli_M_v1": list(MODULI),
        "regime": {
            "left_prime_min": 11,
            "left_prime_max_inclusive": p_max,
            "gaps_scanned": gaps,
            "seconds": round(time.time() - t0, 3),
        },
        "residual_class_counts": dict(class_counts),
        "residual_class_definitions": {
            "A_z4_twin": "z(w)>=4 and gap==2",
            "B_z4_nontwin_ties": "z(w)>=4 and gap>2 and min-tau ties>1",
            "C_z4_nontwin_unique": "z(w)>=4 and gap>2 and unique min-tau",
            "D_z_lt_4": "z(w)<4",
        },
        "derived": {
            "z4_total": z4_total,
            "bare_super_signal_false_positives": bare_ss_false,
            "z4_twin_rate_among_z4": (
                round(class_counts["A_z4_twin"] / z4_total, 6) if z4_total else None
            ),
        },
        "z_histogram": {str(k): v for k, v in sorted(z_hist.items())},
        "gap_histogram_among_z4": {str(k): v for k, v in sorted(g_hist_z4.items())},
        "samples": {k: samples[k] for k in sorted(samples)},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--p-max",
        type=int,
        default=2_000_000,
        help="Inclusive max left prime (default 2e6 = original Super-Signal claim surface)",
    )
    ap.add_argument("--sample-cap", type=int, default=25)
    ap.add_argument(
        "--out",
        type=Path,
        default=HERE / "results.json",
        help="Output JSON path",
    )
    args = ap.parse_args()

    print(
        f"Residual-class probe: left primes p in [11, {args.p_max}], M_v1={MODULI}",
        flush=True,
    )
    out = run_probe(args.p_max, sample_cap=args.sample_cap)
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    counts = out["residual_class_counts"]
    print("\n=== residual class counts ===", flush=True)
    for k in (
        "A_z4_twin",
        "B_z4_nontwin_ties",
        "C_z4_nontwin_unique",
        "D_z_lt_4",
    ):
        print(f"  {k}: {counts.get(k, 0)}", flush=True)
    print(f"gaps: {out['regime']['gaps_scanned']}", flush=True)
    print(f"bare Super-Signal FPs (B+C): {out['derived']['bare_super_signal_false_positives']}", flush=True)
    print(f"seconds: {out['regime']['seconds']}", flush=True)
    print(f"wrote {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
