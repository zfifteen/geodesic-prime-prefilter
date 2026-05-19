#!/usr/bin/env python3
"""Find the cheapest sparse web policy that recovers at least one hidden thread."""

from __future__ import annotations

import csv
import json
import time
from collections import defaultdict
from pathlib import Path

from literal_web_hole_trace import CASES, analyze_case, factor_label, thread_slots, write_jsonl

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "sparse_web_minimum_ladder"
TOP_WINDOW = 5
TOP_DIRECT_WINDOW = 18
MIN_PUBLIC_THREADS = 3

POLICIES = [
    {"name": "trial_2_stop_1", "primes": [2], "max_factors": 1},
    {"name": "trial_2_3_5_stop_1", "primes": [2, 3, 5], "max_factors": 1},
    {"name": "prime_leq_7_stop_2", "primes": [2, 3, 5, 7], "max_factors": 2},
    {"name": "prime_leq_13_stop_2", "primes": [2, 3, 5, 7, 11, 13], "max_factors": 2},
    {"name": "prime_leq_31_stop_2", "primes": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31], "max_factors": 2},
]


def sparse_rows_around(n, radius, policy):
    rows = []
    cost = {
        "touched": 0,
        "trials": 0,
        "zero_yield_inspections": 0,
        "factors_extracted": 0,
    }
    for original in range(n - radius, n + radius + 1):
        if original < 4 or original == n:
            continue
        cost["touched"] += 1
        current = original
        factors = {}
        for r in policy["primes"]:
            if len(factors) >= policy["max_factors"]:
                break
            exponent = 0
            while True:
                cost["trials"] += 1
                if current % r != 0:
                    break
                exponent += 1
                current //= r
            if exponent:
                factors[r] = exponent
        if not factors:
            cost["zero_yield_inspections"] += 1
            continue
        cost["factors_extracted"] += len(factors)
        rows.append(
            {
                "value": original,
                "offset": original - n,
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


def analyze_sparse_case(case, policy):
    started = time.perf_counter()
    p, q, radius = case["p"], case["q"], case["radius"]
    n = p * q
    rows, cost = sparse_rows_around(n, radius, policy)
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
        row = by_offset.get(offset)
        audit = direct_offsets.get(offset)
        holes.append(
            {
                "case": case["name"],
                "policy": policy["name"],
                "offset": offset,
                "value": n + offset,
                "support": len(supporters),
                "supporting_factors": supporters,
                "audit_kind": audit if audit else ("public_sparse_row" if row else "not_observed"),
                "audit_factorization": row["factorization"] if row else None,
            }
        )

    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        supporters = support.get(offset, [])
        direct_rows.append(
            {
                "offset": offset,
                "kind": kind,
                "value": n + offset,
                "support": len(supporters),
                "supporting_factors": supporters,
            }
        )

    factor_hits = [
        {
            "rank": index,
            "offset": hole["offset"],
            "recovered_factor": abs(hole["offset"]),
            "kind": hole["audit_kind"],
            "support": hole["support"],
            "supporting_factors": hole["supporting_factors"],
        }
        for index, hole in enumerate(holes, start=1)
        if hole["audit_kind"] in {"p_thread", "q_thread"} and abs(hole["offset"]) in {p, q}
    ]
    best_factor = factor_hits[0] if factor_hits else None
    eligible = len(public_factors) >= MIN_PUBLIC_THREADS
    top_window = holes[:TOP_WINDOW]
    one_factor_success = eligible and any(
        hole["audit_kind"] in {"p_thread", "q_thread"}
        and abs(hole["offset"]) in {p, q}
        and hole["support"] >= 1
        for hole in top_window
    )
    top_factors = {
        abs(hole["offset"])
        for hole in top_window
        if hole["audit_kind"] in {"p_thread", "q_thread"}
        and abs(hole["offset"]) in {p, q}
        and hole["support"] >= 1
    }
    two_factor_success = eligible and {p, q}.issubset(top_factors)
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
        "policy": policy["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "classification": classification,
        "eligible_for_scoring": eligible,
        "distinct_public_threads": len(public_factors),
        "public_threads": public_factors,
        "one_factor_success": one_factor_success,
        "two_factor_success": two_factor_success,
        "top18_direct_hits": top18_direct_hits,
        "best_hidden_rank": best_factor["rank"] if best_factor else None,
        "best_hidden_offset": best_factor["offset"] if best_factor else None,
        "best_hidden_kind": best_factor["kind"] if best_factor else None,
        "recovered_factor": best_factor["recovered_factor"] if one_factor_success and best_factor else None,
        "row_count_sparse": len(rows),
        "row_count_public": len(public_rows),
        "direct_row_count": len(direct_rows),
        "supported_direct_count": sum(1 for row in direct_rows if row["support"] > 0),
        "cost": cost,
        "seconds": time.perf_counter() - started,
        "direct_rows": direct_rows,
        "top_holes": holes[:TOP_DIRECT_WINDOW],
    }


def policy_passed(results):
    return all(result["classification"] == "one_factor_success" for result in results)


def write_policy_outputs(policy, results):
    out = OUT_ROOT / policy["name"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(out / "top_holes.jsonl", [hole for result in results for hole in result["top_holes"]])
    lines = [
        f"# Sparse Web Minimum Ladder: {policy['name']}",
        "",
        f"Policy primes: `{policy['primes']}`. Max distinct factors per composite: `{policy['max_factors']}`.",
        "",
        "| case | public r count | classification | recovered factor | one-factor | two-factor | best hidden rank | top18 direct hits | touched | trials | zero-yield | seconds |",
        "| --- | ---: | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        best_rank = result["best_hidden_rank"] if result["best_hidden_rank"] is not None else ""
        lines.append(
            f"| {result['name']} | {result['distinct_public_threads']} | "
            f"{result['classification']} | {result['recovered_factor'] or ''} | "
            f"{str(result['one_factor_success']).lower()} | "
            f"{str(result['two_factor_success']).lower()} | {best_rank} | "
            f"{result['top18_direct_hits']} | {result['cost']['touched']} | "
            f"{result['cost']['trials']} | {result['cost']['zero_yield_inspections']} | "
            f"{result['seconds']:.6f} |"
        )
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparison(rows):
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    baseline_by_case = {case["name"]: analyze_case(case) for case in CASES}
    with (OUT_ROOT / "comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case",
                "policy",
                "classification",
                "sparse_public_r_count",
                "sparse_one_factor_success",
                "sparse_recovered_factor",
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
        for result in rows:
            baseline = baseline_by_case[result["name"]]
            writer.writerow(
                {
                    "case": result["name"],
                    "policy": result["policy"],
                    "classification": result["classification"],
                    "sparse_public_r_count": result["distinct_public_threads"],
                    "sparse_one_factor_success": result["one_factor_success"],
                    "sparse_recovered_factor": result["recovered_factor"] or "",
                    "sparse_two_factor_success": result["two_factor_success"],
                    "sparse_top18_direct_hits": result["top18_direct_hits"],
                    "sparse_trials": result["cost"]["trials"],
                    "sparse_zero_yield": result["cost"]["zero_yield_inspections"],
                    "full_web_top18_direct_hits": baseline["top18_direct_hits"],
                    "full_web_direct_rows": baseline["direct_row_count"],
                }
            )


def write_summary(policy_rows, stopping_policy):
    lines = [
        "# Sparse Web Minimum Ladder",
        "",
        "Goal: find the cheapest ordered sparse policy that recovers at least one hidden factor thread on all four toys.",
        "",
        "| policy | cases | passed cases | classifications | total trials | status |",
        "| --- | ---: | ---: | --- | ---: | --- |",
    ]
    for policy in POLICIES:
        results = policy_rows.get(policy["name"], [])
        if not results:
            continue
        counts = {}
        for result in results:
            counts[result["classification"]] = counts.get(result["classification"], 0) + 1
        classes = ", ".join(f"{key}:{value}" for key, value in sorted(counts.items()))
        passed = sum(1 for result in results if result["classification"] == "one_factor_success")
        trials = sum(result["cost"]["trials"] for result in results)
        status = "minimum_success" if stopping_policy == policy["name"] else "measured"
        lines.append(f"| {policy['name']} | {len(results)} | {passed} | {classes} | {trials} | {status} |")
    lines += [
        "",
        "## Result",
        "",
    ]
    if stopping_policy:
        lines.append(f"`{stopping_policy}` is the first ordered policy that finds at least one hidden factor thread on all four toys.")
    else:
        lines.append("No ordered policy found one hidden factor thread on all four toys.")
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    all_results = []
    policy_rows = {}
    stopping_policy = None
    for policy in POLICIES:
        results = [analyze_sparse_case(case, policy) for case in CASES]
        policy_rows[policy["name"]] = results
        all_results.extend(results)
        write_policy_outputs(policy, results)
        if policy_passed(results):
            stopping_policy = policy["name"]
            break
    (OUT_ROOT / "results.json").write_text(json.dumps(all_results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT_ROOT / "results.jsonl", all_results)
    write_comparison(all_results)
    write_summary(policy_rows, stopping_policy)
    print(stopping_policy if stopping_policy else "no_success")


if __name__ == "__main__":
    main()
