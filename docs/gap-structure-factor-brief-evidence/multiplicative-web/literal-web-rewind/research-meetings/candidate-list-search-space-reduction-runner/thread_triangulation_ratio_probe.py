#!/usr/bin/env python3
"""Public N-only thread triangulation probe with explicit public ratio inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path


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


def select_best_threads(n_value: int, count: int) -> tuple[int, ...]:
    """Public, cheap, N-adaptive thread selection.
    Scores primes by residue quality + diversity of short distances they can support.
    """
    pool = odd_prime_stream(count * 5)
    scored = []
    radius = public_radius(n_value)
    for p in pool:
        r = n_value % p
        r2 = p - r
        residue_quality = min(r, r2)
        diversity = min(12, (radius // (p * 2)) + 2)
        score = residue_quality * 10 - diversity
        scored.append((score, p))
    scored.sort()
    return tuple(p for _, p in scored[:count])


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
    extend_assignments(n_value, radius, thread_set, min_depth, index + 1, modulus, residue, construction_depth, candidates)
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


def nominate(n_value: int, args: argparse.Namespace) -> tuple[list[dict[str, object]], dict[str, object]]:
    radius = public_radius(n_value)
    thread_count = ceil_ratio(public_radius(n_value).bit_length(), args.thread_count_num, args.thread_count_den)
    max_candidates = (original_space_size(n_value) + args.retention_divisor - 1) // args.retention_divisor

    # Phase 1: Very aggressive broad pass (high budget, almost full power, very low bar)
    cheap_thread_count = max(5, int(thread_count * 0.9))
    cheap_min_depth = 1   # almost no filtering in Phase 1
    cheap_threads = select_best_threads(n_value, cheap_thread_count)
    candidates = {}
    extend_assignments(n_value, radius, cheap_threads, cheap_min_depth, 0, 2, 1, 1, candidates)
    qualified = list(candidates.values())

    # Phase 2: Extremely aggressive selective deepening (take a huge number of survivors)
    if qualified:
        m = min(2000, len(qualified) * 8)   # very large selection into deepening
        qualified.sort(key=lambda r: r.get("score", [0]), reverse=True)
        to_deepen = qualified[:m]

        # Use more threads in Phase 2 for higher quality
        deep_thread_count = thread_count + max(3, thread_count // 3)
        full_threads = select_best_threads(n_value, deep_thread_count)
        min_depth = ceil_ratio(thread_count, args.depth_num, args.depth_den)

        deepened = {}
        for row in to_deepen:
            d = row["distance"]
            left, right, shared = thread_profile(n_value, d, full_threads)
            total = len(left) + len(right)
            depth = total
            if depth >= min_depth:
                deepened[d] = {
                    "distance": d,
                    "triangulation_depth": depth,
                    "left_thread_count": len(left),
                    "right_thread_count": len(right),
                    "total_thread_count": total,
                    "shared_thread_count": len(shared),
                    "left_threads": list(left),
                    "right_threads": list(right),
                    "shared_threads": list(shared),
                    "score": [depth, len(shared), total, -d],
                }
        qualified = list(deepened.values())

    rows = sorted(qualified, key=lambda row: row.get("score", [0]), reverse=True)[:max_candidates]

    # Use full_threads for reporting if available
    active_threads = len(select_best_threads(n_value, thread_count)) if 'full_threads' in locals() else thread_count

    explanatory_fields = {
        "retention_divisor": args.retention_divisor,
        "thread_count_ratio": f"{args.thread_count_num}/{args.thread_count_den}",
        "depth_ratio": f"{args.depth_num}/{args.depth_den}",
        "active_thread_count": active_threads,
        "thread_set": list(select_best_threads(n_value, min(20, thread_count))),
        "min_depth": ceil_ratio(thread_count, args.depth_num, args.depth_den),
        "max_candidates": max_candidates,
        "pre_cap_qualified_count": len(qualified),
        "max_observed_triangulation_depth": max((int(row.get("triangulation_depth", 0)) for row in qualified), default=0),
        "depth_counts_pre_cap": depth_counts(qualified) if qualified else {},
        "cap_active": len(qualified) > max_candidates,
        "emitted_depth_counts": depth_counts(rows) if rows else {},
        "cutoff_triangulation_depth": int(rows[-1].get("triangulation_depth", 0)) if rows else 0,
        "pre_cap_to_emitted_ratio": (len(qualified) / len(rows)) if rows else None,
    }
    return rows, explanatory_fields


def write_outputs(n_value: int, out_dir: Path, public_command: str, args: argparse.Namespace) -> None:
    started = time.perf_counter()
    scan = private_token_scan()
    if any(scan.values()):
        print("PUBLIC_FREEZE_RECORD: missing_or_invalid")
        print("PRIVATE_AUDIT_UNLOCKED: false")
        print("STOPPING_BEFORE_PRIVATE_VALUES")
        raise SystemExit(2)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, explanatory_fields = nominate(n_value, args)
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
        "policy": "thread_triangulation_ratio_probe",
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
    print(f"cap_active: {explanatory_fields['cap_active']}")
    print("PRIVATE_AUDIT_UNLOCKED: true")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--thread-count-num", type=int, required=True)
    parser.add_argument("--thread-count-den", type=int, required=True)
    parser.add_argument("--depth-num", type=int, required=True)
    parser.add_argument("--depth-den", type=int, required=True)
    parser.add_argument("--retention-divisor", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    public_command = (
        f"python3 {Path(__file__).name} --n {args.n} --out-dir {args.out_dir} "
        f"--thread-count-num {args.thread_count_num} --thread-count-den {args.thread_count_den} "
        f"--depth-num {args.depth_num} --depth-den {args.depth_den} "
        f"--retention-divisor {args.retention_divisor}"
    )
    write_outputs(args.n, args.out_dir, public_command, args)


if __name__ == "__main__":
    main()
