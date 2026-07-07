#!/usr/bin/env python3
"""Demonstrate that prime order is fixed at the integer layer before zeta.

Companion to WHITEPAPER.md in this folder.

The script is self-contained except for mpmath, which the repository already
depends on for exact zeta evaluation.

Outputs:
  - stdout tables for two hand-checkable gaps
  - output/demo_results.json
  - infographic.svg (refreshed with measured values)
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from mpmath import mp
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "mpmath is required. Install with: pip install mpmath"
    ) from exc


OUTPUT_DIR = Path(__file__).resolve().parent / "output"
INFOGRAPHIC_PATH = Path(__file__).resolve().parent / "infographic.svg"

BRIDGE_SCALE = math.e**2 / 2.0

EXAMPLE_GAPS = (
    (23, 29),
    (89, 97),
)

BRIDGE_S = 2.5
BRIDGE_TERMS = 5000
BRIDGE_DPS = 50


@dataclass(frozen=True)
class GapRow:
    n: int
    divisor_count: int
    excess: float
    is_prime: bool
    is_gwr_witness: bool


@dataclass(frozen=True)
class GapReport:
    p: int
    q: int
    rows: list[GapRow]
    gwr_witness: int | None
    interior_min_divisor_count: int | None


@dataclass(frozen=True)
class BridgeReport:
    s: float
    terms: int
    divisor_partial_sum: complex
    zeta_squared: complex
    divisor_abs_error: float
    load_partial_sum: complex
    normalized_ratio: complex
    zeta_log_derivative: complex
    ratio_abs_error: float


def divisor_counts_up_to(limit: int) -> list[int]:
    """Return exact divisor counts tau(n) for 0 <= n <= limit."""
    counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            counts[n] += 1
    return counts


def zero_excess(n: int, divisor_count: int) -> float:
    """Return (tau(n)/2 - 1) * log(n); primes at n>1 land at 0."""
    if n <= 1:
        return 0.0
    return (divisor_count / 2.0 - 1.0) * math.log(n)


def analyze_gap(p: int, q: int, counts: list[int]) -> GapReport:
    """Build the ordered interior table for consecutive primes (p, q)."""
    interior = list(range(p + 1, q))
    min_tau = min(counts[n] for n in interior) if interior else None
    gwr = None
    if interior:
        gwr = min(n for n in interior if counts[n] == min_tau)

    rows: list[GapRow] = []
    for n in range(p, q + 1):
        tau_n = counts[n]
        rows.append(
            GapRow(
                n=n,
                divisor_count=tau_n,
                excess=zero_excess(n, tau_n),
                is_prime=tau_n == 2,
                is_gwr_witness=gwr is not None and n == gwr,
            )
        )
    return GapReport(
        p=p,
        q=q,
        rows=rows,
        gwr_witness=gwr,
        interior_min_divisor_count=min_tau,
    )


def normalization_load(n: int, divisor_count: int) -> float:
    """Scaled load coefficient H(n)/e^2 used in the bridge partial sums."""
    if n <= 1:
        return 0.0
    return divisor_count * math.log(n) / (math.e**2)


def evaluate_bridge(s: float, terms: int, dps: int) -> BridgeReport:
    """Compare divisor-count partial sums to zeta at Re(s) > 1."""
    counts = divisor_counts_up_to(terms)

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

        return BridgeReport(
            s=s,
            terms=terms,
            divisor_partial_sum=complex(divisor_sum),
            zeta_squared=complex(zeta_sq),
            divisor_abs_error=float(abs(divisor_sum - zeta_sq)),
            load_partial_sum=complex(load_sum),
            normalized_ratio=complex(normalized_ratio),
            zeta_log_derivative=complex(zeta_log_deriv),
            ratio_abs_error=float(abs(normalized_ratio - zeta_log_deriv)),
        )


def print_gap_report(report: GapReport) -> None:
    """Print one gap table for terminal inspection."""
    print(f"\nGap from {report.p} to {report.q}")
    print("-" * 64)
    print(f"{'n':>4}  {'divisors':>8}  {'excess':>10}  role")
    for row in report.rows:
        role = ""
        if row.n == report.p:
            role = "start prime"
        elif row.n == report.q:
            role = "next prime (count returns to 2)"
        elif row.is_gwr_witness:
            role = "selected witness (smallest interior count)"
        print(
            f"{row.n:4d}  {row.divisor_count:8d}  {row.excess:10.4f}  {role}"
        )
    if report.gwr_witness is not None:
        print(
            f"Interior minimum divisor count: {report.interior_min_divisor_count}"
        )
        print(f"Selected witness: {report.gwr_witness}")


def write_infographic(
    gap_reports: list[GapReport],
    bridge: BridgeReport,
    path: Path,
) -> None:
    """Write a single-page SVG summary of the integer-to-zeta chain."""
    first = gap_reports[0]
    witness = first.gwr_witness or 25
    divisor_err = f"{bridge.divisor_abs_error:.2e}"
    ratio_err = f"{bridge.ratio_abs_error:.2e}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1560" viewBox="0 0 1200 1560">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#eef2ff"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="#4338ca"/>
    </marker>
    <filter id="shadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="1200" height="1560" fill="url(#bg)"/>
  <rect x="36" y="32" width="1128" height="1496" rx="24" fill="#ffffff" filter="url(#shadow)"/>

  <text x="72" y="88" font-family="Georgia, serif" font-size="36" fill="#0f172a" font-weight="700">Prime Order Is Fixed Before Zeta</text>
  <text x="72" y="124" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#475569">Prime Gap Structure whitepaper | integer source → exact compression → RH language</text>
  <rect x="72" y="140" width="1056" height="4" fill="#4f46e5" rx="2"/>

  <rect x="72" y="168" width="1056" height="88" rx="14" fill="#eef2ff" stroke="#6366f1" stroke-width="1.5"/>
  <text x="96" y="204" font-family="Helvetica, Arial, sans-serif" font-size="20" fill="#312e81" font-weight="700">Core claim</text>
  <text x="96" y="234" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#3730a3">Prime placement is decided by exact divisor structure inside each gap. Zeta is the compressed record of that same arithmetic.</text>

  <text x="72" y="300" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#0f172a" font-weight="700">Layer 1 — Integers (the source)</text>
  <rect x="72" y="316" width="1056" height="300" rx="16" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5"/>
  <text x="96" y="352" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#166534" font-weight="700">Example gap: 23 → 29</text>
  <text x="96" y="380" font-family="monospace" font-size="15" fill="#14532d">23 | 24  25  26  27  28 | 29</text>
  <text x="96" y="408" font-family="monospace" font-size="15" fill="#14532d">τ  |  8   3   4   4   6  |  2</text>
  <rect x="96" y="424" width="56" height="28" rx="6" fill="#86efac" stroke="#16a34a"/>
  <text x="108" y="444" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#14532d">25</text>
  <text x="168" y="444" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#166534">first smallest interior divisor count (3)</text>
  <text x="96" y="484" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#14532d">• Interior composites carry ordered divisor counts</text>
  <text x="96" y="512" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#14532d">• Next prime = first later integer with count 2</text>
  <text x="96" y="540" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#14532d">• Selected witness at n={witness} (hand-checkable, no zeta)</text>
  <text x="96" y="580" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#15803d" font-weight="700">Status: proved local placement theorems (PROOF.md)</text>

  <line x1="600" y1="628" x2="600" y2="668" stroke="#4338ca" stroke-width="3" marker-end="url(#arrow)"/>

  <text x="72" y="708" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#0f172a" font-weight="700">Layer 2 — Exact compression</text>
  <rect x="72" y="724" width="1056" height="280" rx="16" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="96" y="760" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#1d4ed8" font-weight="700">Same divisor counts, packaged as series</text>
  <text x="96" y="792" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#1e3a8a">Σ τ(n) / n^s  =  ζ(s)²</text>
  <text x="96" y="824" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#1e3a8a">load ratio from counts  =  −ζ'(s) / ζ(s)</text>
  <text x="96" y="864" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#1e40af">Measured at s = {bridge.s}, N = {bridge.terms:,} terms:</text>
  <text x="96" y="896" font-family="monospace" font-size="14" fill="#1e3a8a">|divisor sum − ζ²| = {divisor_err}</text>
  <text x="96" y="924" font-family="monospace" font-size="14" fill="#1e3a8a">|ratio − (−ζ'/ζ)| = {ratio_err}</text>
  <text x="96" y="968" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#1d4ed8" font-weight="700">Status: exact identity (not an approximation)</text>

  <line x1="600" y1="1016" x2="600" y2="1056" stroke="#4338ca" stroke-width="3" marker-end="url(#arrow)"/>

  <text x="72" y="1096" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#0f172a" font-weight="700">Layer 3 — RH language (downstream)</text>
  <rect x="72" y="1112" width="1056" height="220" rx="16" fill="#faf5ff" stroke="#a855f7" stroke-width="1.5"/>
  <text x="96" y="1148" font-family="Helvetica, Arial, sans-serif" font-size="17" fill="#6b21a8" font-weight="700">Critical line = spectral coordinate sentence</text>
  <text x="96" y="1180" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#581c87">Zeros of ζ(s) describe correction terms in prime counting.</text>
  <text x="96" y="1208" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#581c87">RH asks whether every nontrivial zero has real part ½.</text>
  <text x="96" y="1236" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#581c87">PGS explains the order: integer structure → exact bridge → pole placement.</text>
  <text x="96" y="1280" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#7e22ce" font-weight="700">Open: final source-to-spectral proof closure in classical form</text>

  <rect x="72" y="1360" width="520" height="140" rx="14" fill="#fff7ed" stroke="#fb923c" stroke-width="1.5"/>
  <text x="96" y="1396" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#9a3412" font-weight="700">Trillions of zero checks</text>
  <text x="96" y="1424" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#7c2d12">Confirm the pattern.</text>
  <text x="96" y="1450" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#7c2d12">Do not name the integer mechanism.</text>

  <rect x="608" y="1360" width="520" height="140" rx="14" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
  <text x="632" y="1396" font-family="Helvetica, Arial, sans-serif" font-size="16" fill="#065f46" font-weight="700">PGS integer read</text>
  <text x="632" y="1424" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#047857">Names the mechanism before zeta.</text>
  <text x="632" y="1450" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#047857">Explains why the spectral pattern is orderly.</text>

  <text x="72" y="1536" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#64748b">Run: python3 integer_order_demo.py  |  Repo: github.com/zfifteen/prime-gap-structure</text>
</svg>
"""
    path.write_text(svg, encoding="utf-8")


