#!/usr/bin/env python3
"""Test the low-prefix shortcut against the fold-transfer guard."""

from __future__ import annotations

import csv
import json
from collections import Counter
from itertools import product
from pathlib import Path


ENDPOINT_COUNT = 20000
ABSTRACT_ALPHABET = (2, 4, 6, 8, 10)
ABSTRACT_MAX_WORD_LENGTH = 8
CRITICAL_MARGIN_LIMIT = 100
LOW_VALUES = {0, 2}

OUT_DIR = Path(__file__).resolve().parent
SUMMARY_PATH = OUT_DIR / "2026-05-23-low_prefix_transfer_guard_summary.json"
CRITICAL_ROWS_PATH = OUT_DIR / "2026-05-23-low_prefix_transfer_guard_critical_rows.csv"
ABSTRACT_FAILURES_PATH = OUT_DIR / "2026-05-23-low_prefix_transfer_guard_abstract_failures.csv"


def divisor_count(n: int) -> int:
    if n < 1:
        raise ValueError("divisor_count expects a positive integer")
    remaining = n
    count = 1
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            exponent = 0
            while remaining % factor == 0:
                remaining //= factor
                exponent += 1
            count *= exponent + 1
        factor += 1 if factor == 2 else 2
    if remaining > 1:
        count *= 2
    return count


def next_endpoint_by_tau(endpoint: int) -> int:
    n = endpoint + 1
    while True:
        if divisor_count(n) == 2:
            return n
        n += 1


def endpoint_chain(count: int) -> list[int]:
    endpoints = [2]
    while len(endpoints) < count + 1:
        endpoints.append(next_endpoint_by_tau(endpoints[-1]))
    return endpoints


def difference_row(row: tuple[int, ...] | list[int]) -> list[int]:
    return [abs(row[i + 1] - row[i]) for i in range(len(row) - 1)]


def right_edge(word: tuple[int, ...] | list[int]) -> list[int]:
    edge: list[int] = []
    row = list(word)
    while row:
        edge.append(row[-1])
        row = difference_row(row)
    return edge


def append_right_edge(edge: list[int], next_gap: int) -> list[int]:
    value = next_gap
    new_edge = [next_gap]
    for entry in edge:
        value = abs(value - entry)
        new_edge.append(value)
    return new_edge


def low_prefix_len(word: tuple[int, ...] | list[int]) -> int:
    index = 1
    while index < len(word) and word[index] in LOW_VALUES:
        index += 1
    return index - 1


def transfer_guard(edge: list[int]) -> tuple[bool, int | None, int | None, int | None]:
    if not edge or edge[-1] != 1:
        return False, None, None, None
    ceiling = 2
    for lane in range(len(edge) - 2, -1, -1):
        entry = edge[lane]
        if entry > ceiling:
            return False, None, lane, ceiling
        ceiling += entry
    return True, ceiling, None, None


def first_open_offset(residue: int) -> int:
    for offset in (2, 4, 6, 8, 10, 12):
        candidate = (residue + offset) % 30
        if candidate % 3 != 0 and candidate % 5 != 0:
            return offset
    raise RuntimeError(f"no open offset for residue {residue}")


def integer_cube_root(n: int) -> int | None:
    low = 1
    high = n
    while low <= high:
        mid = (low + high) // 2
        cube = mid * mid * mid
        if cube == n:
            return mid
        if cube < n:
            low = mid + 1
        else:
            high = mid - 1
    return None


def carrier_family(winner: int, winner_d: int) -> str:
    if winner_d == 3:
        return "prime_square"
    if winner_d == 4:
        root = integer_cube_root(winner)
        if root is not None and divisor_count(root) == 2:
            return "prime_cube"
        if winner % 2 == 0:
            return "even_semiprime"
        return "odd_semiprime"
    if winner % 2 == 0:
        return "higher_divisor_even"
    return "higher_divisor_odd"


def gap_profile(left: int, right: int) -> dict[str, int | str]:
    if right - left <= 1:
        raise ValueError("gap has no interior integer")
    best_d: int | None = None
    best_offset: int | None = None
    for n in range(left + 1, right):
        d_value = divisor_count(n)
        if best_d is None or d_value < best_d:
            best_d = d_value
            best_offset = n - left
    assert best_d is not None
    assert best_offset is not None
    winner = left + best_offset
    family = carrier_family(winner, best_d)
    first_open = first_open_offset(left % 30)
    return {
        "first_open_offset": first_open,
        "winner_d": best_d,
        "winner_offset": best_offset,
        "carrier_family": family,
        "type_key": f"o{first_open}_d{best_d}_a{best_offset}_{family}",
    }


