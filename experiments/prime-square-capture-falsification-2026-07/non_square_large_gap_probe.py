#!/usr/bin/env python3
"""Probe non-square gaps with unusually large width (compositeness proxy).

Falsification target: if very wide gaps without interior prime squares achieve
GWR offsets comparable to square-branch extremes, the decoupling claim fails.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIELD_DIR = ROOT / "src" / "python"
if str(FIELD_DIR) not in sys.path:
    sys.path.insert(0, str(FIELD_DIR))

from z_band_prime_predictor.gwr_boundary_walk import gwr_next_gap_profile  # noqa: E402


def dynamic_cutoff(q: int) -> int:
    return max(64, math.ceil(0.5 * math.log(q) ** 2))


def load_large_gaps(csv_path: Path, min_gap: int = 200) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    with csv_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            gap = int(row["gap_size"])
            if gap >= min_gap:
                rows.append({"p": int(row["gap_start"]), "gap": gap})
    rows.sort(key=lambda item: -item["gap"])
    return rows[:80]


def has_interior_prime_square(p: int, q: int) -> bool:
    r = math.isqrt(p) + 1
    return r * r < q


def main() -> None:
    csv_path = ROOT / "data/external/primegap_list_records_1e12_1e18.csv"
    out_dir = Path("experiments/prime-square-capture-falsification-2026-07")
    candidates = load_large_gaps(csv_path)

    # We cannot sieve 10^12 interiors; use honest square-presence prefilter only.
    without_square = [g for g in candidates if not has_interior_prime_square(g["p"], g["p"] + g["gap"])]

    summary = {
        "note": "Large-gap list used for width/compositeness proxy only; interior tau unavailable at scale.",
        "candidates_tested": len(candidates),
        "wide_gaps_without_interior_prime_square": len(without_square),
        "widest_without_square": without_square[:10],
        "interpretation": (
            "At 10^12+ scales, gaps wider than 200 exist without landing an interior "
            "prime square (square root of left endpoint exceeds gap width). "
            "These are natural falsification targets for decoupling once interior "
            "divisor data is available; on the external list alone we cannot read GWR offset."
        ),
    }
    (out_dir / "non_square_large_gap_probe.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()