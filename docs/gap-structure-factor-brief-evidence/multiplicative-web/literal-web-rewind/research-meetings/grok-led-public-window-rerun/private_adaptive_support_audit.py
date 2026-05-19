#!/usr/bin/env python3
"""Private audit for the public adaptive support v2 rerun.

This audit constructs benchmark semiprimes and scores frozen public outputs.
The public runner receives only N.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_adaptive_support_runner import (
    PUBLIC_RADII,
    PUBLIC_THREADS,
    PUBLIC_TOP_K,
    congruent_offsets,
    public_adaptive_nominate,
)

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_adaptive_support_v2"

AUDIT_CASES: list[dict[str, Any]] = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
    {"name": "continuation_00_131101x144203", "p": 131101, "q": 144203},
    {"name": "continuation_01_1048583x1153441", "p": 1048583, "q": 1153441},
]


def rank_in_attempt(attempt: dict[str, Any], target_offset: int) -> dict[str, Any]:
    for idx, item in enumerate(attempt["top_nominated"], start=1):
        if item["offset"] == target_offset:
            return {
                "found": True,
                "rank": idx,
                "support_count": item["support_count"],
                "threads": item["threads"],
            }
    return {
        "found": False,
        "rank": None,
        "support_count": None,
        "threads": [],
    }


def full_rank_at_radius(n: int, radius: int, target_offset: int) -> dict[str, Any]:
    support: dict[int, list[int]] = {}
    for r in PUBLIC_THREADS:
        for t in congruent_offsets(n, r, radius):
            value = n + t
            if value < 4:
                continue
            support.setdefault(t, []).append(r)

    if target_offset not in support:
        return {
            "found": False,
            "rank": None,
            "support_count": None,
            "threads": [],
            "total_nominated": len(support),
        }

    target = {
        "offset": target_offset,
        "support_count": len(support[target_offset]),
    }
    rank = 1
    for offset, threads in support.items():
        if offset == target_offset:
            continue
        other = {
            "offset": offset,
            "support_count": len(threads),
        }
        if (-other["support_count"], abs(other["offset"]), other["offset"]) < (
            -target["support_count"],
            abs(target["offset"]),
            target["offset"],
        ):
            rank += 1

    return {
        "found": True,
        "rank": rank,
        "support_count": len(support[target_offset]),
        "threads": support[target_offset],
        "total_nominated": len(support),
    }


def audit_case(case: dict[str, Any]) -> dict[str, Any]:
    p = case["p"]
    q = case["q"]
    n = p * q
    name = case["name"]

    public = public_adaptive_nominate(n)
    public_dir = OUT_ROOT / "public_frozen" / name
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "public_result.json").write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    target_offsets = {"p": p, "-p": -p, "q": q, "-q": -q}
    attempt_records = []
    first_hit = None

    for attempt in public["attempts"]:
        per_target = {
            label: rank_in_attempt(attempt, offset)
            for label, offset in target_offsets.items()
        }
        full_ranks = {
            label: full_rank_at_radius(n, attempt["R"], offset)
            for label, offset in target_offsets.items()
        }
        hits = [
            {"which": label, **record}
            for label, record in per_target.items()
            if record["found"]
        ]
        covered = any(abs(offset) <= attempt["R"] for offset in target_offsets.values())
        attempt_record = {
            "R": attempt["R"],
            "covered_by_R": covered,
            "hits": hits,
            "target_ranks": per_target,
            "full_target_ranks": full_ranks,
            "nominated_count": attempt["nominated_count"],
            "cost": attempt["cost"],
        }
        attempt_records.append(attempt_record)
        if hits and first_hit is None:
            best = sorted(hits, key=lambda item: item["rank"])[0]
            first_hit = {
                "R": attempt["R"],
                "which": best["which"],
                "rank": best["rank"],
                "support_count": best["support_count"],
                "threads": best["threads"],
            }

    final_covered = any(abs(offset) <= public["attempts"][-1]["R"] for offset in target_offsets.values())
    final_attempt = attempt_records[-1]
    final_found_ranks = [
        {"which": label, **rank_record}
        for label, rank_record in final_attempt["full_target_ranks"].items()
        if rank_record["found"]
    ]
    best_final_full_rank = None
    if final_found_ranks:
        best_final_full_rank = sorted(final_found_ranks, key=lambda item: item["rank"])[0]
    if first_hit is not None:
        classification = "one_factor_in_public_top_k"
    elif final_covered:
        classification = "covered_but_not_ranked_in_top_k"
    else:
        classification = "public_window_insufficient_coverage"

    return {
        "name": name,
        "N": n,
        "N_bits": n.bit_length(),
        "p": p,
        "q": q,
        "policy": public["policy"],
        "threads": public["threads"],
        "radii": public["radii"],
        "top_k": public["top_k"],
        "first_hit": first_hit,
        "best_final_full_rank": best_final_full_rank,
        "classification": classification,
        "attempts": attempt_records,
    }


def write_summary(records: list[dict[str, Any]]) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "audit_summary.json").write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Adaptive Support V2 Audit Summary",
        "",
        "Public policy: adaptive public radii, threads `(2, 3, 5)`, rank by support count then proximity.",
        f"Public radii: {PUBLIC_RADII}",
        f"Top-K per radius: {PUBLIC_TOP_K}",
        "",
        "Public runner receives only `N`. Private audit uses `p/q` only after public output is frozen.",
        "",
        "| case | bits | final coverage | classification | first hit R | first hit | rank | support | best final full rank |",
        "| --- | ---: | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]

    for record in records:
        final = record["attempts"][-1]["covered_by_R"]
        hit = record["first_hit"]
        if hit is None:
            full_rank = record["best_final_full_rank"]["rank"] if record["best_final_full_rank"] else "-"
            lines.append(
                f"| {record['name']} | {record['N_bits']} | {'yes' if final else 'no'} | "
                f"{record['classification']} | - | - | - | - | {full_rank} |"
            )
        else:
            full_rank = record["best_final_full_rank"]["rank"] if record["best_final_full_rank"] else "-"
            lines.append(
                f"| {record['name']} | {record['N_bits']} | {'yes' if final else 'no'} | "
                f"{record['classification']} | {hit['R']} | {hit['which']} | "
                f"{hit['rank']} | {hit['support_count']} | {full_rank} |"
            )

    successes = sum(1 for record in records if record["first_hit"] is not None)
    covered_failures = sum(1 for record in records if record["classification"] == "covered_but_not_ranked_in_top_k")
    coverage_failures = sum(1 for record in records if record["classification"] == "public_window_insufficient_coverage")
    lines += [
        "",
        "## Counts",
        "",
        f"- one_factor_in_public_top_k: {successes} / {len(records)}",
        f"- covered_but_not_ranked_in_top_k: {covered_failures} / {len(records)}",
        f"- public_window_insufficient_coverage: {coverage_failures} / {len(records)}",
    ]
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    records = []
    for case in AUDIT_CASES:
        record = audit_case(case)
        records.append(record)
        hit = record["first_hit"]
        print(f"{record['name']}: {record['classification']} first_hit={hit}")
    write_summary(records)
    print(f"summary written to {OUT_ROOT / 'summary.md'}")


if __name__ == "__main__":
    main()