def admitted_even_candidates(edge: list[int], limit: int) -> list[int]:
    candidates: list[int] = []
    for candidate in range(2, limit + 1, 2):
        value = candidate
        for entry in edge:
            value = abs(value - entry)
        if value == 1:
            candidates.append(candidate)
    return candidates


def scan_actual_surface() -> dict[str, object]:
    endpoints = endpoint_chain(ENDPOINT_COUNT)
    gaps = [right - left for left, right in zip(endpoints, endpoints[1:])]
    edge = [gaps[0]]

    leading_failures = 0
    transfer_guard_failures = 0
    ceiling_failures = 0
    max_actual_gap = 0
    max_ceiling = 0
    min_margin: int | None = None
    pressure_counts: Counter[str] = Counter()
    max_prefix_by_band = {"0": None, "20": None, "100": None, "1000": None}
    critical_type_counts: Counter[str] = Counter()
    critical_gap_counts: Counter[int] = Counter()
    critical_rows: list[dict[str, int | str]] = []

    with CRITICAL_ROWS_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "prefix_index",
                "current_endpoint",
                "next_endpoint",
                "actual_next_gap",
                "transfer_ceiling",
                "ceiling_margin",
                "right_edge_tail",
                "first_open_offset",
                "winner_d",
                "winner_offset",
                "carrier_family",
                "type_key",
            ],
            lineterminator="\n",
        )
        writer.writeheader()

        for prefix_index, actual_next_gap in enumerate(gaps[1:], start=1):
            current_endpoint = endpoints[prefix_index]
            next_endpoint = endpoints[prefix_index + 1]
            max_actual_gap = max(max_actual_gap, actual_next_gap)

            if edge[-1] != 1:
                leading_failures += 1

            guard_ok, ceiling, failed_lane, failed_lane_ceiling = transfer_guard(edge)
            if not guard_ok:
                transfer_guard_failures += 1
                raise RuntimeError(
                    "actual PGS prefix failed transfer guard at "
                    f"prefix {prefix_index}, lane {failed_lane}, ceiling {failed_lane_ceiling}"
                )
            assert ceiling is not None
            max_ceiling = max(max_ceiling, ceiling)
            margin = ceiling - actual_next_gap
            if min_margin is None or margin < min_margin:
                min_margin = margin
            if margin < 0:
                ceiling_failures += 1

            if margin == 0:
                pressure_counts["tight"] += 1
                max_prefix_by_band["0"] = prefix_index
            elif margin <= 20:
                pressure_counts["1..20"] += 1
                max_prefix_by_band["20"] = prefix_index
            elif margin <= CRITICAL_MARGIN_LIMIT:
                pressure_counts["21..100"] += 1
                max_prefix_by_band["100"] = prefix_index
            elif margin <= 1000:
                pressure_counts["101..1000"] += 1
                max_prefix_by_band["1000"] = prefix_index
            else:
                pressure_counts[">1000"] += 1

            if margin <= 20:
                max_prefix_by_band["20"] = prefix_index
                max_prefix_by_band["100"] = prefix_index
                max_prefix_by_band["1000"] = prefix_index
            elif margin <= CRITICAL_MARGIN_LIMIT:
                max_prefix_by_band["100"] = prefix_index
                max_prefix_by_band["1000"] = prefix_index
            elif margin <= 1000:
                max_prefix_by_band["1000"] = prefix_index

            if margin <= CRITICAL_MARGIN_LIMIT:
                profile = gap_profile(current_endpoint, next_endpoint)
                critical_type_counts[str(profile["type_key"])] += 1
                critical_gap_counts[actual_next_gap] += 1
                record = {
                    "prefix_index": prefix_index,
                    "current_endpoint": current_endpoint,
                    "next_endpoint": next_endpoint,
                    "actual_next_gap": actual_next_gap,
                    "transfer_ceiling": ceiling,
                    "ceiling_margin": margin,
                    "right_edge_tail": " ".join(str(value) for value in edge[-12:]),
                    "first_open_offset": int(profile["first_open_offset"]),
                    "winner_d": int(profile["winner_d"]),
                    "winner_offset": int(profile["winner_offset"]),
                    "carrier_family": str(profile["carrier_family"]),
                    "type_key": str(profile["type_key"]),
                }
                writer.writerow(record)
                critical_rows.append(record)

            edge = append_right_edge(edge, actual_next_gap)

    return {
        "endpoint_count": ENDPOINT_COUNT,
        "seed_endpoint": 2,
        "final_endpoint": endpoints[-1],
        "prefix_extensions_checked": ENDPOINT_COUNT - 1,
        "leading_failures": leading_failures,
        "transfer_guard_failures": transfer_guard_failures,
        "actual_ceiling_failures": ceiling_failures,
        "max_actual_next_gap": max_actual_gap,
        "max_transfer_ceiling": max_ceiling,
        "min_ceiling_margin": min_margin,
        "pressure_counts": dict(sorted(pressure_counts.items())),
        "max_prefix_index_by_margin_band": max_prefix_by_band,
        "critical_margin_limit": CRITICAL_MARGIN_LIMIT,
        "critical_row_count": len(critical_rows),
        "critical_last_row": critical_rows[-1] if critical_rows else None,
        "critical_gap_counts": dict(sorted(critical_gap_counts.items())),
        "critical_type_counts": dict(critical_type_counts.most_common()),
    }


