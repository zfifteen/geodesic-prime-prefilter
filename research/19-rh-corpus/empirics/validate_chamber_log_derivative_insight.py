#!/usr/bin/env python3
"""Falsify or validate: gap-local rho tracks (1/2)log m, not global R(s).

Core insight under test
-----------------------
For a nonempty prime-gap interior I = {p+1, ..., q-1} and fixed s > 1:

  rho_I(s) = sum_I H(n) n^{-s} / sum_I tau(n) n^{-s}
  H(n)     = tau(n) * log(n) / 2

is a tau-weighted average of (1/2) log n on I. It therefore tracks the
integer scale of the gap (about (1/2) log m, m midpoint), while the global
ratio R_N(s) ~ -zeta'/zeta stays an s-only constant. Their gap must grow
like (1/2) log m.

Status: experiment / measured only. Not a theorem about RH.

Predictions (must all hold or the insight is falsified)
-------------------------------------------------------
P1  Scale track:  |rho_I(s) - 0.5 * log m| <= 0.05  for all nonempty
    chambers with m >= 1000 (allowing short-gap and weight effects; the
    algebraic identity is exact for a single point; multi-point chambers
    stay near midpoint log).

P2  Forced divergence: for m >= 1000,
    |rho_I(s) - R_N(s)| >= 0.25 * log m.

P3  Growth law: in each scale bin of midpoints, the median of
    |rho_I - R_N| / log m lies in [0.40, 0.60], and the median absolute
    gap |rho_I - R_N| is nondecreasing across successive bins.

P4  Anti-convergence: raising the partial-sum length N does not make
    chamber rho agree with R. Compare N_small vs N_full on a fixed
    chamber set; |rho - R_N| must not systematically shrink toward zero
    as N grows (rho is chamber-local and independent of N once N >= q).

Usage
-----
  PYTHONPATH=src/python:research/19-rh-corpus/empirics \\
    python3 research/19-rh-corpus/empirics/validate_chamber_log_derivative_insight.py
"""

from __future__ import annotations

import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from sympy import primerange

from z_band_prime_rh_bridge.bridge import (
    divisor_counts_up_to,
    evaluate_partial_sum_bridge,
    normalization_load_coefficients_up_to,
)

from chamber_compression import FIXED_POINT_V

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent / "output"
OUT_JSON = OUT_DIR / "chamber_log_derivative_insight_validation.json"

# Regime
PRIME_LIMIT = 50_000
S_VALUES = (2.0, 2.5, 3.0, 3.5, 4.0)
M_MIN_STRICT = 1_000
HALF_LOG_TOL = 0.05
DIV_FLOOR_FRAC = 0.25  # |rho - R| >= this * log m
GROWTH_MEDIAN_LO = 0.40
GROWTH_MEDIAN_HI = 0.60
SCALE_BINS = (
    (1_000, 3_000),
    (3_000, 10_000),
    (10_000, 30_000),
    (30_000, 60_000),
)


@dataclass(frozen=True)
class ChamberRow:
    p: int
    q: int
    m: float
    gap: int
    s: float
    rho: float
    half_log_m: float
    abs_half_log_err: float
    global_r: float
    abs_div: float
    div_over_log_m: float


def consecutive_prime_pairs(limit: int) -> list[tuple[int, int]]:
    primes = list(primerange(2, limit + 1))
    return list(zip(primes, primes[1:]))


def chamber_rho(
    s: float,
    p: int,
    q: int,
    counts: list[int],
    loads: list[float],
) -> float | None:
    """Return rho_I or None if interior empty or delta_d == 0."""
    interior = range(p + 1, q)
    delta_d = 0.0
    delta_b = 0.0
    for n in interior:
        w = n ** (-s)
        tau = counts[n]
        delta_d += tau * w
        # FIXED_POINT_V * load = H(n) = tau * log(n) / 2
        delta_b += FIXED_POINT_V * loads[n] * w
    if delta_d == 0.0:
        return None
    return delta_b / delta_d


