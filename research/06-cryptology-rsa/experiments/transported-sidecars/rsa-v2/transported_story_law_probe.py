#!/usr/bin/env python3
"""Emit direct transported certificate-story law diagnostics for RSA v2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = THIS_DIR.parents[1]
LIVE_SOLVER_DIR = EXPERIMENTS_DIR / "live-solver" / "rsa-v2"
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
CERTIFICATE_DIR = EXPERIMENTS_DIR / "certificate-mechanics" / "rsa-v2"
for import_dir in (THIS_DIR, LIVE_SOLVER_DIR, CERTIFICATE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from certificate_commitment_story_probe import (  # noqa: E402
    pgspg_certificate_story_rows,
)
from run_experiment import (  # noqa: E402
    LadderCase,
    PGSCertificate,
    load_cases,
    pgs_certificate,
    previous_endpoint,
)


RULE_ID = "transported_story_law_v1"
DEFAULT_MEASURED_ROWS = 256
DEFAULT_RECURSIVE_DEPTH = 4
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "transported_story_law"
EXPECTED_COUNTS = {
    "row_count": 512,
    "ledger_effective_survivor_count": 202,
    "recursive_row_count": 713,
    "recursive_final_survivor_count": 0,
}


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def prior_endpoint_chain(start: gmpy2.mpz, measured_rows: int) -> list[gmpy2.mpz]:
    """Return a measurement-only chain of public previous endpoints."""
    if measured_rows < 1:
        raise ValueError("measured_rows must be positive")
    anchors: list[gmpy2.mpz] = []
    current = gmpy2.mpz(start)
    for _index in range(measured_rows):
        anchors.append(current)
        next_anchor = previous_endpoint(current - 1)
        if next_anchor is None:
            break
        current = next_anchor
    return anchors


def story_event(rows: list[dict[str, object]], event_kind: str) -> dict[str, object] | None:
    """Return the first public story event with one kind."""
    for row in rows:
        if str(row["event_kind"]) == event_kind:
            return row
    return None


def required_event(rows: list[dict[str, object]], event_kind: str) -> dict[str, object]:
    """Return one required public story event."""
    row = story_event(rows, event_kind)
    if row is None:
        raise ValueError(f"certificate story missing event kind: {event_kind}")
    return row


def event_value(row: dict[str, object]) -> gmpy2.mpz:
    """Return one public story event coordinate."""
    return gmpy2.mpz(str(row["event_value"]))


def event_lock_depth(row: dict[str, object]) -> int | None:
    """Return the lock depth attached to one public story event."""
    value = row["lock_carrier_d"]
    if value is None:
        return None
    return int(value)


def image(n_value: gmpy2.mpz, row: dict[str, object] | None) -> gmpy2.mpz | None:
    """Return the reciprocal floor image of one public story event."""
    if row is None:
        return None
    return n_value // event_value(row)


def in_closed_interval(value: gmpy2.mpz, left: gmpy2.mpz, right: gmpy2.mpz) -> bool:
    """Return whether one public coordinate lies inside a closed interval."""
    lo = min(left, right)
    hi = max(left, right)
    return lo <= value <= hi


def story_values(rows: list[dict[str, object]]) -> list[str]:
    """Return ordered public event values for a certificate story."""
    return [str(row["event_value"]) for row in rows]


def story_kinds(rows: list[dict[str, object]]) -> list[str]:
    """Return ordered public event kinds for a certificate story."""
    return [str(row["event_kind"]) for row in rows]


def induced_anchor_for(n_value: gmpy2.mpz, source_reset: dict[str, object]) -> gmpy2.mpz | None:
    """Return the public opposite anchor induced by transported reset."""
    return previous_endpoint(n_value // event_value(source_reset))


def story_law_row(
    case: LadderCase,
    source_certificate: PGSCertificate,
    seen_induced_anchors: set[str],
) -> dict[str, object]:
    """Return one direct transported story-law diagnostic row."""
    source_story = pgspg_certificate_story_rows(case.case_id, source_certificate)
    source_carrier = required_event(source_story, "carrier_lock")
    source_reset = required_event(source_story, "reset")
    source_deadline = required_event(source_story, "deadline")
    source_threat = story_event(source_story, "lower_threat")

    source_carrier_image = image(case.n, source_carrier)
    source_reset_image = image(case.n, source_reset)
    source_deadline_image = image(case.n, source_deadline)
    if source_carrier_image is None or source_reset_image is None or source_deadline_image is None:
        raise ValueError("required source story event image missing")

    induced_anchor = induced_anchor_for(case.n, source_reset)
    induced_certificate = None if induced_anchor is None else pgs_certificate(induced_anchor)
    induced_story = (
        []
        if induced_certificate is None
        else pgspg_certificate_story_rows(case.case_id, induced_certificate)
    )
    induced_carrier = None if induced_certificate is None else story_event(induced_story, "carrier_lock")
    induced_reset = None if induced_certificate is None else story_event(induced_story, "reset")
    induced_deadline = None if induced_certificate is None else story_event(induced_story, "deadline")
    induced_threat = None if induced_certificate is None else story_event(induced_story, "lower_threat")

    induced_carrier_value = None if induced_carrier is None else event_value(induced_carrier)
    induced_threat_value = None if induced_threat is None else event_value(induced_threat)
    source_lock_depth = event_lock_depth(source_carrier)
    induced_lock_depth = None if induced_carrier is None else event_lock_depth(induced_carrier)

    carrier_in_prefix = (
        induced_carrier_value is not None
        and in_closed_interval(induced_carrier_value, source_reset_image, source_carrier_image)
    )
    carrier_in_suffix = (
        induced_carrier_value is not None
        and in_closed_interval(induced_carrier_value, source_deadline_image, source_reset_image)
    )
    prefix_elimination = (
        carrier_in_prefix
        and source_lock_depth is not None
        and induced_lock_depth is not None
        and induced_lock_depth <= source_lock_depth
    )
    suffix_elimination = (
        carrier_in_suffix
        and source_lock_depth is not None
        and induced_lock_depth is not None
        and induced_lock_depth < source_lock_depth
    )
    threat_before_deadline = (
        induced_threat_value is not None
        and induced_threat_value < source_deadline_image
    )
    threat_in_committed_zone = (
        induced_threat_value is not None
        and in_closed_interval(induced_threat_value, source_deadline_image, source_reset_image)
    )
    threat_ceiling_elimination = (
        (threat_before_deadline or threat_in_committed_zone)
        and source_lock_depth is not None
        and induced_lock_depth is not None
        and induced_lock_depth <= source_lock_depth
    )
    ledger_eliminated = (
        prefix_elimination
        or suffix_elimination
        or threat_ceiling_elimination
    )
    induced_anchor_text = None if induced_anchor is None else str(induced_anchor)
    stale_state = induced_anchor_text is None or induced_anchor_text in seen_induced_anchors
    if induced_anchor_text is not None:
        seen_induced_anchors.add(induced_anchor_text)
    frontier_new_state = not stale_state
    ledger_survivor = not ledger_eliminated

    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "source_anchor": str(source_certificate.anchor),
        "source_story_event_kinds": story_kinds(source_story),
        "source_story_event_values": story_values(source_story),
        "source_carrier_event_value": str(event_value(source_carrier)),
        "source_reset_event_value": str(event_value(source_reset)),
        "source_deadline_event_value": str(event_value(source_deadline)),
        "source_threat_event_value": None if source_threat is None else str(event_value(source_threat)),
        "source_lock_carrier_d": source_lock_depth,
        "source_transport_carrier_image": str(source_carrier_image),
        "source_transport_reset_image": str(source_reset_image),
        "source_transport_deadline_image": str(source_deadline_image),
        "transported_prefix_lo": str(min(source_reset_image, source_carrier_image)),
        "transported_prefix_hi": str(max(source_reset_image, source_carrier_image)),
        "transported_suffix_lo": str(min(source_deadline_image, source_reset_image)),
        "transported_suffix_hi": str(max(source_deadline_image, source_reset_image)),
        "induced_anchor": induced_anchor_text,
        "induced_story_event_kinds": story_kinds(induced_story),
        "induced_story_event_values": story_values(induced_story),
        "induced_carrier_event_value": None if induced_carrier is None else str(event_value(induced_carrier)),
        "induced_reset_event_value": None if induced_reset is None else str(event_value(induced_reset)),
        "induced_deadline_event_value": None if induced_deadline is None else str(event_value(induced_deadline)),
        "induced_threat_event_value": None if induced_threat is None else str(event_value(induced_threat)),
        "induced_lock_carrier_d": induced_lock_depth,
        "induced_carrier_in_prefix_zone": carrier_in_prefix,
        "induced_carrier_in_suffix_zone": carrier_in_suffix,
        "induced_threat_before_transported_deadline": threat_before_deadline,
        "induced_threat_in_committed_zone": threat_in_committed_zone,
        "ledger_prefix_elimination": prefix_elimination,
        "ledger_suffix_elimination": suffix_elimination,
        "ledger_threat_ceiling_elimination": threat_ceiling_elimination,
        "ledger_eliminated": ledger_eliminated,
        "ledger_survivor": ledger_survivor,
        "frontier_new_transport_state": frontier_new_state,
        "ledger_stale_transport_state": stale_state,
        "ledger_effective_survivor": ledger_survivor and frontier_new_state,
    }


def case_rows(case: LadderCase, measured_rows: int) -> list[dict[str, object]]:
    """Return direct story-law rows for one public modulus case."""
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []
    rows: list[dict[str, object]] = []
    seen_induced_anchors: set[str] = set()
    for anchor in prior_endpoint_chain(first_anchor, measured_rows):
        certificate = pgs_certificate(anchor)
        if certificate is not None:
            rows.append(story_law_row(case, certificate, seen_induced_anchors))
    return rows


def recursive_case_rows(
    case: LadderCase,
    measured_rows: int,
    recursive_depth: int,
) -> list[dict[str, object]]:
    """Return recursive direct story-law rows for one public modulus case."""
    if recursive_depth < 1:
        return []
    center = gmpy2.isqrt(case.n)
    first_anchor = previous_endpoint(center)
    if first_anchor is None:
        return []

    source_anchors = prior_endpoint_chain(first_anchor, measured_rows)
    seen_induced_anchors: set[str] = set()
    seen_source_anchors: set[str] = set()
    rows: list[dict[str, object]] = []

    for depth in range(recursive_depth):
        layer_source_keys = {str(anchor) for anchor in source_anchors}
        seen_source_anchors.update(layer_source_keys)
        next_anchors: list[gmpy2.mpz] = []

        for anchor in source_anchors:
            certificate = pgs_certificate(anchor)
            if certificate is None:
                continue
            row = story_law_row(case, certificate, seen_induced_anchors)
            induced_anchor = row["induced_anchor"]
            cycle_state = (
                induced_anchor is not None
                and str(induced_anchor) in seen_source_anchors
            )
            row["recursion_depth"] = depth
            row["ledger_recursive_cycle_state"] = cycle_state
            row["ledger_recursive_survivor"] = (
                row["ledger_effective_survivor"] and not cycle_state
            )
            rows.append(row)
            if row["ledger_recursive_survivor"] and induced_anchor is not None:
                next_anchors.append(gmpy2.mpz(str(induced_anchor)))

        if not next_anchors:
            break
        source_anchors = next_anchors

    return rows


def count(rows: list[dict[str, object]], field: str) -> int:
    """Return the number of rows where one boolean field is true."""
    return sum(1 for row in rows if bool(row[field]))


def layer_summaries(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return recursive layer count summaries."""
    summaries = []
    for depth in sorted({int(row["recursion_depth"]) for row in rows}):
        layer_rows = [row for row in rows if int(row["recursion_depth"]) == depth]
        summaries.append(
            {
                "recursion_depth": depth,
                "row_count": len(layer_rows),
                "ledger_eliminated_count": count(layer_rows, "ledger_eliminated"),
                "ledger_stale_transport_state_count": count(
                    layer_rows,
                    "ledger_stale_transport_state",
                ),
                "ledger_recursive_cycle_state_count": count(
                    layer_rows,
                    "ledger_recursive_cycle_state",
                ),
                "ledger_recursive_survivor_count": count(
                    layer_rows,
                    "ledger_recursive_survivor",
                ),
            }
        )
    return summaries


