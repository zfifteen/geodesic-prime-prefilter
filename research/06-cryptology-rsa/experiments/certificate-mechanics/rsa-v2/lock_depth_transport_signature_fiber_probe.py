#!/usr/bin/env python3
"""Measure lock-depth transport signature fibers on public transported rows.

This is a diagnostic calibration report. It is not a reduction evidence
surface and it is not a live resolver.

The probe asks whether a public signature made from transported zone membership,
frontier novelty, recursion-cycle state, and source/induced lock depths maps
cleanly to one transported-ledger survivor class on the current public rows.
An ambiguous fiber falsifies this signature as a sufficient transport frontier
classifier.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DEFAULT_INPUT_DIR = (
    ROOT
    / "research/06-cryptology-rsa/experiments/transported-sidecars/rsa-v2/output/transported_story_law_current"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output/lock_depth_transport_signature_fiber"
REPORT_HEADER = "This is a diagnostic calibration report. It is not a reduction evidence surface."

WEAK_SIGNATURE_FIELDS = (
    "induced_carrier_in_prefix_zone",
    "induced_carrier_in_suffix_zone",
    "frontier_new_transport_state",
    "ledger_recursive_cycle_state",
)

LOCK_DEPTH_SIGNATURE_FIELDS = WEAK_SIGNATURE_FIELDS + (
    "source_lock_carrier_d",
    "induced_lock_carrier_d",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def normalized_row(row: dict[str, Any], surface: str) -> dict[str, Any]:
    """Attach surface and survivor target without changing public fields."""
    result = dict(row)
    result["surface"] = surface
    if surface == "direct":
        result["signature_survivor"] = bool(row["ledger_effective_survivor"])
    else:
        result["signature_survivor"] = bool(row["ledger_recursive_survivor"])
    result.setdefault("ledger_recursive_cycle_state", False)
    return result


def signature(row: dict[str, Any], fields: tuple[str, ...]) -> str:
    """Return a stable public signature key."""
    parts = [f"{field}={row.get(field)}" for field in fields]
    return "|".join(parts)


def fiber_rows(rows: list[dict[str, Any]], fields: tuple[str, ...], signature_name: str) -> list[dict[str, Any]]:
    """Return one row per public signature fiber."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[signature(row, fields)].append(row)

    fibers: list[dict[str, Any]] = []
    for key, fiber in sorted(grouped.items()):
        survivor_count = sum(1 for row in fiber if row["signature_survivor"])
        nonsurvivor_count = len(fiber) - survivor_count
        surfaces = sorted({str(row["surface"]) for row in fiber})
        case_ids = sorted({str(row["case_id"]) for row in fiber})
        fibers.append(
            {
                "signature_name": signature_name,
                "signature": key,
                "row_count": len(fiber),
                "survivor_count": survivor_count,
                "nonsurvivor_count": nonsurvivor_count,
                "ambiguous": survivor_count > 0 and nonsurvivor_count > 0,
                "surfaces": surfaces,
                "case_ids": case_ids,
                "example_source_anchors": [
                    str(row["source_anchor"])
                    for row in fiber[:5]
                    if row.get("source_anchor") is not None
                ],
            }
        )
    return fibers


def summarize(
    rows: list[dict[str, Any]],
    weak_fibers: list[dict[str, Any]],
    lock_depth_fibers: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return aggregate fiber ambiguity status."""
    weak_ambiguous = [row for row in weak_fibers if row["ambiguous"]]
    lock_ambiguous = [row for row in lock_depth_fibers if row["ambiguous"]]
    if lock_ambiguous:
        finding = (
            "The lock-depth transport signature has ambiguous fibers on the current "
            "public transported rows and is falsified as a sufficient frontier classifier."
        )
    else:
        finding = (
            "The lock-depth transport signature has zero ambiguous fibers on the current "
            "public transported rows. This is diagnostic evidence for a Lock-Depth "
            "Transport Signature Sufficiency theorem target, not a resolver claim."
        )
    return {
        "diagnostic_header": REPORT_HEADER,
        "row_count": len(rows),
        "direct_row_count": sum(1 for row in rows if row["surface"] == "direct"),
        "recursive_row_count": sum(1 for row in rows if row["surface"] == "recursive"),
        "weak_signature_fields": list(WEAK_SIGNATURE_FIELDS),
        "lock_depth_signature_fields": list(LOCK_DEPTH_SIGNATURE_FIELDS),
        "weak_fiber_count": len(weak_fibers),
        "weak_ambiguous_fiber_count": len(weak_ambiguous),
        "lock_depth_fiber_count": len(lock_depth_fibers),
        "lock_depth_ambiguous_fiber_count": len(lock_ambiguous),
        "finding": finding,
    }


def markdown_report(summary: dict[str, Any], ambiguous: list[dict[str, Any]]) -> str:
    """Return a compact Markdown report."""
    lines = [
        "# Lock-Depth Transport Signature Fiber Probe",
        "",
        REPORT_HEADER,
        "",
        "## Finding",
        "",
        str(summary["finding"]),
        "",
        "## Aggregate",
        "",
        f"- rows: `{summary['row_count']}`",
        f"- direct rows: `{summary['direct_row_count']}`",
        f"- recursive rows: `{summary['recursive_row_count']}`",
        f"- weak ambiguous fibers: `{summary['weak_ambiguous_fiber_count']}`",
        f"- lock-depth ambiguous fibers: `{summary['lock_depth_ambiguous_fiber_count']}`",
        "",
        "## Ambiguous Lock-Depth Fibers",
        "",
    ]
    if not ambiguous:
        lines.append("None on this diagnostic surface.")
    for row in ambiguous:
        lines.extend(
            [
                f"- `{row['signature']}`",
                f"  - rows: `{row['row_count']}`",
                f"  - survivor/nonsurvivor: `{row['survivor_count']}` / `{row['nonsurvivor_count']}`",
                f"  - cases: `{', '.join(row['case_ids'])}`",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def run(input_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Run the fiber probe from existing transported story-law rows."""
    direct_rows = [
        normalized_row(row, "direct")
        for row in read_jsonl(input_dir / "story_law_rows.jsonl")
    ]
    recursive_rows = [
        normalized_row(row, "recursive")
        for row in read_jsonl(input_dir / "recursive_rows.jsonl")
    ]
    rows = direct_rows + recursive_rows
    weak_fibers = fiber_rows(rows, WEAK_SIGNATURE_FIELDS, "weak_zone_frontier_signature")
    lock_depth_fibers = fiber_rows(
        rows,
        LOCK_DEPTH_SIGNATURE_FIELDS,
        "lock_depth_transport_signature",
    )
    return rows, weak_fibers, lock_depth_fibers, summarize(rows, weak_fibers, lock_depth_fibers)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Measure lock-depth transport signature fiber ambiguity."
    )
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the diagnostic fiber probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _rows, weak_fibers, lock_depth_fibers, summary = run(args.input_dir)
    ambiguous = [row for row in lock_depth_fibers if row["ambiguous"]]
    write_jsonl(args.output_dir / "weak_signature_fibers.jsonl", weak_fibers)
    write_jsonl(args.output_dir / "signature_fibers.jsonl", lock_depth_fibers)
    write_jsonl(args.output_dir / "ambiguous_fibers.jsonl", ambiguous)
    write_json(args.output_dir / "summary.json", summary)
    (args.output_dir / "summary.md").write_text(
        markdown_report(summary, ambiguous),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