def median(xs: list[float]) -> float:
    if not xs:
        return float("nan")
    ys = sorted(xs)
    n = len(ys)
    mid = n // 2
    if n % 2:
        return ys[mid]
    return 0.5 * (ys[mid - 1] + ys[mid])


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def run() -> dict:
    t0 = time.perf_counter()
    pairs = consecutive_prime_pairs(PRIME_LIMIT)
    max_q = pairs[-1][1]
    # Full bridge terms: cover all chambers
    terms = max_q
    counts = divisor_counts_up_to(terms)
    loads = normalization_load_coefficients_up_to(terms, counts)

    global_r_by_s: dict[float, float] = {}
    global_err_by_s: dict[float, float] = {}
    for s in S_VALUES:
        ev = evaluate_partial_sum_bridge(s, terms)
        global_r_by_s[s] = float(ev.normalized_ratio.real)
        global_err_by_s[s] = float(ev.normalized_ratio_error)

    rows: list[ChamberRow] = []
    empty_interiors = 0
    for p, q in pairs:
        if q - p <= 1:
            # no interior integers
            empty_interiors += 1
            continue
        # q - p == 2 has one interior point (even); still nonempty for odds
        m = 0.5 * (p + q)
        for s in S_VALUES:
            rho = chamber_rho(s, p, q, counts, loads)
            if rho is None:
                empty_interiors += 1
                continue
            half = 0.5 * math.log(m)
            r = global_r_by_s[s]
            abs_div = abs(rho - r)
            rows.append(
                ChamberRow(
                    p=p,
                    q=q,
                    m=m,
                    gap=q - p,
                    s=s,
                    rho=rho,
                    half_log_m=half,
                    abs_half_log_err=abs(rho - half),
                    global_r=r,
                    abs_div=abs_div,
                    div_over_log_m=abs_div / math.log(m) if m > 1 else float("nan"),
                )
            )

    # --- Predictions ---
    strict = [r for r in rows if r.m >= M_MIN_STRICT]

    # P1
    p1_violations = [r for r in strict if r.abs_half_log_err > HALF_LOG_TOL]
    p1_pass = len(p1_violations) == 0
    p1_max_err = max((r.abs_half_log_err for r in strict), default=float("nan"))
    p1_med_err = median([r.abs_half_log_err for r in strict])

    # P2
    p2_violations = [
        r for r in strict if r.abs_div < DIV_FLOOR_FRAC * math.log(r.m)
    ]
    p2_pass = len(p2_violations) == 0
    p2_min_ratio = min((r.div_over_log_m for r in strict), default=float("nan"))
    p2_med_ratio = median([r.div_over_log_m for r in strict])

    # P3 by scale bin (aggregate over all s, and also per-s)
    bin_stats = []
    prev_med_abs: float | None = None
    p3_median_band_ok = True
    p3_nondecreasing_ok = True
    for lo, hi in SCALE_BINS:
        bin_rows = [r for r in rows if lo <= r.m < hi]
        if not bin_rows:
            bin_stats.append(
                {
                    "bin": [lo, hi],
                    "n": 0,
                    "median_div_over_log": None,
                    "median_abs_div": None,
                    "median_half_log_err": None,
                }
            )
            continue
        med_ratio = median([r.div_over_log_m for r in bin_rows])
        med_abs = median([r.abs_div for r in bin_rows])
        med_hl = median([r.abs_half_log_err for r in bin_rows])
        if not (GROWTH_MEDIAN_LO <= med_ratio <= GROWTH_MEDIAN_HI):
            p3_median_band_ok = False
        if prev_med_abs is not None and med_abs + 1e-12 < prev_med_abs:
            # allow tiny float noise; real decrease fails
            if med_abs < prev_med_abs - 1e-6:
                p3_nondecreasing_ok = False
        prev_med_abs = med_abs
        bin_stats.append(
            {
                "bin": [lo, hi],
                "n": len(bin_rows),
                "median_div_over_log": med_ratio,
                "median_abs_div": med_abs,
                "median_half_log_err": med_hl,
                "mean_rho": mean([r.rho for r in bin_rows]),
                "mean_half_log_m": mean([r.half_log_m for r in bin_rows]),
                "mean_global_r": mean([r.global_r for r in bin_rows]),
            }
        )
    p3_pass = p3_median_band_ok and p3_nondecreasing_ok

    # P4: rho independent of N (once N >= q). Recompute rho with same counts;
    # vary only R_N at two term budgets. Insight says |rho - R| cannot collapse
    # by enlarging N: rho does not depend on N, R_N converges to a fixed limit.
    sample_pairs = [
        (p, q)
        for p, q in pairs
        if q - p > 1 and 0.5 * (p + q) >= M_MIN_STRICT
    ][:200]
    p4_rows = []
    p4_pass = True
    s_p4 = 2.5
    r_full = global_r_by_s[s_p4]
    # Smaller partial sum: still >= max sample q
    max_sample_q = max(q for _, q in sample_pairs) if sample_pairs else terms
    n_small = max(max_sample_q, min(5_000, terms))
    r_small = float(evaluate_partial_sum_bridge(s_p4, n_small).normalized_ratio.real)
    for p, q in sample_pairs:
        rho = chamber_rho(s_p4, p, q, counts, loads)
        if rho is None:
            continue
        d_full = abs(rho - r_full)
        d_small = abs(rho - r_small)
        # Collapse would mean both near 0; require both stay large
        m = 0.5 * (p + q)
        floor = DIV_FLOOR_FRAC * math.log(m)
        if d_full < floor or d_small < floor:
            p4_pass = False
        p4_rows.append(
            {
                "p": p,
                "q": q,
                "rho": rho,
                "abs_div_N_small": d_small,
                "abs_div_N_full": d_full,
                "floor": floor,
            }
        )
    # Also: enlarging N must not systematically pull R onto rho (impossible
    # since rho grows with log m while R stays O(1)). Check mean |rho-R_full|
    # vs mean |rho-R_small| are both >> 0 and comparable.
    if p4_rows:
        mean_full = mean([x["abs_div_N_full"] for x in p4_rows])
        mean_small = mean([x["abs_div_N_small"] for x in p4_rows])
        if mean_full < 1.0 or mean_small < 1.0:
            p4_pass = False
    else:
        p4_pass = False

    # Per-s summary for the report
    per_s = []
    for s in S_VALUES:
        rs = [r for r in strict if r.s == s]
        per_s.append(
            {
                "s": s,
                "n": len(rs),
                "median_half_log_err": median([r.abs_half_log_err for r in rs]),
                "max_half_log_err": max((r.abs_half_log_err for r in rs), default=None),
                "median_div_over_log": median([r.div_over_log_m for r in rs]),
                "min_div_over_log": min((r.div_over_log_m for r in rs), default=None),
                "global_r": global_r_by_s[s],
                "global_r_error": global_err_by_s[s],
                "p1_violations": sum(1 for r in rs if r.abs_half_log_err > HALF_LOG_TOL),
                "p2_violations": sum(
                    1 for r in rs if r.abs_div < DIV_FLOOR_FRAC * math.log(r.m)
                ),
            }
        )

    # Worst half-log and smallest divergence examples
    worst_hl = max(strict, key=lambda r: r.abs_half_log_err) if strict else None
    smallest_div_ratio = (
        min(strict, key=lambda r: r.div_over_log_m) if strict else None
    )

    all_pass = p1_pass and p2_pass and p3_pass and p4_pass
    elapsed = time.perf_counter() - t0

    payload = {
        "experiment": "chamber_log_derivative_insight_validation",
        "insight": "Gap-local log-derivatives track integer scale, not prime poles",
        "status": "VALIDATED" if all_pass else "FALSIFIED",
        "regime": {
            "prime_limit": PRIME_LIMIT,
            "max_q": max_q,
            "terms_N": terms,
            "s_values": list(S_VALUES),
            "m_min_strict": M_MIN_STRICT,
            "nonempty_chamber_rows": len(rows),
            "strict_rows_m_ge_min": len(strict),
            "prime_pairs": len(pairs),
            "elapsed_sec": round(elapsed, 3),
        },
        "thresholds": {
            "half_log_tol": HALF_LOG_TOL,
            "div_floor_frac": DIV_FLOOR_FRAC,
            "growth_median_band": [GROWTH_MEDIAN_LO, GROWTH_MEDIAN_HI],
        },
        "predictions": {
            "P1_scale_track": {
                "pass": p1_pass,
                "violations": len(p1_violations),
                "max_abs_half_log_err": p1_max_err,
                "median_abs_half_log_err": p1_med_err,
                "worst": asdict(worst_hl) if worst_hl else None,
            },
            "P2_forced_divergence": {
                "pass": p2_pass,
                "violations": len(p2_violations),
                "min_div_over_log_m": p2_min_ratio,
                "median_div_over_log_m": p2_med_ratio,
                "tightest": asdict(smallest_div_ratio) if smallest_div_ratio else None,
            },
            "P3_growth_law": {
                "pass": p3_pass,
                "median_band_ok": p3_median_band_ok,
                "abs_div_nondecreasing_across_bins": p3_nondecreasing_ok,
                "bins": bin_stats,
            },
            "P4_anti_convergence_in_N": {
                "pass": p4_pass,
                "s": s_p4,
                "N_small": n_small,
                "N_full": terms,
                "R_small": r_small,
                "R_full": r_full,
                "sample_chambers": len(p4_rows),
                "mean_abs_div_N_small": mean([x["abs_div_N_small"] for x in p4_rows])
                if p4_rows
                else None,
                "mean_abs_div_N_full": mean([x["abs_div_N_full"] for x in p4_rows])
                if p4_rows
                else None,
            },
        },
        "per_s": per_s,
        "verdict": {
            "all_predictions_pass": all_pass,
            "label": "VALIDATED" if all_pass else "FALSIFIED",
            "claim_status": "measured_support"
            if all_pass
            else "falsified_in_regime",
            "not_a_theorem": True,
            "not_rh": True,
        },
    }
    return payload


