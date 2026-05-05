#!/usr/bin/env python3
"""Toy PGSPG certificate-pair factorizer for bounded semiprime surfaces."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)


RULE_ID = "toy_pgspg_mutual_reciprocal_endpoint_lock_v1"
SEED_ENDPOINT = 5
MIN_FACTOR = 10
DEFAULT_MAX_FACTOR = 99
CANDIDATE_BOUND = 32


@dataclass(frozen=True)
class PGSCertificate:
    """One public PGSPG reset certificate."""

    anchor: int
    reset_endpoint: int
    reset_deadline_value: int
    reset_signature: str
    carrier_d: int | None
    lock_carrier_d: int | None
    lower_d_threat_offset: int | None
    tail_after_reset_offsets: tuple[int, ...]


def reset_deadline_fields(anchor: int, raw: dict[str, object]) -> tuple[int, str]:
    """Return the local reset deadline and deadline kind."""
    tail_offsets = tuple(int(offset) for offset in raw["tail_after_reset_offsets"])
    threat_offset = (
        None
        if raw["lower_d_threat_offset"] is None
        else int(raw["lower_d_threat_offset"])
    )
    deadline_options: list[tuple[int, str]] = []
    if tail_offsets:
        deadline_options.append((tail_offsets[0], "tail"))
    if threat_offset is not None:
        deadline_options.append((threat_offset, "threat"))
    if not deadline_options:
        deadline_options.append((CANDIDATE_BOUND, "bound"))
    deadline_offset, deadline_kind = min(deadline_options)
    return anchor + deadline_offset, deadline_kind


def pgs_certificate(anchor: int) -> PGSCertificate | None:
    """Return one PGSPG certificate from a public anchor."""
    raw = pgs_chamber_reset_state_certificate(anchor, CANDIDATE_BOUND)
    if raw is None:
        return None
    reset_deadline, deadline_kind = reset_deadline_fields(anchor, raw)
    threat_offset = (
        None
        if raw["lower_d_threat_offset"] is None
        else int(raw["lower_d_threat_offset"])
    )
    reset_signature = (
        f"carrier_d={raw['carrier_d']};"
        f"lock_carrier_d={raw['lock_carrier_d']};"
        f"threat={threat_offset is not None};"
        f"deadline={deadline_kind}"
    )
    return PGSCertificate(
        anchor=anchor,
        reset_endpoint=int(raw["q"]),
        reset_deadline_value=reset_deadline,
        reset_signature=reset_signature,
        carrier_d=None if raw["carrier_d"] is None else int(raw["carrier_d"]),
        lock_carrier_d=(
            None if raw["lock_carrier_d"] is None else int(raw["lock_carrier_d"])
        ),
        lower_d_threat_offset=threat_offset,
        tail_after_reset_offsets=tuple(
            int(offset) for offset in raw["tail_after_reset_offsets"]
        ),
    )


def pgs_certificate_ladder(max_endpoint: int) -> list[PGSCertificate]:
    """Return the toy PGSPG endpoint ladder from the fixed seed endpoint."""
    certificates: list[PGSCertificate] = []
    anchor = SEED_ENDPOINT
    while anchor <= max_endpoint:
        certificate = pgs_certificate(anchor)
        if certificate is None:
            raise RuntimeError(f"PGSPG ladder stopped at anchor {anchor}")
        certificates.append(certificate)
        anchor = certificate.reset_endpoint
    return certificates


def reciprocal_floor(n_value: int, value: int) -> int:
    """Return the public reciprocal floor coordinate."""
    return n_value // value


def chamber_image_bounds(n_value: int, certificate: PGSCertificate) -> tuple[int, int]:
    """Return the reciprocal image of one native chamber."""
    return (
        reciprocal_floor(n_value, certificate.reset_deadline_value),
        reciprocal_floor(n_value, certificate.anchor),
    )


def chamber_inside_image(
    chamber: PGSCertificate,
    image_bounds: tuple[int, int],
) -> bool:
    """Return whether one native chamber is contained in one reciprocal image."""
    image_min, image_max = image_bounds
    return image_min <= chamber.anchor and chamber.reset_deadline_value <= image_max


def pair_row(n_value: int, lower: PGSCertificate, upper: PGSCertificate) -> dict[str, object]:
    """Return one public candidate-pair diagnostic row."""
    lower_image = chamber_image_bounds(n_value, lower)
    upper_image = chamber_image_bounds(n_value, upper)
    transported_upper = reciprocal_floor(n_value, lower.reset_endpoint)
    transported_lower = reciprocal_floor(n_value, upper.reset_endpoint)
    endpoint_locked = (
        transported_upper == upper.reset_endpoint
        and transported_lower == lower.reset_endpoint
    )
    return {
        "N": n_value,
        "lower_anchor": lower.anchor,
        "lower_reset_endpoint": lower.reset_endpoint,
        "lower_reset_deadline_value": lower.reset_deadline_value,
        "lower_reset_signature": lower.reset_signature,
        "lower_carrier_d": lower.carrier_d,
        "lower_lock_carrier_d": lower.lock_carrier_d,
        "lower_d_threat_offset": lower.lower_d_threat_offset,
        "lower_tail_after_reset_offsets": list(lower.tail_after_reset_offsets),
        "upper_anchor": upper.anchor,
        "upper_reset_endpoint": upper.reset_endpoint,
        "upper_reset_deadline_value": upper.reset_deadline_value,
        "upper_reset_signature": upper.reset_signature,
        "upper_carrier_d": upper.carrier_d,
        "upper_lock_carrier_d": upper.lock_carrier_d,
        "upper_d_threat_offset": upper.lower_d_threat_offset,
        "upper_tail_after_reset_offsets": list(upper.tail_after_reset_offsets),
        "transported_upper_endpoint": transported_upper,
        "transported_lower_endpoint": transported_lower,
        "lower_chamber_image_min": lower_image[0],
        "lower_chamber_image_max": lower_image[1],
        "upper_chamber_image_min": upper_image[0],
        "upper_chamber_image_max": upper_image[1],
        "upper_chamber_inside_lower_image": chamber_inside_image(upper, lower_image),
        "lower_chamber_inside_upper_image": chamber_inside_image(lower, upper_image),
        "mutual_reciprocal_endpoint_lock": endpoint_locked,
        "survives_rule_stack": endpoint_locked,
        "rule_id": RULE_ID,
    }


def candidate_pair_rows(
    n_value: int,
    max_factor: int = DEFAULT_MAX_FACTOR,
) -> list[dict[str, object]]:
    """Return every public PGSPG candidate pair on the bounded surface."""
    if max_factor < MIN_FACTOR:
        raise ValueError("max_factor must be at least 10")
    center = math.isqrt(n_value)
    certificates = pgs_certificate_ladder(max_factor)
    lower_certificates = [
        certificate
        for certificate in certificates
        if MIN_FACTOR <= certificate.reset_endpoint <= center
    ]
    upper_certificates = [
        certificate
        for certificate in certificates
        if center <= certificate.reset_endpoint <= max_factor
    ]
    return [
        pair_row(n_value, lower, upper)
        for lower in lower_certificates
        for upper in upper_certificates
    ]


def factorize(
    n_value: int,
    max_factor: int = DEFAULT_MAX_FACTOR,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the toy PGSPG factorizer without classical confirmation."""
    if n_value < 1:
        raise ValueError("N must be positive")
    rows = candidate_pair_rows(n_value, max_factor=max_factor)
    survivors = [row for row in rows if row["survives_rule_stack"]]
    if len(survivors) == 1:
        survivor = survivors[0]
        inference = {
            "N": n_value,
            "status": "resolved",
            "p": survivor["lower_reset_endpoint"],
            "q": survivor["upper_reset_endpoint"],
            "survivor_count": 1,
            "candidate_pair_count": len(rows),
            "rule_id": RULE_ID,
        }
    else:
        inference = {
            "N": n_value,
            "status": "unresolved",
            "unresolved_reason": "survivor_count_not_one",
            "survivor_count": len(survivors),
            "candidate_pair_count": len(rows),
            "rule_id": RULE_ID,
        }
    return inference, survivors


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the toy PGSPG factorizer.")
    parser.add_argument("N", type=int)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one public toy factorization case."""
    args = parse_args(argv)
    inference, survivors = factorize(args.N, max_factor=args.max_factor)
    print(json.dumps(inference, sort_keys=True))
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        write_jsonl(args.output_dir / "inference_rows.jsonl", [inference])
        write_jsonl(args.output_dir / "survivor_rows.jsonl", survivors)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
