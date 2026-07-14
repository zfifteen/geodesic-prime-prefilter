"""Small pure-Python helpers and fixture loaders for demos.

These helpers compute divisor counts on tiny toy integers for teaching plots.
They are not PGS inference mechanisms and must not be used as generator logic.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .paths import FIXTURES_DIR


def divisor_count(n: int) -> int:
    """Exact divisor count for a positive integer (toy demo helper only)."""
    if n < 1:
        raise ValueError("n must be positive")
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            count += 1 if i * i == n else 2
        i += 1
    return count


def zero_excess_e(n: int, d: int | None = None) -> float:
    """E(n) = (d(n)/2 - 1) * ln n  (DNI zero-excess coordinate)."""
    if n <= 1:
        return float("nan")
    dd = divisor_count(n) if d is None else d
    return (dd / 2.0 - 1.0) * math.log(n)


def gwr_witness(p: int, q: int) -> tuple[int, int]:
    """Leftmost interior integer with minimum divisor count (GWR selection).

    Returns (w, d(w)). Requires q > p + 1 (nonempty interior).
    """
    if q <= p + 1:
        raise ValueError("gap interior is empty")
    best_n = p + 1
    best_d = divisor_count(best_n)
    for n in range(p + 2, q):
        d = divisor_count(n)
        if d < best_d:
            best_d = d
            best_n = n
    return best_n, best_d


def load_exemplar_gaps() -> list[dict[str, Any]]:
    path = FIXTURES_DIR / "exemplars" / "gaps.json"
    with path.open(encoding="utf-8") as fh:
        payload = json.load(fh)
    return list(payload["gaps"])


def load_json_fixture(relative: str) -> Any:
    path = FIXTURES_DIR / relative
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def materialize_gap_field(p: int, q: int) -> dict[str, Any]:
    """Build a full interior field for one known prime gap (toy)."""
    values = list(range(p, q + 1))
    ds = [divisor_count(n) for n in values]
    es = [0.0 if d == 2 else zero_excess_e(n, d) for n, d in zip(values, ds)]
    if q > p + 1:
        w, wd = gwr_witness(p, q)
    else:
        w, wd = p, 2
    return {
        "p": p,
        "q": q,
        "values": values,
        "divisors": ds,
        "excess": es,
        "w": w,
        "w_d": wd,
        "gap": q - p,
        "offset": w - p,
    }