def format_report(payload: dict) -> str:
    reg = payload["regime"]
    pred = payload["predictions"]
    verdict = payload["verdict"]["label"]
    lines = []
    lines.append("=" * 72)
    lines.append("EXPERIMENT REPORT: Chamber log-derivative insight")
    lines.append("=" * 72)
    lines.append("")
    lines.append("INSIGHT UNDER TEST")
    lines.append("  Gap-local rho_I(s) tracks (1/2) log(midpoint of the gap).")
    lines.append("  It does NOT sample the global prime-encoding ratio R(s).")
    lines.append("  Therefore |rho_I - R| must grow like (1/2) log m.")
    lines.append("")
    lines.append("REGIME (measured only)")
    lines.append(f"  primes up to          {reg['prime_limit']}")
    lines.append(f"  consecutive pairs     {reg['prime_pairs']}")
    lines.append(f"  chamber-s rows        {reg['nonempty_chamber_rows']}")
    lines.append(f"  rows with m >= {reg['m_min_strict']}  {reg['strict_rows_m_ge_min']}")
    lines.append(f"  s values              {reg['s_values']}")
    lines.append(f"  partial-sum N         {reg['terms_N']}")
    lines.append(f"  runtime               {reg['elapsed_sec']} s")
    lines.append("")
    lines.append("-" * 72)
    lines.append("PREDICTION SCORECARD")
    lines.append("-" * 72)

    def mark(ok: bool) -> str:
        return "PASS" if ok else "FAIL"

    p1 = pred["P1_scale_track"]
    lines.append(
        f"  P1 scale track     [{mark(p1['pass'])}]  "
        f"|rho - 0.5 log m| <= {payload['thresholds']['half_log_tol']}"
    )
    lines.append(
        f"       violations={p1['violations']}  "
        f"median_err={p1['median_abs_half_log_err']:.6g}  "
        f"max_err={p1['max_abs_half_log_err']:.6g}"
    )

    p2 = pred["P2_forced_divergence"]
    lines.append(
        f"  P2 forced diverge  [{mark(p2['pass'])}]  "
        f"|rho - R| >= {payload['thresholds']['div_floor_frac']} * log m"
    )
    lines.append(
        f"       violations={p2['violations']}  "
        f"median(|rho-R|/log m)={p2['median_div_over_log_m']:.6g}  "
        f"min={p2['min_div_over_log_m']:.6g}"
    )

    p3 = pred["P3_growth_law"]
    lines.append(
        f"  P3 growth law      [{mark(p3['pass'])}]  "
        f"median ratio in {payload['thresholds']['growth_median_band']}; "
        f"|rho-R| nondecreasing by scale bin"
    )
    lines.append(
        f"       band_ok={p3['median_band_ok']}  "
        f"nondecreasing={p3['abs_div_nondecreasing_across_bins']}"
    )
    lines.append("       scale bins (median |rho-R|, median |rho-R|/log m):")
    for b in p3["bins"]:
        if b["n"] == 0:
            lines.append(f"         [{b['bin'][0]}, {b['bin'][1]}): n=0")
            continue
        lines.append(
            f"         [{b['bin'][0]:>5}, {b['bin'][1]:>5}): n={b['n']:<6}  "
            f"med|rho-R|={b['median_abs_div']:.4f}  "
            f"med ratio={b['median_div_over_log']:.4f}  "
            f"med half-log err={b['median_half_log_err']:.4e}"
        )

    p4 = pred["P4_anti_convergence_in_N"]
    lines.append(
        f"  P4 anti-converge N [{mark(p4['pass'])}]  "
        f"enlarging partial-sum N does not collapse |rho - R|"
    )
    lines.append(
        f"       s={p4['s']}  N_small={p4['N_small']}  N_full={p4['N_full']}  "
        f"mean|rho-R|_small={p4['mean_abs_div_N_small']:.4f}  "
        f"mean|rho-R|_full={p4['mean_abs_div_N_full']:.4f}"
    )

    lines.append("")
    lines.append("-" * 72)
    lines.append("PER-s DETAIL (m >= 1000)")
    lines.append("-" * 72)
    lines.append(
        f"  {'s':>4}  {'n':>6}  {'med_hl_err':>12}  {'max_hl_err':>12}  "
        f"{'med|rho-R|/logm':>16}  {'min ratio':>10}  {'R':>10}"
    )
    for row in payload["per_s"]:
        lines.append(
            f"  {row['s']:4.1f}  {row['n']:6d}  "
            f"{row['median_half_log_err']:12.6g}  "
            f"{row['max_half_log_err']:12.6g}  "
            f"{row['median_div_over_log']:16.6g}  "
            f"{row['min_div_over_log']:10.6g}  "
            f"{row['global_r']:10.6g}"
        )

    lines.append("")
    lines.append("-" * 72)
    lines.append("WHAT THIS MEANS IN PLAIN LANGUAGE")
    lines.append("-" * 72)
    if verdict == "VALIDATED":
        lines.append("  All four predictions held on this regime.")
        lines.append("  Chamber ratios act like a tape measure of the integer size")
        lines.append("  of the gap (half the log of the midpoint).")
        lines.append("  The global prime ratio R(s) is a different object: for each")
        lines.append("  fixed s it is essentially a constant, not a local gap probe.")
        lines.append("  The distance between them grows as primes get larger.")
        lines.append("  Raising the partial-sum length N does not close that gap.")
        lines.append("")
        lines.append("  Design consequence supported by data:")
        lines.append("  do not use |rho_chamber - R| as a spectral alignment score")
        lines.append("  or as an RH intermediate. Use continuation-native kernels.")
    else:
        lines.append("  At least one prediction FAILED on this regime.")
        lines.append("  The core insight is FALSIFIED as stated (or thresholds need")
        lines.append("  revision). Inspect the FAIL rows above.")
    lines.append("")
    lines.append("STATUS LABELS")
    lines.append(f"  verdict:           {verdict}")
    lines.append("  claim status:      measured support only (not a theorem)")
    lines.append("  RH:                not addressed; no pole-placement claim")
    lines.append("")
    lines.append("=" * 72)
    lines.append(f"FINAL VERDICT: {verdict}")
    lines.append("=" * 72)
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = run()
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    report = format_report(payload)
    print(report)
    print(f"\nJSON artifact: {OUT_JSON.relative_to(REPO_ROOT)}")
    return 0 if payload["verdict"]["all_predictions_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
