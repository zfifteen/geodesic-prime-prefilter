#!/usr/bin/env python3
"""Downstream audit for the toy RSA inference-elimination probe."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path


SURVIVOR_PATH = Path("experiments/rsa/inference_elimination_survivors.jsonl")
SUMMARY_PATH = Path("experiments/rsa/inference_elimination_probe.csv")
AUDIT_PATH = Path("experiments/rsa/inference_elimination_audit.csv")


@dataclass(frozen=True)
class AuditCase:
    case_id: str
    p: int
    q: int

    @property
    def n(self) -> int:
        return self.p * self.q


AUDIT_CASES = (
    AuditCase("rsa_like_60bit_skew_14", 805289981, 805322753),
    AuditCase("rsa_like_80bit_skew_16", 824633655283, 824633786381),
    AuditCase("rsa_like_100bit_skew_18", 844424929869767, 844424930394187),
    AuditCase("rsa_like_125bit_skew_18", 6917529027640819673, 6917529027641344003),
    AuditCase("rsa_like_150bit_skew_20", 28334198897217870233539, 28334198897217872330779),
)


def read_survivors(path: Path) -> dict[str, list[dict[str, int | str]]]:
    """Read ranked survivors emitted by the inference script."""
    survivors: dict[str, list[dict[str, int | str]]] = {}
    with path.open() as handle:
        for line in handle:
            row = json.loads(line)
            case_id = str(row["case_id"])
            survivors.setdefault(case_id, []).append(row)
    for rows in survivors.values():
        rows.sort(key=lambda row: int(row["rank"]))
    return survivors


def read_summary_status(path: Path) -> dict[str, str]:
    """Read completion status emitted by the inference script."""
    with path.open() as handle:
        return {
            str(row["case_id"]): str(row["status"])
            for row in csv.DictReader(handle)
        }


def audit_case(
    case: AuditCase,
    survivors: list[dict[str, int | str]],
    status: str,
) -> dict[str, object]:
    """Audit whether hidden factors survived and where certification would stop."""
    hidden = {case.p, case.q}
    p_survived = any(int(row["d"]) == case.p for row in survivors)
    q_survived = any(int(row["d"]) == case.q for row in survivors)

    factor_rank = None
    gcd_checks = None
    for row in survivors:
        rank = int(row["rank"])
        d = int(row["d"])
        if d in hidden:
            factor_rank = rank
            if math.gcd(case.n, d) not in (1, case.n):
                gcd_checks = rank
            break

    return {
        "case_id": case.case_id,
        "N": case.n,
        "bits": case.n.bit_length(),
        "p_hidden": case.p,
        "q_hidden": case.q,
        "status": status,
        "survivors": len(survivors),
        "p_survived": int(p_survived),
        "q_survived": int(q_survived),
        "false_rejection": "" if status != "completed" else int(not (p_survived or q_survived)),
        "factor_survivor_rank": "" if factor_rank is None else factor_rank,
        "gcd_checks_before_factor": "" if gcd_checks is None else gcd_checks,
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    """Write audit rows with LF line endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    survivors_by_case = read_survivors(SURVIVOR_PATH)
    status_by_case = read_summary_status(SUMMARY_PATH)
    rows = [
        audit_case(
            case,
            survivors_by_case.get(case.case_id, []),
            status_by_case.get(case.case_id, "missing_inference_summary"),
        )
        for case in AUDIT_CASES
    ]
    write_csv(rows, AUDIT_PATH)

    print("case_id,survivors,false_rejection,factor_rank,gcd_checks_before_factor")
    for row in rows:
        print(
            f"{row['case_id']},{row['survivors']},{row['false_rejection']},"
            f"{row['factor_survivor_rank']},{row['gcd_checks_before_factor']}"
        )
    print(f"wrote {AUDIT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
