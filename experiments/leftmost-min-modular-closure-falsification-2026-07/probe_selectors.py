#!/usr/bin/env python3
"""Comparative selector falsification for leftmost-min modular closure insight.

PGS objects first:
  - consecutive prime gap (p, q) with g = q - p
  - divisor-count field tau on the interior
  - remainder-zero count z(n) on fixed M_v1 = (2, 3, 5, 7, 30, 210, 2310)

Selectors (witness rules under test):
  GWR  = leftmost interior n with minimal tau
  A    = rightmost interior n with minimal tau  (global min, no leftmost bias)
  B    = first interior p + 1                   (position only)

Mismatch (decision failure of "z >= 4 forces g = 2"):
  z(w) >= 4 and g > 2

Status:
  H-absolute (GWR Super-Signal universal): already invalidated in PROOF.md;
    reconfirmed here if any GWR mismatch appears.
  H-comparative: hypothesis until this probe reports measured outcomes.

Classical sieves prepare primes and tau only. They do not choose the decision.
No Miller-Rabin / isprime / nextprime gate in the inference path.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

MODULI = (2, 3, 5, 7, 30, 210, 2310)
HERE = Path(__file__).resolve().parent
ZERO_THRESHOLD = 4

# Pinned Super-Signal counterexamples (PROOF.md certificates).
PINNED_GWR_CE = (
    {"p": 17_666_309, "q": 17_666_317, "g": 8, "w": 17_666_310, "z": 4},
    {"p": 22_284_029, "q": 22_284_037, "g": 8, "w": 22_284_030, "z": 4},
)


def zcount(n: int) -> int:
    """Count remainder zeros of n on M_v1."""
    return sum(1 for m in MODULI if n % m == 0)


def sieve_primes(limit: int) -> list[int]:
    """Primes in [2, limit] (field prep, not inference)."""
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
    """tau[n] for n in 0..limit by linear accumulation (field prep)."""
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def select_witnesses(p: int, q: int, tau: list[int]) -> dict[str, int | None]:
    """Return witness integers for GWR and alternatives.

    alt_a_rightmost_min: global min-tau with leftmost bias removed (rightmost).
    alt_a_unique_only: the single global min-tau n when ties==1; else None
      (literal reading of "the single interior number of globally minimal
      divisor count (position ignored)").
    alt_b_first: first interior p+1.
    """
    if q - p < 2:
        return {
            "gwr": None,
            "alt_a_rightmost_min": None,
            "alt_a_unique_only": None,
            "alt_b_first": None,
        }

    first = p + 1
    last = q - 1
    min_tau = min(tau[n] for n in range(first, q))
    mins = [n for n in range(first, q) if tau[n] == min_tau]
    w_left = mins[0]
    w_right = mins[-1]
    w_unique = mins[0] if len(mins) == 1 else None
    return {
        "gwr": w_left,
        "alt_a_rightmost_min": w_right,
        "alt_a_unique_only": w_unique,
        "alt_b_first": first,
    }


def classify_row(p: int, q: int, name: str, w: int | None, tau: list[int]) -> dict[str, Any]:
    """Build one selector row with mismatch / hit flags."""
    g = q - p
    if w is None:
        return {
            "selector": name,
            "p": p,
            "q": q,
            "g": g,
            "w": None,
            "tau_w": None,
            "z": None,
            "z4": False,
            "hit_twin": False,
            "mismatch": False,
            "unresolved": True,
        }
    z = zcount(w)
    z4 = z >= ZERO_THRESHOLD
    return {
        "selector": name,
        "p": p,
        "q": q,
        "g": g,
        "w": w,
        "tau_w": tau[w],
        "z": z,
        "z4": z4,
        "hit_twin": bool(z4 and g == 2),
        "mismatch": bool(z4 and g > 2),
        "unresolved": False,
    }


def analyze_gap(p: int, q: int, tau: list[int]) -> dict[str, dict[str, Any]]:
    """Analyze one gap under all selectors."""
    ws = select_witnesses(p, q, tau)
    return {
        name: classify_row(p, q, name, w, tau) for name, w in ws.items()
    }


def empty_stats() -> dict[str, Any]:
    return {
        "gaps": 0,
        "z4": 0,
        "hit_twin": 0,
        "mismatch": 0,
        "ties_differ_from_gwr": 0,
        "sample_mismatches": [],
    }


def run_probe(
    p_max: int,
    sample_cap: int = 15,
    p_min: int = 11,
) -> dict[str, Any]:
    """Scan consecutive gaps with left prime in [p_min, p_max]."""
    t0 = time.time()
    hard_limit = p_max + 400
    primes = sieve_primes(hard_limit)
    tau = divisor_counts(hard_limit)

    selector_keys = (
        "gwr",
        "alt_a_rightmost_min",
        "alt_a_unique_only",
        "alt_b_first",
    )
    stats = {k: empty_stats() for k in selector_keys}
    gaps = 0
    pinned_seen = {ce["p"]: False for ce in PINNED_GWR_CE}
    unique_unresolved = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        if p < p_min:
            continue
        if p > p_max:
            break
        q = primes[i + 1]
        if q > hard_limit:
            break
        gaps += 1
        rows = analyze_gap(p, q, tau)

        # Track when rightmost-min differs from GWR (tie for min-tau).
        if (
            rows["gwr"]["w"] is not None
            and rows["alt_a_rightmost_min"]["w"] is not None
            and rows["gwr"]["w"] != rows["alt_a_rightmost_min"]["w"]
        ):
            stats["alt_a_rightmost_min"]["ties_differ_from_gwr"] += 1

        if rows["alt_a_unique_only"]["unresolved"]:
            unique_unresolved += 1

        for key, row in rows.items():
            s = stats[key]
            s["gaps"] += 1
            if row["unresolved"]:
                continue
            if row["z4"]:
                s["z4"] += 1
            if row["hit_twin"]:
                s["hit_twin"] += 1
            if row["mismatch"]:
                s["mismatch"] += 1
                if len(s["sample_mismatches"]) < sample_cap:
                    s["sample_mismatches"].append(
                        {
                            "p": row["p"],
                            "q": row["q"],
                            "g": row["g"],
                            "w": row["w"],
                            "tau_w": row["tau_w"],
                            "z": row["z"],
                        }
                    )

        if rows["gwr"]["mismatch"] and p in pinned_seen:
            pinned_seen[p] = True

    m_gwr = stats["gwr"]["mismatch"]
    m_a_right = stats["alt_a_rightmost_min"]["mismatch"]
    m_a_unique = stats["alt_a_unique_only"]["mismatch"]
    m_b = stats["alt_b_first"]["mismatch"]

    # H-absolute is already globally invalidated in PROOF.md.
    # Regime labels only reconfirm or note that known CEs lie outside the window.
    # Never emit "not_falsified_in_tested_regime" for H-absolute (that reopens Super-Signal).
    pinned_in_regime = [ce for ce in PINNED_GWR_CE if ce["p"] <= p_max]
    if m_gwr > 0:
        h_absolute_status = "invalidated_reconfirmed_on_regime"
    elif pinned_in_regime:
        h_absolute_status = "invalidated_known_PROOF_CEs_in_regime_not_hit"
    else:
        h_absolute_status = "invalidated_known_PROOF_no_CE_in_regime"

    # Comparative falsifiers from the share:
    # 1) an alternative has zero mismatches on multi-thousand gaps
    # 2) an alternative has strictly fewer mismatches than GWR
    alt_counts = {
        "alt_a_rightmost_min": m_a_right,
        "alt_a_unique_only": m_a_unique,
        "alt_b_first": m_b,
    }
    any_strictly_fewer = any(m < m_gwr for m in alt_counts.values())
    # "at least one mismatch" is tested on the share's named alts a and b.
    # For unique-only, zero can mean "never fired" rather than perfect rule.
    share_a_zero = m_a_right == 0  # position-ignored global min reading
    share_b_zero = m_b == 0
    share_a_or_b_zero_on_large = gaps >= 2000 and (share_a_zero or share_b_zero)

    if any_strictly_fewer:
        h_comparative_status = "falsified"
    elif share_a_or_b_zero_on_large:
        h_comparative_status = "falsified_zero_mismatch_arm"
    elif m_a_right >= 1 and m_b >= 1:
        h_comparative_status = "not_falsified_in_tested_regime"
    elif gaps < 2000:
        h_comparative_status = "regime_too_small"
    else:
        h_comparative_status = "falsified_zero_mismatch_arm"

    return {
        "status": "measured",
        "not_a_theorem": True,
        "source_share": "https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553",
        "moduli_M_v1": list(MODULI),
        "zero_threshold": ZERO_THRESHOLD,
        "selectors": {
            "gwr": "leftmost interior n with minimal tau",
            "alt_a_rightmost_min": (
                "rightmost interior n with minimal tau "
                "(global min-tau, leftmost bias removed)"
            ),
            "alt_a_unique_only": (
                "single global min-tau n only when ties==1; else unresolved"
            ),
            "alt_b_first": "first interior p+1 (no tau minimization)",
        },
        "mismatch_definition": "z(w) >= 4 and g > 2",
        "regime": {
            "left_prime_min": p_min,
            "left_prime_max_inclusive": p_max,
            "gaps_scanned": gaps,
            "unique_only_unresolved_gaps": unique_unresolved,
            "seconds": round(time.time() - t0, 3),
        },
        "counts_by_selector": {
            k: {
                "gaps": v["gaps"],
                "z4": v["z4"],
                "hit_twin": v["hit_twin"],
                "mismatch": v["mismatch"],
                "ties_differ_from_gwr": v.get("ties_differ_from_gwr", 0),
                "twin_rate_among_z4": (
                    round(v["hit_twin"] / v["z4"], 6) if v["z4"] else None
                ),
            }
            for k, v in stats.items()
        },
        "sample_mismatches": {
            k: v["sample_mismatches"] for k, v in stats.items()
        },
        "decisions": {
            "H_absolute_universal_z4_implies_g2": {
                "status": h_absolute_status,
                "gwr_mismatch_count": m_gwr,
                "note": (
                    "Universal Super-Signal already invalidated in PROOF.md. "
                    "Status enum is always invalidated_*; never reopened as open "
                    "on regimes that miss the pinned CEs."
                ),
            },
            "H_comparative_selector_necessity": {
                "status": h_comparative_status,
                "gwr_mismatch": m_gwr,
                "alt_a_rightmost_min_mismatch": m_a_right,
                "alt_a_unique_only_mismatch": m_a_unique,
                "alt_b_first_mismatch": m_b,
                "any_alt_strictly_fewer_than_gwr": any_strictly_fewer,
                "alt_a_rightmost_strictly_fewer": m_a_right < m_gwr,
                "alt_a_unique_strictly_fewer": m_a_unique < m_gwr,
                "alt_b_strictly_fewer": m_b < m_gwr,
                "alt_a_rightmost_at_least_one": m_a_right >= 1,
                "alt_b_at_least_one": m_b >= 1,
            },
        },
        "pinned_ce_visibility": {
            "expected_when_p_max_ge": 22_284_029,
            "seen": pinned_seen,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p-min", type=int, default=11)
    ap.add_argument(
        "--p-max",
        type=int,
        default=2_000_000,
        help="Inclusive max left prime (default 2e6)",
    )
    ap.add_argument("--sample-cap", type=int, default=15)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON path (default artifacts/results_pmax_<n>.json)",
    )
    args = ap.parse_args()
    out = args.out or (HERE / "artifacts" / f"results_pmax_{args.p_max}.json")
    out.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"Selector probe: p in [{args.p_min}, {args.p_max}], M_v1={MODULI}",
        flush=True,
    )
    result = run_probe(args.p_max, sample_cap=args.sample_cap, p_min=args.p_min)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("\n=== mismatch counts (z>=4 and g>2) ===", flush=True)
    for k, v in result["counts_by_selector"].items():
        print(
            f"  {k}: mismatch={v['mismatch']}  z4={v['z4']}  "
            f"hit_twin={v['hit_twin']}  twin_rate_among_z4={v['twin_rate_among_z4']}",
            flush=True,
        )
    print(f"gaps: {result['regime']['gaps_scanned']}", flush=True)
    print(
        f"H-absolute: {result['decisions']['H_absolute_universal_z4_implies_g2']['status']}",
        flush=True,
    )
    print(
        f"H-comparative: {result['decisions']['H_comparative_selector_necessity']['status']}",
        flush=True,
    )
    print(f"seconds: {result['regime']['seconds']}", flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
