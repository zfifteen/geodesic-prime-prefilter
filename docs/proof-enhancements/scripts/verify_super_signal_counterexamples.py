#!/usr/bin/env python3
"""Verify pinned Super-Signal counterexamples (audit-only classical tools).

Universal claim under test (INVALIDATED):
  If GWR witness w has z(w) >= 4 remainder zeros on
  M = (2, 3, 5, 7, 30, 210, 2310), then gap size g = 2.

Exit 0 if both counterexamples falsify the implication and GWR/zero
arithmetic matches the certificates. Exit 1 otherwise.

Repro:
  python3 docs/proof-enhancements/scripts/verify_super_signal_counterexamples.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT_DIR = ROOT / "docs" / "proof-enhancements" / "certificates" / "counterexamples"
MODULI = (2, 3, 5, 7, 30, 210, 2310)

# Pinned counterexamples (also in JSON certificates).
COUNTEREXAMPLES = (
    {
        "id": "ce_17666309",
        "p": 17_666_309,
        "q": 17_666_317,
        "gap": 8,
        "w": 17_666_310,
        "tau_w": 16,
        "zeros": 4,
    },
    {
        "id": "ce_22284029",
        "p": 22_284_029,
        "q": 22_284_037,
        "gap": 8,
        "w": 22_284_030,
        "tau_w": 16,
        "zeros": 4,
    },
)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def next_prime_after(p: int) -> int:
    n = p + 1 if p % 2 == 0 else p + 2
    if p == 2:
        return 3
    while not is_prime(n):
        n += 2
    return n


def tau(n: int) -> int:
    x = n
    t = 1
    e = 0
    while x % 2 == 0:
        e += 1
        x //= 2
    if e:
        t *= e + 1
    d = 3
    while d * d <= x:
        e = 0
        while x % d == 0:
            e += 1
            x //= d
        if e:
            t *= e + 1
        d += 2
    if x > 1:
        t *= 2
    return t


def remainder_zeros(n: int) -> tuple[list[int], int]:
    rem = [n % m for m in MODULI]
    return rem, sum(1 for r in rem if r == 0)


def gwr_witness(p: int, q: int) -> tuple[int, int]:
    """Leftmost interior minimum divisor count."""
    best_t = 10**18
    best_w = None
    for n in range(p + 1, q):
        t = tau(n)
        if t < best_t:
            best_t = t
            best_w = n
    assert best_w is not None
    return best_w, best_t


def verify_one(ce: dict) -> None:
    p, q = int(ce["p"]), int(ce["q"])
    assert is_prime(p), f"{ce['id']}: p not prime"
    assert is_prime(q), f"{ce['id']}: q not prime"
    assert next_prime_after(p) == q, f"{ce['id']}: not consecutive primes"
    gap = q - p
    assert gap == int(ce["gap"]), f"{ce['id']}: gap mismatch"
    assert gap > 2, f"{ce['id']}: expected non-twin gap"

    w, tw = gwr_witness(p, q)
    rem, z = remainder_zeros(w)
    assert w == int(ce["w"]), f"{ce['id']}: GWR mismatch {w} != {ce['w']}"
    assert tw == int(ce["tau_w"]), f"{ce['id']}: tau(w) mismatch"
    assert z == int(ce["zeros"]), f"{ce['id']}: zeros mismatch {z}"
    assert z >= 4, f"{ce['id']}: antecedent z>=4 failed"
    assert w % 30 == 0, f"{ce['id']}: modular half failed"

    implication_holds = (not (z >= 4)) or (gap == 2)
    assert not implication_holds, f"{ce['id']}: implication unexpectedly holds"

    print(f"OK {ce['id']}: p={p} q={q} g={gap} w={w} tau={tw} z={z} rem={rem}")
    print(f"   z(w)>=4 => g=2 holds? False  (INVALIDATES universal Super-Signal)")


def load_json_certs() -> None:
    for ce in COUNTEREXAMPLES:
        path = CERT_DIR / f"{ce['id']}.json"
        if not path.is_file():
            raise FileNotFoundError(f"missing certificate {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in ("p", "q", "gap", "w", "tau_w", "zeros"):
            if data.get(key) != ce[key]:
                raise AssertionError(
                    f"{path.name}: field {key}={data.get(key)!r} != pinned {ce[key]!r}"
                )


def main() -> int:
    load_json_certs()
    for ce in COUNTEREXAMPLES:
        verify_one(ce)
    print("RESULT: both counterexamples verified; universal implication invalidated")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 — script boundary
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
