#!/usr/bin/env python3
"""Falsification probe: left-endpoint parity modular bias under min-tau.

PGS objects first:
  ordered prime gap (p, q)
  -> divisor-count field tau on the interior
  -> min-tau set; leftmost (GWR) and rightmost witnesses
  -> witness parity and endpoint flag (w == p + 1)
  -> remainder-zero count z on M_v1
  -> mismatch if z >= T and g > 2

Hypotheses under attack: H-parity, H-endpoint, H-rightmost, H-tie-break.
See HYPOTHESIS.md.

Classical sieves prepare primes and tau only. They do not choose the decision.
No Miller-Rabin / isprime / nextprime / gcd / product closure in the inference path.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

MODULI = (2, 3, 5, 7, 30, 210, 2310)
HERE = Path(__file__).resolve().parent
ZERO_THRESHOLD_PRIMARY = 4
ZERO_THRESHOLD_ALT = 3

# Pinned mod30-adjacent counterexamples (PROOF.md certificates).
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


def min_tau_set(p: int, q: int, tau: list[int]) -> list[int]:
    """Interior n in (p, q) achieving minimal tau, left-to-right order."""
    first = p + 1
    if first > q - 1:
        return []
    min_t = min(tau[n] for n in range(first, q))
    return [n for n in range(first, q) if tau[n] == min_t]


def rate(num: int, den: int) -> float | None:
    if den == 0:
        return None
    return round(num / den, 9)


def empty_bucket() -> dict[str, int]:
    return {
        "gaps": 0,
        "z3": 0,
        "z4": 0,
        "mismatch_z3": 0,
        "mismatch_z4": 0,
        "hit_twin_z4": 0,
        "w_is_p1": 0,
        "w_even": 0,
        "w_odd": 0,
    }


def bump(bucket: dict[str, int], *, z: int, g: int, w: int, p: int) -> None:
    bucket["gaps"] += 1
    if w % 2 == 0:
        bucket["w_even"] += 1
    else:
        bucket["w_odd"] += 1
    if w == p + 1:
        bucket["w_is_p1"] += 1
    if z >= ZERO_THRESHOLD_ALT:
        bucket["z3"] += 1
    if z >= ZERO_THRESHOLD_PRIMARY:
        bucket["z4"] += 1
    if z >= ZERO_THRESHOLD_ALT and g > 2:
        bucket["mismatch_z3"] += 1
    if z >= ZERO_THRESHOLD_PRIMARY and g > 2:
        bucket["mismatch_z4"] += 1
    if z >= ZERO_THRESHOLD_PRIMARY and g == 2:
        bucket["hit_twin_z4"] += 1


def summarize_bucket(bucket: dict[str, int]) -> dict[str, Any]:
    g = bucket["gaps"]
    return {
        **bucket,
        "rate_mismatch_z4": rate(bucket["mismatch_z4"], g),
        "rate_mismatch_z3": rate(bucket["mismatch_z3"], g),
        "rate_z4": rate(bucket["z4"], g),
        "rate_z3": rate(bucket["z3"], g),
        "rate_w_is_p1": rate(bucket["w_is_p1"], g),
        "twin_rate_among_z4": rate(bucket["hit_twin_z4"], bucket["z4"]),
    }


def run_probe(
    p_max: int,
    p_min: int = 11,
    sample_cap: int = 20,
    exclusive_min: bool = False,
) -> dict[str, Any]:
    """Scan consecutive gaps with left prime in the stated window.

    If exclusive_min is True, require p > p_min (fresh open interval on the left).
    If False, require p >= p_min (closed on the left).
    Right bound is always p <= p_max inclusive.
    """
    t0 = time.time()
    hard_limit = p_max + 400
    primes = sieve_primes(hard_limit)
    tau = divisor_counts(hard_limit)

    # Global leftmost / rightmost mismatch tallies.
    left_mm4 = 0
    right_mm4 = 0
    left_mm3 = 0
    right_mm3 = 0
    left_z4 = 0
    right_z4 = 0
    gaps = 0
    twins = 0
    g_gt_2 = 0

    # Probe 1: GWR even vs odd.
    gwr_even = empty_bucket()
    gwr_odd = empty_bucket()

    # Probe 2: endpoint vs not under GWR.
    gwr_at_p1 = empty_bucket()
    gwr_not_p1 = empty_bucket()

    # Probe 4: unique vs ties.
    unique = empty_bucket()
    unique_even = empty_bucket()
    unique_odd = empty_bucket()
    unique_at_p1 = empty_bucket()
    unique_not_p1 = empty_bucket()
    ties = empty_bucket()
    ties_left_even = empty_bucket()
    ties_left_odd = empty_bucket()
    ties_left_at_p1 = empty_bucket()
    ties_left_not_p1 = empty_bucket()
    ties_right_even = empty_bucket()
    ties_right_odd = empty_bucket()

    # Tie structure details.
    ties_count = 0
    ties_left_is_p1 = 0
    ties_right_is_p1 = 0
    ties_p1_in_min_set = 0
    ties_left_even_count = 0
    ties_right_even_count = 0
    ties_left_even_right_odd = 0
    ties_left_odd_right_even = 0
    ties_both_even = 0
    ties_both_odd = 0
    ties_min_set_size_hist: dict[str, int] = {}

    # Endpoint concentration on mismatches.
    gwr_mm4_samples: list[dict[str, Any]] = []
    gwr_mm4_at_p1 = 0
    gwr_mm4_even = 0
    gwr_mm4_odd = 0
    gwr_mm4_unique = 0
    gwr_mm4_ties = 0
    gwr_z4_at_p1 = 0
    gwr_z4_total = 0

    pinned_seen = {ce["p"]: False for ce in PINNED_GWR_CE}

    # Structural sanity: odd z4 should stay 0.
    odd_z4_events = 0
    odd_z3_events = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        if exclusive_min:
            if p <= p_min:
                continue
        else:
            if p < p_min:
                continue
        if p > p_max:
            break
        q = primes[i + 1]
        if q > hard_limit:
            break

        mins = min_tau_set(p, q, tau)
        if not mins:
            continue

        gaps += 1
        g = q - p
        if g == 2:
            twins += 1
        else:
            g_gt_2 += 1

        w_left = mins[0]
        w_right = mins[-1]
        unique_min = len(mins) == 1
        z_left = zcount(w_left)
        z_right = zcount(w_right)

        if z_left >= 4:
            left_z4 += 1
            gwr_z4_total += 1
            if w_left == p + 1:
                gwr_z4_at_p1 += 1
        if z_right >= 4:
            right_z4 += 1

        left_mm4_flag = z_left >= 4 and g > 2
        right_mm4_flag = z_right >= 4 and g > 2
        left_mm3_flag = z_left >= 3 and g > 2
        right_mm3_flag = z_right >= 3 and g > 2

        if left_mm4_flag:
            left_mm4 += 1
        if right_mm4_flag:
            right_mm4 += 1
        if left_mm3_flag:
            left_mm3 += 1
        if right_mm3_flag:
            right_mm3 += 1

        # Probe 1 parity split (GWR).
        if w_left % 2 == 0:
            bump(gwr_even, z=z_left, g=g, w=w_left, p=p)
        else:
            bump(gwr_odd, z=z_left, g=g, w=w_left, p=p)
            if z_left >= 4:
                odd_z4_events += 1
            if z_left >= 3:
                odd_z3_events += 1

        # Probe 2 endpoint split (GWR).
        if w_left == p + 1:
            bump(gwr_at_p1, z=z_left, g=g, w=w_left, p=p)
        else:
            bump(gwr_not_p1, z=z_left, g=g, w=w_left, p=p)

        # Probe 4 unique vs ties.
        if unique_min:
            bump(unique, z=z_left, g=g, w=w_left, p=p)
            if w_left % 2 == 0:
                bump(unique_even, z=z_left, g=g, w=w_left, p=p)
            else:
                bump(unique_odd, z=z_left, g=g, w=w_left, p=p)
            if w_left == p + 1:
                bump(unique_at_p1, z=z_left, g=g, w=w_left, p=p)
            else:
                bump(unique_not_p1, z=z_left, g=g, w=w_left, p=p)
        else:
            ties_count += 1
            bump(ties, z=z_left, g=g, w=w_left, p=p)
            size_key = str(len(mins)) if len(mins) <= 10 else "gt10"
            ties_min_set_size_hist[size_key] = ties_min_set_size_hist.get(size_key, 0) + 1

            if w_left == p + 1:
                ties_left_is_p1 += 1
                bump(ties_left_at_p1, z=z_left, g=g, w=w_left, p=p)
            else:
                bump(ties_left_not_p1, z=z_left, g=g, w=w_left, p=p)
            if w_right == p + 1:
                ties_right_is_p1 += 1
            if p + 1 in mins:
                ties_p1_in_min_set += 1

            if w_left % 2 == 0:
                ties_left_even_count += 1
                bump(ties_left_even, z=z_left, g=g, w=w_left, p=p)
            else:
                bump(ties_left_odd, z=z_left, g=g, w=w_left, p=p)

            if w_right % 2 == 0:
                ties_right_even_count += 1
                bump(ties_right_even, z=z_right, g=g, w=w_right, p=p)
            else:
                bump(ties_right_odd, z=z_right, g=g, w=w_right, p=p)

            le = w_left % 2 == 0
            re = w_right % 2 == 0
            if le and re:
                ties_both_even += 1
            elif (not le) and (not re):
                ties_both_odd += 1
            elif le and (not re):
                ties_left_even_right_odd += 1
            else:
                ties_left_odd_right_even += 1

        # Mismatch forensics for GWR z4 non-twins.
        if left_mm4_flag:
            if w_left == p + 1:
                gwr_mm4_at_p1 += 1
            if w_left % 2 == 0:
                gwr_mm4_even += 1
            else:
                gwr_mm4_odd += 1
            if unique_min:
                gwr_mm4_unique += 1
            else:
                gwr_mm4_ties += 1
            if len(gwr_mm4_samples) < sample_cap:
                gwr_mm4_samples.append(
                    {
                        "p": p,
                        "q": q,
                        "g": g,
                        "w_left": w_left,
                        "w_right": w_right,
                        "z_left": z_left,
                        "z_right": z_right,
                        "tau_left": tau[w_left],
                        "tau_right": tau[w_right],
                        "min_set_size": len(mins),
                        "w_left_is_p1": w_left == p + 1,
                        "w_left_even": w_left % 2 == 0,
                        "p1_in_min_set": (p + 1) in mins,
                        "unique_min": unique_min,
                    }
                )
            if p in pinned_seen:
                pinned_seen[p] = True

    # --- Decision rules (pre-registered disconfirmations) ---
    rate_even_mm4 = rate(gwr_even["mismatch_z4"], gwr_even["gaps"])
    rate_odd_mm4 = rate(gwr_odd["mismatch_z4"], gwr_odd["gaps"])
    rate_even_mm3 = rate(gwr_even["mismatch_z3"], gwr_even["gaps"])
    rate_odd_mm3 = rate(gwr_odd["mismatch_z3"], gwr_odd["gaps"])

    # D-a: no measurable even-vs-odd mismatch difference at z>=4.
    # Degenerate if odd_z4 is structurally zero and even has any mismatch, or both zero.
    structural_odd_z4_impossible = odd_z4_events == 0
    if gwr_even["gaps"] == 0 or gwr_odd["gaps"] == 0:
        d_a = "unresolved_empty_parity_bucket"
        h_parity_z4 = "unresolved"
    elif rate_even_mm4 is not None and rate_odd_mm4 is not None:
        if rate_even_mm4 > rate_odd_mm4:
            if structural_odd_z4_impossible and gwr_odd["mismatch_z4"] == 0:
                d_a = "not_met_but_structurally_forced"
                h_parity_z4 = "weakened_logically_forced_by_z4_implies_even"
            else:
                d_a = "not_met_empirical_strict"
                h_parity_z4 = "survives_measured"
        elif rate_even_mm4 == rate_odd_mm4:
            if gwr_even["mismatch_z4"] == 0 and gwr_odd["mismatch_z4"] == 0:
                d_a = "vacuous_both_zero_no_mismatch_surface"
                h_parity_z4 = "no_mismatch_surface"
            else:
                d_a = "met_equal_rates"
                h_parity_z4 = "falsified"
        else:
            d_a = "met_odd_higher"
            h_parity_z4 = "falsified"
    else:
        d_a = "unresolved"
        h_parity_z4 = "unresolved"

    # D-a3: non-degenerate z>=3 even vs odd.
    if gwr_even["gaps"] == 0 or gwr_odd["gaps"] == 0:
        d_a3 = "unresolved_empty_parity_bucket"
        h_parity_z3 = "unresolved"
    elif rate_even_mm3 is not None and rate_odd_mm3 is not None:
        if rate_even_mm3 > rate_odd_mm3:
            d_a3 = "not_met_even_strictly_higher"
            h_parity_z3 = "survives_measured"
        elif rate_even_mm3 == rate_odd_mm3:
            if gwr_even["mismatch_z3"] == 0 and gwr_odd["mismatch_z3"] == 0:
                d_a3 = "vacuous_both_zero_no_mismatch_surface"
                h_parity_z3 = "no_mismatch_surface"
            else:
                d_a3 = "met_equal_rates"
                h_parity_z3 = "falsified"
        else:
            d_a3 = "met_odd_higher_or_not_strict"
            h_parity_z3 = "falsified"
    else:
        d_a3 = "unresolved"
        h_parity_z3 = "unresolved"

    # D-b: rightmost produces MORE mismatches than leftmost on this regime.
    if left_mm4 < right_mm4:
        d_b = "met_rightmost_more_mismatches"
        h_rightmost = "falsified"
    elif left_mm4 > right_mm4:
        d_b = "not_met_rightmost_fewer"
        h_rightmost = "survives_measured"
    else:
        d_b = "not_met_equal_counts"
        # Equal is not the pre-registered "rightmost MORE" kill, but also not
        # the predicted "rightmost fewer". Label as not confirming prediction.
        h_rightmost = "not_confirmed_equal_counts"

    # D-c: mismatches not concentrated at p+1.
    if left_mm4 == 0:
        d_c = "no_gwr_mismatches_in_regime"
        h_endpoint = "no_mismatch_surface"
        frac_mm_at_p1 = None
    else:
        frac_mm_at_p1 = rate(gwr_mm4_at_p1, left_mm4)
        # Concentration: fraction >= 0.5 treated as concentrated (pre-registered
        # soft threshold for this probe; exact fraction always reported).
        if frac_mm_at_p1 is not None and frac_mm_at_p1 >= 0.5:
            d_c = "not_met_concentrated_at_p1"
            h_endpoint = "survives_measured"
        else:
            d_c = "met_not_concentrated_at_p1"
            h_endpoint = "falsified_or_weakened"

    # D-d: unique-min shows same p+1 inflation without ties.
    unique_mm4 = unique["mismatch_z4"]
    ties_mm4 = ties["mismatch_z4"]
    if unique_mm4 > 0 and ties_mm4 == 0:
        d_d = "unique_carries_all_mismatches"
        h_tie_break = "weakened_unique_alone_suffices"
    elif unique_mm4 == 0 and ties_mm4 > 0:
        d_d = "ties_carry_all_mismatches"
        h_tie_break = "survives_measured_ties_only"
    elif unique_mm4 == 0 and ties_mm4 == 0:
        d_d = "no_mismatches"
        h_tie_break = "no_mismatch_surface"
    else:
        d_d = "both_unique_and_ties_mismatch"
        h_tie_break = "mixed_measured"

    return {
        "status": "measured",
        "not_a_theorem": True,
        "hypothesis": "left-endpoint parity modular bias under min-tau gap reading",
        "moduli_M_v1": list(MODULI),
        "mismatch_definitions": {
            "primary": "z(w) >= 4 and g > 2",
            "alt_z3": "z(w) >= 3 and g > 2",
        },
        "regime": {
            "left_prime_min": p_min,
            "left_prime_min_exclusive": exclusive_min,
            "left_prime_max_inclusive": p_max,
            "gaps_scanned": gaps,
            "twins_g2": twins,
            "gaps_g_gt_2": g_gt_2,
            "seconds": round(time.time() - t0, 3),
        },
        "probe1_parity_gwr": {
            "even": summarize_bucket(gwr_even),
            "odd": summarize_bucket(gwr_odd),
            "rate_mismatch_z4_even": rate_even_mm4,
            "rate_mismatch_z4_odd": rate_odd_mm4,
            "rate_mismatch_z3_even": rate_even_mm3,
            "rate_mismatch_z3_odd": rate_odd_mm3,
            "strict_even_higher_z4": (
                rate_even_mm4 is not None
                and rate_odd_mm4 is not None
                and rate_even_mm4 > rate_odd_mm4
            ),
            "strict_even_higher_z3": (
                rate_even_mm3 is not None
                and rate_odd_mm3 is not None
                and rate_even_mm3 > rate_odd_mm3
            ),
            "odd_z4_events": odd_z4_events,
            "odd_z3_events": odd_z3_events,
            "structural_note": (
                "On M_v1, z >= 4 forces 30|w hence even; odd GWR witnesses "
                "cannot mismatch under the primary definition."
            ),
        },
        "probe2_endpoint_gwr": {
            "at_p1": summarize_bucket(gwr_at_p1),
            "not_p1": summarize_bucket(gwr_not_p1),
            "z4_total": gwr_z4_total,
            "z4_at_p1": gwr_z4_at_p1,
            "frac_z4_at_p1": rate(gwr_z4_at_p1, gwr_z4_total),
            "mismatch_z4_total": left_mm4,
            "mismatch_z4_at_p1": gwr_mm4_at_p1,
            "frac_mismatch_z4_at_p1": frac_mm_at_p1,
        },
        "probe3_left_vs_right": {
            "leftmost_mismatch_z4": left_mm4,
            "rightmost_mismatch_z4": right_mm4,
            "leftmost_mismatch_z3": left_mm3,
            "rightmost_mismatch_z3": right_mm3,
            "leftmost_z4": left_z4,
            "rightmost_z4": right_z4,
            "rightmost_strictly_fewer_z4": right_mm4 < left_mm4,
            "rightmost_strictly_more_z4": right_mm4 > left_mm4,
        },
        "probe4_ties_vs_unique": {
            "unique": summarize_bucket(unique),
            "unique_even": summarize_bucket(unique_even),
            "unique_odd": summarize_bucket(unique_odd),
            "unique_at_p1": summarize_bucket(unique_at_p1),
            "unique_not_p1": summarize_bucket(unique_not_p1),
            "ties": summarize_bucket(ties),
            "ties_left_even": summarize_bucket(ties_left_even),
            "ties_left_odd": summarize_bucket(ties_left_odd),
            "ties_left_at_p1": summarize_bucket(ties_left_at_p1),
            "ties_left_not_p1": summarize_bucket(ties_left_not_p1),
            "ties_right_even": summarize_bucket(ties_right_even),
            "ties_right_odd": summarize_bucket(ties_right_odd),
            "tie_structure": {
                "ties_count": ties_count,
                "ties_left_is_p1": ties_left_is_p1,
                "ties_right_is_p1": ties_right_is_p1,
                "ties_p1_in_min_set": ties_p1_in_min_set,
                "frac_ties_left_is_p1": rate(ties_left_is_p1, ties_count),
                "frac_ties_p1_in_min_set": rate(ties_p1_in_min_set, ties_count),
                "ties_left_even": ties_left_even_count,
                "ties_right_even": ties_right_even_count,
                "frac_ties_left_even": rate(ties_left_even_count, ties_count),
                "frac_ties_right_even": rate(ties_right_even_count, ties_count),
                "ties_left_even_right_odd": ties_left_even_right_odd,
                "ties_left_odd_right_even": ties_left_odd_right_even,
                "ties_both_even": ties_both_even,
                "ties_both_odd": ties_both_odd,
                "min_set_size_hist": ties_min_set_size_hist,
            },
            "gwr_mismatch_z4_unique": gwr_mm4_unique,
            "gwr_mismatch_z4_ties": gwr_mm4_ties,
            "gwr_mismatch_z4_even": gwr_mm4_even,
            "gwr_mismatch_z4_odd": gwr_mm4_odd,
            "gwr_mismatch_z4_at_p1": gwr_mm4_at_p1,
        },
        "gwr_mismatch_z4_samples": gwr_mm4_samples,
        "pinned_ce_visibility": {
            "expected_when_window_covers": [ce["p"] for ce in PINNED_GWR_CE],
            "seen": pinned_seen,
        },
        "decisions": {
            "D_a_even_vs_odd_z4": {
                "criterion": "no measurable even-vs-odd mismatch difference at z>=4",
                "result": d_a,
                "H_parity_z4_status": h_parity_z4,
            },
            "D_a3_even_vs_odd_z3": {
                "criterion": "at z>=3, even rate not strictly higher than odd",
                "result": d_a3,
                "H_parity_z3_status": h_parity_z3,
            },
            "D_b_rightmost_more": {
                "criterion": "rightmost MORE mismatches than leftmost",
                "result": d_b,
                "H_rightmost_status": h_rightmost,
                "leftmost_mm4": left_mm4,
                "rightmost_mm4": right_mm4,
            },
            "D_c_endpoint_concentration": {
                "criterion": "mismatches not concentrated at w==p+1",
                "result": d_c,
                "H_endpoint_status": h_endpoint,
                "frac_mismatch_at_p1": frac_mm_at_p1,
            },
            "D_d_unique_vs_ties": {
                "criterion": "unique-min alone carries p+1 inflation (weakens tie-break story)",
                "result": d_d,
                "H_tie_break_status": h_tie_break,
                "unique_mm4": unique_mm4,
                "ties_mm4": ties_mm4,
            },
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--p-min", type=int, default=11)
    ap.add_argument("--p-max", type=int, default=2_000_000)
    ap.add_argument(
        "--exclusive-min",
        action="store_true",
        help="Require p > p_min (open on the left); default is p >= p_min",
    )
    ap.add_argument("--sample-cap", type=int, default=20)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    tag = f"pmin_{args.p_min}_pmax_{args.p_max}"
    if args.exclusive_min:
        tag = f"pgt_{args.p_min}_pmax_{args.p_max}"
    out = args.out or (HERE / "artifacts" / f"results_{tag}.json")
    out.parent.mkdir(parents=True, exist_ok=True)

    left_note = f"p > {args.p_min}" if args.exclusive_min else f"p >= {args.p_min}"
    print(
        f"Parity-bias probe: {left_note}, p <= {args.p_max}, M_v1={MODULI}",
        flush=True,
    )
    result = run_probe(
        p_max=args.p_max,
        p_min=args.p_min,
        sample_cap=args.sample_cap,
        exclusive_min=args.exclusive_min,
    )
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    r = result["regime"]
    p1 = result["probe1_parity_gwr"]
    p2 = result["probe2_endpoint_gwr"]
    p3 = result["probe3_left_vs_right"]
    print(f"gaps: {r['gaps_scanned']}  twins: {r['twins_g2']}  g>2: {r['gaps_g_gt_2']}", flush=True)
    print(
        f"parity z4 mm rates: even={p1['rate_mismatch_z4_even']} "
        f"odd={p1['rate_mismatch_z4_odd']}",
        flush=True,
    )
    print(
        f"parity z3 mm rates: even={p1['rate_mismatch_z3_even']} "
        f"odd={p1['rate_mismatch_z3_odd']}",
        flush=True,
    )
    print(
        f"endpoint: mm4_at_p1={p2['mismatch_z4_at_p1']}/{p2['mismatch_z4_total']} "
        f"frac={p2['frac_mismatch_z4_at_p1']}",
        flush=True,
    )
    print(
        f"L vs R mm4: left={p3['leftmost_mismatch_z4']} "
        f"right={p3['rightmost_mismatch_z4']}",
        flush=True,
    )
    print("decisions:", flush=True)
    for k, v in result["decisions"].items():
        status_key = [x for x in v if x.endswith("_status")][0]
        print(f"  {k}: {v['result']} -> {v[status_key]}", flush=True)
    print(f"seconds: {r['seconds']}", flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
