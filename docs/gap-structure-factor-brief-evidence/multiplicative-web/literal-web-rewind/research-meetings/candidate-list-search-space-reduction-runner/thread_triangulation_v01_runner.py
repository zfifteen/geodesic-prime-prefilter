#!/usr/bin/env python3
"""Public N-only thread triangulation candidate-list runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

# Frozen v01 values per design_contract.html in this meeting folder.
THREAD_SET = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
MIN_DEPTH = 5
MAX_CANDIDATES = 512


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


def thread_profile(n_value: int, distance: int) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    left_threads = []
    right_threads = []
    for thread in THREAD_SET:
        current = distance % thread
        if current == n_value % thread:
            left_threads.append(thread)
        if current == (-n_value) % thread:
            right_threads.append(thread)
    shared_threads = tuple(sorted(set(left_threads) & set(right_threads)))
    return tuple(left_threads), tuple(right_threads), shared_threads


def add_candidate(candidates: dict[int, dict[str, object]], n_value: int, distance: int, construction_depth: int) -> None:
    left_threads, right_threads, shared_threads = thread_profile(n_value, distance)
    left_count = len(left_threads)
    right_count = len(right_threads)
    total_count = left_count + right_count
    if construction_depth < MIN_DEPTH:
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
    index: int,
    modulus: int,
    residue: int,
    construction_depth: int,
    candidates: dict[int, dict[str, object]],
) -> None:
    if index == len(THREAD_SET):
        distance = smallest_positive_residue(modulus, residue)
        if distance <= radius:
            add_candidate(candidates, n_value, distance, construction_depth)
        return

    thread = THREAD_SET[index]
    extend_assignments(n_value, radius, index + 1, modulus, residue, construction_depth, candidates)
    for side in ("left", "right"):
        next_modulus, next_residue = crt_pair(modulus, residue, thread, side_residue(n_value, thread, side))
        distance = smallest_positive_residue(next_modulus, next_residue)
        next_depth = construction_depth + 1
        if distance <= radius:
            add_candidate(candidates, n_value, distance, next_depth)
        extend_assignments(n_value, radius, index + 1, next_modulus, next_residue, next_depth, candidates)


def nominate(n_value: int) -> list[dict[str, object]]:
    radius = public_radius(n_value)
    candidates: dict[int, dict[str, object]] = {}
    extend_assignments(n_value, radius, 0, 2, 1, 1, candidates)
    rows = sorted(candidates.values(), key=lambda row: row["score"], reverse=True)
    return rows[:MAX_CANDIDATES]


def write_outputs(n_value: int, out_dir: Path, public_command: str) -> None:
    started = time.perf_counter()
    scan = private_token_scan()
    if any(scan.values()):
        print("PUBLIC_FREEZE_RECORD: missing_or_invalid")
        print("PRIVATE_AUDIT_UNLOCKED: false")
        print("STOPPING_BEFORE_PRIVATE_VALUES")
        raise SystemExit(2)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = nominate(n_value)
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
        "policy": "thread_triangulation_v01",
        "public_only": True,
        "thread_set": list(THREAD_SET),
        "min_depth": MIN_DEPTH,
        "max_candidates": MAX_CANDIDATES,
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
    print("public_nominations_summary:")
    for rank, row in enumerate(rows[:30], start=1):
        print(f"  - rank: {rank}")
        print(f"    distance: {row['distance']}")
        print(f"    score: {row['score']}")
    print("PRIVATE_AUDIT_UNLOCKED: true")
    print(json.dumps(manifest, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    public_command = f"python3 thread_triangulation_v01_runner.py --n {args.n} --out-dir {args.out_dir}"
    write_outputs(args.n, args.out_dir, public_command)


if __name__ == "__main__":
    main()
