#!/usr/bin/env python3
"""Private audit for the public anchor-confirmed band expansion test."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_anchor_band_runner import public_anchor_band_nominate

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_anchor_band_expansion"

CASES: tuple[dict[str, Any], ...] = (
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
    {"name": "continuation_00_131101x144203", "p": 131101, "q": 144203},
    {"name": "continuation_01_1048583x1153441", "p": 1048583, "q": 1153441},
)


def audit_public(public: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    targets = {case["p"]: "p", case["q"]: "q"}
    hit = None
    for rank, row in enumerate(public["top_distances"], start=1):
        which = targets.get(row["distance"])
        if which is None:
            continue
        band_rank = 0
        target_band = (row["distance"] - 1) // public["band_width"]
        for prior in public["top_distances"][:rank]:
            if (prior["distance"] - 1) // public["band_width"] == target_band:
                band_rank += 1
        hit = {
            "which": which,
            "distance": row["distance"],
            "rank": rank,
            "band_rank": band_rank,
            "score": row["score"],
            "shared_thread_count": row["shared_thread_count"],
            "union_thread_count": row["union_thread_count"],
        }
        break

    covered = public["radius"] >= min(case["p"], case["q"])
    if hit:
        classification = "one_factor_in_public_top_k"
    elif covered:
        classification = "covered_but_not_ranked_in_top_k"
    else:
        classification = "public_window_insufficient_coverage"

    return {
        "name": case["name"],
        "N": public["N"],
        "N_bits": public["N_bits"],
        "p": case["p"],
        "q": case["q"],
        "classification": classification,
        "covered": covered,
        "hit": hit,
        "public_cost": public["public_cost"],
    }


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    public_root = OUT_ROOT / "public_frozen"
    records = []
    for case in CASES:
        n = case["p"] * case["q"]
        public = public_anchor_band_nominate(n)
        case_dir = public_root / case["name"]
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "public_result.json").write_text(
            json.dumps(public, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        record = audit_public(public, case)
        records.append(record)
        print(f"{record['name']}: {record['classification']} hit={record['hit']}")

    success_count = sum(1 for row in records if row["classification"] == "one_factor_in_public_top_k")
    covered_failure_count = sum(1 for row in records if row["classification"] == "covered_but_not_ranked_in_top_k")
    coverage_failure_count = sum(1 for row in records if row["classification"] == "public_window_insufficient_coverage")
    status = "success" if success_count == len(records) else "failed"
    summary = {
        "status": status,
        "success_count": success_count,
        "covered_failure_count": covered_failure_count,
        "coverage_failure_count": coverage_failure_count,
        "cases": records,
    }
    (OUT_ROOT / "audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Anchor-Confirmed Band Expansion Audit",
        "",
        f"Status: `{status}`",
        "",
        "| case | classification | hit | rank | band rank |",
        "| --- | --- | --- | ---: | ---: |",
    ]
    for row in records:
        hit = row["hit"]
        if hit is None:
            lines.append(f"| {row['name']} | {row['classification']} | - | - | - |")
        else:
            lines.append(
                f"| {row['name']} | {row['classification']} | {hit['which']}={hit['distance']} | "
                f"{hit['rank']} | {hit['band_rank']} |"
            )
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"status={status}; successes={success_count}; summary={OUT_ROOT / 'summary.md'}")


if __name__ == "__main__":
    main()
