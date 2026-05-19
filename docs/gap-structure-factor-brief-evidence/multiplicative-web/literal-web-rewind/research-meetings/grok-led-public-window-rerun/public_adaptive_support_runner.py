#!/usr/bin/env python3
"""Public-only adaptive support runner for the sparse-window v2 rerun.

Contract:
- Receives only N and public policy constants.
- Uses the public threads (2, 3, 5).
- Expands through a fixed public radius schedule.
- Ranks offsets by public support count, then proximity.
- Emits only public data.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PUBLIC_OUT_ROOT = HERE / "output" / "public_adaptive_support_v2"

PUBLIC_THREADS: tuple[int, ...] = (2, 3, 5)
PUBLIC_RADII: tuple[int, ...] = (
    1 << 8,
    1 << 10,
    1 << 12,
    1 << 14,
    1 << 16,
    1 << 18,
    1 << 20,
    1 << 21,
)
PUBLIC_TOP_K: int = 100


def congruent_offsets(n: int, r: int, radius: int) -> list[int]:
    """Return public offsets t with N + t divisible by r."""
    res = (-n) % r
    t0 = res if res != 0 else r
    out: list[int] = []

    t = t0
    while t <= radius:
        out.append(t)
        t += r

    t = t0 - r
    while t >= -radius:
        if t != 0:
            out.append(t)
        t -= r

    return out


def nominate_at_radius(n: int, radius: int, threads: tuple[int, ...], top_k: int) -> dict[str, Any]:
    started = time.perf_counter()
    support: dict[int, list[int]] = {}
    generator_steps = 0

    for r in threads:
        for t in congruent_offsets(n, r, radius):
            generator_steps += 1
            value = n + t
            if value < 4:
                continue
            support.setdefault(t, []).append(r)

    ranked = []
    for t, rs in support.items():
        ranked.append({
            "offset": t,
            "value": n + t,
            "support_count": len(rs),
            "threads": rs,
        })

    ranked.sort(key=lambda item: (-item["support_count"], abs(item["offset"]), item["offset"]))
    elapsed = time.perf_counter() - started

    return {
        "R": radius,
        "top_nominated": ranked[:top_k],
        "nominated_count": len(ranked),
        "cost": {
            "generator_steps": generator_steps,
            "unique_nominated_within_R": len(ranked),
            "top_k_emitted": min(top_k, len(ranked)),
            "elapsed_seconds": round(elapsed, 6),
        },
    }


def public_adaptive_nominate(
    n: int,
    radii: tuple[int, ...] | None = None,
    threads: tuple[int, ...] | None = None,
    top_k: int | None = None,
) -> dict[str, Any]:
    if n < 4:
        raise ValueError("N must be >= 4")
    if radii is None:
        radii = PUBLIC_RADII
    if threads is None:
        threads = PUBLIC_THREADS
    if top_k is None:
        top_k = PUBLIC_TOP_K

    attempts = [nominate_at_radius(n, radius, threads, top_k) for radius in radii]

    return {
        "policy": "adaptive_support_v2",
        "N": n,
        "N_bits": n.bit_length(),
        "threads": list(threads),
        "radii": list(radii),
        "top_k": top_k,
        "attempts": attempts,
        "public_only": True,
    }


def write_public_result(n: int, case_name: str, result: dict[str, Any]) -> Path:
    case_dir = PUBLIC_OUT_ROOT / case_name
    case_dir.mkdir(parents=True, exist_ok=True)
    out_path = case_dir / "public_result.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    test_ns = [
        (713, "public_N_10bit_01"),
        (2537, "public_N_12bit_01"),
        (5063, "public_N_13bit_01"),
        (10057, "public_N_14bit_01"),
        (18905157503, "public_N_35bit_01"),
        (1209478624103, "public_N_41bit_01"),
    ]
    PUBLIC_OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for n, name in test_ns:
        result = public_adaptive_nominate(n)
        path = write_public_result(n, name, result)
        final = result["attempts"][-1]
        print(
            f"{name}: wrote {path}; final_R={final['R']}; "
            f"nominated={final['nominated_count']}; top_k={result['top_k']}"
        )


if __name__ == "__main__":
    main()
