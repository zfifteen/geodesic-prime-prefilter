#!/usr/bin/env python3
"""Public N-only thread triangulation runner with ratio-derived controls."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

RETENTION_DIVISOR = 1024
THREAD_COUNT_NUMERATOR = 3
THREAD_COUNT_DENOMINATOR = 8
DEPTH_NUMERATOR = 5
DEPTH_DENOMINATOR = 12


def private_token_labels() -> tuple[str, ...]:
    return (
        "p" + " =",
        "q" + " =",
        "CA" + "SE",
        "known_" + "factor",
        "factor_" + "distance",
        "exact_" + "factor_" + "rank",
        "target_" + "distance",
        "private_" + "distance",
        "g" + "cd",
        "factor" + "int",
        "is" + "prime",
        "next" + "prime",
        "sq" + "rt",
        "rand" + "om",
    )


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_token_scan() -> dict[str, bool]:
    source_text = Path(__file__).read_text(encoding="utf-8")
    return {token: token in source_text for token in private_token_labels()}


def public_radius(n_value: int) -> int:
    return 1 << ((n_value.bit_length() + 1) // 2)


def original_space_size(n_value: int) -> int:
    return (public_radius(n_value) + 1) // 2


def ceil_ratio(value: int, numerator: int, denominator: int) -> int:
    return (value * numerator + denominator - 1) // denominator


def active_thread_count(n_value: int) -> int:
    return ceil_ratio(public_radius(n_value).bit_length(), THREAD_COUNT_NUMERATOR, THREAD_COUNT_DENOMINATOR)


def min_depth_for(thread_count: int) -> int:
    return ceil_ratio(thread_count, DEPTH_NUMERATOR, DEPTH_DENOMINATOR)


def max_candidates_for(n_value: int) -> int:
    return (original_space_size(n_value) + RETENTION_DIVISOR - 1) // RETENTION_DIVISOR


def odd_prime_stream(limit: int) -> tuple[int, ...]:
    primes: list[int] = []
    candidate = 3
    while len(primes) < limit:
        accepted = True
        for divisor in primes:
            if divisor * divisor > candidate:
                break
            if candidate % divisor == 0:
                accepted = False
                break
        if accepted:
            primes.append(candidate)
        candidate += 2
    return tuple(primes)


def crt_pair(base_modulus: int, base_residue: int, next_modulus: int, next_residue: int) -> tuple[int, int]:
    inverse = pow(base_modulus, -1, next_modulus)
    advance = ((next_residue - base_residue) * inverse) % next_modulus
    combined_modulus = base_modulus * next_modulus
    combined_residue = (base_residue + base_modulus * advance) % combined_modulus
    return combined_modulus, combined_residue


def smallest_positive_residue(modulus: int, residue: int) -> int:
    value = residue % modulus
    return modulus if value == 0 else value


def side_residue(n_value: int, thread: int, side: str) -> int:
    if side == "left":
        return n_value % thread
    return (-n_value) % thread


def thread_profile(
    n_value: int,
    distance: int,
    thread_set: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    left_threads = []
    right_threads = []
    for thread in thread_set:
        current = distance % thread
        if current == n_value % thread:
            left_threads.append(thread)
        if current == (-n_value) % thread:
            right_threads.append(thread)
    shared_threads = tuple(sorted(set(left_threads) & set(right_threads)))
    return tuple(left_threads), tuple(right_threads), shared_threads


def add_candidate(
    candidates: dict[int, dict[str, object]],
    n_value: int,
    distance: int,
    construction_depth: int,
    thread_set: tuple[int, ...],
    min_depth: int,
) -> None:
    left_threads, right_threads, shared_threads = thread_profile(n_value, distance, thread_set)
    left_count = len(left_threads)
    right_count = len(right_threads)
    total_count = left_count + right_count
    if construction_depth < min_depth:
        return
    row = candidates.get(distance)
    if row is None or construction_depth > int(row["triangulation_depth"]):
        candidates[distance] = {
            "distance": distance,
            "triangulation_depth": construction_depth,
            "left_thread_count": left_count,
            "right_thread_count": right_count,
            "total_thread_count": total_count,
            "shared_thread_count": len(shared_threads),
            "left_threads": list(left_threads),
            "right_threads": list(right_threads),
            "shared_threads": list(shared_threads),
            "score": [construction_depth, len(shared_threads), total_count, -distance],
        }


def extend_assignments(
    n_value: int,
    radius: int,
    thread_set: tuple[int, ...],
    min_depth: int,
    index: int,
    modulus: int,
    residue: int,
    construction_depth: int,
    candidates: dict[int, dict[str, object]],
) -> None:
    if index == len(thread_set):
        distance = smallest_positive_residue(modulus, residue)
        if distance <= radius:
            add_candidate(candidates, n_value, distance, construction_depth, thread_set, min_depth)
        return

    thread = thread_set[index]
    extend_assignments(
        n_value,
        radius,
        thread_set,
        min_depth,
        index + 1,
        modulus,
        residue,
        construction_depth,
        candidates,
    )
    for side in ("left", "right"):
        next_modulus, next_residue = crt_pair(modulus, residue, thread, side_residue(n_value, thread, side))
        distance = smallest_positive_residue(next_modulus, next_residue)
        next_depth = construction_depth + 1
        if distance <= radius:
            add_candidate(candidates, n_value, distance, next_depth, thread_set, min_depth)
        extend_assignments(
            n_value,
            radius,
            thread_set,
            min_depth,
            index + 1,
            next_modulus,
            next_residue,
            next_depth,
            candidates,
        )


def depth_counts(rows: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["triangulation_depth"])
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def nominate_with_explanatory_fields(n_value: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    radius = public_radius(n_value)
    thread_count = active_thread_count(n_value)
    thread_set = odd_prime_stream(thread_count)
    min_depth = min_depth_for(thread_count)
    max_candidates = max_candidates_for(n_value)
    candidates: dict[int, dict[str, object]] = {}
    extend_assignments(n_value, radius, thread_set, min_depth, 0, 2, 1, 1, candidates)
    qualified = list(candidates.values())
    rows = sorted(qualified, key=lambda row: row["score"], reverse=True)[:max_candidates]
    pre_cap_qualified_count = len(qualified)
    emitted_count = len(rows)
    if pre_cap_qualified_count == 0:
        max_depth = 0
    else:
        max_depth = max(int(row["triangulation_depth"]) for row in qualified)
    if emitted_count == 0:
        cutoff_depth = 0
        pre_cap_to_emitted_ratio = None
    else:
        cutoff_depth = int(rows[-1]["triangulation_depth"])
        pre_cap_to_emitted_ratio = pre_cap_qualified_count / emitted_count
    explanatory_fields = {
        "retention_divisor": RETENTION_DIVISOR,
        "thread_count_ratio": f"{THREAD_COUNT_NUMERATOR}/{THREAD_COUNT_DENOMINATOR}",
        "depth_ratio": f"{DEPTH_NUMERATOR}/{DEPTH_DENOMINATOR}",
        "active_thread_count": thread_count,
        "thread_set": list(thread_set),
        "min_depth": min_depth,
        "max_candidates": max_candidates,
        "pre_cap_qualified_count": pre_cap_qualified_count,
        "max_observed_triangulation_depth": max_depth,
        "depth_counts_pre_cap": depth_counts(qualified),
        "cap_active": pre_cap_qualified_count > max_candidates,
        "emitted_depth_counts": depth_counts(rows),
        "cutoff_triangulation_depth": cutoff_depth,
        "pre_cap_to_emitted_ratio": pre_cap_to_emitted_ratio,
    }
    return rows, explanatory_fields


def write_outputs(n_value: int, out_dir: Path, public_command: str) -> None:
    started = time.perf_counter()
    scan = private_token_scan()
    if any(scan.values()):
        print("PUBLIC_FREEZE_RECORD: missing_or_invalid")
        print("PRIVATE_AUDIT_UNLOCKED: false")
        print("STOPPING_BEFORE_PRIVATE_VALUES")
        raise SystemExit(2)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, explanatory_fields = nominate_with_explanatory_fields(n_value)
    out_file = out_dir / "public_output.jsonl"
    with out_file.open("w", encoding="utf-8", newline="\n") as handle:
        for rank, row in enumerate(rows, start=1):
            handle.write(json.dumps({"rank": rank, **row}, sort_keys=True) + "\n")
    space_size = original_space_size(n_value)
    emitted_count = len(rows)
    if emitted_count == 0:
        reduction_ratio = None
        reduction_bits = None
        reduction_status = "unresolved"
    else:
        reduction_ratio = f"{space_size}/{emitted_count}"
        reduction_bits = math.log2(space_size) - math.log2(emitted_count)
        reduction_status = "measured"
    manifest = {
        "N": n_value,
        "N_bits": n_value.bit_length(),
        "policy": "thread_triangulation_v02_ratio",
        "public_only": True,
        "public_radius": public_radius(n_value),
        "original_space_definition": "count of odd positive distances d with 1 <= d <= public_radius(N)",
        "original_space_size": space_size,
        "emitted_count": emitted_count,
        "candidate_reduction_ratio": reduction_ratio,
        "candidate_reduction_bits": reduction_bits,
        "reduction_status": reduction_status,
        "source_sha256": source_sha256(),
        "score_key": [
            "triangulation_depth descending",
            "shared_thread_count descending",
            "total_thread_count descending",
            "distance ascending",
        ],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    manifest.update(explanatory_fields)
    manifest_path = out_dir / "public_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PUBLIC_FREEZE_RECORD:")
    print(f"public_source_path: {Path(__file__).resolve()}")
    print(f"public_source_sha256: {source_sha256()}")
    print("public_source_private_token_scan: pass")
    for token, present in scan.items():
        print(f"  {token}: {present}")
    print(f"public_command: {public_command}")
    print(f"public_output_path: {out_file.resolve()}")
    print(f"public_output_sha256: {file_sha256(out_file)}")
    print(f"public_manifest_path: {manifest_path.resolve()}")
    print(f"public_manifest_sha256: {file_sha256(manifest_path)}")
    print(f"public_record_count: {emitted_count}")
    print(f"original_space_size: {space_size}")
    print(f"candidate_reduction_ratio: {reduction_ratio}")
    print(f"candidate_reduction_bits: {reduction_bits}")
    print(f"active_thread_count: {explanatory_fields['active_thread_count']}")
    print(f"min_depth: {explanatory_fields['min_depth']}")
    print(f"max_candidates: {explanatory_fields['max_candidates']}")
    print(f"pre_cap_qualified_count: {explanatory_fields['pre_cap_qualified_count']}")
    print(f"max_observed_triangulation_depth: {explanatory_fields['max_observed_triangulation_depth']}")
    print(f"depth_counts_pre_cap: {json.dumps(explanatory_fields['depth_counts_pre_cap'], sort_keys=True)}")
    print(f"cap_active: {explanatory_fields['cap_active']}")
    print(f"emitted_depth_counts: {json.dumps(explanatory_fields['emitted_depth_counts'], sort_keys=True)}")
    print(f"cutoff_triangulation_depth: {explanatory_fields['cutoff_triangulation_depth']}")
    print(f"pre_cap_to_emitted_ratio: {explanatory_fields['pre_cap_to_emitted_ratio']}")
    print("public_nominations_summary: see public_output.jsonl")
    print("PRIVATE_AUDIT_UNLOCKED: true")
    print(json.dumps(manifest, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    public_command = f"python3 {Path(__file__).name} --n {args.n} --out-dir {args.out_dir}"
    write_outputs(args.n, args.out_dir, public_command)


if __name__ == "__main__":
    main()
