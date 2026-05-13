#!/usr/bin/env python3
"""Public Endpoint Determinacy Kernel for RSA v2 public modulus rows."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
EXPERIMENTS_DIR = THIS_DIR.parents[1]
LIVE_SOLVER_DIR = EXPERIMENTS_DIR / "live-solver" / "rsa-v2"
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
if str(LIVE_SOLVER_DIR) not in sys.path:
    sys.path.insert(0, str(LIVE_SOLVER_DIR))

from run_experiment import LadderCase, certificate_pair, load_cases  # noqa: E402


RULE_ID = "public_endpoint_determinacy_kernel_v0"
DEFAULT_OUTPUT = THIS_DIR / "output" / "pedk_rows.jsonl"

DETERMINED_CLOSURES = {
    "endpoint_class_by_mutual_certificate_closure",
    "endpoint_class_by_reciprocal_deadline_signature_correction",
}
CANDIDATE_CLOSURES = {
    "endpoint_class_by_oriented_endpoint_chain_closure",
}


@dataclass(frozen=True)
class PublicEndpointState:
    """One public endpoint determinacy state emitted from N alone."""

    case_id: str
    bits: int
    n: gmpy2.mpz
    pedk_status: str
    public_closure_status: str
    endpoint_class_lower: gmpy2.mpz | None
    endpoint_class_upper: gmpy2.mpz | None

    def to_row(self) -> dict[str, object]:
        """Return the JSON-safe public row."""
        row: dict[str, object] = {
            "case_id": self.case_id,
            "bits": self.bits,
            "N": str(self.n),
            "pedk_status": self.pedk_status,
            "public_structure_found": self.endpoint_class_lower is not None
            and self.endpoint_class_upper is not None,
            "public_closure_status": self.public_closure_status,
            "endpoint_class_lower": (
                None if self.endpoint_class_lower is None else str(self.endpoint_class_lower)
            ),
            "endpoint_class_upper": (
                None if self.endpoint_class_upper is None else str(self.endpoint_class_upper)
            ),
            "rule_id": RULE_ID,
        }
        return row


def endpoint_class_from_pair(pair) -> tuple[str, gmpy2.mpz | None, gmpy2.mpz | None]:
    """Return the public endpoint class carried by one closure pair."""
    if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
        if pair.lower is None or pair.upper is None:
            raise ValueError("mutual closure missing public certificates")
        return pair.closure_status, pair.lower.reset_endpoint, pair.upper.reset_endpoint
    if pair.closure_status in {
        "endpoint_class_by_reciprocal_deadline_signature_correction",
        "endpoint_class_by_oriented_endpoint_chain_closure",
    }:
        return pair.closure_status, pair.corrected_lower_endpoint, pair.corrected_upper_endpoint
    return pair.closure_status, None, None


def evaluate_case(case: LadderCase) -> PublicEndpointState:
    """Evaluate one public modulus row through PEDK."""
    pair = certificate_pair(case)
    closure_status, lower, upper = endpoint_class_from_pair(pair)
    if closure_status in DETERMINED_CLOSURES:
        pedk_status = "public_endpoint_class_determined"
    elif closure_status in CANDIDATE_CLOSURES:
        pedk_status = "public_endpoint_class_candidate"
    elif closure_status.startswith("unresolved_"):
        pedk_status = "unresolved_structural_state"
    else:
        pedk_status = "invalidated_path"
    return PublicEndpointState(
        case.case_id,
        case.bits,
        case.n,
        pedk_status,
        closure_status,
        lower,
        upper,
    )


def run_pedk(cases: list[LadderCase]) -> list[dict[str, object]]:
    """Return PEDK rows for public ladder cases."""
    return [evaluate_case(case).to_row() for case in cases]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the Public Endpoint Determinacy Kernel.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="PEDK JSONL output path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run PEDK and write LF-terminated JSONL rows."""
    args = parse_args(argv)
    rows = run_pedk(load_cases(args.cases))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row))
            handle.write("\n")
    print(json.dumps({"rule_id": RULE_ID, "row_count": len(rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
