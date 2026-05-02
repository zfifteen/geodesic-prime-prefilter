#!/usr/bin/env python3
"""Side probe for reciprocal PGS chamber lock on RSA survivor rows."""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON_SRC = REPO_ROOT / "src" / "python"
sys.path.insert(0, str(PYTHON_SRC))

from run_inference_elimination_probe import (
    RULE_X_CANDIDATE_BOUND,
    previous_pgs_endpoint,
    rule_x_endpoint_from_anchor,
)


SURVIVOR_PATH = Path("experiments/rsa/inference_elimination_survivors.jsonl")
DETAIL_PATH = Path("experiments/rsa/reciprocal_chamber_lock_details.csv")
SUMMARY_PATH = Path("experiments/rsa/reciprocal_chamber_lock_summary.csv")
MAX_ROUNDS = 4


@dataclass(frozen=True)
class LockStep:
    side: str
    value: int
    anchor: int | None
    endpoint: int | None
    locked: bool


@dataclass(frozen=True)
class LockResult:
    case_id: str
    rank: int
    n: int
    d: int
    q_floor: int
    rounds_locked: int
    pair_product_error: int
    final_p: int
    final_q: int
    signature: str


def read_survivors(path: Path) -> dict[str, list[dict[str, object]]]:
    """Read survivor rows emitted by the inference probe."""
    rows_by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    with path.open() as handle:
        for line in handle:
            row = json.loads(line)
            rows_by_case[str(row["case_id"])].append(row)
    for rows in rows_by_case.values():
        rows.sort(key=lambda row: int(row["rank"]))
    return dict(rows_by_case)


def lock_step(side: str, value: int) -> LockStep:
    """Return one chamber lock step for a value."""
    anchor = previous_pgs_endpoint(value)
    if anchor is None:
        return LockStep(side, value, None, None, False)
    endpoint = rule_x_endpoint_from_anchor(anchor)
    return LockStep(side, value, anchor, endpoint, endpoint == value)


def reciprocal_lock(row: dict[str, object], max_rounds: int) -> LockResult:
    """Apply reciprocal chamber lock to one survivor row."""
    case_id = str(row["case_id"])
    rank = int(row["rank"])
    n = int(row["N"])
    p_value = int(row["d"])
    q_value = int(row["q_floor"])
    signature_parts: list[str] = []
    rounds_locked = 0

    for round_index in range(1, max_rounds + 1):
        p_step = lock_step("p", p_value)
        q_step = lock_step("q", q_value)
        signature_parts.append(
            f"{round_index}:p={p_step.endpoint}:q={q_step.endpoint}"
        )
        if not (p_step.locked and q_step.locked):
            break
        next_p = int(n // q_step.endpoint)
        next_q = int(n // p_step.endpoint)
        if next_p != p_step.endpoint or next_q != q_step.endpoint:
            break
        rounds_locked = round_index
        p_value = p_step.endpoint
        q_value = q_step.endpoint

    return LockResult(
        case_id=case_id,
        rank=rank,
        n=n,
        d=int(row["d"]),
        q_floor=int(row["q_floor"]),
        rounds_locked=rounds_locked,
        pair_product_error=abs(n - p_value * q_value),
        final_p=p_value,
        final_q=q_value,
        signature=";".join(signature_parts),
    )


def write_detail(rows: list[LockResult], path: Path) -> None:
    """Write detail rows with LF line endings."""
    fieldnames = [
        "case_id",
        "rank",
        "N",
        "d",
        "q_floor",
        "rounds_locked",
        "pair_product_error",
        "final_p",
        "final_q",
        "signature",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "case_id": row.case_id,
                    "rank": row.rank,
                    "N": row.n,
                    "d": row.d,
                    "q_floor": row.q_floor,
                    "rounds_locked": row.rounds_locked,
                    "pair_product_error": row.pair_product_error,
                    "final_p": row.final_p,
                    "final_q": row.final_q,
                    "signature": row.signature,
                }
            )


def summarize(rows: list[LockResult]) -> list[dict[str, object]]:
    """Summarize lock results by case."""
    rows_by_case: dict[str, list[LockResult]] = defaultdict(list)
    for row in rows:
        rows_by_case[row.case_id].append(row)

    summaries: list[dict[str, object]] = []
    for case_id, case_rows in sorted(rows_by_case.items()):
        best_rounds = max(row.rounds_locked for row in case_rows)
        exact_locked = [
            row
            for row in case_rows
            if row.rounds_locked == best_rounds and row.pair_product_error == 0
        ]
        summaries.append(
            {
                "case_id": case_id,
                "survivors_in": len(case_rows),
                "best_rounds_locked": best_rounds,
                "exact_locked_survivors": len(exact_locked),
                "best_rank": "" if not exact_locked else min(row.rank for row in exact_locked),
                "recursive_survivors": sum(
                    1 for row in case_rows if row.rounds_locked == best_rounds
                ),
            }
        )
    return summaries


def write_summary(rows: list[dict[str, object]], path: Path) -> None:
    """Write summary rows with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    rows_by_case = read_survivors(SURVIVOR_PATH)
    details = [
        reciprocal_lock(row, MAX_ROUNDS)
        for rows in rows_by_case.values()
        for row in rows
    ]
    summaries = summarize(details)
    write_detail(details, DETAIL_PATH)
    write_summary(summaries, SUMMARY_PATH)

    print(
        "case_id,survivors_in,best_rounds_locked,exact_locked_survivors,"
        "best_rank,recursive_survivors"
    )
    for row in summaries:
        print(
            f"{row['case_id']},{row['survivors_in']},{row['best_rounds_locked']},"
            f"{row['exact_locked_survivors']},{row['best_rank']},"
            f"{row['recursive_survivors']}"
        )
    print(f"wrote {DETAIL_PATH}")
    print(f"wrote {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
