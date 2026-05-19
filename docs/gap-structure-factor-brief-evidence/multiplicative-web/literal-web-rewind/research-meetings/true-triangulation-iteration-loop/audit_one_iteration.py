#!/usr/bin/env python3
"""Run one true triangulation iteration and private post-freeze audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from public_loop_policy import load_spec, public_nominate

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output"

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
        hit = {
            "which": which,
            "distance": row["distance"],
            "rank": rank,
            "score": row["score"],
            "left_source_count": row["left_source_count"],
            "right_source_count": row["right_source_count"],
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
        "iteration": public["iteration"],
        "radius": public["radius"],
        "covered": covered,
        "classification": classification,
        "hit": hit,
        "public_cost": public["public_cost"],
    }


def write_summary(iteration_dir: Path, spec: dict[str, Any], records: list[dict[str, Any]]) -> None:
    success_count = sum(1 for row in records if row["classification"] == "one_factor_in_public_top_k")
    covered_failure_count = sum(1 for row in records if row["classification"] == "covered_but_not_ranked_in_top_k")
    coverage_failure_count = sum(1 for row in records if row["classification"] == "public_window_insufficient_coverage")
    status = "success" if success_count == len(records) else "failed_iteration"

    summary = {
        "iteration": spec["iteration"],
        "status": status,
        "success_count": success_count,
        "covered_failure_count": covered_failure_count,
        "coverage_failure_count": coverage_failure_count,
        "spec": spec,
        "cases": records,
    }
    (iteration_dir / "audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        f"# Iteration {spec['iteration']} Audit",
        "",
        f"Status: `{status}`",
        "",
        f"Radius: `{spec['radius']}`",
        f"Small primes: `{spec['small_primes']}`",
        f"Residual limit: `{spec['residual_limit']}`",
        f"Score mode: `{spec['score_mode']}`",
        f"Top-K: `{spec['top_k']}`",
        "",
        "| case | classification | hit | rank | source rows | vote targets |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in records:
        hit = row["hit"]
        hit_label = "-" if hit is None else f"{hit['which']}={hit['distance']}"
        rank = "-" if hit is None else str(hit["rank"])
        lines.append(
            f"| {row['name']} | {row['classification']} | {hit_label} | {rank} | "
            f"{row['public_cost']['source_rows']} | {row['public_cost']['vote_targets']} |"
        )
    (iteration_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"iteration {spec['iteration']}: {status}; successes={success_count}; covered_failures={covered_failure_count}; coverage_failures={coverage_failure_count}")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: audit_one_iteration.py spec.json")
    spec_path = Path(sys.argv[1])
    spec = load_spec(spec_path)
    iteration_dir = OUT_ROOT / f"iteration_{int(spec['iteration']):02d}"
    public_dir = iteration_dir / "public_frozen"
    public_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for case in CASES:
        n = case["p"] * case["q"]
        public = public_nominate(n, spec)
        case_dir = public_dir / case["name"]
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "public_result.json").write_text(
            json.dumps(public, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        records.append(audit_public(public, case))

    write_summary(iteration_dir, spec, records)


if __name__ == "__main__":
    main()
