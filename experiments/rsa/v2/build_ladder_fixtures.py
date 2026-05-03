#!/usr/bin/env python3
"""Write the deterministic RSA v2 ladder fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import gmpy2


DEFAULT_LADDER_SPEC = Path(__file__).resolve().parent / "ladder_spec.json"
DEFAULT_AUDIT_SPEC = Path(__file__).resolve().parent / "audit_spec.json"


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON object from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def default_case_id(n_text: str, index: int) -> str:
    """Return the stable case identifier derived from one public modulus."""
    # The bit length labels the rung without changing the solver rule.
    bits = gmpy2.mpz(n_text).bit_length()
    return f"rsa_v2_{bits}bit_static_{index:03d}"


def case_row(spec_row: dict[str, object], index: int) -> dict[str, object]:
    """Return one public ladder case row."""
    if "p" in spec_row or "q" in spec_row:
        raise ValueError("public ladder spec rows must not contain audit endpoints")
    n_text = str(spec_row["N"])
    n_value = gmpy2.mpz(n_text)
    # The bit length is public metadata derived directly from N.
    bits = n_value.bit_length()
    row = {
        "case_id": str(spec_row.get("case_id", default_case_id(n_text, index))),
        "bits": int(bits),
        "N": str(n_value),
    }
    if "description" in spec_row:
        row["description"] = str(spec_row["description"])
    return row


def audit_row(spec_row: dict[str, object]) -> dict[str, object]:
    """Return one separate audit row for downstream certification."""
    return {
        "case_id": str(spec_row["case_id"]),
        "p": str(spec_row["p"]),
        "q": str(spec_row["q"]),
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def build_fixtures(output_dir: Path, ladder_spec: Path, audit_spec: Path) -> None:
    """Write public cases and physically separate audit rows."""
    output_dir.mkdir(parents=True, exist_ok=True)
    public_payload = read_json(ladder_spec)
    audit_payload = read_json(audit_spec)
    case_rows = [
        case_row(dict(row), index)
        for index, row in enumerate(public_payload["cases"], start=1)
    ]
    audit_rows = [audit_row(dict(row)) for row in audit_payload["factors"]]
    public_case_ids = {str(row["case_id"]) for row in case_rows}
    audit_case_ids = {str(row["case_id"]) for row in audit_rows}
    if not public_case_ids.issubset(audit_case_ids):
        missing = sorted(public_case_ids - audit_case_ids)
        raise ValueError(f"audit spec missing case ids: {missing}")
    write_jsonl(output_dir / "ladder_cases.jsonl", case_rows)
    write_jsonl(output_dir / "audit_factors.jsonl", audit_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Write RSA v2 ladder fixtures.")
    parser.add_argument(
        "--ladder-spec",
        type=Path,
        default=DEFAULT_LADDER_SPEC,
        help="Public ladder spec JSON path.",
    )
    parser.add_argument(
        "--audit-spec",
        type=Path,
        default=DEFAULT_AUDIT_SPEC,
        help="Physically separate audit spec JSON path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "fixtures",
        help="Directory for ladder_cases.jsonl and audit_factors.jsonl.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run fixture writing from the command line."""
    args = parse_args(argv)
    build_fixtures(args.output_dir, args.ladder_spec, args.audit_spec)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
