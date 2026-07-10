#!/usr/bin/env python3
"""Build public-only scale corpora for A1 instrumentation.

Fixture generation may use deterministic arithmetic to form public moduli.
The resulting JSONL files contain only case_id, bits, N (no private factors).
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

# Fixed public ladder anchors reused as seeds for scale instrumentation.
KNOWN_PUBLIC = [
    {
        "case_id": "rsa_v2_40bit_static_001",
        "bits": 40,
        "N": "1099507433251",
    },
    {
        "case_id": "rsa_v2_50bit_static_001",
        "bits": 50,
        "N": "1027435935526951",
    },
    {
        "case_id": "rsa_v2_64bit_static_001",
        "bits": 64,
        "N": "10376454699372036973",
    },
    {
        "case_id": "rsa_v2_128bit_static_001",
        "bits": 127,
        "N": "85070591730234615902737140005361155371",
    },
    {
        "case_id": "rsa_v2_256bit_static_001",
        "bits": 256,
        "N": "57896044618658097711785492504343955952566120322525139588585136554122987719313",
    },
]


def _is_probable_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for fixture generation only (not inference)."""
    if n < 2:
        return False
    # small primes
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        if n % p == 0:
            return n == p
    # write n-1 = d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Deterministic bases sufficient for 64-bit; extended set for larger fixture build.
    bases = (2, 3, 5, 7, 11, 13, 23, 29, 31, 37)
    for a in bases:
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        skip = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                skip = True
                break
        if skip:
            continue
        return False
    return True


def _next_prime(n: int) -> int:
    if n <= 2:
        return 2
    if n % 2 == 0:
        n += 1
    while not _is_probable_prime(n):
        n += 2
    return n


def generate_public_semiprimes(bit_length: int, count: int, seed: int) -> list[dict[str, object]]:
    """Generate public-only semiprime rows. Factors never written."""
    rng = random.Random(seed)
    half = bit_length // 2
    rows: list[dict[str, object]] = []
    seen: set[int] = set()
    attempts = 0
    while len(rows) < count and attempts < count * 200:
        attempts += 1
        # Random odd starts near 2^(half-1)
        lo = 1 << (half - 1)
        hi = (1 << half) - 1
        a = rng.randrange(lo | 1, hi, 2)
        b = rng.randrange(lo | 1, hi, 2)
        p = _next_prime(a)
        q = _next_prime(b)
        if p == q:
            q = _next_prime(q + 2)
        n = p * q
        if n in seen:
            continue
        if n.bit_length() < bit_length - 1 or n.bit_length() > bit_length + 1:
            continue
        seen.add(n)
        rows.append(
            {
                "case_id": f"a1_corpus_{bit_length}bit_{len(rows):03d}_seed{seed}",
                "bits": int(n.bit_length()),
                "N": str(n),
            }
        )
    if len(rows) < count:
        raise RuntimeError(f"only generated {len(rows)}/{count} for {bit_length}-bit seed={seed}")
    return rows


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            if "p" in row or "q" in row:
                raise ValueError("public corpus must not contain factors")
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent / "corpora")
    parser.add_argument("--seed", type=int, default=20260709)
    args = parser.parse_args()

    # Regression-scale public anchors
    write_jsonl(args.out_dir / "known_public_anchors.jsonl", KNOWN_PUBLIC)

    # A1-TP guidance: 32 @ 128, 16 @ 256, 4 @ 512
    c128 = generate_public_semiprimes(128, 32, args.seed)
    c256 = generate_public_semiprimes(256, 16, args.seed + 1)
    c512 = generate_public_semiprimes(512, 4, args.seed + 2)
    write_jsonl(args.out_dir / "corpus_128bit.jsonl", c128)
    write_jsonl(args.out_dir / "corpus_256bit.jsonl", c256)
    write_jsonl(args.out_dir / "corpus_512bit.jsonl", c512)

    recipe = {
        "seed": args.seed,
        "generator": "build_corpora.py",
        "counts": {"128": len(c128), "256": len(c256), "512": len(c512)},
        "public_fields_only": ["case_id", "bits", "N"],
        "note": "Factors are never written. Miller-Rabin used only in fixture construction, not inference.",
    }
    (args.out_dir / "GENERATION_RECIPE.json").write_text(
        json.dumps(recipe, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(recipe, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
