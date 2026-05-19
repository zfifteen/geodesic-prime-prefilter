#!/usr/bin/env python3
"""Benchmark the safe window-ratio band for the frozen three-thread web."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from literal_web_hole_trace import CASES, write_jsonl
from literal_web_hole_trace_ladder import RUNG_FACTORS
from sparse_web_scaling_ladder import CONTINUATION_FACTORS, scan_cost, supported_holes

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "sparse_web_ratio_window_audit"
TOP_WINDOW = 5
RATIOS = [
    0.5,
    0.75,
    1,
    1.25,
    1.5,
    2,
    3,
    4,
    6,
    8,
    10,
    12,
    16,
    20,
    24,
    32,
    40,
    48,
    56,
    64,
    80,
    96,
    112,
    128,
]


def cases():
    rows = [{"name": case["name"], "p": case["p"], "q": case["q"]} for case in CASES]
    for index, (p, q) in enumerate(RUNG_FACTORS[4:], start=4):
        rows.append({"name": f"rung_{index:02d}_{p}x{q}", "p": p, "q": q})
    for index, (p, q) in enumerate(CONTINUATION_FACTORS):
        rows.append({"name": f"continuation_{index:02d}_{p}x{q}", "p": p, "q": q})
    return rows


def classify(p, q, radius, holes):
    exact_hits = [
        (index, hole)
        for index, hole in enumerate(holes, start=1)
        if hole["is_fundamental"] and hole["support"] >= 1
    ]
    top_exact = [(index, hole) for index, hole in exact_hits if index <= TOP_WINDOW]
    if top_exact:
        return "one_factor_success", top_exact[0]
    if radius < min(p, q):
        return "coverage_failure", exact_hits[0] if exact_hits else None
    return "signal_failure", exact_hits[0] if exact_hits else None


def analyze_ratio(case, ratio):
    p, q = case["p"], case["q"]
    n = p * q
    radius = math.ceil(min(p, q) * ratio)
    holes = supported_holes(n, p, q, radius)
    classification, best = classify(p, q, radius, holes)
    best_index, best_hole = best if best else (None, None)
    cost = scan_cost(n, radius)
    return {
        "name": case["name"],
        "p": p,
        "q": q,
        "N": n,
        "bits": n.bit_length(),
        "ratio": ratio,
        "radius": radius,
        "classification": classification,
        "recovered_factor": best_hole["recovered_factor"] if best_hole else None,
        "recovered_offset": best_hole["offset"] if best_hole else None,
        "best_exact_rank": best_index,
        "best_support": best_hole["support"] if best_hole else None,
        "top_holes": holes[:10],
        "cost": cost,
    }


def summarize_case(rows):
    successes = [row for row in rows if row["classification"] == "one_factor_success"]
    failures_after_success = [
        row
        for row in rows
        if row["classification"] == "signal_failure"
        and any(prev["classification"] == "one_factor_success" for prev in rows if prev["ratio"] < row["ratio"])
    ]
    return {
        "case": rows[0]["name"],
        "bits": rows[0]["bits"],
        "p": rows[0]["p"],
        "q": rows[0]["q"],
        "first_success_ratio": successes[0]["ratio"] if successes else None,
        "last_success_ratio": successes[-1]["ratio"] if successes else None,
        "first_failure_after_success_ratio": failures_after_success[0]["ratio"] if failures_after_success else None,
        "first_success_recovered_factor": successes[0]["recovered_factor"] if successes else None,
        "first_success_rank": successes[0]["best_exact_rank"] if successes else None,
        "last_success_rank": successes[-1]["best_exact_rank"] if successes else None,
    }


def write_summary(case_summaries):
    lines = [
        "# Sparse Web Ratio Window Audit",
        "",
        "Frozen method: presence-only public thread set `2,3,5` with exact-factor top-5 audit scoring.",
        "",
        "Benchmark variable: `radius = ratio * min(p,q)`. This uses known factors only to measure the safe ratio band; it is not a public RSA-scale controller.",
        "",
        "| case | bits | first success ratio | last success ratio | first failure after success | recovered at first success | rank |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in case_summaries:
        lines.append(
            f"| {row['case']} | {row['bits']} | {row['first_success_ratio'] or ''} | "
            f"{row['last_success_ratio'] or ''} | {row['first_failure_after_success_ratio'] or ''} | "
            f"{row['first_success_recovered_factor'] or ''} | {row['first_success_rank'] or ''} |"
        )
    first_failures = [row["first_failure_after_success_ratio"] for row in case_summaries if row["first_failure_after_success_ratio"]]
    lines += ["", "## Result", ""]
    if first_failures:
        lines.append(f"First observed post-success failure ratio: `{min(first_failures)}`.")
    else:
        lines.append("No post-success failure observed within the tested ratio list.")
    lines.append("The adaptive controller target is therefore not a large fixed window. It is a small covering window near the first success ratio, with a measured upper danger band recorded separately.")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison(case_summaries):
    with (OUT / "comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case",
                "bits",
                "p",
                "q",
                "first_success_ratio",
                "last_success_ratio",
                "first_failure_after_success_ratio",
                "first_success_recovered_factor",
                "first_success_rank",
                "last_success_rank",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(case_summaries)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    attempts = []
    best_holes = []
    summaries = []
    for case in cases():
        rows = [analyze_ratio(case, ratio) for ratio in RATIOS]
        attempts.extend(rows)
        summaries.append(summarize_case(rows))
        for row in rows:
            if row["ratio"] in {1, 2, 4, 8, 16, 32, 40, 48, 64, 128}:
                for hole in row["top_holes"]:
                    best_holes.append({"case": row["name"], "ratio": row["ratio"], **hole})
    (OUT / "attempts.json").write_text(json.dumps(attempts, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "attempts.jsonl", attempts)
    write_jsonl(OUT / "sampled_top_holes.jsonl", best_holes)
    write_comparison(summaries)
    write_summary(summaries)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
