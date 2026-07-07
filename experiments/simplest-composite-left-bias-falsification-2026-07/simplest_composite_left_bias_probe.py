#!/usr/bin/env python3
"""Falsification probe: left-bias placement of high-complexity simplest composites.

PGS objects (AGENTS.md entry frame):
  - ordered prime-gap state (p, q) with interior I = {p+1, ..., q-1}
  - divisor-count field tau(n)
  - GWR witness w = leftmost interior argmin tau(n)  [simplest composite]
  - prefix distance offset = w - p
  - dynamic cutoff C(q) = max(64, ceil(0.5 * log(q)^2))

Hypothesis under test:
  High-complexity gap minima (large tau(w)) sit much closer to the earlier prime
  than low-complexity minima (small tau(w)). Two visibly different offset clouds
  should appear: a spreading low-tau cloud and a tight left-edge high-tau cloud.

Falsification targets:
  F1  Cloud separation: median offset for high-tau bucket < median offset for tau=4.
  F2  Monotonic tightening: p90(offset) is non-increasing across tau buckets >= 4.
  F3  Prefix cleanliness: if offset > 1, every interior n < w must have tau(n) > tau(w).
  F4  Deep high-tau counterexamples: tau(w) >= 12 with offset >= 6 (tau=4 p90).
  F5  Scale decoupling: high-tau offsets stay at 1 while tau=4 p90 grows in log(p) bins.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
if str(FIELD_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_DIR))

from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile  # noqa: E402


def dynamic_cutoff(q: int) -> int:
    return max(64, math.ceil(0.5 * math.log(q) ** 2))


def divisor_counts(limit: int) -> list[int]:
    tau = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for n in range(d, limit + 1, d):
            tau[n] += 1
    return tau


def percentile(values: list[int], p: float) -> float:
    if not values:
        return float("nan")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(math.ceil(p * len(ordered)) - 1)))
    return float(ordered[index])


@dataclass(frozen=True)
class GapRecord:
    p: int
    q: int
    gap_size: int
    w: int
    offset: int
    tau_w: int
    min_tau: int
    cutoff: int
    utilization: float
    prefix_clean: bool
    easier_in_prefix: int


def analyze_gap(p: int, q: int, tau: list[int]) -> GapRecord | None:
    if q - p <= 1:
        return None

    min_tau = min(tau[n] for n in range(p + 1, q))
    w = p + 1
    for n in range(p + 1, q):
        if tau[n] == min_tau:
            w = n
            break

    offset = w - p
    easier_in_prefix = sum(1 for n in range(p + 1, w) if tau[n] < tau[w])
    prefix_clean = easier_in_prefix == 0

    cutoff = dynamic_cutoff(q)
    return GapRecord(
        p=p,
        q=q,
        gap_size=q - p,
        w=w,
        offset=offset,
        tau_w=tau[w],
        min_tau=min_tau,
        cutoff=cutoff,
        utilization=offset / cutoff,
        prefix_clean=prefix_clean,
        easier_in_prefix=easier_in_prefix,
    )


def scan_gaps(limit: int) -> list[GapRecord]:
    tau = divisor_counts(limit)
    primes = [n for n in range(2, limit + 1) if tau[n] == 2]
    records: list[GapRecord] = []
    for p, q in zip(primes, primes[1:]):
        row = analyze_gap(p, q, tau)
        if row is not None:
            records.append(row)
    return records


def bucket_offsets(records: list[GapRecord], predicate) -> list[int]:
    return [r.offset for r in records if predicate(r)]


def summarize(records: list[GapRecord]) -> dict[str, object]:
    tau4_offsets = bucket_offsets(records, lambda r: r.tau_w == 4)
    high_offsets = bucket_offsets(records, lambda r: r.tau_w >= 12)
    very_high_offsets = bucket_offsets(records, lambda r: r.tau_w >= 24)

    tau4_p90 = percentile(tau4_offsets, 0.90)
    deep_high = [
        r for r in records
        if r.tau_w >= 12 and r.offset >= int(tau4_p90)
    ]

    prefix_violations = [r for r in records if not r.prefix_clean]

    bucket_defs = [
        ("tau_4", lambda r: r.tau_w == 4),
        ("tau_6_7", lambda r: 6 <= r.tau_w <= 7),
        ("tau_8_11", lambda r: 8 <= r.tau_w <= 11),
        ("tau_12_23", lambda r: 12 <= r.tau_w <= 23),
        ("tau_ge_24", lambda r: r.tau_w >= 24),
    ]
    bucket_stats: dict[str, dict[str, float | int]] = {}
    p90_series: list[float] = []
    for name, pred in bucket_defs:
        offs = bucket_offsets(records, pred)
        if not offs:
            continue
        stats = {
            "count": len(offs),
            "min": min(offs),
            "median": float(median(offs)),
            "p90": percentile(offs, 0.90),
            "max": max(offs),
            "mean": sum(offs) / len(offs),
        }
        bucket_stats[name] = stats
        p90_series.append(stats["p90"])

    monotonic_p90 = all(
        p90_series[i] >= p90_series[i + 1]
        for i in range(len(p90_series) - 1)
    )

    log_bins: dict[str, dict[str, float | int]] = {}
    for lo_exp in range(1, 7):
        hi_exp = lo_exp + 1
        lo = 10**lo_exp
        hi = 10**hi_exp
        bin_records = [r for r in records if lo <= r.p < hi]
        if not bin_records:
            continue
        low_offs = [r.offset for r in bin_records if r.tau_w == 4]
        high_offs_bin = [r.offset for r in bin_records if r.tau_w >= 16]
        log_bins[f"10^{lo_exp}..10^{hi_exp}"] = {
            "gaps": len(bin_records),
            "tau4_p90": percentile(low_offs, 0.90),
            "tau4_max": max(low_offs) if low_offs else 0,
            "tau_ge16_median": float(median(high_offs_bin)) if high_offs_bin else float("nan"),
            "tau_ge16_max": max(high_offs_bin) if high_offs_bin else 0,
        }

    f1_falsified = (
        not tau4_offsets
        or not high_offsets
        or median(high_offsets) >= median(tau4_offsets)
    )
    f2_falsified = not monotonic_p90
    f3_falsified = bool(prefix_violations)
    f4_falsified = bool(deep_high)
    f5_falsified = any(
        isinstance(v.get("tau4_p90"), float)
        and isinstance(v.get("tau_ge16_median"), float)
        and not math.isnan(v["tau_ge16_median"])  # type: ignore[arg-type]
        and v["tau_ge16_median"] >= v["tau4_p90"]  # type: ignore[operator]
        for v in log_bins.values()
    )

    overall_falsified = f1_falsified or f3_falsified or f4_falsified

    return {
        "regime": {
            "prime_limit": records[-1].q if records else None,
            "gaps_with_interior": len(records),
        },
        "tau4_reference": {
            "count": len(tau4_offsets),
            "median_offset": float(median(tau4_offsets)) if tau4_offsets else None,
            "p90_offset": tau4_p90,
            "max_offset": max(tau4_offsets) if tau4_offsets else None,
            "mean_offset": sum(tau4_offsets) / len(tau4_offsets) if tau4_offsets else None,
        },
        "high_tau_reference": {
            "tau_ge_12_count": len(high_offsets),
            "tau_ge_12_median_offset": float(median(high_offsets)) if high_offsets else None,
            "tau_ge_12_p90_offset": percentile(high_offsets, 0.90),
            "tau_ge_12_max_offset": max(high_offsets) if high_offsets else None,
            "tau_ge_24_count": len(very_high_offsets),
            "tau_ge_24_max_offset": max(very_high_offsets) if very_high_offsets else None,
        },
        "bucket_stats": bucket_stats,
        "log_p_bins": log_bins,
        "f1_cloud_separation": {
            "criterion": "median(offset | tau>=12) < median(offset | tau=4)",
            "tau4_median": float(median(tau4_offsets)) if tau4_offsets else None,
            "tau_ge12_median": float(median(high_offsets)) if high_offsets else None,
            "falsified": f1_falsified,
        },
        "f2_monotonic_p90": {
            "criterion": "p90(offset) non-increasing across tau buckets tau_4..tau_ge_24",
            "p90_series": p90_series,
            "falsified": f2_falsified,
        },
        "f3_prefix_cleanliness": {
            "criterion": "no interior n<w with tau(n) < tau(w)",
            "violations": len(prefix_violations),
            "falsified": f3_falsified,
            "counterexamples": [
                {
                    "p": r.p,
                    "q": r.q,
                    "w": r.w,
                    "offset": r.offset,
                    "tau_w": r.tau_w,
                    "easier_in_prefix": r.easier_in_prefix,
                }
                for r in prefix_violations[:10]
            ],
        },
        "f4_deep_high_tau": {
            "criterion": f"no tau>=12 gap with offset >= tau=4 p90 ({int(tau4_p90)})",
            "tau4_p90_threshold": int(tau4_p90),
            "counterexample_count": len(deep_high),
            "falsified": f4_falsified,
            "counterexamples": [
                {
                    "p": r.p,
                    "q": r.q,
                    "w": r.w,
                    "offset": r.offset,
                    "tau_w": r.tau_w,
                }
                for r in deep_high[:15]
            ],
        },
        "f5_scale_decoupling": {
            "criterion": "in each log(p) bin, tau>=16 median offset stays below tau=4 p90",
            "falsified": f5_falsified,
            "bins": log_bins,
        },
        "verdict": {
            "hypothesis_falsified": overall_falsified,
            "supporting_checks_passed": not overall_falsified,
            "sharpened_notes": (
                "Square-branch tau=3 gaps excluded from high/low comparison; "
                "they are low-divisor but can offset far."
            ),
        },
    }


def write_csv(path: Path, records: list[GapRecord]) -> None:
    fields = [
        "p", "q", "gap_size", "w", "offset", "tau_w", "min_tau",
        "cutoff", "utilization", "prefix_clean", "easier_in_prefix",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            writer.writerow({
                "p": row.p,
                "q": row.q,
                "gap_size": row.gap_size,
                "w": row.w,
                "offset": row.offset,
                "tau_w": row.tau_w,
                "min_tau": row.min_tau,
                "cutoff": row.cutoff,
                "utilization": row.utilization,
                "prefix_clean": row.prefix_clean,
                "easier_in_prefix": row.easier_in_prefix,
            })


def write_scatter_svg(path: Path, records: list[GapRecord]) -> None:
    """Minimal SVG scatter: log10(p) vs offset, colored by tau bucket."""
    if not records:
        path.write_text("<svg xmlns='http://www.w3.org/2000/svg'/>")
        return

    width, height = 960, 520
    margin = 60
    points = []
    for r in records:
        if r.tau_w == 3:
            continue
        x = math.log10(r.p)
        y = r.offset
        if r.tau_w == 4:
            color = "#1f77b4"
        elif r.tau_w <= 11:
            color = "#ff7f0e"
        else:
            color = "#d62728"
        points.append((x, y, color))

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = 1, max(ys)

    def sx(x: float) -> float:
        return margin + (x - x_min) / (x_max - x_min) * (width - 2 * margin)

    def sy(y: float) -> float:
        return height - margin - (y - y_min) / (y_max - y_min) * (height - 2 * margin)

    circles = "\n".join(
        f"<circle cx='{sx(x):.2f}' cy='{sy(y):.2f}' r='1.6' fill='{color}' fill-opacity='0.35'/>"
        for x, y, color in points
    )
    svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>
  <rect x='0' y='0' width='{width}' height='{height}' fill='white'/>
  <text x='{width/2:.0f}' y='24' text-anchor='middle' font-size='14'>Simplest-composite offset vs log10(p)</text>
  <text x='{width/2:.0f}' y='{height-12}' text-anchor='middle' font-size='12'>log10(earlier prime p)</text>
  <text x='16' y='{height/2:.0f}' transform='rotate(-90 16 {height/2:.0f})' text-anchor='middle' font-size='12'>offset w-p</text>
  {circles}
  <text x='{margin}' y='{margin-8}' font-size='11' fill='#1f77b4'>tau=4</text>
  <text x='{margin+50}' y='{margin-8}' font-size='11' fill='#ff7f0e'>tau 6-11</text>
  <text x='{margin+120}' y='{margin-8}' font-size='11' fill='#d62728'>tau>=12</text>
</svg>
"""
    path.write_text(svg)


def cross_check_profile(records: list[GapRecord], sample: int = 200) -> dict[str, object]:
    mismatches: list[dict[str, int]] = []
    checked = 0
    step = max(1, len(records) // sample)
    for row in records[::step]:
        profile = gwr_next_gap_profile(row.p)
        if profile["next_prime"] != row.q:
            mismatches.append({"p": row.p, "expected_q": row.q, "profile_q": profile["next_prime"]})
        if profile["winner_offset"] is not None and profile["winner_offset"] != row.offset:
            mismatches.append({
                "p": row.p,
                "expected_offset": row.offset,
                "profile_offset": profile["winner_offset"],
            })
        checked += 1
    return {"checked": checked, "mismatches": mismatches, "ok": not mismatches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=2_000_000)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/simplest-composite-left-bias-falsification-2026-07"),
    )
    args = parser.parse_args()

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    records = scan_gaps(args.limit)
    summary = summarize(records)
    summary["cross_check"] = cross_check_profile(records)

    write_csv(out_dir / "gap_simplest_composite_rows.csv", records)
    write_scatter_svg(out_dir / "offset_clouds.svg", records)
    (out_dir / "falsification_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()