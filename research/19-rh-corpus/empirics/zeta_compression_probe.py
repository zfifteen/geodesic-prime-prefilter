#!/usr/bin/env python3
"""Multi-s partial-sum probe for Layer 3 zeta compression identities.

Validates D(s)=ζ(s)² and R(s)=-ζ'(s)/ζ(s) at several Re(s)>1 points.
Output: empirics/output/compression_probe_results.json

Companion to by-layer/03-zeta-compression.md and RH-105.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from mpmath import mp
except ImportError as exc:  # pragma: no cover
    raise SystemExit("mpmath required: pip install mpmath") from exc


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

S_VALUES = (1.5, 2.0, 2.5, 3.0, 4.0)
TERMS = 10_000
DPS = 60
BRIDGE_SCALE = math.e**2 / 2.0


@dataclass(frozen=True)
class ProbePoint:
    s: float
    terms: int
    divisor_abs_error: float
    ratio_abs_error: float
    divisor_partial_real: float
    zeta_squared_real: float
    ratio_partial_real: float
    zeta_log_deriv_real: float


def divisor_counts_up_to(limit: int) -> list[int]:
    counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            counts[n] += 1
    return counts


def normalization_load(n: int, tau: int) -> float:
    if n <= 1:
        return 0.0
    return tau * math.log(n) / (math.e**2)


def probe_at(s: float, terms: int, counts: list[int], dps: int) -> ProbePoint:
    with mp.workdps(dps):
        s_mp = mp.mpc(s)
        divisor_sum = mp.mpc(0)
        load_sum = mp.mpc(0)
        for n in range(1, terms + 1):
            term = mp.power(n, -s_mp)
            divisor_sum += counts[n] * term
            load_sum += normalization_load(n, counts[n]) * term

        zeta_val = mp.zeta(s_mp)
        zeta_sq = zeta_val**2
        zeta_log_deriv = -mp.diff(mp.zeta, s_mp) / zeta_val
        normalized_ratio = BRIDGE_SCALE * load_sum / divisor_sum

        return ProbePoint(
            s=s,
            terms=terms,
            divisor_abs_error=float(abs(divisor_sum - zeta_sq)),
            ratio_abs_error=float(abs(normalized_ratio - zeta_log_deriv)),
            divisor_partial_real=float(divisor_sum.real),
            zeta_squared_real=float(zeta_sq.real),
            ratio_partial_real=float(normalized_ratio.real),
            zeta_log_deriv_real=float(zeta_log_deriv.real),
        )


def main() -> int:
    counts = divisor_counts_up_to(TERMS)
    points = [probe_at(s, TERMS, counts, DPS) for s in S_VALUES]

    payload = {
        "probe": "zeta_compression_multi_s",
        "layer": "L3",
        "finding_id": "RH-105",
        "terms": TERMS,
        "dps": DPS,
        "bridge_scale": BRIDGE_SCALE,
        "points": [asdict(p) for p in points],
        "max_divisor_abs_error": max(p.divisor_abs_error for p in points),
        "max_ratio_abs_error": max(p.ratio_abs_error for p in points),
        "interpretation": {
            "D_identity": "sum tau(n)/n^s = zeta(s)^2",
            "R_identity": "(e^2/2)*K(s)/D(s) = -zeta'(s)/zeta(s)",
            "status": "measured partial-sum convergence; not a proof of continuation",
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "compression_probe_results.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Layer 3 compression probe (N={TERMS})")
    print("-" * 72)
    for p in points:
        print(
            f"s={p.s:4.1f}  |D-ζ²|={p.divisor_abs_error:.3e}  "
            f"|R+ζ'/ζ|={p.ratio_abs_error:.3e}"
        )
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())