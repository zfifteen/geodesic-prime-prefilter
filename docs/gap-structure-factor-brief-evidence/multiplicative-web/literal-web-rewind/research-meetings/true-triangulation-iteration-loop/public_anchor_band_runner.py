#!/usr/bin/env python3
"""Public anchor-confirmed band-output runner.

This is the post-loop test implied by iteration 10. It keeps the learned public
selector and widens band-local output. The runner receives only N.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_loop_policy import public_nominate

HERE = Path(__file__).resolve().parent
PUBLIC_OUT_ROOT = HERE / "output" / "anchor_band_expansion_public"

SPEC: dict[str, Any] = {
    "iteration": 11,
    "radius": 2097152,
    "small_primes": [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
    "residual_limit": 1,
    "score_mode": "anchor_confirmed",
    "band_width": 32768,
    "top_per_band": 2500,
    "top_k": 160000,
}


def compact_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "distance": row["distance"],
        "score": row["score"],
        "left_source_count": row["left_source_count"],
        "right_source_count": row["right_source_count"],
        "shared_thread_count": row["shared_thread_count"],
        "union_thread_count": row["union_thread_count"],
    }


def public_anchor_band_nominate(n: int) -> dict[str, Any]:
    public = public_nominate(n, SPEC)
    return {
        "policy": "anchor_confirmed_band_expansion",
        "N": public["N"],
        "N_bits": public["N_bits"],
        "radius": public["radius"],
        "small_primes": public["small_primes"],
        "residual_limit": public["residual_limit"],
        "score_mode": public["score_mode"],
        "band_width": public["band_width"],
        "top_per_band": public["top_per_band"],
        "top_k": public["top_k"],
        "top_distances": [compact_row(row) for row in public["top_distances"]],
        "public_cost": public["public_cost"],
        "public_only": True,
    }


def write_public_result(n: int, case_name: str) -> Path:
    result = public_anchor_band_nominate(n)
    out_dir = PUBLIC_OUT_ROOT / case_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "public_result.json"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_path


def main() -> None:
    public_inputs = [
        (713, "public_N_10bit_01"),
        (2537, "public_N_12bit_01"),
        (5063, "public_N_13bit_01"),
        (10057, "public_N_14bit_01"),
        (18905157503, "public_N_35bit_01"),
        (1209478624103, "public_N_41bit_01"),
    ]
    for n, name in public_inputs:
        path = write_public_result(n, name)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
