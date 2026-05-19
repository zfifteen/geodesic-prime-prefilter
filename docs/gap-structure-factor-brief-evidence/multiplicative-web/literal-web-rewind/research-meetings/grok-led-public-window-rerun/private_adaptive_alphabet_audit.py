#!/usr/bin/env python3
"""Private audit for adaptive alphabet v3.

The public runner receives only N. This audit uses benchmark factors only after
the frozen public nomination has been emitted.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_adaptive_alphabet_runner import (
    public_adaptive_alphabet_nominate,
)
from public_alphabet_policy import PUBLIC_TOP_K, ranked_offsets_at_rung

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_adaptive_alphabet_v3"

AUDIT_CASES: list[dict[str, Any]] = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
    {"name": "continuation_00_131101x144203", "p": 131101, "q": 144203},
    {"name": "continuation_01_1048583x1153441", "p": 1048583, "q": 1153441},
]


def hit_in_top(attempt: dict[str, Any], target_offset: int) -> dict[str, Any]:
    for rank, item in enumerate(attempt["top_nominated"], start=1):
        if item["offset"] == target_offset:
            return {
                "found": True,
                "rank": rank,
                "support_count": item["support_count"],
                "signature_count": item["signature_count"],
                "signature_weight": item["signature_weight"],
                "threads": item["threads"],
            }
    return {
        "found": False,
        "rank": None,
        "support_count": None,
        "signature_count": None,
        "signature_weight": None,
        "threads": [],
    }


def audit_case(case: dict[str, Any]) -> dict[str, Any]:
    p = case["p"]
    q = case["q"]
    n = p * q
    name = case["name"]

    public = public_adaptive_alphabet_nominate(n)
    public_dir = OUT_ROOT / "public_frozen" / name
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "public_result.json").write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    target_offsets = {"p": p, "-p": -p, "q": q, "-q": -q}
    first_hit = None
    attempt_records = []

    for attempt in public["attempts"]:
        top_hits = {
            label: hit_in_top(attempt, offset)
            for label, offset in target_offsets.items()
        }
        full_attempt = ranked_offsets_at_rung(n, attempt["R"], tuple(attempt["threads"]), None)
        rank_by_offset = {
            item["offset"]: (rank, item)
            for rank, item in enumerate(full_attempt["top_nominated"], start=1)
        }
        full_ranks = {}
        for label, offset in target_offsets.items():
            ranked_item = rank_by_offset.get(offset)
            if ranked_item is None:
                full_ranks[label] = {
                    "found": False,
                    "rank": None,
                    "support_count": None,
                    "signature_count": None,
                    "signature_weight": None,
                    "threads": [],
                    "total_nominated": full_attempt["nominated_count"],
                }
                continue
            rank, item = ranked_item
            full_ranks[label] = {
                "found": True,
                "rank": rank,
                "support_count": item["support_count"],
                "signature_count": item["signature_count"],
                "signature_weight": item["signature_weight"],
                "threads": item["threads"],
                "total_nominated": full_attempt["nominated_count"],
            }
        hits = [
            {"which": label, **record}
            for label, record in top_hits.items()
            if record["found"]
        ]
        if hits and first_hit is None:
            first_hit = sorted(hits, key=lambda item: item["rank"])[0] | {
                "R": attempt["R"],
                "thread_count": attempt["thread_count"],
            }

        attempt_records.append({
            "R": attempt["R"],
            "thread_count": attempt["thread_count"],
            "threads": attempt["threads"],
            "covered_by_R": any(abs(offset) <= attempt["R"] for offset in target_offsets.values()),
            "top_hits": top_hits,
            "full_ranks": full_ranks,
            "nominated_count": attempt["nominated_count"],
            "cost": attempt["cost"],
        })

    final_found = [
        {"which": label, **rank_record}
        for label, rank_record in attempt_records[-1]["full_ranks"].items()
        if rank_record["found"]
    ]
    best_final_full_rank = None
    if final_found:
        best_final_full_rank = sorted(final_found, key=lambda item: item["rank"])[0]

    final_covered = attempt_records[-1]["covered_by_R"]
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
        "# Adaptive Alphabet V3 Audit Summary",
        "",
        "Public policy: adaptive public radius, adaptive public thread alphabet, rank by support count, signature rarity, signature weight, then proximity.",
        f"Top-K per rung: {PUBLIC_TOP_K}",
        "",
        "Public runner receives only `N`. Private audit uses `p/q` only after public output is frozen.",
        "",
        "| case | bits | classification | first hit R | threads | hit | rank | support | signature count | best final full rank |",
        "| --- | ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for record in records:
        hit = record["first_hit"]
        final_rank = record["best_final_full_rank"]["rank"] if record["best_final_full_rank"] else "-"
        if hit is None:
            lines.append(
                f"| {record['name']} | {record['N_bits']} | {record['classification']} | - | - | - | - | - | - | {final_rank} |"
            )
        else:
            lines.append(
                f"| {record['name']} | {record['N_bits']} | {record['classification']} | "
                f"{hit['R']} | {hit['thread_count']} | {hit['which']} | {hit['rank']} | "
                f"{hit['support_count']} | {hit['signature_count']} | {final_rank} |"
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
        print(f"{record['name']}: {record['classification']} first_hit={record['first_hit']}")
    write_summary(records)
    print(f"summary written to {OUT_ROOT / 'summary.md'}")


if __name__ == "__main__":
    main()
