#!/usr/bin/env python3
"""Generate one provenance-logged RSA-like semiprime rung."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import gmpy2


DEFAULT_NAMESPACE = "PGS_ladder_50bit_v1"
DEFAULT_BITS = 50
DEFAULT_PRIME_BITS = 25
DEFAULT_MIN_GAP = 1 << 12
DEFAULT_CASE_ID = "rsa_v2_50bit_static_001"
DEFAULT_DESCRIPTION = "50-bit externally generated RSA-like ladder rung."


@dataclass(frozen=True)
class CandidatePrime:
    """One deterministic generated prime candidate."""

    value: gmpy2.mpz
    counter: int


@dataclass(frozen=True)
class GeneratedRung:
    """One generated semiprime rung and its provenance."""

    case_id: str
    description: str
    bits: int
    prime_bits: int
    namespace: str
    p: gmpy2.mpz
    q: gmpy2.mpz
    n: gmpy2.mpz
    p_counter: int
    q_counter: int


def stable_digest(namespace: str, label: str, counter: int) -> bytes:
    """Return one deterministic SHA-256 digest for the generator stream."""
    payload = f"{namespace}:{label}:{counter}".encode("utf-8")
    return hashlib.sha256(payload).digest()


def candidate_from_digest(digest: bytes, prime_bits: int) -> gmpy2.mpz:
    """Return one odd prime-sized candidate from one digest."""
    byte_length = (prime_bits + 7) // 8
    value = int.from_bytes(digest[:byte_length], "big")
    # The bit mask keeps only the requested prime-size coordinate width.
    value &= (1 << prime_bits) - 1
    # The top bit fixes the candidate in the requested prime-size band.
    value |= 1 << (prime_bits - 1)
    # The low bit makes the candidate odd before primality testing.
    value |= 1
    return gmpy2.mpz(value)


def deterministic_prime(namespace: str, label: str, prime_bits: int) -> CandidatePrime:
    """Return the first prime in one deterministic SHA-256 counter stream."""
    counter = 0
    while True:
        candidate = candidate_from_digest(
            stable_digest(namespace, label, counter),
            prime_bits,
        )
        if candidate.bit_length() != prime_bits:
            raise AssertionError("candidate left the fixed prime-size band")
        if gmpy2.is_prime(candidate, 100):
            return CandidatePrime(candidate, counter)
        counter += 1


def generate_rung(
    case_id: str,
    description: str,
    bits: int,
    prime_bits: int,
    namespace: str,
    min_gap: int,
) -> GeneratedRung:
    """Generate the first semiprime satisfying the predeclared public criteria."""
    q_stream_index = 0
    p_candidate = deterministic_prime(namespace, "p", prime_bits)
    while True:
        q_candidate = deterministic_prime(namespace, f"q:{q_stream_index}", prime_bits)
        if p_candidate.value != q_candidate.value:
            p_value = min(p_candidate.value, q_candidate.value)
            q_value = max(p_candidate.value, q_candidate.value)
            # The prime gap guard prevents an artificially near-square duplicate pair.
            gap = q_value - p_value
            # The product constructs the public semiprime modulus for the rung.
            n_value = p_value * q_value
            if gap >= min_gap and n_value.bit_length() == bits:
                return GeneratedRung(
                    case_id=case_id,
                    description=description,
                    bits=bits,
                    prime_bits=prime_bits,
                    namespace=namespace,
                    p=p_value,
                    q=q_value,
                    n=n_value,
                    p_counter=p_candidate.counter,
                    q_counter=q_candidate.counter,
                )
        q_stream_index += 1


def public_snippet(rung: GeneratedRung) -> dict[str, object]:
    """Return the public ladder-spec row for one generated rung."""
    return {
        "case_id": rung.case_id,
        "description": rung.description,
        "N": str(rung.n),
    }


def audit_snippet(rung: GeneratedRung) -> dict[str, object]:
    """Return the separate audit-spec row for one generated rung."""
    return {
        "case_id": rung.case_id,
        "p": str(rung.p),
        "q": str(rung.q),
    }


def provenance(rung: GeneratedRung, min_gap: int) -> dict[str, object]:
    """Return the full generation provenance for one rung."""
    return {
        "generator": "experiments/rsa/v2/generate_ladder_rung.py",
        "case_id": rung.case_id,
        "description": rung.description,
        "namespace": rung.namespace,
        "bits": rung.bits,
        "prime_bits": rung.prime_bits,
        "min_gap": min_gap,
        "primality_test": "gmpy2.is_prime(candidate, 100)",
        "selection_rule": "first pair from fixed SHA-256 counter streams satisfying all criteria",
        "criteria": {
            "p_bit_length": rung.prime_bits,
            "q_bit_length": rung.prime_bits,
            "N_bit_length": rung.bits,
            "p_not_equal_q": True,
            "q_minus_p_at_least": min_gap,
        },
        "p_counter": rung.p_counter,
        "q_counter": rung.q_counter,
        "public_ladder_spec_row": public_snippet(rung),
        "audit_spec_row": audit_snippet(rung),
    }


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate one isolated RSA-like semiprime ladder rung."
    )
    parser.add_argument("--case-id", default=DEFAULT_CASE_ID)
    parser.add_argument("--description", default=DEFAULT_DESCRIPTION)
    parser.add_argument("--bits", type=int, default=DEFAULT_BITS)
    parser.add_argument("--prime-bits", type=int, default=DEFAULT_PRIME_BITS)
    parser.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    parser.add_argument("--min-gap", type=int, default=DEFAULT_MIN_GAP)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "generated" / "rung_50bit_provenance.json",
        help="Path for provenance JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Generate one rung and write its provenance JSON."""
    args = parse_args(argv)
    rung = generate_rung(
        case_id=str(args.case_id),
        description=str(args.description),
        bits=int(args.bits),
        prime_bits=int(args.prime_bits),
        namespace=str(args.namespace),
        min_gap=int(args.min_gap),
    )
    payload = provenance(rung, int(args.min_gap))
    write_json(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
