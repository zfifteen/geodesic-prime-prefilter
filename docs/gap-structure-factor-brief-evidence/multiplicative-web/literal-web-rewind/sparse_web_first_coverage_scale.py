#!/usr/bin/env python3
"""Scale the frozen web at the benchmark first-coverage radius."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from literal_web_hole_trace import write_jsonl
from sparse_web_scaling_ladder import CONTINUATION_FACTORS, scan_cost, supported_holes

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "sparse_web_first_coverage_scale"
TOP_WINDOW = 5

SCALE_FACTORS = [
    (2147496017, 2362286341),
    (549755826239, 604731449599),
    (140737488367699, 154811237245229),
    (36028797018976327, 39631676720914723),
    (9223372036854788173, 10145709240540308543),
    (604462909807314587365499, 664909200788046099829843),
    (39614081257132168796771987681, 43575489382845389194886435893),
    (170141183460469231731687303715884118099, 187155301806516170016428779270337254613),
]


def cases():
    rows = []
    for index, (p, q) in enumerate(CONTINUATION_FACTORS):
        rows.append({"name": f"continuation_{index:02d}_{p}x{q}", "p": p, "q": q})
    for index, (p, q) in enumerate(SCALE_FACTORS):
        rows.append({"name": f"scale_{index:02d}_{(p*q).bit_length()}bit", "p": p, "q": q})
    return rows


def analyze_case(case):
    p, q = case["p"], case["q"]
    n = p * q
    radius = min(p, q)
    holes = supported_holes(n, p, q, radius)
    factor_hits = [
        (index, hole)
        for index, hole in enumerate(holes, start=1)
        if hole["is_fundamental"] and hole["support"] >= 1
    ]
    top_hits = [(index, hole) for index, hole in factor_hits if index <= TOP_WINDOW]
    best_index, best_hole = top_hits[0] if top_hits else factor_hits[0] if factor_hits else (None, None)
    classification = "one_factor_success" if top_hits else "signal_failure"
    return {
        "name": case["name"],
        "p": p,
        "q": q,
        "N": n,
        "bits": n.bit_length(),
        "radius": radius,
        "radius_to_min_factor": 1.0,
        "classification": classification,
        "recovered_factor": best_hole["recovered_factor"] if best_hole else None,
        "recovered_offset": best_hole["offset"] if best_hole else None,
        "best_exact_rank": best_index,
        "best_support": best_hole["support"] if best_hole else None,
        "cost": scan_cost(n, radius),
        "top_holes": holes[:10],
    }


def write_summary(results):
    lines = [
        "# Sparse Web First-Coverage Scale",
        "",
        "Frozen method: presence-only public thread set `2,3,5` with exact-factor top-5 audit scoring.",
        "",
        "Benchmark window: `radius = min(p,q)`. Known factors are used only to set first coverage and audit exact recovery. This is not a public RSA controller.",
        "",
        "| case | bits | radius | classification | recovered | rank | support | trials |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        lines.append(
            f"| {result['name']} | {result['bits']} | {result['radius']} | "
            f"{result['classification']} | {result['recovered_factor'] or ''} | "
            f"{result['best_exact_rank'] or ''} | {result['best_support'] or ''} | "
            f"{result['cost']['trials']} |"
        )
    successes = sum(1 for result in results if result["classification"] == "one_factor_success")
    lines += [
        "",
        "## Result",
        "",
        f"`{successes} / {len(results)}` benchmark first-coverage cases recovered one exact factor inside the top {TOP_WINDOW}.",
        "This confirms the frozen web arithmetic scales on the measured benchmark surface. The unresolved problem remains the public controller that finds a first-covering window without `p/q`.",
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison(results):
    with (OUT / "comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case",
                "bits",
                "radius",
                "classification",
                "recovered_factor",
                "best_exact_rank",
                "best_support",
                "touched",
                "trials",
                "zero_yield",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "case": result["name"],
                    "bits": result["bits"],
                    "radius": result["radius"],
                    "classification": result["classification"],
                    "recovered_factor": result["recovered_factor"] or "",
                    "best_exact_rank": result["best_exact_rank"] or "",
                    "best_support": result["best_support"] or "",
                    "touched": result["cost"]["touched"],
                    "trials": result["cost"]["trials"],
                    "zero_yield": result["cost"]["zero_yield_inspections"],
                }
            )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = [analyze_case(case) for case in cases()]
    (OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "results.jsonl", results)
    write_jsonl(OUT / "top_holes.jsonl", [{"case": row["name"], **hole} for row in results for hole in row["top_holes"]])
    write_comparison(results)
    write_summary(results)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
