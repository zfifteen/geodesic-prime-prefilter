#!/usr/bin/env python3
"""Run a minimal typed-coordinate RSA v2 PGS solver."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
EXPERIMENTS_DIR = THIS_DIR.parents[1]
DATA_LADDER_DIR = EXPERIMENTS_DIR / "data-ladder" / "rsa-v2"
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)


RULE_ID = "minimal_typed_coordinate_solver_v0"
PREVIOUS_ENDPOINT_WINDOW = 128
CERTIFICATE_MEASUREMENT_BOUND = 128
BALANCE_BAND = gmpy2.mpz(2)


@dataclass(frozen=True)
class LadderCase:
    """One public modulus row."""

    case_id: str
    bits: int
    n: gmpy2.mpz


@dataclass(frozen=True)
class Certificate:
    """One public PGS certificate at an endpoint anchor."""

    anchor: gmpy2.mpz
    reset_endpoint: gmpy2.mpz
    reset_deadline: gmpy2.mpz
    reset_signature: str


@dataclass(frozen=True)
class TypedClosure:
    """One reciprocal closure between typed certificate coordinates."""

    case: LadderCase
    lower_step: int
    lower_anchor: gmpy2.mpz
    lower_coordinate_role: str
    lower_coordinate_value: gmpy2.mpz
    upper_anchor: gmpy2.mpz
    upper_coordinate_role: str
    upper_coordinate_value: gmpy2.mpz
    lower_reset_signature: str
    upper_reset_signature: str
    lower_floor_drop: int
    upper_floor_drop: int


SegmentCache = dict[tuple[int, int], object]
PreviousEndpointCache = dict[int, gmpy2.mpz | None]
CertificateCache = dict[int, Certificate | None]


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


def load_cases(path: Path, max_bits: int) -> list[LadderCase]:
    """Load public ladder cases up to the requested public bit length."""
    cases: list[LadderCase] = []
    for row in read_jsonl(path):
        if "p" in row or "q" in row:
            raise ValueError("public case rows must not contain audit-only endpoints")
        bits = int(row["bits"])
        if bits <= max_bits:
            cases.append(
                LadderCase(
                    case_id=str(row["case_id"]),
                    bits=bits,
                    n=gmpy2.mpz(str(row["N"])),
                )
            )
    return cases


def divisor_counts_window(lo: int, hi: int, segment_cache: SegmentCache) -> object:
    """Return a cached exact divisor-count segment."""
    key = (lo, hi)
    if key not in segment_cache:
        segment_cache[key] = divisor_counts_segment(lo, hi)
    return segment_cache[key]


def previous_endpoint(
    value: gmpy2.mpz,
    segment_cache: SegmentCache,
) -> gmpy2.mpz | None:
    """Return the previous public endpoint before one coordinate."""
    hi = int(value)
    while hi > 2:
        lo = max(2, hi - PREVIOUS_ENDPOINT_WINDOW)
        counts = divisor_counts_window(lo, hi, segment_cache)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return gmpy2.mpz(lo + offset)
        hi = lo
    return None


def cached_previous_endpoint(
    value: gmpy2.mpz,
    previous_cache: PreviousEndpointCache,
    segment_cache: SegmentCache,
) -> gmpy2.mpz | None:
    """Return one cached previous endpoint."""
    key = int(value)
    if key not in previous_cache:
        previous_cache[key] = previous_endpoint(value, segment_cache)
    return previous_cache[key]


def reset_deadline(anchor: gmpy2.mpz, raw: dict[str, object]) -> tuple[gmpy2.mpz, str]:
    """Return the first public reset deadline and its signature."""
    tail_offsets = [int(offset) for offset in raw["tail_after_reset_offsets"]]
    threat_offset = (
        None
        if raw["lower_d_threat_offset"] is None
        else int(raw["lower_d_threat_offset"])
    )
    options: list[tuple[int, str]] = []
    if tail_offsets:
        options.append((tail_offsets[0], "tail"))
    if threat_offset is not None:
        options.append((threat_offset, "threat"))
    if not options:
        options.append((CERTIFICATE_MEASUREMENT_BOUND, "horizon"))
    offset, deadline_kind = min(options)
    signature = (
        f"carrier_d={raw['carrier_d']};"
        f"lock_carrier_d={raw['lock_carrier_d']};"
        f"threat={threat_offset is not None};"
        f"deadline={deadline_kind}"
    )
    return anchor + offset, signature


def certificate(anchor: gmpy2.mpz) -> Certificate | None:
    """Build one public PGS certificate."""
    raw = pgs_chamber_reset_state_certificate(
        int(anchor),
        CERTIFICATE_MEASUREMENT_BOUND,
    )
    if raw is None:
        return None
    deadline, signature = reset_deadline(anchor, raw)
    return Certificate(
        anchor=anchor,
        reset_endpoint=gmpy2.mpz(int(raw["q"])),
        reset_deadline=deadline,
        reset_signature=signature,
    )


def cached_certificate(
    anchor: gmpy2.mpz,
    certificate_cache: CertificateCache,
) -> Certificate | None:
    """Return one cached public PGS certificate."""
    key = int(anchor)
    if key not in certificate_cache:
        certificate_cache[key] = certificate(anchor)
    return certificate_cache[key]


def typed_coordinates(cert: Certificate) -> tuple[tuple[str, gmpy2.mpz], ...]:
    """Return the typed public coordinates carried by one certificate."""
    return (
        ("anchor", cert.anchor),
        ("reset_endpoint", cert.reset_endpoint),
        ("reset_deadline", cert.reset_deadline),
    )


def balance_bounds(center: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Return the public balanced interval around the square-root center."""
    return center // BALANCE_BAND, center * BALANCE_BAND


