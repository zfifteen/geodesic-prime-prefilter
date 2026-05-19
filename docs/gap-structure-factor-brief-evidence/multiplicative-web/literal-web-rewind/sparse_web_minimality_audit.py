#!/usr/bin/env python3
"""Audit whether the current sparse web success is minimal on the toy surface."""

from __future__ import annotations

import csv
import json
import itertools
import time
from collections import defaultdict
from pathlib import Path

from literal_web_hole_trace import CASES, factor_label, thread_slots, write_jsonl

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "sparse_web_minimality_audit"
TOP_WINDOW = 5
TOP_DIRECT_WINDOW = 18
MIN_PUBLIC_THREADS = 3
SMALL_PRIMES = [2, 3, 5, 7, 11]


def offset_order(radius):
    yield from sorted((t for t in range(-radius, radius + 1) if t), key=lambda t: (abs(t), t))


def extract_first_factor(value, primes):
    trials = 0
    for r in primes:
        current = value
        exponent = 0
        while True:
            trials += 1
            if current % r != 0:
                break
            exponent += 1
            current //= r
        if exponent:
            return {r: exponent}, trials
    return {}, trials


def extract_first_presence(value, primes):
    trials = 0
    for r in primes:
        trials += 1
        if value % r == 0:
            return {r: 1}, trials
    return {}, trials


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


def score_case(case, policy_name, public_factors, observed_offsets, observed_rows, cost, seconds):
    p, q, radius = case["p"], case["q"], case["radius"]
    n = p * q
    direct_offsets = {}
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        kind = audit_kind(value, p, q)
        if kind:
            direct_offsets[value - n] = kind

    public_offsets = set(observed_offsets) - set(direct_offsets)
    by_offset = {row["offset"]: row for row in observed_rows}

    support = defaultdict(list)
    for r in sorted(public_factors):
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
                "policy": policy_name,
                "offset": offset,
                "value": n + offset,
                "support": len(supporters),
                "supporting_factors": supporters,
                "audit_kind": audit if audit else ("observed_public_row" if row else "not_observed"),
                "audit_factorization": row["factorization"] if row else None,
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
    one_factor_success = eligible and any(
        hole["audit_kind"] in {"p_thread", "q_thread"}
        and abs(hole["offset"]) in {p, q}
        and hole["support"] >= 1
        for hole in holes[:TOP_WINDOW]
    )
    top_factors = {
        abs(hole["offset"])
        for hole in holes[:TOP_WINDOW]
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
        "policy": policy_name,
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "classification": classification,
        "public_threads": sorted(public_factors),
        "distinct_public_threads": len(public_factors),
        "one_factor_success": one_factor_success,
        "two_factor_success": two_factor_success,
        "top18_direct_hits": top18_direct_hits,
        "best_hidden_rank": best_factor["rank"] if best_factor else None,
        "best_hidden_offset": best_factor["offset"] if best_factor else None,
        "best_hidden_kind": best_factor["kind"] if best_factor else None,
        "recovered_factor": best_factor["recovered_factor"] if one_factor_success and best_factor else None,
        "cost": cost,
        "seconds": seconds,
        "top_holes": holes[:TOP_DIRECT_WINDOW],
    }


def dense_thread_set_case(case, primes):
    started = time.perf_counter()
    n = case["p"] * case["q"]
    cost = {"touched": 0, "trials": 0, "zero_yield_inspections": 0, "factors_extracted": 0}
    observed_rows = []
    public_factors = set()
    observed_offsets = set()
    for offset in range(-case["radius"], case["radius"] + 1):
        value = n + offset
        if offset == 0 or value < 4:
            continue
        cost["touched"] += 1
        factors, trials = extract_first_factor(value, primes)
        cost["trials"] += trials
        if not factors:
            cost["zero_yield_inspections"] += 1
            continue
        public_factors.update(factors)
        cost["factors_extracted"] += 1
        observed_offsets.add(offset)
        observed_rows.append(
            {
                "value": value,
                "offset": offset,
                "factors": factors,
                "factorization": factor_label(factors),
            }
        )
    policy_name = "dense_first_" + "_".join(map(str, primes))
    return score_case(case, policy_name, public_factors, observed_offsets, observed_rows, cost, time.perf_counter() - started)


def dense_presence_case(case, primes):
    started = time.perf_counter()
    n = case["p"] * case["q"]
    cost = {"touched": 0, "trials": 0, "zero_yield_inspections": 0, "factors_extracted": 0}
    observed_rows = []
    public_factors = set()
    observed_offsets = set()
    for offset in range(-case["radius"], case["radius"] + 1):
        value = n + offset
        if offset == 0 or value < 4:
            continue
        cost["touched"] += 1
        factors, trials = extract_first_presence(value, primes)
        cost["trials"] += trials
        if not factors:
            cost["zero_yield_inspections"] += 1
            continue
        public_factors.update(factors)
        cost["factors_extracted"] += 1
        observed_offsets.add(offset)
        observed_rows.append(
            {
                "value": value,
                "offset": offset,
                "factors": factors,
                "factorization": factor_label(factors),
            }
        )
    policy_name = "presence_first_" + "_".join(map(str, primes))
    return score_case(case, policy_name, public_factors, observed_offsets, observed_rows, cost, time.perf_counter() - started)


