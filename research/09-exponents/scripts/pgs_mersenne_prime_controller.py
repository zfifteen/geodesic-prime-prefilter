#!/usr/bin/env python3
"""Controller for PGSMPG v0.1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import pgs_mersenne_prime_generator as generator


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "09-exponents"
    / "output"
    / "pgs_mersenne_prime_generator_v0_1"
)
DEFAULT_START_EXPONENT = 2
DEFAULT_CHAIN_LENGTH = 10


def parse_anchors(raw: str) -> list[int]:
    """Parse comma-separated accepted exponents."""
    return [int(part) for part in raw.split(",") if part.strip()]


def build_parser() -> argparse.ArgumentParser:
    """Build the controller CLI."""
    parser = argparse.ArgumentParser(description="Run PGSMPG v0.1.")
    parser.add_argument("--anchors")
    parser.add_argument("--start-exponent", type=int, default=DEFAULT_START_EXPONENT)
    parser.add_argument("--chain-length", type=int, default=DEFAULT_CHAIN_LENGTH)
    parser.add_argument("--max-exponent", type=int, default=generator.DEFAULT_MAX_EXPONENT)
    parser.add_argument("--candidate-bound", type=int, default=generator.DEFAULT_CANDIDATE_BOUND)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def chain_generation_artifacts(
    start_exponent: int,
    chain_length: int,
    max_exponent: int,
    candidate_bound: int,
    on_exponent: Callable[[int], None] | None = None,
) -> tuple[list[int], list[dict[str, int]], list[dict[str, object]]]:
    """Return one PGSMPG exponent chain and compact diagnostics."""
    if chain_length < 2:
        raise ValueError("chain_length must be at least 2")

    exponents = [int(start_exponent)]
    if on_exponent is not None:
        on_exponent(int(start_exponent))
    records: list[dict[str, int]] = []
    diagnostics: list[dict[str, object]] = []
    current = int(start_exponent)
    while len(exponents) < chain_length:
        try:
            q, source, certificate = generator.resolve_q(
                current,
                max_exponent,
                candidate_bound,
            )
        except generator.PGSMPGUnresolvedError as exc:
            diagnostics.append(
                {
                    "p": current,
                    "q": "",
                    "source": generator.PGSMPG_SOURCE,
                    "status": "unresolved",
                    "error": str(exc),
                }
            )
            break
        records.append({"p": current, "q": q})
        diagnostics.append(
            {
                "p": current,
                "q": q,
                "source": source,
                "status": "resolved",
                "error": "",
                "attempt_count": int(certificate["attempt_count"]),
                "rule_id": certificate["rule_id"],
            }
        )
        exponents.append(q)
        if on_exponent is not None:
            on_exponent(q)
        current = q
    return exponents, records, diagnostics


def generation_artifacts(
    anchors: list[int],
    max_exponent: int,
    candidate_bound: int,
) -> tuple[list[dict[str, int]], list[dict[str, object]]]:
    """Return minimal records and compact diagnostics."""
    records: list[dict[str, int]] = []
    diagnostics: list[dict[str, object]] = []
    for anchor in anchors:
        try:
            q, source, certificate = generator.resolve_q(
                anchor,
                max_exponent,
                candidate_bound,
            )
        except generator.PGSMPGUnresolvedError as exc:
            diagnostics.append(
                {
                    "p": anchor,
                    "q": "",
                    "source": generator.PGSMPG_SOURCE,
                    "status": "unresolved",
                    "error": str(exc),
                }
            )
            continue
        records.append({"p": anchor, "q": q})
        diagnostics.append(
            {
                "p": anchor,
                "q": q,
                "source": source,
                "status": "resolved",
                "error": "",
                "attempt_count": int(certificate["attempt_count"]),
                "rule_id": certificate["rule_id"],
            }
        )
    return records, diagnostics


def summary(
    input_count: int,
    records: list[dict[str, int]],
    diagnostics: list[dict[str, object]],
    max_exponent: int,
    candidate_bound: int,
    chain_exponents: list[int] | None = None,
    chain_length_requested: int | None = None,
) -> dict[str, object]:
    """Return compact generation summary."""
    payload: dict[str, object] = {
        "version": generator.PGSMPG_VERSION,
        "freeze_id": generator.PGSMPG_FREEZE_ID,
        "input_count": input_count,
        "emitted": len(records),
        "unresolved": sum(record["status"] == "unresolved" for record in diagnostics),
        "max_exponent": max_exponent,
        "candidate_bound": candidate_bound,
    }
    if chain_exponents is not None:
        payload["chain_length_requested"] = chain_length_requested
        payload["chain_exponent_count"] = len(chain_exponents)
        payload["chain_exponents"] = chain_exponents
    return payload


def write_jsonl(records: list[dict[str, object]], path: Path) -> None:
    """Write LF-terminated JSONL."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def write_json(record: dict[str, object], path: Path) -> None:
    """Write LF-terminated JSON."""
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def run_controller(
    *,
    anchors: list[int] | None,
    start_exponent: int,
    chain_length: int,
    max_exponent: int,
    candidate_bound: int,
    output_dir: Path,
    on_exponent: Callable[[int], None] | None = None,
) -> dict[str, object]:
    """Run PGSMPG and write generation-only artifacts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    chain_exponents: list[int] | None = None
    if anchors is None:
        chain_exponents, records, diagnostics = chain_generation_artifacts(
            start_exponent,
            chain_length,
            max_exponent,
            candidate_bound,
            on_exponent,
        )
        input_count = 1
    else:
        records, diagnostics = generation_artifacts(anchors, max_exponent, candidate_bound)
        input_count = len(anchors)
    pgs_summary = summary(
        input_count,
        records,
        diagnostics,
        max_exponent,
        candidate_bound,
        chain_exponents,
        chain_length if chain_exponents is not None else None,
    )

    records_path = output_dir / "records.jsonl"
    diagnostics_path = output_dir / "diagnostics.jsonl"
    write_jsonl(records, records_path)
    write_jsonl(diagnostics, diagnostics_path)
    if chain_exponents is not None:
        write_jsonl(
            [{"e": exponent} for exponent in chain_exponents],
            output_dir / "mersenne_exponents.jsonl",
        )
    write_json(pgs_summary, output_dir / "pgs_summary.json")

    combined = {
        "pgs_generator": pgs_summary,
        "controller_order": "pgs_generator_only",
    }
    write_json(combined, output_dir / "summary.json")
    return combined


def main(argv: list[str] | None = None) -> int:
    """Run the controller."""
    args = build_parser().parse_args(argv)

    def print_exponent(exponent: int) -> None:
        print(f"PGSMPG exponent: {exponent}", flush=True)

    summary_payload = run_controller(
        anchors=None if args.anchors is None else parse_anchors(args.anchors),
        start_exponent=args.start_exponent,
        chain_length=args.chain_length,
        max_exponent=args.max_exponent,
        candidate_bound=args.candidate_bound,
        output_dir=args.output_dir,
        on_exponent=None if args.anchors is not None else print_exponent,
    )
    pgs_summary = summary_payload["pgs_generator"]
    if "chain_exponents" in pgs_summary:
        print(
            "PGSMPG exponents: "
            + ", ".join(str(value) for value in pgs_summary["chain_exponents"])
        )
    print(
        "PGSMPG records: "
        f"{pgs_summary['emitted']} emitted, {pgs_summary['unresolved']} unresolved"
    )
    print(f"Output dir: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