def complex_pair(value: complex) -> dict[str, float]:
    return {"real": value.real, "imag": value.imag}


def main() -> int:
    max_prime = max(q for _, q in EXAMPLE_GAPS)
    counts = divisor_counts_up_to(max_prime)

    gap_reports = [analyze_gap(p, q, counts) for p, q in EXAMPLE_GAPS]

    print("=" * 64)
    print("Prime order at the integer layer (before zeta)")
    print("=" * 64)
    for report in gap_reports:
        print_gap_report(report)

    print("\n" + "=" * 64)
    print(f"Exact zeta compression at s = {BRIDGE_S}, terms = {BRIDGE_TERMS}")
    print("=" * 64)
    bridge = evaluate_bridge(BRIDGE_S, BRIDGE_TERMS, BRIDGE_DPS)
    print(f"divisor partial sum     = {bridge.divisor_partial_sum}")
    print(f"ζ(s)²                   = {bridge.zeta_squared}")
    print(f"|error|                 = {bridge.divisor_abs_error:.6e}")
    print()
    print(f"normalized load ratio   = {bridge.normalized_ratio}")
    print(f"-ζ'(s)/ζ(s)             = {bridge.zeta_log_derivative}")
    print(f"|error|                 = {bridge.ratio_abs_error:.6e}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "whitepaper": "integer-order-before-zeta",
        "gap_examples": [
            {
                "p": r.p,
                "q": r.q,
                "gwr_witness": r.gwr_witness,
                "interior_min_divisor_count": r.interior_min_divisor_count,
                "rows": [asdict(row) for row in r.rows],
            }
            for r in gap_reports
        ],
        "bridge": {
            "s": bridge.s,
            "terms": bridge.terms,
            "divisor_partial_sum": complex_pair(bridge.divisor_partial_sum),
            "zeta_squared": complex_pair(bridge.zeta_squared),
            "divisor_abs_error": bridge.divisor_abs_error,
            "load_partial_sum": complex_pair(bridge.load_partial_sum),
            "normalized_ratio": complex_pair(bridge.normalized_ratio),
            "zeta_log_derivative": complex_pair(bridge.zeta_log_derivative),
            "ratio_abs_error": bridge.ratio_abs_error,
        },
        "bridge_scale": BRIDGE_SCALE,
        "interpretation": {
            "source_layer": "divisor counts inside consecutive prime gaps",
            "compression": "divisor series equals zeta(s)^2; load ratio equals -zeta'(s)/zeta(s)",
            "downstream": "RH is pole-placement language after exact compression",
        },
    }
    results_path = OUTPUT_DIR / "demo_results.json"
    results_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    write_infographic(gap_reports, bridge, INFOGRAPHIC_PATH)

    print(f"\nWrote {results_path}")
    print(f"Wrote {INFOGRAPHIC_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())