def divergence_rows(summary: dict[str, object]) -> list[dict[str, object]]:
    """Return named count divergences against the experiment contract."""
    field_sources = {
        "row_count": "story_law_rows",
        "ledger_effective_survivor_count": "ledger_effective_survivor",
        "recursive_row_count": "recursive_rows",
        "recursive_final_survivor_count": "ledger_recursive_survivor",
    }
    rows = []
    for field, expected in EXPECTED_COUNTS.items():
        observed = int(summary[field])
        if observed != expected:
            rows.append(
                {
                    "field": field,
                    "expected": expected,
                    "observed": observed,
                    "public_story_field": field_sources[field],
                }
            )
    return rows


def summarize(
    rows: list[dict[str, object]],
    recursive_rows: list[dict[str, object]],
    measured_rows: int,
    recursive_depth: int,
) -> dict[str, object]:
    """Return direct story-law falsification counts."""
    layers = layer_summaries(recursive_rows)
    summary: dict[str, object] = {
        "rule_id": RULE_ID,
        "measured_rows_per_case": measured_rows,
        "recursive_depth_limit": recursive_depth,
        "row_count": len(rows),
        "ledger_prefix_elimination_count": count(rows, "ledger_prefix_elimination"),
        "ledger_suffix_elimination_count": count(rows, "ledger_suffix_elimination"),
        "ledger_threat_ceiling_elimination_count": count(
            rows,
            "ledger_threat_ceiling_elimination",
        ),
        "ledger_eliminated_count": count(rows, "ledger_eliminated"),
        "ledger_survivor_count": count(rows, "ledger_survivor"),
        "ledger_stale_transport_state_count": count(rows, "ledger_stale_transport_state"),
        "ledger_effective_survivor_count": count(rows, "ledger_effective_survivor"),
        "recursive_row_count": len(recursive_rows),
        "recursive_layer_summaries": layers,
        "recursive_final_survivor_count": (
            0 if not layers else int(layers[-1]["ledger_recursive_survivor_count"])
        ),
    }
    divergences = divergence_rows(summary)
    summary["expected_counts"] = EXPECTED_COUNTS
    summary["falsification_status"] = "passed" if not divergences else "failed"
    summary["divergences"] = divergences
    return summary


def run_probe(
    cases_path: Path,
    measured_rows: int,
    recursive_depth: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the direct transported story-law probe."""
    cases = load_cases(cases_path)
    rows: list[dict[str, object]] = []
    recursive_rows: list[dict[str, object]] = []
    for case in cases:
        rows.extend(case_rows(case, measured_rows))
        recursive_rows.extend(recursive_case_rows(case, measured_rows, recursive_depth))
    return rows, recursive_rows, summarize(rows, recursive_rows, measured_rows, recursive_depth)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Emit direct transported certificate-story law diagnostics."
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--measured-rows",
        type=int,
        default=DEFAULT_MEASURED_ROWS,
        help="Measurement-only public frontier rows per case.",
    )
    parser.add_argument(
        "--recursive-depth",
        type=int,
        default=DEFAULT_RECURSIVE_DEPTH,
        help="Measurement-only recursive transported-ledger depth limit.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for story_law_rows.jsonl, recursive_rows.jsonl, and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, recursive_rows, summary = run_probe(
        args.cases,
        args.measured_rows,
        args.recursive_depth,
    )
    write_jsonl(args.output_dir / "story_law_rows.jsonl", rows)
    write_jsonl(args.output_dir / "recursive_rows.jsonl", recursive_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
