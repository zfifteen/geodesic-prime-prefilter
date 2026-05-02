#!/usr/bin/env python3
"""Generate an OpenSSL-backed 150-bit semiprime and run the RSA probe."""

from __future__ import annotations

import csv
import math
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "experiments" / "rsa"))

from run_inference_elimination_probe import ToyCase, run_case


OUTPUT_PATH = Path("experiments/rsa/kitchen/openssl_150bit_semiprime_probe.csv")
PRIME_BITS = 75
MAX_SEED_ATTEMPTS = 64
MAX_NEARBY_SCAN = 1_000_000
TARGET_GAP = 1 << 20
GENERATION_POLICY = "openssl_prime_seed_plus_openssl_prime_at_target_gap_no_pgs_filter"


def openssl_prime_generate(bits: int) -> int:
    """Generate one prime with OpenSSL."""
    result = subprocess.run(
        ["openssl", "prime", "-generate", "-bits", str(bits)],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.strip())


def openssl_is_prime(value: int) -> bool:
    """Return whether OpenSSL reports value as prime."""
    result = subprocess.run(
        ["openssl", "prime", str(value)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().endswith(" is prime")


def generate_seed_prime() -> int:
    """Generate a 75-bit seed prime whose square is 150 bits."""
    for _ in range(MAX_SEED_ATTEMPTS):
        candidate = openssl_prime_generate(PRIME_BITS)
        if (candidate * candidate).bit_length() == 150:
            return candidate
    raise RuntimeError("OpenSSL did not generate a usable 150-bit seed prime")


def prime_at_or_after(value: int) -> int:
    """Find the next prime at or above value using OpenSSL primality checks."""
    candidate = value if value % 2 else value + 1
    for _ in range(MAX_NEARBY_SCAN):
        if openssl_is_prime(candidate):
            return candidate
        candidate += 2
    raise RuntimeError("nearby OpenSSL prime scan exceeded bound")


def audit_hidden_factor_rank(p: int, q: int, survivors: list[dict[str, object]]) -> int | None:
    """Return the first survivor rank containing either hidden factor."""
    hidden = {p, q}
    for row in survivors:
        if int(row["d"]) in hidden:
            return int(row["rank"])
    return None


def main() -> int:
    p = generate_seed_prime()
    q = prime_at_or_after(p + TARGET_GAP)
    n = p * q
    sqrt_n = math.isqrt(n)
    radius = max(abs(sqrt_n - p), abs(q - sqrt_n)) + 256
    case = ToyCase("openssl_150bit_nearby", n, radius, 2)

    summary, survivors = run_case(case)
    factor_rank = audit_hidden_factor_rank(p, q, survivors)

    row = {
        "case_id": case.case_id,
        "generation_policy": GENERATION_POLICY,
        "p": p,
        "q": q,
        "N": n,
        "bits": n.bit_length(),
        "gap": q - p,
        "radius": radius,
        "generated": summary["generated"],
        "post_wheel": int(summary["generated"])
        - int(summary["balance_rejected"])
        - int(summary["wheel_rejected"]),
        "pgs_rule_x_rejected": int(summary["pgs_chamber_rejected"])
        + int(summary["rule_x_rejected"]),
        "survivors": summary["survivors"],
        "false_rejection": int(factor_rank is None),
        "factor_rank": "" if factor_rank is None else factor_rank,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)

    print(",".join(row.keys()))
    print(",".join(str(value) for value in row.values()))
    print(f"wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
