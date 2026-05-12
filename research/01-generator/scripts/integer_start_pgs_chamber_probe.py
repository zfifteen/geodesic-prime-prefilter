"""Probe PGS chamber resolution from arbitrary integer starts."""

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

from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_probe_certificate,
)


DEFAULT_OUTPUT_DIR = Path("output/integer_start_pgs_chamber_probe")


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


def probe_start(n: int, candidate_bound: int | None) -> dict[str, object]:
    """Probe one integer start with audit-only nextprime labels."""
    q = int(nextprime(int(n)))
    true_gap = q - int(n)
    bound = int(candidate_bound) if candidate_bound is not None else true_gap
    certificate = pgs_probe_certificate(int(n), bound)
    resolved_q = None if certificate is None else int(certificate["q"])
    return {
        "n": int(n),
        "true_q_for_audit_only": q,
        "true_gap_for_audit_only": true_gap,
        "candidate_bound": bound,
        "resolved": certificate is not None,
        "resolved_q": resolved_q,
        "audit_passed": resolved_q == q,
        "gap_offset": None if certificate is None else int(certificate["gap_offset"]),
    }


def decade_starts(min_exponent: int, max_exponent: int) -> list[int]:
    """Return integer starts 10^k."""
    return [10**exponent for exponent in range(min_exponent, max_exponent + 1)]


def consecutive_starts(start: int, count: int) -> list[int]:
    """Return consecutive integer starts from one point."""
    return [int(start) + offset for offset in range(int(count))]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return a compact probe summary."""
    resolved_count = sum(1 for row in rows if bool(row["resolved"]))
    audit_passed = sum(1 for row in rows if bool(row["audit_passed"]))
    return {
        "starts": len(rows),
        "resolved": resolved_count,
        "audit_passed": audit_passed,
        "audit_failed": len(rows) - audit_passed,
        "all_passed": audit_passed == len(rows),
        "max_true_gap_for_audit_only": max(
            int(row["true_gap_for_audit_only"]) for row in rows
        ) if rows else 0,
    }


def build_parser() -> argparse.ArgumentParser:
    """Build the probe CLI."""
    parser = argparse.ArgumentParser(description="Probe integer-start PGS chambers.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-exponent", type=int, default=1)
    parser.add_argument("--max-exponent", type=int, default=18)
    parser.add_argument("--start", type=int, default=10_000)
    parser.add_argument("--count", type=int, default=256)
    parser.add_argument("--candidate-bound", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the integer-start chamber probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    starts = decade_starts(args.min_exponent, args.max_exponent)
    starts.extend(consecutive_starts(args.start, args.count))
    rows = [probe_start(n, args.candidate_bound) for n in starts if int(n) >= 5]
    summary = summarize(rows)

    write_json({"rows": rows}, args.output_dir / "rows.json")
    write_json(summary, args.output_dir / "summary.json")
    write_csv(rows, args.output_dir / "rows.csv")

    print(json.dumps(summary, sort_keys=True))
    return 0 if bool(summary["all_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
