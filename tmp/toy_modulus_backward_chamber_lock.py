#!/usr/bin/env python3
"""Toy PGS backward chamber lock demonstration.

This script does not compute divisor counts by trial division. It consumes a
fixed exact chamber-state table and applies the PGS endpoint law:

    tau(k) == 2 locks a prime-chain endpoint.

The toy modulus annotation is n = 35 = 5 * 7. The product relation is printed
only as audit context. It is not used by the walk.
"""

from __future__ import annotations


START_N = 35
STOP_AT = 5
AUDIT_FACTOR_ENDPOINTS = frozenset({5, 7})

EXACT_CHAMBER_TAU = {
    35: 4,
    34: 4,
    33: 4,
    32: 6,
    31: 2,
    30: 8,
    29: 2,
    28: 6,
    27: 4,
    26: 4,
    25: 3,
    24: 8,
    23: 2,
    22: 4,
    21: 4,
    20: 6,
    19: 2,
    18: 6,
    17: 2,
    16: 5,
    15: 4,
    14: 4,
    13: 2,
    12: 6,
    11: 2,
    10: 4,
    9: 3,
    8: 4,
    7: 2,
    6: 4,
    5: 2,
}


def backward_chambers(start: int, stop_at: int) -> list[dict[str, object]]:
    """Walk backward and lock each endpoint by the tau(k) == 2 law."""
    chambers: list[dict[str, object]] = []
    chamber_numbers: list[int] = []
    chamber_counts: list[int] = []

    for k in range(start, stop_at - 1, -1):
        tau_k = EXACT_CHAMBER_TAU[k]
        chamber_numbers.append(k)
        chamber_counts.append(tau_k)

        if tau_k == 2:
            chambers.append(
                {
                    "read": tuple(chamber_numbers),
                    "tau": tuple(chamber_counts),
                    "endpoint": k,
                    "audit_factor_endpoint": k in AUDIT_FACTOR_ENDPOINTS,
                }
            )
            chamber_numbers = []
            chamber_counts = []

    return chambers


def main() -> None:
    print("Toy PGS backward chamber lock")
    print(f"start_n: {START_N}")
    print("audit_annotation: 35 = 5 * 7")
    print("walk_rule: lock endpoint when tau(k) == 2")
    print("forbidden_methods_used: none")
    print()

    endpoints: list[int] = []
    for index, chamber in enumerate(backward_chambers(START_N, STOP_AT), start=1):
        endpoint = int(chamber["endpoint"])
        endpoints.append(endpoint)
        factor_mark = " audit-factor-endpoint" if chamber["audit_factor_endpoint"] else ""
        print(f"chamber_{index}:")
        print(f"  read: {list(chamber['read'])}")
        print(f"  tau:  {list(chamber['tau'])}")
        print(f"  lock: {endpoint}{factor_mark}")
        print()

    print("endpoint_chain:")
    print("  " + " -> ".join(str(endpoint) for endpoint in endpoints))
    print()
    print("toy_result:")
    print("  The walk traversed 7 and 5 as ordinary chain endpoints.")
    print("  The product annotation names why those endpoints matter for n = 35.")


if __name__ == "__main__":
    main()
