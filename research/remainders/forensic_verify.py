#!/usr/bin/env python3
"""Forensic verification for REMAINDER_FORENSIC_REPORT.md."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REMAINDERS = ROOT / "research" / "remainders"
REPORT = REMAINDERS / "REMAINDER_FORENSIC_REPORT.md"
INVESTIGATION = REMAINDERS / "correlations" / "investigation"

LANE_AGENTS = [
    "interior_rnm",
    "super_signal_status",
    "endpoint_mask",
    "mod30_ridge",
    "state_budget",
    "rsa_backward",
]

SPOTCHECKS = [
    (
        "gaps_with_interiors",
        INVESTIGATION / "interior_placement_stats.json",
        ["gaps_with_interiors"],
        114154,
    ),
    (
        "gwr_last_rate",
        INVESTIGATION / "interior_placement_stats.json",
        ["gwr_last_rate"],
        0.13861975927256162,
    ),
    (
        "super_signal_at_gwr_count",
        INVESTIGATION / "interior_placement_stats.json",
        ["super_signal_at_gwr_count"],
        3842,
    ),
    (
        "endpoint_resolved_fraction",
        INVESTIGATION / "endpoint_lane_summary.json",
        ["fresh_probe", "resolved_in_mask_fraction"],
        0.2373,
    ),
    (
        "mod30_p13_lift_1e6",
        INVESTIGATION / "mod30_ridge_lane_summary.json",
        None,
        1.5759927769127229,
        lambda data: next(
            r["right_lift"]
            for r in data["pinned_scale_1e6_summary"]
            if r["residue"] == 13
        ),
    ),
    (
        "state_budget_mod30_pairs",
        INVESTIGATION / "state_budget_lane_summary.json",
        ["mod30_decisive_pairs"],
        230,
    ),
    (
        "rsa_factor_reach",
        INVESTIGATION / "rsa_lane_summary.json",
        ["best_factor_reach_recall"],
        0.0,
    ),
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def dig(data: dict, keys: list[str]):
    cur = data
    for key in keys:
        cur = cur[key]
    return cur


def run_spotchecks() -> list[str]:
    lines: list[str] = []
    for spec in SPOTCHECKS:
        name = spec[0]
        path = spec[1]
        keys = spec[2]
        expected = spec[3]
        getter = spec[4] if len(spec) > 4 else None
        data = load_json(path)
        actual = getter(data) if getter else dig(data, keys)
        ok = actual == expected
        lines.append(
            f"{name}: expected={expected!r} actual={actual!r} source={path.relative_to(ROOT)} "
            f"{'PASS' if ok else 'FAIL'}"
        )
        if not ok:
            raise SystemExit(f"spotcheck failed: {name}")
    return lines


def lane_coverage(report_text: str) -> list[str]:
    missing = [a for a in LANE_AGENTS if a not in report_text]
    lines = [f"lane_agents_required: {len(LANE_AGENTS)}"]
    for agent in LANE_AGENTS:
        lines.append(f"{agent}: {'present' if agent in report_text else 'MISSING'}")
    if missing:
        raise SystemExit(f"report missing lane agents: {missing}")
    return lines


def epistemic_audit(report_text: str) -> list[str]:
    required_sources = [
        "PROOF.md",
        "docs/proof-enhancements/goals.md",
        "REMAINDER_LANES_SYNTHESIS.md",
        "README.md",
    ]
    lines = []
    for src in required_sources:
        present = src in report_text
        lines.append(f"{src}: {'cited' if present else 'MISSING'}")
        if not present:
            raise SystemExit(f"report missing epistemic source: {src}")
    if "measured · corollary" not in report_text and "measured \u00b7 corollary" not in report_text:
        raise SystemExit("report missing reconciled super-signal status")
    return lines


def run_log_summary() -> list[str]:
    run_log = load_json(INVESTIGATION / "RUN_LOG.json")
    super_run = load_json(INVESTIGATION / "SUPER_TEAM_RUN.json")
    lines = [
        f"timestamp_utc: {run_log.get('timestamp_utc')}",
        f"gaps_with_interiors: {run_log.get('gaps_with_interiors')}",
        f"records_analyzed: {run_log.get('records_analyzed')}",
    ]
    for lane, info in run_log.get("lane_collector_runs", {}).items():
        lines.append(f"{lane}: returncode={info.get('returncode')}")
    for status in super_run.get("agent_status", []):
        lines.append(
            f"{status['agent_id']}: status={status.get('status')} "
            f"returncode={status.get('returncode', 'n/a')}"
        )
    return lines


def key_findings_check(report_text: str) -> list[str]:
    pointers = [
        ("CORRELATION_REPORT.md", "gap-echo"),
        ("interior_placement_stats.json", "super-signal"),
        ("g2_with_super_signal_gwr", "g=2"),
    ]
    lines = []
    for needle, label in pointers:
        ok = needle.lower() in report_text.lower()
        lines.append(f"{label}: {needle} -> {'present' if ok else 'MISSING'}")
        if not ok:
            raise SystemExit(f"report missing key finding pointer: {needle}")
    return lines


def main() -> int:
    if not REPORT.is_file():
        print(f"missing report: {REPORT}", file=sys.stderr)
        return 1
    text = REPORT.read_text(encoding="utf-8")
    for section in ("## Synthesis", "## Downstream Research Index", "## Cross-Lane Epistemic Audit"):
        if section not in text:
            print(f"missing section: {section}", file=sys.stderr)
            return 1

    coverage = lane_coverage(text)
    spotchecks = run_spotchecks()
    epistemic = epistemic_audit(text)
    run_log = run_log_summary()
    key_findings = key_findings_check(text)

    print("forensic_verify: PASS")
    print("lane_coverage:", len(coverage), "lines")
    print("spotchecks:", len(spotchecks), "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())