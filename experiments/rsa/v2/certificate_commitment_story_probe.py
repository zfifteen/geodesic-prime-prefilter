#!/usr/bin/env python3
"""Emit public ordered commitment-story rows for PGSPG certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "certificate_commitment_story_v1"


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


def event_row(
    case_id: str,
    source_anchor: str,
    event_index: int,
    event_kind: str,
    event_offset: int,
    event_value: str,
    carrier_d_at_event: int | None,
    lock_carrier_d: int | None,
    dominates_offset_lo: int | None,
    dominates_offset_hi: int | None,
    reduced_state_before: str,
    reduced_state_after: str,
) -> dict[str, object]:
    """Return one public story event row."""
    return {
        "case_id": case_id,
        "source_anchor": source_anchor,
        "event_index": event_index,
        "event_kind": event_kind,
        "event_offset": event_offset,
        "event_value": event_value,
        "carrier_d_at_event": carrier_d_at_event,
        "lock_carrier_d": lock_carrier_d,
        "dominates_offset_lo": dominates_offset_lo,
        "dominates_offset_hi": dominates_offset_hi,
        "reduced_state_before": reduced_state_before,
        "reduced_state_after": reduced_state_after,
        "rule_id": RULE_ID,
    }


def certificate_present(row: dict[str, object], prefix: str) -> bool:
    """Return whether one prefixed certificate is present in a runner row."""
    return row.get(f"{prefix}_anchor") is not None


def certificate_story_rows(
    runner_row: dict[str, object],
    prefix: str,
) -> list[dict[str, object]]:
    """Return story rows for one prefixed PGSPG certificate."""
    case_id = str(runner_row["case_id"])
    source_anchor = str(runner_row[f"{prefix}_anchor"])
    anchor_value = int(source_anchor)
    lock_carrier_d = runner_row[f"{prefix}_lock_carrier_d"]
    carrier_d = runner_row[f"{prefix}_carrier_d"]
    event_index = 0
    rows: list[dict[str, object]] = []

    for offset in runner_row[f"{prefix}_closed_offsets_before_q"]:
        closed_offset = int(offset)
        rows.append(
            event_row(
                case_id,
                source_anchor,
                event_index,
                "closed_offset",
                closed_offset,
                str(anchor_value + closed_offset),
                None if lock_carrier_d is None else int(lock_carrier_d),
                None if lock_carrier_d is None else int(lock_carrier_d),
                closed_offset,
                closed_offset,
                "offset_open",
                "offset_closed",
            )
        )
        event_index += 1

    lock_offset = runner_row[f"{prefix}_lock_carrier_offset"]
    carrier_w = runner_row[f"{prefix}_carrier_w"]
    if lock_offset is not None and carrier_w is not None:
        carrier_offset = int(lock_offset)
        rows.append(
            event_row(
                case_id,
                source_anchor,
                event_index,
                "carrier_lock",
                carrier_offset,
                str(carrier_w),
                None if carrier_d is None else int(carrier_d),
                None if lock_carrier_d is None else int(lock_carrier_d),
                carrier_offset,
                carrier_offset,
                "carrier_unlocked",
                "carrier_locked",
            )
        )
        event_index += 1

    reset_offset = int(runner_row[f"{prefix}_gap_offset"])
    rows.append(
        event_row(
            case_id,
            source_anchor,
            event_index,
            "reset",
            reset_offset,
            str(runner_row[f"{prefix}_reset_endpoint"]),
            None if carrier_d is None else int(carrier_d),
            None if lock_carrier_d is None else int(lock_carrier_d),
            reset_offset,
            reset_offset,
            "reset_open",
            "reset_committed",
        )
    )
    event_index += 1

    threat_offset = runner_row[f"{prefix}_d_threat_offset"]
    if threat_offset is not None:
        lower_threat_offset = int(threat_offset)
        rows.append(
            event_row(
                case_id,
                source_anchor,
                event_index,
                "lower_threat",
                lower_threat_offset,
                str(anchor_value + lower_threat_offset),
                None if carrier_d is None else int(carrier_d),
                None if lock_carrier_d is None else int(lock_carrier_d),
                lower_threat_offset,
                lower_threat_offset,
                "lower_threat_absent",
                "lower_threat_present",
            )
        )
        event_index += 1

    for offset in runner_row[f"{prefix}_tail_after_reset_offsets"]:
        tail_offset = int(offset)
        rows.append(
            event_row(
                case_id,
                source_anchor,
                event_index,
                "tail",
                tail_offset,
                str(anchor_value + tail_offset),
                None if carrier_d is None else int(carrier_d),
                None if lock_carrier_d is None else int(lock_carrier_d),
                tail_offset,
                tail_offset,
                "tail_offset_open",
                "tail_offset_committed",
            )
        )
        event_index += 1

    deadline_value = str(runner_row[f"{prefix}_reset_deadline_value"])
    deadline_offset = int(deadline_value) - anchor_value
    rows.append(
        event_row(
            case_id,
            source_anchor,
            event_index,
            "deadline",
            deadline_offset,
            deadline_value,
            None if carrier_d is None else int(carrier_d),
            None if lock_carrier_d is None else int(lock_carrier_d),
            reset_offset,
            deadline_offset,
            "deadline_open",
            "deadline_committed",
        )
    )
    return rows


def story_rows_from_certificates(
    certificate_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return ordered story rows for every public certificate emitted by the runner."""
    rows: list[dict[str, object]] = []
    for runner_row in certificate_rows:
        for prefix in ("lower", "upper"):
            if certificate_present(runner_row, prefix):
                rows.extend(certificate_story_rows(runner_row, prefix))
    return rows


def summarize(
    certificate_rows: list[dict[str, object]],
    story_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return public story materialization counts."""
    certificates = {
        (str(row["case_id"]), str(row[f"{prefix}_anchor"]))
        for row in certificate_rows
        for prefix in ("lower", "upper")
        if certificate_present(row, prefix)
    }
    event_kind_counts: dict[str, int] = {}
    for row in story_rows:
        event_kind = str(row["event_kind"])
        event_kind_counts[event_kind] = event_kind_counts.get(event_kind, 0) + 1
    return {
        "rule_id": RULE_ID,
        "source_certificate_row_count": len(certificate_rows),
        "certificate_count": len(certificates),
        "story_row_count": len(story_rows),
        "event_kind_counts": event_kind_counts,
    }


def run_probe(certificate_rows_path: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Run the public commitment-story sidecar probe."""
    certificate_rows = read_jsonl(certificate_rows_path)
    story_rows = story_rows_from_certificates(certificate_rows)
    return story_rows, summarize(certificate_rows, story_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Emit public PGSPG commitment-story rows.")
    parser.add_argument(
        "--certificate-rows",
        type=Path,
        default=THIS_DIR / "output" / "survivor_rows.jsonl",
        help="Public runner survivor_rows.jsonl path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "certificate_commitment_story",
        help="Directory for story_rows.jsonl and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, summary = run_probe(args.certificate_rows)
    write_jsonl(args.output_dir / "story_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