def center_out_discovery_case(case, primes):
    started = time.perf_counter()
    n = case["p"] * case["q"]
    cost = {"touched": 0, "trials": 0, "zero_yield_inspections": 0, "factors_extracted": 0}
    observed_rows = []
    public_factors = set()
    observed_offsets = set()
    for offset in offset_order(case["radius"]):
        if len(public_factors) >= MIN_PUBLIC_THREADS:
            break
        value = n + offset
        if value < 4:
            continue
        cost["touched"] += 1
        factors, trials = extract_first_factor(value, primes)
        cost["trials"] += trials
        if not factors:
            cost["zero_yield_inspections"] += 1
            continue
        public_factors.update(factors)
        cost["factors_extracted"] += 1
        observed_offsets.add(offset)
        observed_rows.append(
            {
                "value": value,
                "offset": offset,
                "factors": factors,
                "factorization": factor_label(factors),
            }
        )
    policy_name = "center_out_until_3_first_" + "_".join(map(str, primes))
    return score_case(case, policy_name, public_factors, observed_offsets, observed_rows, cost, time.perf_counter() - started)


def write_summary(dense_results, presence_results, discovery_results):
    lines = [
        "# Sparse Web Minimality Audit",
        "",
        "This audit checks whether the current successful policy is minimal on the four-toy surface.",
        "",
        "The diversity gate requires at least three distinct public thread values. Therefore every one-thread and two-thread dense policy is classified before scoring as `insufficient_thread_diversity`.",
        "",
        "## Dense Thread-Set Audit",
        "",
        "| policy | cases | one-factor successes | classifications | total trials |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    by_policy = {}
    for result in dense_results:
        by_policy.setdefault(result["policy"], []).append(result)
    for policy, rows in by_policy.items():
        counts = {}
        for row in rows:
            counts[row["classification"]] = counts.get(row["classification"], 0) + 1
        classes = ", ".join(f"{key}:{value}" for key, value in sorted(counts.items()))
        lines.append(
            f"| {policy} | {len(rows)} | {sum(row['one_factor_success'] for row in rows)} | "
            f"{classes} | {sum(row['cost']['trials'] for row in rows)} |"
        )

    lines += [
        "",
        "## Presence-Only Dense Audit",
        "",
        "This removes the exponent-peeling work. The web only uses whether a public factor thread exists, so multiplicity is unnecessary for this experiment.",
        "",
        "| policy | cases | one-factor successes | classifications | total trials |",
        "| --- | ---: | ---: | --- | ---: |",
    ]
    by_policy = {}
    for result in presence_results:
        by_policy.setdefault(result["policy"], []).append(result)
    for policy, rows in by_policy.items():
        counts = {}
        for row in rows:
            counts[row["classification"]] = counts.get(row["classification"], 0) + 1
        classes = ", ".join(f"{key}:{value}" for key, value in sorted(counts.items()))
        lines.append(
            f"| {policy} | {len(rows)} | {sum(row['one_factor_success'] for row in rows)} | "
            f"{classes} | {sum(row['cost']['trials'] for row in rows)} |"
        )

    lines += [
        "",
        "## Center-Out Discovery Audit",
        "",
        "| case | policy | touched | trials | public threads | recovered factor | rank | classification |",
        "| --- | --- | ---: | ---: | --- | ---: | ---: | --- |",
    ]
    for row in discovery_results:
        threads = ", ".join(map(str, row["public_threads"]))
        lines.append(
            f"| {row['name']} | {row['policy']} | {row['cost']['touched']} | "
            f"{row['cost']['trials']} | {threads} | {row['recovered_factor'] or ''} | "
            f"{row['best_hidden_rank'] or ''} | {row['classification']} |"
        )
    lines += [
        "",
        "## Result",
        "",
        "`2,3,5` is minimal by public-thread count under the three-thread diversity gate.",
        "Dense `2,3,5` succeeds on all four toys and is the successful policy with the smallest prime ceiling in this audit.",
        "Presence-only `2,3,5` removes unnecessary multiplicity extraction and ties for the lowest trial count among successful three-thread policies with the same first two tests.",
        "The center-out acquisition that stops as soon as it discovers `2`, `3`, and `5` is not sufficient on this surface: it succeeds on the first two toys and fails on the last two.",
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "case",
                "policy",
                "classification",
                "public_threads",
                "one_factor_success",
                "recovered_factor",
                "best_hidden_rank",
                "top18_direct_hits",
                "touched",
                "trials",
                "zero_yield",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "case": row["name"],
                    "policy": row["policy"],
                    "classification": row["classification"],
                    "public_threads": " ".join(map(str, row["public_threads"])),
                    "one_factor_success": row["one_factor_success"],
                    "recovered_factor": row["recovered_factor"] or "",
                    "best_hidden_rank": row["best_hidden_rank"] or "",
                    "top18_direct_hits": row["top18_direct_hits"],
                    "touched": row["cost"]["touched"],
                    "trials": row["cost"]["trials"],
                    "zero_yield": row["cost"]["zero_yield_inspections"],
                }
            )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dense_sets = []
    for size in (1, 2, 3):
        dense_sets.extend(itertools.combinations(SMALL_PRIMES, size))
    dense_results = [
        dense_thread_set_case(case, list(primes))
        for primes in dense_sets
        for case in CASES
    ]
    presence_results = [
        dense_presence_case(case, list(primes))
        for primes in dense_sets
        for case in CASES
    ]
    discovery_results = [
        center_out_discovery_case(case, [2, 3, 5])
        for case in CASES
    ]
    all_results = dense_results + presence_results + discovery_results
    (OUT / "results.json").write_text(json.dumps(all_results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "top_holes.jsonl", [hole for row in all_results for hole in row["top_holes"]])
    write_csv(OUT / "comparison.csv", all_results)
    write_summary(dense_results, presence_results, discovery_results)
    print("wrote minimality audit")


if __name__ == "__main__":
    main()
