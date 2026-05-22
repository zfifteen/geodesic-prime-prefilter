"""Probe batch modular factor closure for integer-start PGS chambers.

Classical divisibility and next-prime calls are benchmark/audit instruments here.
They do not select PGS-native endpoints.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from sympy import nextprime


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))


WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})
DEFAULT_OUTPUT_DIR = ROOT / "research" / "06-cryptology-rsa" / "output" / "batch_modular_factor_closure_probe"


def write_json(record: dict[str, object], path: Path) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    """Write LF-terminated CSV rows."""
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def wheel_open_offsets(n: int, candidate_bound: int) -> list[int]:
    """Return wheel-open offsets to the right of one integer start."""
    return [
        offset
        for offset in range(1, int(candidate_bound) + 1)
        if (int(n) + offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30
    ]


def witness_for_offset(n: int, offset: int, factor_bound: int) -> int | None:
    """Return the first benchmark divisibility witness within the bound."""
    candidate = int(n) + int(offset)
    max_factor = min(int(factor_bound), candidate - 1)
    for factor in range(2, max_factor + 1):
        if candidate % factor == 0:
            return factor
    return None


def closure_row(
    n: int,
    candidate_bound: int,
    factor_bound: int,
    audit: bool,
) -> dict[str, object]:
    """Return one closure probe row."""
    offsets = wheel_open_offsets(n, candidate_bound)
    witnesses = {
        offset: witness
        for offset in offsets
        if (witness := witness_for_offset(n, offset, factor_bound)) is not None
    }
    closed_offsets = sorted(witnesses)
    open_offsets = [offset for offset in offsets if offset not in witnesses]

    # Classical nextprime is an audit label for measuring closure, not inference.
    audit_q = int(nextprime(n)) if audit else None
    audit_gap = None if audit_q is None else audit_q - int(n)
    pre_q_offsets = [
        offset for offset in offsets
        if audit_gap is not None and offset < audit_gap
    ]
    pre_q_closed = [
        offset for offset in pre_q_offsets
        if offset in witnesses
    ]
    q_closed = audit_gap in witnesses if audit_gap is not None else None
    first_open_offset = open_offsets[0] if open_offsets else None
    return {
        "n": str(n),
        "candidate_bound": int(candidate_bound),
        "factor_bound": int(factor_bound),
        "wheel_open_count": len(offsets),
        "closed_count": len(closed_offsets),
        "open_count": len(open_offsets),
        "closure_rate": 0.0 if not offsets else len(closed_offsets) / len(offsets),
        "first_open_offset": first_open_offset,
        "audit_q": None if audit_q is None else str(audit_q),
        "audit_gap": audit_gap,
        "pre_q_open_count": len(pre_q_offsets) - len(pre_q_closed),
        "pre_q_all_closed": None if audit_gap is None else len(pre_q_offsets) == len(pre_q_closed),
        "q_closed": q_closed,
        "first_open_matches_q": None if audit_gap is None else first_open_offset == audit_gap,
    }


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return summary metrics."""
    audited = [row for row in rows if row["audit_gap"] is not None]
    return {
        "rows": len(rows),
        "audited_rows": len(audited),
        "pre_q_all_closed_count": sum(1 for row in audited if row["pre_q_all_closed"]),
        "q_closed_count": sum(1 for row in audited if row["q_closed"]),
        "first_open_matches_q_count": sum(1 for row in audited if row["first_open_matches_q"]),
        "average_closure_rate": (
            0.0 if not rows else sum(float(row["closure_rate"]) for row in rows) / len(rows)
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the probe CLI."""
    parser = argparse.ArgumentParser(description="Probe batch modular factor closure.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--candidate-bound", type=int, default=4096)
    parser.add_argument("--factor-bound", type=int, default=10000)
    parser.add_argument("--min-exponent", type=int, default=3)
    parser.add_argument("--max-exponent", type=int, default=18)
    parser.add_argument("--huge-exponent", type=int, default=1233)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the closure probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        closure_row(
            10**exponent,
            args.candidate_bound,
            args.factor_bound,
            audit=True,
        )
        for exponent in range(args.min_exponent, args.max_exponent + 1)
    ]
    rows.append(
        closure_row(
            10**args.huge_exponent,
            args.candidate_bound,
            args.factor_bound,
            audit=False,
        )
    )

    summary = summarize(rows)
    write_json({"rows": rows}, args.output_dir / "rows.json")
    write_json(summary, args.output_dir / "summary.json")
    write_csv(rows, args.output_dir / "rows.csv")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
