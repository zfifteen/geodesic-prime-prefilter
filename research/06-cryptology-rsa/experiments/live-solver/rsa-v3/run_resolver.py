#!/usr/bin/env python3
"""Launch the A1 endpoint resolver on public cases."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from residual import is_resolved_status
from resolver import git_commit, load_public_cases, resolve_cases
from structural_certificate import ALGORITHM_VERSION, RULE_ID


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A1 PGS RSA endpoint resolver v3")
    parser.add_argument("--cases", type=Path, required=True, help="Public cases JSONL")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--max-steps", type=int, default=None, help="Optional chain step budget")
    parser.add_argument(
        "--case-ids",
        type=str,
        default=None,
        help="Comma-separated case_id filter",
    )
    args = parser.parse_args(argv)

    cases = load_public_cases(args.cases)
    if args.case_ids:
        wanted = {x.strip() for x in args.case_ids.split(",") if x.strip()}
        cases = [c for c in cases if c.case_id in wanted]

    commit = git_commit()
    results = resolve_cases(cases, max_steps=args.max_steps, commit=commit)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = [r["summary"] for r in results]
    inference = [r["inference"] for r in results]
    pairs = [r["pair"] for r in results]
    residuals = [r["residual"] for r in results if r["residual"] is not None]
    certs = [r["structural_certificate"] for r in results if r["structural_certificate"] is not None]

    write_jsonl(args.output_dir / "inference_rows.jsonl", inference)
    write_jsonl(args.output_dir / "survivor_rows.jsonl", pairs)
    write_jsonl(args.output_dir / "residuals.jsonl", residuals)
    if certs:
        write_jsonl(args.output_dir / "structural_certificates.jsonl", certs)

    residual_hist = Counter(r["residual_code"] for r in residuals)
    resolved = sum(1 for s in summaries if is_resolved_status(str(s["closure_status"])))
    measured = {
        "algorithm_version": ALGORITHM_VERSION,
        "rule_id": RULE_ID,
        "git_commit": commit,
        "case_count": len(summaries),
        "resolved_count": resolved,
        "unresolved_count": len(summaries) - resolved,
        "resolution_rate_measured_only": (
            None if not summaries else resolved / len(summaries)
        ),
        "residual_histogram_measured_only": dict(residual_hist),
        "note": "resolution_rate is measured only and is not a pass criterion",
    }
    write_json(
        args.output_dir / "summary.json",
        {"cases": summaries, "measured": measured},
    )
    print(json.dumps({"cases": summaries, "measured": measured}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
