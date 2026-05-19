#!/usr/bin/env python3
"""Private 256-bit audit for the frozen ratio web formula."""

from __future__ import annotations

import json
import time
from pathlib import Path

from audit_anchor_band_128bit import (
    BAND_WIDTH_RATIO,
    CAP_RATIO,
    exact_band_rank,
    public_band_width,
    public_cap,
    public_radius,
    public_thread_counts,
)

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_anchor_band_256bit"

CASE = {
    "name": "scale_256bit_340282366920937228895484483974979199073x340282366920928586920163619777447112591",
    "p": 340282366920937228895484483974979199073,
    "q": 340282366920928586920163619777447112591,
}


def main() -> None:
    started = time.perf_counter()
    p_value = CASE["p"]
    q_value = CASE["q"]
    n_value = p_value * q_value
    radius = public_radius(n_value)
    band_width = public_band_width(radius)
    cap = public_cap(band_width)
    counts = public_thread_counts(n_value, radius)
    p_rank = exact_band_rank(n_value, p_value, radius, band_width, counts)
    q_rank = exact_band_rank(n_value, q_value, radius, band_width, counts)
    hits = []
    if p_rank["band_rank"] <= cap:
        hits.append({"which": "p", **p_rank})
    if q_rank["band_rank"] <= cap:
        hits.append({"which": "q", **q_rank})
    summary = {
        "status": "success" if hits else "failure",
        "case": CASE["name"],
        "N": n_value,
        "N_bits": n_value.bit_length(),
        "radius": radius,
        "band_width_ratio": f"{BAND_WIDTH_RATIO.numerator}/{BAND_WIDTH_RATIO.denominator}",
        "band_width": band_width,
        "cap_ratio": f"{CAP_RATIO.numerator}/{CAP_RATIO.denominator}",
        "top_per_band": cap,
        "thread_counts": counts,
        "p": p_value,
        "q": q_value,
        "p_rank": p_rank,
        "q_rank": q_rank,
        "hits": hits,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Anchor-Confirmed 256-Bit Ratio Audit",
        "",
        f"Status: `{summary['status']}`",
        "",
        f"- case: `{summary['case']}`",
        f"- bits: `{summary['N_bits']}`",
        f"- radius: `{summary['radius']}`",
        f"- band width ratio: `{summary['band_width_ratio']}`",
        f"- cap ratio: `{summary['cap_ratio']}`",
        f"- top per band: `{summary['top_per_band']}`",
        f"- p band rank: `{summary['p_rank']['band_rank']}`",
        f"- q band rank: `{summary['q_rank']['band_rank']}`",
        f"- elapsed seconds: `{summary['elapsed_seconds']}`",
        "",
        "## Hit",
        "",
    ]
    for hit in hits:
        lines.append(f"- `{hit['which']}={hit['distance']}` at band rank `{hit['band_rank']}`")
    if not hits:
        lines.append("- none")
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
