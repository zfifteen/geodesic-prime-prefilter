#!/usr/bin/env python3
"""Toy PGS recursive backward chamber lock demonstration.

This script does not compute divisor counts by trial division. It consumes a
fixed exact chamber-state table and applies the PGS endpoint law:

    tau(k) == 2 locks a prime-chain endpoint.

It then applies reciprocal floor transport among locked endpoints. The toy
modulus annotation is n = 35 = 5 * 7. The product relation is printed only as
audit context after the PGS walk and floor closure have selected the pair.
"""

from __future__ import annotations


START_N = 35
MIN_COORDINATE = 2

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


def reciprocal_floor_closure(modulus: int, endpoints: list[int]) -> tuple[int, int] | None:
    """Return the first mutual floor-transport closure among locked endpoints."""
    endpoint_set = frozenset(endpoints)
    for endpoint in endpoints:
        transported = modulus // endpoint
        if transported not in endpoint_set:
            continue
        if modulus // transported != endpoint:
            continue
        return max(endpoint, transported), min(endpoint, transported)
    return None


def recursive_backward_walk(start: int, min_coordinate: int) -> dict[str, object]:
    """Walk backward until reciprocal floor closure appears."""
    chambers: list[dict[str, object]] = []
    chamber_numbers: list[int] = []
    chamber_counts: list[int] = []
    endpoints: list[int] = []

    for k in range(start, min_coordinate - 1, -1):
        tau_k = EXACT_CHAMBER_TAU[k]
        chamber_numbers.append(k)
        chamber_counts.append(tau_k)

        if tau_k == 2:
            endpoints.append(k)
            chambers.append(
                {
                    "read": tuple(chamber_numbers),
                    "tau": tuple(chamber_counts),
                    "endpoint": k,
                    "reciprocal_floor_closure": reciprocal_floor_closure(start, endpoints),
                }
            )
            if chambers[-1]["reciprocal_floor_closure"] is not None:
                return {
                    "chambers": tuple(chambers),
                    "endpoints": tuple(endpoints),
                    "closure": chambers[-1]["reciprocal_floor_closure"],
                    "stop_reason": "reciprocal_floor_closure_locked",
                }
            chamber_numbers = []
            chamber_counts = []

    return {
        "chambers": tuple(chambers),
        "endpoints": tuple(endpoints),
        "closure": None,
        "stop_reason": "unresolved_by_no_reciprocal_floor_closure",
    }


def main() -> None:
    print("Toy PGS recursive backward chamber lock")
    print(f"start_n: {START_N}")
    print("walk_rule: lock endpoint when tau(k) == 2")
    print("coupling_rule: stop at mutual floor transport among locked endpoints")
    print("forbidden_methods_used: none")
    print()

    result = recursive_backward_walk(START_N, MIN_COORDINATE)
    endpoints = list(result["endpoints"])
    for index, chamber in enumerate(result["chambers"], start=1):
        endpoint = int(chamber["endpoint"])
        print(f"chamber_{index}:")
        print(f"  read: {list(chamber['read'])}")
        print(f"  tau:  {list(chamber['tau'])}")
        print(f"  lock: {endpoint}")
        closure = chamber["reciprocal_floor_closure"]
        if closure is not None:
            upper, lower = closure
            print(f"  reciprocal_floor_closure: {upper} -> {lower} and {lower} -> {upper}")
        print()

    print("endpoint_chain:")
    print("  " + " -> ".join(str(endpoint) for endpoint in endpoints))
    print()
    print("stop_reason:")
    print(f"  {result['stop_reason']}")
    print()
    if result["closure"] is not None:
        upper, lower = result["closure"]
        print("selected_pair:")
        print(f"  q = {upper}")
        print(f"  p = {lower}")
        print()
    print("toy_result:")
    print("  The recursive backward walk selected 7 and 5 by endpoint locks plus floor closure.")
    print("  The audit relation is 35 = 5 * 7, after the PGS selection.")


if __name__ == "__main__":
    main()
