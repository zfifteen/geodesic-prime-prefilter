#!/usr/bin/env python3
"""Diagnostic Gate-A probe for public-coordinate certificate acquisition.

This is a diagnostic calibration report. It is not a reduction evidence
surface and it is not a live resolver.

Question:
    Can a public coordinate start recover the RB-grade PGSPG certificate story
    needed by the transported frontier layer, without adjacent endpoint
    acquisition?

The current probe uses the committed exact-state implementation as a reference
oracle only. Any row produced here is diagnostic evidence, not a PGS-native
live derivation claim.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Any

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
LIVE_SOLVER = ROOT / "research/06-cryptology-rsa/experiments/live-solver/rsa-v2/run_experiment.py"
DEFAULT_CASES = (
    ROOT
    / "research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/fixtures/ladder_cases.jsonl"
)
DEFAULT_OUTPUT = THIS_DIR / "output/coordinate_start_certificate_acquisition_probe"

REPORT_HEADER = "This is a diagnostic calibration report. It is not a reduction evidence surface."
FORBIDDEN_BACKEND_FLAGS = ("exact_divisor_count_state",)
REQUIRED_STORY_FIELDS = (
    "anchor",
    "reset_endpoint",
    "gap_offset",
    "closed_offsets_before_q",
    "carrier_w",
    "carrier_d",
    "lock_carrier_offset",
    "lock_carrier_d",
    "lower_d_threat_offset",
    "tail_after_reset_offsets",
    "reset_deadline_value",
    "reset_signature",
)


def load_live_solver() -> ModuleType:
    """Load the current RSA v2 live-solver module as a reference oracle."""
    spec = importlib.util.spec_from_file_location("rsa_v2_live_solver_reference", LIVE_SOLVER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load live solver from {LIVE_SOLVER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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


def cert_field(certificate: Any, field: str) -> Any:
    """Return one JSON-safe certificate field."""
    value = getattr(certificate, field)
    if isinstance(value, gmpy2.mpz):
        return str(value)
    if isinstance(value, tuple):
        return list(value)
    return value


def cert_json(certificate: Any | None) -> dict[str, Any] | None:
    """Return the RB-grade certificate story fields used by this probe."""
    if certificate is None:
        return None
    return {field: cert_field(certificate, field) for field in REQUIRED_STORY_FIELDS}


def first_mismatch(reference: dict[str, Any] | None, coordinate: dict[str, Any] | None) -> str | None:
    """Return the first certificate-story component that fails to reproduce."""
    if reference is None:
        return "reference_certificate"
    if coordinate is None:
        return "coordinate_certificate"
    for field in REQUIRED_STORY_FIELDS:
        if reference.get(field) != coordinate.get(field):
            return field
    return None


def mismatched_fields(reference: dict[str, Any] | None, coordinate: dict[str, Any] | None) -> list[str]:
    """Return every RB-grade story field that fails to reproduce."""
    if reference is None:
        return ["reference_certificate"]
    if coordinate is None:
        return ["coordinate_certificate"]
    return [
        field
        for field in REQUIRED_STORY_FIELDS
        if reference.get(field) != coordinate.get(field)
    ]


def row_status(reference: dict[str, Any] | None, coordinate: dict[str, Any] | None) -> str:
    """Classify one Gate-A acquisition attempt."""
    mismatch = first_mismatch(reference, coordinate)
    if mismatch is None:
        return "reference_story_reproduced_by_coordinate_start_diagnostic"
    if reference is None:
        return "reference_certificate_unavailable"
    if coordinate is None:
        return "coordinate_start_unresolved"
    if reference.get("reset_endpoint") == coordinate.get("reset_endpoint"):
        return "endpoint_recovered_but_anchor_story_mismatch"
    return "coordinate_start_different_endpoint"


def build_row(case: Any, live: ModuleType) -> dict[str, Any]:
    """Build one public-coordinate acquisition diagnostic row."""
    diagnostics = live.make_diagnostics()
    center = gmpy2.isqrt(case.n)
    certificate_cache: dict[int, Any] = {}
    previous_endpoint_cache: dict[int, Any] = {}
    segment_cache: dict[tuple[int, int], object] = {}

    reference_anchor = live.previous_endpoint_at(
        center,
        previous_endpoint_cache,
        segment_cache,
        diagnostics,
    )
    reference = (
        None
        if reference_anchor is None
        else live.certificate_at(reference_anchor, certificate_cache, diagnostics)
    )
    coordinate = live.pgs_certificate(center)

    reference_story = cert_json(reference)
    coordinate_story = cert_json(coordinate)
    mismatch = first_mismatch(reference_story, coordinate_story)
    all_mismatches = mismatched_fields(reference_story, coordinate_story)
    status = row_status(reference_story, coordinate_story)
    endpoint_match = (
        reference_story is not None
        and coordinate_story is not None
        and reference_story["reset_endpoint"] == coordinate_story["reset_endpoint"]
    )
    story_match = mismatch is None

    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "diagnostic_header": REPORT_HEADER,
        "probe": "coordinate_start_certificate_acquisition_gate",
        "public_coordinate": str(center),
        "reference_provider": "previous_endpoint_at_plus_exact_state_oracle",
        "coordinate_provider": "coordinate_start_exact_state_diagnostic",
        "live_eligible": False,
        "forbidden_backend_flags": list(FORBIDDEN_BACKEND_FLAGS),
        "reference_anchor": None if reference_anchor is None else str(reference_anchor),
        "reference_story": reference_story,
        "coordinate_story": coordinate_story,
        "endpoint_match": endpoint_match,
        "rb_grade_story_match": story_match,
        "first_failing_component": mismatch,
        "mismatched_fields": all_mismatches,
        "gate_a_status": status,
        "diagnostics": diagnostics,
    }


def markdown_report(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    """Return a compact Markdown report."""
    lines = [
        "# Coordinate-Start Certificate Acquisition Probe",
        "",
        REPORT_HEADER,
        "",
        "## Finding",
        "",
        str(summary["finding"]),
        "",
        "## Aggregate",
        "",
        f"- cases: `{summary['case_count']}`",
        f"- endpoint matches: `{summary['endpoint_match_count']}`",
        f"- RB-grade story matches: `{summary['rb_grade_story_match_count']}`",
        f"- live Gate-A passes: `{summary['live_gate_a_pass_count']}`",
        f"- forbidden backend flags: `{', '.join(summary['forbidden_backend_flags'])}`",
        "",
        "## First Failing Components",
        "",
    ]
    for component, count in summary["first_failing_components"].items():
        lines.append(f"- `{component}`: `{count}`")
    lines.extend(["", "## Rows", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['case_id']}",
                "",
                f"- bits: `{row['bits']}`",
                f"- public coordinate: `{row['public_coordinate']}`",
                f"- status: `{row['gate_a_status']}`",
                f"- endpoint match: `{row['endpoint_match']}`",
                f"- RB-grade story match: `{row['rb_grade_story_match']}`",
                f"- first failing component: `{row['first_failing_component']}`",
                f"- mismatched fields: `{', '.join(row['mismatched_fields'])}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Return aggregate probe status."""
    failures = Counter(str(row["first_failing_component"]) for row in rows)
    all_failures = Counter(
        field
        for row in rows
        for field in row["mismatched_fields"]
    )
    endpoint_matches = sum(1 for row in rows if row["endpoint_match"])
    story_matches = sum(1 for row in rows if row["rb_grade_story_match"])
    live_passes = sum(
        1
        for row in rows
        if row["rb_grade_story_match"] and row["live_eligible"] and not row["forbidden_backend_flags"]
    )
    if story_matches == len(rows) and live_passes == len(rows):
        finding = "Coordinate-start acquisition satisfies the live Gate-A contract on this surface."
    elif endpoint_matches:
        finding = (
            "Coordinate-start exact-state diagnostics recover at least one endpoint, but they do not "
            "reproduce the anchor-relative RB-grade certificate story and remain live-ineligible."
        )
    else:
        finding = (
            "Coordinate-start exact-state diagnostics do not reproduce the current reference "
            "certificate story on this surface."
        )
    return {
        "diagnostic_header": REPORT_HEADER,
        "case_count": len(rows),
        "endpoint_match_count": endpoint_matches,
        "rb_grade_story_match_count": story_matches,
        "live_gate_a_pass_count": live_passes,
        "forbidden_backend_flags": list(FORBIDDEN_BACKEND_FLAGS),
        "first_failing_components": dict(sorted(failures.items())),
        "all_mismatched_fields": dict(sorted(all_failures.items())),
        "finding": finding,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the diagnostic coordinate-start certificate acquisition Gate-A probe."
    )
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the diagnostic probe."""
    args = parse_args(argv)
    live = load_live_solver()
    cases = live.load_cases(args.cases)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = [build_row(case, live) for case in cases]
    summary = summarize(rows)
    write_jsonl(args.output_dir / "acquisition_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    (args.output_dir / "summary.md").write_text(markdown_report(summary, rows), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
