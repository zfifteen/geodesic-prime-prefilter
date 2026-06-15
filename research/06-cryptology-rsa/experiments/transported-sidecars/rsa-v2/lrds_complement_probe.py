#!/usr/bin/env python3
"""Minimal LRDS (Lag-Reduced Divisor Signature) complement probe for RSA v2.

Implements the falsification probe proposed in the Hermes + Grok bus collaboration
for the LRDS hypothesis.

Focus: for reciprocal certificate pairs (lower/upper), compute a basic LRDS
as the first few d=4 positions relative to carrier_w (GWR w) and reset_endpoint
in the relevant window, using the existing divisor_counts_segment.

Then measure whether "resolved" rungs (bits 40, 64) show different LRDS
characteristics (e.g. d4 count between w and reset, or relative signatures)
compared to unresolved (50) or general ledger rows.

PGS-first: uses only divisor-count field around the GWR-selected w and
reset_endpoint from the structural certificate, under reciprocal transport
context. No classical search, no primality, etc.

Run:
  python3 research/06-cryptology-rsa/experiments/transported-sidecars/rsa-v2/lrds_complement_probe.py

Outputs sidecar summary + optional rows with lrds info.
State: hypothesis + probe; will emit measured rates or invalidation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_SURVIVOR_ROWS = (
    ROOT
    / "research"
    / "06-cryptology-rsa"
    / "experiments"
    / "live-solver"
    / "rsa-v2"
    / "output"
    / "survivor_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "lrds_complement_current"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def int_or_none(v):
    if v is None:
        return None
    try:
        return int(str(v))
    except Exception:
        return None


def d4_in_window(lo: int, hi: int) -> list[int]:
    """d=4 coordinates in [lo, hi] inclusive, using existing segment tool."""
    if hi <= lo:
        return []
    counts = divisor_counts_segment(lo, hi + 1)
    return [lo + i for i, c in enumerate(counts) if int(c) == 4]


def lrds_basic(w: int | None, r: int | None, window: int = 4096) -> dict[str, object]:
    """Basic LRDS signature around GWR w (carrier_w) and reset_endpoint r.

    Returns count of d4 strictly between w and r (if w < r), and first 3
    relative offsets from w in the window [w-window, r+window].
    This is a starting operationalization of the "canonical tuple of relative
    d=4 positions ... around ... w and the reset_endpoint (DNI-normalized)".
    """
    if w is None or r is None:
        return {"num_d4_between": None, "rel_d4_from_w": [], "window": window}

    lo = min(w, r) - window
    hi = max(w, r) + window
    d4s = d4_in_window(lo, hi)

    between = [p for p in d4s if min(w, r) < p < max(w, r)]
    num_between = len(between)

    # Relative to w, the ones "around" the segment
    rel = sorted([p - w for p in d4s if abs(p - w) < window or abs(p - r) < window])[:3]

    return {
        "num_d4_between_w_r": num_between,
        "first_rel_d4_from_w": rel,
        "w": int(w),
        "r": int(r),
        "window": window,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--survivor-rows", type=Path, default=DEFAULT_SURVIVOR_ROWS)
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = read_jsonl(args.survivor_rows)
    print(f"Loaded {len(rows)} survivor rows")

    by_bits: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        bits = int_or_none(row.get("bits"))
        if bits in (40, 50, 64):
            by_bits[bits].append(row)

    summaries = {}
    all_lrds_rows = []

    for bits, group in sorted(by_bits.items()):
        lrds_list = []
        for row in group:
            lw = int_or_none(row.get("lower_carrier_w"))
            lr = int_or_none(row.get("lower_reset_endpoint"))
            uw = int_or_none(row.get("upper_carrier_w"))
            ur = int_or_none(row.get("upper_reset_endpoint"))

            lrds_l = lrds_basic(lw, lr)
            lrds_u = lrds_basic(uw, ur)
            lrds_list.append(
                {
                    "N": str(row.get("N")),
                    "bits": bits,
                    "closure_status": row.get("closure_status"),
                    "lower_lrds": lrds_l,
                    "upper_lrds": lrds_u,
                }
            )

        num_between_lower = [
            x["lower_lrds"]["num_d4_between_w_r"]
            for x in lrds_list
            if x["lower_lrds"]["num_d4_between_w_r"] is not None
        ]
        avg_lower = sum(num_between_lower) / len(num_between_lower) if num_between_lower else None

        summaries[bits] = {
            "count": len(group),
            "avg_d4_between_lower_w_r": avg_lower,
            "sample_rel_d4_lower": [x["lower_lrds"]["first_rel_d4_from_w"] for x in lrds_list[:2]],
        }
        all_lrds_rows.extend(lrds_list)

    # Write sidecar
    summary_path = args.output_dir / "lrds_summary.json"
    write_json(
        summary_path,
        {
            "rule_id": "lrds_complement_v0_probe",
            "source": str(args.survivor_rows),
            "by_bits": summaries,
            "note": "LRDS hypothesis probe. num_d4_between_w_r and rel offsets for lower/upper. Resolved rungs (40/64) vs 50. See collab artifact for full hypothesis.",
        },
    )

    rows_path = args.output_dir / "lrds_rows.jsonl"
    with rows_path.open("w", encoding="utf-8", newline="\n") as f:
        for r in all_lrds_rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    print("LRDS probe summary:")
    for b, s in summaries.items():
        print(f"  bits={b}: n={s['count']}, avg_d4_between_lower={s['avg_d4_between_lower_w_r']}")

    print(f"\nWrote {summary_path}")
    print(f"Wrote {rows_path}")
    print("State: measured on this surface (the 3 static rungs + other survivors in file).")
    print("For full 48 solved grammar rows + 512 story law, extend with grammar output loader.")
    print("Hypothesis remains unresolved until differential rates or complement signal is clear and replicated.")


if __name__ == "__main__":
    main()