def scan_abstract_low_prefix_words() -> dict[str, object]:
    admitted_low_counts: Counter[int] = Counter()
    guard_failure_counts: Counter[int] = Counter()
    failure_lane_counts: Counter[int] = Counter()
    failure_value_counts: Counter[int] = Counter()
    minimal_failure: dict[str, object] | None = None
    failure_count = 0

    with ABSTRACT_FAILURES_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "word_length",
                "word",
                "right_edge",
                "low_prefix_len",
                "failed_lane",
                "failed_value",
                "lane_ceiling",
                "admitted_even_candidates_up_to_30",
            ],
            lineterminator="\n",
        )
        writer.writeheader()

        for word_length in range(2, ABSTRACT_MAX_WORD_LENGTH + 1):
            for tail in product(ABSTRACT_ALPHABET, repeat=word_length - 1):
                word = (1,) + tail
                ell = low_prefix_len(word)
                edge = right_edge(word)
                if edge[-1] != 1 or ell < 2:
                    continue

                admitted_low_counts[word_length] += 1
                guard_ok, _, failed_lane, lane_ceiling = transfer_guard(edge)
                if guard_ok:
                    continue

                assert failed_lane is not None
                assert lane_ceiling is not None
                failure_count += 1
                guard_failure_counts[word_length] += 1
                failure_lane_counts[failed_lane] += 1
                failure_value = edge[failed_lane]
                failure_value_counts[failure_value] += 1
                candidates = admitted_even_candidates(edge, 30)
                record = {
                    "word_length": word_length,
                    "word": ",".join(str(value) for value in word),
                    "right_edge": ",".join(str(value) for value in edge),
                    "low_prefix_len": ell,
                    "failed_lane": failed_lane,
                    "failed_value": failure_value,
                    "lane_ceiling": lane_ceiling,
                    "admitted_even_candidates_up_to_30": ",".join(
                        str(value) for value in candidates
                    ),
                }
                writer.writerow(record)
                if minimal_failure is None:
                    minimal_failure = dict(record)

    return {
        "alphabet": list(ABSTRACT_ALPHABET),
        "max_word_length": ABSTRACT_MAX_WORD_LENGTH,
        "admitted_low_prefix_counts_by_length": {
            str(key): admitted_low_counts[key] for key in sorted(admitted_low_counts)
        },
        "transfer_guard_failure_counts_by_length": {
            str(key): guard_failure_counts[key] for key in sorted(guard_failure_counts)
        },
        "transfer_guard_failure_count": failure_count,
        "failure_lane_counts": {
            str(key): failure_lane_counts[key] for key in sorted(failure_lane_counts)
        },
        "failure_value_counts": {
            str(key): failure_value_counts[key] for key in sorted(failure_value_counts)
        },
        "minimal_failure": minimal_failure,
        "invalidated_shortcut": (
            "Seeded prefix admission plus low-prefix length at least 2 does not imply "
            "the right-edge fold-transfer guard."
        ),
    }


def main() -> None:
    actual_surface = scan_actual_surface()
    abstract_surface = scan_abstract_low_prefix_words()
    summary = {
        "status": "ADVANCE",
        "headline": (
            "The low-prefix corridor does not imply the right-edge fold-transfer "
            "guard; actual PGS prefixes satisfy the guard on the measured surface."
        ),
        "actual_pgs_surface": actual_surface,
        "abstract_low_prefix_surface": abstract_surface,
        "proof_tree_change": (
            "The proof cannot derive fold admission from low-prefix depletion/reset "
            "alone. It must prove an actual ordered PGS endpoint-gap exclusion law "
            "for the abstract low-prefix guard-failure family, beginning with "
            "(1,2,2,6,2), or prove another PGS invariant that supplies the same "
            "right-edge guard."
        ),
        "theorem_status": "unresolved",
        "implementation_status": "deterministic exact-divisor-count endpoint probe plus finite abstract grammar enumeration",
        "audit_status": (
            "verify with probe rerun, json.tool on summary, py_compile on probe, "
            "HTMLParser on notes, git diff --check, and CR scan"
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
