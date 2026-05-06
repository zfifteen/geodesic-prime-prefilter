#!/usr/bin/env python3
"""Scale probe for the recursive PGS backward chamber walk.

The inference path is the same as the toy demonstrator:

1. walk backward from `n`;
2. lock an endpoint when `tau(k) == 2`;
3. after each lock, apply mutual floor transport among locked endpoints;
4. stop at the first reciprocal floor closure.

The exact chamber table is built once up front by the repository's exact
divisor-count field. That table-build step is deliberately outside the
inference rule measured here.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import AbstractSet, Sequence

from z_band_prime_composite_field import divisor_counts_segment


@dataclass(frozen=True)
class ScaleCase:
    """One deterministic semiprime scale case with audit-only endpoints."""

    label: str
    n: int
    expected_q: int
    expected_p: int


@dataclass(frozen=True)
class WalkResult:
    """Summary of one backward chamber walk."""

    n: int
    q: int
    p: int
    locked_endpoint_count: int
    chamber_rows_read: int
    first_locked_endpoint: int
    endpoint_prefix: tuple[int, ...]
    endpoint_suffix: tuple[int, ...]
    stop_reason: str


SCALE_CASES = (
    ScaleCase("toy_35", 35, 7, 5),
    ScaleCase("small_77", 77, 11, 7),
    ScaleCase("small_143", 143, 13, 11),
    ScaleCase("small_221", 221, 17, 13),
    ScaleCase("medium_899", 899, 31, 29),
    ScaleCase("large_10403", 10403, 103, 101),
    ScaleCase("large_1022117", 1022117, 1013, 1009),
)


def build_exact_chamber_table(max_n: int) -> tuple[int, ...]:
    """Build exact tau values for coordinates 2..max_n inclusive."""
    if max_n < 2:
        raise ValueError("max_n must be at least 2")
    return tuple(int(value) for value in divisor_counts_segment(2, max_n + 1))


def tau_from_table(table: Sequence[int], coordinate: int) -> int:
    """Read one tau value from a table indexed from coordinate 2."""
    if coordinate < 2:
        raise ValueError("coordinate must be at least 2")
    return int(table[coordinate - 2])


def closure_for_new_endpoint(
    modulus: int,
    endpoint_set: AbstractSet[int],
    endpoint: int,
) -> tuple[int, int] | None:
    """Return mutual floor closure for a newly locked endpoint."""
    transported = modulus // endpoint
    if transported not in endpoint_set:
        return None
    if modulus // transported != endpoint:
        return None
    return max(endpoint, transported), min(endpoint, transported)


def recursive_backward_walk(
    modulus: int,
    table: Sequence[int],
    min_coordinate: int = 2,
) -> WalkResult:
    """Walk backward until reciprocal floor closure appears."""
    endpoints: list[int] = []
    endpoint_set: set[int] = set()
    rows_read = 0

    for coordinate in range(modulus, min_coordinate - 1, -1):
        rows_read += 1
        if tau_from_table(table, coordinate) != 2:
            continue

        endpoints.append(coordinate)
        endpoint_set.add(coordinate)
        closure = closure_for_new_endpoint(
            modulus,
            endpoint_set,
            coordinate,
        )
        if closure is not None:
            q, p = closure
            return WalkResult(
                n=modulus,
                q=q,
                p=p,
                locked_endpoint_count=len(endpoints),
                chamber_rows_read=rows_read,
                first_locked_endpoint=endpoints[0],
                endpoint_prefix=tuple(endpoints[:8]),
                endpoint_suffix=tuple(endpoints[-8:]),
                stop_reason="reciprocal_floor_closure_locked",
            )

    raise RuntimeError("recursive backward walk did not floor-close")


def run_scale_probe(cases: Sequence[ScaleCase] = SCALE_CASES) -> tuple[WalkResult, ...]:
    """Run all scale cases against one exact chamber table."""
    max_n = max(case.n for case in cases)
    table = build_exact_chamber_table(max_n)
    return tuple(recursive_backward_walk(case.n, table) for case in cases)


def main() -> int:
    """Run the scale probe and print deterministic results."""
    table_start = perf_counter()
    max_n = max(case.n for case in SCALE_CASES)
    table = build_exact_chamber_table(max_n)
    table_elapsed = perf_counter() - table_start

    print("Recursive PGS backward chamber walk scale probe")
    print("inference_rule: endpoint tau lock plus reciprocal floor closure")
    print("table_build_boundary: exact chamber table built once before inference")
    print(f"max_n: {max_n}")
    print(f"table_build_seconds: {table_elapsed:.6f}")
    print()
    print(
        "case,n,selected_q,selected_p,locked_endpoints,chamber_rows_read,"
        "first_locked_endpoint,audit_match,stop_reason"
    )

    for case in SCALE_CASES:
        walk_start = perf_counter()
        result = recursive_backward_walk(case.n, table)
        walk_elapsed = perf_counter() - walk_start
        audit_match = result.q == case.expected_q and result.p == case.expected_p
        print(
            f"{case.label},{result.n},{result.q},{result.p},"
            f"{result.locked_endpoint_count},{result.chamber_rows_read},"
            f"{result.first_locked_endpoint},{audit_match},{result.stop_reason}"
        )
        print(f"  endpoint_prefix: {list(result.endpoint_prefix)}")
        print(f"  endpoint_suffix: {list(result.endpoint_suffix)}")
        print(f"  inference_seconds: {walk_elapsed:.6f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
