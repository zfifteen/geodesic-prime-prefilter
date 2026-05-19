#!/usr/bin/env python3
"""First sparse-web slice: trial only by 2, then apply the diversity gate."""

from __future__ import annotations

import csv
import json
import time
from collections import defaultdict
from pathlib import Path

from literal_web_hole_trace import CASES, analyze_case, factor_label, thread_slots, write_jsonl

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "sparse_web_minimality_ladder"
POLICY = "trial_2_stop_1"
OUT = OUT_ROOT / POLICY
TOP_WINDOW = 5
TOP_DIRECT_WINDOW = 18
MIN_PUBLIC_THREADS = 3


def sparse_rows_around(n, radius):
    rows = []
    cost = {
        "touched": 0,
        "trials": 0,
        "zero_yield_inspections": 0,
        "factors_extracted": 0,
    }
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        cost["touched"] += 1
        current = value
        exponent = 0
        while True:
            cost["trials"] += 1
            if current % 2 != 0:
                break
            exponent += 1
            current //= 2
        if exponent == 0:
            cost["zero_yield_inspections"] += 1
            continue
        factors = {2: exponent}
        cost["factors_extracted"] += 1
        rows.append(
            {
                "value": value,
                "offset": value - n,
                "factors": factors,
                "factorization": factor_label(factors),
            }
        )
    return rows, cost


def audit_kind(value, p, q):
    has_p = value % p == 0
    has_q = value % q == 0
    if has_p and has_q:
        return "center"
    if has_p:
        return "p_thread"
    if has_q:
        return "q_thread"
    return None


def analyze_sparse_case(case):
    started = time.perf_counter()
    p, q, radius = case["p"], case["q"], case["radius"]
    n = p * q
    rows, cost = sparse_rows_around(n, radius)
    by_offset = {row["offset"]: row for row in rows}

    direct_offsets = {}
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        kind = audit_kind(value, p, q)
        if kind:
            direct_offsets[value - n] = kind

    public_rows = [row for row in rows if row["offset"] not in direct_offsets]
    public_offsets = {row["offset"] for row in public_rows}
    public_factors = sorted({r for row in public_rows for r in row["factors"]})

    support = defaultdict(list)
    for r in public_factors:
        for offset in thread_slots(n, radius, r):
            if offset not in public_offsets:
                support[offset].append(r)

    holes = []
    for offset, supporters in sorted(
        support.items(), key=lambda item: (-len(item[1]), abs(item[0]), item[0])
    ):
        value = n + offset
        audit = direct_offsets.get(offset)
        row = by_offset.get(offset)
        holes.append(
            {
                "case": case["name"],
                "policy": POLICY,
                "offset": offset,
                "value": value,
                "support": len(supporters),
                "supporting_factors": supporters,
                "audit_kind": audit if audit else ("public_sparse_row" if row else "not_observed"),
                "audit_factorization": row["factorization"] if row else None,
            }
        )

    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        value = n + offset
        supporters = support.get(offset, [])
        direct_rows.append(
            {
                "offset": offset,
                "kind": kind,
                "value": value,
                "support": len(supporters),
                "supporting_factors": supporters,
            }
        )

    hidden_ranks = []
    for index, hole in enumerate(holes, start=1):
        if hole["audit_kind"] in {"p_thread", "q_thread"}:
            hidden_ranks.append(index)

    distinct_public_threads = len(public_factors)
    eligible = distinct_public_threads >= MIN_PUBLIC_THREADS
    top_window = holes[:TOP_WINDOW]
    one_factor_success = (
        eligible
        and any(
            hole["audit_kind"] in {"p_thread", "q_thread"} and hole["support"] >= 1
            for hole in top_window
        )
    )
    top_kinds = {hole["audit_kind"] for hole in top_window if hole["support"] >= 1}
    two_factor_success = eligible and {"p_thread", "q_thread"}.issubset(top_kinds)
    top18_direct_hits = sum(
        1 for hole in holes[:TOP_DIRECT_WINDOW] if hole["audit_kind"] in {"p_thread", "q_thread"}
    )

    if not eligible:
        classification = "insufficient_thread_diversity"
    elif one_factor_success:
        classification = "one_factor_success"
    else:
        classification = "signal_failure"

    return {
        "name": case["name"],
        "policy": POLICY,
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "classification": classification,
        "eligible_for_scoring": eligible,
        "distinct_public_threads": distinct_public_threads,
        "public_threads": public_factors,
        "one_factor_success": one_factor_success,
        "two_factor_success": two_factor_success,
        "top18_direct_hits": top18_direct_hits,
        "best_hidden_rank": min(hidden_ranks) if hidden_ranks else None,
        "row_count_sparse": len(rows),
        "row_count_public": len(public_rows),
        "direct_row_count": len(direct_rows),
        "supported_direct_count": sum(1 for row in direct_rows if row["support"] > 0),
        "cost": cost,
        "seconds": time.perf_counter() - started,
        "direct_rows": direct_rows,
        "top_holes": holes[:TOP_DIRECT_WINDOW],
    }


