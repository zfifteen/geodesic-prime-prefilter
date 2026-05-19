#!/usr/bin/env python3
"""N-only sparse web nomination runner."""

from __future__ import annotations

import argparse
import json
import time
from itertools import combinations
from pathlib import Path

THREADS = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
ODD_THREADS = THREADS[1:]
EMIT_LIMIT = 30
MIN_THREAD_COUNT = 4


def public_radius(n_value: int) -> int:
    return 1 << ((n_value.bit_length() + 1) // 2)


def crt_pair(base_modulus: int, base_residue: int, next_modulus: int, next_residue: int) -> tuple[int, int]:
    inverse = pow(base_modulus, -1, next_modulus)
    advance = ((next_residue - base_residue) * inverse) % next_modulus
    combined_modulus = base_modulus * next_modulus
    combined_residue = (base_residue + base_modulus * advance) % combined_modulus
    return combined_modulus, combined_residue


def smallest_positive_residue(modulus: int, residue: int) -> int:
    value = residue % modulus
    return modulus if value == 0 else value


def thread_residue(n_value: int, thread: int, side: str) -> int:
    if side == "left":
        return n_value % thread
    return (-n_value) % thread


def nomination_rows(n_value: int) -> list[dict[str, object]]:
    radius = public_radius(n_value)
    rows: dict[int, dict[str, object]] = {}
    for side in ("left", "right"):
        for size in range(len(ODD_THREADS), MIN_THREAD_COUNT - 1, -1):
            for subset in combinations(ODD_THREADS, size):
                modulus = 2
                residue = 1
                for thread in subset:
                    modulus, residue = crt_pair(modulus, residue, thread, thread_residue(n_value, thread, side))
                distance = smallest_positive_residue(modulus, residue)
                if distance > radius:
                    continue
                row = rows.setdefault(
                    distance,
                    {
                        "distance": distance,
                        "left_threads": [],
                        "right_threads": [],
                    },
                )
                row[f"{side}_threads"] = sorted(set(row[f"{side}_threads"]) | set(subset) | {2})
    scored = []
    for row in rows.values():
        left_count = len(row["left_threads"])
        right_count = len(row["right_threads"])
        shared_count = len(set(row["left_threads"]) & set(row["right_threads"]))
        score = [max(left_count, right_count), shared_count, left_count + right_count, -int(row["distance"])]
        row["score"] = score
        row["left_thread_count"] = left_count
        row["right_thread_count"] = right_count
        row["shared_thread_count"] = shared_count
        scored.append(row)
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:EMIT_LIMIT]


def write_public_output(n_value: int, out_dir: Path) -> None:
    started = time.perf_counter()
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = nomination_rows(n_value)
    output_path = out_dir / "public_output.jsonl"
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for rank, row in enumerate(rows, start=1):
            handle.write(json.dumps({"rank": rank, **row}, sort_keys=True) + "\n")
    manifest = {
        "N": n_value,
        "N_bits": n_value.bit_length(),
        "policy": "n_only_sparse_web_crt_nomination",
        "public_only": True,
        "radius": public_radius(n_value),
        "threads": list(THREADS),
        "min_thread_count": MIN_THREAD_COUNT,
        "emit_limit": EMIT_LIMIT,
        "public_record_count": len(rows),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    (out_dir / "public_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_public_output(args.n, args.out_dir)


if __name__ == "__main__":
    main()
