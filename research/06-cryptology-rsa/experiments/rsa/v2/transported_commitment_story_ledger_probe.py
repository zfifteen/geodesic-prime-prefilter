#!/usr/bin/env python3
"""Emit story-conflict diagnostics over transported exclusion-ledger rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "transported_commitment_story_ledger_v1"
DEFAULT_INPUT_DIR = THIS_DIR / "output" / "transported_exclusion_debt"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "transported_commitment_story_ledger"

EXPECTED_COUNTS = {
    "row_count": 512,
    "ledger_effective_survivor_count": 202,
    "recursive_row_count": 713,
    "recursive_final_survivor_count": 0,
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def required(row: dict[str, object], field: str) -> object:
    """Return one required public field or fail with a named missing field."""
    if field not in row:
        raise ValueError(f"transported ledger row missing public field: {field}")
    return row[field]


def closed_interval_contains(value: object, left: object, right: object) -> bool:
    """Return whether one decimal public coordinate lies in a closed interval."""
    coordinate = int(str(value))
    lo = min(int(str(left)), int(str(right)))
    hi = max(int(str(left)), int(str(right)))
    return lo <= coordinate <= hi


def lock_carrier_d_relation(row: dict[str, object]) -> str:
    """Compare induced and source lock depths using public row fields."""
    source = required(row, "source_lock_carrier_d")
    induced = required(row, "induced_lock_carrier_d")
    if source is None or induced is None:
        return "missing"
    source_d = int(source)
    induced_d = int(induced)
    if induced_d < source_d:
        return "lower"
    if induced_d == source_d:
        return "equal"
    return "higher"


def transported_zone(row: dict[str, object]) -> str:
    """Locate the induced carrier in the transported source commitment zones."""
    induced = required(row, "induced_carrier_value")
    if induced is None:
        return "outside"
    in_prefix = closed_interval_contains(
        induced,
        required(row, "transported_prefix_lo"),
        required(row, "transported_prefix_hi"),
    )
    in_suffix = closed_interval_contains(
        induced,
        required(row, "transported_suffix_lo"),
        required(row, "transported_suffix_hi"),
    )
    if in_prefix:
        return "prefix"
    if in_suffix:
        return "suffix"
    return "outside"


def induced_event_kind(row: dict[str, object], zone: str) -> str:
    """Name the induced public story event located by the transported zones."""
    if required(row, "induced_carrier_value") is not None and zone != "outside":
        return "carrier_lock"
    if bool(required(row, "induced_threat_before_transported_deadline")):
        return "lower_threat"
    if bool(required(row, "induced_threat_in_committed_zone")):
        return "lower_threat"
    return "reset"


def induced_event_value(row: dict[str, object], event_kind: str) -> object:
    """Return the public coordinate attached to one induced story event."""
    if event_kind == "carrier_lock":
        return required(row, "induced_carrier_value")
    if event_kind == "lower_threat":
        return required(row, "induced_lower_threat_value")
    return required(row, "induced_reset_endpoint")


def story_rewrite(zone: str, relation: str) -> bool:
    """Return whether an induced event rewrites a committed transported event."""
    return zone in {"prefix", "suffix"} and relation in {"lower", "equal"}


def ledger_row(source: dict[str, object], recursion_depth: int) -> dict[str, object]:
    """Return one transported commitment story-ledger diagnostic row."""
    zone = transported_zone(source)
    relation = lock_carrier_d_relation(source)
    induced_kind = induced_event_kind(source, zone)
    return {
        "case_id": required(source, "case_id"),
        "recursion_depth": recursion_depth,
        "source_anchor": required(source, "source_anchor"),
        "induced_anchor": required(source, "induced_anchor"),
        "source_event_kind": "carrier_lock",
        "source_event_value": required(source, "source_carrier_value"),
        "source_transport_image": required(source, "source_transport_carrier_image"),
        "induced_event_kind": induced_kind,
        "induced_event_value": induced_event_value(source, induced_kind),
        "transported_zone": zone,
        "lock_carrier_d_relation": relation,
        "story_rewrite": story_rewrite(zone, relation),
        "ledger_prefix_elimination": required(source, "ledger_prefix_elimination"),
        "ledger_suffix_elimination": required(source, "ledger_suffix_elimination"),
        "ledger_recursive_cycle_state": False,
        "ledger_recursive_survivor": False,
        "ledger_effective_survivor": required(source, "ledger_effective_survivor"),
        "rule_id": RULE_ID,
    }


def count_by(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    """Return deterministic value counts for one row field."""
    counts: dict[str, int] = {}
    for row in rows:
        key = str(required(row, field))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def recursive_final_survivor_count(rows: list[dict[str, object]]) -> int:
    """Return the survivor count in the final measured recursive layer."""
    if not rows:
        return 0
    final_depth = max(int(required(row, "recursion_depth")) for row in rows)
    return sum(
        1
        for row in rows
        if int(required(row, "recursion_depth")) == final_depth
        and bool(required(row, "ledger_recursive_survivor"))
    )


def divergence_rows(summary: dict[str, object]) -> list[dict[str, object]]:
    """Return named count divergences against the experiment contract."""
    field_sources = {
        "row_count": "ledger_rows",
        "ledger_effective_survivor_count": "ledger_effective_survivor",
        "recursive_row_count": "recursive_rows",
        "recursive_final_survivor_count": "ledger_recursive_survivor",
    }
    divergences = []
    for field, expected in EXPECTED_COUNTS.items():
        observed = int(required(summary, field))
        if observed != expected:
            divergences.append(
                {
                    "field": field,
                    "expected": expected,
                    "observed": observed,
                    "public_story_field": field_sources[field],
                }
            )
    return divergences


def summarize(
    ledger_rows: list[dict[str, object]],
    recursive_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return falsification-oriented story-ledger counts."""
    summary: dict[str, object] = {
        "rule_id": RULE_ID,
        "row_count": len(ledger_rows),
        "recursive_row_count": len(recursive_rows),
        "ledger_effective_survivor_count": sum(
            1 for row in ledger_rows if bool(required(row, "ledger_effective_survivor"))
        ),
        "recursive_final_survivor_count": recursive_final_survivor_count(recursive_rows),
        "story_rewrite_count": sum(1 for row in ledger_rows if bool(required(row, "story_rewrite"))),
        "transported_zone_counts": count_by(ledger_rows, "transported_zone"),
        "lock_carrier_d_relation_counts": count_by(ledger_rows, "lock_carrier_d_relation"),
        "induced_event_kind_counts": count_by(ledger_rows, "induced_event_kind"),
        "ledger_prefix_elimination_count": sum(
            1 for row in ledger_rows if bool(required(row, "ledger_prefix_elimination"))
        ),
        "ledger_suffix_elimination_count": sum(
            1 for row in ledger_rows if bool(required(row, "ledger_suffix_elimination"))
        ),
    }
    divergences = divergence_rows(summary)
    summary["expected_counts"] = EXPECTED_COUNTS
    summary["falsification_status"] = "passed" if not divergences else "failed"
    summary["divergences"] = divergences
    return summary


def run_probe(
    input_dir: Path,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Run the story-conflict diagnostic over existing transported ledger rows."""
    debt_rows = read_jsonl(input_dir / "debt_rows.jsonl")
    recursive_rows = read_jsonl(input_dir / "recursive_rows.jsonl")
    ledger_rows = [ledger_row(row, 0) for row in debt_rows]
    return ledger_rows, summarize(ledger_rows, recursive_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Emit transported commitment story-ledger diagnostics."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing transported_exclusion_debt rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for ledger_rows.jsonl and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary = run_probe(args.input_dir)
    write_jsonl(args.output_dir / "ledger_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
