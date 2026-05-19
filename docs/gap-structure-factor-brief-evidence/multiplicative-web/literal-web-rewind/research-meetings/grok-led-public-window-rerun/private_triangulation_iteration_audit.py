#!/usr/bin/env python3
"""Private audit for the 10-iteration triangulated-distance runner.

The public policy receives only N. This script uses p/q only to construct
benchmark semiprimes and to score frozen public distance nominations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_triangulation_policy import TOP_K, nominate_distances

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_triangulated_distance_v1"

AUDIT_CASES: tuple[dict[str, Any], ...] = (
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
    {"name": "continuation_00_131101x144203", "p": 131101, "q": 144203},
    {"name": "continuation_01_1048583x1153441", "p": 1048583, "q": 1153441},
)


def audit_public_result(public: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    p_value = case["p"]
    q_value = case["q"]
    targets = {p_value: "p", q_value: "q"}
    hit = None
    for rank, row in enumerate(public["top_distances"], start=1):
        label = targets.get(row["distance"])
        if label is None:
            continue
        hit = {
            "which": label,
            "distance": row["distance"],
            "rank": rank,
            "score": row["score"],
            "left_threads": row["left_threads"],
            "right_threads": row["right_threads"],
            "shared_threads": row["shared_threads"],
            "union_threads": row["union_threads"],
        }
        break

    covered = public["R"] >= min(p_value, q_value)
    if hit is not None:
        classification = "one_factor_in_public_top_k"
    elif covered:
        classification = "covered_but_not_ranked_in_top_k"
    else:
        classification = "public_window_insufficient_coverage"

    return {
        "name": case["name"],
        "N": public["N"],
        "N_bits": public["N_bits"],
        "p": p_value,
        "q": q_value,
        "iteration": public["iteration"],
        "mode": public["mode"],
        "R": public["R"],
        "threads": public["threads"],
        "top_k": public["top_k"],
        "covered": covered,
        "hit": hit,
        "classification": classification,
        "public_cost": public["cost"],
    }


def write_public_result(iteration: int, case_name: str, public: dict[str, Any]) -> None:
    out_dir = OUT_ROOT / "public_frozen" / f"iteration_{iteration:02d}" / case_name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "public_result.json").write_text(
        json.dumps(public, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_summary(iteration_records: list[dict[str, Any]], stop: dict[str, Any]) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "iterations.json").write_text(
        json.dumps(iteration_records, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT_ROOT / "stop.json").write_text(
        json.dumps(stop, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Triangulated Distance V1 Iteration Audit",
        "",
        "Public method: rank absolute distances by two-sided small-thread triangulation.",
        f"Top-K per public result: {TOP_K}",
        "",
        "Stop conditions:",
        "",
        "1. Stop when an iteration places `p` or `q` in the public top-K for every benchmark case.",
        "2. Stop after 10 failed iterations.",
        "",
        "| iteration | mode | R | threads | successes | covered failures | coverage failures | status |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for record in iteration_records:
        lines.append(
            f"| {record['iteration']} | {record['mode']} | {record['R']} | {record['thread_count']} | "
            f"{record['success_count']} | {record['covered_failure_count']} | "
            f"{record['coverage_failure_count']} | {record['status']} |"
        )

    lines += [
        "",
        "## Stop",
        "",
        f"`{stop['status']}` at iteration `{stop['iteration']}`.",
        "",
        "## Final Iteration Case Results",
        "",
        "| case | classification | hit | rank | R | threads |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in iteration_records[-1]["cases"]:
        hit = row["hit"]
        if hit:
            lines.append(
                f"| {row['name']} | {row['classification']} | {hit['which']}={hit['distance']} | "
                f"{hit['rank']} | {row['R']} | {len(row['threads'])} |"
            )
        else:
            lines.append(
                f"| {row['name']} | {row['classification']} | - | - | {row['R']} | {len(row['threads'])} |"
            )

    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_iterations() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    stop: dict[str, Any] | None = None

    for iteration in range(1, 11):
        case_rows = []
        for case in AUDIT_CASES:
            n_value = case["p"] * case["q"]
            public = nominate_distances(n_value, iteration)
            write_public_result(iteration, case["name"], public)
            case_rows.append(audit_public_result(public, case))

        success_count = sum(1 for row in case_rows if row["classification"] == "one_factor_in_public_top_k")
        covered_failure_count = sum(1 for row in case_rows if row["classification"] == "covered_but_not_ranked_in_top_k")
        coverage_failure_count = sum(1 for row in case_rows if row["classification"] == "public_window_insufficient_coverage")
        status = "success" if success_count == len(AUDIT_CASES) else "failed_iteration"

        record = {
            "iteration": iteration,
            "mode": case_rows[0]["mode"],
            "R": case_rows[0]["R"],
            "thread_count": len(case_rows[0]["threads"]),
            "success_count": success_count,
            "covered_failure_count": covered_failure_count,
            "coverage_failure_count": coverage_failure_count,
            "status": status,
            "cases": case_rows,
        }
        records.append(record)
        print(
            f"iteration {iteration}: {status}; successes={success_count}; "
            f"covered_failures={covered_failure_count}; coverage_failures={coverage_failure_count}"
        )

        if status == "success":
            stop = {"status": "success", "iteration": iteration}
            break

    if stop is None:
        stop = {"status": "failed_after_10_iterations", "iteration": 10}
    return records, stop


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    records, stop = run_iterations()
    write_summary(records, stop)
    print(f"stop={stop['status']} iteration={stop['iteration']}")
    print(f"summary written to {OUT_ROOT / 'summary.md'}")


if __name__ == "__main__":
    main()
