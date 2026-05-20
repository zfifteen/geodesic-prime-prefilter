#!/usr/bin/env python3
"""Measure endpoint position inside the selected-d4 composite-boundary residual."""

from __future__ import annotations

import argparse
import csv
import json
from array import array
from math import isqrt
from pathlib import Path


def build_tau(limit: int) -> array:
    if limit < 4:
        raise ValueError("limit must be at least 4")

    spf = array("I", [0]) * (limit + 1)
    root = isqrt(limit)
    for i in range(2, root + 1):
        if spf[i] != 0:
            continue
        spf[i] = i
        for j in range(i * i, limit + 1, i):
            if spf[j] == 0:
                spf[j] = i

    for i in range(2, limit + 1):
        if spf[i] == 0:
            spf[i] = i

    tau = array("H", [0]) * (limit + 1)
    tau[1] = 1
    for x in range(2, limit + 1):
        prime_factor = spf[x]
        rest = x // prime_factor
        exponent = 1
        while rest > 1 and spf[rest] == prime_factor:
            rest //= prime_factor
            exponent += 1
        tau[x] = tau[rest] * (exponent + 1)
    return tau


def previous_endpoint(tau: array, start: int) -> int:
    x = start - 1
    while x >= 2:
        if tau[x] == 2:
            return x
        x -= 1
    raise ValueError(f"no tau=2 endpoint before {start}")


def next_endpoint(tau: array, start: int) -> int:
    x = start + 1
    while x < len(tau):
        if tau[x] == 2:
            return x
        x += 1
    raise ValueError(f"tau table ended before next endpoint after {start}")


def selected_witness(tau: array, p: int, q: int) -> tuple[int, int]:
    best_w = None
    best_tau = None
    for x in range(p + 1, q):
        d = int(tau[x])
        if best_tau is None or d < best_tau:
            best_w = x
            best_tau = d
    if best_w is None or best_tau is None:
        raise ValueError(f"empty interior for endpoint pair ({p}, {q})")
    return best_w, best_tau


def next_prime_square_after_witness(tau: array, w: int) -> int:
    root = isqrt(w) + 1
    while root < len(tau):
        if tau[root] == 2:
            square = root * root
            if square < len(tau):
                return square
            break
        root += 1
    raise ValueError(f"tau table ended before next prime square after {w}")


def residual_rows(max_n: int) -> tuple[list[dict[str, int]], int]:
    square_ceiling_root_limit = max_n + 1000
    limit = square_ceiling_root_limit * square_ceiling_root_limit
    tau = build_tau(limit)
    rows: list[dict[str, int]] = []

    for n in range(2, max_n + 1):
        left_square = n * n
        right_square = (n + 1) * (n + 1)
        p = previous_endpoint(tau, left_square)
        q = next_endpoint(tau, left_square)
        w, witness_tau = selected_witness(tau, p, q)
        square_ceiling = next_prime_square_after_witness(tau, w)

        if witness_tau != 4:
            continue
        if w >= left_square:
            continue
        if tau[n] == 2 or tau[n + 1] == 2:
            continue
        if square_ceiling <= right_square:
            continue

        chamber_width = right_square - left_square
        endpoint_offset = q - left_square
        last_tail_d4 = 0
        tail_d4_count = 0
        for x in range(left_square + 1, q):
            if tau[x] == 4:
                tail_d4_count += 1
                last_tail_d4 = x

        rows.append(
            {
                "n": n,
                "p": p,
                "q": q,
                "w": w,
                "left_square": left_square,
                "right_square": right_square,
                "witness_tau": witness_tau,
                "square_ceiling": square_ceiling,
                "chamber_width": chamber_width,
                "endpoint_offset": endpoint_offset,
                "quarter_slack": chamber_width - 4 * endpoint_offset,
                "right_margin": right_square - q,
                "tail_d4_count": tail_d4_count,
                "last_tail_d4": last_tail_d4,
                "q_minus_last_tail_d4": q - last_tail_d4 if last_tail_d4 else 0,
            }
        )

    return rows, limit


def summarize(rows: list[dict[str, int]], max_n: int, limit: int) -> dict[str, object]:
    violations = [row for row in rows if row["quarter_slack"] <= 0]
    crossings = [row for row in rows if row["q"] >= row["right_square"]]
    no_tail_d4 = [row for row in rows if row["tail_d4_count"] == 0]
    max_fraction_row = max(
        rows,
        key=lambda row: row["endpoint_offset"] / row["chamber_width"],
        default=None,
    )
    max_offset_row = max(rows, key=lambda row: row["endpoint_offset"], default=None)
    min_right_margin_row = min(rows, key=lambda row: row["right_margin"], default=None)
    max_tail_gap_row = max(
        (row for row in rows if row["tail_d4_count"] > 0),
        key=lambda row: row["q_minus_last_tail_d4"],
        default=None,
    )

    return {
        "status": "ADVANCE",
        "probe": "selected-d4 composite-boundary residual endpoint quarter",
        "max_n": max_n,
        "tau_limit": limit,
        "chambers_checked": max_n - 1,
        "residual_rows": len(rows),
        "square_crossing_residual_rows": len(crossings),
        "endpoint_quarter_violations": len(violations),
        "tail_d4_absent_rows": len(no_tail_d4),
        "tail_d4_present_rows": len(rows) - len(no_tail_d4),
        "max_endpoint_fraction_row": max_fraction_row,
        "max_endpoint_offset_row": max_offset_row,
        "min_right_margin_row": min_right_margin_row,
        "max_q_minus_last_tail_d4_row": max_tail_gap_row,
        "theorem_obligation": (
            "For every selected-d4 composite-boundary residual row, prove "
            "4 * (q - n^2) < 2n + 1."
        ),
    }


def write_outputs(rows: list[dict[str, int]], summary: dict[str, object], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "2026-05-20-residual-endpoint-quarter-summary.json"
    frontier_path = out_dir / "2026-05-20-residual-endpoint-quarter-frontier.csv"

    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    frontier = sorted(
        rows,
        key=lambda row: (
            row["endpoint_offset"] / row["chamber_width"],
            row["endpoint_offset"],
            -row["n"],
        ),
        reverse=True,
    )[:40]
    fieldnames = [
        "n",
        "p",
        "q",
        "w",
        "left_square",
        "right_square",
        "square_ceiling",
        "chamber_width",
        "endpoint_offset",
        "quarter_slack",
        "right_margin",
        "tail_d4_count",
        "last_tail_d4",
        "q_minus_last_tail_d4",
    ]
    with frontier_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in frontier:
            writer.writerow({field: row[field] for field in fieldnames})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5000)
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    if args.max_n < 2:
        raise ValueError("--max-n must be at least 2")

    rows, limit = residual_rows(args.max_n)
    summary = summarize(rows, args.max_n, limit)
    write_outputs(rows, summary, args.out_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
