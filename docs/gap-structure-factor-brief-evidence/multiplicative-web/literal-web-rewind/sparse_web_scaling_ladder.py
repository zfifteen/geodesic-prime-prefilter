#!/usr/bin/env python3
"""Scale the frozen presence-only three-thread web by changing only N and radius."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

from literal_web_hole_trace import CASES, write_jsonl
from literal_web_hole_trace_ladder import RUNG_FACTORS

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "sparse_web_scaling_ladder"

THREADS = (2, 3, 5)
TOP_WINDOW = 5
TOP_HOLES = 10
MAX_DOUBLINGS = 6
MAX_RADIUS = 2**28
MAX_SINGLE_SECONDS = 180
MAX_RUNG_SECONDS = 20 * 60

CONTINUATION_FACTORS = [
    (131101, 144203),
    (1048583, 1153441),
    (8388617, 9227479),
    (67108879, 73819771),
    (536870923, 590558011),
    (104869, 10485767),
    (10487, 104857601),
    (6710887, 671088667),
    (671093, 6710886407),
    (53687099, 5368709131),
    (5368739, 53687091251),
]


def count_divisible(lo, hi, divisor):
    return hi // divisor - (lo - 1) // divisor


def count_not_divisible_by_2(lo, hi, skip):
    total = hi - lo + 1
    count = total - count_divisible(lo, hi, 2)
    if skip % 2 != 0:
        count -= 1
    return count


def count_not_divisible_by_2_or_3(lo, hi, skip):
    total = hi - lo + 1
    count = total
    count -= count_divisible(lo, hi, 2)
    count -= count_divisible(lo, hi, 3)
    count += count_divisible(lo, hi, 6)
    if skip % 2 != 0 and skip % 3 != 0:
        count -= 1
    return count


def count_not_divisible_by_threads(lo, hi, skip):
    total = hi - lo + 1
    count = total
    count -= count_divisible(lo, hi, 2)
    count -= count_divisible(lo, hi, 3)
    count -= count_divisible(lo, hi, 5)
    count += count_divisible(lo, hi, 6)
    count += count_divisible(lo, hi, 10)
    count += count_divisible(lo, hi, 15)
    count -= count_divisible(lo, hi, 30)
    if all(skip % r != 0 for r in THREADS):
        count -= 1
    return count


def scan_cost(n, radius):
    lo = max(4, n - radius)
    hi = n + radius
    touched = hi - lo + 1
    if lo <= n <= hi:
        touched -= 1
    trials = touched
    trials += count_not_divisible_by_2(lo, hi, n)
    trials += count_not_divisible_by_2_or_3(lo, hi, n)
    zero_yield = count_not_divisible_by_threads(lo, hi, n)
    return {
        "touched": touched,
        "trials": trials,
        "zero_yield_inspections": zero_yield,
        "factors_extracted": touched - zero_yield,
    }


def direct_offsets(p, q, radius):
    offsets = {}
    for factor, kind in ((p, "p_thread"), (q, "q_thread")):
        start = -radius // factor
        end = radius // factor
        for multiplier in range(start, end + 1):
            if multiplier == 0:
                continue
            offset = multiplier * factor
            if abs(offset) <= radius:
                offsets[offset] = kind if offset not in offsets else "center"
    return offsets


def supported_holes(n, p, q, radius):
    holes = []
    for offset, kind in direct_offsets(p, q, radius).items():
        value = n + offset
        if value < 4:
            continue
        supporters = [r for r in THREADS if value % r == 0]
        if not supporters:
            continue
        holes.append(
            {
                "offset": offset,
                "value": value,
                "support": len(supporters),
                "supporting_factors": supporters,
                "audit_kind": kind,
                "is_fundamental": abs(offset) in {p, q},
                "recovered_factor": abs(offset) if abs(offset) in {p, q} else None,
            }
        )
    return sorted(holes, key=lambda hole: (-hole["support"], abs(hole["offset"]), hole["offset"]))


def initial_radius(n):
    exponent = max(0, ((n.bit_length() + 1) // 2) - 5)
    return max(16384, 1 << exponent)


def radius_attempts(n):
    radius = initial_radius(n)
    seen = set()
    for _ in range(MAX_DOUBLINGS + 1):
        radius = min(radius, MAX_RADIUS)
        if radius in seen:
            break
        seen.add(radius)
        yield radius
        if radius >= MAX_RADIUS:
            break
        radius *= 2


def coverage_state(radius, p, q):
    if radius >= max(p, q):
        return "full_factor_coverage"
    if radius >= min(p, q):
        return "partial_factor_coverage"
    return "no_factor_coverage"


def classify(radius, p, q, holes, seconds, rung_seconds):
    factor_hits = [
        (index, hole)
        for index, hole in enumerate(holes, start=1)
        if hole["is_fundamental"] and hole["support"] >= 1
    ]
    top_factor_hits = [(index, hole) for index, hole in factor_hits if index <= TOP_WINDOW]
    if top_factor_hits:
        return "one_factor_success", top_factor_hits[0]
    if seconds > MAX_SINGLE_SECONDS or rung_seconds > MAX_RUNG_SECONDS:
        if radius < min(p, q):
            return "coverage_not_reached_at_cap", factor_hits[0] if factor_hits else None
        return "feasibility_cap", factor_hits[0] if factor_hits else None
    if radius < min(p, q):
        return "coverage_failure", factor_hits[0] if factor_hits else None
    return "signal_failure", factor_hits[0] if factor_hits else None


def analyze_attempt(case, radius, rung_seconds):
    started = time.perf_counter()
    p, q = case["p"], case["q"]
    n = p * q
    cost = scan_cost(n, radius)
    holes = supported_holes(n, p, q, radius)
    seconds = time.perf_counter() - started
    classification, best = classify(radius, p, q, holes, seconds, rung_seconds + seconds)
    best_index, best_hole = best if best else (None, None)
    return {
        "name": case["name"],
        "p": p,
        "q": q,
        "N": n,
        "bits": n.bit_length(),
        "radius": radius,
        "radius_to_min_factor": radius / min(p, q),
        "coverage_state": coverage_state(radius, p, q),
        "classification": classification,
        "one_factor_success": classification == "one_factor_success",
        "two_factor_success": (
            classification == "one_factor_success"
            and {p, q}.issubset(
                {
                    hole["recovered_factor"]
                    for index, hole in enumerate(holes, start=1)
                    if index <= TOP_WINDOW and hole["is_fundamental"]
                }
            )
        ),
        "recovered_factor": best_hole["recovered_factor"] if best_hole else None,
        "recovered_offset": best_hole["offset"] if best_hole else None,
        "best_exact_rank": best_index,
        "best_support": best_hole["support"] if best_hole else None,
        "public_threads": list(THREADS),
        "top_holes": holes[:TOP_HOLES],
        "cost": cost,
        "seconds": seconds,
    }


def toy_cases():
    return [{"name": case["name"], "p": case["p"], "q": case["q"]} for case in CASES]


def ladder_cases():
    cases = toy_cases()
    existing = RUNG_FACTORS[4:]
    for index, (p, q) in enumerate(existing, start=4):
        cases.append({"name": f"rung_{index:02d}_{p}x{q}", "p": p, "q": q})
    for index, (p, q) in enumerate(CONTINUATION_FACTORS):
        cases.append({"name": f"continuation_{index:02d}_{p}x{q}", "p": p, "q": q})
    return cases


def write_comparison(rows):
    with (OUT / "comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "rung",
                "bits",
                "p",
                "q",
                "radius",
                "radius_to_min_factor",
                "coverage_state",
                "classification",
                "recovered_factor",
                "best_exact_rank",
                "best_support",
                "touched",
                "trials",
                "zero_yield",
                "seconds",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "rung": row["name"],
                    "bits": row["bits"],
                    "p": row["p"],
                    "q": row["q"],
                    "radius": row["radius"],
                    "radius_to_min_factor": f"{row['radius_to_min_factor']:.6f}",
                    "coverage_state": row["coverage_state"],
                    "classification": row["classification"],
                    "recovered_factor": row["recovered_factor"] or "",
                    "best_exact_rank": row["best_exact_rank"] or "",
                    "best_support": row["best_support"] or "",
                    "touched": row["cost"]["touched"],
                    "trials": row["cost"]["trials"],
                    "zero_yield": row["cost"]["zero_yield_inspections"],
                    "seconds": f"{row['seconds']:.6f}",
                }
            )


def write_summary(best_rows, stop):
    lines = [
        "# Sparse Web Scaling Ladder",
        "",
        "Frozen method: dense presence-only public threads `2,3,5`; first public thread only; no exponent extraction.",
        "",
        f"Radius schedule: `max(16384, 1 << max(0, ((N.bit_length()+1)//2 - 5)))`, doubled up to {MAX_DOUBLINGS} times, capped at `{MAX_RADIUS}`.",
        "",
        "| rung | bits | p | q | radius | radius/min(p,q) | classification | recovered | rank | trials | seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in best_rows:
        lines.append(
            f"| {row['name']} | {row['bits']} | {row['p']} | {row['q']} | "
            f"{row['radius']} | {row['radius_to_min_factor']:.3f} | "
            f"{row['classification']} | {row['recovered_factor'] or ''} | "
            f"{row['best_exact_rank'] or ''} | {row['cost']['trials']} | {row['seconds']:.6f} |"
        )
    lines += ["", "## Stop", "", stop]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    attempts = []
    best_rows = []
    best_holes = []
    stop = "No stop reached."
    for case in ladder_cases():
        rung_seconds = 0.0
        last_attempt = None
        for radius in radius_attempts(case["p"] * case["q"]):
            attempt = analyze_attempt(case, radius, rung_seconds)
            rung_seconds += attempt["seconds"]
            attempts.append(attempt)
            last_attempt = attempt
            if attempt["classification"] == "one_factor_success":
                break
            if attempt["classification"] in {"signal_failure", "coverage_not_reached_at_cap", "feasibility_cap"}:
                break
        if last_attempt is None:
            continue
        best_rows.append(last_attempt)
        for hole in last_attempt["top_holes"]:
            best_holes.append({"rung": last_attempt["name"], **hole})
        if last_attempt["classification"] == "signal_failure":
            stop = f"Stopped at {last_attempt['name']}: covering radius reached but exact factor was not in the top {TOP_WINDOW}."
            break
        if last_attempt["classification"] in {"coverage_not_reached_at_cap", "feasibility_cap"}:
            stop = f"Stopped at {last_attempt['name']}: {last_attempt['classification']}."
            break
    (OUT / "attempts.json").write_text(json.dumps(attempts, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "attempts.jsonl", attempts)
    write_jsonl(OUT / "best_holes.jsonl", best_holes)
    write_comparison(best_rows)
    write_summary(best_rows, stop)
    print(stop)


if __name__ == "__main__":
    main()
