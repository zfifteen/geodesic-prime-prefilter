#!/usr/bin/env python3
"""Public adaptive window plus adaptive thread alphabet runner.

The runner receives only N and public policy constants. Each rung increases
both the public radius and the public small-prime thread prefix. Ranking uses
only the observed thread signature inside that public window.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from public_alphabet_policy import (
    PUBLIC_RADII,
    PUBLIC_THREAD_PREFIXES,
    PUBLIC_TOP_K,
    ranked_offsets_at_rung,
)

HERE = Path(__file__).resolve().parent
PUBLIC_OUT_ROOT = HERE / "output" / "public_adaptive_alphabet_v3"


def public_adaptive_alphabet_nominate(n: int, top_k: int | None = None) -> dict[str, Any]:
    if n < 4:
        raise ValueError("N must be >= 4")
    if top_k is None:
        top_k = PUBLIC_TOP_K

    attempts = [
        ranked_offsets_at_rung(n, radius, threads, top_k)
        for radius, threads in zip(PUBLIC_RADII, PUBLIC_THREAD_PREFIXES)
    ]

    return {
        "policy": "adaptive_alphabet_signature_rarity_v3",
        "N": n,
        "N_bits": n.bit_length(),
        "radii": list(PUBLIC_RADII),
        "thread_prefixes": [list(threads) for threads in PUBLIC_THREAD_PREFIXES],
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
    public_inputs = [
        (713, "public_N_10bit_01"),
        (2537, "public_N_12bit_01"),
        (5063, "public_N_13bit_01"),
        (10057, "public_N_14bit_01"),
        (18905157503, "public_N_35bit_01"),
        (1209478624103, "public_N_41bit_01"),
    ]
    PUBLIC_OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for n, name in public_inputs:
        result = public_adaptive_alphabet_nominate(n)
        path = write_public_result(n, name, result)
        final = result["attempts"][-1]
        print(
            f"{name}: wrote {path}; final_R={final['R']}; "
            f"threads={final['thread_count']}; nominated={final['nominated_count']}"
        )


if __name__ == "__main__":
    main()