def floor_drop(n_value: gmpy2.mpz, coordinate: gmpy2.mpz) -> int:
    """Return the local drop in the public floor map after one coordinate."""
    return int((n_value // coordinate) - (n_value // (coordinate + 1)))


def closure_row(closure: TypedClosure) -> dict[str, object]:
    """Return a JSON-safe typed closure row."""
    return {
        "case_id": closure.case.case_id,
        "bits": closure.case.bits,
        "N": str(closure.case.n),
        "rule_id": RULE_ID,
        "lower_step": closure.lower_step,
        "lower_anchor": str(closure.lower_anchor),
        "lower_coordinate_role": closure.lower_coordinate_role,
        "lower_coordinate_value": str(closure.lower_coordinate_value),
        "upper_anchor": str(closure.upper_anchor),
        "upper_coordinate_role": closure.upper_coordinate_role,
        "upper_coordinate_value": str(closure.upper_coordinate_value),
        "reciprocal_forward_value": str(closure.upper_coordinate_value),
        "reciprocal_back_value": str(closure.lower_coordinate_value),
        "lower_reset_signature": closure.lower_reset_signature,
        "upper_reset_signature": closure.upper_reset_signature,
        "lower_floor_drop": closure.lower_floor_drop,
        "upper_floor_drop": closure.upper_floor_drop,
    }


def decisive_minimal_v0(closure: TypedClosure) -> bool:
    """Return whether the first typed closure is decisive for this minimal solver."""
    return (
        closure.lower_step <= 1
        and closure.lower_coordinate_role == "anchor"
        and closure.upper_coordinate_role == "reset_endpoint"
        and closure.lower_floor_drop > 1
        and closure.lower_reset_signature == closure.upper_reset_signature
    )


def first_typed_closure(case: LadderCase) -> tuple[TypedClosure | None, int]:
    """Return the first public typed reciprocal closure for one case."""
    center = gmpy2.isqrt(case.n)
    lower_balance, upper_balance = balance_bounds(center)
    segment_cache: SegmentCache = {}
    previous_cache: PreviousEndpointCache = {}
    certificate_cache: CertificateCache = {}
    lower_anchor = cached_previous_endpoint(center, previous_cache, segment_cache)
    lower_step = 0
    while lower_anchor is not None and lower_anchor >= lower_balance:
        lower = cached_certificate(lower_anchor, certificate_cache)
        if lower is not None:
            for lower_role, lower_value in typed_coordinates(lower):
                if lower_value > center:
                    continue
                transported = case.n // lower_value
                if transported < center or transported > upper_balance:
                    continue
                upper_anchor = cached_previous_endpoint(
                    transported,
                    previous_cache,
                    segment_cache,
                )
                if upper_anchor is None:
                    continue
                upper = cached_certificate(upper_anchor, certificate_cache)
                if upper is None:
                    continue
                for upper_role, upper_value in typed_coordinates(upper):
                    if transported == upper_value and case.n // upper_value == lower_value:
                        return (
                            TypedClosure(
                                case=case,
                                lower_step=lower_step,
                                lower_anchor=lower.anchor,
                                lower_coordinate_role=lower_role,
                                lower_coordinate_value=lower_value,
                                upper_anchor=upper.anchor,
                                upper_coordinate_role=upper_role,
                                upper_coordinate_value=upper_value,
                                lower_reset_signature=lower.reset_signature,
                                upper_reset_signature=upper.reset_signature,
                                lower_floor_drop=floor_drop(case.n, lower_value),
                                upper_floor_drop=floor_drop(case.n, upper_value),
                            ),
                            lower_step,
                        )
        lower_anchor = cached_previous_endpoint(lower_anchor, previous_cache, segment_cache)
        lower_step += 1
    return None, lower_step


def inference_row(case: LadderCase, closure: TypedClosure | None, steps: int) -> dict[str, object]:
    """Return one minimal solver inference row."""
    base: dict[str, object] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "implementation_label": "MINIMAL_TYPED_SOLVER_V0",
        "endpoint_steps_examined": steps,
    }
    if closure is None:
        return {
            **base,
            "status": "unresolved",
            "unresolved_reason": "unresolved_by_balance_boundary_exhaustion",
        }
    if decisive_minimal_v0(closure):
        return {
            **base,
            "status": "public_endpoint_class_found",
            "endpoint_class_lower": str(closure.lower_coordinate_value),
            "endpoint_class_upper": str(closure.upper_coordinate_value),
            "lower_coordinate_role": closure.lower_coordinate_role,
            "upper_coordinate_role": closure.upper_coordinate_role,
        }
    return {
        **base,
        "status": "unresolved",
        "unresolved_reason": "unresolved_by_first_typed_closure_not_decisive",
        "first_closure_lower_coordinate_role": closure.lower_coordinate_role,
        "first_closure_upper_coordinate_role": closure.upper_coordinate_role,
        "first_closure_lower_coordinate_value": str(closure.lower_coordinate_value),
        "first_closure_upper_coordinate_value": str(closure.upper_coordinate_value),
    }


def run_cases(cases: list[LadderCase]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Run every public case through the minimal typed solver."""
    inferences: list[dict[str, object]] = []
    closures: list[dict[str, object]] = []
    for case in cases:
        closure, steps = first_typed_closure(case)
        if closure is not None:
            closures.append(closure_row(closure))
        inferences.append(inference_row(case, closure, steps))
    return inferences, closures


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the minimal typed-coordinate RSA v2 solver.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=DATA_LADDER_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--max-bits",
        type=int,
        default=50,
        help="Maximum public modulus bit length to include.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output",
        help="Directory for minimal solver output rows.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the minimal typed-coordinate solver."""
    args = parse_args(argv)
    cases = load_cases(args.cases, args.max_bits)
    inferences, closures = run_cases(cases)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "minimal_inference_rows.jsonl", inferences)
    write_jsonl(args.output_dir / "typed_closure_rows.jsonl", closures)
    write_json(
        args.output_dir / "summary.json",
        {
            "rule_id": RULE_ID,
            "case_count": len(cases),
            "endpoint_class_count": sum(row["status"] == "public_endpoint_class_found" for row in inferences),
            "unresolved_count": sum(row["status"] == "unresolved" for row in inferences),
        },
    )
    print(json.dumps({"cases": inferences}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
