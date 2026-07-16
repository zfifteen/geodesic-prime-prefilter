#!/usr/bin/env python3
"""D1 bounded-gap interior atlas harness (execution collab).

Status: measured harness for named regimes only. Not verified.
PGS-first: interior via gwr_next_gap_profile (divisor field).
Prime catalog via sieve is INPUT ONLY.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from math import ceil, log
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src" / "python"))

from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile  # noqa: E402


def primes_upto(n: int) -> list[int]:
    """Input catalog only (not PGS inference)."""
    if n < 2:
        return []
    s = bytearray(b"\x01") * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            start = i * i
            s[start : n + 1 : i] = b"\x00" * (((n - start) // i) + 1)
    return [i for i in range(2, n + 1) if s[i]]


def compression_bound(q: int) -> float:
    return max(64.0, float(ceil(0.5 * (log(q) ** 2))))


def is_perfect_square(n: int) -> bool:
    if n < 1:
        return False
    r = int(n**0.5)
    return r * r == n


def h_tags(gap: int) -> str:
    tags = [f"H{h}" for h in (246, 600, 1000) if gap <= h]
    return "|".join(tags)


def decade_bin(p: int) -> int:
    return 1 if p < 10 else int(log(p, 10))


def profile_row(p: int, q: int, gap: int, cohort: str, regime: str) -> dict:
    try:
        prof = gwr_next_gap_profile(p)
        next_p = prof["next_prime"]
        w_off = prof["winner_offset"]
        w_d = prof["winner_d"]
        if next_p != q:
            return {
                "p": p, "q": q, "gap": gap, "w": None, "d_w": None,
                "offset": None, "compression": None,
                "compression_bound": compression_bound(q),
                "square_flag": False, "h_filters": h_tags(gap),
                "cohort": cohort, "regime": regime, "status": "unresolved",
                "notes": f"profile_next={next_p}_catalog_q={q}",
            }
        if w_off is None:
            return {
                "p": p, "q": q, "gap": gap, "w": None, "d_w": None,
                "offset": None, "compression": None,
                "compression_bound": compression_bound(q),
                "square_flag": False, "h_filters": h_tags(gap),
                "cohort": cohort, "regime": regime, "status": "resolved",
                "notes": "empty_interior",
            }
        offset = int(w_off)
        w = p + offset
        bound = compression_bound(q)
        return {
            "p": p, "q": q, "gap": gap, "w": w,
            "d_w": int(w_d) if w_d is not None else None,
            "offset": offset,
            "compression": float(offset) / bound if bound else None,
            "compression_bound": bound,
            "square_flag": is_perfect_square(w),
            "h_filters": h_tags(gap),
            "cohort": cohort, "regime": regime, "status": "resolved",
            "notes": "",
        }
    except Exception as e:
        return {
            "p": p, "q": q, "gap": gap, "w": None, "d_w": None,
            "offset": None, "compression": None,
            "compression_bound": compression_bound(q),
            "square_flag": False, "h_filters": h_tags(gap),
            "cohort": cohort, "regime": regime, "status": "unresolved",
            "notes": f"error:{type(e).__name__}",
        }


def run_regime(p_max: int, regime: str, control_mode: str = "quartile") -> list[dict]:
    """control_mode: 'h1000' (legacy, often empty at low p) or 'quartile' (recommended)."""
    primes = primes_upto(p_max + 5000)
    pairs = []
    for i in range(len(primes) - 1):
        p, q = primes[i], primes[i + 1]
        if p > p_max:
            break
        pairs.append((p, q, q - p))

    rows: list[dict] = []
    if control_mode == "h1000":
        for p, q, gap in pairs:
            cohort = "bounded" if gap <= 1000 else "control"
            if cohort == "control":
                continue  # sample controls later
            rows.append(profile_row(p, q, gap, cohort, regime))
        # (legacy control sampling omitted; use quartile)
        return rows

    # Profile all pairs once, then tag quartile cohorts by log-bin
    raw = [profile_row(p, q, gap, "all", regime) for p, q, gap in pairs]
    by_bin: dict[int, list] = {}
    for r in raw:
        by_bin.setdefault(decade_bin(r["p"]), []).append(r)
    out = []
    for items in by_bin.values():
        gaps = sorted(x["gap"] for x in items)
        if not gaps:
            continue
        p25 = gaps[int(round((len(gaps) - 1) * 0.25))]
        p75 = gaps[int(round((len(gaps) - 1) * 0.75))]
        for r in items:
            rr = dict(r)
            g = r["gap"]
            if g <= p25:
                rr["cohort"] = "small_gap"
            elif g >= p75:
                rr["cohort"] = "large_gap"
            else:
                rr["cohort"] = "mid_gap"
            rr["gap_p25"] = p25
            rr["gap_p75"] = p75
            out.append(rr)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="D1 interior atlas harness")
    ap.add_argument("--p-max", type=int, default=1_000_000)
    ap.add_argument("--regime", type=str, default="")
    ap.add_argument("--control-mode", choices=("quartile", "h1000"), default="quartile")
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    regime = args.regime or f"R_p_le_{args.p_max}"
    t0 = time.time()
    rows = run_regime(args.p_max, regime, control_mode=args.control_mode)
    elapsed = time.time() - t0
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"rows_{regime}.jsonl"
    with out.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    summary = {
        "regime": regime,
        "p_max": args.p_max,
        "control_mode": args.control_mode,
        "elapsed_s": elapsed,
        "n_rows": len(rows),
        "resolved": sum(1 for r in rows if r["status"] == "resolved"),
        "max_gap": max((r["gap"] for r in rows), default=None),
        "status_language": "measured_on_regime_only",
        "not_verified": True,
        "rows_path": str(out),
    }
    (args.out_dir / f"summary_{regime}.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