def load_or_run_baseline(case):
    return analyze_case(case)


def write_summary(results):
    lines = [
        "# Sparse Web First Slice",
        "",
        f"Policy: `{POLICY}`.",
        "",
        "Extractor: dense offsets, trial division only by `2`, record multiplicity, stop.",
        "",
        f"Scoring gate: at least `{MIN_PUBLIC_THREADS}` distinct public thread values before one-factor scoring.",
        "",
        "| case | public r count | classification | one-factor | two-factor | best hidden rank | top18 direct hits | touched | trials | zero-yield | seconds |",
        "| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        best_rank = result["best_hidden_rank"] if result["best_hidden_rank"] is not None else ""
        lines.append(
            f"| {result['name']} | {result['distinct_public_threads']} | "
            f"{result['classification']} | {str(result['one_factor_success']).lower()} | "
            f"{str(result['two_factor_success']).lower()} | {best_rank} | "
            f"{result['top18_direct_hits']} | {result['cost']['touched']} | "
            f"{result['cost']['trials']} | {result['cost']['zero_yield_inspections']} | "
            f"{result['seconds']:.6f} |"
        )
    lines += [
        "",
        "## Measured Result",
        "",
        "`trial_2_stop_1` reaches only one public thread value, `r = 2`, on every toy case.",
        "Under the v1.0 contract, each run is classified `insufficient_thread_diversity` before hidden-thread scoring.",
        "This is an informative lower bound: parity alone creates a comb, not a multiplicative web with public-thread intersections.",
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison(results):
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    path = OUT_ROOT / "comparison.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case",
                "policy",
                "classification",
                "sparse_public_r_count",
                "sparse_one_factor_success",
                "sparse_two_factor_success",
                "sparse_top18_direct_hits",
                "sparse_trials",
                "sparse_zero_yield",
                "full_web_top18_direct_hits",
                "full_web_direct_rows",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for result in results:
            baseline = load_or_run_baseline(
                {"name": result["name"], "p": result["p"], "q": result["q"], "radius": result["radius"]}
            )
            writer.writerow(
                {
                    "case": result["name"],
                    "policy": POLICY,
                    "classification": result["classification"],
                    "sparse_public_r_count": result["distinct_public_threads"],
                    "sparse_one_factor_success": result["one_factor_success"],
                    "sparse_two_factor_success": result["two_factor_success"],
                    "sparse_top18_direct_hits": result["top18_direct_hits"],
                    "sparse_trials": result["cost"]["trials"],
                    "sparse_zero_yield": result["cost"]["zero_yield_inspections"],
                    "full_web_top18_direct_hits": baseline["top18_direct_hits"],
                    "full_web_direct_rows": baseline["direct_row_count"],
                }
            )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = [analyze_sparse_case(case) for case in CASES]
    (OUT / "summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(
        OUT / "top_holes.jsonl",
        [hole for result in results for hole in result["top_holes"]],
    )
    write_summary(results)
    write_comparison(results)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
